#!/usr/local/bin/python
from flask import Flask, render_template, jsonify, redirect
import datetime
import RPi.GPIO as GPIO
import time
from sensor import data
from flask_pymongo import PyMongo
app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'python-test'
app.config['MONGO_URI'] = 'mongodb://Vanhorn:mongodb123@ds123926.mlab.com:23926/python-testing'

mongo = PyMongo(app)

@app.route("/")
def hello():
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %H:%M")
	templateData = {
		'title' : 'HELLO!',
		'time': timeString
		}
	return render_template('main.html', **templateData)

@app.route("/getData")
def getData():
	

	return redirect("http://127.0.0.1:5000/star", code=302)


def datas():

	GPIO.setmode(GPIO.BOARD)

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
			#print rc_time(pin_to_circuit)
			data = mongo.db.data
    			data.insert({'Data': rc_time(pin_to_circuit)})
			return redirect("http://127.0.0.1:5000/star", code=302)
	except KeyboardInterrupt:
		pass
	finally:
		GPIO.cleanup()

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000, debug=True)
data()
