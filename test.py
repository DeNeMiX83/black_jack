import inspect


class A:
    ...

class B:
    ...

def f(df: A, df2: B):
    ...


d = inspect.signature(f)
for i in d.parameters.values():
    print(i.annotation)
