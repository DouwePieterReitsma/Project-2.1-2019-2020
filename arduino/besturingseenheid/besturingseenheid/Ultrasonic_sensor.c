#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdio.h>

#define F_CPU 16E6
#include <util/delay.h>

#include <stdlib.h>
#include <string.h>
#include "serial.h"
#include "ultrasonic_sensor.h"

volatile uint8_t distancewanted = 0;
volatile uint8_t resultready = 0;
volatile uint8_t inprogress = 0;
volatile uint16_t echo = 0;

ISR(INT0_vect)
{
	if(distancewanted == 1 && inprogress == 0 && (PIND & (1<<PORTD2))) {
		TCCR1B |= (1<<CS11); // Enable Timer
		TCNT1 = 0; // Reset Timer
		inprogress = 1;
		distancewanted = 0;
		} else if(inprogress == 1 && ((PIND & (1<<PORTD2)) == 0)) {
		TCCR1B &= ~(1<<CS11); // Disable Timer
		echo = TCNT1; // Count echo
		inprogress = 0;
		resultready = 1;
	}
}

ISR(TIMER1_OVF_vect)
{
	TCCR1B &= ~(1 << CS11);
	resultready = 1;
	inprogress = 0;
}

void init_ultrasonic_sensor()
{
	DDRB |= 0b00001000; // set port B as output
	TIMSK1 |= (1 << TOIE1); // Enable Timer1 overflow interrupts
	TCNT1 = 0;

	EICRA = (1<<ISC00);
	EIMSK = (1<<INT0);
	
	sei();
}

uint16_t get_distance()
{
	distancewanted = 1;
	PORTB |= (1 << PORTB3);
	_delay_us(10);
	PORTB &= (~(1 << PORTB3));
	while(resultready == 0);
	//return echo / 15;
	echo /= 58;
	echo /= 2;
	return echo;
}
