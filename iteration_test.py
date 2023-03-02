# use of built in "iter" and "next" on a class
# containing __iter__ and __next__.


import iteration as it


p2 = it.PowTwo(10)
gen = iter(p2)
while True:
	try:
		print(next(gen))
	except StopIteration:
		break

