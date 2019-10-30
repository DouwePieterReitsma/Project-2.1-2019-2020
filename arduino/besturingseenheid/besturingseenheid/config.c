#include "config.h"

#include <avr/io.h>
#include <avr/eeprom.h>

#define CONFIG_EEPROM_ADDRESS 0x0 // store the struct data at address 0 of the eeprom

void set_config(Config* config)
{
    if(!config) return; // nothing to set if config equals null
    
    eeprom_busy_wait();
    
    eeprom_update_block(config, (void*)CONFIG_EEPROM_ADDRESS, sizeof(Config));
}

Config* get_config(void)
{
    Config* config = NULL;
    
    eeprom_busy_wait();
    
    eeprom_read_block(config, (void*)CONFIG_EEPROM_ADDRESS, sizeof(Config));
    
    //eeprom_read_block()
    
    return config;
}