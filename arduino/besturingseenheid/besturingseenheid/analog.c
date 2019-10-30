#include "analog.h"

#include <avr/io.h>

void init_adc(void)
{
    ADMUX = (1 << REFS0);
    ADCSRA = (1 << ADEN) | 7; // enable analog-to-digital converter and set prescaler to 128
}

uint16_t read_analog_pin(uint8_t pin)
{
    ADMUX = (1 << REFS0) | (pin & 0x0f);
    ADCSRA |= (1 << ADSC);
    
    loop_until_bit_is_clear(ADCSRA, ADSC);
    
    return ADCW;
}