# Shows scope rules in classes


# Global variables
a = 'whatever'
b = 'jojo'


class Klass:
    b = 34

    def foo(self):
        #global a
        a = 'duh'
        self.c = 3.1415
        print(a)
        print(b)
        print(self.b)

obj = Klass()
obj.foo()

print()
print(a)
print(b)
print(obj.b)
print(Klass.b)
print(obj.c)
