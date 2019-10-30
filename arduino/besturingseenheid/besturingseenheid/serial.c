/*
 * serial_communication.c
 *
 * Created: 2-11-2018 15:08:53
 *  Author: dprei
 */ 

#include "serial.h"

#include <avr/io.h>
#include <stdlib.h>
#include <avr/sfr_defs.h>

#define F_CPU 16E6
#include <util/delay.h>

#define UBRRVAL 51

void init_serial_port(void)
{
    //set baud rate 19200
    UBRR0H = 0;
    UBRR0L = UBRRVAL;
    
    //disable U2X mode
    UCSR0A = 0;
    
    //enable transmitter
    UCSR0B= _BV(RXEN0) | _BV(TXEN0);
    
    //set frame format : asynchronous, 8 data bits, 1 stop bit, no parity
    UCSR0C=_BV(UCSZ01)|_BV(UCSZ00);
}

void transmit(char value)
{
    loop_until_bit_is_set(UCSR0A, UDRE0);
    
    UDR0 = value;
}

void transmit_message(const char* message)
{
    for(; *message != '\0'; message++) 
        transmit(*message);       
}

char receive(void)
{
    loop_until_bit_is_set(UCSR0A, RXC0);
    
    return UDR0;
}