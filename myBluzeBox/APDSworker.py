#!/usr/bin/env python
import APDS_9301 as APDS
import time
import paho.mqtt.client as paho                             #establish connection
import threading
import DataGestion as dg

class APDStr(threading.Thread):
    def __init__(self, client1,bdd,ID,var=60):
        threading.Thread.__init__(self)
        self.client1=client1
        self.var=var
        self.bdd=bdd;
        self.ID=ID;
        try:
            self.sensor = APDS.adps9300()
        except IOError:
            print ('error in APDS :')
            self.stop()
        else: 
            print("------------------------")       
            sql ='INSERT INTO Donnee (IDx,DATA1) VALUES( %s,%s)'
            val=(self.ID,str(self.sensor.read_lux()));
            self.bdd.execute(sql,val);
        self.Terminated = False
        
    def stop(self):
        self.Terminated = True	
        
    def run(self):
        

        print('\n APDS is Started')
        
        while not self.Terminated:     #add the interupt   
            ret= self.client1.publish("home/lux",(self.sensor.read_lux()))   
            
            
            time.sleep(self.var)            


