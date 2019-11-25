#include <avr/io.h>
#include <avr/sfr_defs.h>
#include <stdlib.h>

#define F_CPU 16E6
#include <util/delay.h>

#include "serial.h"
#include "rolluik.h"

int is_rolled_down = 0;

void init_rolluik_leds(void)
{
	DDRD = ((1 << GREEN_LED_PORT) | (1 << YELLOW_LED_PORT) | (1 << RED_LED_PORT));
}

void rolluik_up(void) // Turn on green led
{
	turn_off_all_leds();
	
	PORTD |= (1 << GREEN_LED_PORT);
	
	is_rolled_down = 0;
}

void rolluik_down(void) // Turn on red led
{
	turn_off_all_leds();
	
	PORTD |= (1 << RED_LED_PORT);
	
	is_rolled_down = 1;
}

void rolluik_going_down(int timer) // blink yellow red led
{
	turn_off_all_leds();

	for(int i = 0; i < timer; i++)
	{
		PORTD |= (1 << YELLOW_LED_PORT) | (1 << RED_LED_PORT);
		_delay_ms(500);
		turn_off_all_leds();
		_delay_ms(500);
	}
	rolluik_down();
}

void rolluik_going_up(int timer) // blink green yellow led
{
	turn_off_all_leds();
	
	for(int i = 0; i < timer; i++)
	{
		PORTD |= (1 << GREEN_LED_PORT) | (1 << YELLOW_LED_PORT);
		_delay_ms(500);
		turn_off_all_leds();
		_delay_ms(500);
	}
	rolluik_up();
}

int rolluik_is_rolled_down(void)
{
	return is_rolled_down;
}

void test_rolluik_leds(void)
{
	if(is_rolled_down == 0)
	{
		rolluik_going_down(2);
	}
	else if(is_rolled_down == 1)
	{
		rolluik_going_up(2);
	}
}

void turn_off_all_leds(void)
{
	PORTD &= ~((1 << GREEN_LED_PORT) | (1 << YELLOW_LED_PORT) | (1 << RED_LED_PORT));
}