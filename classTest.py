class MyClass:
    def __new__(cls, *args, **kwargs):
        print("Creating instance")
        instance = super().__new__(cls)
        return instance

    def __init__(self, x):
        print("Initializing instance")
        self.x = x
        print(self.x)

obj = MyClass(10)


class Date:
    def mget(self):
        return self._day

    def mset(self, day):
        self._day = day

    mday = property(mget, mset)




