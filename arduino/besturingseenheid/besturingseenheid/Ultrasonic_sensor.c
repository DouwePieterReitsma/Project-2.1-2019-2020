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
	return echo;
}


/*
uint16_t counter = 0;

float previous_distance;
float distance;

void init_ultrasonic_sensor()
{
	DDRD &= ~(1 << ECHO_PORT);
	DDRD |= (1 << TRIGGER_PORT);
	
	PORTD &= ~(1 << TRIGGER_PORT);
	
	PCICR = (1 << PCIE0);
	PCMSK0 |= (1 << PCINT18);
	sei();
}

void measure_distance()
{
	counter = 0;
	
	PORTD |= (1 << TRIGGER_PORT);
	_delay_us(10);
	PORTD &= ~(1 << TRIGGER_PORT);
}

ISR(TIMER0_OVF_vect)
{
	counter += 255;
}

ISR(INT0_vect)
{
	if(bit_is_set(PIND, ECHO_PORT))
	{
		TCCR0B |= (1 << CS01);
		TIMSK0 |= (1 << TOIE0);
		
		TCNT0 = 0;
	} else {
		cli();
		
		TCCR0B &= ~(1 << CS01);
		counter += TCNT0;
		distance = (float)counter / 58.0f / 2.0f;
	}
}

uint16_t get_distance()
{
	return distance;
}
*/
/*
int TimerOverFlow = 0;

char string[10];
long count;
double distance;

init_ultrasonic_sensor()
{
	DDRD = 0x01;
	PORTB = 0xff;
	sei();
	TIMSK1 = (1 << TOIE1);
	TCCR1A = 0;
}

ISR(TIMER1_OVF_vect)
{
	TimerOverFlow++;
}

double get_distance()
{
	return distance;
}

void measure_distance()
{
	PORTD |= (1 << PIND0);
	_delay_us(10);
	PORTD &= (~(1 << PIND0));
	
	TCNT1 = 0;
	TCCR1B = 0x41;
	TIFR1 = 1 << ICF1;
	TIFR1 = 1 << TOV1;
	
	while((TIFR1 & (1 << ICF1)) == 0);
	TCNT1 = 0;
	TCCR1B = 0x01;
	TIFR1 = 1 << ICF1;
	TIFR1 = 1 << TOV1;
	TimerOverFlow = 0;
	
	while((TIFR1 & (1 << ICF1)) == 0);
	count = ICR1 + (65535 * TimerOverFlow);
	distance = (double)count / 466.47;
}

*/
/*
// defines variables
static volatile int pulse = 0;
static volatile int i = 0;
uint16_t distance = 0;
uint16_t COUNTA = 0; // storing digital output
char buffer[100];



void init_ultrasonic_sensor()
{
	DDRD = 0b11111011;
	
	_delay_ms(50);
	
	EIMSK |= (1 << INT0); // enabling interrupt1
	EICRA |= (1 << ISC00); // setting interrupt triggering logic change
	
	TCCR1A = 0;
	
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

const char* get_distance()
{	
	char SHOWA;
	itoa(distance, SHOWA, 10);
	return SHOWA;
	//sprintf(buffer, "%d\r\n", distance);
	//return buffer;
}

void measure_distance()
{
	PORTD |= (1 << PIND0);
	_delay_us(15);
	PORTD &= ~(1 << PIND0);
	
	COUNTA = pulse / 58; // getting the distance based on formula
	
	distance = COUNTA;
}
*/