/*
 * besturingseenheid.c
 *
 * Created: 30-10-2019 14:46:02
 */ 

#include <avr/io.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <avr/sfr_defs.h>

#define F_CPU 16E6
#include <util/delay.h>

#include "light_sensor.h"
#include "temperature_sensor.h"
//#include "sensor_protocol.h"
//#include "AVR_TTC_scheduler.h"
#include "serial.h"
//#include "config.h"
#include "rolluik.h"

void test();
void test2();
void test3();
//void test(void);
//void test2(void);
//void serial_receiver(void);

int main(void)
{
	init_serial_port();
	_delay_ms(1000);
	init_temperature_sensor();
	_delay_ms(1000);
	init_light_sensor();
	_delay_ms(1000);
	init_rolluik_leds();
	_delay_ms(1000);
	DDRD = 0xff;
	
	//SCH_Init_T1();
	
	//SCH_Add_Task(&measure_temperature, 0, 100); // measure temperature every second
	//SCH_Add_Task(&calculate_average_temperature, 4000, 4000); // calculate average temperature every 40 seconds
	//SCH_Add_Task(&test, 100, 100); // transmit sensor data temperature every 60 seconds
	
	//SCH_Add_Task(&serial_receiver, 0, 1);
	//SCH_Add_Task(&test2, 0, 500);
	
	//device_config.temperature_threshold = 15.0f;
	
	//save_config();
	
	//SCH_Start();
	
	//int value = 12;
	
	while(1)
	{
		test();	// test de temperatuur
		test2(); // test de licht intensiteit
		test3(); // test de LEDs
	}
}

void test() // test de temperatuur
{
	float temperatures[40];
	float average_temperature = 0.0f;

	for(int i = 0; i < 40; i++)
	{
		temperatures[i] = get_temperature_in_celsius();
		average_temperature += temperatures[i];
		_delay_ms(1000);
	}
	average_temperature /= 40;
	
	transmit(average_temperature);
	_delay_ms(1000);
}

void test2() // test de licht intensiteit
{
	float light_intensities[30];
	float average_light_intensity = 0.0f;
	
	for(int i = 0; i < 30; i++)
	{
		light_intensities[i] = get_light_intensity();
		average_light_intensity += light_intensities[i];
		_delay_ms(1000);
	}
	average_light_intensity /= 30;
	
	transmit(average_light_intensity);
	_delay_ms(1000);
}

void test3() // test de LEDs
{
	rolluik_going_down(15);
	rolluik_going_up(15);
}
/*
void test(void)
{
	SensorData data;
	
	data.temperature = get_temperature_in_celsius();
	data.light_intensity = 0;
	data.distance = 0;
	
	char buffer[100];
	
	serialize_sensor_data(&data, buffer);
	
	transmit_message(buffer);
}

void test2(void)
{
	char buffer[100];
	sprintf(buffer, "Output: %f\r\n", device_config.temperature_threshold);
	
	transmit_message(buffer);
}

void serial_receiver(void)
{	
	#define BUFFER_SIZE 100
	char buffer[BUFFER_SIZE];
	int command = -1;
	float param;
	
	receive_string(buffer, BUFFER_SIZE);
	
	sscanf(buffer, "%d:%f", &command, &param);
	
	process_command_with_param(command, &param);
}
*/