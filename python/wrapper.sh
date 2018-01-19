#!/bin/sh

# Create Python bindings as armbianio module

# Run in the python dir of the ArmbianIO project. Expects a clean install of Armbian.

# Clean up
rm -f *.o *.so
rm -rf armbianio

# Install python-dev
if [ $(dpkg-query -W -f='${Status}' python-dev 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
	sudo apt-get -y install python-dev
fi

# Install pip and ctypesgen
if ! command -v pip
then
	sudo apt-get -y install python-pip
	sudo -H pip install --upgrade pip setuptools
	sudo apt-get -y purge python-pip
	sudo apt -y autoremove
	sudo -H pip install --upgrade ctypesgen
fi

# Compile armbian as shared library
gcc -c -Wall -O2 -fPIC ../armbianio.c

# Link objects
ld -shared armbianio.o -o libarmbianio.so

# Deploy shared library
sudo cp libarmbianio.so /usr/local/lib/.

# Generate armbianio python module
mkdir armbianio
touch armbianio/__init__.py
ctypesgen.py -o armbianio/armbianio.py -l /usr/local/lib/libarmbianio.so ../armbianio.h

# Install Python package
sudo -H pip install -e .
