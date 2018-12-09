import armbianio.ArmbianIoLib;
import com.sun.jna.Native;
import com.sun.jna.Pointer;

import static armbianio.ArmbianIoLib.GPIO_IN;

/**
 * Simple callback using built in button.
 * 
 * Copyright (c) 2018 Steven P. Goldsmith
 * See LICENSE.md for details.
 */

public class IR {
	private final ArmbianIoLib armbianIoLib;
	private final int pin;
	private int counter = 0;

	public IR(int iPin, int thresholdLow_us, int thresholdHigh_us) {
		this.pin = iPin;

		// Use to debug if JNA cannot find shared library
		System.setProperty("jna.debug_load", "false");
		System.setProperty("jna.debug_load.jna", "false");
		// Load shared library
		armbianIoLib = Native.loadLibrary("/usr/local/lib/libarmbianio.so", ArmbianIoLib.class);
		final int rc = armbianIoLib.AIOInit();
		if (rc == 1) {
			System.out.println(String.format("Running on a %s", armbianIoLib.AIOGetBoardName()));
			armbianIoLib.AIOAddGPIO(this.pin, GPIO_IN);
			armbianIoLib.AIOWriteGPIOEdge(this.pin, ArmbianIoLib.EDGE_BOTH);
			ArmbianIoLib.AIOIRCALLBACK func = (Pointer pCode) -> {
				decode(pCode, thresholdLow_us, thresholdHigh_us);
				System.out.println(counter++);
			};
			armbianIoLib.AIOAddGPIOIRCallback(this.pin, func);
			System.out.println("Inited ArmbianIO. Press some buttons on your remote control.");
		}
	}

	public void shutDown() {
		armbianIoLib.AIORemoveGPIOIRCallback(pin);
		armbianIoLib.AIORemoveGPIO(pin);
		armbianIoLib.AIOShutdown();
	}

	public static void main(String argv[]) throws InterruptedException {
		IR ir = new IR(11, 200, 2300);
		System.out.println("Press Ctrl+c to exit");
		try {
			while (true) {
				Thread.sleep(1000);
				System.out.println("Tick");
			}
		} catch (Exception e) {
			ir.shutDown();
		}
	}

	private static void decode(Pointer pCode, int thresholdLow_us, int thresholdHigh_us) throws InterruptedException {
		char[] codeCharArray = new char[50];
		int[] code = pCode.getIntArray(0, 52);
		int min = thresholdHigh_us;
		int max = thresholdLow_us;
		int codeLength = 0;
		for(int c : code) {
			if(c > thresholdLow_us && c < thresholdHigh_us) {
				codeLength++;
				if(c < min) min = c;
				if(c > max) max = c;
			}
//			System.out.print(c + ", ");
		}
		System.out.println("\nmin/max: " + min + ", " + max + ", length: " + codeLength);
		if(codeLength > 16) {
			int thresholdMed_us = (min + max) / 2;
			int counter = 0;
			for(int c : code) {
				if(c > thresholdLow_us && c < thresholdHigh_us) {
					if(c < thresholdMed_us) {
						codeCharArray[counter++] = 'S';
					} else {
						codeCharArray[counter++] = 'L';
					}
				}
			}
			String codeString = new String(codeCharArray);
			System.out.println("'" + codeString + "'");
		}
	}
}
