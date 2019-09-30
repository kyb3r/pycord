

import inspect
from abc import ABC
from collections import defaultdict
import anyio


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
                    raise RuntimeWarning('Callback is not a coroutine!')
                self._events[event].append(coro)
                return coro
            return wrapper

    async def emit(self, event, *args, **kwargs):
        on_event = 'on_{}'.format(event)
        try:
            if hasattr(self, on_event):
                await getattr(self, on_event)(*args, **kwargs)

            if event in self._events:
                for callback in self._events[event]:
                    async with anyio.create_task_group() as n:
                        await n.spawn(callback, *args, **kwargs)

        except Exception as e:
            await self.emit('error', e)
