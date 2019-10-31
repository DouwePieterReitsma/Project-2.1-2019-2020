#ifndef LIGHT_SENSOR_H_
#define LIGHT_SENSOR_H_

#define LIGHT_ANALOG_PORT 0

void init_light_sensor(void);
float get_light_intensity(void);
float get_average_light_intensity(void);


// scheduler callback functions
void measure_light_intensity(void);
void calculate_average_light_intensity(void);


#endif /* LIGHT_SENSOR_H_ */