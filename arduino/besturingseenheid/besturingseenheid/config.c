#include "config.h"

#include <avr/io.h>
#include <avr/eeprom.h>
#include <string.h>

#define CONFIG_EEPROM_ADDRESS 0x0 // store the struct data at address 0 of the eeprom

Config device_config = {
	.max_unroll_distance = DEFAULT_MAX_UNROLL_DISTANCE,
	.min_unroll_distance = DEFAULT_MIN_UNROLL_DISTANCE,
	.temperature_threshold = DEFAULT_TEMPERATURE_THRESHOLD,
	.light_intensity_threshold = DEFAULT_LIGHT_INTENSITY_THRESHOLD,
	.automatic_mode = DEFAULT_AUTOMATIC_MODE_VALUE
};

void save_config(void)
{
	eeprom_busy_wait();
	
	eeprom_update_block(&device_config, CONFIG_EEPROM_ADDRESS, sizeof(Config));
}

void load_config(void)
{
	eeprom_busy_wait();
	
	eeprom_read_block(&device_config, CONFIG_EEPROM_ADDRESS, sizeof(Config));
}

void factory_reset(void)
{
	strcpy(device_config.device_name, DEFAULT_DEVICE_NAME);
	device_config.max_unroll_distance = DEFAULT_MAX_UNROLL_DISTANCE;
	device_config.min_unroll_distance = DEFAULT_MIN_UNROLL_DISTANCE;
	device_config.temperature_threshold = DEFAULT_TEMPERATURE_THRESHOLD;
	device_config.light_intensity_threshold = DEFAULT_LIGHT_INTENSITY_THRESHOLD;
	device_config.automatic_mode = DEFAULT_AUTOMATIC_MODE_VALUE;
	
	eeprom_busy_wait();
	
	eeprom_update_block(&device_config, CONFIG_EEPROM_ADDRESS, sizeof(Config));
}