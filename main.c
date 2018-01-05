//
// ArmbianIO test program
//
// Copyright (c) 2017 Larry Bank
// email: bitbank@pobox.com
// Project started 11/15/2017
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.
//
//
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <armbianio.h>

void GPIOCallback(int, pin, int iValue)
{
	printf("Pin changed, new value = %d\n", iValue);
} /* GPIOCallback() */

int main(int argc, char* argv[])
{
int i, rc;
const char *szBoardName;

	// Initialize the library
	rc = AIOInit("Raspberry Pi");
	if (rc == 0)
	{
		printf("Problem initializing ArmbianIO library\n");
		return 0;
	}
	szBoardName = AIOGetBoardName();
	printf("Running on a %s\n", szBoardName);
	if (AIOHasButton())
#ifdef POLL_BUTTON
	{
		for (i=0; i<100; i++)
		{
			printf("Button = %d\n", AIOReadButton());
			usleep(500000);
    		}
	}
#else // use interrupts
	{
		AIOAddGPIOCallback(0, EDGE_RISING, GPIOCallback);
		// wait for presses
		for (i=0; i<30; i++)
		{
			usleep(1000000);
		}
		AIORemoveGPIO(0);
	}
#endif
	else
	{
// blink an LED on pin 37
		AIOAddGPIO(37, GPIO_OUT);
		for (i=0; i<10; i++)
		{
			AIOWriteGPIO(37, 1);
			usleep(500000);
			AIOWriteGPIO(37, 0);
			usleep(500000);
		}
	}

	// Quit library and free resources
	AIOShutdown();

   return 0;
} /* main() */
