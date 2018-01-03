#!/bin/sh

# Create Python bindings as armbianio module

# Run in the python dir of the ArmbianIO project

# Clean up
rm -f *.c *.o *.so armbianio/armbianio.*
sudo rm -f /usr/local/lib/_armbianio.so

# Get python includes
includes=$(python-config --includes)

# Install swig if needed
if [ $(dpkg-query -W -f='${Status}' swig 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
  apt-get -y install swig;
fi
# Generate module in package
swig -python -outdir armbianio armbianio.i
# Compile wrapper
gcc -c -fPIC ../armbianio.c armbianio_wrap.c $includes
# Link objects
ld -shared armbianio.o armbianio_wrap.o -o _armbianio.so

# Deploy shared library
sudo cp _armbianio.so /usr/local/lib/.

# Install Python package
sudo -H pip install -e .