# This shows a base class


from pprint import pprint


class Mammal:
    legs = 4
    gestation = "womb"  # not "egg"
    def __init__(self, name, weight = None):
        print("Inside the Mammal constructor")
        self.name = name
        self.weight = weight

    def __str__(self):
        # user friendly string representation of object
        # used in print() or casting to str
        return 'Mammal("{}")'.format(str(self.name))
    
    def __repr__(self):
        # unambiguous string representation of object
        # used in python shell and for debugging; used instead of __str__ if __str__ is missing
        return f'Mammal({str(self.data())})'

    def data(self):
        dobj = self.__dict__
        d1 = self.__class__.__dict__
        d1 = {k: d1[k] for k in d1 if k[0] != '_' and type(d1[k]) in (int, float, str)}
        d2 = {'class': d1, 'object': dobj}
        return d2

if __name__ == "__main__":
    # Create an object:
    x = Mammal("Cow")
    print(x)
    print("'__repr__':", x.__repr__())
    pprint(x.data())
    input('')
