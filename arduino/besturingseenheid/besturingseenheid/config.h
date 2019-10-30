#ifndef CONFIG_H_
#define CONFIG_H_

typedef struct 
{
    char uuid[37]; //36 characters + \0 
    int max_unroll_distance;
    int min_unroll_distance;
} Config;

void set_config(Config* config);
Config* get_config(void);

#endif