// gcc -fPIC -shared -o ctest.so ctest.c
// ref: Sven Manarch
// https://stackoverflow.com/questions/5862915/passing-numpy-arrays-to-a-c-function-for-input-and-output


#include <stdio.h>

void cfun(const double *indata, size_t size, double *outdata) 
{
    size_t i;
    for (i = 0; i < size; ++i)
        outdata[i] = indata[i] * 2.0;
}