#!/usr/bin/python3 import os

###########################################################

#          IGUA TOOLKIT

#          V0.1

###########################################################

# ¿Cómo preparar una máquina IGUA?

# se necesita instalar librerìas de pyhton:
# para leer el teclado en background:
# python3 -m pip install Pynput
# para conectar con google sheets:
# pip3 install gspread (como pi para que funcione el autoarranque)
# además hay que incluir el archivo "IGUA_DRIVE_SECRET.json"
# además hay que hacer: pip3 install --upgrade oauth2client


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

# para poder entrar mejor con VNC, (resolucion por defecto es ridicula)
# modificamos estas líneas en config.txt:
# (basado en: https://www.youtube.com/watch?v=LlXx9yVfQ0k)
# #uncomment to force a specific HDMI mode (this will force VGA)
# #hdmi_group=1
# #hdmi_mode=1
# hdmi_ignore_edid=0xa5000080
# hdmi_group=2
# hdmi_mode=85

# para poder acceder remotamente con dataplicity, es necesario ejecutar
# un comando que se obtiene al crear una nueva cuenta con dataplicity
# las cuentas dataplicity que estamos usando son igua.devs+001@gmail.com
# donde 001 es para la maquina de dani, 002 es para la 2da azul

###########################################################

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

#modulos custom
from igua_display import startdisplay, refreshdisplay 
from igua_display import display_bienvenida_linear, display_bienvenida_pwyw
from igua_display import display_acumula_pwyw, display_acumula_linear
from igua_display import display_servidos_lt, display_agradece 
from pynput.keyboard import Key, Listener

#inicializando variables
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

#globales del keypad
keypadcredit = float(0.0)
cancelrequest_timeout = 0
keypadcreditbuffer = ''
pass_credit_today = 0
passcelda = ''
pass_dia_N = 1000    #un nro mayor al tope de 7 o 30, se chancará

# para el keypad
def on_press(key):
	global cancelrequest_timeout
	global keypadcredit
	global keypadcreditbuffer
	global process_id
	global pass_credit_today
	global passcelda
	global pass_dia_N
	global formadepago
	global worksheet
	
	k = 0   #declarando indice para cadena
	#para monitorear todas las teclas
	print('{0} pressed'.format(key))
	
	
	#caso que se haya ingresado enter
	if key == Key.enter and process_id==0:
		userpassnr = '0000'   #codigo por defecto
		pass_row = [0,0,0]
		keypadcredit = float(0.0)
		print("se presionó enter")
		keypadcreditbuffer = keypadcreditbuffer.replace(",", ".")

		try:
			if float(keypadcreditbuffer) > 2.0:
				print("valor sospechosamente alto. se descarta. ")
				print("keypadcredit resulting value: " + str(keypadcredit))
				
			else:
				keypadcredit = float(keypadcreditbuffer)
				print("se convirtio el valor de teclado en float.")
				print("keypadcredit verified value: " + str(keypadcredit))
				
		except:   
				print("el nro del keypad no se logró convertir a soles")
				
		if keypadcreditbuffer[0:1] == "*":   #veamos si hay un código de iguapass
			print("se ingresó código iguapass nro: " + keypadcreditbuffer[1:5])
			print("buscando crédito ... ")
			
			try:
				userpassnr = keypadcreditbuffer[1:5]
				dummyint = int(userpassnr)
				print('userpassnr es: ' + userpassnr)
			except: 
				print("el código debe contener solo caracteres numericos")
					
			if userpassnr != '0000':
				print('pasó, hay un nro diferente de cero')
				try:
					sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1XzZeGav7xOc-Vvhuq6aCoox_dsWTQruLx04xkl_SBbg/edit?usp=drive_web&ouid=106328115973184488048')
					worksheet = sheet.get_worksheet(0)
					passcelda = worksheet.find(userpassnr) #Find a cell with exact string value
					# print('pass està en la celda: ' + str(passcelda))
					# print("Text found at R%sC%s" % (passcelda.row, passcelda.col))
					pass_row = worksheet.row_values(passcelda.row)
					print('exito! se encontró igua pass')
				except: 
					print('no fue posible obtener registro de iguapass')
					pass_row = [0]
		
			if pass_row != [0]:
				print(pass_row)
				if len(pass_row) <2:    #descartamos que la fila esté vacía
					print('cuenta sin suficientes datos. osea fila de excel vacía')
				else:
					pass_user = pass_row[0]
					pass_plantype = pass_row[1]
					pass_activeflag = pass_row[2]
					pass_activationdate = pass_row[3]
					if pass_activeflag == '0':
						pass_activeflag = 1
						pass_activationdate = datetime.now().timetuple().tm_yday
						try:
							worksheet.update_cell(passcelda.row, 4, pass_activationdate)
							print('se actualizó registro de fecha de activación')
						except:
							print('no se pudo completar registro de fecha de activación')
						
						try:
							worksheet.update_cell(passcelda.row, 3, '1')
							print('se actualizó registro de activeflag')
						except:
							print('no se pudo completar registro de activeflag')
						
					# pass_credits[7] = [pass_row[4], pass_row[5], pass_row[6], pass_row[7], pass_row[8], pass_row[9], pass_row[10]]
					
					pass_dia_N = datetime.now().timetuple().tm_yday - int(pass_activationdate)
					pass_credit_today = int(pass_row[(4 + pass_dia_N)])
					if pass_credit_today == 0:
						print('no hay credito disponible por hoy')
					else:
						print('se cargó crédito de hoy: ' + str(pass_credit_today))
						formadepago = 'pass'
						process_id = 3  
				
		keypadcreditbuffer = ""
	
	#caso que sea cualquier otra tecla, acumular cadena	
	elif process_id==0 and key == Key.backspace:
		keypadcreditbuffer = ""
		print("se borro la cadena, ahora solo queda un string vacio como este: " + keypadcreditbuffer)
	
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
		
	elif process_id==3 and (key == Key.backspace or key == Key.enter):
		print("se presiono backspace para cancelar tiempo de servida.")
		cancelrequest_timeout = 1		
	
	else:
		pass
   
def escribir_nuevo_saldo_para_pass():
	global passcelda
	global pass_dia_N
	global pass_credit_today
	global worksheet
	worksheet.update_cell(passcelda.row, (pass_dia_N + 5), pass_credit_today)
	'''
	try:
		worksheet.update_cell(passcelda.row, pass_dia_N, '')
		print('se actualizó saldo.')
	except:
		print('no se pudo actualizar saldo.')
	'''
		
def on_release(key):
    # print('{0} release'.format(key))
    # if key == Key.esc:
        # Stopstener
    #    return False
    sleep(0)
    
#fin para el keypad

#para gspread (google "spreadsheets"(?) api)
try: 
	import gspread
	from oauth2client.service_account import ServiceAccountCredentials
	scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
	credentials = ServiceAccountCredentials.from_json_keyfile_name('IGUA_DRIVE_SECRET.json', scope)
	gc = gspread.authorize(credentials)
	# wks = gc.open("Where is the money Lebowski?").sheet1
	sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1XzZeGav7xOc-Vvhuq6aCoox_dsWTQruLx04xkl_SBbg/edit?usp=drive_web&ouid=106328115973184488048')
	worksheet = sheet.get_worksheet(0)

except:
	logger.error('No fue posible importar librerìa *gspread*. probar con instalar: pip3 install gspread')

#importando funciones y librerias
from time import sleep
from time import strftime 
import time
import serial
import re
import socket
import threading

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

def send_to_carriots():  #send collected data to carriots
	global device
	global servidos_lt
	global solesacumulados
	global formadepago
	timestamp = int(mktime(datetime.utcnow().timetuple()))
	solesstring = str(format(solesacumulados*100, ".0f"))
	mlservidosstring = str(format(servidos_lt, ".0f"))
	#data = {"protocol": "v2", "device": device, "at": timestamp, "data": {"maquina": "IGUA_01", "colectado soles": solesstring, "servido litros": format(servidos_lt/1000, '.3f')}}
	data = {"protocol": "v2", "device": device, "at": timestamp, "data": {"maquina": "IGUA_02", "forma de pago": formadepago, "colectado centavos": solesstring, "servido mililitros": mlservidosstring}}
	print(data)
	if is_connected() == True:
		carriots_response = client_carriots.send(data)
		print('conexion ok!')
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

# declarar los puertos serialers en caso que se use máquina modo usb
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
		

# setup display
startdisplay()
		
		
#para lcd
def lcd_bienvenida_linear(now):
	if  now == 0:
		ser_lcd.write('mAs agua pura...   para Todos!!!'.encode())
	elif now == 1:
		ser_lcd.write('cuida tu salud..y la del planeta'.encode())
	elif now == 2:
		ser_lcd.write('juntos contra      el plAstico!!'.encode())
	elif now == 3:
		ser_lcd.write('f/aguaigua      http://igua.pe  '.encode())
	elif now == 4:
		ser_lcd.write('hola mundo!!!   hola igua!!!    '.encode())
	elif now == 5:
		ser_lcd.write('agua igua!!!           salud!   '.encode())
	
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
	ser_lcd.write(('tienes: S/ ' + str(format(solesacumulados, '.2f')) + '                 ').encode())
	return 1
	
def lcd_acumula_pwyw(solesacumulados):
	ser_lcd.write(('tu aporte: S/. ' + str(format(solesacumulados, '.2f')) + '             ').encode())	
		
def lcd_servidos_lt(servidos_lt,diff):
	global button
	button_state = GPIO.input(button)
	if button_state == GPIO.LOW:
		ser_lcd.write(('tienes: ' + str(format(servidos_lt/1000, '.3f')) + ' l  ' + '                ' ).encode())	
	if button_state == GPIO.HIGH:
		ser_lcd.write(('tienes: ' + str(format(servidos_lt/1000, '.3f')) + ' l  ' + '          ... ' + str(format(diff, '.0f')) + 's').encode())	
	
	
def lcd_ozonizando():
	ser_lcd.write('... ozonizando ...              '.encode())	
	
def lcd_cancelando():
	ser_lcd.write('..gracias! ...       #tomaigua !'.encode())	

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
precio = 0.5
formadepago = "keypad"

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
		now = int((now/4)%6)
		if now != now_1:
			if modo_maquina == 0:
				display_bienvenida_linear(now)
				lcd_bienvenida_linear(now)
			if modo_maquina == 1:
				display_bienvenida_pwyw(now)
				lcd_bienvenida_pwyw(now)  # cuidado CUIDADO!!!! no existe declaración!
				
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
			print('estamos listos!')

	
    #leer aceptador de monedas
		before = int(time.time())    #se necesita esto aqui?
		bytesToRead = ser_acc.inWaiting()
		if bytesToRead > 0:
			formadepago = "cash"
			now = int(time.time())   #se necesita esto aqui?
			process_id = 1
			
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
		bytesToRead = ser_acc.inWaiting()
		if bytesToRead > 0:
			sleep(0.5)
			bytesToRead = ser_acc.inWaiting()
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
		#print("diff vale:", cuenta_de_ciclos)


		#tap_button pressed?
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
			# print ("button is NOT PRESSED")	
		
	elif process_id == 2:	
		# enciende el pin de Ozono
		set_ozono(0)
		# muestra display "OZONIZANDO"
		# lcd_ozonizando()
		# espera N segs
		sleep(0)
		set_ozono(0)
		# apaga el pin de Ozono
		process_id = 3
	
	# habilitada vavula y muestra litros
	elif process_id == 3:
		set_accepting(1)
		ser_flw.write('a'.encode())
		sleep(0.1)
		read_flw()
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
			
			ser_flw.write('a'.encode())
			sleep(0.1)
			read_flw()

			# se podrìa borrar?   if secondcycle == 1:     #a partir de la segunda corrida, muestro la cuenta regresiva
			servidos_lt = float(int(string_flw)/10)*0.95
			display_servidos_lt((litros_servir - servidos_lt),30 - tiempo_desde_inicio_servida)
			lcd_servidos_lt((litros_servir - servidos_lt),30 - tiempo_desde_inicio_servida)
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
				lcd_agradece()
				if formadepago == "pass":
					print(' formadepago =es= pass ')
					pass_credit_today = 0
					print(' remaining credit: ' + pass_credit_today)
					escribir_nuevo_saldo_para_pass()
					pass_credit_today = 0
				process_id = 4
					
			if tiempo_desde_inicio_servida > 30:     #si se demora mucho en 0.0.2 re-servir		
				print ("se acabó el tiempo_desde_inicio_de_servida")
				set_valve(0)   #cerrando la valvula
				lcd_agradece()
				if formadepago == "pass":
					print(' formadepago =es= pass ')
					pass_credit_today = pass_credit_today - int(servidos_lt)
					print(' remaining credit: ' + str(pass_credit_today))
					escribir_nuevo_saldo_para_pass()
					pass_credit_today = 0            #una vez transferido el saldo a la db, borramos el credito local
				process_id = 4
				
			if cancelrequest_timeout == 1:
				print ("se cancelo el tiempo de espera (backspace)")
				set_valve(0)   #cerrando la valvula
				if formadepago == "pass":
					pass_credit_today = pass_credit_today - int(servidos_lt)
					escribir_nuevo_saldo_para_pass()
					pass_credit_today = 0
				cancelrequest_timeout = 0
				lcd_cancelando()
				sleep(0.1)
				lcd_cancelando()
				process_id = 4
				
				
					

	# deshabilita vavula y ozonizando
	elif process_id == 4:
		
		#registra la transacción en la nube
		send_to_carriots()
        
        #anexa al archivo en local
		timestamp = int(mktime(datetime.utcnow().timetuple()))
		fd = open('IGUA_DANNY_log.csv','a')
		# fd.write('timestamp: ' + str(timestamp) +', máquina: igua_bodega, volumen: ' + str(format(string_flw, '.3f')) + "\n")
		fd.write('timestamp: ' + str(timestamp) +', máquina: igua_bodegadanny, volumen: ' + str(format(servidos_lt, '.3f')) + "\n")
		fd.close()
        
        #resetea variables para nuevo ciclo
		keypadcredit = 0
		keypadcreditbuffer = ""
		
		#resetea el flujometro
		ser_flw.write('aasdfasdf'.encode())
		
		
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
	
	
