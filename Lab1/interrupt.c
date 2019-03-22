#include "mbed.h"

InterruptIn button(USER_BUTTON);
DigitalOut led1(LED1);

double delay = 0.5; 

void pressed() {
    delay = 0.1;
}

void released() {
    delay = 0.5;
}

int main() {
    button.fall(&pressed);
    button.rise(&released);

    while (1) {
        led1 = !led1;
        wait(delay);
    }
}
