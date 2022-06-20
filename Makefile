# Temporary makefile
# Should ideally be kept up to date by an ide






CC=gcc
CFLAGS=-I.
FOLDER = ./lib/protocol/
DEPS = $(FOLDER)protocol.h
OBJ = phantom.c

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

Phantom: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)
