import time
import datetime
import RPi.GPIO as GPIO
from flask_pymongo import PyMongo
from pymongo import MongoClient
from key import *
client = MongoClient(moClient)
db = client[dbClient]

def data():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)
	GPIO.setup(18,GPIO.OUT)
	print "LED on"
	GPIO.output(18,GPIO.HIGH)
	time.sleep(1)
	print "LED off"
	GPIO.output(18,GPIO.LOW)



        #define the pin that gose to the circuit
        pin_to_circuit = 7

        def rc_time (pin_to_circuit):
                count = 0

                #Output to the pin for
                GPIO.setup(pin_to_circuit, GPIO.OUT)
                GPIO.output(pin_to_circuit, GPIO.LOW)
                time.sleep(0.5)

                #change the pin back to input
                GPIO.setup(pin_to_circuit, GPIO.IN)

                #Count until the pin gose high
                while (GPIO.input(pin_to_circuit) == GPIO.LOW):
			count += 1
                	
		return count

        #Catch when script is interrupted, cleanup correctly
        try:
                # Main loop
                while True:
                        print rc_time(pin_to_circuit)
                        data = db.data.insert_one({'Data' : rc_time(pin_to_circuit)})
        except KeyboardInterrupt:
                pass
        finally:
                GPIO.cleanup()

data()
