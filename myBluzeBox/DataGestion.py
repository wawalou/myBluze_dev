#!/usr/bin/env python
import mysql.connector
import threading
import time

class DataGestion (threading.Thread):
    #self.mydb = None;#init mydb
    ready= False;
    def __init__(self):
        threading.Thread.__init__(self)
            #affichage info


            #test existance database
        try:
            self.mydb=mysql.connector.connect(host="localhost",user="onilys",passwd="w98kgi771",database="onilysDb")
        except :
            self.mydb=mysql.connector.connect(host="localhost",user="onilys",passwd="w98kgi771")
            self.mycursor = self.mydb.cursor()
            self.mycursor.execute("CREATE DATABASE onilysDb")
            self.mydb=mysql.connector.connect(host="localhost",user="onilys",passwd="w98kgi771",database="onilysDb")
            print("Database create")
        else:
            print("Database exist")
            self.mycursor = self.mydb.cursor()



        try:
            self.mycursor.execute("CREATE TABLE Type_M( ID INT AUTO_INCREMENT NOT NULL PRIMARY KEY, TYPE CHAR(25), UNITE CHAR(25), DATA_TYPE CHAR(25) )")
        except:
            print("Type_M already exist")
        try:
            self.mycursor.execute("CREATE TABLE Type_P( ID INT AUTO_INCREMENT NOT NULL PRIMARY KEY, NOM CHAR(25))")
        except:
            print("Type_P already exist")

        try:
            self.mycursor.execute("CREATE TABLE Type_PT( ID INT AUTO_INCREMENT NOT NULL PRIMARY KEY, NOM CHAR(25),ADRESSE CHAR(25),IDENTIFIANT CHAR(25))")
        except:
            print("Type_PT already exist")
        try:
            self.mycursor.execute("CREATE TABLE Piece( ID INT AUTO_INCREMENT NOT NULL PRIMARY KEY, NOM CHAR(25),TYPE CHAR(25))")
        except:
            print("Piece already exist")
        try:
            self.mycursor.execute("CREATE TABLE Equipement( ID INT AUTO_INCREMENT NOT NULL PRIMARY KEY, NOM CHAR(25),HCREATION DATETIME,HUPDATE DATETIME,PROTOCOLE CHAR(25),ADRESSE CHAR(25),IDENTIFIANT CHAR(25),PIECE CHAR(25)  )")
        except:
            print("Equipement already exist")
        try:
            self.mycursor.execute("CREATE TABLE Donnee( ID INT AUTO_INCREMENT NOT NULL PRIMARY KEY, IDx INT,DATA1 CHAR(25),DATA2 CHAR(25),DATA3 CHAR(25),DATA4 CHAR(25),DATA5 CHAR(25) )")
        except:
            print("Donnee already exist")
        try:
            self.mycursor.execute("DELETE FROM Donnee")
        except:
            print("Donnee can't be erase")
        else:
            self.mydb.commit()            

        self.ready=True;
        self.mycursor.close()
        self.mydb.close()
        self.Terminated = False
        
        

    def stop(self):
        self.Terminated = True

    def run(self):
        print("why?")
        while not self.Terminated: 
            time.sleep(60)
        
    def getState(self):
        return self.ready
        
    def getexecute(self,message):
        self.mydb=mysql.connector.connect(host="localhost",user="onilys",passwd="w98kgi771",database="onilysDb")
        self.mycursor = self.mydb.cursor()        
        try:
            self.mycursor.execute(message)
        except:
            print("Error")
            print(message)
            self.mycursor.close()
            self.mydb.close()
            return False
        else:
            print("message done")
            data=self.mycursor.fetchone()            
            self.mycursor.close()
            self.mydb.close()            
            return data
        
        
    def execute1(self,message):
        self.mydb=mysql.connector.connect(host="localhost",user="onilys",passwd="w98kgi771",database="onilysDb")
        self.mycursor = self.mydb.cursor()        
        try:
            self.mycursor.execute(message)
        except:
            print("Error")
            print(message)
            self.mycursor.close()
            self.mydb.close()
            return False
        else:
            print("message done")
            self.mydb.commit()
            self.mycursor.close()
            self.mydb.close()
            
            return True
                   
    def execute(self,message,val):
        self.mydb=mysql.connector.connect(host="localhost",user="onilys",passwd="w98kgi771",database="onilysDb")
        self.mycursor = self.mydb.cursor()        
        try:
            self.mycursor.execute(message,val)
        except:
            print("Error")
            print(message,val)
            self.mycursor.close()
            self.mydb.close()
            return False
        else:
            print("message done")
            self.mydb.commit()
            self.mycursor.close()
            self.mydb.close()
            
            return True

def main(args):
    test1=DataGestion()

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
