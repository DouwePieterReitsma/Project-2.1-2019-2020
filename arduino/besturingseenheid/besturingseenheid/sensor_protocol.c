#include "sensor_protocol.h"

#include <stdio.h>

int serialize_sensor_data(SensorData* data, char* buffer)
{
    if (data == NULL)
    {
        return 0;
    }
    
    switch(data->type)
    {
        case SENSOR_TYPE_TEMPERATURE:
            sprintf(buffer, "%d:%f\r\n", data->type, data->data.temperature);
            break;
        case SENSOR_TYPE_LIGHT:
            sprintf(buffer, "%d:%d\r\n", data->type, data->data.light_intensity);
            break;
        case SENSOR_TYPE_DISTANCE:
            sprintf(buffer, "%d:%f\r\n", data->type, data->data.distance);
            break;
        default:
            return 0;
    }
    
    return 1;
}