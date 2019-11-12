#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdio.h>

#define F_CPU 16E6
#include <util/delay.h>

#include <stdlib.h>
#include <string.h>
#include "serial.h"
#include "ultrasonic_sensor.h"

static volatile int pulse = 0;
static volatile int i = 0;

int16_t count_a = 0;

void init_ultrasonic_sensor()
{
	DDRB = 0b00001000;
	DDRD = 0b00000000;
	EICRA = (1<<ISC00);
	EIMSK = (1<<INT0);
}

uint16_t get_distance()
{
	return count_a;
}

void measure_distance()
{
	PORTB |= 1<<TRIGGER_PORT;
	_delay_us(10);
	PORTB &= ~(1<<TRIGGER_PORT);
	count_a = pulse / 7;
}

ISR(INT0_vect)
{
	if(i == 1)
	{
		TCCR1B = 0;
		pulse = TCNT1;
		TCNT1 = 0;
		i = 0;
	}

	if(i==0)
	{
		TCCR1B |= 1<<CS10;
		i = 1;
	}
}