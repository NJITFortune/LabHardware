from pwmio import PWMOut
import board
import time
import digitalio
import random
import math

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

rPinky = PWMOut(pin=board.GP2, frequency=250, duty_cycle=0, variable_frequency=False)
rRing = PWMOut(pin=board.GP3, frequency=250, duty_cycle=0, variable_frequency=False)
rMiddle = PWMOut(pin=board.GP4, frequency=250, duty_cycle=0, variable_frequency=False)
rPoint = PWMOut(pin=board.GP5, frequency=250, duty_cycle=0, variable_frequency=False)

lPinky = PWMOut(pin=board.GP10, frequency=250, duty_cycle=0, variable_frequency=False)
lRing = PWMOut(pin=board.GP11, frequency=250, duty_cycle=0, variable_frequency=False)
lMiddle = PWMOut(pin=board.GP12, frequency=250, duty_cycle=0, variable_frequency=False)
lPoint = PWMOut(pin=board.GP13, frequency=250, duty_cycle=0, variable_frequency=False)
randPattern = int
nSeq = int
cnt = int

cnt = 0

while True:
    randPattern = random.randint(1, 16)  # There are 24 permutations of 1:4 sequences
    led.value = True
    nSeq = [32768, 0, 0, 0,  0, 32768, 0, 0,  0, 0, 32768, 0,  0, 0, 0, 32768]
    cnt = cnt + 1
    
    if randPattern == 1: 
        nSeq = [32768, 0, 0, 0,  0, 32768, 0, 0,  0, 0, 32768, 0,  0, 0, 0, 32768]
        print('randPattern 1234')
    if randPattern == 2: 
        nSeq = [0, 32768, 0, 0,  0, 0, 32768, 0,  0, 0, 0, 32768,  32768, 0, 0, 0]
        print('randPattern 2341')
    if randPattern == 3: 
        nSeq = [0, 0, 32768, 0,  0, 0, 0, 32768,  32768, 0, 0, 0,  0, 32768, 0, 0]
        print('randPattern 3412')
    if randPattern == 4: 
        nSeq = [0, 0, 0, 32768,  32768, 0, 0, 0,  0, 32768, 0, 0,  0, 0, 32768, 0]
        print('randPattern 4123')
        
    if randPattern == 5: 
        nSeq = [32768, 0, 0, 0,  0, 0, 32768, 0,  0, 32768, 0, 0,  0, 0, 0, 32768]
        print('randPattern 1324')
    if randPattern == 6: 
        nSeq = [0, 32768, 0, 0,  0, 0, 0, 32768,  0, 0, 32768, 0,  32768, 0, 0, 0]
        print('randPattern 2431')
    if randPattern == 7: 
        nSeq = [0, 0, 32768, 0,  32768, 0, 0, 0,  0, 0, 0, 32768,  0, 32768, 0, 0]
        print('randPattern 3142')
    if randPattern == 8: 
        nSeq = [0, 0, 0, 32768,  0, 32768, 0, 0,  32768, 0, 0, 0,  0, 0, 32768, 0]
        print('randPattern 4213')
        
    if randPattern == 9: 
        nSeq = [32768, 0, 0, 0,  0, 32768, 0, 0,  0, 0, 0, 32768,  0, 0, 32768, 0]
        print('randPattern 1243')
    if randPattern == 10: 
        nSeq = [0, 32768, 0, 0,  0, 0, 32768, 0,  32768, 0, 0, 0,  0, 0, 0, 32768]
        print('randPattern 2314')
    if randPattern == 11: 
        nSeq = [0, 0, 32768, 0,  0, 0, 0, 32768,  0, 32768, 0, 0,  32768, 0, 0, 0]
        print('randPattern 3421')
    if randPattern == 12: 
        nSeq = [0, 0, 0, 32768,  32768, 0, 0, 0,  0, 0, 32768, 0,  0, 32768, 0, 0]
        print('randPattern 4132')
        
    if randPattern == 13: 
        nSeq = [32768, 0, 0, 0,  0, 0, 0, 32768,  0, 0, 32768, 0,  0, 32768, 0, 0]
        print('randPattern 1432')
    if randPattern == 14: 
        nSeq = [0, 32768, 0, 0,  32768, 0, 0, 0,  0, 0, 0, 32768,  0, 0, 32768, 0]
        print('randPattern 2143')
    if randPattern == 15: 
        nSeq = [0, 0, 32768, 0,  0, 32768, 0, 0,  32768, 0, 0, 0,  0, 0, 0, 32768]
        print('randPattern 3214')
    if randPattern == 16: 
        nSeq = [0, 0, 0, 32768,  0, 0, 32768, 0,  0, 32768, 0, 0,  32768, 0, 0, 0]
        print('randPattern 4321')
        
    rPinky.duty_cycle = nSeq[0]
    lPinky.duty_cycle = nSeq[0]
    rRing.duty_cycle = nSeq[1]
    lRing.duty_cycle = nSeq[1]
    rMiddle.duty_cycle = nSeq[2]
    lMiddle.duty_cycle = nSeq[2]
    rPoint.duty_cycle = nSeq[3]
    lPoint.duty_cycle = nSeq[3]
    time.sleep(0.1)
    rPinky.duty_cycle = 0
    lPinky.duty_cycle = 0
    rRing.duty_cycle = 0
    lRing.duty_cycle = 0
    rMiddle.duty_cycle = 0
    lMiddle.duty_cycle = 0
    rPoint.duty_cycle = 0
    lPoint.duty_cycle = 0
    time.sleep(0.001 * random.randint(25, 75))
    rPinky.duty_cycle = nSeq[4]
    lPinky.duty_cycle = nSeq[4]
    rRing.duty_cycle = nSeq[5]
    lRing.duty_cycle = nSeq[5]
    rMiddle.duty_cycle = nSeq[6]
    lMiddle.duty_cycle = nSeq[6]
    rPoint.duty_cycle = nSeq[7]
    lPoint.duty_cycle = nSeq[7]
    time.sleep(0.1)
    rPinky.duty_cycle = 0
    lPinky.duty_cycle = 0
    rRing.duty_cycle = 0
    lRing.duty_cycle = 0
    rMiddle.duty_cycle = 0
    lMiddle.duty_cycle = 0
    rPoint.duty_cycle = 0
    lPoint.duty_cycle = 0
    time.sleep(0.001 * random.randint(25, 75))
    rPinky.duty_cycle = nSeq[8]
    lPinky.duty_cycle = nSeq[8]
    rRing.duty_cycle = nSeq[9]
    lRing.duty_cycle = nSeq[9]
    rMiddle.duty_cycle = nSeq[10]
    lMiddle.duty_cycle = nSeq[10]
    rPoint.duty_cycle = nSeq[11]
    lPoint.duty_cycle = nSeq[11]
    time.sleep(0.1)
    rPinky.duty_cycle = 0
    lPinky.duty_cycle = 0
    rRing.duty_cycle = 0
    lRing.duty_cycle = 0
    rMiddle.duty_cycle = 0
    lMiddle.duty_cycle = 0
    rPoint.duty_cycle = 0
    lPoint.duty_cycle = 0
    time.sleep(0.001 * random.randint(25, 75))
    rPinky.duty_cycle = nSeq[12]
    lPinky.duty_cycle = nSeq[12]
    rRing.duty_cycle = nSeq[13]
    lRing.duty_cycle = nSeq[13]
    rMiddle.duty_cycle = nSeq[14]
    lMiddle.duty_cycle = nSeq[14]
    rPoint.duty_cycle = nSeq[15]
    lPoint.duty_cycle = nSeq[15]
    time.sleep(0.1)
    rPinky.duty_cycle = 0
    lPinky.duty_cycle = 0
    rRing.duty_cycle = 0
    lRing.duty_cycle = 0
    rMiddle.duty_cycle = 0
    lMiddle.duty_cycle = 0
    rPoint.duty_cycle = 0
    lPoint.duty_cycle = 0
    led.value = False
    time.sleep(0.05)
    
    if cnt == 3:
        time.sleep(random.randint(1, 2))
        cnt = 0
    
