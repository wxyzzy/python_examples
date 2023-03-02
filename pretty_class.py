# example function to convert to a class
# prerequisite: string formating


def pretty(d):
    s = ''
    for k in d:
        s += f'{k}\t{d[k]}\n'
    return s


d = {'name': 'jojo', 'phone': '0701-112233'}
s = pretty(d)
print(s)


# Refactor function pretty() as a class:
class PhoneUser:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def presentation(self):
        print(f"Name:\t", self.name, "\n"f"Phone:\t", self.phone)
       
pu1 = PhoneUser("Jojo", "0701122334")
pu1.presentation()


# Extend class PhoneUser to include any dictionary of values:
class Pretty:
    def __init__(self, **d):
        self._dict = d

    def pprint(self):
        s = ''
        for k in self._dict:
            s += f'{k}\t{self._dict[k]}\n'
        print(s)
        
per = Pretty(**d)
per.pprint()

perr = Pretty(name = 'July', phone = '12341234', email = 'abc@def.gh')
perr.pprint()

