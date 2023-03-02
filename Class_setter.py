# Class setter and getter
# with example of raising an exception if parameter is not a string.


class Klass:
	def __init__(self):
		self._name = ''
		
	@property
	def name(self):
		print('in getter')
		return self._name
	
	@name.setter
	def name(self, value):
		print(f'in setter (value == {value})')
		if type(value) != str:
			raise ValueError('Class variable must be a string.')
		self._name = value


k = Klass()
k.name = 'this is a string'
print(k.name)
k.name = 3
print(k.name)
