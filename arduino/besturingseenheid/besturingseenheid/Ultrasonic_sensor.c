#include <avr/io.h>
#include <avr/interrupt.h>

#define F_CPU 10E6
#include <util/delay.h>

#include <stdlib.h>

// defines variables
static volatile int pulse = 0;
static volatile int i = 0;
int16_t distance = 0;
int16_t COUNTA = 0; // storing digital output


void init_ultrasonic_sensor()
{
	DDRD = 0xff;
	_delay_ms(50);
	
	EIMSK |= (1 << INT0); // enabling interrupt0
	EICRA |= (1 << ISC00); // setting interrupt triggering logic change
	
	sei();
}

ISR(INT0_vect) // interrupt service routine when there is a change in logic level
{
	if(i == 1) // when logic from HIGH to LOW
	{
		TCCR1B = 0; // disabling counter
		pulse = TCNT1; // count memory is updated to integer
		TCNT1 = 0; // resetting the counter memory
		i = 0;
	}
	if(i == 0) // when logic change is from LOW to HIGH
	{
		TCCR1B |= (1 << CS10); // enabling counter
		i = 1;
	}
}

int16_t get_distance()
{
	return distance;
}

void measure_distance()
{
	PORTD |= (1 << PIND2);
	_delay_us(15);
	PORTD &= ~(1 << PIND2);
	
	COUNTA = pulse / 58; // getting the distance based on formula
	
	distance = COUNTA;
}