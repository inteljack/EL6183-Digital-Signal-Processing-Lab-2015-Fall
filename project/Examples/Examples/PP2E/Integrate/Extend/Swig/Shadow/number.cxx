#include "number.h"
#include "iostream.h"
// #include "stdio.h"

Number::Number(int start) { 
   data = start; 
   cout << "Number: " << data << endl;    // cout and printf both work
   // printf("Number: %d\n", data);       // python print goes to stdout
}

Number::~Number() { 
   cout << "~Number: " << data << endl; 
}

void Number::add(int value) { 
   data += value; 
   cout << "add " << value << endl; 
}

void Number::sub(int value) { 
   data -= value; 
   cout << "sub " << value << endl; 
}

void Number::display() { 
   cout << "Number = " << data << endl; 
}
