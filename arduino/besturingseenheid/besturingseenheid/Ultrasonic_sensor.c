#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdio.h>

#define F_CPU 16E6
#include <util/delay.h>

#include <stdlib.h>
#include <string.h>
#include "serial.h"
#include "ultrasonic_sensor.h"

volatile uint8_t wait = 0; // 0 means the result is not yet ready, 1 means the result is ready
volatile uint8_t ready = 0; // 0 means ready, 1 means not ready
volatile uint8_t acquire = 0; // 1 means you need the distance, 0 means you don't
volatile uint8_t distance = 0; // this is the distance u send out

ISR(INT0_vect)
{
	if(acquire == 1 && ready == 0 && (PIND & (1 << ECHO_PORT))) {
		TCCR0B |= (1 << CS01); // Enable Timer
		TCNT0 = 0; // Reset Timer
		ready = 1;
		acquire = 0;
	} else if(ready == 1 && ((PIND & (1 << ECHO_PORT)) == 0)) {
		TCCR0B &= ~(1 << CS01); // Disable Timer
		distance = TCNT0; // Count echo
		ready = 0;
		wait = 1;
	}
}

ISR(TIMER0_OVF_vect)
{
	TCCR0B &= ~(1 << CS01);
	wait = 1;
	ready = 0;
}

void init_ultrasonic_sensor()
{
	DDRB |= 0b00001000; // set port B as output
	TIMSK0 |= (1 << TOIE0); // Enable Timer1 overflow interrupts
	TCNT0 = 0;

	EICRA = (1 << ISC00);
	EIMSK = (1 << INT0);
	
	PCIFR |= bit (PCIF2);
	
	sei();
}

uint16_t get_distance()
{
	return distance;
}

void measure_distance()
{
	acquire = 1;
	PORTB |= (1 << TRIGGER_PORT);
	_delay_ms(60);
	PORTB &= (~(1 << TRIGGER_PORT));
	while(wait == 0);
	distance /= 58;
	distance /= 2;
}
