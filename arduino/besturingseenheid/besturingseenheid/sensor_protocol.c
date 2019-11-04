#include "sensor_protocol.h"

#include <stdio.h>
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

void process_command(DeviceCommand command, void* param)
{
	switch(command)
	{
		case SET_TEMPERATURE_THRESHOLD:
		transmit_message((char*)param);
		break;
		
		case SET_LIGHT_THRESHOLD:
		break;
		
		case SET_MAX_UNROLL_LENGTH:
		break;
		
		case SET_MIN_UNROLL_LENGTH:
		break;
		
		case SET_DEVICE_NAME:
		break;
		
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
	}
}