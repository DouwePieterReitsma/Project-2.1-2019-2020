#include <avr/delay.h>
#include <avr/io.h>

void init_rolluik_leds(void)
{
	uint8_t PORT_WRITE_ALL = 0b00001110;
	
	uint8_t temp = PORT_WRITE_ALL;
	DDRD = temp;
}

void rolluik_up(void)
{
	PORTD = 0b00000010;
}

void rolluik_down(void)
{
	PORTD = 0b00001000;
}

void rolluik_going(int time, int down) // down: 1 betekent dat hij omlaag gaat, 0 betekent dat hij omhoog gaat.
{
	/*
	if(down == 1)
	{
		for(int i = 0; i < time; i++)
		{
			PORTD = 0b00000100;
			_delay_ms(500);
			PORTD = 0b00001000;
			_delay_ms(500);
		}
		rolluik_down();
	}
	else if(down == 0)
	{
		for(int i = 0; i < time; i++)
		{
			PORTD = 0b00000100;
			_delay_ms(500);
			PORTD = 0b00000010;
			_delay_ms(500);
		}
		rolluik_up();
	}
	*/
}