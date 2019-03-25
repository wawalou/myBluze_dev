#!/usr/bin/env python
import APDS_9301 as APDS
import time
import paho.mqtt.client as paho                             #establish connection
import threading

class APDStr(threading.Thread):
    def __init__(self, client1,var=60):
        threading.Thread.__init__(self)
        self.client1=client1
        self.var=var
        self.Terminated = False
        
    def stop(self):
        self.Terminated = True	
        
    def run(self):
        try:
            sensor = APDS.adps9300()
        except IOError:
            print ('error in APDS :')
            self.stop()

        print('\n APDS is Started')
        
        while not self.Terminated:     #add the interupt   
            ret= self.client1.publish("home/lux",(sensor.read_lux()))   
            #print(  'light is'+str(sensor.read_lux()))
            time.sleep(self.var)            


