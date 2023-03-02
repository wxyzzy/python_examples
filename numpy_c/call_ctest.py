# ref: Sven Manarch
# https://stackoverflow.com/questions/5862915/passing-numpy-arrays-to-a-c-function-for-input-and-output


import ctypes
import numpy
from numpy.ctypeslib import ndpointer

# get the C function and define the format of arguments
lib = ctypes.cdll.LoadLibrary("./ctest.so")
fun = lib.cfun
fun.restype = None
fun.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                ctypes.c_size_t,
                ndpointer(ctypes.c_double, flags="C_CONTIGUOUS")]

# create numpy data arrays for testing and call the C function
#indata = numpy.ones((5,6))
indata = numpy.array([float(x) for x in range(30)])
indata.resize(5, 6)
outdata = numpy.empty((5, 6))
fun(indata, indata.size, outdata)
print("indata")
print(indata)
print("outdata")
print(outdata)


def wrap_fun(indata, outdata):
    assert indata.size == outdata.size
    fun(indata, indata.size, outdata)
