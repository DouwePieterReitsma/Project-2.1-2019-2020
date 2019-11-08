#include "temperature_sensor.h"
#include "analog.h"
#include "serial.h"
#include "sensor_protocol.h"
#include "config.h"
#include "rolluik.h"

#define NUM_TEMPERATURES 40

float temperatures[NUM_TEMPERATURES];
float average_temperature = 0.0f;

void init_temperature_sensor(void)
{
    init_adc();    
}

float get_temperature_in_celsius(void)
{
    int reading = read_analog_pin(TEMPERATURE_ANALOG_PORT);
    
    //float voltage = reading * (5.0f / 1024.0f);
    float voltage = reading * 5.0f / 1024.0f;
    
    float temperature = (voltage - 0.5f) * 100;
    
    return temperature;
}

float get_average_temperature_in_celsius(void)
{
	return average_temperature;
}

void measure_temperature(void)
{
    static int index = 0;
    
    if(index == NUM_TEMPERATURES)
    {
        index = 0;
    }
    
    temperatures[index] = get_temperature_in_celsius();
    
    index++;
}

void calculate_average_temperature(void)
{
    average_temperature = 0.0f; // reset average temperature
    
    for(int i = 0; i < NUM_TEMPERATURES; ++i)
    {
        average_temperature += temperatures[i];
    }
    
    average_temperature /= NUM_TEMPERATURES;
	
	
	//// automatic controls
	//if (device_config.automatic_mode)
	//{
		//if (average_temperature >= device_config.temperature_threshold && !rolluik_is_rolled_down())
		//{
			//rolluik_going_down(10);
			//rolluik_down();
		//}
		//else if(average_temperature < device_config.temperature_threshold && rolluik_is_rolled_down())
		//{
			//rolluik_going_up(10);
			//rolluik_up();
		//}
	//}
}