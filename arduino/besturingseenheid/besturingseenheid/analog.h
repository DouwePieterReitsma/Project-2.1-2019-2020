#ifndef ANALOG_H
#define ANALOG_H

#include <stdint.h>

void init_adc(void);
uint16_t read_analog_pin(uint8_t pin);

#endif