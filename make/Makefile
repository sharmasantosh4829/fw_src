#
IDIR =../include
CC=gcc
CFLAGS=-I$(IDIR)
ODIR=../obj
LDIR =../lib
SRC =../src
BIN =../bin
BUILD =../build

func3: $(SRC)/main.c
	$(CC) -shared -o $(BUILD)/lib.so -fPIC $(SRC)/main.c

func2: $(ODIR)/main.o
	$(CC) $(ODIR)/main.o -o ../bin/arithc

func1: $(SRC)/main.c
	$(CC) -c $(SRC)/main.c -o $(ODIR)/main.o

clean:
	rm -rf $(ODIR)/*.o
	rm -rf $(BIN)/*
	rm -rf $(BUILD)/*.so
