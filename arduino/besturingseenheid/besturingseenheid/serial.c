/*
* serial_communication.c
*
* Created: 2-11-2018 15:08:53
*  Author: dprei
*/

#include "serial.h"

#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <avr/sfr_defs.h>

#define F_CPU 16E6
#include <util/delay.h>

#define UBRRVAL 51

char serial_input_buffer[SERIAL_INPUT_BUFFER_SIZE];
int is_string_ready = 0;

void init_serial_port(void)
{
<<<<<<< HEAD
    //set baud rate 19200
    UBRR0H = 0;
    UBRR0L = UBRRVAL;
    
    //disable U2X mode
    UCSR0A = 0;
    
    //enable transmitter
    UCSR0B = _BV(TXEN0) | _BV(RXEN0);
    
    //set frame format : asynchronous, 8 data bits, 1 stop bit, no parity
    UCSR0C = _BV(UCSZ01)|_BV(UCSZ00);
=======
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

void serial_transmit(char value)
{
	loop_until_bit_is_set(UCSR0A, UDRE0);
	
	UDR0 = value;
}

void serial_transmit_message(const char* message)
{
	for(; *message != '\0'; message++)
	serial_transmit(*message);
>>>>>>> master
}

void serial_check_for_input(void)
{
	static int i = 0;
	
	if(bit_is_set(UCSR0A, RXC0)) // check if there is serial input
	{
		char c = UDR0;
		
		if (c != EOF && i < SERIAL_INPUT_BUFFER_SIZE && !is_string_ready)
		{
			if (c == '\n')
			{
				serial_input_buffer[i] = '\0';
				
				i = 0;
				is_string_ready = 1;
			}
			else
			{
				serial_input_buffer[i++] = c;
			}
		}
	}
}

int serial_string_ready(void)
{
	return is_string_ready;
}

void serial_get_string(char* buffer)
{
<<<<<<< HEAD
    loop_until_bit_is_set(UCSR0A, RXC0);
    
	return UDR0;
=======
	if (!serial_string_ready()) return; // string not ready
	
	memcpy(buffer, serial_input_buffer, sizeof(serial_input_buffer)); // copy input buffer
	
	memset(serial_input_buffer, 0, SERIAL_INPUT_BUFFER_SIZE); // clear input buffer
	
	is_string_ready = 0;
>>>>>>> master
}