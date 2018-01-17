#!/bin/sh

# Create Python bindings as armbianio module

# Run in the python dir of the ArmbianIO project

# Clean up
rm -f *.c *.o *.so
sudo rm -f /usr/local/lib/armbianio_java.so
sudo rm -rf armbianio

# Install Java
if ! command -v java
then
	sudo ./install-java.sh
fi

# Install swig
if [ $(dpkg-query -W -f='${Status}' swig 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
	sudo apt-get -y install swig
fi

mkdir -p armbianio

# Generate module in package
swig -java -package armbianio -outdir armbianio armbianio.i

# Compile wrapper
gcc -c -Wall -O2 -fPIC -fno-strict-aliasing ../armbianio.c armbianio_wrap.c -I/usr/lib/jvm/jdk1.8.0/include -I/usr/lib/jvm/jdk1.8.0/include/linux

# Link objects
ld -shared armbianio.o armbianio_wrap.o -o armbianio_java.so

# Deploy shared library
sudo cp armbianio_java.so /usr/local/lib/.

# Compile Java wrapper code
javac armbianio/ArmbianIO.java

# Create package
/usr/lib/jvm/jdk1.8.0/bin/jar cf armbianio.jar armbianio/*.class

# Compile demo code
javac -cp armbianio.jar LedTest.java
javac -cp jna-4.5.0.jar Button.java
