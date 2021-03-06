#!/usr/bin/python3 import os

###########################################################
#          IGUA TOOLKIT

#          V0.1

###########################################################

# ¿Cómo preparar una máquina IGUA?

# se necesita instalar librerìas de pyhton:

# para leer el teclado en background:
# python3 -m pip install Pynput
#
# para conectar con google sheets:
# pip3 install gspread (como pi para que funcione el autoarranque)
# pip3 install --upgrade oauth2client
#
# para manejar la hora sin rolos
# pip3 install pytz
#
# para reproducir audio toca:
# sudo apt-get install mpg123
# 
# para audio por PWM ademas, agregar:
# dtoverlay=pwm-2chan,pin=18,func=2,pin2=13,func2=4
# en:
# sudo nano /boot/config.txt
# tomado de:
# https://www.youtube.com/watch?v=3pXB90IDNoY
#
# para instalar el modem ZTE MF 626 HSDPA
# http://myhowtosandprojects.blogspot.com/2013/12/how-to-setup-usb-3g-modem-linux.html
# parametros de este modem son:
'''
	########################################################
	# ZTE MF622 (aka "Onda MDC502HS")
	# ZTE MF626
	# ZTE MF628+ (tested version from Telia / Sweden)
	# ZTE MF633
	# ZTE MF636 (aka "Telstra / BigPond 7.2 Mobile Card")
	# ZTE MF637
	# and probably others not listed here
	#
	# Contributor: Joakim Wennergren and others

	DefaultVendor=  0x19d2
	DefaultProduct= 0x2000

	TargetVendor=   0x19d2
	TargetProduct=  0x0031

	MessageContent="5553424312345678000000000000061e000000000000000000000000000000"
	MessageContent2="5553424312345679000000000000061b000000020000000000000000000000"

	NeedResponse=1
'''
# para marcar el modem:
'''
lo que va adentro de /etc/wvdial.conf:

[Dialer 3gconnect] 
Init1 = ATZ 
Init2 = ATQ0 V1 E1 S0=0 &C1 &D2 +FCLASS=0 
Init3 = AT+CGDCONT=1,"IP","m2m.erictel.pe" 
Stupid Mode = 1 
Modem Type = Analog Modem 
ISDN = 0 
Phone = *99# 
Modem = /dev/gsmmodem 
Username = { } 
Password = { } 
Baud = 460800
'''


# además hay que incluir el archivo "IGUA_DRIVE_SECRET.json" dos veces:
# una vez en la carpeta  ~/ y otra vez en la carpeta igua-toolkit
#
# en raspi-config:
# i2c habilitado, vnc habilitado, ssh habilitado
#
# para clonar la carpeta de github a local:
# git clone http://github.com/kikomayorga/igua_toolkit/

# usando el Nexxt, la ip de la maquina suele ser:
# 192.168.0.100

# para configurar qué redes queremos aprender u olvidar:
# sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

# para hacer autostart:
# vamos a este folder: ~/.config/lxsession/LXDE-pi/
# y alli pegamos y sobreescribimos con el archivo autostart que viene
# en el folder igua-toolkit
#
# para poder entrar mejor con VNC, (resolucion por defecto es ridicula)
# modificamos estas líneas en config.txt:
# (basado en: https://www.youtube.com/watch?v=LlXx9yVfQ0k)
# #uncomment to force a specific HDMI mode (this will force VGA)
# #hdmi_group=1
# #hdmi_mode=1
# hdmi_ignore_edid=0xa5000080
# hdmi_group=2
# hdmi_mode=*100077
#
# para poder acceder remotamente con dataplicity, es necesario ejecutar
# un comando que se obtiene al crear una nueva cuenta con dataplicity
# las cuentas dataplicity que estamos usando son igua.devs+001@gmail.com
# donde 001 es para la maquina de dani, 002 es para la 2da azul

# para instalar USB de telefonica: ZTE MF 626 HSDPA
# instruccciones en: 
# http://myhowtosandprojects.blogspot.com/2013/12/how-to-setup-usb-3g-modem-linux.html


###########################################################
# intentando conectar a inernet



# instalando un logger
import logging

logger = logging.getLogger('scope.name')
file_log_handler = logging.FileHandler('logfile.log')
logger.addHandler(file_log_handler)
stderr_log_handler = logging.StreamHandler()
logger.addHandler(stderr_log_handler)
# nice output format para el logger
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_log_handler.setFormatter(formatter)
stderr_log_handler.setFormatter(formatter)
# logger.info('Info message')
# logger.error('Error message')

#librerias propias
from igua_display import startdisplay, refreshdisplay
from igua_display import display_bienvenida_linear, display_bienvenida_pwyw
from igua_display import display_acumula_pwyw, display_acumula_linear
from igua_display import display_servidos_lt, display_agradece

#librerias necesarias
from pynput.keyboard import Key, Listener
import os

#inicializando variables
codigodemaquina = "IGUA_I2C_000_socorro_test"
modo_serial = 'i2c'  #puede ser 'usb' o 'i2c'   ojo Jose Velarde

process_id = 0                  #
last = 0.0
running = 1
solesacumulados = 0   			#transaction-wise accumulator
ferrosacumulados = 0  			#transaction-wise accumulator
cuenta_de_ciclos = 0			#transactions counter on eeprom	FUNCIONA?????
modo_maquina = 0  				# 1: pay what you want , 0: linear mode
button_state = 0
now = 0
now_1 = 0
rfid_id = 0

#globales del keypad
keypadcredit = float(0.0)
cancelrequest_timeout = 0
keypadcreditbuffer = ''
pass_user = '000000'
pass_credit_today = 0
passcelda = ''
pass_dia_N = 1000    #un nro mayor al tope de 7 o 30, se chancará
lcd_captured_by_keypad = 0

# para el keypad
def on_press(key):

	try:
		os.system('mpg123 -q iguino_sounds/_iguino_keypress.mp3 &')
	except:
		pass

	global cancelrequest_timeout
	global keypadcredit
	global keypadcreditbuffer
	global process_id
	global pass_user
	global pass_credit_today
	global passcelda
	global pass_dia_N
	global formadepago
	global worksheet0
	global worksheet1
	global worksheet2
	global worksheet3
	global lcd_captured_by_keypad
	global credentials
	global gc
	global sheet

	k = 0   #declarando indice para cadena
	#para monitorear todas las teclas
	print('{0} pressed'.format(key))
	lcd_captured_by_keypad = 1

	#caso que se haya ingresado enter
	if key == Key.enter and process_id==0:
		userpassnr = '000000'   #codigo por defecto
		pass_row = [0,0,0]
		keypadcredit = float(0.0)
		print("se presionó enter")
		keypadcreditbuffer = keypadcreditbuffer.replace(",", ".")

		try:
			if float(keypadcreditbuffer) > 2.0:
				print("valor sospechosamente alto. se descarta. ")
				lcd_string('Ingrese valor     menor a 2.00 S/')
				print("keypadcredit resulting value: " + str(keypadcredit))
				lcd_captured_by_keypad = 0

			else:
				keypadcredit = float(keypadcreditbuffer)
				print("se convirtio el valor de teclado en float.")
				print("keypadcredit verified value: " + str(keypadcredit))
				lcd_string('se cargó soles  S/' + str(keypadcredit))


		except:
				print("el nro del keypad no se logró convertir a soles.... ahora veamos si hay iguapass")


		if keypadcreditbuffer[0:1] == "*" or keypadcreditbuffer[0:1] == "+":   #veamos si hay un código de iguapass
			print("se ingresó código iguapass nro: " + keypadcreditbuffer[1:5])

			try:
				userpassnr = keypadcreditbuffer[1:7]
				dummyint = int(userpassnr)
				print('userpassnr es: ' + userpassnr)
				lcd_string('buscando... pass ...' + userpassnr)


			except:
				print("el pass debe ser de la forma *NNNNNN o +NNNNNN.")
				lcd_string('codigo de pass  ..no reconocido.')
				sleep(1.2)
				lcd_captured_by_keypad = 0
				userpassnr = '000000'
				pass_row = [0]


            # para pases 7x1
			if userpassnr != '000000':
				print("buscando crédito en pestaña 7x1... ")
				lcd_string("buscando crEdito ...            ")
				auth_on_gspread()
				if connection_flag == 1:
					# worksheet2: aquí están los igua passes 7x1
					try:
						passcelda = worksheet2.find(userpassnr)
						pass_row = worksheet2.row_values(passcelda.row)
						print('Exito! se encontró igua pass 7x1')
					except:
						print('no fue posible obtener registro de iguapass 7x1')
						pass_row = [0]
						# lcd_captured_by_keypad = 0
				else:
					pass_row = [0]
					print('al parecer no hay internet')
					lcd_string('sin internet... no tenemos pases')
					sleep(1.5)
					lcd_captured_by_keypad = 0

			if pass_row != [0]:
				print(pass_row)
				if len(pass_row) <2:    #descartamos que la fila esté vacía
					print('cuenta sin suficientes datos. probablemente la fila de excel está vacía')
					lcd_string('cOdigo no reconocido            ')
					lcd_captured_by_keypad = 0

				else:
					pass_user = pass_row[0]
					pass_plantype = pass_row[1]
					pass_activeflag = pass_row[2]
					pass_activationdate = pass_row[3]
					if pass_activeflag == '0':
						pass_activeflag = 1
						pass_activationdate = datetime.now().timetuple().tm_yday
						try:
							worksheet2.update_cell(passcelda.row, 4, pass_activationdate)
							print('se actualizó registro de fecha de activación')
							worksheet2.update_cell(passcelda.row, 3, '1')
							print('se actualizó registro de activeflag')
						except:
							print('no se pudo completar registro de fecha de activación')
							print('no, no se pudo completar registro de activeflag')

					pass_dia_N = datetime.now().timetuple().tm_yday - int(pass_activationdate)

					pass_credit_today = int(pass_row[(6 + pass_dia_N)])
					if pass_credit_today == 0:
						print('no hay credito disponible por hoy')
						lcd_string('sin crEdito hoy.')
						sleep(3)
						lcd_captured_by_keypad = 0
					elif pass_dia_N > 7:
						print('este iguapass 7x1 ya venciO...')
						lcd_string('este iguapass 7x1 ya venciO.....')
						sleep(2)
						lcd_captured_by_keypad = 0

					else:
						print('se cargó crédito de hoy: ' + str(pass_credit_today))
						lcd_string('su saldo de hoy:' + (str(pass_credit_today) + ' mililitros!').ljust(16))
						sleep(2)
						formadepago = 'pass-7x1'
						process_id = 3

			#para pases "30-dias"
			if process_id == 0 and userpassnr != '000000':   #para pases "30-dias"
				print("buscando crédito en pestaña 30-dias... ")
				lcd_string('buscando crEdito Iguapass...    ')
				auth_on_gspread()
				if connection_flag == 1:
					try:
						passcelda = worksheet3.find(userpassnr) #Find a cell with exact string value
						pass_row = worksheet3.row_values(passcelda.row)
						print('Exito! se encontrO igua pass 30 dIas')
					except:
						print('no fue posible obtener registro de iguapass 30-días')
						lcd_string('No se hallO Igua-pass : (       ')
						sleep(1.2)
						pass_row = [0]
						lcd_captured_by_keypad = 0
				else:
					pass_row = [0]
					print('al parecer no hay internet')
					sleep(1)
					lcd_captured_by_keypad = 0

			if process_id == 0 and pass_row != [0]:
				print(pass_row)
				if len(pass_row) <2:    #descartamos que la fila esté vacía
					print('cuenta sin suficientes datos. probablemente la fila de excel está vacía')
					lcd_string('contactar: igua.devs@gmail.com')
					sleep(2)
					lcd_captured_by_keypad = 0

				else:
					pass_user = pass_row[0]
					pass_plantype = pass_row[1]
					pass_activeflag = pass_row[2]
					pass_activationdate = pass_row[3]
					if pass_activeflag == '0':
						pass_activeflag = 1
						pass_activationdate = datetime.now().timetuple().tm_yday
						try:
							worksheet3.update_cell(passcelda.row, 4, pass_activationdate)
							print('se actualizó registro de fecha de activación')
							worksheet3.update_cell(passcelda.row, 3, '1')
							print('se actualizó registro de activeflag')
						except:
							print('no se pudo completar registro de fecha de activación')
							print('o, no se pudo completar registro de activeflag')

					pass_dia_N = datetime.now().timetuple().tm_yday - int(pass_activationdate)
					# pass_credit_today = int(pass_row[(6 + pass_dia_N)])
					pass_credit_today = int(pass_row[6])
					if pass_credit_today == 0:
						print('ooops. iguapass sin saldo....   ')
						lcd_string('ooops! no hay credito disponible para hoy')
						sleep(2)
						lcd_captured_by_keypad = 0
					elif pass_dia_N > 30:
						print('ooops. iguapass vencido....   ')
						lcd_string('ooops. iguapass vencido....     ')
						sleep(2)
						lcd_captured_by_keypad = 0
					else:
						print('se cargó crédito: ' + str(pass_credit_today))
						lcd_string('saldo en pass:  ' + str(pass_credit_today).ljust(16))
						sleep(2)
						lcd_captured_by_keypad = 0
						formadepago = 'pass-30dias'
						process_id = 3

		keypadcreditbuffer = ""    #no se logró cargar iguapass alguno

	#caso que sea cualquier otra tecla, acumular cadena
	elif process_id==0 and key == Key.backspace:
		keypadcreditbuffer = ""
		print("se borro la cadena, ahora solo queda un string vacio como este: " + keypadcreditbuffer)
		lcd_string("anulando...")
		sleep(0.5)
		lcd_captured_by_keypad = 0

	elif process_id==0:

		if key == Key.end:
			key = "'1'"
		if key == Key.down:
			key = "'2'"
		if key == Key.page_down:
			key = "'3'"
		if key == Key.left:
			key = "'4'"
		if str(key)[0:1]=="<":
			key = "'5'"
		if key == Key.right:
			key = "'6'"
		if key == Key.home:
			key = "'7'"
		if key == Key.up:
			key = "'8'"
		if key == Key.page_up:
			key = "'9'"
		if key == Key.insert:
			key = "'0'"
		if key == Key.delete:
			key = "'.'"

		keypadcreditbuffer = keypadcreditbuffer + str(key)[1:2]
		print("se va acumulando la cadena: " + keypadcreditbuffer)
		if len(keypadcreditbuffer) > 8:
			keypadcreditbuffer = ''
		if modo_serial == 'usb':
			lcd_string(('>>> ' + keypadcreditbuffer).ljust(32))
		elif modo_serial == 'i2c':
			lcd_string(('>>> ' + keypadcreditbuffer))
			sleep(0.2)

	elif process_id==3 and (key == Key.backspace or key == Key.enter):
		print("se presiono backspace para cancelar tiempo de servida.")
		lcd_captured_by_keypad = 0
		cancelrequest_timeout = 1

	else:
		pass

def escribir_nuevo_saldo_para_pass():
	global passcelda
	global pass_dia_N
	global pass_credit_today
	global worksheet0
	global worksheet1
	global worksheet2
	global worksheet3
	global formadepago

	if formadepago == 'pass-7x1':
		auth_on_gspread()
		try:
			worksheet2.update_cell(passcelda.row, (pass_dia_N + 7), pass_credit_today)
			print('Se logró actualizar saldo del día.')
		except:
			print('No se logró actualizar saldo del pass-7x1.')

	if formadepago == 'pass-30dias':
		auth_on_gspread()
		try:
			worksheet3.update_cell(passcelda.row, 7, pass_credit_today)
			print('Se logró actualizar saldo del pass-30dias.')
		except:
			print('No se logró actualizar saldo del pass-30dias.')

def on_release(key):
    # print('{0} release'.format(key))
    # if key == Key.esc:
        # Stopstener
    #    return False
    pass

#fin para el keypad


#para gspread

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def auth_on_gspread():
	global gc
	global worksheet0
	global worksheet1
	global worksheet2
	global worksheet3
	global connection_flag

	try:
		sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1XzZeGav7xOc-Vvhuq6aCoox_dsWTQruLx04xkl_SBbg/edit?usp=drive_web&ouid=106328115973184488048')
		worksheet0 = sheet.get_worksheet(0)
		worksheet1 = sheet.get_worksheet(1)
		worksheet2 = sheet.get_worksheet(2)
		worksheet3 = sheet.get_worksheet(3)
	except:
		scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
		credentials = ServiceAccountCredentials.from_json_keyfile_name('IGUA_DRIVE_SECRET.json', scope)
		try:
			gc = gspread.authorize(credentials)
			sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1XzZeGav7xOc-Vvhuq6aCoox_dsWTQruLx04xkl_SBbg/edit?usp=drive_web&ouid=106328115973184488048')
			connection_flag = 1
			print('bien! nos conectamos con oauth2client!')
		except:
			connection_flag = 0
			print('probablemente no haya conexion a internet')
		try:
			worksheet0 = sheet.get_worksheet(0)
			worksheet1 = sheet.get_worksheet(1)
			worksheet2 = sheet.get_worksheet(2)
			worksheet3 = sheet.get_worksheet(3)
			print('se logró cargar las hojas de accounts_data en drive de igua.devs')
		except:
			print('no se logró cargar las hojas de accounts_data en drive de igua.devs')
			logger.error('No se logró recuperar autenticaciòn en gspread.')



def registra_en_drive():
	global device
	global servidos_lt
	global solesacumulados
	global formadepago
	global pass_user
	global gc
	global credentials
	global worksheet0
	global worksheet1
	global worksheet2
	global worksheet3

	# preprarar data
	timestamp = int(mktime(datetime.utcnow().timetuple())) #timestampglobal utc
	now = datetime.now(pytz.timezone('America/Lima')) #timestamplocal lima
	# timestamplocalstring = now.strftime('%Y-%m-%d %H:%M:%S') #como string en HRF
	timestamplocalstring_date = now.strftime('%d/%m/%Y') #la fecha como string en HRF
	timestamplocalstring_time = now.strftime('%H:%M:%S') #la hora como string en HRF
	solesstring = str(format(solesacumulados*100, ".0f"))
	mlservidosstring = str(format(servidos_lt, ".0f"))
	data = [timestamp, timestamplocalstring_date, timestamplocalstring_time, codigodemaquina, str(formadepago), pass_user, solesstring, mlservidosstring]

	# verificar primero que haya donde escribir (drive)
	auth_on_gspread()
	if connection_flag == 1:
		# averiguar cual es la siguiente fila:
		next_row = int(worksheet1.cell(3, 2).value)
		print('next row: ' + str(next_row))
		#indicar region a escribir
		cell_list = worksheet1.range('A' + str(next_row) + ':H' + str(next_row))
		#cargar la data en cell-list
		looper = 0
		for cell in cell_list:
			cell.value = str(data[looper])
			looper = looper + 1

		# Registrando en drive en "batch" (cell_list)
		worksheet1.update_cells(cell_list)
		next_row = int(next_row) + 1
		worksheet1.update_acell('B3', next_row)
		print(data)
	else:
		print('no se pudo registrar venta, no hay internet. ')
		lcd_string('sin internet... no tenemos pases')
		sleep(1.5)


#importando funciones y librerias
from datetime import datetime, timezone
from datetime import datetime, timezone
import pytz
from time import sleep
from time import strftime
import time
import serial
import re
import socket
import threading

#importando modulos para i2c
if modo_serial == 'i2c':
	from smbus import SMBus
	bus = SMBus(1)

REMOTE_SERVER = "www.google.com"

# para threading
class myThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      print ("Starting " + self.name)
      # Get lock to synchronize threads
      threadLock.acquire()
      keyboardpoller()
      # Free lock to release next thread
      threadLock.release()

def keyboardpoller():
	while 1==1:
		# Collect events until released
		with Listener(
				on_press=on_press,
				on_release=on_release) as listener:
			listener.join()

#creamos thread y lo inicializamos
threadLock = threading.Lock()
threads = []
thread1 = myThread(1, "keylistener", 1)
thread1.start()
threads.append(thread1)


# configuaracion de entradas/saldas del RPI
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

if modo_serial == 'usb':
	button = 4         # GPIO04, pin nro 07
	valve_relay = 17   # GPIO17, pin nro 11
	spritz_relay = 22	# GPIO22, pin nro 15        
	button2 = 27			# GPIO27, pin nro 13
	ozono = 24				# GPIO24, pin nro 18
	coinhibitor_relay = 23	# GPIO23, pin nro 16
	UV_relay = 18			# GPIO18, pin nro 12

elif modo_serial == 'i2c':
	button = 27         # GPIO04, pin nro 11
	button2 = 10
	button_light= 22
	valve_relay = 4
	spritz_relay = 17
	ozono = 9				# GPIO24, pin nro 18
	coinhibitor_relay = 23	# GPIO23, pin nro 16
	UV_relay = 24			# GPIO18, pin nro 12
	   
GPIO.setup(button, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(valve_relay, GPIO.OUT)
GPIO.setup(ozono, GPIO.OUT)
GPIO.setup(spritz_relay, GPIO.OUT)
GPIO.setup(coinhibitor_relay, GPIO.OUT)
GPIO.setup(UV_relay, GPIO.OUT)
if modo_serial == 'i2c':
	GPIO.setup(button_light, GPIO.OUT)


#para carriots
from urllib.request import urlopen, Request
from time import mktime, sleep
from datetime import datetime, timezone
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

def send_to_carriots():  #send collected data to carriots
	global device
	global servidos_lt
	global solesacumulados
	global formadepago
	global pass_user
	global codigodemaquina

	timestamp = int(mktime(datetime.utcnow().timetuple()))
	solesstring = str(format(solesacumulados*100, ".0f"))
	mlservidosstring = str(format(servidos_lt, ".0f"))
	data = {"protocol": "v2", "device": device, "at": timestamp, "data": {"maquina": (codigodemaquina + " - " + str(formadepago)), "iguapassnr: ": pass_user, "colectado centavos": solesstring, "servido mililitros": mlservidosstring}}
	# print(data)
	if is_connected() == True:
		carriots_response = client_carriots.send(data)
		print('conexion ok! respuesta de carriots:')
		print(carriots_response.read())
	else:
		print('no connectivity available')

#para carriots
device = "IGUA@igua.devs.igua.devs"  # Replace with the id_developer of your device
apikey = "8971eb3a06dd2d55a7794f6c5c0067cbd8d349a04fd67fc611dc0dec552c41ce"  # Replace with your Carriots apikey
client_carriots = Client(apikey)



# funciòn que verifica conectividad
def is_connected():
    try:
        host = socket.gethostbyname(REMOTE_SERVER)
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False

# declarar los puertos seriales o crear puertos i2c



if modo_serial == 'usb':
	try:
		ser_acc = serial.Serial('/dev/ttyACM0',9600,timeout = 0)
		ser_flw =  serial.Serial('/dev/ttyACM2',9600,timeout = None)
		ser_lcd =  serial.Serial('/dev/ttyACM1',9600,timeout = None, parity = serial.PARITY_NONE, xonxoff = False, rtscts = False, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS)
	except:
		print('algo anda mal al declarar los puertos usb...')

if modo_serial == 'i2c':
	#acá va lo de Jose Velarde
	add_acc = 0x03 #address i2c del acceptor
	add_rfid = 0x04 #address i2c del rfid
	add_lcd = 0x05 #address i2c del lcd
	add_flw = 0x06 #address i2c del flujometro



def read_flw():
	global modo_serial
	if modo_serial == 'usb':
		global ser_flw
		global string_flw
		bytesToRead = ser_flw.inWaiting()
		if bytesToRead > 0:
			sleep(0.05)
			diff = 0
			string_flw = str(ser_flw.readline(),'utf-8')
			string_flw = string_flw.lstrip('r')
			string_flw = string_flw.strip('\n\r')
			string_flw = string_flw.strip('\r\n')
	elif modo_serial == 'i2c':
		try:
			lectura_flujo = bus.read_i2c_block_data(add_flw,0,2)
			if lectura_flujo [1]!=255:
				string_flw=lectura_flujo [0]+lectura_flujo [1]*128
				print(str(lectura_flujo )+" = "+str(lectura_flujo [0]+lectura_flujo [1]*128))
				sleep(0.01)
		except:
			pass



# setup display
startdisplay()


#para lcd
def lcd_bienvenida_linear(now):
	global lcd_captured_by_keypad
	global modo_serial
	if lcd_captured_by_keypad == 0:
		if modo_serial == 'usb' and now == 0:
			ser_lcd.write('mAs agua pura...   para Todos!!!'.encode())
		if modo_serial == 'usb' and now == 1:
			ser_lcd.write('cuida tu salud..y la del planeta'.encode())
		if modo_serial == 'usb' and now == 2:
			ser_lcd.write('juntos contra      el plAstico!!'.encode())
		if modo_serial == 'usb' and now == 3:
			ser_lcd.write('f/aguaigua      http://igua.pe  '.encode())
		if modo_serial == 'usb' and now == 4:
			ser_lcd.write('hola mundo!!!   hola igua!!!    '.encode())
		if modo_serial == 'usb' and now == 5:
			ser_lcd.write('agua igua!!!           salud!   '.encode())

		if modo_serial == 'i2c' and now == 0:
			cadena_i2c("mAs agua pura...   para Todos!!!")
			#sleep(2)
		if modo_serial == 'i2c' and now == 1:
			cadena_i2c("cuida tu salud y la del planeta")
			#sleep(2)
		if modo_serial == 'i2c' and now == 2:
			cadena_i2c("juntos contra      el plAstico!!")
			#sleep(2)
		if modo_serial == 'i2c' and now == 3:
			cadena_i2c("f/aguaigua      http://igua.pe ")
			#sleep(2)
		if modo_serial == 'i2c' and now == 4:
			cadena_i2c("hola mundo!!!   hola igua!!!")
			#sleep(2)
		if modo_serial == 'i2c' and now == 5:
			cadena_i2c("agua igua!!!           salud!")
			#sleep(2)
	else:
		pass

def lcd_bienvenida_pwyw(now):
	### revisar bien esto... se ha roto !
	global lcd_captured_by_keypad
	global modo_serial
	if lcd_captured_by_keypad == 0:
		if modo_serial == 'usb':
			if  now == 0:
				ser_lcd.write('mAs agua pura...   para Todos!!!'.encode())
			elif now == 1:
				ser_lcd.write('cuida tu salud y la del planeta'.encode())
			elif now == 2:
				ser_lcd.write('y la del planeta                '.encode())
			elif now == 3:
				ser_lcd.write('f/aguaigua      http://igua.pe  '.encode())
			elif now == 4:
				ser_lcd.write('hola mundo!!!   hola igua!!!    '.encode())
			elif now == 5:
				ser_lcd.write('agua igua,      salud!          '.encode())

		elif modo_serial == 'i2c':
			#acá va lo de Jose Velarde
			pass
		else:
			pass


	return 1

def lcd_acumula_linear(solesacumulados):
	global modo_serial
	if modo_serial == 'usb':
		ser_lcd.write(('tienes: S/ ' + str(format(solesacumulados, '.2f')) + '                 ').encode())
	elif modo_serial == 'i2c':
		#acá va lo de Jose Velarde
		pass
	else:
		pass

def lcd_acumula_pwyw(solesacumulados):
	global modo_serial
	if modo_serial == 'usb':
		ser_lcd.write(('tu aporte: S/. ' + str(format(solesacumulados, '.2f')) + '             ').encode())
	elif modo_serial == 'i2c':
		#acá va lo de Jose Velarde
		pass
	else:
		pass


def lcd_servidos_lt(servidos_lt,diff):
	global button
	button_state = GPIO.input(button)
	global modo_serial
	if modo_serial == 'usb':
		if button_state == GPIO.LOW:
			ser_lcd.write(('tienes: ' + str(format(servidos_lt/1000, '.3f')) + ' l  ' + '                ' ).encode())
		if button_state == GPIO.HIGH:
			ser_lcd.write(('tienes: ' + str(format(servidos_lt/1000, '.3f')) + ' l  ' + '          ... ' + str(format(diff, '.0f')) + 's').encode())
	elif modo_serial == 'i2c':
		cadena_i2c(('tienes: ' + str(format(servidos_lt/1000, '.3f')) + 'l  ' + '     ... ' + str(format(diff, '.0f')) + 's'))
	else:
		pass



def lcd_ozonizando():
	global modo_serial
	if modo_serial == 'usb':
		ser_lcd.write('... ozonizando ...              '.encode())
	elif modo_serial == 'i2c':
		cadena_i2c('... ozonizando ...              ')
		pass
	else:
		pass


def lcd_cancelando():
	global modo_serial
	if modo_serial == 'usb':
		ser_lcd.write('..gracias! ...       #tomaigua !'.encode())
	elif modo_serial == 'i2c':
		cadena_i2c('..gracias! ...       #tomaigua !')
		pass
	else:
		pass

def lcd_agradece():
	global modo_serial
	if modo_serial == 'usb':
		ser_lcd.write('... gracias !!!                 '.encode())
	elif modo_serial == 'i2c':
		cadena_i2c('..gracias! ...       #tomaigua !')
	else:
		pass

def lcd_string(cadena):
	global modo_serial
	if modo_serial == 'usb':
		if len(cadena) > 32:
			print('cadena mayor a 32 caracteres')
		else:
			ser_lcd.write((cadena.ljust(32)).encode())
	elif modo_serial == 'i2c':
		if len(cadena) > 32:
			print('cadena mayor a 32 caracteres')
		else:
			cadena = cadena.ljust(32)

		try:
			bus.write_byte(0x05,38)
			sleep(0.0001)
			for char in cadena:
				bus.write_byte(0x05,ord(char))
				sleep(0.0001)
		except:
			pass
		pass
	else:
		print('wrong modo_serial')
		pass

def inicializaGPIO():
	set_valve(0)
	set_UV(1)
	set_ozono(0)

def set_valve(valor):
	if valor == 0:
		if modo_serial == 'usb':
			GPIO.output(valve_relay, 1)
			GPIO.output(spritz_relay, 0)
		if modo_serial == 'i2c':
			GPIO.output(valve_relay, 0)
			GPIO.output(spritz_relay, 1)
			GPIO.output(button_light, 0)
	if valor == 1:
		if modo_serial == 'usb':
			GPIO.output(valve_relay, 0)
			GPIO.output(spritz_relay, 1)
		if modo_serial == 'i2c':
			GPIO.output(valve_relay, 1)
			GPIO.output(spritz_relay, 0)
			GPIO.output(button_light, 1)

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

def cadena_i2c(string):
	
	if len(string) > 32:
		print('cadena mayor a 32 caracteres')
	else:
		string = string.ljust(32)

	try:
		bus.write_byte(0x05,38)
		sleep(0.0001)
		for char in string:
			bus.write_byte(0x05,ord(char))
			sleep(0.0001)
	except:
		pass
	
	return 

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





#globals
servidos_lt = 0
servidos_lt_old = 0
servidos_litros_older = 0
loopcounter = 0
servidos_total_old = 0
precio = 1.0
formadepago = "cash"
connection_flag = 1   #asumimos que si hay internet

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

last_valve_state = "closed"
current_valve_state = "closed"


tiempo_ultimo_click = int(round(time.time() * 1000))
tiempo_penultimo_click = tiempo_ultimo_click
tiempo_entre_clicks = 10000

inicializaGPIO()


lcd_string(' CONECTANDO ..               ...')
print('se intetará marcar el modem....')
os.system('sudo wvdial 3gconnect &')
sleep(15)
#inicializamos con drive
auth_on_gspread()


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
				lcd_bienvenida_pwyw(now)  # cuidado CUIDADO!!!! no existe declaración!

		ahora = time.time()
		# print(ahora - hora_de_ultimo_ozono)
		if (ahora - hora_de_ultimo_ozono) > 500:
			if is_connected() == False:
				lcd_string('RECONECTANDO ...        loop  ...')
				print('se intetará marcar el modem....')
				os.system('sudo wvdial 3gconnect')
				print('se intetará marcar el modem....')
				delay(10)
			else:
				print('bien! seguimos conectados con erictel....')
			# cada 20 minutos
			# set_ozono(1)
			# set_accepting(1) #deja de aceptar
			# sleep(0.3)
			# lcd_ozonizando()
			# sleep(6)
			# set_ozono(0)
			# set_accepting(0) #vuelve a aceptar
			hora_de_ultimo_ozono = time.time()
			print('ciclo de verificacion de conexion = 500 !')


    #leer aceptador de monedas
		before = int(time.time())    #se necesita esto aqui?
		if modo_serial == 'usb':
			bytesToRead = ser_acc.inWaiting()
		elif modo_serial == 'i2c':
			#aca viene lo de Jose Velarde
			bytesToRead = 0
			pass
    #leer rfid
		if modo_serial == 'usb':
			pass
		elif modo_serial == 'i2c':
			try:
				rfid_id = bus.read_i2c_block_data(0x04,0,4)
			except:
				pass


		if bytesToRead > 0:
			formadepago = "cash"
			try:
				os.system('mpg123 -q iguino_sounds/_iguino_beep2.mp3 &')
			except:
				print('no se puedo reproducir audio de moneda')
			now = int(time.time())   #se necesita esto aqui?
			process_id = 1


		if modo_serial == 'i2c':
			if (rfid_id[0]>0):
				print('primer digito del id:' + str(rfid_id[0]))

		if keypadcredit > 0.0:
			formadepago = "keypad"
			solesacumulados = keypadcredit
			before = int(time.time())  #se necesita esto?
			if modo_maquina == 0:
				display_acumula_linear(solesacumulados)
				lcd_acumula_linear(solesacumulados)
				sleep(1)
			if modo_maquina == 1:
				display_acumula_pwyw(solesacumulados)
				lcd_acumula_pwyw(solesacumulados)
				sleep(1)
			process_id = 2;


	#aceptando monedas
	elif process_id == 1:
		set_UV(0)
		set_accepting(0)
		secondcycle = 0   #variable que inicializa el pid2
		if modo_serial == 'usb':
			bytesToRead = ser_acc.inWaiting()
		elif modo_serial == 'i2c':
			#aca viene lo de Jose Velarde
			pass

		if bytesToRead > 0:
			sleep(0.5)
			if modo_serial == 'usb':
				bytesToRead = ser_acc.inWaiting()
				string_igua = ser_acc.read(2)
			elif modo_serial == 'i2c':
				#acá viene lo de Jose Velarde
				pass

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
		#print("diff vale:", cuenta_de_ciclos)


		#se presiona el botón
		button_state = GPIO.input(button)
		if (button_state == GPIO.LOW) or (diff > 200):
			diff = 0
			#print ("switching to PID2")
			time.sleep(0.5)
			diff = 0
			before = int(time.time())
			process_id = 2
			latch = 1
			servidos_lt = 0

			servidos_total = 0
			counter_al_inicio = 0
			secondcycle = 0
			process_id = 2
		else:
			process_id = 1
			

	elif process_id == 2:
		# enciende el pin de Ozono
		# set_ozono(0)
		# muestra display "OZONIZANDO"
		# lcd_ozonizando()
		# espera N segs
		# sleep(0)
		# set_ozono(0)
		# apaga el pin de Ozono
		process_id = 3

	# habilitada vavula y muestra litros
	elif process_id == 3:
		# os.system('mpg123 -q iguino_sounds/_iguino_serving.mp3 &')
		set_accepting(1)
		if modo_serial == 'usb':
			ser_flw.write('a'.encode())
		elif modo_serial == 'i2c':
			#acá viene lo de Jose Velarde
			pass
		sleep(0.1)
		read_flw()   #este se llama para ambos modos de modoserial
		hora_actual = int(time.time())
		hora_de_re_inicio_servida = hora_actual


		if modo_maquina == 0:
			if pass_credit_today != 0:
				litros_servir = int(pass_credit_today)
			else:
				litros_servir = 1000 * (solesacumulados / precio)

		# modo pay what you want
		if modo_maquina == 1:
			litros_servir = 1000

		while process_id == 3:

			#verifica timeout
			hora_actual = int(time.time())
			tiempo_desde_inicio_servida = hora_actual - hora_de_re_inicio_servida

			if modo_serial == 'usb':
				ser_flw.write('a'.encode())
				sleep(0.1)
			elif modo_serial == 'i2c':
				#acá viene lo de Jose Velarde
				pass
			
			read_flw()   #este funciona para ambos modos
			sleep(0.01)
			
			servidos_lt = float(int(string_flw)/10)*0.95
			# display_servidos_lt((litros_servir - servidos_lt),30 - tiempo_desde_inicio_servida)
			lcd_servidos_lt((litros_servir - servidos_lt),30 - tiempo_desde_inicio_servida)
			

			# el boton resetea el tiempo maximo y enciende la válvula
			button_state = GPIO.input(button)
			if button_state == GPIO.LOW:
				hora_de_re_inicio_servida = int(time.time())
				# print ("button is LOW - OR PRESSED")
				# time.sleep(0.05)
				set_valve(1)
				last_valve_state = current_valve_state
				current_valve_state = "open"

			# el boton libre cierra la valvula
			if button_state == GPIO.HIGH:
				set_valve(0)
				last_valve_state = current_valve_state
				current_valve_state = "closed"
				# print('se solto boton')
				
			# doble click
			if last_valve_state == "closed" and current_valve_state == "open":
				# flancosubida / se presionó
				tiempo_penultimo_click = tiempo_ultimo_click
				tiempo_ultimo_click = int(round(time.time() * 1000))
				tiempo_entre_clicks = tiempo_ultimo_click - tiempo_penultimo_click
				print("tiempo entre clicks: " + str(tiempo_entre_clicks))
				if tiempo_entre_clicks < 200:
					print("hubo un doble click")			
				pass
				
			if last_valve_state == "open" and current_valve_state == "closed":
				# flancobajada / se soltò
				# no se hace nada
				pass
 			

			if (servidos_lt - litros_servir) > 0:  # si se pasa del limite a servir
				print ("se pasó del volumen a servir")
				set_valve(0)
				lcd_agradece()
				if formadepago == "pass-7x1" or formadepago == "pass-30dias":
					print(' formadepago =es= pass ')
					pass_credit_today = '0'
					print(' remaining credit: ' + pass_credit_today)
					escribir_nuevo_saldo_para_pass()
					pass_credit_today = 0
				process_id = 4

			if tiempo_desde_inicio_servida > 30:     #si se demora mucho en 0.0.2 re-servir
				print ("se acabó el tiempo_desde_inicio_de_servida")
				set_valve(0)   #cerrando la valvula
				lcd_agradece()
				if formadepago == "pass-7x1" or formadepago == "pass-30dias":
					print(' formadepago =es= pass ')
					pass_credit_today = pass_credit_today - int(servidos_lt)
					print(' remaining credit: ' + str(pass_credit_today))
					escribir_nuevo_saldo_para_pass()
					pass_credit_today = 0            #una vez transferido el saldo a la db, borramos el credito local
				process_id = 4

			if cancelrequest_timeout == 1:
				print ("se cancelo el tiempo de espera (backspace)")
				set_valve(0)   #cerrando la valvula
				if formadepago == "pass-7x1" or formadepago == "pass-30dias":
					pass_credit_today = pass_credit_today - int(servidos_lt)
					escribir_nuevo_saldo_para_pass()
					pass_credit_today = 0
				if formadepago == "keypad":
					pass_credit_today = 0
				cancelrequest_timeout = 0
				lcd_cancelando()
				sleep(0.1)
				lcd_cancelando()
				process_id = 4


	# deshabilita vavula y ozonizando
	elif process_id == 4:
		os.system('mpg123 -q iguino_sounds/_iguino_thrills_upoct.mp3 &')
		#registra la transacción en la nube
		send_to_carriots()
		registra_en_drive()

        #anexa al archivo en local
		timestamp = int(mktime(datetime.utcnow().timetuple()))
		fd = open('IGUA_DANNY_log.csv','a')
		# fd.write('timestamp: ' + str(timestamp) +', máquina: igua_bodega, volumen: ' + str(format(string_flw, '.3f')) + "\n")
		fd.write(str(timestamp) +','+ codigodemaquina + ',' + formadepago + ',' + str(servidos_lt) + "\n")
		fd.close()

        #resetea variables para nuevo ciclo
		keypadcredit = 0
		servidos_lt = 0
		keypadcreditbuffer = ""

		lcd_captured_by_keypad = 0

		#resetea el flujometro
		if modo_serial == 'usb':
			ser_flw.write('aasdfasdf'.encode())
		elif modo_serial == 'i2c':
			#acá viene lo de Jose Velarde
			bus.write_byte(add_flw, 1)
			pass




		#bloque de ozono

		# set_ozono(1)
		# muestra display "OZONIZANDO"
		# lcd_ozonizando()
		# espera N segs
		# sleep(10)
		# set_ozono(0)

		before = int(time.time())
		while process_id==4:
			now = int(time.time())
			diff = now - before
			if diff > 1:
				set_UV(1)
				process_id = 0
				#   apagar ozono


