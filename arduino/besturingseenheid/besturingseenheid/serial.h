#ifndef SERIAL_H_
#define SERIAL_H_

#include <avr/io.h>

#define SERIAL_INPUT_BUFFER_SIZE 100

extern char serial_input_buffer[SERIAL_INPUT_BUFFER_SIZE];

void init_serial_port(void);

//void serial_transmit(char value);
void serial_transmit(uint16_t value);
void serial_transmit_message(const char* message);

void serial_check_for_input(void);

int serial_string_ready(void);
void serial_get_string(char* buffer);


#endif /* SERIAL_COMMUNICATION_H_ */