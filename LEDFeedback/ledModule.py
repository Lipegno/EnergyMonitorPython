import mraa
import threading, time
from PublishSubscriber.Subscriber import Subscriber

class LedController(Subscriber):

    def __init__(self, pinRed, pinBlue, pinGreen):
        self.pwmRed = mraa.Pwm(pinRed)
        self.pwmGreen = mraa.Pwm(pinGreen)
        self.pwmBlue = mraa.Pwm(pinBlue)
        #Enables the pin's
        self.pwmRed.enable(True)
        self.pwmGreen.enable(True)
        self.pwmBlue.enable(True)
        #self.processedSamplesQueue = processedSamplesQueue
        #self.processedSamplesQueueLock = processedSamplesQueueLock
        # STATE CONSTANTS
        self.CONST_STATE_GREEN = "green"
        self.CONST_STATE_YELLOW = "yellow"
        self.CONST_STATE_RED = "red"
        #Leds State
        self.currentState = self.CONST_STATE_GREEN
        self.pastState = self.CONST_STATE_GREEN
        #The color min value
        self.CONST_GRADIENT = 0.10
        #Starts with the led in green
        self.pinRed = 0.0000
        self.pinBlue = 0.0000
        self.pinGreen = 0.0000
        """self.led(self.pinGreen,self.pinRed)
        """#Data that is receive by the thread
        self.powerBuffer = []
        self.ledSemaphoreController = threading.Semaphore(value=0) # This will controll the led reads on the list that has the current values

    def led(self,valueGreen, valueRed):
        """
        Led color change
        :param valueGreen:
        :param valueRed:
        :return:
        """
        self.pwmGreen.write(valueGreen)
        self.pwmRed.write(valueRed)

    def changeState(self, power):
        """
        Will make the current state var according with the power received.
        :param power:
        :return:
        """
        self.power = power

        previousState = self.currentState
        self.pastState = self.currentState
        if self.power >= 1000:
            self.currentState = self.CONST_STATE_RED
        elif self.power > 300 and self.power < 1000:
            self.currentState = self.CONST_STATE_YELLOW
        else:
            self.currentState = self.CONST_STATE_GREEN


    def colorChange(self):
        if self.currentState == self.CONST_STATE_RED:
            if self.pastState == self.CONST_STATE_RED:
                self.led(0.0000,1.0000)
                self.pinRed = 1.0000
                self.pinGreen = 0.0000
            elif self.pastState == self.CONST_STATE_YELLOW:
                while self.pinGreen > 0.0000 and self.pinRed < 1.0000:
                    self.pinGreen = self.pinGreen + self.CONST_GRADIENT
                    self.led(self.pinGreen, 1.0000)
                    time.sleep(0.1)
                self.pastState = self.CONST_STATE_RED
            else:
                while self.pinGreen > 0.0000 and self.pinRed < 1.0000:
                    self.pinRed = self.pinRed + self.CONST_GRADIENT
                    self.pinGreen = self.pinGreen - self.CONST_GRADIENT
                    self.led(self.pinGreen, self.pinRed)
                    time.sleep(0.1)
                self.pastState = self.CONST_STATE_RED


        if self.currentState == self.CONST_STATE_YELLOW:
            if self.pastState == self.CONST_STATE_YELLOW:
                self.led(1.0000,1.0000)
                self.pinRed = 1.0000
                self.pinGreen = 1.0000
            elif self.pastState == self.CONST_STATE_RED:
                while self.pinGreen < 1.0000:
                    self.pinGreen = self.pinGreen + self.CONST_GRADIENT
                    self.led(self.pinGreen, 1.0000)
                    time.sleep(0.1)
                self.pastState = self.CONST_STATE_YELLOW
            else :
                while self.pinRed < 1.0000:
                    self.pinRed = self.pinRed + self.CONST_GRADIENT
                    self.led(1.0000, self.pinRed)
                    time.sleep(0.1)
                self.pastState = self.CONST_STATE_YELLOW
        
        if self.currentState == self.CONST_STATE_GREEN:
            if self.pastState == self.CONST_STATE_GREEN:
                self.led(1.0000,0.0000) #TODO PROBABLY NEED TO TI CHANFE THE GREEN VALUE AN NOT CHANGE IT SO NEED TO READ FROM THE PIN
                self.pinRed = 0.0000
                self.pinGreen = 1.0000
            elif self.pastState == self.CONST_STATE_RED:
                while self.pinGreen < 1.0000 and self.pinRed > 0.0000:
                    self.pinRed = self.pinRed - self.CONST_GRADIENT
                    self.pinGreen = self.pinGreen + self.CONST_GRADIENT
                    self.led(self.pinGreen,self.pinRed)
                    time.sleep(0.1)
                self.pastState = self.CONST_STATE_GREEN
            else:
                while self.pinGreen < 1.0000 and self.pinRed > 0.0000:
                    self.pinRed = self.pinRed - self.CONST_GRADIENT
                    self.led(1.0000,self.pinRed)
                    time.sleep(0.1)
                self.pastState = self.CONST_STATE_GREEN

    def update(self,data):
        print("LED receive power")
        # self.powerBuffer.append(data['power'])
        # self.ledSemaphoreController.release()
        #print("Subscriber LED " + ))
        self.changeState(data['power'])
        self.colorChange()

"""
if __name__ == "__main__":
    ledContoller = LedController(20,14,21)

    while True:
        power = 0
        while power <= 4400:
            if ledContoller.currentState == ledContoller.CONST_NO_STATE:
                ledContoller.greenLedTransition()
                ledContoller.currentState = ledContoller.CONST_STATE_GREEN
"""
