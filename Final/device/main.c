/* mbed Microcontroller Library
 * Copyright (c) 2006-2015 ARM Limited
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "mbed.h"
#include "ble/BLE.h"

DigitalOut led1(LED1);

const static char    DEVICE_NAME[] = "LINE_BEACON";
const static uint8_t AdvServiceUUIDs[] = { 0x6F, 0xFE };
const static uint8_t AdvData[] = { 0x6F, 0xFE, 0x02, 0x01, 0x2B, 0x0E, 0x6E, 0x45, 0x7F, 0x02 };  /* Replace 0xFF, 0xFF, 0xFF, 0xFF, 0xFF to your bot's HWID */
                                            
static volatile bool  triggerSensorPolling = false;

uint8_t hrmCounter = 100; // init HRM to 100bps

void disconnectionCallback(const Gap::DisconnectionCallbackParams_t *params)
{
    BLE::Instance(BLE::DEFAULT_INSTANCE).gap().startAdvertising(); // restart advertising
}

void periodicCallback(void)
{
    led1 = !led1; /* Do blinky on LED1 while we're waiting for BLE events */

    /* Note that the periodicCallback() executes in interrupt context, so it is safer to do
     * heavy-weight sensor polling from the main thread. */
    triggerSensorPolling = true;
}

void bleInitComplete(BLE::InitializationCompleteCallbackContext *params)
{
    BLE &ble          = params->ble;
    ble_error_t error = params->error;

    if (error != BLE_ERROR_NONE) {
        return;
    }

    ble.gap().setDeviceName((const uint8_t *) DEVICE_NAME);
    ble.gap().onDisconnection(disconnectionCallback);

    /* Setup advertising. */
    ble.gap().accumulateAdvertisingPayload(GapAdvertisingData::BREDR_NOT_SUPPORTED | GapAdvertisingData::LE_GENERAL_DISCOVERABLE);
    ble.gap().setAdvertisingType(GapAdvertisingParams::ADV_CONNECTABLE_UNDIRECTED);
    
    ble.gap().accumulateAdvertisingPayload(GapAdvertisingData::COMPLETE_LIST_16BIT_SERVICE_IDS, AdvServiceUUIDs, sizeof(AdvServiceUUIDs));
    ble.gap().accumulateAdvertisingPayload(GapAdvertisingData::SERVICE_DATA, AdvServiceUUIDs, sizeof(AdvServiceUUIDs));
    ble.gap().accumulateAdvertisingPayload(GapAdvertisingData::SERVICE_DATA, AdvData, sizeof(AdvData));
    
    ble.gap().setAdvertisingInterval(1000); /* 1000ms */
    ble.gap().startAdvertising();
}

int main(void)
{
    led1 = 1;
    Ticker ticker;
    ticker.attach(periodicCallback, 1); // blink LED every second

    BLE& ble = BLE::Instance(BLE::DEFAULT_INSTANCE);
    ble.init(bleInitComplete);
    
    /* SpinWait for initialization to complete. This is necessary because the
     * BLE object is used in the main loop below. */
    while (ble.hasInitialized()  == false) { /* spin loop */ }

    // infinite loop
    while (1) {
        // check for trigger from periodicCallback()
        if (triggerSensorPolling && ble.getGapState().connected) {
            triggerSensorPolling = false;
        } else {
            ble.waitForEvent(); // low power wait for event
        }
    }
}
