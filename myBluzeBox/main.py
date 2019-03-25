#!/usr/bin/env python
import time
import paho.mqtt.client as paho
import Bme680worker as bme
import APDSworker as APDS
import Weatherworker as wh

broker="localhost"
port=1883
debug=0
#en cas de publicaion et de debug
def on_publish(client,userdata,result):  
    if debug :
        print("data published \n"+client+' '+' '+userdata+' '+result)
    pass

def main(args):
    client1= paho.Client("home")                           #create client object
    client1.on_publish = on_publish                          #assign function to callback
    client1.connect(broker,port)                                 #establish connection
    ret= client1.publish("home/state","ok start")

    test1 = bme.Bme680Tr(client1)
    test1.start()

    test2 = APDS.APDStr(client1)
    test2.start()

    test3 = wh.Weathertr(client1)
    test3.start()

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
