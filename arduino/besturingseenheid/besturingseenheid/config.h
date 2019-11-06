#ifndef CONFIG_H_
#define CONFIG_H_

typedef struct
{
	char device_name[51]; //50 characters + \0
	
	int max_unroll_distance;
	int min_unroll_distance;
	
	float temperature_threshold;
	float light_intensity_threshold;
	
	int automatic_mode;
} Config;

#define DEFAULT_DEVICE_NAME "Besturingseenheid"
#define DEFAULT_MAX_UNROLL_DISTANCE 100
#define DEFAULT_MIN_UNROLL_DISTANCE 10
#define DEFAULT_TEMPERATURE_THRESHOLD 22.0f
#define DEFAULT_LIGHT_INTENSITY_THRESHOLD 3
#define DEFAULT_AUTOMATIC_MODE_VALUE 1


extern Config device_config;

void factory_reset(void);
void save_config(void);
void load_config(void);

#endif