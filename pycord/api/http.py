import sys
import time
import asyncio
import aiohttp
import weakref
from urllib.parse import quote
from .. import __version__, __github__
from ..utils import get_event_loop, to_json, from_json, API

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
            self.lock.release()

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
    def __init__(self, loop=None):
        self.token = None
        self.retries = 5
        self.loop = loop or get_event_loop()
        self.buckets = weakref.WeakValueDictionary()
        self.global_event = asyncio.Event(loop=self.loop)
        self.session = aiohttp.ClientSession(loop=self.loop)

        # set global lock and create user agent
        self.global_event.set()
        user_agent = 'DiscordBot ({0} {1}) Python/{2[0]}.{2[1]}'
        self.user_agent = user_agent.format(
            __github__, __version__, sys.version_info)

    def __del__(self):
        self.session.close()

    async def get(self, endpoint, **kwargs):
        ''' Helper function for GET request '''
        return await self.request('GET', endpoint, **kwargs)

    async def put(self, endpoint, **kwargs):
        ''' Helper function for PUT request '''
        return await self.request('PUT', endpoint, **kwargs)

    async def post(self, endpoint, **kwargs):
        ''' Helper function for POST request '''
        return await self.request('POST', endpoint, **kwargs)

    async def patch(self, endpoint, **kwargs):
        ''' Helper function for PATCH request '''
        return await self.request('PATCH', endpoint, **kwargs)

    async def delete(self, endpoint, **kwargs):
        ''' Helper function for DELETE request '''
        return await self.request('DELETE', endpoint, **kwargs)

    async def request(self, method, endpoint, **kwargs):
        ''' Perform an HTTP request with rate limiting '''
        method = method
        endpoint = endpoint
        bucket = f"{method}.{endpoint}"
        endpoint = API.HTTP_ENDPOINT + endpoint

        # get lock
        lock = self.buckets.get(bucket)
        if lock is None:
            lock = asyncio.Lock(loop=self.loop)
            self.buckets[bucket] = lock

        # create headers
        headers = {'User-Agent': self.user_agent}
        if self.token is not None:
            headers['Authorization'] = f'Bot {self.token}'
        if 'reason' in kwargs:
            headers['X-Audit-Log-Reason'] = kwargs.get('reason')
        
        # get data
        data = kwargs.get('data')
        if data is not None:
            if isinstance(data, dict):
                data = to_json(data)
            if isinstance(data, str):
                data = data.encode('utf-8')

            headers['Content-Type'] = 'application/json'

        # check if global rate limited
        if not self.global_event.is_set():
            await self.global_event.wait()

        # open http request with retries
        async with HoldableLock(lock) as hold_lock:
            for tries in range(self.retries):
                async with self.session.request(method, endpoint, headers=headers, data=data) as resp:

                    # get response and header data
                    data = await resp.text(encoding='utf-8')
                    if 'application/json' in resp.headers['content-type']:
                        data = from_json(data)
                    remaining = resp.headers.get('X-Ratelimit-Remaining', 0)

                    # check if route should be rate limited
                    if remaining == '0' and resp.status != 429:
                        hold_lock.hold()
                        delay = int(resp.headers.get('X-Ratelimit-Reset')) - time.time()
                        self.loop.call_later(delay, lock.release)

                    # check if route IS rate limited
                    elif resp.status == 429:
                        with GlobalLock(self.global_event, data.get('global', False)):

                            # wait for rate limit delay delay
                            retry_after = data.get('retry-after', 0)
                            await asyncio.sleep(retry_after / 1000.0, loop=self.loop)

                        # retry request
                        continue

                    # return response data
                    if 300 > resp.status >= 200:
                        return data or None

                    # forbidden path
                    elif resp.status == 403:
                        raise Exception(f"Forbidden: {method} {endpoint}")

                    # path not found
                    elif resp.status == 404:
                        raise Exception(f"Not Found: {method} {endpoint}")

                    # service is down, wait a bit and retry later
                    elif resp.status in (500, 502):
                        await asyncio.sleep(1 + tries * 2, loop=self.loop)
                        continue

                    # unknown http error
                    else:
                        raise Exception(f"HTTP Error: {resp.status} {method} {endpoint}")

        # retries have been exhausted
        raise Exception(f"Failed HTTP Request: {resp.status} {method} {endpoint}")


    def send_message(self, channel, **kwargs):
        '''Send a message to a channel.'''
        route = f'/channels/{channel.id}/messages'

        payload = {
            'content' : kwargs.get('content'),
            'embed' : kwargs.get('embed'),
            'tts' : kwargs.get('tts', False)
        }

        return self.post(route, data=payload)

    def send_typing(self, channel):
        route = f'/channels/{channel.id}/typing'
        return self.post(route)

    def send_files(self, channel, *, files, content=None, tts=False, embed=None, nonce=None):
        '''Send files to a channel.'''
        route = f'/channels/{channel.id}/messages'

        form = aiohttp.FormData()

        payload = {
            'content' : kwargs.get('content'),
            'embed' : kwargs.get('embed'),
            'tts' : kwargs.get('tts', False)
        }

        form.add_field('payload_json', to_json(payload))

        for i, (buffer, filename) in enumerate(files):
            form.add_field(f'file{i}', buffer, filename=filename, content_type='application/octet-stream')

        return self.post(route, data=form)

    def start_private_message(self, user):
        payload = {
            'recipient_id': user.id
        }
        return self.post('/users/@me/channels', data=payload)

    def delete_message(self, channel, message_id, *, reason=None):
        route = f'/channels/{channel.id}/messages/{message.id}'
        return self.delete(r, reason=reason)

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
        route = f'/channels/{channel.id}/messages/{message.id}/reactions/{emoji}/{member.id}'
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
        r = f'/channels/{channel.id}/messages/{message.id}'
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
            'name' : name,
            'icon' : icon
        }

        return self.patch( data=payload)

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

        return self.put(r, params=params)

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

        route = f'/users/@me/relationships/{user.id}'

        if type_ is not None:
            payload = {'type': type_}

        return self.put(route, json=payload)

    def send_friend_request(self, username, discriminator):
        payload = {
            'username': username,
            'discriminator': int(discriminator)
        }
        return self.request('/users/@me/relationships', json=payload)






