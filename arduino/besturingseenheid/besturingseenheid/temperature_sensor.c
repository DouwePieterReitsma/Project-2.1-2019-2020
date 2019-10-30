/*
 * temperature_sensor.c
 *
 * Created: 2-11-2018 15:57:44
 *  Author: dprei
 */ 

#include "temperature_sensor.h"
#include "../common/analog.h"
#include "../common/serial.h"
#include "../common/sensor_protocol.h"

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
    
    float voltage = reading * (5.0f / 1024.0f);
    
    float temperature = (voltage - 0.5f) * 100;
    
    return temperature;
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
}

void transmit_average_temperature(void)
{
    char buffer[100];
    SensorData data;
    int result = 0;
    
    data.type = SENSOR_TYPE_TEMPERATURE;
    data.data.temperature = average_temperature;
    
    result = serialize_sensor_data(&data, buffer);
    
    if (result)
    {
        transmit_message(buffer);
    }
}