#ifndef ULTRASONIC_SENSOR_H_
#define ULTRASONIC_SENSOR_H_

//defines pin numbers
#define ECHO_PORT 2 //PD2 (2)
#define TRIGGER_PORT 3 //PB3 (11)

void init_ultrasonic_sensor();

uint16_t get_distance();
void measure_distance();

#endif /* ULTRASONIC_SENSOR_H_ */