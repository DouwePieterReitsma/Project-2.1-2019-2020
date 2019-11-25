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
#include "rolluik.h"
#include "ultrasonic_sensor.h"

void parse_python_input(void);

int main(void)
{
	init_serial_port();
	init_temperature_sensor();
	init_rolluik_leds();
	init_ultrasonic_sensor();
	init_light_sensor();

	load_config();

	
	SCH_Init_T1();
	
 	SCH_Add_Task(&measure_temperature, 0, 100); // measure temperature every second
 	SCH_Add_Task(&calculate_average_temperature, 400, 400); // calculate average temperature every 40 seconds
 	
 	SCH_Add_Task(&measure_light_intensity, 0, 100); // measure light intensity every second
 	SCH_Add_Task(&calculate_average_light_intensity, 300, 300); // measure light intensity every second

	SCH_Add_Task(&measure_distance, 0, 100);
	
	SCH_Add_Task(&test_rolluik_leds, 0, 1000);
	
	SCH_Add_Task(&transmit_sensor_data, 0, 1000); // test omdat 60 seconden te lang zijn
//	SCH_Add_Task(&transmit_sensor_data, 6000, 6000); // transmit sensor data temperature every 60 seconds
		
	SCH_Start();
	
	while(1)
	{
		/*
		rolluik_up();
		_delay_ms(500);
		rolluik_down();
		_delay_ms(500);
		rolluik_going_down(10);*/
		//test_rolluik_leds();
		SCH_Dispatch_Tasks();
	}
}

void parse_python_input(void)
{	
	serial_check_for_input();
	
	char buffer[SERIAL_INPUT_BUFFER_SIZE];
	
	if (serial_string_ready()) 
	{
		serial_get_string(buffer);
		
		parse_input(buffer);
	}
}