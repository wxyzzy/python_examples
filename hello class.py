# This is an example of a class

class Hello:
    info = 'This is a class that writes "Hello" to someone.'

    def __init__(self, who):
        self.who = who

    def __str__(self):
        return self.who

    def set_who(self, who):
        self.who = who


h = Hello('some pig')

print(h.info)

print('Hello, {}'.format(h))

h.who = 'whatever'
print('Hello, {}'.format(h))

h.set_who('you guys')
print('Hello, {}'.format(h))

print('Hello again, ' + h.who)
