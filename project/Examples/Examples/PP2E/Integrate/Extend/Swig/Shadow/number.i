/********************************************************
 * Swig module description file for wrapping a C++ class.
 * Generate by saying "swig -python -shadow number.i".   
 * The C module is generated in file number_wrap.c; here,
 * module 'number' refers to the number.py shadow class.
 ********************************************************/

%module number

%{
#include "number.h"
%}

%include number.h
