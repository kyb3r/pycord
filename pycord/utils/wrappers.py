from functools import update_wrapper, partial


class Wrapper:
    def __init__(self, func, _args=(), **kwargs):
        update_wrapper(self, func)
        self.args = _args
        self.kwargs = kwargs

    def __new__(cls, *args, **kwargs):
        if len(args) == 1 and callable(args[0]):
            obj = object.__new__(cls)
            obj.__init__(args[0], **kwargs)
            return obj
        else:
            return partial(cls, _args=args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.__wrapped__(*args, **kwargs)


class Command(Wrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.before_calls = list()
        self.after_calls = list()

    async def __call__(self, *args, **kwargs):
        await self.run_before(args[0])
        await self.run_after(args[0])
        await super().__call__(*args, **kwargs)

    async def run_before(self, context):
        for call in self.before_calls:
            await call(context)

    async def run_after(self, context):
        for call in self.after_calls:
            await call(context)


class keyword(Wrapper):
    def __init__(self, func, *keywords):
        pass
