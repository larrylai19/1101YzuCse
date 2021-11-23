import RPi.GPIO as GPIO
import time

l = [2, 1, 0.5]
idx = 0

def clicked(btn):
    global idx
    idx += 1
    if idx > 2:
        idx = 0
    print(f'State change, sleep {l[idx]} s.')

GPIO.setmode(GPIO.BOARD)

BTN_PIN = 13
LED_PIN = 15

GPIO.setup(BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.add_event_detect(BTN_PIN, GPIO.FALLING, clicked, 200)

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(l[idx])
except KeyboardInterrupt:
    print("Exception: KeyboardInterrupt")
finally:
    GPIO.cleanup()
