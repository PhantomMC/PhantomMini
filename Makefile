# Temporary makefile
# Should ideally be kept up to date by an ide






CC=gcc
CFLAGS=-I.
#FOLDER = ./lib/temporary/
#DEPS = $(FOLDER)gibonacci.h $(FOLDER)primals.h
OBJ = phantom.c

#%.o: %.c $(DEPS)
#	$(CC) -c -o $@ $< $(CFLAGS)

Phantom: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)