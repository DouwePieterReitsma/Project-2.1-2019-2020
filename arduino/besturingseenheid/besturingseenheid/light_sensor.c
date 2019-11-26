#include "light_sensor.h"
#include "analog.h"
#include "serial.h"
#include "sensor_protocol.h"
#include "config.h"
#include "rolluik.h"

#define NUM_LIGHTINTENSITIES 30

float lightintensities[NUM_LIGHTINTENSITIES];
float averageLightIntensity = 0.0f;

void init_light_sensor(void)
{
	init_adc();
}

float get_light_intensity(void)
{
	int reading = read_analog_pin(LIGHT_ANALOG_PORT);
	
	float light = reading;
	
	return light;
}

float get_average_light_intensity(void)
{
	return averageLightIntensity;
}

void measure_light_intensity(void)
{
	static int index = 0;
	
	if(index == NUM_LIGHTINTENSITIES)
	{
		index = 0;
	}
	
	lightintensities[index] = get_light_intensity();
	
	index++;
}

void calculate_average_light_intensity(void)
{
	averageLightIntensity = 0.0f; // reset average light strength
	
	for(int i = 0; i < NUM_LIGHTINTENSITIES; i++)
	{
		averageLightIntensity += lightintensities[i];
	}
	
	averageLightIntensity /= NUM_LIGHTINTENSITIES;
	
	//// automatic controls
	if (device_config.automatic_mode)
	{
		if (averageLightIntensity >= device_config.light_intensity_threshold && !rolluik_is_rolled_down())
		{
			rolluik_going_down(10);
			rolluik_down();
		}
		else if(averageLightIntensity < device_config.light_intensity_threshold && rolluik_is_rolled_down())
		{
			rolluik_going_up(10);
			rolluik_up();
		}
	}
}