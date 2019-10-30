/*
 * sensor_data.h
 *
 * Created: 5-11-2018 15:19:38
 *  Author: dprei
 */ 


#ifndef SENSOR_DATA_H_
#define SENSOR_DATA_H_

typedef enum
{
    SENSOR_TYPE_TEMPERATURE = 0,
    SENSOR_TYPE_LIGHT = 1,
    SENSOR_TYPE_DISTANCE = 2
} SensorType;

typedef struct
{
    SensorType type;
    
    union
    {
        float distance;
        float temperature;
        int light_intensity;
    } data;    
} SensorData;

int serialize_sensor_data(SensorData* data, char* buffer);


#endif /* SENSOR_DATA_H_ */