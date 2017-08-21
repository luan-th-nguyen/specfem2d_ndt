EXE		=
LIB		= .a
OBJ		= .o

MAKE		= make
AR		= ar
######ARFLAGS		= -ruv
####### DK DK removed "u" to avoid a warning with GNU gcc
ARFLAGS		= -rv
CAT		= cat
CCS		= gcc
CCP		= mpicc
CCD		= gcc
CFLAGS		= -O3 -DCOMMON_FILE_COMPRESS_GZ -DCOMMON_PTHREAD -DCOMMON_RANDOM_FIXED_SEED -DSCOTCH_RENAME -DSCOTCH_RENAME_PARSER -DSCOTCH_PTHREAD -Drestrict=__restrict -pthread
CLIBFLAGS	=
LDFLAGS		= -lz -lm 
CP		= cp
LEX		= : -Pscotchyy -olex.yy.c
LN		= ln
MKDIR		= mkdir
MV		= mv
RANLIB		= ranlib
YACC		= yacc -pscotchyy -b y
