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

# usando el Nexxt, la ip de la maquina suele ser:
# 192.168.0.100


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
ozono = 24				# GPIO24, pin nro 18
spritz_relay = 22		# GPIO22, pin nro 15
coinhibitor_relay = 23	# GPIO23, pin nro 16
UV_relay = 18			# GPIO18, pin nro 12

GPIO.setup(button, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(valve_relay, GPIO.OUT)
GPIO.setup(ozono, GPIO.OUT)
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
    api_read_url = "http://api.carriots.com/streams/IGUA@igua.devs.igua.devs"

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

ser_acc = serial.Serial('/dev/ttyACM0',9600,timeout = 0)
ser_flw =  serial.Serial('/dev/ttyACM2',9600,timeout = None)
ser_lcd =  serial.Serial('/dev/ttyACM1',9600,timeout = None, parity = serial.PARITY_NONE, xonxoff = False, rtscts = False, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS)


def read_flw():
	global ser_flw
	global string_flw
	bytesToRead = ser_flw.inWaiting()
	if bytesToRead > 0:
		sleep(0.05)
		diff = 0
		bytesToRead = ser_flw.inWaiting()
		# print("bytes to read on ser_flw: ", bytesToRead)
		string_flw = str(ser_flw.readline(),'utf-8')
		# print("received on ser_flw: ", string_flw)
		string_flw = string_flw.lstrip('r')
		string_flw = string_flw.strip('\n\r')
		string_flw = string_flw.strip('\r\n')
		

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
device = "IGUA@igua.devs.igua.devs"  # Replace with the id_developer of your device
# device = "IGUA_FEST_1@kikomayorga.kikomayorga"
# device = "IGUA_FEST_1@kikomayorga.kikomayorga"
# device = "IGUA_FEST_1@kikomayorga.kikomayorga"
# device = "IGUA_FEST_1@kikomayorga.kikomayorga"
# device = "IGUA_FEST_CHANCHA@kikomayorga.kikomayorga"
# device = "IGUA_FEST_DMD@kikomayorga.kikomayorga"  
apikey = "8971eb3a06dd2d55a7794f6c5c0067cbd8d349a04fd67fc611dc0dec552c41ce"  # Replace with your Carriots apikey
client_carriots = Client(apikey)

# ejemplo de curl "para traer todos los ulktimos streams"
# curl --header carriots.apikey:13f622d642b12cc336fa6bfde36e1561c6ac7eea19bd88d7c32246d0fca45691 http://api.carriots.com/streams/?device=IGUA01@kikomayorga.kikomayorga

#para carriots




#para lcd
def lcd_bienvenida_linear(now):
	if  now == 0:
		ser_lcd.write('mAs agua pura...   para Todos!!!'.encode())
	elif now == 1:
		ser_lcd.write('cuida tu salud..y la del planeta'.encode())
	elif now == 2:
		ser_lcd.write('y la del planetamenos plAstico!!'.encode())
	elif now == 3:
		ser_lcd.write('f/aguaigua      http://igua.pe  '.encode())
	elif now == 4:
		ser_lcd.write('hola mundo!!!   hola igua!!!    '.encode())
	elif now == 5:
		ser_lcd.write('hola igua!!!    salud!          '.encode())
	
	return 1

def lcd_bienvenida_pwyw(now):
	if  now == 0:
		ser_lcd.write('mAs agua pura...   para Todos!!!'.encode())
	elif now == 1:
		ser_lcd.write('cuida tu salud..y la del planeta'.encode())
	elif now == 2:
		ser_lcd.write('y la del planeta                '.encode())
	elif now == 3:
		ser_lcd.write('f/aguaigua      http://igua.pe  '.encode())
	elif now == 4:
		ser_lcd.write('hola mundo!!!   hola igua!!!    '.encode())
	elif now == 5:
		ser_lcd.write('agua igua,      salud!          '.encode())
	
	return 1

def lcd_acumula_linear(solesacumulados):
	ser_lcd.write(('saldo: S/ ' + str(format(solesacumulados, '.2f'))).encode())
	return 1
	
def lcd_acumula_pwyw(solesacumulados):
	ser_lcd.write(('tu aporte: S/. ' + str(format(solesacumulados, '.2f'))).encode())	
		
def lcd_servidos_lt(servidos_lt,diff):
	global button
	button_state = GPIO.input(button)
	if button_state == GPIO.LOW:
		ser_lcd.write(('tienes: ' + str(format(servidos_lt/1000, '.3f')) + ' l  ' + '                ' ).encode())	
	if button_state == GPIO.HIGH:
		ser_lcd.write(('tienes: ' + str(format(servidos_lt/1000, '.3f')) + ' l  ' + '          ... ' + str(format(diff, '.0f')) + 's').encode())	
	
	
def lcd_ozonizando():
	ser_lcd.write('... ozonizando ...              '.encode())	

def lcd_agradece():
	ser_lcd.write('... gracias !!!                 '.encode())	

def inicializaGPIO():
	set_valve(0)
	set_UV(1)
	set_ozono(0)	
	
def set_valve(valor):
	if valor == 0:
		GPIO.output(valve_relay, 1)
		GPIO.output(spritz_relay, 0)
	if valor == 1:
		GPIO.output(valve_relay, 0)
		GPIO.output(spritz_relay, 1)
		
def set_ozono(valor):
	if valor == 0:
		GPIO.output(ozono, 1)
	if valor == 1:
		GPIO.output(ozono, 0)
		
def set_UV(valor):
	if valor == 0:
		GPIO.output(UV_relay, 0)
	if valor == 1:
		GPIO.output(UV_relay, 1)
		
def set_accepting(valor):
	if valor == 0:
		GPIO.output(coinhibitor_relay, 1)
	if valor == 1:
		GPIO.output(coinhibitor_relay, 0)

'''
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
	
def detectaUsb():
	try ser_flw =  serial.Serial('/dev/ttyACM1',9600,timeout = None)
	
	 
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
		'''
				
def send_to_carriots():  #send collected data to carriots
	global device
	global servidolitros
	global solesacumulados
	timestamp = int(mktime(datetime.utcnow().timetuple()))
	timestamp = int(mktime(datetime.utcnow().timetuple()))
	solesstring = str(solesacumulados)
	data = {"protocol": "v2", "device": device, "at": timestamp, "data": {"maquina": "IGUA_02", "colectado soles": solesacumulados, "servido litros": format(servidos_lt/1000, '.3f')}}
	print(data)
	if is_connected() == True:
		carriots_response = client_carriots.send(data)
		print('conexion ok!')
		print(carriots_response.read())
	else:
		print('no connectivity available')
		
def read_flw():
	global ser_flw
	global string_flw
	bytesToRead = ser_flw.inWaiting()
	if bytesToRead > 0:
		sleep(0.05)
		diff = 0
		bytesToRead = ser_flw.inWaiting()
		# print("bytes to read on ser_flw: ", bytesToRead)
		string_flw = str(ser_flw.readline(),'utf-8')
		# print("received on ser_flw: ", string_flw)
		string_flw = string_flw.lstrip('r')
		string_flw = string_flw.strip('\n\r')
		string_flw = string_flw.strip('\r\n')
		

#globals		
servidos_lt = 0
servidos_lt_old = 0
servidos_litros_older = 0
loopcounter = 0	
servidos_total_old = 0

# last_string_psi_10 = "default string"
# last_string_psi_9 = "default string"
# last_string_psi_8 = "default string"
# last_string_psi_7 = "default string"
# last_string_psi_6 = "default string"
# last_string_psi_5 = "default string"
# last_string_psi_4 = "default string"
# last_string_psi_3 = "default string"
# last_string_psi_2 = "default string"
# last_string_psi_1 = "default string"
# string_tds = "default string"
# string_psi = "default string"
string_flw = "0"
diff = 0
# string_psi_array = ["0", "0",  "0",  "0", "0", "0"]
# string_psi_v1 = 0
# string_psi_psi1 = 0
# string_psi_v2 = 0
# string_psi_psi2 = 0
# string_psi_v3 = 0 
# string_psi_psi3 = 0

sleep(2)
hora_de_ultimo_ozono = time.time()		
inicializaGPIO()


#MAIN LOOP	
while 1 == 1:
	
	if process_id == 0:  #espera monedas
		set_accepting(0)
		ferrosacumulados = 0
		now_1 = now
		now = time.time()
		now = int((now/2)%6)
		if now != now_1:
			if modo_maquina == 0:
				display_bienvenida_linear(now)
				lcd_bienvenida_linear(now)
			if modo_maquina == 1:
				display_bienvenida_pwyw(now)
				lcd_bienvenida_pwyw(now)  # cuidado CUIDADO!!!!
				
		ahora = time.time()
		# print(ahora - hora_de_ultimo_ozono)
		if (ahora - hora_de_ultimo_ozono) > 10:  #cada 20 minutos
			# set_ozono(1)
			# set_accepting(1) #deja de aceptar
			# sleep(0.3)
			# lcd_ozonizando()
			# sleep(6)
			# set_ozono(0)
			# set_accepting(0) #vuelve a aceptar
			hora_de_ultimo_ozono = time.time()
			print("pasaron 2 minutos")

			
		
			
		
	
    #leer aceptador de monedas
		before = int(time.time())
		
		bytesToRead = ser_acc.inWaiting()
		if bytesToRead > 0:
			now = int(time.time())
			process_id = 1
			
	#aceptando monedas
	elif process_id == 1:
		set_UV(0)
		set_accepting(0)
		secondcycle = 0   #variable que inicializa el pid2
		bytesToRead = ser_acc.inWaiting()
		if bytesToRead > 0:
			sleep(0.5)
			bytesToRead = ser_acc.inWaiting()
			# print("bytes to read: ", bytesToRead)
			# string_igua = str(ser_acc.readline(),'utf-8')
			string_igua = ser_acc.read(2)		
			ferros = int(string_igua)
			ferrosacumulados = ferrosacumulados + ferros
			solesacumulados = ferrosacumulados / 10.0
			before = int(time.time()) 
			
			if modo_maquina == 0:
				display_acumula_linear(solesacumulados)
				lcd_acumula_linear(solesacumulados)
			if modo_maquina == 1:
				display_acumula_pwyw(solesacumulados)
				lcd_acumula_pwyw(solesacumulados)
		
		
		
		#TIMEOUT 
		now = int(time.time())
		diff = now - before
		print("diff vale:", cuenta_de_ciclos)


		#tap_button pressed
		button_state = GPIO.input(button)
		if (button_state == GPIO.LOW) or (diff > 20):
			diff = 0
			print ("switching to PID2")
			time.sleep(0.5)	
			diff = 0
			before = int(time.time())
			process_id = 2
			latch = 1
			servidos_lt = 0
			precio = 0.5
			servidos_total = 0
			counter_al_inicio = 0		           
			secondcycle = 0
			
			process_id = 2
		else:
			process_id = 1
			# print ("button is NOT PRESSED")	
		
	elif process_id == 2:	
		# enciende el pin de Ozono
		set_ozono(0)
		
		# muestra display "OZONIZANDO"
		# lcd_ozonizando()
		# espera N segs
		sleep(0.1)
		set_ozono(0)
		# apaga el pin de Ozono
		process_id = 3
	
	# habilitada vavula y muestra litros
	elif process_id == 3:
		set_accepting(1)
		print("estoy en el PID2")
		# ser_flw.flushInput()
		# read_psi()
		# clean_string_psi()
		# update_globalvars_psi()
		# read_tds()
		ser_flw.write('a'.encode())
		sleep(0.1)
		read_flw()
		hora_actual = int(time.time())
		hora_de_re_inicio_servida = hora_actual

						
		if modo_maquina == 0:
			litros_servir = 1000 * (solesacumulados / precio) 
		if modo_maquina == 1:
			litros_servir = 1000
		
		while process_id == 3:

			#verifica timeout
			hora_actual = int(time.time())
			tiempo_desde_inicio_servida = hora_actual - hora_de_re_inicio_servida
			
			ser_flw.write('a'.encode())
			sleep(0.1)
			read_flw()

			# se podrìa borrar?   if secondcycle == 1:     #a partir de la segunda corrida, muestro la cuenta regresiva
			servidos_lt = float(int(string_flw)/10)*0.95
			display_servidos_lt((litros_servir - servidos_lt),10 - tiempo_desde_inicio_servida)
			lcd_servidos_lt((litros_servir - servidos_lt),10 - tiempo_desde_inicio_servida)
			sleep(0.05)
				
				# print("mande el comando al display")
				
			# el boton resetea el tiempo maximo y enciende la válvula
			button_state = GPIO.input(button)
			if button_state == GPIO.LOW: 
				hora_de_re_inicio_servida = int(time.time())
				# print ("button is LOW - OR PRESSED")
				# time.sleep(0.05)
				set_valve(1)
				
			# el boton libre cierra la valvula
			if button_state == GPIO.HIGH:
				set_valve(0)
				# print('se solto boton')

			if (servidos_lt - litros_servir) > 0:  # si se pasa del limite a servir
				print ("se pasó del volumen a servir")
				set_valve(0)
				send_to_carriots()
				process_id = 4
					
			if tiempo_desde_inicio_servida > 10:     #si se demora mucho en re-servir		
				print ("se acabó el tiempo_desde_inicio_de_servida")
				set_valve(0)   #cerrando la valvula
				send_to_carriots()
				process_id = 4
				
					

	# deshabilita vavula y ozonizando
	elif process_id == 4:
		lcd_agradece()
		
		sleep(0.5)
		
		#resetea el flujometro
		ser_flw.write('aasdfasdf'.encode())
		
		#anexa al archivo en local
		timestamp = int(mktime(datetime.utcnow().timetuple()))
		fd = open('IGUA_DANNY_log.csv','a')
		# fd.write('timestamp: ' + str(timestamp) +', máquina: igua_bodega, volumen: ' + str(format(string_flw, '.3f')) + "\n")
		fd.write('timestamp: ' + str(timestamp) +', máquina: igua_bodegadanny, volumen: ' + str(format(servidos_lt, '.3f')) + "\n")
		fd.close()
		
		# set_ozono(1)		
		# muestra display "OZONIZANDO"
		# lcd_ozonizando()
		# espera N segs
		# sleep(10)
		# set_ozono(0)
		
		before = int(time.time()) 
		# print("before: ", before)

		
		while process_id==4:
			now = int(time.time())
			# print("now: ", now)	
			diff = now - before
			# print("diff: ", diff)
			if diff > 3:
				set_UV(1)
				process_id = 0
				#   apagar ozono
	
	


# todo: rfid
	
