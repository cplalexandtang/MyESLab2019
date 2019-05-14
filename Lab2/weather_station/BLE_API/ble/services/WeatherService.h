/* mbed Microcontroller Library
 * Copyright (c) 2006-2013 ARM Limited
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

#ifndef __WEATHER_SERVICE_H__
#define __WEATHER_SERVICE_H__

#include "ble/BLE.h"

class WeatherService {
public:
    WeatherService(BLE &_ble) :
        ble(_ble),
        temperatureCharacteristic(GattCharacteristic::UUID_TEMPERATURE_CHAR, &temperature, GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_NOTIFY),
        humidityCharacteristic(GattCharacteristic::UUID_HUMIDITY_CHAR, &humidity, GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_NOTIFY),
        pressureCharacteristic(GattCharacteristic::UUID_PRESSURE_CHAR, &pressure, GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_NOTIFY),
        windDirectionCharacteristic(GattCharacteristic::UUID_TRUE_WIND_DIRECTION_CHAR, &windDirection, GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_NOTIFY)   {
        
        GattCharacteristic *charTable[] = { &temperatureCharacteristic,
                                            &humidityCharacteristic,
                                            &pressureCharacteristic,
                                            &windDirectionCharacteristic };
        GattService weatherService(GattService::UUID_ENVIRONMENTAL_SERVICE, charTable, sizeof(charTable) / sizeof(GattCharacteristic *));

        ble.addService(weatherService);
    }

    void updateTemperature(float newTemperature) {
        temperature = (int16_t)newTemperature;
        ble.gattServer().write(temperatureCharacteristic.getValueHandle(), (uint8_t *)&temperature, sizeof(int16_t));
    }
    
    void updateHumidity(float newHumidity) {
        humidity = (uint16_t)newHumidity;
        ble.gattServer().write(humidityCharacteristic.getValueHandle(), (uint8_t *)&humidity, sizeof(uint16_t));
    }
    
    void updatePressure(float newPressure) {
        pressure = (uint32_t)newPressure;
        ble.gattServer().write(pressureCharacteristic.getValueHandle(), (uint8_t *)&pressure, sizeof(uint32_t));
    }
    
    void updateWindDirection(float newWindDirection) {
        windDirection = (uint16_t)newWindDirection;
        ble.gattServer().write(windDirectionCharacteristic.getValueHandle(), (uint8_t *)&windDirection, sizeof(uint16_t));
    }

protected:
    BLE &ble;

    int16_t    temperature;
    uint16_t   humidity;
    uint32_t   pressure;
    uint16_t   windDirection;
    
    ReadOnlyGattCharacteristic<int16_t>     temperatureCharacteristic;
    ReadOnlyGattCharacteristic<uint16_t>    humidityCharacteristic;
    ReadOnlyGattCharacteristic<uint32_t>    pressureCharacteristic;
    ReadOnlyGattCharacteristic<uint16_t>    windDirectionCharacteristic;
};

#endif /* #ifndef __WEATHER_SERVICE_H__*/