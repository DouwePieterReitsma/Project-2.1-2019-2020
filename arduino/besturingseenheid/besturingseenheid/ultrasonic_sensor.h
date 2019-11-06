#ifndef ULTRASONIC_SENSOR_H_
#define ULTRASONIC_SENSOR_H_

//defines pin numbers
#define ECHO_PORT 6
#define TRIGGER_PORT 7

void init_ultrasonic_sensor();

int16_t get_distance();
void measure_distance();

#endif /* ULTRASONIC_SENSOR_H_ */