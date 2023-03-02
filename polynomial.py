# graph a polynomial


import matplotlib.pyplot as plt
from numpy import poly1d


p = poly1d([-1, -1, 100, 0])    # 3rd order polynomial
x = [a for a in range(-20, 20)]
y = p(x)
plt.plot(x, y)
plt.show()
