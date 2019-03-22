#include "mbed.h"

DigitalOut led1(LED1);

InterruptIn button1(USER_BUTTON);

volatile bool button1_pressed = false; 
volatile bool button1_enabled = true; 

Timeout button1_timeout;

void button1_enabled_cb(void) {
    button1_enabled = true;
}

void button1_onpressed_cb(void){
    if (button1_enabled) { 
        button1_enabled = false;
        button1_pressed = true; 
        button1_timeout.attach(callback(button1_enabled_cb), 0.3); 
    }
}

int main(){
    button1.fall(callback(button1_onpressed_cb)); 

    int idx = 0; 

    while(1) {
        if (button1_pressed) {
            button1_pressed = false;
            printf("Button pressed %d\n", idx++);
            led1 = !led1;
        }
    }
}
