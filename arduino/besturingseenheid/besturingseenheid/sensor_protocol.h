#ifndef SENSOR_DATA_H_
#define SENSOR_DATA_H_


typedef struct
{
	int light_intensity;
	float temperature;
	float distance;
} SensorData;

int serialize_sensor_data(SensorData* data, char* buffer);


#endif /* SENSOR_DATA_H_ */