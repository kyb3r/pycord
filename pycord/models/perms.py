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


class Permissions:

    __slots__ = ('value')
    
    def __init__(self, permissions=0):
        self.value = int(permissions)

    def _bit(self, index):
        return bool((self.value >> index) & 1)

    def _set(self, index, value):
        if value:
            self.value |= (1 << index)
        else:
            self.value &= ~(1 << index)

    def handle_overwrite(self, allow, deny):
        self.value = (self.value & ~deny) | allow

    @property
    def create_instant_invite(self):
        """Returns True if the user can create instant invites."""
        return self._bit(0)

    @create_instant_invite.setter
    def create_instant_invite(self, value):
        self._set(0, value)

    @property
    def kick_members(self):
        """Returns True if the user can kick users from the guild."""
        return self._bit(1)

    @kick_members.setter
    def kick_members(self, value):
        self._set(1, value)

    @property
    def ban_members(self):
        """Returns True if a user can ban users from the guild."""
        return self._bit(2)

    @ban_members.setter
    def ban_members(self, value):
        self._set(2, value)

    @property
    def administrator(self):
        """Returns True if a user is an administrator. This role overrides all other permissions.
        This also bypasses all channel-specific overrides.
        """
        return self._bit(3)

    @administrator.setter
    def administrator(self, value):
        self._set(3, value)

    @property
    def manage_channels(self):
        """Returns True if a user can edit, delete, or create channels in the guild.
        This also corresponds to the "manage channel" channel-specific override."""
        return self._bit(4)

    @manage_channels.setter
    def manage_channels(self, value):
        self._set(4, value)

    @property
    def manage_guild(self):
        """Returns True if a user can edit guild properties."""
        return self._bit(5)

    @manage_guild.setter
    def manage_guild(self, value):
        self._set(5, value)

    @property
    def add_reactions(self):
        """Returns True if a user can add reactions to messages."""
        return self._bit(6)

    @add_reactions.setter
    def add_reactions(self, value):
        self._set(6, value)

    @property
    def view_audit_log(self):
        """Returns True if a user can view the guild's audit log."""
        return self._bit(7)

    @view_audit_log.setter
    def view_audit_log(self, value):
        self._set(7, value)

    # 2 unused

    @property
    def read_messages(self):
        """Returns True if a user can read messages from all or specific text channels."""
        return self._bit(10)

    @read_messages.setter
    def read_messages(self, value):
        self._set(10, value)

    @property
    def send_messages(self):
        """Returns True if a user can send messages from all or specific text channels."""
        return self._bit(11)

    @send_messages.setter
    def send_messages(self, value):
        self._set(11, value)

    @property
    def send_tts_messages(self):
        """Returns True if a user can send TTS messages from all or specific text channels."""
        return self._bit(12)

    @send_tts_messages.setter
    def send_tts_messages(self, value):
        self._set(12, value)

    @property
    def manage_messages(self):
        """Returns True if a user can delete or pin messages in a text channel. Note that there are currently no ways to edit other people's messages."""
        return self._bit(13)

    @manage_messages.setter
    def manage_messages(self, value):
        self._set(13, value)

    @property
    def embed_links(self):
        """Returns True if a user's messages will automatically be embedded by Discord."""
        return self._bit(14)

    @embed_links.setter
    def embed_links(self, value):
        self._set(14, value)

    @property
    def attach_files(self):
        """Returns True if a user can send files in their messages."""
        return self._bit(15)

    @attach_files.setter
    def attach_files(self, value):
        self._set(15, value)

    @property
    def read_message_history(self):
        """Returns True if a user can read a text channel's previous messages."""
        return self._bit(16)

    @read_message_history.setter
    def read_message_history(self, value):
        self._set(16, value)

    @property
    def mention_everyone(self):
        """Returns True if a user's @everyone will mention everyone in the text channel."""
        return self._bit(17)

    @mention_everyone.setter
    def mention_everyone(self, value):
        self._set(17, value)

    @property
    def external_emojis(self):
        """Returns True if a user can use emojis from other guilds."""
        return self._bit(18)

    @external_emojis.setter
    def external_emojis(self, value):
        self._set(18, value)

    # 1 unused

    @property
    def connect(self):
        """Returns True if a user can connect to a voice channel."""
        return self._bit(20)

    @connect.setter
    def connect(self, value):
        self._set(20, value)

    @property
    def speak(self):
        """Returns True if a user can speak in a voice channel."""
        return self._bit(21)

    @speak.setter
    def speak(self, value):
        self._set(21, value)

    @property
    def mute_members(self):
        """Returns True if a user can mute other users."""
        return self._bit(22)

    @mute_members.setter
    def mute_members(self, value):
        self._set(22, value)

    @property
    def deafen_members(self):
        """Returns True if a user can deafen other users."""
        return self._bit(23)

    @deafen_members.setter
    def deafen_members(self, value):
        self._set(23, value)

    @property
    def move_members(self):
        """Returns True if a user can move users between other voice channels."""
        return self._bit(24)

    @move_members.setter
    def move_members(self, value):
        self._set(24, value)

    @property
    def use_voice_activation(self):
        """Returns True if a user can use voice activation in voice channels."""
        return self._bit(25)

    @use_voice_activation.setter
    def use_voice_activation(self, value):
        self._set(25, value)

    @property
    def change_nickname(self):
        """Returns True if a user can change their nickname in the guild."""
        return self._bit(26)

    @change_nickname.setter
    def change_nickname(self, value):
        self._set(26, value)

    @property
    def manage_nicknames(self):
        """Returns True if a user can change other user's nickname in the guild."""
        return self._bit(27)

    @manage_nicknames.setter
    def manage_nicknames(self, value):
        self._set(27, value)

    @property
    def manage_roles(self):
        """Returns True if a user can create or edit roles less than their role's position.
        This also corresponds to the "manage permissions" channel-specific override.
        """
        return self._bit(28)

    @manage_roles.setter
    def manage_roles(self, value):
        self._set(28, value)

    @property
    def manage_webhooks(self):
        """Returns True if a user can create, edit, or delete webhooks."""
        return self._bit(29)

    @manage_webhooks.setter
    def manage_webhooks(self, value):
        self._set(29, value)

    @property
    def manage_emojis(self):
        """Returns True if a user can create, edit, or delete emojis."""
        return self._bit(30)

    @manage_emojis.setter
    def manage_emojis(self, value):
        self._set(30, value)
