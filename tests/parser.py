import inspect

def is_mod(ctx):
    return True


def test(first:int, last:str):
    pass

print(inspect.signature(test).return_annotation is inspect._empty)

