import inspect
import shlex

msg = 'bob because he is a bad boy'

msg = shlex.split(msg)

args = []
kwargs = {}

class Test():
    def kick(self, member, *, reason):
        pass

xd = Test()

for name, param in inspect.signature(xd.kick).parameters.items():
    print(name, param)
    if param.kind is param.POSITIONAL_OR_KEYWORD:
        args.append(msg.pop(0))
    if param.kind is param.KEYWORD_ONLY:
        kwargs[name] = ' '.join(msg)


print(args)
print(kwargs)


