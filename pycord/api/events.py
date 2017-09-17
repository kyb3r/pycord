from ..utils import json

async def Handle(self, event, data):

    print("Handling event:", event, json.dumps(data, sort_keys=True, indent=2))

    if event == 'READY':
        await self.client.emit('ready') # not supposed to be here
        self.client.user.from_dict(data.get('user'))
        self.session_id = data.get('session_id')
        self.resume = False

    elif event == 'RESUMED':
        await self.client.emit('resume')
        self.resume = False

    elif event == 'CHANNEL_CREATE':
        await self.client.emit('channel_create')
        pass

    elif event == 'CHANNEL_UPDATE':
        await self.client.emit('channel_update')
        pass

    elif event == 'CHANNEL_DELETE':
        await self.client.emit('channel_delete')
        pass

    elif event == 'CHANNEL_PINS_UPDATE':
        await self.client.emit('pins_update')
        pass

    elif event == 'GUILD_CREATE':
        await self.client.emit('guild_create')
        pass

    elif event == 'GUILD_UPDATE':
        await self.client.emit('guild_update')
        pass

    elif event == 'GUILD_DELETE':
        await self.client.emit('guild_delete')
        pass

    elif event == 'GUILD_BAN_ADD':
        await self.client.emit('member_ban')
        pass

    elif event == 'GUILD_BAN_REMOVE':
        await self.client.emit('member_unban')
        pass

    elif event == 'GUILD_EMOJIS_UPDATE':
        await self.client.emit('emoji_update')
        pass

    elif event == 'GUILD_INTERGRATIONS_UPDATE':
        await self.client.emit('intergrations_update')
        pass

    elif event == 'GUILD_MEMBER_ADD':
        await self.client.emit('member_join')
        pass

    elif event == 'GUILD_MEMBER_REMOVE':
        await self.client.emit('member_leave')
        pass
        
    elif event == 'GUILD_MEMBERS_CHUNK':
        await self.client.emit('guild_members_chunk')
        pass

    elif event == 'GUILD_ROLE_CREATE':
        await self.client.emit('role_create')
        pass

    elif event == 'GUILD_ROLE_UPDATE':
        await self.client.emit('role_update')
        pass

    elif event == 'GUILD_ROLE_DELETE':
        await self.client.emit('role_delete')
        pass

    elif event == 'MESSAGE_CREATE':
        await self.client.emit('message', data) # for testing
        pass

    elif event == 'MESSAGE_UPDATE':
        await self.client.emit('message_edit')
        pass

    elif event == 'MESSAGE_DELETE':
        await self.client.emit('message_delete')
        pass

    elif event == 'MESSAGE_DELETE_BULK':
        await self.client.emit('message_delete_bulk')
        pass

    elif event == 'MESSAGE_REACTION_ADD':
        await self.client.emit('reaction_add')
        pass

    elif event == 'MESSAGE_REACTION_REMOVE':
        await self.client.emit('reaction_remove')
        pass

    elif event == 'MESSAGE_REACTION_REMOVE_ALL':
        await self.client.emit('reaction_remove_all')
        pass

    elif event == 'PRESENCE_UPDATE':
        await self.client.emit('presence_update')
        pass

    elif event == 'GAME_OBJECT':
        await self.client.emit('game_object')
        pass

    elif event == 'TYPING_START':
        await self.client.emit('typing_start')
        pass

    elif event == 'USER_UPDATE':
        await self.client.emit('user_update')
        pass

    elif event == 'VOICE_STATE_UPDATE':
        await self.client.emit('voice_state_update')
        pass

    elif event == 'VOICE_SERVER_UPDATE':
        await self.client.emit('voice_server_update')
        pass

    elif event == 'WEBHOOKS_UPDATE':
        await self.client.emit('webhook_update')
        pass