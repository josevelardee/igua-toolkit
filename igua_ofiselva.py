#!/usr/bin/python3 import os

# sleep(15)

# how to set to autostart:
# lo mismo pero adaptado a raspi: https://www.raspberrypi-spy.co.uk/2014/05/how-to-autostart-apps-in-rasbian-lxde-desktop/
# lo que funcó para hacer autostart: editamos este file: 
# sudo nano ~/.config/lxsession/LXDE-pi/autostart
# y alli adentro ponemos lo sgte: 
# @sudo /home/pi/Desktop/igua-toolkit/run.sh
# notar que debes escribilo antes de la linea que dice "screensaver"
# luego conviene crear un bookmark en el filemanager (pcmanfm) a la carpeta .config/lxsession/LXDE-pi/

# para configurar qué redes queremos aprender u olvidar: 
# sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

# para clonar la carpeta de github a local:
# git clone http://github.com/kikomayorga/igua_toolkit/


#importando modulos genericos
from time import sleep
from time import strftime 
import time
import serial
import re
import socket
REMOTE_SERVER = "www.google.com"

# configuaracion de entradas/saldas del RPI
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

button = 4				# GPIO04, pin nro 07 
valve_relay = 17		# GPIO17, pin nro 11   
button2 = 27			# GPIO27, pin nro 13
spritz_relay = 22		# GPIO22, pin nro 15
coinhibitor_relay = 23	# GPIO23, pin nro 16
UV_relay = 18			# GPIO18, pin nro 12

GPIO.setup(button, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(valve_relay, GPIO.OUT)
GPIO.setup(spritz_relay, GPIO.OUT)
GPIO.setup(coinhibitor_relay, GPIO.OUT)
GPIO.setup(UV_relay, GPIO.OUT)

#para carriots
from urllib.request import urlopen, Request
from time import mktime, sleep
from datetime import datetime
from json import dumps

class Client (object):
    api_url = "http://api.carriots.com/streams"
    api_read_url = "http://api.carriots.com/streams/IGUA01@kikomayorga.kikomayorga/"

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
        
def rc_time(pipin):
    measurement = 0
    GPIO.setup(pipin, GPIO.OUT)
    GPIO.output(pipin, GPIO.LOW)
    sleep(0.1)

    GPIO.setup(pipin, GPIO.IN)

    while GPIO.input(pipin) == GPIO.LOW:
        measurement += 1

    return measurement
    
    
#fin para carriots

# declaramos una función que la usaremos mas adelante para 
# validar conexion disponible

def is_connected():
    try:
        host = socket.gethostbyname(REMOTE_SERVER)
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False



		
# ser = serial.Serial('/dev/ttyACM1',9600,timeout = 0) #puerto del acceptor 
ser_flw =  serial.Serial('/dev/ttyACM0',9600,timeout = None) #puerto del flujometro es ser_flw 
ser_lcd =  serial.Serial('/dev/ttyACM1',9600,timeout = None, parity = serial.PARITY_NONE, xonxoff = False, rtscts = False, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS) # puerto de lcd es ser_lcd 
# ser_tds = serial.Serial('/dev/ttyACM1',9600,timeout = None) # puerto de tds es ser_tds
# ser_psi = serial.Serial('/dev/ttyACM2',9600,timeout = None) # puerto de psi es ser_psi

#modulos custom
from igua_display import startdisplay, refreshdisplay 
from igua_display import display_bienvenida_linear, display_bienvenida_pwyw
from igua_display import display_acumula_pwyw, display_acumula_linear
from igua_display import display_servidos_lt, display_agradece 

# import flowmeter
# import valve

#from display + coinacceptor

last = 0.0
running = 1


solesacumulados = 0   			#transaction-wise accumulator
ferrosacumulados = 0  			#transaction-wise accumulator
cuenta_de_ciclos = 0				#transactions counter on eeprom	

process_id = 0                  #
modo_maquina = 0  # 1: pay what you want , 0: linear mode
button_state = 0
now = 0
now_1 = 0

#setup
startdisplay()
		
#main loop

#para carriots
device = "IGUA_FEST_1@kikomayorga.kikomayorga"
apikey = "13f622d642b12cc336fa6bfde36e1561c6ac7eea19bd88d7c32246d0fca45691"  # Replace with your Carriots apikey
client_carriots = Client(apikey)

# ejemplo de curl "para traer todos los ulktimos streams"
# curl --header carriots.apikey:13f622d642b12cc336fa6bfde36e1561c6ac7eea19bd88d7c32246d0fca45691 http://api.carriots.com/streams/?device=IGUA01@kikomayorga.kikomayorga


#para lcd
def lcd_bienvenida_linear(now):
	if  now == 0:
		ser_lcd.write('agua pura!      toma igua!!!    '.encode())
	elif now == 1:
		ser_lcd.write('hola mundo!!!   hola igua!!!    '.encode())
	elif now == 2:
		ser_lcd.write('chauuuuuuu!!!   hola igua!!!    '.encode())
	elif now == 3:
		ser_lcd.write('hola mundo!!!   hola igua!!!    '.encode())
	elif now == 4:
		ser_lcd.write('chauuuuuuu!!!   hola igua!!!    '.encode())
	elif now == 5:
		ser_lcd.write('hola mundo!!!   hola igua!!!    '.encode())
	
	return 1

def lcd_bienvenida_pwyw(now):
	if  now == 0:
		ser_lcd.write('agua pura!      toma igua!!!    '.encode())
	elif now == 1:
		ser_lcd.write('hola mundo!!!   hola igua!!!    '.encode())
	elif now == 2:
		ser_lcd.write('chauuuuuuu!!!   hola igua!!!    '.encode())
	elif now == 3:
		ser_lcd.write('hola mundo!!!   hola igua!!!    '.encode())
	elif now == 4:
		ser_lcd.write('chauuuuuuu!!!   hola igua!!!    '.encode())
	elif now == 5:
		ser_lcd.write('hola mundo!!!   hola igua!!!    '.encode())
	
	return 1

def lcd_acumula_linear(solesacumulados):
	# ser_lcd.write('hola mundo!!!      hola igua!!! '.encode())	
	ser_lcd.write(('tu saldo: S/. ' + str(format(solesacumulados, '.2f'))).encode())
	# msgSurfaceObj = fontObj.render('tu saldo: S/. ' + format(solesacumulados, '.2f'), False,whiteColor)
	# msgSurfaceObj2 = fontObj2.render('deposita o sirvete ' + format(solesacumulados / 0.5, '.2f') + ' litros.', False,whiteColor)
	return 1
	
def lcd_acumula_pwyw(solesacumulados):
	# ser_lcd.write('hola mundo!!!      hola igua!!! '.encode())	
	# msgSurfaceObj = fontObj.render('tu aporte: S/. ' + format(solesacumulados, '.2f'), False,whiteColor)
	ser_lcd.write(('tu aporte: S/. ' + str(format(solesacumulados, '.2f'))).encode())	
	# msgSurfaceObj2 = fontObj2.render('deposita mas o sirvete! ', False,whiteColor)	

	
def lcd_servidos_lt(servidos_lt,diff):
	# ser_lcd.write(('mAs agua pura!  mAs agua pura!  ' + ' + ' + str(format(servidos_lt/1000, '.3f')) + ' litros!').encode())	
	# ser_lcd.write(('mAs agua pura!  mAs agua pura!  ').encode())    # + ' + ' + str(format(servidos_lt/1000, '.3f')) + ' litros!'))	
	ser_lcd.write(('  + ' + str(format(servidos_lt/1000, '.3f')) + ' litros! ').encode())	

def lcd_ahorradas_bot(ahorradas_bot,diff):
	# ser_lcd.write(('mAs agua pura!  mAs agua pura!  ' + ' + ' + str(format(servidos_lt/1000, '.3f')) + ' litros!').encode())	
	# ser_lcd.write(('mAs agua pura!  mAs agua pura!  ').encode())    # + ' + ' + str(format(servidos_lt/1000, '.3f')) + ' litros!'))	
	ser_lcd.write(('  - ' + str(format(ahorradas_bot/1000, '.0f')) + ' botellas! ').encode())	
	
		
	# ser_lcd.write(('QWERTYUIASDFGHJKL').encode())    # + ' + ' + str(format(servidos_lt/1000, '.3f')) + ' litros!'))	
	# msgSurfaceObj = fontObj.render('te quedan: ' + format(servidos_lt/1000, '.3f') + ' litros!', False,whiteColor)
	# msgSurfaceObj = fontObj.render('te quedan: ' + format(servidos_lt/1000, '.3f') + ' litros!', False,whiteColor)
	# msgSurfaceObj2 = fontObj2.render('aun tienes: ' + format(diff) + ' segs. ', False,whiteColor)

	
def lcd_agradece():
	ser_lcd.write('gracias!!!! igua ague pe ! '.encode())	

def read_tds():
	global string_tds
	global ser_tds
	bytesToRead = ser_tds.inWaiting()
	if bytesToRead > 0:
		sleep(0.1)
		bytesToRead = ser_tds.inWaiting()
		print("bytes to read on ser_tds: ", bytesToRead)
		string_tds = str(ser_tds.readline(),'utf-8')
		print("received on ser_tds: ", string_tds)
		string_tds = string_tds.lstrip('r')
		string_tds = string_tds.strip('\n\r')
		string_tds = string_tds.strip('\r\n')		

def read_psi():
	global last_string_psi_1
	global last_string_psi_2
	global last_string_psi_3
	global last_string_psi_4
	global last_string_psi_5
	global last_string_psi_6
	global last_string_psi_7
	global last_string_psi_8
	global last_string_psi_9
	global last_string_psi_10
	global string_psi
	global ser_psi
		
	bytesToRead = ser_psi.inWaiting()
	if bytesToRead > 0:
		last_string_psi_10 = last_string_psi_9
		last_string_psi_9 = last_string_psi_8
		last_string_psi_8 = last_string_psi_7
		last_string_psi_7 = last_string_psi_6
		last_string_psi_6 = last_string_psi_5
		last_string_psi_5 = last_string_psi_4
		last_string_psi_4 = last_string_psi_3
		last_string_psi_3 = last_string_psi_2
		last_string_psi_2 = last_string_psi_1
		last_string_psi_1 = string_psi
		sleep(0.5)
		bytesToRead = ser_psi.inWaiting()
		# print("bytes to read on ser_psi: ", bytesToRead)
		string_psi = str(ser_psi.readline(),'utf-8')
		# print("received on ser_psi: ", string_psi)
		
def clean_string_psi():
		global string_psi	
		global string_psi_array
        # Entrada: 0.93 Voltios - Presion = 19.49 psi // Carbon: 0.95 Voltios - Presion = 18.12 psi // UF: 0.91 Voltios - Presion = 18.94 psi // 

		string_psi = string_psi.lstrip('r')
		string_psi = string_psi.strip('\n\r')
		string_psi = string_psi.strip('\r\n')
		string_psi = string_psi.lstrip('Entrada: ')
		string_psi = string_psi.replace(' Voltios - Presion = ', ' ')
		string_psi = string_psi.replace(' psi // Carbon: ', ' ')
		string_psi = string_psi.replace(' Voltios - Presion = ', ' ')
		string_psi = string_psi.replace(' psi // UF: ', ' ')
		string_psi = string_psi.replace(' Voltios - Presion = ',' ')
		string_psi = string_psi.replace(' psi // ', ' ')
		string_psi_array = string_psi.split(' ')
		
		
def update_globalvars_psi():		
		global string_psi_v1
		global string_psi_psi1
		global string_psi_v2
		global string_psi_psi2
		global string_psi_v3
		global string_psi_psi3
		global string_psi_array
		# print('voltaje 1: ', string_psi_array[0])
		# print('presion 1: ', string_psi_array[1])
		# print('voltaje 2: ', string_psi_array[2])
		# print('presion 2: ', string_psi_array[3])
		# print('voltaje 3: ', string_psi_array[4])
		# print('presion 3: ', string_psi_array[5])
		string_psi_v1 = string_psi_array[0]
		string_psi_psi1 = string_psi_array[1]
		string_psi_v2 = string_psi_array[2]
		string_psi_psi2 = string_psi_array[3]
		string_psi_v3 = string_psi_array[4]
		string_psi_psi3 = string_psi_array[5]
						
def read_flw():
	global ser_flw
	global string_flw
	bytesToRead = ser_flw.inWaiting()
	if bytesToRead > 0:
		sleep(0.1)
		diff = 0
		bytesToRead = ser_flw.inWaiting()
		# print("bytes to read on ser_flw: ", bytesToRead)
		string_flw = str(ser_flw.readline(),'utf-8')
		# print("received on ser_flw: ", string_flw)
		string_flw = string_flw.lstrip('r')
		string_flw = string_flw.strip('\n\r')
		string_flw = string_flw.strip('\r\n')
		
		
servidos_lt = 0
servidos_lt_old = 0
servidos_litros_older = 0
loopcounter = 0	
servidos_total_old = 0

last_string_psi_10 = "default string"
last_string_psi_9 = "default string"
last_string_psi_8 = "default string"
last_string_psi_7 = "default string"
last_string_psi_6 = "default string"
last_string_psi_5 = "default string"
last_string_psi_4 = "default string"
last_string_psi_3 = "default string"
last_string_psi_2 = "default string"
last_string_psi_1 = "default string"
string_tds = "default string"
string_psi = "default string"
string_flw = "0"
diff = 0
string_psi_array = ["0", "0",  "0",  "0", "0", "0"]
string_psi_v1 = 0
string_psi_psi1 = 0
string_psi_v2 = 0
string_psi_psi2 = 0
string_psi_v3 = 0 
string_psi_psi3 = 0

sleep(2)

while 1 == 1:
		
	# ser_flw.flushInput()
	sleep(0.3)
		
	servidos_total = int(string_flw)
	servidos_litros_older = servidos_lt_old
	servidos_lt_old = servidos_lt
	servidos_lt = 0.9 * ((servidos_total) * 2640)/(22*2000)

	ahorradas_bot = servidos_lt / 0.75
	# diff = 10 - diff
	loopcounter = loopcounter + 1
		
	read_psi()
	clean_string_psi()
	update_globalvars_psi()
	read_tds()
	read_flw()
	
	if int(loopcounter/int(2))%3 == 0:
		lcd_servidos_lt((servidos_lt),diff)
	if int(loopcounter/int(2))%3 == 1:
		lcd_ahorradas_bot(ahorradas_bot,diff)
	if int(loopcounter/int(2))%3 == 2:
		ser_lcd.write('mAs agua pura!'.encode())
				
	if (servidos_lt_old == servidos_lt) and (servidos_litros_older != servidos_lt_old):			
		timestamp = int(mktime(datetime.utcnow().timetuple()))
		
		data = {"protocol": "v2", "device": device, "at": timestamp, "data": {"colectado soles": solesacumulados, "servido litros": format(servidos_lt/1000, '.3f'), "maquina": "2", "psi_1" : string_psi_psi1,  "psi_2" : string_psi_psi2,  "psi_3" : string_psi_psi3,"tds": string_tds} }
		print(data)
		if is_connected() == True:
			carriots_response = client_carriots.send(data)
			print('conexion ok!')
			print(carriots_response.read())
		else:
			print('no connectivity available')
