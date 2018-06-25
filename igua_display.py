#display variables 
import pygame, sys
from pygame.locals import *
# import datetime

img = pygame.image.load('/home/pi/igua-toolkit/igua1.bmp')
#variables del display

width = 1400
height = 768
fontsize = 64
fontsize2 = 48

def startdisplay():
	pygame.init()
	pygame.display.set_caption('IGUA')
	
	
def display_bienvenida_linear(now):
	whiteColor = pygame.Color(255,255,255)
	blackColor = pygame.Color(100,100,100)
	fontObj = pygame.font.Font('freesansbold.ttf',fontsize2)
	windowSurfaceObj = pygame.display.set_mode((width,height),1,16)
	pygame.draw.rect(windowSurfaceObj,blackColor,Rect(0,0,width,height))
	# pygame.display.update(pygame.Rect(0,0,width,height))
	# datetime.datetime.now()
	splash_message = "agua igua salud!"
	if  now == 0:
		splash_message = "mas agua pura para todos!"
	elif now == 1:
		splash_message = "cuida tu salud y la del planeta!"
	elif now == 2:
		splash_message = "juntos contra el plastico"	
	elif now == 3:
		splash_message = "f/aguaigua  http://igua.pe"
	elif now == 4:
		splash_message = "hola mundo! hola igua!"	
	elif now == 5:
		splash_message = "agua igua! salud! "
		
	msgSurfaceObj = fontObj.render(splash_message, False,whiteColor)
	msgRectobj = msgSurfaceObj.get_rect()   
	msgRectobj.topleft=(80,80)
	windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
	windowSurfaceObj.blit(img,(200,800))                         #nuevo
	pygame.display.update(pygame.Rect(0,0,width,height))

def display_bienvenida_pwyw(now):
	whiteColor = pygame.Color(255,255,255)
	blackColor = pygame.Color(100,100,100)
	fontObj = pygame.font.Font('freesansbold.ttf',fontsize2)
	windowSurfaceObj = pygame.display.set_mode((width,height),1,16)
	pygame.draw.rect(windowSurfaceObj,blackColor,Rect(0,0,width,height))
	# pygame.display.update(pygame.Rect(0,0,width,height))
 	# datetime.datetime.now()
	if  now == 0:
		splash_message = "agua pura!"
		# ser3.write('hola igua!!!!      hola igua!!!    '.encode())
	elif now == 1:
		splash_message = "heladita!"
		# ser3.write('chauuuuuuu!!!      hola igua!!!    '.encode())
	elif now == 2:
		splash_message = "llévala!"	
	elif now == 3:
		splash_message = "... aporta 'tu voluntad'"
	elif now == 4:
		splash_message = "... sirvete hasta un litro! "	
	elif now == 5:
		splash_message = "... y conserva tu botella! "
		
	msgSurfaceObj = fontObj.render(splash_message, False,whiteColor)
	msgRectobj = msgSurfaceObj.get_rect()   
	msgRectobj.topleft=(80,80)
	windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
	# windowSurfaceObj.blit(img,(200,800))                         #nuevo
	pygame.display.update(pygame.Rect(0,0,width,height))
		
def display_acumula_linear(solesacumulados):
	whiteColor = pygame.Color(255,255,255)
	blackColor = pygame.Color(100,100,100)
	fontObj = pygame.font.Font('freesansbold.ttf',fontsize)
	fontObj2 = pygame.font.Font('freesansbold.ttf',fontsize2)
	windowSurfaceObj = pygame.display.set_mode((width,height),1,16)
	pygame.draw.rect(windowSurfaceObj,blackColor,Rect(0,0,width,height))
	pygame.display.update(pygame.Rect(0,0,width,height))
	# print(solesacumulados)
	msgSurfaceObj = fontObj.render('tu saldo: S/. ' + format(solesacumulados, '.2f'), False,whiteColor)
	msgSurfaceObj2 = fontObj2.render('deposita o sirvete ' + format(solesacumulados / 0.5, '.2f') + ' litros.', False,whiteColor)
	msgRectobj = msgSurfaceObj.get_rect()   
	msgRectobj2 = msgSurfaceObj.get_rect()
	msgRectobj.topleft=(80,80)
	msgRectobj2.topleft=(80,280)                                                                                                                                             
	windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
	windowSurfaceObj.blit(msgSurfaceObj2, msgRectobj2)   
	windowSurfaceObj.blit(img,(600,80))                         #nuevo
	# pygame.display.flip()                              #nuevo
	pygame.display.update(pygame.Rect(0,0,width,height))

def display_acumula_pwyw(solesacumulados):
	whiteColor = pygame.Color(255,255,255)
	blackColor = pygame.Color(100,100,100)
	fontObj = pygame.font.Font('freesansbold.ttf',fontsize)
	fontObj2 = pygame.font.Font('freesansbold.ttf',fontsize2)
	windowSurfaceObj = pygame.display.set_mode((width,height),1,16)
	pygame.draw.rect(windowSurfaceObj,blackColor,Rect(0,0,width,height))
	pygame.display.update(pygame.Rect(0,0,width,height))
	# print(solesacumulados)
	msgSurfaceObj = fontObj.render('tu aporte: S/. ' + format(solesacumulados, '.2f'), False,whiteColor)
	msgSurfaceObj2 = fontObj2.render('deposita mas o sirvete! ', False,whiteColor)
	msgRectobj = msgSurfaceObj.get_rect()   
	msgRectobj2 = msgSurfaceObj.get_rect()
	msgRectobj.topleft=(80,80)
	msgRectobj2.topleft=(80,280)                                                                                                                                             
	windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
	windowSurfaceObj.blit(msgSurfaceObj2, msgRectobj2)   
	windowSurfaceObj.blit(img,(600,80))                         #nuevo
	# pygame.display.flip()                              #nuevo
	pygame.display.update(pygame.Rect(0,0,width,height))
		
def display_servidos_lt(servidos_lt,diff):
	whiteColor = pygame.Color(255,255,255)
	blackColor = pygame.Color(100,100,100)
	fontObj = pygame.font.Font('freesansbold.ttf',fontsize)
	fontObj2 = pygame.font.Font('freesansbold.ttf',fontsize2)
	windowSurfaceObj = pygame.display.set_mode((width,height),1,16)
	pygame.draw.rect(windowSurfaceObj,blackColor,Rect(0,0,width,height))
	pygame.display.update(pygame.Rect(0,0,width,height))
	# print(solesacumulados)
	msgSurfaceObj = fontObj.render('te quedan: ' + format(servidos_lt/1000, '.3f') + ' litros!', False,whiteColor)
	# msgSurfaceObj = fontObj.render('hemos servido:', False,whiteColor)
	msgSurfaceObj2 = fontObj2.render('aun tienes: ' + format(diff) + ' segs. ', False,whiteColor)
	# msgSurfaceObj2 = fontObj2.render(format(servidos_lt/1000, '.3f') + ' litros!', False, whiteColor)
	msgRectobj = msgSurfaceObj.get_rect()   
	msgRectobj2 = msgSurfaceObj.get_rect()
	msgRectobj.topleft=(80,80)
	msgRectobj2.topleft=(80,280)                                                                                                                                             
	windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
	windowSurfaceObj.blit(msgSurfaceObj2, msgRectobj2)   
	windowSurfaceObj.blit(img,(600,80))                         #nuevo
	# pygame.display.flip()                              #nuevo
	pygame.display.update(pygame.Rect(0,0,width,height))
	# presione el boton para servirse
	
def display_agradece():
	whiteColor = pygame.Color(255,255,255)
	blackColor = pygame.Color(100,100,100)
	fontObj = pygame.font.Font('freesansbold.ttf',fontsize)
	fontObj2 = pygame.font.Font('freesansbold.ttf',fontsize2)
	windowSurfaceObj = pygame.display.set_mode((width,height),1,16)
	pygame.draw.rect(windowSurfaceObj,blackColor,Rect(0,0,width,height))
	pygame.display.update(pygame.Rect(0,0,width,height))
	# print(solesacumulados)
	msgSurfaceObj = fontObj.render('gracias!', False,whiteColor)
	msgSurfaceObj2 = fontObj2.render('f/ aguaigua', False,whiteColor)
	msgRectobj = msgSurfaceObj.get_rect()   
	msgRectobj2 = msgSurfaceObj.get_rect()
	msgRectobj.topleft=(80,80)
	msgRectobj2.topleft=(80,280)                                                                                                                                             
	windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
	windowSurfaceObj.blit(msgSurfaceObj2, msgRectobj2)   
	windowSurfaceObj.blit(img,(600,80))                         #nuevo
	pygame.display.flip()                              #nuevo
	pygame.display.update(pygame.Rect(0,0,width,height))
		

# version antigua de @cowdfunding@   (as seen at fiiS)
	
def refreshdisplay(solesacumulados):    
	whiteColor = pygame.Color(255,255,255)
	blackColor = pygame.Color(100,100,100)
	fontObj = pygame.font.Font('freesansbold.ttf',fontsize)
	fontObj2 = pygame.font.Font('freesansbold.ttf',fontsize2)
	windowSurfaceObj = pygame.display.set_mode((width,height),1,16)
#	pygame.draw.rect(windowSurfaceObj,blackColor,Rect(0,0,width,height))
	pygame.display.update(pygame.Rect(0,0,width,height))
#	print(solesacumulados)
	msgSurfaceObj = fontObj.render('S/. ' + format(solesacumulados, '.2f'), False,)
	msgSurfaceObj2 = fontObj2.render('vamos sumando...! ', False,redColor)
	msgRectobj = msgSurfaceObj.get_rect()   
	msgRectobj2 = msgSurfaceObj.get_rect()
	msgRectobj.topleft=(80,80)
	msgRectobj2.topleft=(80,280)                                                                                                                                             
	windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
	windowSurfaceObj.blit(msgSurfaceObj2, msgRectobj2)   
	windowSurfaceObj.blit(img,(200,800))                         #nuevo
	pygame.display.flip()                              #nuevo
	pygame.display.update(pygame.Rect(0,0,width,height))
