#include <avr/io.h>
#include <avr/sfr_defs.h>
#include <stdlib.h>

#define F_CPU 16E6
#include <util/delay.h>

void init_rolluik_leds(void)
{
	uint8_t PORT_WRITE_ALL = 0b00011100;
	
	uint8_t temp = PORT_WRITE_ALL;
	DDRD = temp;
}

void rolluik_up(void)
{
	PORTD = 0b00000100;
}

void rolluik_down(void)
{
	PORTD = 0b00010000;
}

void rolluik_going_down(int timer)
{
	for(int i = 0; i < timer; i++)
	{
		PORTD = 0b00011000;
		_delay_ms(500);
		PORTD = 0b00000000;
		_delay_ms(500);
	}
}

void rolluik_going_up(int timer)
{
	for(int i = 0; i < 15; i++)
	{
		PORTD = 0b00001100;
		_delay_ms(500);
		PORTD = 0b00000000;
		_delay_ms(500);
	}
}