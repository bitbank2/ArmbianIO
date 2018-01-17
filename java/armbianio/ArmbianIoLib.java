package armbianio;

import com.sun.jna.Callback;
import com.sun.jna.Library;

/**
 * Interface for JNA that mirrors armbianio.h.
 * 
 * Copyright (c) 2018 Steven P. Goldsmith
 * See LICENSE.md for details.
 */

public interface ArmbianIoLib extends Library {
	int GPIO_OUT = 0;
	int GPIO_IN = 1;
	int EDGE_FALLING = 0;
	int EDGE_RISING = 1;
	int EDGE_BOTH = 2;
	
	int AIOInit();	

	int AIOInitBoard(String boardName);

	void AIOShutdown();

	String AIOGetBoardName();

	int AIOOpenI2C(int iChannel, int iAddress);

	int AIOOpenSPI(int iChannel, int iSpeed);

	void AIOCloseI2C(int iHandle);

	void AIOCloseSPI(int iHandle);

	int AIOReadI2C(int iHandle, byte ucRegister, byte[] buf, int iCount);

	int AIOWriteI2C(int iHandle, byte ucRegister, byte[] buf, int iCount);

	int AIOReadSPI(int iHandle, byte[] buf, int iCount);

	int AIOWriteSPI(int iHandle, byte[] buf, int iCount);

	int AIOReadWriteSPI(int iHandle, byte[] inbuf, byte[] outbuf, int iCount);

	int AIOHasButton();

	int AIOReadButton();

	int AIOAddGPIO(int iPin, int iDirection);

	interface AIOCALLBACK extends Callback {
		void invoke(int iPin, int iState);
	}

	int AIOAddGPIOCallback(int iPin, int iEdge, AIOCALLBACK callback);

	void AIORemoveGPIO(int iPin);

	int AIOReadGPIO(int iPin);

	int AIOWriteGPIO(int iPin, int iValue);
}
