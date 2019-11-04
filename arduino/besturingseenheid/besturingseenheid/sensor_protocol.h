#ifndef SENSOR_DATA_H_
#define SENSOR_DATA_H_


typedef struct
{
	int light_intensity;
	float temperature;
	float distance;
} SensorData;

typedef enum {
	SET_TEMPERATURE_THRESHOLD = 0,
	SET_LIGHT_THRESHOLD = 1,
	SET_MAX_UNROLL_LENGTH = 2,
	SET_MIN_UNROLL_LENGTH = 3,
	SET_DEVICE_NAME = 4,
	GET_TEMPERATURE_THRESHOLD = 5,
	GET_LIGHT_THRESHOLD = 6,
	GET_MAX_UNROLL_LENGTH = 7,
	GET_MIN_UNROLL_LENGTH = 8,
	GET_DEVICE_NAME = 9,
	TOGGLE_AUTOMATIC_MODE = 10,
	ROLL_SUNSHADES_UP = 11,
	ROLL_SUNSHADES_DOWN = 12
} DeviceCommand;

int serialize_sensor_data(SensorData* data, char* buffer);

int parse_input(char* buffer, DeviceCommand* command, void* param);

void process_command(DeviceCommand command);
void process_command_with_param(DeviceCommand command, void* param);


#endif /* SENSOR_DATA_H_ */