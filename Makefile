PROCESSOR:=$(shell uname -m)
ifeq ($(PROCESSOR), armv6l)
CFLAGS=-c -Wall -O2 -D RPIZERO
else
CFLAGS=-c -Wall -O2
endif

all: libarmbianio.a

libarmbianio.a: armbianio.o
	ar -rc libarmbianio.a armbianio.o ;\
	sudo cp libarmbianio.a /usr/local/lib ;\
	sudo cp armbianio.h /usr/local/include

armbianio.o: armbianio.c armbianio.h
	$(CC) $(CFLAGS) armbianio.c

clean:
	rm *.o libarmbianio.a

