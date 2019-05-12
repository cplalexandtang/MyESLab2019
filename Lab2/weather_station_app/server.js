const noble = require('noble');
const express = require('express');
const app = express();
const PORT = process.env.PORT || 9000;
var cors = require('cors');
const uuidInfo = {
  '2a6e': { name: 'Temperature', type: 'int16', value: 0 },
  '2a6d': { name: 'Pressure', type: 'uint32', value: 0 },
  '2a6f': { name: 'Humidity', type: 'uint16', value: 0 },
  '2a71': { name: 'WindDirection', type: 'uint16', value: 0 }
};

const wsData = {
  'Temperature': 0,
  'Pressure': 0,
  'Humidity': 0,
  'WindDirection': 0
}
app.use(cors());

app.get('/WeatherStation', (req, res, next) => {
  res.send({
    temperature: wsData.Temperature,
    pressure: wsData.Pressure,
    humidity: wsData.Humidity,
    windDirection: wsData.WindDirection
  });
});

app.get('/WeatherStation/:name', (req, res, next) => {
  res.send(wsData[req.params.name].toString());
});

app.listen(PORT, () => {
  console.log(`Listening on port ${PORT}`);
});

noble.on('stateChange', state => (state === 'poweredOn') ? noble.startScanning() : noble.stopScanning());

noble.on('discover', peripheral => {
  if (peripheral.advertisement.localName && peripheral.advertisement.localName.replace('\0', '') === 'MD305_HRM87') {
    peripheral.connect(function (error) {
      console.log('connected to peripheral: ' + peripheral.uuid);
      peripheral.discoverServices(['181a'], function (error, services) {
        var deviceInformationService = services[0];
        console.log('discovered device information service');

        deviceInformationService.discoverCharacteristics(['2a6e', '2a6d', '2a6f', '2a71'], function (error, characteristics) {
          characteristics.forEach((e) => {
            let uuid = e.uuid;
            e.on('data', function (data, isNotification) {
              if (uuidInfo[uuid].type === 'int16') {
                wsData[uuidInfo[uuid].name] = data.readInt16LE(0) / 100;
              } else if (uuidInfo[uuid].type === 'uint16') {
                wsData[uuidInfo[uuid].name] = data.readInt16LE(0) / 100;
              } else if (uuidInfo[uuid].type === 'uint32') {
                wsData[uuidInfo[uuid].name] = data.readUInt32LE(0) / 10;
              }
              console.log(uuidInfo[uuid].name, wsData[uuidInfo[uuid].name]);
            });

            e.subscribe(function (error) {
              console.log(uuidInfo[uuid].name, ' notification on');
            });
          })
        });
      });
    });
  }
});

