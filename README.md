![Logo](images/logo.png)

ArmbianIO is a C library for accessing I2C, SPI and GPIO ports in a consistent
way across all of the SBCs that Armbian supports. Since Armbian supports SBCs
from multiple OEMs using a variety of SoCs, the GPIO pin numbering is different
on each board. Linux provides kernel drivers for communicating with the I2C
and SPI bus in a consistent way, but the GPIO numbering can vary widely.
This library aims to create simple wrapper functions for accessing I2C, SPI
and creates a consistent numbering scheme for accessing GPIO ports based on
the physical pin number. Other I/O libraries have tried to copy the BCM
(Broadcom) I/O numbering to be compatible with Raspberry Pi hardware, but this
creates a new layer of confusion and incompatibility since different boards
expose different numbers and arrangements of GPIO ports. By using a numbering
scheme based on the physical pin numbers of the boards, it becomes much easier
to correctly connect devices on every board supported by Armbian. This also
allows for boards with additional GPIOs such as the Orange Pi Zero which has
two more usable pins on its TTY header.

NB: ArmbianIO requires Armbian with a mainline (4.x) kernel. Older versions
don't have the unique board identifier (/run/machine.id)

Features
--------
- Now supports any Linux distribution for ARM SBCs (e.g. RPI, OrangePi, NanoPi, etc)
- Will support all SBCs supported by Armbian (soon)
- Includes simple functions for communicating with GPIO, I2C and SPI buses
- References GPIO pins by physical pin number
- Includes functions for detecting presence of and reading status of on-board
  key/button (not all boards have one)
- Python bindings are generated with ctypesgen
- Cross platform RPi.GPIO clone is in the works
- Java bindings use a simple interface file and JNA
 
To build the C library, simply type 'make' in the terminal. To build the sample
app, type 'make -f make_demo'. This will build the 'demo' executable to show
that the library is working.

To build Python bindings `cd ArmbianIO/python` then `./wrapper.sh`. You can run
as many times as you like since the script cleans up and regenerates the wrapper
from the C headers. `sudo python ledtest.py` to run LED test after wiring up
project.

To build Java bindings `cd ArmbianIO/java` then `./wrapper.sh`. You can run as
many times as you like since the script cleans up and compiles the wrapper. The
Java bindings depend on Oracle JDK 8 which wrapper.sh installs. If you wish to
use another JDK then you will need to modify wrapper.sh. Use
`sudo java -Djava.library.path=/usr/local/lib -cp jna-4.5.0.jar:armbianio.jar:. LedTest`
to run LED test after wiring up project.

Copyright (c) 2017 by Larry Bank<br>
Project started 11/13/2017<br>
bitbank@pobox.com<br>

If you find this code useful, please consider buying me a cup of coffee<br>
[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=SR4F44J2UR8S4)
