#ifndef ULTRASONIC_SENSOR_H_
#define ULTRASONIC_SENSOR_H_

//defines pin numbers
#define ECHO_PORT 2
#define TRIGGER_PORT 3

void init_ultrasonic_sensor();

char get_distance();
void measure_distance();

#endif /* ULTRASONIC_SENSOR_H_ */