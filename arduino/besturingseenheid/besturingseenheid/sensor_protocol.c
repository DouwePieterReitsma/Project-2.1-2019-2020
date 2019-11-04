#include "sensor_protocol.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "serial.h"
#include "config.h"

int serialize_sensor_data(SensorData* data, char* buffer)
{
	if (data == NULL || buffer == NULL)
	{
		return 0;
	}
	
	sprintf(buffer, "1:%d:%f:%f\n", data->light_intensity, data->temperature, data->distance);
	
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
	switch(command)
	{
		case SET_TEMPERATURE_THRESHOLD:
		{
			device_config.temperature_threshold = atof(param);
			break;
		}
		
		case SET_LIGHT_THRESHOLD:
		{
			device_config.light_intensity_threshold = atof(param);
			break;
		}
		
		case SET_MAX_UNROLL_LENGTH:
		{
			device_config.max_unroll_distance = atoi(param);
			break;
		}
		
		case SET_MIN_UNROLL_LENGTH:
		{
			device_config.min_unroll_distance = atoi(param);
			break;
		}
		
		case SET_DEVICE_NAME:
		{
			strcpy(device_config.device_name, param);
			break;
		}
		
		case GET_TEMPERATURE_THRESHOLD:
		break;
		
		case GET_LIGHT_THRESHOLD:
		break;
		
		case GET_MAX_UNROLL_LENGTH:
		break;
		
		case GET_MIN_UNROLL_LENGTH:
		break;
		
		case GET_DEVICE_NAME:
		break;
		
		case TOGGLE_AUTOMATIC_MODE:
		break;
		
		case ROLL_SUNSHADES_UP:
		break;
		
		case ROLL_SUNSHADES_DOWN:
		break;
		
		default:
		return;
	}
	
	save_config();
}

