import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

import requests
import json
import sys 
import datetime
from subprocess import call
from firebase import firebase
from keys import *


firebase = firebase.FirebaseApplication('https://MYFIREBASELINK.firebaseio.com', None)

lastCircle = ""
lastSwipe = ""
lastKeyTap = ""
lastScreenTap = ""
lastNumberOne = ""
lastGun = ""
lastStop = ""

atm = True
walmart = True


class SampleListener(Leap.Listener):
	initial = None
	first60 = False
	second60 = False
	third60 = False
	startHands = 0
	numOneActive = False
	lastNumOne = datetime.datetime.now() - datetime.timedelta(hours=1) 
	gunActive = False
	lastGun = datetime.datetime.now() - datetime.timedelta(hours=1) 
	stopActive = False
	lastStop = datetime.datetime.now() - datetime.timedelta(hours=1) 

	def on_connect(self, controller):
		print "Connected"
		controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);
		controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);


	def on_frame(self, controller):
		frame = controller.frame()
		currentGesture = frame.gestures()[0]
		if currentGesture.type is Leap.Gesture.TYPE_CIRCLE:
			if (len(controller.frame(1).gestures()) == 0) and (len(controller.frame(2).gestures()) == 0) and (len(controller.frame(3).gestures()) == 0):
				print "Circle"
				speak(firebase.get('/circleMessage', None), "circle")
		elif currentGesture.type is Leap.Gesture.TYPE_SWIPE:
			if (len(controller.frame(1).gestures()) == 0) and (len(controller.frame(2).gestures()) == 0) and (len(controller.frame(3).gestures()) == 0):
				print "Swipe"
				speak(firebase.get('/swipeMessage', None), "swipe")
		elif currentGesture.type is Leap.Gesture.TYPE_KEY_TAP:
			if (len(controller.frame(1).gestures()) == 0) and (len(controller.frame(2).gestures()) == 0) and (len(controller.frame(3).gestures()) == 0):
				print "Key Tap"
				speak(firebase.get('/keyTapMessage', None), "keytap")
		elif currentGesture.type is Leap.Gesture.TYPE_SCREEN_TAP:
			if (len(controller.frame(1).gestures()) == 0) and (len(controller.frame(2).gestures()) == 0) and (len(controller.frame(3).gestures()) == 0):
				print "Screen Tap"
				speak(firebase.get('/screenTapMessage', None), "screentap")

		for hand in frame.hands:
			# print hand.palm_normal
			if not self.gunActive and hand.fingers[0].direction[1] > 0.75 and (hand.fingers[1].direction[0] > -0.2 and hand.fingers[1].direction[0] < 0.2) and hand.fingers[0].is_extended and hand.fingers[1].is_extended and not hand.fingers[2].is_extended and not hand.fingers[3].is_extended and not hand.fingers[4].is_extended and ((datetime.datetime.now() - self.lastGun).seconds > 3):
				self.gunActive = True
				self.lastGun = datetime.datetime.now()
				tempATM = firebase.get('/gunMessage', None)
				atm = firebase.get('/capitalOne', None)
				if atm == "True":
					print "Gun, with atm details"
					c = requests.get("http://api.reimaginebanking.com/atms?lat=38.9283&lng=-77.1753&rad=3&key=" + capitalKey)
					cjData = c.json()
					atmAddress = cjData["data"][0]["address"]["street_number"] + " " + cjData["data"][0]["address"]["street_name"] + ", " + cjData["data"][0]["address"]["city"] + ", " + cjData["data"][0]["address"]["state"]
					tempATM += " For your convenience, the nearest atm is located at " + atmAddress
				else:
					print "Gun"
				speak(tempATM, "gun")
			else:
				self.gunActive = False

			if not self.numOneActive and hand.fingers[1].direction[1] > 0.75 and hand.fingers[1].is_extended and not hand.fingers[0].is_extended and not hand.fingers[2].is_extended and not hand.fingers[3].is_extended and not hand.fingers[4].is_extended and ((datetime.datetime.now() - self.lastNumOne).seconds > 3):
				self.numOneActive = True
				self.lastNumOne = datetime.datetime.now()
				tempWalmart = firebase.get('/numberOneMessage', None)
				walmart = firebase.get('/walmart', None)
				if walmart == "True":
					print "Number One, with Walmart product info"
					a = requests.get("http://api.walmartlabs.com/v1/trends?apiKey=" + walmartKey)
					ajData = a.json()
					topWalmartProduct = ajData["items"][0]["name"]
					tempWalmart += " For your convenience, the top Walmart product right now is the " + topWalmartProduct
				else:
					print "Number One"
				speak(tempWalmart, "numOne")
			else:
				self.numOneActive = False

			if hand.fingers[0].is_extended and hand.fingers[1].is_extended and hand.fingers[2].is_extended and hand.fingers[3].is_extended and hand.fingers[4].is_extended and (hand.palm_normal[0] < 0 and hand.palm_normal[0] > -0.5) and (hand.palm_normal[1] < 0.2 and hand.palm_normal[1] > -0.2) and hand.palm_normal[2] < -0.7 and ((datetime.datetime.now() - self.lastStop).seconds > 3):
				self.stopActive = True
				self.lastStop = datetime.datetime.now()
				print "Stop"
				speak(firebase.get('/stopMessage', None), "stop")
			else:
				self.stopActive = False

		'''	
		if ((frame.id - self.initial) % 100) == 0:
			print "100 frames passed"
		
		print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
			   frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))
		'''


def speak(text, gestureType):
	global lastCircle, lastSwipe, lastKeyTap, lastScreenTap, lastNumberOne, lastGun, lastStop

	text = text
	if text == lastCircle:
		if sys.platform == 'linux2': 
			call(["xdg-open","circle.mp3"]) 
		elif sys.platform == 'darwin': 
			call(["afplay","circle.mp3"])
	elif text == lastSwipe:
		if sys.platform == 'linux2': 
			call(["xdg-open","swipe.mp3"]) 
		elif sys.platform == 'darwin': 
			call(["afplay","swipe.mp3"])
	elif text == lastKeyTap:
		if sys.platform == 'linux2': 
			call(["xdg-open","keytap.mp3"]) 
		elif sys.platform == 'darwin': 
			call(["afplay","keytap.mp3"])
	elif text == lastScreenTap:
		if sys.platform == 'linux2': 
			call(["xdg-open","screentap.mp3"]) 
		elif sys.platform == 'darwin': 
			call(["afplay","screentap.mp3"])
	elif text == lastNumberOne:
		if sys.platform == 'linux2': 
			call(["xdg-open","numOne.mp3"]) 
		elif sys.platform == 'darwin': 
			call(["afplay","numOne.mp3"])
	elif text == lastGun:
		if sys.platform == 'linux2': 
			call(["xdg-open","gun.mp3"]) 
		elif sys.platform == 'darwin': 
			call(["afplay","gun.mp3"])
	elif text == lastStop:
		if sys.platform == 'linux2': 
			call(["xdg-open","stop.mp3"]) 
		elif sys.platform == 'darwin': 
			call(["afplay","stop.mp3"])
	else:
		if gestureType == "circle":
			lastCircle = text
		elif gestureType == "swipe":
			lastSwipe = text
		elif gestureType == "keytap":
			lastKeyTap = text
		elif gestureType == "screentap":
			lastScreenTap = text
		elif gestureType == "numOne":
			lastNumberOne = text
		elif gestureType == "gun":
			lastGun = text
		elif gestureType == "stop":
			lastStop = text

		url = "http://api.voicerss.org/"
		filename = gestureType + ".mp3"

		payload = {"hl": "en-us", "r": 0, "src": text, "key": ttsKey}

		with open(filename, 'wb') as handle:
			r = requests.get(url, params=payload, stream=True)
			# print r.status_code

			for block in r.iter_content(1024):
				handle.write(block)	

		if sys.platform == 'linux2': 
			call(["xdg-open",filename]) 
		elif sys.platform == 'darwin': 
			call(["afplay",filename])


def main():
	# Create a sample listener and controller
	listener = SampleListener()
	controller = Leap.Controller()

	# Have the sample listener receive events from the controller
	controller.add_listener(listener)

	# Keep this process running until Enter is pressed
	print "Press Enter to quit..."
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		# Remove the sample listener when done
		controller.remove_listener(listener)

if __name__ == "__main__":
	main()

