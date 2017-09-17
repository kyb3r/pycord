import asyncio
from abc import ABC

class Emitter(ABC):
    __slots__ = ('_events')

    def __init__(self):
        self._events = {}

    async def get_events(self, event):
        for callback in self._events[event]:
            yield callback

    async def emit(self, event, *args, **kwargs):
        if event in self._events:
            async for callback in self.get_events(event):
                await callback(*args, **kwargs)

    def on(self, event, callback=None):
        if event not in self._events:
            self._events[event] = []
        if asyncio.iscoroutinefunction(callback):
            self._events[event].append(callback)
        else:
            def wrapper(coro):
                if not asyncio.iscoroutinefunction(coro):
                    raise RuntimeWarning(f'Callback is not a coroutine!')
                self._events[event].append(coro)
                return coro
            return wrapper
