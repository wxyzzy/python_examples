# This shows a derived class

from Class2 import Mammal
from pprint import pprint

# units of measurment
kg = 1  
g = 0.001

class Cat(Mammal):
    def __init__(self, name, weight):
        print('Inside the Cat constructor')
        cat = 'cat: ' + name
        Mammal.__init__(self, cat, weight)

    def data(self):
        d = Mammal.data(self)
        d.update(self.__dict__)
        return d

if __name__ == "__main__":
    x = Cat("Missa", 5*kg)
    print(x)
    pprint(x.data())

