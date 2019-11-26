#ifndef ROLLUIK_H_
#define ROLLUIK_H_

#define GREEN_LED_PORT 4
#define YELLOW_LED_PORT 5
#define RED_LED_PORT 6

void init_rolluik_leds(void);
void rolluik_up(void);
void rolluik_down(void);
void rolluik_going_down(int timer);
void rolluik_going_up(int timer);

int rolluik_is_rolled_down(void);
void test_rolluik_leds(void);
void turn_off_all_leds(void);

#endif /* ROLLUIK_H_ */