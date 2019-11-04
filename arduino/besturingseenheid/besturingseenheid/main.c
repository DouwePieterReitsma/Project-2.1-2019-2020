/*
 * besturingseenheid.c
 *
 * Created: 30-10-2019 14:46:02
 */ 

#include <avr/io.h>
#include <avr/delay.h>

#include "rolluik.h"
#include "temperature_sensor.h"
#include "light_sensor.h"
#include "temperature_sensor.h"
#include "light_sensor.h"
#include "sensor_protocol.h"
#include "AVR_TTC_scheduler.h"
#include "serial.h"

void test(void);

int main(void)
{
	init_serial_port();
	init_rolluik_leds();
	init_temperature_sensor();
	init_light_sensor();
	init_light_sensor();
	
	/*
	SCH_Init_T1();
	
	SCH_Add_Task(&measure_temperature, 0, 100); // measure temperature every second
	SCH_Add_Task(&calculate_average_temperature, 4000, 4000); // calculate average temperature every 40 seconds
	SCH_Add_Task(&measure_light_intensity, 0, 100); // measure lightintensity every second
	SCH_Add_Task(&calculate_average_light_intensity, 3000, 3000); // calculate average temperature every 30 seconds
	
	SCH_Add_Task(&test, 6000, 6000); // transmit sensor data temperature every 60 seconds
	
	SCH_Start();
	*/
	while(1)
	{
		//SCH_Dispatch_Tasks();
		//transmit(get_average_light_intensity());
		//_delay_ms(10000);
		transmit(get_average_temperature_in_celsius());
		_delay_ms(10000);
	}
}
/*
void test(void)
{
	rolluik_down();
	
	SensorData data;
		
	data.temperature = 0; //get_average_temperature_in_celsius();
	data.light_intensity = get_average_light_intensity(); //0;
	data.distance = 0;
	
	char buffer[100];
	
	serialize_sensor_data(&data, buffer);
	transmit_message(buffer);
}
*/