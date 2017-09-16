from ..utils import json

async def Handle(self, event, data):
    print("Handling event:", event, json.dumps(data, sort_keys=True, indent=2))

    if event == 'READY':
        self.client.user.from_dict(data.get('user'))
        self.session_id = data.get('session_id')
        self.resume = False

    elif event == 'RESUMED':
        self.resume = False

    elif event == 'CHANNEL_CREATE':
        pass

    elif event == 'CHANNEL_UPDATE':
        pass

    elif event == 'CHANNEL_DELETE':
        pass

    elif event == 'CHANNEL_PINS_UPDATE':
        pass

    elif event == 'GUILD_CREATE':
        pass

    elif event == 'GUILD_UPDATE':
        pass

    elif event == 'GUILD_DELETE':
        pass

    elif event == 'GUILD_BAN_ADD':
        pass

    elif event == 'GUILD_BAN_REMOVE':
        pass

    elif event == 'GUILD_EMOJIS_UPDATE':
        pass

    elif event == 'GUILD_INTERGRATIONS_UPDATE':
        pass

    elif event == 'GUILD_MEMBER_ADD':
        pass

    elif event == 'GUILD_MEMBER_REMOVE':
        pass
        
    elif event == 'GUILD_MEMBERS_CHUNK':
        pass

    elif event == 'GUILD_ROLE_CREATE':
        pass

    elif event == 'GUILD_ROLE_UPDATE':
        pass

    elif event == 'GUILD_ROLE_DELETE':
        pass

    elif event == 'MESSAGE_CREATE':
        pass

    elif event == 'MESSAGE_UPDATE':
        pass

    elif event == 'MESSAGE_DELETE':
        pass

    elif event == 'MESSAGE_DELETE_BULK':
        pass

    elif event == 'MESSAGE_REACTION_ADD':
        pass

    elif event == 'MESSAGE_REACTION_REMOVE':
        pass

    elif event == 'MESSAGE_REACTION_REMOVE_ALL':
        pass

    elif event == 'PRESENCE_UPDATE':
        pass

    elif event == 'GAME_OBJECT':
        pass

    elif event == 'TYPING_START':
        pass

    elif event == 'USER_UPDATE':
        pass

    elif event == 'VOICE_STATE_UPDATE':
        pass

    elif event == 'VOICE_SERVER_UPDATE':
        pass

    elif event == 'WEBHOOKS_UPDATE':
        pass