#!/bin/sh

# Create Python bindings as armbianio module

# Run in the python dir of the ArmbianIO project

# Clean up
rm -f *.c *.o *.so armbianio/armbianio.* /usr/local/lib/_armbianio.so

# Get python includes
includes=$(python-config --includes)
# Generate module in package
swig -python -outdir armbianio armbianio.i
# Compile wrapper
gcc -c -fPIC ../armbianio.c armbianio_wrap.c $includes
# Link objects
ld -shared armbianio.o armbianio_wrap.o -o _armbianio.so

# Deploy shared library
cp _armbianio.so /usr/local/lib/_armbianio.so