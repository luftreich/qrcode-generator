BIN = galois
BIN_C	= test.c \
		  ec.c \
		  gp.c \
		  bitstream.c \
		  util.c \
		  dataencoder.c


LIB_NAME = 
LIB_C   = 

DEPENDFILE = .depend


LIB_SRC = $(LIB_C) $(LIB_CPP)
LIB_OBJ = $(LIB_CPP:%.cpp=%.o)
LIB_OBJ += $(LIB_C:%.c=%.o)
LIB = $(LIB_NAME:%=%.so.1)
BIN_SRC = $(BIN_C) $(BIN_CPP)
BIN_OBJ = $(BIN_CPP:%.cpp=%.o) 
BIN_OBJ += $(BIN_C:%.c=%.o) 
OBJ = $(LIB_OBJ) $(BIN_OBJ)
SRC = $(BIN_SRC) $(LIB_SRC)

CC = cc

CFLAGS += -Wall 
CFLAGS += -ggdb
#CFLAGS += -fPIC
CFLAGS += -I/usr/include/c++/4.1.0
CFLAGS += $(PKGCONFIGCFLAGS)

ifdef O
CFLAGS += -O$O
endif

#CPPFLAGS += $(CFLAGS)

CFLAGS +=

#LDFLAGS += $(PKGCONFIGLIBS)

.PHONY : clean all depend

all : bin lib
bin : $(DEPENDFILE) $(BIN)
lib : $(DEPENDFILE) $(LIB)
depend : $(DEPENDFILE) $(SRC)

$(BIN) : $(LIB) $(BIN_OBJ) 
	$(CC) $(LDFLAGS) -o $@ $^

$(LIB) : $(LIB_OBJ)
	$(CC) -shared -Wl,-soname,$(LIB_NAME).so.1 -o $@ $^
	ln -fs $@ $(LIB_NAME).so

%.o : %.c
	$(CC) $(CFLAGS) -c $< 

$(DEPENDFILE) : $(SRC)
	$(CC) -MM $^ > $@

clean :	
	rm -rf $(BIN) $(LIB) $(OBJ) $(GENFILES) $(LIB_NAME) $(DEPENDFILE)

-include .depend
