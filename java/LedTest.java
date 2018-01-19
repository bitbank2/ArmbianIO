import com.sun.jna.Native;
import java.util.concurrent.TimeUnit;
import armbianio.ArmbianIoLib;

/**
 * Simple LED blink
 * 
 * Using the NanoPi Duo connect a 220Ω resistor to the anode (the long pin of
 * the LED), then the resistor to 3.3 V, and connect the cathode (the short
 * pin) of the LED to pin 12 (IOG11). The anode of LED connects to a
 * current-limiting resistor and then to 3.3V. Therefore, to turn on an LED,
 * we need to make pin 12 low (0V) level. It can be realized by programming.
 * See images/ledtest.jpg for schematic.
 * 
 * Copyright (c) 2018 Steven P. Goldsmith
 * See LICENSE.md for details.
 */

public class LedTest {

	static {
		System.load("/usr/local/lib/libarmbianio.so");
	}

	public static void main(String argv[]) throws InterruptedException {
		// Load shared library
		final ArmbianIoLib armbianIoLib = (ArmbianIoLib) Native.loadLibrary("/usr/local/lib/libarmbianio.so",
				ArmbianIoLib.class);
		final int rc = armbianIoLib.AIOInit();
		if (rc == 1) {
			System.out.println(String.format("Running on a %s", armbianIoLib.AIOGetBoardName().trim()));
			// Pin 12 set to output
			final int pin = 12;
			armbianIoLib.AIOAddGPIO(pin, ArmbianIoLib.GPIO_OUT);
			armbianIoLib.AIOWriteGPIO(pin, 0);
			TimeUnit.SECONDS.sleep(3);
			armbianIoLib.AIOWriteGPIO(pin, 1);
			armbianIoLib.AIOShutdown();
		}
	}
}
