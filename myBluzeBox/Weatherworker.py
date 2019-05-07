#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Wheather_OpenWheather.py

import requests
import sys
import time
import datetime
import os
import re
import json
import urllib3
import threading

API_Key = "c0b8e95c0bd5dc51bf0046e41ae69a9b"
k2c = 273.15 #Kelvin to celsius
class Weathertr (threading.Thread):
	timeToUpdate = 15; #minutes
	def __init__(self, client1,var=60):
                threading.Thread.__init__(self)
                self.client1=client1
                self.var=var
		self.url = 'http://ip-api.com/json'
		self.http = urllib3.PoolManager()
		self.response = self.http.request('GET',self.url)
		self.data = json.loads(self.response.data.decode('utf-8'))
		#test d'echec
		if self.data['status']=="fail":
			self.city = 'Rennes'
			self.IP='127.0.1.1'
		else:
			self.city = self.data['city']
			self.IP=self.data['query']
		self.r = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+self.city+",fr&appid="+API_Key)
		#print("http://api.openweathermap.org/data/2.5/weather?q="+self.city+",fr&appid="+API_Key)
		self.data=self.r.json()
		self.Terminated = False	


	def run(self):
                print('\n Wheather is Started')
		while not self.Terminated: 
                        self.get_data()
                        ret= self.client1.publish("out/wheather_C",(self.get_weather_C()))
                        ret= self.client1.publish("out/humidity",(self.get_humidity()))
                        ret= self.client1.publish("out/wind_speed",(self.get_wind_speed()))
                        ret= self.client1.publish("out/wind_deg",(self.get_wind_deg()))
                        ret= self.client1.publish("out/pressure",(self.get_pressure()))
			time.sleep(self.var)   



#adresse IP
	def get_IP(self):
		return self.IP;
#récuperer la self.data
	def get_data(self):
		r = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+self.city+",fr&appid="+API_Key)
		self.data=r.json()
#temperature
	def get_weather_C(self):
		t=(float(self.data['main']['temp']))
		t=t-k2c #temperature en C°
		return t
	def get_weather_K(self):
		r = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+self.city+",fr&appid="+API_Key)
		self.data=r.json()
		t=(float(self.data['main']['temp']))
		return t
	def get_weather_F(self):
		r = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+self.city+",fr&appid="+API_Key)
		self.data=r.json()
		t=(float(self.data['main']['temp']))
		t=(t-k2c)*(9/5)+32
		return t
#Max
	def get_weather_max_C(self):
		r = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+self.city+",fr&appid="+API_Key)
		self.data=r.json()
		t=(float(self.data['main']['temp_max']))
		t=t-k2c #temperature en C°
		return t
	def get_weather_max_K(self):
		r = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+self.city+",fr&appid="+API_Key)
		self.data=r.json()
		t=(float(self.data['main']['temp_max']))
		return t
	def get_weather_max_F(self):
		r = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+self.city+",fr&appid="+API_Key)
		self.data=r.json()
		t=(float(self.data['main']['temp_max']))
		t=(t-k2c)*(9/5)+32
		return t
#pressure
	def get_pressure(self):
		r = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+self.city+",fr&appid="+API_Key)
		self.data=r.json()
		t=(float(self.data['main']['pressure']))
		return t
#humidity
	def get_humidity(self):
		r = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+self.city+",fr&appid="+API_Key)
		self.data=r.json()
		t=(float(self.data['main']['humidity']))
		return t
#wind
	def get_wind_speed(self):
		r = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+self.city+",fr&appid="+API_Key)
		self.data=r.json()
		t=(float(self.data['wind']['speed']))
		return t
	def get_wind_deg(self):
		r = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+self.city+",fr&appid="+API_Key)
		self.data=r.json()
		t=(float(self.data['wind']['deg']))
		return t

#temp entre chaque MAJ
	def set_timeToUpdate(self,a):
		self.var = a;
	def get_timeToUpdate(self):
		return self.var;
