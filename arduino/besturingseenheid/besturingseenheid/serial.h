#ifndef SERIAL_H_
#define SERIAL_H_

void init_serial_port(void);
void transmit(char value);
void transmit_message(const char* message);
char receive(void);

#endif /* SERIAL_COMMUNICATION_H_ */