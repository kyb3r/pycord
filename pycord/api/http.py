"""
MIT License

Copyright (c) 2017 verixx / king1600

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys
import time
from collections import defaultdict
from urllib.parse import quote

import asks
import multio

from .. import __version__, __github__
from ..utils import API, run_later, encoder, decoder


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
            await self.lock.release()


class GlobalLock:
    __slots__ = ('global_event', 'is_global')

    def __init__(self, global_event, is_global):
        self.is_global = is_global
        self.global_event = global_event

    def __enter__(self):
        if self.is_global:
            self.global_event.clear()

    def __exit__(self, *args):
        if self.is_global:
            self.global_event.set()


class HttpClient:
    def __init__(self, client):
        self.client = client
        self.token = client.token
        self.retries = 5
        self.buckets = defaultdict(multio.Lock)
        self.global_event = multio.Event()

        # set global lock and create user agent
        user_agent = 'DiscordBot ({0} {1}) Python/{2[0]}.{2[1]}'
        self.user_agent = user_agent.format(
            __github__, __version__, sys.version_info)

        token = f'Bot {self.token}' if self.client.is_bot else self.token

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
        bucket = f"{method}.{endpoint}"
        endpoint = API.HTTP_ENDPOINT + endpoint

        lock = self.buckets[bucket]

        token = f'Bot {self.token}' if self.client.is_bot else self.token
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
            async with multio.asynclib.task_manager() as nursery:
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
                        multio.asynclib.spawn(nursery, run_later(delay, lock.release()))

                    # check if route IS rate limited
                    elif resp.status_code == 429:
                        with GlobalLock(self.global_event, data.get('global', False)):

                            # wait for rate limit delay delay
                            retry_after = data.get('retry-after', 0)
                            await multio.asynclib.sleep(retry_after / 1000.0)

                        # retry request
                        continue

                    # return response data
                    if 300 > resp.status_code >= 200:
                        return data or None

                    # forbidden path
                    elif resp.status_code == 403:
                        raise Exception(f"Forbidden: {method} {endpoint}")

                    # path not found
                    elif resp.status_code == 404:
                        raise Exception(f"Not Found: {method} {endpoint}")

                    # service is down, wait a bit and retry later
                    elif resp.status_code in (500, 502):
                        await multio.asynclib.sleep(1 + tries * 2)
                        continue

                    # unknown http error
                    else:
                        raise Exception(f"HTTP Error: {resp.status_code} {method} {endpoint}")

        # retries have been exhausted
        raise Exception(f"Failed HTTP Request: {resp.status_code} {method} {endpoint}")

    def send_message(self, channel, **kwargs):
        """Send a message to a channel."""
        route = f'/channels/{channel.id}/messages'

        payload = {
            'content': kwargs.get('content'),
            'embed': kwargs.get('embed'),
            'tts': kwargs.get('tts', False)
        }

        return self.post(route, data=payload)

    def send_typing(self, channel):
        route = f'/channels/{channel.id}/typing'
        return self.post(route)

    def send_files(self, channel, *, files, **kwargs):
        """Send files to a channel."""
        route = f'/channels/{channel.id}/messages'

        files = dict(files)

        return self.post(route, json=kwargs, files=files)

    def start_private_message(self, user):
        payload = {
            'recipient_id': user.id
        }
        return self.post('/users/@me/channels', data=payload)

    def delete_message(self, channel, message, *, reason=None):
        route = f'/channels/{channel.id}/messages/{message.id}'
        return self.delete(route, reason=reason)

    def delete_messages(self, channel, messages, *, reason=None):
        route = f'/channels/{channel.id}/messages/bulk_delete'
        payload = {
            'messages': [m.id for m in messages]
        }

        return self.post(route, data=payload, reason=reason)

    def edit_message(self, channel, message, **fields):
        route = f'/channels/{channel.id}/messages/{message.id}'
        return self.patch(route, data=fields)

    def add_reaction(self, channel, message, emoji):
        route = f'/channels/{channel.id}/messages/{message.id}/reactions/{emoji}/@me'
        # emoji in format 'name:id'
        return self.put(route)

    def remove_reaction(self, channel, message, emoji, member_id):
        route = f'/channels/{channel.id}/messages/{message.id}/reactions/{emoji}/{member_id}'
        return self.delete(route)

    def get_reaction_users(self, channel, message, emoji, limit, after=None):
        route = f'/channels/{channel.id}/messages/{message.id}/reactions/{emoji}',

        params = {
            'limit': limit,
            'after': after
        }

        return self.get(route, params=params)

    def clear_reactions(self, channel, message):
        route = f'/channels/{channel.id}/messages/{message.id}/reactions',

        return self.delete(route)

    def get_message(self, channel, message):
        route = f'/channels/{channel.id}/messages/{message.id}'
        return self.get(route)

    def logs_from(self, channel, limit, before=None, after=None, around=None):
        route = f'/channels/{channel.id}/messages'

        params = {
            'limit': limit,
            'before': before,
            'after': after,
            'around': around
        }

        return self.get(route, params=params)

    def pin_message(self, channel, message):
        return self.put(f'/channels/{channel.id}/pins/{message.id}')

    def unpin_message(self, channel, message):
        return self.delete(f'/channels/{channel.id}/pins/{message.id}')

    def pins_from(self, channel):
        return self.get(f'/channels/{channel.id}/pins')

    def start_group(self, user, recipients):
        route = f'/users/{user.id}/channels'

        payload = {
            'recipients': [r.id for r in recipients]
        }

        return self.post(route, data=payload)

    def leave_group(self, channel):
        return self.delete(f'/channels/{channel.id}')

    def add_group_recipient(self, channel, user):
        route = f'/channels/{channel.id}/recipients/{user.id}'
        return self.put(route)

    def remove_group_recipient(self, channel, user):
        route = f'/channels/{channel.id}/recipients/{user.id}'
        return self.delete(route)

    def edit_group(self, channel, *, name=None, icon=None):
        route = f'/channels/channel.id'

        payload = {
            'name': name,
            'icon': icon
        }

        return self.patch(route, data=payload)

    def convert_group(self, channel):
        return self.post(f'/channels/{channel.id}/convert')

    def edit_channel(self, channel, *, reason=None, **options):
        route = f'/channels/{channel.id}'

        valid_keys = ('name', 'topic', 'bitrate', 'nsfw', 'user_limit', 'position', 'permission_overwrites')
        payload = {
            k: v for k, v in options.items() if k in valid_keys
        }
        return self.patch(route, reason=reason, json=payload)

    def bulk_channel_update(self, guild, data, *, reason=None):
        r = f'/guilds/{guild.id}/channels'
        return self.patch(r, json=data, reason=reason)

    def create_channel(self, guild, name, channel_type, permission_overwrites=None, *, reason=None):
        route = f'/guilds/{guild.id}/channels'

        payload = {
            'name': name,
            'type': channel_type
        }

        if permission_overwrites is not None:
            payload['permission_overwrites'] = permission_overwrites

        return self.post(route, json=payload, reason=reason)

    def delete_channel(self, channel, *, reason=None):
        return self.delete(f'/channels/{channel.id}', reason=reason)

    def kick(self, member, guild, reason=None):
        route = f'/guilds/{guild.id}/members/{member.id}'
        if reason:
            route += f'?reason={quote(reason)}'
        return self.delete(route)

    def ban(self, member, guild, delete_message_days=1, reason=None):
        route = f'/guilds/{guild.id}/bans/{member.id}'
        params = {
            'delete-message-days': delete_message_days,
        }
        if reason:
            route += f'?reason={quote(reason)}'

        return self.put(route, params=params)

    def unban(self, member, guild, *, reason=None):
        route = f'/guilds/{guild.id}/bans/{member.id}'
        return self.delete(route, reason=reason)

    def guild_voice_state(self, member, guild, *, mute=None, deafen=None, reason=None):
        route = f'/guilds/{guild.id}/members/{member.id}'
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
        route = f'/guilds/{guild.id}/members/@me/nick'
        payload = {
            'nick': nickname
        }
        return self.patch(route, json=payload, reason=reason)

    def change_nickname(self, guild, member, nickname, *, reason=None):
        route = f'/guilds/{guild.id}/members/{member.id}'
        payload = {
            'nick': nickname
        }
        return self.patch(route, json=payload, reason=reason)

    def edit_member(self, guild, member, *, reason=None, **fields):
        route = f'/guilds/{guild.id}/members/{member.id}'
        return self.patch(route, json=fields, reason=reason)

    def application_info(self):
        return self.get('/oauth2/applications/@me')

    def get_user_info(self, user_id):
        return self.get(f'/users/{user_id}')

    def get_user_profile(self, user_id):
        return self.get(f'/users/{user_id}/profile')

    def remove_relationship(self, user):
        return self.delete(f'/users/@me/relationships/{user.id}')

    def add_relationship(self, user_id, type_=None):
        payload = {}
        route = f'/users/@me/relationships/{user_id}'

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
        route = f'/channels/{channel.id}/webhooks'

        payload = {}
        if name is not None:
            payload['name'] = name
        if avatar is not None:
            payload['avatar'] = avatar

        return self.post(route, json=payload)

    def channel_webhooks(self, channel):
        return self.get(f'/channels/{channel.id}/webhooks')

    def guild_webhooks(self, guild):
        return self.get(f'/guilds/{guild.id}/webhooks')

    def get_webhook(self, webhook):
        return self.get(f'/webhooks/{webhook.id}')

    def leave_guild(self, guild):
        return self.delete(f'/users/@me/guilds/{guild.id}')

    def delete_guild(self, guild):
        return self.delete(f'/guilds/{guild.id}')

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

        return self.patch(f'/guilds/{guild.id}', json=payload, reason=reason)

    def get_bans(self, guild):
        return self.get(f'/guilds/{guild.id}/bans')

    def get_vanity_code(self, guild):
        return self.get(f'/guilds/{guild.id}/vanity-url')

    def change_vanity_code(self, guild, code, *, reason=None):
        payload = {'code': code}
        return self.patch(f'/guilds/{guild.id}/vanity-url', json=payload, reason=reason)

    def prune_members(self, guild, days, *, reason=None):
        params = {
            'days': days
        }
        return self.post(f'/guilds/{guild.id}/prune', params=params, reason=reason)

    def estimate_pruned_members(self, guild, days):
        params = {
            'days': days
        }
        return self.get(f'/guilds/{guild.id}/prune', params=params)

    def create_custom_emoji(self, guild, name, image, *, reason=None):
        payload = {
            'name': name,
            'image': image
        }

        return self.post(f'/guilds/{guild.id}/emojis', json=payload, reason=reason)

    def delete_custom_emoji(self, guild, emoji, *, reason=None):
        return self.delete(f'/guilds/{guild.id}/emojis/{emoji.id}', reason=reason)

    def edit_custom_emoji(self, guild, emoji, *, name, reason=None):
        payload = {
            'name': name
        }
        route = f'/guilds/{guild.id}/emojis/{emoji.id}'
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

        return self.get(f'/guilds/{guild.id}/audit-logs', params=params)

    def create_invite(self, channel, *, reason=None, **kwargs):

        payload = {
            'max_age': kwargs.get('max_age', 0),
            'max_uses': kwargs.get('max_uses', 0),
            'temporary': kwargs.get('temporary', False),
            'unique': kwargs.get('unique', True)
        }

        return self.post(f'/channels/{channel.id}/invites', reason=reason, json=payload)

    def get_invite(self, invite_id):
        return self.get(f'/invite/{invite_id}')

    def invites_from(self, guild):
        return self.get(f'/guilds/{guild.id}/invites')

    def invites_from_channel(self, channel):
        return self.get(f'/channels/{channel.id}/invites')

    def delete_invite(self, invite_id, *, reason=None):
        return self.delete(f'/invite/{invite_id}', reason=reason)

    def edit_role(self, guild, role, *, reason=None, **fields):
        route = f'/guilds/{guild.id}/roles/{role.id}'
        valid_keys = ('name', 'permissions', 'color', 'hoist', 'mentionable')
        payload = {
            k: v for k, v in fields.items() if k in valid_keys
        }
        return self.patch(route, json=payload, reason=reason)

    def delete_role(self, guild, role, *, reason=None):
        route = f'/guilds/{guild.id}/roles/{role.id}'
        return self.delete(route, reason=reason)

    def replace_roles(self, user, guild, role_ids, *, reason=None):
        return self.edit_member(guild=guild, user=user, roles=role_ids, reason=reason)

    def create_role(self, guild, *, reason=None, **fields):
        return self.post(f'/guilds/{guild.id}/roles', json=fields, reason=reason)

    def move_role_position(self, guild, positions, *, reason=None):
        return self.patch(f'/guilds/{guild.id}/roles', json=positions, reason=reason)

    def add_role(self, guild, user, role, *, reason=None):
        route = f'/guilds/{guild.id}/members/{user.id}/roles/{role.id}'
        return self.put(route, reason=reason)

    def remove_role(self, guild, user, role, *, reason=None):
        route = f'/guilds/{guild.id}/members/{user.id}/roles/{role.id}'
        return self.delete(route, reason=reason)

    def edit_channel_permissions(self, channel, target, allow, deny, type, *, reason=None):
        payload = {
            'id': target,
            'allow': allow,
            'deny': deny,
            'type': type
        }
        route = f'/channels/{channel.id}/permissions/{target}'
        return self.put(route, json=payload, reason=reason)

    def delete_channel_permissions(self, channel_id, target, *, reason=None):
        route = f'/channels/{channel_id}/permissions/{target}'
        return self.delete(route, reason=reason)

    def move_member(self, user, guild, channel, *, reason=None):  # (voice)
        return self.edit_member(guild=guild, member=user, channel_id=channel.id, reason=reason)
