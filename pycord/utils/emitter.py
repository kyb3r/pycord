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

import inspect
from abc import ABC
from collections import defaultdict


class Emitter(ABC):
    __slots__ = ('_events',)

    def __init__(self):
        self._events = defaultdict(list)

    def on(self, event, callback=None):
        if inspect.iscoroutinefunction(callback):
            self._events[event].append(callback)
        else:
            def wrapper(coro):
                if not inspect.iscoroutinefunction(coro):
                    raise RuntimeWarning(f'Callback is not a coroutine!')
                self._events[event].append(coro)
                return coro
            return wrapper

    async def emit(self, event, *args, **kwargs):
        on_event = f'on_{event}'
        try:
            if hasattr(self, on_event):
                await getattr(self, on_event)(*args, **kwargs)
            if event in self._events:
                for callback in self._events[event]:
                    await callback(*args, **kwargs)
        except Exception as e:
            await self.emit('error', e)
