from machine import Pin
from utime import sleep

onBoard = Pin("LED", Pin.OUT)
led1 = Pin(8, Pin.OUT)
led2 = Pin(18, Pin.OUT)

while True:
    try:
        onBoard.toggle()
        led1.toggle()
        led2.toggle()
        sleep(1) 
    except KeyboardInterrupt:
        break
        sleep(1)
    except KeyboardInterrupt:
        break

onBoard.off()
led1.off()
led2.off()
print("Finished.")