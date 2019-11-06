#ifndef ROLLUIK_H_
#define ROLLUIK_H_

#define GREEN_LED_PORT 2
#define YELLOW_LED_PORT 3
#define RED_LED_PORT 4

void init_rolluik_leds(void);
void rolluik_up(void);
void rolluik_down(void);
void rolluik_going_down(int timer);
void rolluik_going_up(int timer);

#endif /* ROLLUIK_H_ */