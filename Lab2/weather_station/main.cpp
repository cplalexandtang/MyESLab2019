#include "mbed.h"
#include "ble/BLE.h"
#include "ble/services/WeatherService.h"
#include "XNucleoIKS01A2.h"


DigitalOut led1(LED1, 1);
Serial pc(USBTX, USBRX);

const static char     DEVICE_NAME[]        = "MD305_HRM87";
static const uint16_t uuid16_list[]        = {GattService::UUID_ENVIRONMENTAL_SERVICE};

static volatile bool  triggerSensorPolling = false;

static XNucleoIKS01A2 *mems_expansion_board = XNucleoIKS01A2::instance(D14, D15, D4, D5);

float TEMPERATURE_C;
float HUMIDITY;
float PRESSURE;
float WIND_DIRECTION;
int32_t MAGNETIC[3];

Ticker sensor_ticker;
Ticker led_ticker;

void disconnectionCallback(const Gap::DisconnectionCallbackParams_t *params)
{
    (void)params;
    BLE::Instance().gap().startAdvertising(); // restart advertising
    pc.printf("Disconnected!\n\r");
    pc.printf("Restarting the advertising process\n\r");
}


void sensor_handle() {
    triggerSensorPolling = true;
}

void led_handle() {
    led1 = !led1;
}

void onBleInitError(BLE &ble, ble_error_t error)
{
    (void)ble;
    (void)error;
   /* Initialization error handling should go here */
}

void bleInitComplete(BLE::InitializationCompleteCallbackContext *params)
{
    pc.printf("Initialising \n\r");
    BLE&        ble   = params->ble;
    ble_error_t error = params->error;

    if (error != BLE_ERROR_NONE) {
        onBleInitError(ble, error);
        return;
    }

    if (ble.getInstanceID() != BLE::DEFAULT_INSTANCE) {
        return;
    }

    ble.gap().onDisconnection(disconnectionCallback);

    WeatherService wService(ble);

    /* Setup advertising. */
    ble.gap().accumulateAdvertisingPayload(GapAdvertisingData::BREDR_NOT_SUPPORTED | GapAdvertisingData::LE_GENERAL_DISCOVERABLE);
    ble.gap().accumulateAdvertisingPayload(GapAdvertisingData::COMPLETE_LIST_16BIT_SERVICE_IDS, (uint8_t *)uuid16_list, sizeof(uuid16_list));
    ble.gap().accumulateAdvertisingPayload(GapAdvertisingData::GENERIC_THERMOMETER);
    ble.gap().accumulateAdvertisingPayload(GapAdvertisingData::COMPLETE_LOCAL_NAME, (uint8_t *)DEVICE_NAME, sizeof(DEVICE_NAME));
    ble.gap().setAdvertisingType(GapAdvertisingParams::ADV_CONNECTABLE_UNDIRECTED);
    ble.gap().setAdvertisingInterval(1000); /* 1000ms */
    ble.gap().startAdvertising();

    // infinite loop
    while (true) {
        // check for trigger from periodicCallback()
        if (triggerSensorPolling && ble.getGapState().connected) {
            triggerSensorPolling = false;

            mems_expansion_board->ht_sensor->get_temperature(&TEMPERATURE_C);
            mems_expansion_board->ht_sensor->get_humidity(&HUMIDITY);
            mems_expansion_board->pt_sensor->get_pressure(&PRESSURE);
            mems_expansion_board->magnetometer->get_m_axes(MAGNETIC);
            
            TEMPERATURE_C = TEMPERATURE_C * 100;
            HUMIDITY = HUMIDITY * 100;
            PRESSURE = PRESSURE * 1000;
            
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
            
            WIND_DIRECTION *= 100;
            
            wService.updateTemperature(TEMPERATURE_C);
            wService.updateHumidity(HUMIDITY);
            wService.updatePressure(PRESSURE);
            wService.updateWindDirection(WIND_DIRECTION);
            pc.printf("Temperature(C): %f\r\n", TEMPERATURE_C);
            pc.printf("Humidity: %f\r\n", HUMIDITY);
            pc.printf("Pressure: %f\r\n", PRESSURE);
            pc.printf("Magnetic: %d %d %d\r\n", MAGNETIC[0], MAGNETIC[1], MAGNETIC[2]);
            pc.printf("Wind Direction: %f\r\n", WIND_DIRECTION);
        } else {
            ble.waitForEvent(); // low power wait for event
        }
    }
}

int main(void)
{
    sensor_ticker.attach(&sensor_handle, 2);
    led_ticker.attach(&led_handle, 1);
    
    mems_expansion_board->ht_sensor->enable();
    mems_expansion_board->pt_sensor->enable();
    mems_expansion_board->magnetometer->enable();

    BLE::Instance().init(bleInitComplete);
}

