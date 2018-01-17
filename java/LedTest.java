import java.util.concurrent.TimeUnit;
import armbianio.ArmbianIOConstants;
import armbianio.ArmbianIO;

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
		System.load("/usr/local/lib/armbianio_java.so");
	}

	public static void main(String argv[]) throws InterruptedException {
		final int rc = ArmbianIO.AIOInit();
		if (rc == 1) {
			System.out.println(String.format("Running on a %s", ArmbianIO.AIOGetBoardName().trim()));
			// Pin 12 set to output
			final int pin = 12;
			ArmbianIO.AIOAddGPIO(pin, ArmbianIOConstants.GPIO_OUT);
			ArmbianIO.AIOWriteGPIO(pin, 0);
			TimeUnit.SECONDS.sleep(3);
			ArmbianIO.AIOWriteGPIO(pin, 1);
			ArmbianIO.AIOShutdown();
		}
	}
}
