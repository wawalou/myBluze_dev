#!/usr/bin/env python
import time
import paho.mqtt.client as paho
import Bme680worker as bme
import APDSworker as APDS
import DataGestion as dg
import Weatherworker as wh
import socket
import json

broker="localhost"
port=1883
debug=0
#en cas de publicaion et de debug
def on_publish(client,userdata,result):
    if debug :
        print("data published \n"+client+' '+' '+userdata+' '+result)
    pass

def main(args):
    googleIP = "8.8.8.8"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((googleIP, 0))
    addrIP = s.getsockname()[0]
    client1= paho.Client("home")                           #create client object
    client1.on_publish = on_publish                          #assign function to callback
    client1.connect(broker,port)                                 #establish connection
    ret= client1.publish("home/state","ok start")

    test0 = dg.DataGestion()    
    test0.start()
    sql = "DELETE FROM Equipement WHERE NOM = 'box'"
    test0.execute1(sql);
    sql = "INSERT INTO Equipement VALUES( 0,%s,NOW() ,NOW() ,%s,%s,%s,%s)"
    val = ("box","all",str(addrIP),"mac","MAISON")
    test0.execute(sql,val);    
    value=test0.getexecute("SELECT ID FROM Equipement WHERE NOM ='box'")
    for (ID) in value:
        boxID=int(ID)
    
    #test3 = wh.Weathertr(client1) 
    test1 = bme.Bme680Tr(client1)
    test2 = APDS.APDStr(client1,test0,boxID)
    

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
