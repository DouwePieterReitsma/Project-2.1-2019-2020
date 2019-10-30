#ifndef TEMPERATURE_SENSOR_H_
#define TEMPERATURE_SENSOR_H_

#define TEMPERATURE_ANALOG_PORT 1

void init_temperature_sensor(void);
float get_temperature_in_celsius(void);

// scheduler callback functions
void measure_temperature(void);
void calculate_average_temperature(void);


#endif /* TEMPERATURE_SENSOR_H_ */