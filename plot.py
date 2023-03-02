# Example of plotting with matplotlib
# Install from a system shell with -
#     python -m pip install matplotlib


import matplotlib.pyplot as plt
import math
import numpy as np


# example use of data in lists
x = [a for a in range(500)]
y = [math.sqrt(a) for a in x]
plt.plot(x, y)
plt.show()


# example use of data in numpy arrays
# https://www.tutorialspoint.com/numpy/numpy_matplotlib.htm
x = np.arange(1, 500)
y = x * x / 10
plt.title("Matplotlib demo")
plt.xlabel("x axis caption")
plt.ylabel("y axis caption")
plt.plot(x, y)
plt.show()
