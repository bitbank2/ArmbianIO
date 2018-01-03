#!/bin/sh

# Create Python bindings

# Get python includes
includes=$(python-config --includes)

swig -python armbianio.i
gcc -c -fPIC ../armbianio.c ArmbianIO_wrap.c $includes
ld -shared ../armbianio.o ArmbianIO_wrap.o -o _ArmbianIO.so
