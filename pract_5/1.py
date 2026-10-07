# Что выведет?
# Что будет, если написать просто x вместо self.x?


x = "global"

class A:
    x = "class"

    def __init__(self):
        self.x = "instance"

    def show(self):
        x = "local"
        print(x)
        print(self.x)
        print(A.x)
        print(globals()["x"])


a = A()
a.show()