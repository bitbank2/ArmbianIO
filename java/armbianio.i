/*
Swig interface file
*/

%module ArmbianIO
%{
/* Includes the header in the wrapper code */
#include "../armbianio.h"
%}

/* Parse the header file to generate wrappers */
%include "../armbianio.h"
