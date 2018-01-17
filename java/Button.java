import com.sun.jna.Callback;
import com.sun.jna.Library;
import com.sun.jna.Native;
import java.util.concurrent.TimeUnit;

public class Button {

	public interface ArmbianIoLib extends Library {
		interface AIOCALLBACK extends Callback {
			void invoke(int iPin, int iState);
		}

		int AIOAddGPIOCallback(int iPin, int iEdge, AIOCALLBACK callback);

		int AIOInit();

		int AIOHasButton();

		String AIOGetBoardName();

		void AIOShutdown();
	}

	public static void main(String argv[]) throws InterruptedException {
		System.setProperty("jna.debug_load", "true");
		System.setProperty("jna.debug_load.jna", "true");
		// Make sure libjnidispatch.so isn't loaded from JNA jar file
		System.out.println(System.getProperty("java.library.path"));
		final ArmbianIoLib armbianIoLib = (ArmbianIoLib) Native.loadLibrary("/usr/local/lib/armbianio_java.so",
				ArmbianIoLib.class);
		final int rc = armbianIoLib.AIOInit();
		if (rc == 1) {
			System.out.println(String.format("Running on a %s", armbianIoLib.AIOGetBoardName().trim()));
			if (armbianIoLib.AIOHasButton() == 1) {
				ArmbianIoLib.AIOCALLBACK func = new ArmbianIoLib.AIOCALLBACK() {
					public void invoke(int iPin, int iEdge) {
						System.out.println(String.format("Button state: pin = %d, value = %d", iPin, iEdge));
					}
				};
				System.out.println("Press/release button a few times");
				armbianIoLib.AIOAddGPIOCallback(0, 2, func);
				TimeUnit.SECONDS.sleep(10);
			} else {
				System.out.println(String.format("%s does not have a button", armbianIoLib.AIOGetBoardName()));
			}
			armbianIoLib.AIOShutdown();
		}
	}
}
