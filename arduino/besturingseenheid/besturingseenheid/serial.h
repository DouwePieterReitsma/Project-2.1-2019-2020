#ifndef SERIAL_H_
#define SERIAL_H_

#include <stdlib.h>

void init_serial_port(void);
void transmit(char value);
void transmit_message(const char* message);
char receive(void);
void receive_string(char* buffer, size_t size);

#endif /* SERIAL_COMMUNICATION_H_ */