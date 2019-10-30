#include "sensor_protocol.h"

#include <stdio.h>

int serialize_sensor_data(SensorData* data, char* buffer)
{
    if (data == NULL || buffer == NULL)
    {
        return 0;
    }
	
	sprintf(buffer, "1:%d:%f:%f\n", data->light_intensity, data->temperature, data->distance);
	
    return 1;
}