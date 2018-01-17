/*
Swig interface file
*/

%module armbianio
%{
/* Includes the header in the wrapper code */
#include "../armbianio.h"
%}

/* Parse the header file to generate wrappers */
%include "../armbianio.h"

/* Ignore AIOAddGPIOCallback since Swig generated function doesn't work */
%ignore AIOAddGPIOCallback;
