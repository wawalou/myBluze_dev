#!/usr/bin/env python
import bme680
import time
import paho.mqtt.client as paho                             #establish connection
import threading

class Bme680Tr(threading.Thread):
    def __init__(self, client1):
        threading.Thread.__init__(self)
        self.client1=client1
        self.Terminated = False
        
    def stop(self):
        self.Terminated = True	
        
    def run(self):
        try:
            sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except IOError:
            sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

        # These calibration data can safely be commented
        # out, if desired.

        #print('Calibration data:')
        for name in dir(sensor.calibration_data):

            if not name.startswith('_'):
                value = getattr(sensor.calibration_data, name)

                #if isinstance(value, int):
                  #  print('{}: {}'.format(name, value))

        # These oversampling settings can be tweaked to
        # change the balance between accuracy and noise in
        # the data.

        sensor.set_humidity_oversample(bme680.OS_2X)
        sensor.set_pressure_oversample(bme680.OS_4X)
        sensor.set_temperature_oversample(bme680.OS_8X)
        sensor.set_filter(bme680.FILTER_SIZE_3)
        sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)


        sensor.set_gas_heater_temperature(320)
        sensor.set_gas_heater_duration(150)
        sensor.select_gas_heater_profile(0)

        # Up to 10 heater profiles can be configured, each
        # with their own temperature and duration.
        # sensor.set_gas_heater_profile(200, 150, nb_profile=1)
        # sensor.select_gas_heater_profile(1)
        print('\n BME680 is Started')
        
        while not self.Terminated:            
            if sensor.get_sensor_data():
                ret= self.client1.publish("home/temperature",(sensor.data.temperature))
                ret= self.client1.publish("home/pressure",(sensor.data.pressure))
                ret= self.client1.publish("home/humidity",(sensor.data.humidity))        
            time.sleep(60)
            
