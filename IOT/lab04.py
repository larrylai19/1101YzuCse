import RPi.GPIO as GPIO
import time
import serial

ser = serial.Serial('/dev/ttyAMA1', baudrate=9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS
)

GPIO.setmode(GPIO.BOARD)

LED_PIN = 12
GPIO.setup(LED_PIN, GPIO.OUT)

BUZZ_PIN = 16
# pitches = [262, 294, 330, 349, 392, 440, 493]
pitches = {
    'c': 262,
    'd': 294,
    'e': 330,
    'f': 349,
    'g': 392,
    'a': 440,
    'b': 493
}

GPIO.setup(BUZZ_PIN, GPIO.OUT)

pwm = GPIO.PWM(BUZZ_PIN, 262)
pwm.start(0)

pwm2 = GPIO.PWM(LED_PIN, 100)
pwm2.start(0)

bright = 50

try:
    pwm.ChangeDutyCycle(bright)

    while True:
        data = ser.readline()
        print(data.decode("utf-8").strip())
        ser.write(data)
        ser.flushInput()
        data = data.decode("utf-8").strip()
        print(len(data.strip()))

        if 'set' in data:
            # print(data.split(' '))
            bright = int(data.split(' ')[1])
            pwm2.ChangeDutyCycle(bright)
        
        if 'play' in data:
            l = data.split(',')
            for s in l:
                if len(s) > 1:
                    pwm.ChangeDutyCycle(50)
                    pwm.ChangeFrequency(pitches[s[-1]])
                    print(pitches[s[-1]])
                else:
                    pwm.ChangeDutyCycle(50)
                    pwm.ChangeFrequency(pitches[s])
                    print(pitches[s])
                time.sleep(2)

except KeyboardInterrupt:
    pass

finally:
    ser.close()
    pwm.stop()
    GPIO.cleanup()
