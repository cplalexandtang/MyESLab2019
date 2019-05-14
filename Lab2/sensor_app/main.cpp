#include "mbed.h"
#include "XNucleoIKS01A2.h"

DigitalOut myled(LED1);
Serial pc(USBTX, USBRX);

static XNucleoIKS01A2 *mems_expansion_board = XNucleoIKS01A2::instance();

volatile float TEMPERATURE_C;
volatile float TEMPERATURE_F;
volatile float TEMPERATURE_K;
volatile float HUMIDITY;
volatile float PRESSURE;
volatile float WIND_DIRECTION;
volatile int32_t MAGNETIC[3];

Ticker sensor_ticker;
Ticker led_ticker;

bool measurements_update = false;

void sensor_handle() {
    measurements_update = true;
}

void led_handle() {
    myled = !myled;
}

int main() {
    sensor_ticker.attach(&sensor_handle, 3);
    led_ticker.attach(&led_handle, 0.5);
    
    mems_expansion_board->ht_sensor->enable();
    mems_expansion_board->pt_sensor->enable();
    mems_expansion_board->magnetometer->enable();
    
    while(1) {
        if (measurements_update) {
            mems_expansion_board->ht_sensor->get_temperature((float *)&TEMPERATURE_C);
            mems_expansion_board->ht_sensor->get_humidity((float *)&HUMIDITY);
            mems_expansion_board->pt_sensor->get_pressure((float *)&PRESSURE);
            mems_expansion_board->magnetometer->get_m_axes((int32_t *)MAGNETIC);
            
            
            int32_t magnitude = MAGNETIC[0] * MAGNETIC[0] + MAGNETIC[1] * MAGNETIC[1];
            int32_t magnitude_x = MAGNETIC[0] * MAGNETIC[0];
            float angle = 0;
            if ((float)magnitude_x / (float)magnitude < 0.15f) {
                angle = 0;
            } else if ((float)magnitude_x / (float)magnitude >= 0.85f) {
                angle = 90;
            } else {
                angle = 45;
            }
            
            if (MAGNETIC[0] > 0 && MAGNETIC[1] > 0) {
                WIND_DIRECTION = angle;
            } else if (MAGNETIC[0] <= 0 && MAGNETIC[1] > 0){
                WIND_DIRECTION = 360 - angle;
            } else if (MAGNETIC[0] > 0 && MAGNETIC[1] <= 0) {
                WIND_DIRECTION = -1 * angle + 180;
            } else if (MAGNETIC[0] <= 0 && MAGNETIC[1] <= 0) {
                WIND_DIRECTION = angle + 180;
            } 
            
            if (WIND_DIRECTION == 360) {
                WIND_DIRECTION  = 0;
            }
            
            
            TEMPERATURE_F = (TEMPERATURE_C * 9.0f / 5.0f) + 32.0f;
            TEMPERATURE_K = TEMPERATURE_C + 273.15f;
            
            pc.printf("Temperature(C): %f\r\n", TEMPERATURE_C);
            pc.printf("Temperature(F): %f\r\n", TEMPERATURE_F);
            pc.printf("Temperature(K): %f\r\n", TEMPERATURE_K);
            pc.printf("Humidity: %f\r\n", HUMIDITY);
            pc.printf("Pressure: %f\r\n", PRESSURE);
            pc.printf("Wind Direction: %f\r\n", WIND_DIRECTION);
            measurements_update = false;
        }
    }
}
