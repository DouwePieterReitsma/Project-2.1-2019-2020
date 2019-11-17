#include "sensor_protocol.h"

#include <avr/io.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "serial.h"
#include "config.h"
#include "temperature_sensor.h"
#include "light_sensor.h"
#include "rolluik.h"
#include "ultrasonic_sensor.h"

int serialize_sensor_data(SensorData* data, char* buffer)
{
	if (data == NULL || buffer == NULL)
	{
		return 0;
	}
	
	sprintf(buffer, "1:%d:%f:%f\r\n", data->light_intensity, data->temperature, data->distance);
	
	return 1;
}

int parse_input(char* input)
{
	int command = -1;
	char param[100];
	
	if (input == NULL) return 0;
	
	sscanf(input, "%d:%s", &command, param);
	
	process_command(command, param);
	
	return 1;
}

void process_command(DeviceCommand command, char* param)
{
	char buffer[100];
	
	switch(command)
	{
		case SET_TEMPERATURE_THRESHOLD:
		{
			device_config.temperature_threshold = atof(param);
			
			save_config();
			break;
		}
		
		case SET_LIGHT_THRESHOLD:
		{
			device_config.light_intensity_threshold = atof(param);
			
			save_config();
			break;
		}
		
		case SET_MAX_UNROLL_LENGTH:
		{
			device_config.max_unroll_distance = atoi(param);
			
			save_config();
			break;
		}
		
		case SET_MIN_UNROLL_LENGTH:
		{
			device_config.min_unroll_distance = atoi(param);
			
			save_config();
			break;
		}
		
		case SET_DEVICE_NAME:
		{
			strcpy(device_config.device_name, param);
			
			save_config();
			break;
		}
		
		case GET_TEMPERATURE_THRESHOLD:
		{
			sprintf(buffer, "0:%d:%f\r\n", GET_TEMPERATURE_THRESHOLD, device_config.temperature_threshold);
			
			serial_transmit_message(buffer);
			
			break;
		}
		
		case GET_LIGHT_THRESHOLD:
		{
			sprintf(buffer, "0:%d:%f\r\n", GET_LIGHT_THRESHOLD, device_config.light_intensity_threshold);
			
			serial_transmit_message(buffer);
			
			break;
		}
		
		case GET_MAX_UNROLL_LENGTH:
		{
			sprintf(buffer, "0:%d:%d\r\n", GET_MAX_UNROLL_LENGTH, device_config.max_unroll_distance);
			
			serial_transmit_message(buffer);
			
			break;
		}
		
		
		case GET_MIN_UNROLL_LENGTH:
		{
			sprintf(buffer, "0:%d:%d\r\n", GET_MIN_UNROLL_LENGTH, device_config.min_unroll_distance);
			
			serial_transmit_message(buffer);
			
			break;
		}
		
		case GET_DEVICE_NAME:
		{
			sprintf(buffer, "0:%d:%s\r\n", GET_DEVICE_NAME, device_config.device_name);
			
			serial_transmit_message(buffer);
			
			break;
		}
		
		case TOGGLE_AUTOMATIC_MODE:
		{
			device_config.automatic_mode = !device_config.automatic_mode;
			
			break;
		}
		
		case ROLL_SUNSHADES_UP:
		{
			if (device_config.automatic_mode == 0)
			{
				rolluik_going_up(10);
				rolluik_up();
			}
			else
			{
				error_message("Manual mode not enabled.");
			}
			
			break;
		}
		
		case ROLL_SUNSHADES_DOWN:
		{
			if (device_config.automatic_mode == 0)
			{
				rolluik_going_down(10);
				rolluik_down();
			}
			else
			{
				error_message("Manual mode not enabled.");
			}
			
			break;
		}
		
		case FACTORY_RESET:
		{
			factory_reset();
			
			break;
		}
		
		default:
		return;
	}
}

void error_message(const char* message)
{
	char buffer[100];
	
	sprintf(buffer, "3:%s\r\n", message);
	
	serial_transmit_message(buffer);
}

void transmit_sensor_data(void)
{
	SensorData data;
	
	data.temperature = get_average_temperature_in_celsius();
	data.light_intensity = get_average_light_intensity();
	data.distance = get_distance();
	
	if (device_config.automatic_mode) {
		if ((data.temperature >= device_config.temperature_threshold || data.light_intensity >= device_config.light_intensity_threshold) && !rolluik_is_rolled_down())
		{
			rolluik_going_down(10);
			rolluik_down();
		}
		else if ((data.temperature < device_config.temperature_threshold || data.light_intensity < device_config.light_intensity_threshold) && rolluik_is_rolled_down())
		{
			rolluik_going_up(10);
			rolluik_up();
		}
	}
	
	char buffer[100];
	
	serialize_sensor_data(&data, buffer);
	
	serial_transmit_message(buffer);
}