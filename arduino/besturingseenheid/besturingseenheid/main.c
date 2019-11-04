/*
 * besturingseenheid.c
 *
 * Created: 30-10-2019 14:46:02
 */ 

#include <avr/io.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "temperature_sensor.h"
#include "sensor_protocol.h"
#include "AVR_TTC_scheduler.h"
#include "serial.h"
#include "config.h"

void test(void);
void test2(void);
void serial_receiver(void);

int main(void)
{
	init_serial_port();
	init_temperature_sensor();
	
	load_config();
	
	SCH_Init_T1();
	
	//SCH_Add_Task(&measure_temperature, 0, 100); // measure temperature every second
	//SCH_Add_Task(&calculate_average_temperature, 4000, 4000); // calculate average temperature every 40 seconds
	//SCH_Add_Task(&test, 6000, 6000); // transmit sensor data temperature every 60 seconds
	
	SCH_Add_Task(&serial_receiver, 0, 1);
	SCH_Add_Task(&test2, 0, 500);
	
	//device_config.temperature_threshold = 15.0f;
	
	//save_config();
	
	SCH_Start();
	
	while(1)
	{
		SCH_Dispatch_Tasks();
	}
}

void test(void)
{
	SensorData data;
	
	data.temperature = get_average_temperature_in_celsius();
	data.light_intensity = 0;
	data.distance = 0;
	
	char buffer[100];
	
	serialize_sensor_data(&data, buffer);
	
	transmit_message(buffer);
}

void test2(void)
{
	char buffer[100];
	sprintf(buffer, "Device Name: %s\r\nTemperature Threshold: %f\r\n", device_config.device_name, device_config.temperature_threshold);
	
	transmit_message(buffer);
}

void serial_receiver(void)
{	
	#define BUFFER_SIZE 100
	char buffer[BUFFER_SIZE];
	//int command = -1;
	//float param;
	
	receive_string(buffer, BUFFER_SIZE);
	
	parse_input(buffer);
	
	//sscanf(buffer, "%d:%f", &command, &param);
	
	//process_command(command, &param);
}