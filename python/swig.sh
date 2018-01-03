#!/bin/sh

# Create Python bindings as armbianio module

# Get python includes
includes=$(python-config --includes)

# Generate module
swig -python armbianio.i
# Compile wrapper
gcc -c -fPIC ../armbianio.c armbianio_wrap.c $includes
# Link objects
ld -shared armbianio.o armbianio_wrap.o -o _armbianio.so
