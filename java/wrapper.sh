#!/bin/sh

# Create Java bindings as armbianio.jar

# Run in the python dir of the ArmbianIO project. Expects a clean install of Armbian.

# Clean up
rm -f *.o *.so

# Install Java
if ! command -v java
then
	sudo ./install-java.sh
fi

# Compile armbian as shared library
gcc -c -Wall -O2 -fPIC ../armbianio.c

# Link objects
ld -shared armbianio.o -o libarmbianio.so

# Deploy shared library
sudo cp libarmbianio.so /usr/local/lib/.

# Compile JNA interface
javac -cp jna-4.5.0.jar armbianio/ArmbianIoLib.java

# Create package
/usr/lib/jvm/jdk1.8.0/bin/jar cf armbianio.jar armbianio/*.class

# Compile demo code
javac -cp jna-4.5.0.jar:armbianio.jar LedTest.java
javac -cp jna-4.5.0.jar:armbianio.jar Button.java
