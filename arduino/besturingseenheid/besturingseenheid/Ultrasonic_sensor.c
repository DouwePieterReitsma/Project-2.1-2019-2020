#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdio.h>

#define F_CPU 16E6
#include <util/delay.h>

#include <stdlib.h>
#include <string.h>
#include "serial.h"
#include "ultrasonic_sensor.h"

/*// Begin werkende zonder scheduler deel
volatile uint8_t acquiredistance = 0; // 1 betekent dat je de afstand wilt hebben, 0 betekent dat er niet om gevraagd is(of je al gevraagt hebt)
volatile uint8_t ready = 0; // 1 betekent dat er een resultaat klaar staat, 0 niet
volatile uint8_t busy = 0; // 1 betekent dat je nog bezig bent, 0 betekent 
volatile uint16_t distance = 0; // dit is de afstand die je meegeeft

ISR(INT0_vect)
{
	if(acquiredistance == 1 && busy == 0 && (PIND & (1<<PORTD2))) {
		TCCR1B |= (1<<CS11); // Enable Timer
		TCNT1 = 0; // Reset Timer
		busy = 1;
		acquiredistance = 0;
		} else if(busy == 1 && ((PIND & (1<<PORTD2)) == 0)) {
		TCCR1B &= ~(1<<CS11); // Disable Timer
		distance = TCNT1; // Count echo
		busy = 0;
		ready = 1;
	}
}

ISR(TIMER1_OVF_vect)
{
	TCCR1B &= ~(1 << CS11);
	ready = 1;
	busy = 0;
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
	return distance;
}

void measure_distance()
{
	acquiredistance = 1;
	PORTB |= (1 << PORTB3);
	_delay_us(10);
	PORTB &= (~(1 << PORTB3));
	while(ready == 0);
	distance /= 58;
	distance /= 2;
}
*/ // Einde werkende zonder scheduler deel

// Begin test met andere timer
static volatile int pulse = 0;
static volatile int i = 0;

int16_t count_a = 0;

void init_ultrasonic_sensor()
{
	//sei();
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
	PORTB |= 1<<PINB3;
	_delay_us(10);
	PORTB &= ~(1<<PINB3);
	count_a = pulse/58;
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
// Einde test met andere timer
