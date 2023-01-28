import conexionRed
from utelegram import Bot
from machine import Pin, PWM
from time import sleep
import time
#import _thread

TOKEN = '5746612826:AAE38gqigZyRKqZs1ZDtDw-mYjUBKKl_PkA'
bot = Bot(TOKEN)
relay1 = Pin(16, Pin.OUT, value=1)
relay2 = Pin(19, Pin.OUT, value=1)
servo = PWM(Pin(25), freq=50)
pir = Pin(15, Pin.IN)
# Simular relay
led1 = Pin(22, Pin.OUT)
# Simular relay
led2 = Pin(23, Pin.OUT)

def map(x):
    return int((x - 0) * (8328-2178) / (180 - 0) + 2178)
    
#_thread.start_new_thread(, ())

# Configuracion de BOT
@bot.add_message_handler('Menu')
def help(update):
    update.reply('''Menu Principal
                    Seleccione la opcion:
                    Estado de todos los dispositivos: 0
                    Menu Luces: 1
                    Menu Otros Dispositivos: 2
                    Menu Ventanas: 3
                    Otras Funciones: 4''')
        
@bot.add_message_handler("0")
def value(update):
    update.reply('Estado de los dispositivos:')
    if relay1.value():
        update.reply('Luz sala apagada')
    else:
        update.reply('Luz sala encendida')
    if relay2.value():
        update.reply('Luz habitacion apagada')
    else:
        update.reply('Luz habitacion encendida')
    if led1.value(0):
        update.reply('Luz lampara 1 apagada')
    else:
        update.reply('Luz lampara 1 encendida')
    if led2.value(0):
        update.reply('Luz lampara 2 apagada')
    else:
        update.reply('Luz lampara 2 encendida')

@bot.add_message_handler('1')
def help(update):
    update.reply('''Menu Luces
                    Encender Luz Sala: S1
                    Apagar Luz Sala: S2
                    
                    Encender Luz Habitacion: H1
                    Apagar Luz Habitacion: H2''')
    
@bot.add_message_handler('S1')
def help(update):
    update.reply('Luz Sala Encendida:')
    relay1.value(0)
        
@bot.add_message_handler('S2')
def help(update):
    update.reply('Luz Sala Apagada:')
    relay1.value(1)
    
@bot.add_message_handler('H1')
def help(update):
    update.reply('Luz Habitacion Encendida:')
    relay2.value(0)
        
@bot.add_message_handler('H2')
def help(update):
    update.reply('Luz Habitacion Apagada:')
    relay2.value(1)
            
@bot.add_message_handler('2')
def help(update):
    update.reply('''Menu Otros Dispositivos:
                    Encender Lampara 1 Hab: Lh1
                    Apagar Lampara 1 Hab: Lh2
                    
                    Encender Lampara 2 Hab: Lh3
                    Apagar Lampara 2 Hab: Lh4''')
    
@bot.add_message_handler('Lh1')
def help(update):
    led1.value(1)
    update.reply('Lampara 1 Hab Encendida:')
        
@bot.add_message_handler('Lh2')
def help(update):
    led1.value(0)
    update.reply('Lampara 1 Hab Apagada:')
    
@bot.add_message_handler('Lh3')
def help(update):
    led2.value(1)
    update.reply('Lampara 2 Hab Encendida:')
        
@bot.add_message_handler('Lh4')
def help(update):
    led2.value(0)
    update.reply('Lampara 2 Hab Apagada:')
    
@bot.add_message_handler('3')
def help(update):
    update.reply('''Menu Ventanas
                    Abrir Ventana Hab: V1
                    Cerrar Ventana Hab: V2''')
   
@bot.add_message_handler('V1')
def servoopen(update):
    update.reply('Ventana Habitacion Abierta')
    m = map(90)
    servo.duty_u16(m)
    
@bot.add_message_handler('V2')
def servoclose(update):
    update.reply('Ventana Habitacion Cerrada')
    m = map(0)
    servo.duty_u16(m)
    
@bot.add_message_handler('4')
def help(update):
    update.reply('''Funciones Adicionales
                    Apagar luz de la sala si no hay nadie: F1
                    Apagar todo: F2
                    Encender todo: F3''')
    
@bot.add_message_handler('F1')
def senmov(update):
    estado = pir.value()
    if estado == 0:
        update.reply('No hay nadie, se apagara la luz')
        relay1.value(1)
    else:
        update.reply('Hay movimiento en la sala, no se apagara la luz')
        
@bot.add_message_handler('F2')
def todooff(update):
    relay1.value(1)
    relay2.value(1)
    led1.value(0)
    led2.value(0)
    update.reply('Todos los dispositvos fueron apagados')
    
@bot.add_message_handler('F3')
def todoon(update):
    relay1.value(0)
    relay2.value(0)
    led1.value(1)
    led2.value(1)
    update.reply('Todos los dispositivos fueron encendidos')
    
bot.start_loop()

# Iniciar codigo principal
def do_main():
    conexionRed.conectaWifi()

if __name__ == "__main__":
    do_main()