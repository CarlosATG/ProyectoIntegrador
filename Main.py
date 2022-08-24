tot_cnt += 1 # Contabilizamos los mililitros

#Definimos el modo de uso de los puertos de la Raspberry 
GPIO.setmode(GPIO.BCM)
Flujo = 13 # Definir el puerto de data donde se conectara el sensor de flujo
#La salidas de los LEDs
rojo = 8
amarillo = 7
verde = 6
GPIO.setup(rojo, GPIO.OUT)
GPIO.setup(amarillo, GPIO.OUT)
GPIO.setup(verde, GPIO.OUT)
GPIO.setup(Flujo, GPIO.IN) # Estabelcemos en modo IN el puerto del sensor de flujo

#Variables globales, es necesario hacer esto para todas las funciones puedan utilizar los datos
global rate_cnt, tot_cnt, TotMil, MilperM, tiempo, inicio,check
rate_cnt = 0
tot_cnt = 0
GPIO.add_event_detect(inpt, GPIO.FALLING, callback=Pulse_cnt)
#Función prinicpal
def flujo():
    inicio = 0
    check = 1
    constant = 0.00210 #para calibrar el sensor
    litros = round(tot_cnt * constant, 5) 
    auxct = 0
    while litros > 0:  # Espera a que haya flujo de agua para comenzar a contar el tiempo
        auxTime = 0
        TotMil = round((tot_cnt * constant) , 5) * 0.1 # Contabiliza los litros por cada ciclo realizado para obtener un total
        GPIO.output( verde , GPIO.HIGH )
        if(TotMil > 0.1 and TotMil < 0.4):
          GPIO.output( verde , GPIO.LOW )
          GPIO.output( amarillo , GPIO.HIGH )
        elif(TotMil>0.4):
          GPIO.output( amarillo , GPIO.LOW )
          GPIO.output( rojo , GPIO.HIGH )
        if(check - TotMil == 0): #Si la cantidad de agua durante el ciclo pasado y el actual es igual, significa que ya se apagó al regadera
            GPIO.output( rojo , GPIO.LOW )
            GPIO.cleanup() # Cerramos y limpiamos los pines que usamos de la raspberry
        time.sleep(0.99)#para no estar capurando miles de valores por segundo
        check = TotMil # Igualamos una variable auxiliar a los litro al final del ciclo y volvemos a empezar
    return 3
  
  Verificar = flujo()
  print(Verificar)
