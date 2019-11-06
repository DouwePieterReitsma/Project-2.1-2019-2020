/*
 * besturingseenheid.c
 *
 * Created: 30-10-2019 14:46:02
 */ 

#define F_CPU 16000000UL

#include <avr/io.h>
#include <util/delay.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "temperature_sensor.h"
#include "light_sensor.h"
#include "sensor_protocol.h"
#include "AVR_TTC_scheduler.h"
#include "serial.h"
#include "config.h"

void parse_python_input(void);

int main(void)
{
	init_serial_port();
	init_temperature_sensor();
	
	load_config();
	
	DDRD |= (1 << PD2);
	
	SCH_Init_T1();
	
	SCH_Add_Task(&measure_temperature, 0, 100); // measure temperature every second
	SCH_Add_Task(&calculate_average_temperature, 4000, 4000); // calculate average temperature every 40 seconds
	
	SCH_Add_Task(&measure_light_intensity, 0, 100); // measure light intensity every second
	SCH_Add_Task(&calculate_average_light_intensity, 3000, 3000); // measure light intensity every second
	
	SCH_Add_Task(&transmit_sensor_data, 6000, 6000); // transmit sensor data temperature every 60 seconds
	
	SCH_Add_Task(&serial_check_for_input, 0, 1); // get characters
	SCH_Add_Task(&parse_python_input, 0, 1); // parse python input
		
	SCH_Start();
	
	while(1)
	{	
		SCH_Dispatch_Tasks();
	}
}

void parse_python_input(void)
{	
	char buffer[SERIAL_INPUT_BUFFER_SIZE];
	
	if (serial_string_ready()) 
	{
		serial_get_string(buffer);
		
		parse_input(buffer);
	}
}