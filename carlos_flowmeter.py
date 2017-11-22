from time import sleep
from time import strftime 
import time
import serial
import re
import socket
REMOTE_SERVER = "www.google.com"

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

from urllib.request import urlopen, Request
from time import mktime, sleep
from datetime import datetime
from json import dumps

class Client (object):
    api_url = "http://api.carriots.com/streams"
    api_read_url = "http://api.carriots.com/streams/IGUA_FEST_1@kikomayorga.kikomayorga/"

    def __init__(self, api_key=None, client_type='json'):
        self.client_type = client_type
        self.api_key = api_key
        self.content_type = "application/vnd.carriots.api.v2+%s" % self.client_type
        self.headers = {'User-Agent': 'Raspberry-Carriots',
                        'Content-Type': self.content_type,
                        'Accept': self.content_type,
                        'Carriots.apikey': self.api_key}
        self.data = None
        self.response = None

    def send(self, data):
        self.data = dumps(data).encode('utf8')
        request = Request(Client.api_url, self.data, self.headers)     
        self.response = urlopen(request)
        return self.response
    
def is_connected():
    try:
        host = socket.gethostbyname(REMOTE_SERVER)
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False

ser2 =  serial.Serial('/dev/ttyACM1',9600,timeout = None) 
ser3 =  serial.Serial('/dev/ttyACM0',9600,timeout = None, parity = serial.PARITY_NONE, xonxoff = False, rtscts = False, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS) 
ser4 =  serial.Serial('/dev/ttyACM2',9600,timeout = None)


device = "IGUA_FEST_1@kikomayorga.kikomayorga"  
apikey = "13f622d642b12cc336fa6bfde36e1561c6ac7eea19bd88d7c32246d0fca45691"  # Replace with your Carriots apikey
client_carriots = Client(apikey)
	
def lcd_servidos_lt(servidos_lt,diff):
	ser3.write(('  + ' + str(format(servidos_lt/1000, '.2f')) + ' litros! ').encode())	

def lcd_ahorradas_bot(ahorradas_bot,diff):
	ser3.write(('  - ' + str(format(ahorradas_bot/1000, '.0f')) + ' botellas! ').encode())	

servidos_lt = 0
servidos_lt_old = 0
servidos_litros_older = 0
loopcounter = 0	
servidos_total_old = 0

secondcycle = 0
while 1==1:
	bytesToRead = ser2.inWaiting()
	if bytesToRead > 0:
		sleep(0.1)
		diff = 0
		bytesToRead = ser2.inWaiting()
		string_igua = str(ser2.readline(),'utf-8')
		string_igua = string_igua.lstrip('r')
		string_igua = string_igua.strip('\n\r')
		string_igua = string_igua.strip('\r\n')		
		if secondcycle == 0:
			try:
				countstart = int(string_igua)
			except ValueError:
				print('error')
			secondcycle = 1 
		servidos_total = int(string_igua)
		servidos_litros_older = servidos_lt_old
		servidos_lt_old = servidos_lt
		servidos_lt = 0.9 * ((servidos_total) * 2640)/(22*2000)
		countstart_lt = 0.9 * ((countstart) * 2640)/(22*2000)
		ahorradas_bot = servidos_lt / 0.75
		diff = 10 - diff
		loopcounter = loopcounter + 1
		if int(loopcounter/int(2))%3 == 0:
			lcd_servidos_lt((servidos_lt),diff)
			nada = 0
		if int(loopcounter/int(2))%3 == 1:
			lcd_ahorradas_bot(ahorradas_bot,diff)
			nada = 0
		if int(loopcounter/int(2))%3 == 2:
			ser3.write('MAS AGUA PURA!'.encode())
			nada = 0
			
		if (servidos_lt_old == servidos_lt) and (servidos_litros_older != servidos_lt_old):
                        timestamp = int(mktime(datetime.utcnow().timetuple()))
                        data = {"protocol": "v2", "device": device, "at": timestamp, "data": {"servido litros": format(servidos_lt/1000, '.3f')}}
                        print(data)
                        if is_connected() == True:
                                carriots_response = client_carriots.send(data)
                                print('conexion ok!')
                                print(carriots_response.read())
                        else:
                                print('no connectivity available')
                                
##while 1==1:
##	bytesToRead = ser4.inWaiting()
##	if bytesToRead > 0:
##		sleep(0.1)
##		diff = 0
##		bytesToRead = ser4.inWaiting()
##		string_igua = str(ser4.readline(),'utf-8')
##		string_igua = string_igua.lstrip('r')
##		string_igua = string_igua.strip('\n\r')
##		string_igua = string_igua.strip('\r\n')		
##		if secondcycle == 0:
##			try:
##				countstart = int(string_igua)
##			except ValueError:
##				print('error')