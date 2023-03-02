# ffttest


from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import math


# define test function
x = [(10.0 * math.pi * a / 500) for a in range(500)]
y = [(math.sin(a) + math.sin(a * 20)) * a for a in x]
n = len(x)
plt.plot(x, y)
plt.show()

# compute norm of fft
z = fft(y)
timestep = 1
freq = fftfreq(n, d=timestep)
w = [math.sqrt((c * c.conjugate()).real) for c in z]
plt.plot(freq[:n//2], w[:n//2])
plt.show()
