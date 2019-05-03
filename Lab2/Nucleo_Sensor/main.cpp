#include "mbed.h"
#include "x_cube_mems.h"
#include "x_cube_mems_i2c.h"

DigitalOut myled(LED1);
Serial pc(USBTX, USBRX);

volatile float TEMPERATURE_C;
volatile float TEMPERATURE_F;
volatile float TEMPERATURE_K;
volatile float HUMIDITY;
volatile float PRESSURE;

Ticker sensor_update;
Ticker led_toggle;

bool measurements_update = false;

void sensor_handle() {
    measurements_update = true;
}

void led_handle() {
    myled = !myled;
}

int main() {
    static X_CUBE_MEMS *mems_expansion_board = X_CUBE_MEMS::Instance();
    sensor_update.attach(&sensor_handle, 3);
    led_toggle.attach(&led_handle, 1);
    
    while(1) {
        if (measurements_update) {
            mems_expansion_board->hts221.GetTemperature((float *)&TEMPERATURE_C);
            mems_expansion_board->hts221.GetHumidity((float *)&HUMIDITY);
            mems_expansion_board->lps25h.GetPressure((float *)&PRESSURE);
            
            TEMPERATURE_F = (TEMPERATURE_C * 9.0f / 5.0f) + 32.0f;
            TEMPERATURE_K = TEMPERATURE_C + 273.15f;
            
            pc.printf("Temperature(C): %f\n", TEMPERATURE_C);
            pc.printf("Temperature(F): %f\n", TEMPERATURE_F);
            pc.printf("Temperature(K): %f\n", TEMPERATURE_K);
            pc.printf("Humidity: %f\n", HUMIDITY);
            pc.printf("Pressure: %f\n", PRESSURE);
            measurements_update = false;
        }
    }
}
