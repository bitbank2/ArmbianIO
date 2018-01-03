#!/bin/sh

# Create Python bindings

swig -python armbianio.i
gcc -c -fPIC ../armbianio.c ArmbianIO_wrap.c -I/usr/include/python2.7
ld -shared ../armbianio.o ArmbianIO_wrap.o -o _ArmbianIO.so
