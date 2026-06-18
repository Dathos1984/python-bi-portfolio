import pyautogui
import time
import sys

print("El programa comenzará en 5 segundos😈")
time.sleep(5)
try: 
    while True:
       x_inicial, y_inicial = pyautogui.position()
       nueva_x = x_inicial + 50
       nueva_y = y_inicial
       pyautogui.moveTo(nueva_x, nueva_y, duration=0.2)
       nueva_x = x_inicial
       pyautogui.moveTo(nueva_x, nueva_y, duration=0.2)
       time.sleep(1)
       x_actual, y_actual = pyautogui.position()
       time.sleep(1)
       pyautogui.click()
       if (x_actual, y_actual) != (nueva_x, nueva_y):
            print("¡Movimiento detectado! Deteniendo el programa.")
            break
except KeyboardInterrupt:
    print("Programa detenido por el usuario.")
    sys.exit() 