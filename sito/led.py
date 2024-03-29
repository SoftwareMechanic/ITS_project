
#coding=utf-8
# Author: Baruch Manigrasso



# Importazione della libreria Adafruit per controllare il sensore, Rpi.GPIO per cotrollare i pin, time 
#from sito import db per importare l istanza db ( database) e da sito.models  importo le tabelle per poterci lavorare

import Adafruit_DHT   #librerie sensore temperatura DHT 11

import RPi.GPIO as GPIO   #numerazione pin raspberry

import time    

import datetime


from sito import db            #importo istanza db per lavorare sul database
from sito.models import Info    #importo la tabella Info del database per poter creare istanze
from flask_login import current_user
 #importo funzioni rilevanti al login per riconoscere se l'utente è collegato o no





# Setting di una variabile il tipo di sensore utilizzato

sensor = Adafruit_DHT.DHT11



# Setting del pin a cui è collegato il sensore

pin = 26



# Setting di alcuni parametri inerenti al funzionamento del LED

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

GPIO.setup(17,GPIO.OUT)



# Setting temperatura massima limite

max = 27


#flag per bloccare l esecuzione dell analisi automatica
flag = False

#variabile di appoggio globale
temp = 0



def analisi():




    global flag   #uso la flag globale perchè dovrò lavorarci su piu funzioni
    flag = False

    # Ciclo in cui si recupera il valore della temperatura e si accende eventualmente il LED
    # flag serve ad evitare di continuare l'analisi automatica anche se si attiva una funziona manuale
    while flag == False:


    # Prelevo la temperatura e l'umidità dal sensore dandogli come parametri le variabili dichiarate prima

        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        global temp   #variabile dichiarata globalmente perche ci lavoro su più funzioni
        temp = float(temperature)

    # Se la temperatura è maggiore del valore limite il LED si accende

        if (temp >=float(max)) & flag == False:

            GPIO.output(17, GPIO.HIGH)

            time.sleep(10)           #se la temp è maggiore del massimo e la flag e ancora falsa, accendi il led per 10 secondi

            x = Info(temperatura=temp, mode="auto", stato="ON")   #creo variabile con parametri per entrare nel database in tabella Info

            db.session.add(x)    #aggiungo x al database
           
            if flag == False:
                db.session.commit()     #effettuo cambiamenti al database
            #grazie ad aver importato db e le tabelle posso aggiornare il database da programma

      	    # Se la temperatura è minore del valore limite il LED si spegne, se la flag è ancora falsa

        elif (temp < float(max)) & flag == False:


            GPIO.output(17, GPIO.LOW)

            time.sleep(10)

            x = Info(temperatura=temp, mode="auto", stato="OFF")

            db.session.add(x)
            
            if flag == False:
                db.session.commit()




def spegni():

    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    global temp
    if not current_user.is_authenticated:
        GPIO.output(17, GPIO.LOW)            # se l utente non è collegato si spegne il sistema, non volontariamente

    global temp
    global flag
    flag = True   #flag vera per evitare che la funzione di analisi automatica continui comunque

    GPIO.output(17, GPIO.LOW)     #spegni il sistema 

    x = Info(temperatura=temperature, mode="manual", stato="OFF")

    db.session.add(x) 
    db.session.commit()       #aggiunge al database

def accendi():

    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    if not current_user.is_authenticated:
        GPIO.output(17, GPIO.LOW)

    global temp

    global flag
    flag = True

    GPIO.output(17, GPIO.HIGH)

    x = Info(temperatura=temperature, mode="manual", stato="ON")

    db.session.add(x)
    db.session.commit()




