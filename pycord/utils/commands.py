'''
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
'''

import inspect

class Command:
    def __init__(self, client, **kwargs):
        self.client = client
        self.callback = kwargs.get('callback')
        self.name = kwargs.get('name')
        self.aliases = [self.name] + kwargs.get('aliases', [])
        self.help_doc = self.callback.__doc__

    @property
    def signature(self):
        pass






class CommandCollection:
    def __init__(self, client):
        self.client = client
        self.commands = {}


    def __iter__(self):
        for cmd in self.commands.values():
            yield cmd

    def _is_already_registered(self, cmd):
        for command in self.commands.values():
            for alias in cmd.aliases:
                if alias in command.aliases:
                    return True

    def add(self, cmd):
        if not isinstance(cmd, Command):
            raise ValueError('cmd must be a subclass of Command')
        if self._is_already_registered(cmd):
            raise ValueError('A name or alias is already registered')
        self.commands[cmd.name] = cmd

    def get(self, alias, prefix='',fallback=None):
        try:
            return self.commands[alias]
        except KeyError:
            pass
        for command in self.commands:
            if alias in command.aliases:
                return command
        return fallback



