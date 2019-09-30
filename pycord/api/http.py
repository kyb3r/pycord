import sys
import time
from collections import defaultdict
from urllib.parse import quote

import anyio
import asks

from .. import __version__, __github__
from ..utils import API, run_later, encoder, decoder, id_now
from ..models.errors import HttpError


class HoldableLock:
    __slots__ = ('lock', 'unlock')

    def __init__(self, lock):
        self.unlock, self.lock = True, lock

    def hold(self):
        self.unlock = False

    async def __aenter__(self):
        await self.lock.acquire()
        return self

    async def __aexit__(self, *args):
        if self.unlock:
            rel = self.lock.release()
            if rel is not None:
                await rel


class GlobalLock:
    __slots__ = ('global_event', 'is_global')

    def __init__(self, global_event, is_global):
        self.is_global = is_global
        self.global_event = global_event

    async def __aenter__(self):
        if self.is_global:
            self.global_event.clear()

    async def __aexit__(self, *args):
        if self.is_global:
            await self.global_event.set()


class HttpClient:
    def __init__(self, client):
        self.client = client
        self.token = client.token
        self.retries = 5
        self.buckets = defaultdict(anyio.create_lock)
        self.global_event = anyio.create_event()

        # set global lock and create user agent
        user_agent = 'DiscordBot ({0} {1}) Python/{2[0]}.{2[1]}'
        self.user_agent = user_agent.format(
            __github__, __version__, sys.version_info)

        token = 'Bot {.token}'.format(self) if self.client.is_bot else self.token

        headers = {
            "Authorization": token,
            "User-Agent": self.user_agent
        }

        self.session = asks.Session(headers=headers)

    def __del__(self):
        pass

    async def get(self, endpoint, **kwargs):
        """ Helper function for GET request """
        return await self.request('GET', endpoint, **kwargs)

    async def put(self, endpoint, **kwargs):
        """ Helper function for PUT request """
        return await self.request('PUT', endpoint, **kwargs)

    async def post(self, endpoint, **kwargs):
        """ Helper function for POST request """
        return await self.request('POST', endpoint, **kwargs)

    async def patch(self, endpoint, **kwargs):
        """ Helper function for PATCH request """
        return await self.request('PATCH', endpoint, **kwargs)

    async def delete(self, endpoint, **kwargs):
        """ Helper function for DELETE request """
        return await self.request('DELETE', endpoint, **kwargs)

    async def request(self, method, endpoint, **kwargs):
        """ Perform an HTTP request with rate limiting """
        method = method
        endpoint = endpoint
        bucket = "{}.{}".format(method, endpoint)
        endpoint = API.HTTP_ENDPOINT + endpoint

        lock = self.buckets[bucket]

        token = 'Bot {.token}'.format(self) if self.client.is_bot else self.token
        # create headers
        headers = {'User-Agent': self.user_agent}
        if self.token is not None:
            headers['Authorization'] = token
        if kwargs.get('reason'):
            headers['X-Audit-Log-Reason'] = quote(kwargs.get('reason'), safe='/ ')

        # get data
        data = kwargs.get('data')
        if data is not None:
            if isinstance(data, dict):
                data = encoder(data)
            if isinstance(data, str):
                data = data.encode('utf-8')

            headers['Content-Type'] = 'application/json'

        _json = kwargs.get('json')

        # check if global rate limited
        if self.global_event.is_set():
            await self.global_event.wait()

        # open http request with retries
        async with HoldableLock(lock) as hold_lock:
            async with anyio.create_task_group() as nursery:
                for tries in range(self.retries):
                    resp = await self.session.request(method, endpoint, headers=headers, data=data, json=_json)

                    # get response and header data
                    data = resp.text
                    if 'application/json' in resp.headers['content-type']:
                        data = decoder(data)
                    remaining = resp.headers.get('X-Ratelimit-Remaining', 0)

                    # check if route should be rate limited
                    if remaining == '0' and resp.status_code != 429:
                        hold_lock.hold()
                        delay = int(resp.headers.get('X-Ratelimit-Reset')) - time.time()
                        await nursery.spawn(run_later, delay, lock.release())

                    # check if route IS rate limited
                    elif resp.status_code == 429:
                        async with GlobalLock(self.global_event, data.get('global', False)):

                            # wait for rate limit delay delay
                            retry_after = data.get('retry-after', 0)
                            await anyio.sleep(retry_after / 1000.0)

                        # retry request
                        continue

                    # return response data
                    if 300 > resp.status_code >= 200:
                        return data or None

                    # forbidden path
                    elif resp.status_code == 403:
                        raise HttpError(resp, data)

                    # path not found
                    elif resp.status_code == 404:
                        raise HttpError(resp, data)

                    # service is down, wait a bit and retry later
                    elif resp.status_code in (500, 502):
                        await anyio.sleep(1 + tries * 2)
                        continue

                    # unknown http error
                    else:
                        raise HttpError(resp, data)

        # retries have been exhausted
        raise Exception("Failed HTTP Request: {.status_code} {} {}".format(resp, method, endpoint))

    async def send_message(self, channel, **kwargs):
        """Send a message to a channel."""
        route = '/channels/{.id}/messages'.format(channel)
        nonce = id_now()

        payload = {
            'content': kwargs.get('content'),
            'embed': kwargs.get('embed'),
            'tts': kwargs.get('tts', False),
            'nonce': nonce,
        }

        await self.post(route, data=payload)
        await self.client.wait_for_nonce(nonce)

    def send_typing(self, channel):
        route = '/channels/{.id}/typing'.format(channel)
        return self.post(route)

    def send_files(self, channel, *, files, **kwargs):
        """Send files to a channel."""
        route = '/channels/{.id}/messages'.format(channel)

        files = dict(files)

        return self.post(route, json=kwargs, files=files)

    def start_private_message(self, user):
        payload = {
            'recipient_id': user.id
        }
        return self.post('/users/@me/channels', data=payload)

    def delete_message(self, channel, message, *, reason=None):
        route = '/channels/{.id}/messages/{.id}'.format(channel, message)
        return self.delete(route, reason=reason)

    def delete_messages(self, channel, messages, *, reason=None):
        route = '/channels/{.id}/messages/bulk_delete'.format(channel)
        payload = {
            'messages': [m.id for m in messages]
        }

        return self.post(route, data=payload, reason=reason)

    def edit_message(self, channel, message, **fields):
        route = '/channels/{.id}/messages/{.id}'.format(channel, message)
        return self.patch(route, data=fields)

    def add_reaction(self, channel, message, emoji):
        route = '/channels/{.id}/messages/{.id}/reactions/{}/@me'.format(channel, message, emoji)
        # emoji in format 'name:id'
        return self.put(route)

    def remove_reaction(self, channel, message, emoji, member_id):
        route = '/channels/{.id}/messages/{.id}/reactions/{}/{}'.format(channel, message, emoji, member_id)
        return self.delete(route)

    def get_reaction_users(self, channel, message, emoji, limit, after=None):
        route = '/channels/{.id}/messages/{.id}/reactions/{}'.format(channel, message, emoji),

        params = {
            'limit': limit,
            'after': after
        }

        return self.get(route, params=params)

    def clear_reactions(self, channel, message):
        route = '/channels/{.id}/messages/{.id}/reactions'.format(channel, message),

        return self.delete(route)

    def get_message(self, channel, message):
        route = '/channels/{.id}/messages/{.id}'.format(channel, message)
        return self.get(route)

    def logs_from(self, channel, limit, before=None, after=None, around=None):
        route = '/channels/{.id}/messages'.format(channel)

        params = {
            'limit': limit,
            'before': before,
            'after': after,
            'around': around
        }

        return self.get(route, params=params)

    def pin_message(self, channel, message):
        return self.put('/channels/{.id}/pins/{.id}'.format(channel, message))

    def unpin_message(self, channel, message):
        return self.delete('/channels/{.id}/pins/{.id}'.format(channel, message))

    def pins_from(self, channel):
        return self.get('/channels/{.id}/pins'.format(channel))

    def start_group(self, user, recipients):
        route = '/users/{.id}/channels'.format(user)

        payload = {
            'recipients': [r.id for r in recipients]
        }

        return self.post(route, data=payload)

    def leave_group(self, channel):
        return self.delete('/channels/{.id}'.format(channel))

    def add_group_recipient(self, channel, user):
        route = '/channels/{.id}/recipients/{.id}'.format(channel, user)
        return self.put(route)

    def remove_group_recipient(self, channel, user):
        route = '/channels/{.id}/recipients/{.id}'.format(channel, user)
        return self.delete(route)

    def edit_group(self, channel, *, name=None, icon=None):
        route = '/channels/{.id}'.format(channel)

        payload = {
            'name': name,
            'icon': icon
        }

        return self.patch(route, data=payload)

    def convert_group(self, channel):
        return self.post('/channels/{.id}/convert'.format(channel))

    def edit_channel(self, channel, *, reason=None, **options):
        route = '/channels/{.id}'.format(channel)

        valid_keys = ('name', 'topic', 'bitrate', 'nsfw', 'user_limit', 'position', 'permission_overwrites')
        payload = {
            k: v for k, v in options.items() if k in valid_keys
        }
        return self.patch(route, reason=reason, json=payload)

    def bulk_channel_update(self, guild, data, *, reason=None):
        r = '/guilds/{.id}/channels'.format(guild)
        return self.patch(r, json=data, reason=reason)

    def create_channel(self, guild, name, channel_type, permission_overwrites=None, *, reason=None):
        route = '/guilds/{.id}/channels'.format(guild)

        payload = {
            'name': name,
            'type': channel_type
        }

        if permission_overwrites is not None:
            payload['permission_overwrites'] = permission_overwrites

        return self.post(route, json=payload, reason=reason)

    def delete_channel(self, channel, *, reason=None):
        return self.delete('/channels/{.id}'.format(channel), reason=reason)

    def kick(self, member, guild, reason=None):
        route = '/guilds/{.id}/members/{.id}'.format(guild, member)
        if reason:
            route += '?reason={}'.format(quote(reason))
        return self.delete(route)

    def ban(self, member, guild, delete_message_days=1, reason=None):
        route = '/guilds/{.id}/bans/{.id}'.format(guild, member)
        params = {
            'delete-message-days': delete_message_days,
        }
        if reason:
            route += '?reason={}'.format(quote(reason))

        return self.put(route, params=params)

    def unban(self, member, guild, *, reason=None):
        route = '/guilds/{.id}/bans/{.id}'.format(guild, member)
        return self.delete(route, reason=reason)

    def guild_voice_state(self, member, guild, *, mute=None, deafen=None, reason=None):
        route = '/guilds/{.id}/members/{.id}'.format(guild, member)
        payload = {}
        if mute is not None:
            payload['mute'] = mute
        if deafen is not None:
            payload['deaf'] = deafen

        return self.patch(route, json=payload, reason=reason)

    def edit_profile(self, password, username, avatar, **kwargs):
        payload = {
            'password': password,
            'username': username,
            'avatar': avatar
        }
        if 'email' in kwargs:
            payload['email'] = kwargs['email']

        if 'new_password' in kwargs:
            payload['new_password'] = kwargs['new_password']

        return self.patch('/users/@me', json=payload)

    def change_my_nickname(self, guild, nickname, *, reason=None):
        route = '/guilds/{.id}/members/@me/nick'.format(guild)
        payload = {
            'nick': nickname
        }
        return self.patch(route, json=payload, reason=reason)

    def change_nickname(self, guild, member, nickname, *, reason=None):
        route = '/guilds/{.id}/members/{.id}'.format(guild, member)
        payload = {
            'nick': nickname
        }
        return self.patch(route, json=payload, reason=reason)

    def edit_member(self, guild, member, *, reason=None, **fields):
        route = '/guilds/{.id}/members/{.id}'.format(guild, member)
        return self.patch(route, json=fields, reason=reason)

    def application_info(self):
        return self.get('/oauth2/applications/@me')

    def get_user_info(self, user_id):
        return self.get('/users/{}'.format(user_id))

    def get_user_profile(self, user_id):
        return self.get('/users/{}/profile'.format(user_id))

    def remove_relationship(self, user):
        return self.delete('/users/@me/relationships/{.id}'.format(user))

    def add_relationship(self, user_id, type_=None):
        payload = {}
        route = '/users/@me/relationships/{}'.format(user_id)

        if type_ is not None:
            payload = {'type': type_}

        return self.put(route, json=payload)

    def send_friend_request(self, username, discriminator):
        payload = {
            'username': username,
            'discriminator': int(discriminator)
        }
        return self.post('/users/@me/relationships', json=payload)

    def create_webhook(self, channel, *, name=None, avatar=None):
        route = '/channels/{.id}/webhooks'.format(channel)

        payload = {}
        if name is not None:
            payload['name'] = name
        if avatar is not None:
            payload['avatar'] = avatar

        return self.post(route, json=payload)

    def channel_webhooks(self, channel):
        return self.get('/channels/{.id}/webhooks'.format(channel))

    def guild_webhooks(self, guild):
        return self.get('/guilds/{.id}/webhooks'.format(guild))

    def get_webhook(self, webhook):
        return self.get('/webhooks/{.id}'.format(webhook))

    def leave_guild(self, guild):
        return self.delete('/users/@me/guilds/{.id}'.format(guild))

    def delete_guild(self, guild):
        return self.delete('/guilds/{.id}'.format(guild))

    def create_guild(self, name, region, icon):
        payload = {
            'name': name,
            'icon': icon,
            'region': region
        }
        return self.post('/guilds', json=payload)

    def edit_guild(self, guild, *, reason=None, **fields):
        valid_keys = ('name', 'region', 'icon', 'afk_timeout', 'owner_id',
                      'afk_channel_id', 'splash', 'verification_level',
                      'system_channel_id')

        payload = {
            k: v for k, v in fields.items() if k in valid_keys
        }

        return self.patch('/guilds/{.id}'.format(guild), json=payload, reason=reason)

    def get_bans(self, guild):
        return self.get('/guilds/{.id}/bans'.format(guild))

    def get_vanity_code(self, guild):
        return self.get('/guilds/{.id}/vanity-url'.format(guild))

    def change_vanity_code(self, guild, code, *, reason=None):
        payload = {'code': code}
        return self.patch('/guilds/{.id}/vanity-url'.format(guild), json=payload, reason=reason)

    def prune_members(self, guild, days, *, reason=None):
        params = {
            'days': days
        }
        return self.post('/guilds/{.id}/prune'.format(guild), params=params, reason=reason)

    def estimate_pruned_members(self, guild, days):
        params = {
            'days': days
        }
        return self.get('/guilds/{.id}/prune'.format(guild), params=params)

    def create_custom_emoji(self, guild, name, image, *, reason=None):
        payload = {
            'name': name,
            'image': image
        }

        return self.post('/guilds/{.id}/emojis'.format(guild), json=payload, reason=reason)

    def delete_custom_emoji(self, guild, emoji, *, reason=None):
        return self.delete('/guilds/{.id}/emojis/{.id}'.format(guild, emoji), reason=reason)

    def edit_custom_emoji(self, guild, emoji, *, name, reason=None):
        payload = {
            'name': name
        }
        route = '/guilds/{.id}/emojis/{.id}'.format(guild, emoji)
        return self.patch(route, json=payload, reason=reason)

    def get_audit_logs(self, guild, limit=100, before=None, after=None, user_id=None, action_type=None):
        params = {'limit': limit}
        if before:
            params['before'] = before
        if after:
            params['after'] = after
        if user_id:
            params['user_id'] = user_id
        if action_type:
            params['action_type'] = action_type

        return self.get('/guilds/{.id}/audit-logs'.format(guild), params=params)

    def create_invite(self, channel, *, reason=None, **kwargs):

        payload = {
            'max_age': kwargs.get('max_age', 0),
            'max_uses': kwargs.get('max_uses', 0),
            'temporary': kwargs.get('temporary', False),
            'unique': kwargs.get('unique', True)
        }

        return self.post('/channels/{.id}/invites'.format(channel), reason=reason, json=payload)

    def get_invite(self, invite_id):
        return self.get('/invite/{}'.format(invite_id))

    def invites_from(self, guild):
        return self.get('/guilds/{.id}/invites'.format(guild))

    def invites_from_channel(self, channel):
        return self.get('/channels/{.id}/invites'.format(channel))

    def delete_invite(self, invite_id, *, reason=None):
        return self.delete('/invite/{}'.format(invite_id), reason=reason)

    def edit_role(self, guild, role, *, reason=None, **fields):
        route = '/guilds/{.id}/roles/{.id}'.format(guild, role)
        valid_keys = ('name', 'permissions', 'color', 'hoist', 'mentionable')
        payload = {
            k: v for k, v in fields.items() if k in valid_keys
        }
        return self.patch(route, json=payload, reason=reason)

    def delete_role(self, guild, role, *, reason=None):
        route = '/guilds/{.id}/roles/{.id}'.format(guild, role)
        return self.delete(route, reason=reason)

    def replace_roles(self, user, guild, role_ids, *, reason=None):
        return self.edit_member(guild=guild, member=user, roles=role_ids, reason=reason)

    def create_role(self, guild, *, reason=None, **fields):
        return self.post('/guilds/{.id}/roles'.format(guild), json=fields, reason=reason)

    def move_role_position(self, guild, positions, *, reason=None):
        return self.patch('/guilds/{.id}/roles'.format(guild), json=positions, reason=reason)

    def add_role(self, guild, user, role, *, reason=None):
        route = '/guilds/{.id}/members/{.id}/roles/{.id}'.format(guild, user, role)
        return self.put(route, reason=reason)

    def remove_role(self, guild, user, role, *, reason=None):
        route = '/guilds/{.id}/members/{.id}/roles/{.id}'.format(guild, user, role)
        return self.delete(route, reason=reason)

    def edit_channel_permissions(self, channel, target, allow, deny, type, *, reason=None):
        payload = {
            'id': target,
            'allow': allow,
            'deny': deny,
            'type': type
        }
        route = '/channels/{.id}/permissions/{}'.format(channel, target)
        return self.put(route, json=payload, reason=reason)

    def delete_channel_permissions(self, channel_id, target, *, reason=None):
        route = '/channels/{}/permissions/{}'.format(channel_id, target)
        return self.delete(route, reason=reason)

    def move_member(self, user, guild, channel, *, reason=None):  # (voice)
        return self.edit_member(guild=guild, member=user, channel_id=channel.id, reason=reason)
