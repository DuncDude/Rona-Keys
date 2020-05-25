#Martin O'Hanlon
#www.stuffaboutcode.com
#A class for reading values from an xbox controller
# uses xboxdrv and pygame
# xboxdrv should already be running


#https://pynput.readthedocs.io/en/latest/keyboard.html
#even more fuckery!------------------------------------------------------------------------------
import socket
import time
import pickle






import pygame
from pygame.locals import *
import os, sys
import threading
import time
from pynput.keyboard import Key, Controller
keyboard = Controller()

"""
NOTES - pygame events and values

JOYAXISMOTION
event.axis              event.value
0 - x axis left thumb   (+1 is right, -1 is left)
1 - y axis left thumb   (+1 is down, -1 is up)
2 - x axis right thumb  (+1 is right, -1 is left)
3 - y axis right thumb  (+1 is down, -1 is up)
4 - right trigger
5 - left trigger

JOYBUTTONDOWN | JOYBUTTONUP
event.button
A = 0
B = 1
X = 2
Y = 3
LB = 4
RB = 5
BACK = 6
START = 7
XBOX = 8
LEFTTHUMB = 9
RIGHTTHUMB = 10

JOYHATMOTION
event.value
[0] - horizontal
[1] - vertival
[0].0 - middle
[0].-1 - left
[0].+1 - right
[1].0 - middle
[1].-1 - bottom
[1].+1 - top

"""

#Pause Function
def Pause():
	pase = raw_input("Press Enter.. ")
	return
#OTHER FUCKERY HERE TOO -----------------------------------------------------------------------------------------------------------------------------------


def Banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("__________                                ____  __.                   ")
    print("\______   \ ____   ____ _____            |    |/ _|____ ___.__. ______")
    print(" |       _//  _ \ /    \\__  \    ______ |      <_/ __ <   |  |/  ___/")
    print(" |    |   (  <_> )   |  \/ __ \_ /_____/ |    |  \  ___/\___  |\___ \ ")
    print(" |____|_  /\____/|___|  (____  /         |____|__ \___  > ____/____  >")
    print("        \/            \/     \/                  \/   \/\/         \/ ")
    print("CLIENT")
    print("------------------------------------------------------------------------")
    return
	
Banner()	
print("SUP Bitch MAKE SHO YOUR USB CONTROLLER IS PLUGGEDD IN  !")
Pause()
def receive(socket, signal):
    while signal:
        try:
            data = socket.recv(32)
            print(str(data.decode("utf-8")))
        except:
            print("You have been disconnected from the server")
            signal = False
            break

#Get host and port
#host = 'localhost'
host = 'localhost'
new = raw_input("Enter this box's IP, if hosting both client and server on same computer leave blank for local host: ")
if new:
    host = new
port = int(input("Port: "))
#Attempt connection to server
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
except:
    print("Could not make a connection to the server")
    input("Press enter to quit")
    sys.exit(0)

#Create new thread to wait for data
receiveThread = threading.Thread(target = receive, args = (sock, True))
receiveThread.start()











#Main class for reading the xbox controller values
class XboxController(threading.Thread):

    #internal ids for the xbox controls
    class XboxControls():
        LTHUMBX = 0
        LTHUMBY = 1
        RTHUMBX = 2
        RTHUMBY = 3
        RTRIGGER = 4
        LTRIGGER = 5
        A = 6
        B = 7
        X = 8
        Y = 9
        LB = 10
        RB = 11
        BACK = 12
        START = 13
        XBOX = 14
        LEFTTHUMB = 15
        RIGHTTHUMB = 16
        DPAD = 17

    #pygame axis constants for the analogue controls of the xbox controller
    class PyGameAxis():
        LTHUMBX = 0
        LTHUMBY = 1
        RTHUMBX = 2
        RTHUMBY = 3
        RTRIGGER = 4
        LTRIGGER = 5

    #pygame constants for the buttons of the xbox controller
    class PyGameButtons():
        A = 0
        B = 1
        X = 2
        Y = 3
        LB = 4
        RB = 5
        BACK = 6
        START = 7
        XBOX = 8
        LEFTTHUMB = 9
        RIGHTTHUMB = 10

    #map between pygame axis (analogue stick) ids and xbox control ids
    AXISCONTROLMAP = {PyGameAxis.LTHUMBX: XboxControls.LTHUMBX,
                      PyGameAxis.LTHUMBY: XboxControls.LTHUMBY,
                      PyGameAxis.RTHUMBX: XboxControls.RTHUMBX,
                      PyGameAxis.RTHUMBY: XboxControls.RTHUMBY}
    
    #map between pygame axis (trigger) ids and xbox control ids
    TRIGGERCONTROLMAP = {PyGameAxis.RTRIGGER: XboxControls.RTRIGGER,
                         PyGameAxis.LTRIGGER: XboxControls.LTRIGGER}

    #map between pygame buttons ids and xbox contorl ids
    BUTTONCONTROLMAP = {PyGameButtons.A: XboxControls.A,
                        PyGameButtons.B: XboxControls.B,
                        PyGameButtons.X: XboxControls.X,
                        PyGameButtons.Y: XboxControls.Y,
                        PyGameButtons.LB: XboxControls.LB,
                        PyGameButtons.RB: XboxControls.RB,
                        PyGameButtons.BACK: XboxControls.BACK,
                        PyGameButtons.START: XboxControls.START,
                        PyGameButtons.XBOX: XboxControls.XBOX,
                        PyGameButtons.LEFTTHUMB: XboxControls.LEFTTHUMB,
                        PyGameButtons.RIGHTTHUMB: XboxControls.RIGHTTHUMB}
                        
    #setup xbox controller class
    def __init__(self,
                 controllerCallBack = None,
                 joystickNo = 0,
                 deadzone = 0.1,
                 scale = 1,
                 invertYAxis = False):

        #setup threading
        threading.Thread.__init__(self)
        
        #persist values
        self.running = False
        self.controllerCallBack = controllerCallBack
        self.joystickNo = joystickNo
        self.lowerDeadzone = deadzone * -1
        self.upperDeadzone = deadzone
        self.scale = scale
        self.invertYAxis = invertYAxis
        self.controlCallbacks = {}

        #setup controller properties
        self.controlValues = {self.XboxControls.LTHUMBX:0,
                              self.XboxControls.LTHUMBY:0,
                              self.XboxControls.RTHUMBX:0,
                              self.XboxControls.RTHUMBY:0,
                              self.XboxControls.RTRIGGER:0,
                              self.XboxControls.LTRIGGER:0,
                              self.XboxControls.A:0,
                              self.XboxControls.B:0,
                              self.XboxControls.X:0,
                              self.XboxControls.Y:0,
                              self.XboxControls.LB:0,
                              self.XboxControls.RB:0,
                              self.XboxControls.BACK:0,
                              self.XboxControls.START:0,
                              self.XboxControls.XBOX:0,
                              self.XboxControls.LEFTTHUMB:0,
                              self.XboxControls.RIGHTTHUMB:0,
                              self.XboxControls.DPAD:(0,0)}

        #setup pygame
        self._setupPygame(joystickNo)

    #Create controller properties
    @property
    def LTHUMBX(self):
        return self.controlValues[self.XboxControls.LTHUMBX]

    @property
    def LTHUMBY(self):
        return self.controlValues[self.XboxControls.LTHUMBY]

    @property
    def RTHUMBX(self):
        return self.controlValues[self.XboxControls.RTHUMBX]

    @property
    def RTHUMBY(self):
        return self.controlValues[self.XboxControls.RTHUMBY]

    @property
    def RTRIGGER(self):
        return self.controlValues[self.XboxControls.RTRIGGER]

    @property
    def LTRIGGER(self):
        return self.controlValues[self.XboxControls.LTRIGGER]

    @property
    def A(self):
        return self.controlValues[self.XboxControls.A]

    @property
    def B(self):
        return self.controlValues[self.XboxControls.B]

    @property
    def X(self):
        return self.controlValues[self.XboxControls.X]

    @property
    def Y(self):
        return self.controlValues[self.XboxControls.Y]

    @property
    def LB(self):
        return self.controlValues[self.XboxControls.LB]

    @property
    def RB(self):
        return self.controlValues[self.XboxControls.RB]

    @property
    def BACK(self):
        return self.controlValues[self.XboxControls.BACK]

    @property
    def START(self):
        return self.controlValues[self.XboxControls.START]

    @property
    def XBOX(self):
        return self.controlValues[self.XboxControls.XBOX]

    @property
    def LEFTTHUMB(self):
        return self.controlValues[self.XboxControls.LEFTTHUMB]

    @property
    def RIGHTTHUMB(self):
        return self.controlValues[self.XboxControls.RIGHTTHUMB]

    @property
    def DPAD(self):
        return self.controlValues[self.XboxControls.DPAD]

    #setup pygame
    def _setupPygame(self, joystickNo):
        # set SDL to use the dummy NULL video driver, so it doesn't need a windowing system.
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        # init pygame
        pygame.init()
        # create a 1x1 pixel screen, its not used so it doesnt matter
        screen = pygame.display.set_mode((1, 1))
        # init the joystick control
        pygame.joystick.init()
        # how many joysticks are there
        #print pygame.joystick.get_count()
        # get the first joystick
        joy = pygame.joystick.Joystick(joystickNo)
        # init that joystick
        joy.init()

    #called by the thread
    def run(self):
        self._start()

    #start the controller
    def _start(self):
        
        self.running = True
        
        #run until the controller is stopped
        while(self.running):
            #react to the pygame events that come from the xbox controller
            for event in pygame.event.get():

                #thumb sticks, trigger buttons                    
                if event.type == JOYAXISMOTION:
                    #is this axis on our xbox controller
                    if event.axis in self.AXISCONTROLMAP:
                        #is this a y axis
                        yAxis = True if (event.axis == self.PyGameAxis.LTHUMBY or event.axis == self.PyGameAxis.RTHUMBY) else False
                        #update the control value
                        self.updateControlValue(self.AXISCONTROLMAP[event.axis],
                                                self._sortOutAxisValue(event.value, yAxis))
                    #is this axis a trigger
                    if event.axis in self.TRIGGERCONTROLMAP:
                        #update the control value
                        self.updateControlValue(self.TRIGGERCONTROLMAP[event.axis],
                                                self._sortOutTriggerValue(event.value))
                        
                #d pad
                elif event.type == JOYHATMOTION:
                    #update control value
                    self.updateControlValue(self.XboxControls.DPAD, event.value)

                #button pressed and unpressed
                elif event.type == JOYBUTTONUP or event.type == JOYBUTTONDOWN:
                    #is this button on our xbox controller
                    if event.button in self.BUTTONCONTROLMAP:
                        #update control value
                        self.updateControlValue(self.BUTTONCONTROLMAP[event.button],
                                                self._sortOutButtonValue(event.type))
        
    #stops the controller
    def stop(self):
        self.running = False

    #updates a specific value in the control dictionary
    def updateControlValue(self, control, value):
        #if the value has changed update it and call the callbacks
        if self.controlValues[control] != value:
            self.controlValues[control] = value
            self.doCallBacks(control, value)
    
    #calls the call backs if necessary
    def doCallBacks(self, control, value):
        #call the general callback
        if self.controllerCallBack != None: self.controllerCallBack(control, value)

        #has a specific callback been setup?
        if control in self.controlCallbacks:
            self.controlCallbacks[control](value)
            
    #used to add a specific callback to a control
    def setupControlCallback(self, control, callbackFunction):
        # add callback to the dictionary
        self.controlCallbacks[control] = callbackFunction
                
    #scales the axis values, applies the deadzone
    def _sortOutAxisValue(self, value, yAxis = False):
        #invert yAxis
        if yAxis and self.invertYAxis: value = value * -1
        #scale the value
        value = value * self.scale
        #apply the deadzone
        if value < self.upperDeadzone and value > self.lowerDeadzone: value = 0
        return value

    #turns the trigger value into something sensible and scales it
    def _sortOutTriggerValue(self, value):
        #trigger goes -1 to 1 (-1 is off, 1 is full on, half is 0) - I want this to be 0 - 1
        value = max(0,(value + 1) / 2)
        #scale the value
        value = value * self.scale
        return value

    #turns the event type (up/down) into a value
    def _sortOutButtonValue(self, eventType):
        #if the button is down its 1, if the button is up its 0
        value = 1 if eventType == JOYBUTTONDOWN else 0
        return value

	
	

#BEGINING FUCKERY
#--------------------------------------------------------------------------------------------------------------------------------------------------------  
#tests
if __name__ == '__main__':

    #generic call back
    def controlCallBack(xboxControlId, value):
        if 1 == 1:
           # print "Control Id = {}, Value = {} ".format(xboxControlId, value)
	#check for what the input emulated is

            print(xboxControlId, value)
            command = ''
            
			
            if xboxControlId == 13 and value == 1 :
                print("START(enter)")
                command='s'
				#keyboard.press(Key.enter)

           # keyboard.release(Key.enter)
            if xboxControlId == 6 and value == 1:
                print("A(SHIT_L)")
                command = 'a'
                #keyboard.press(Key.shift_l)
               # keyboard.release('z')
            if xboxControlId == 7 and value == 1:
                print("B(ctrl_l)")
                command = 'b'
                #keyboard.press(Key.ctrl_l)
               # keyboard.release('')
            if xboxControlId == 8 and value == 1:
                print("X(z)")
                command='x'
				#keyboard.press('z')
               # keyboard.release('z')
            if xboxControlId == 9 and value == 1 :
                print("Y")
                command='y'               
			#keyboard.press('y')
               # keyboard.release('y')
            if xboxControlId == 2 and value == 1 :
                print("lT")
                command='lT'				
               # keyboard.press('l')
            if xboxControlId == 10 and value == 1 :
                print("lB")
                command='lB'				
                #keyboard.press('l')
            if xboxControlId == 5 and value == 1 :
                print("rT")
                command='rT'				
               # keyboard.press('r')
            if xboxControlId == 11 and value == 1 :
                print("rB")
                command='rB'				
                #keyboard.press('r')
	#gettin tricking reading the dpad for direction
	        
            if xboxControlId == 17:
                if value == (0, 1):
                    print("UP")
                    command='up'					
                    #keyboard.press('w')
                    #keyboard.release('w')
                if value == (0, -1):
                    print("DOWN")
                    command='down'
                    #keyboard.press('s')
                   # keyboard.release('s')
                if value == (1, 0):
                    print("RIGHT")
                    command='right'
                   # keyboard.press('d')
                   # keyboard.release('d')
                if value == (-1, 0):
                    print("LEFT")
                    command='left'
					#keyboard.press('a')
                    #keyboard.release('a')
					
					
		#TURN SHIT OFF FRO THIS PONT DOWN
            if xboxControlId == 13 and value == 0 :
                command="s off"
            if xboxControlId == 6 and value == 0 :
                command="a off"
            if xboxControlId == 7 and value == 0 :
                command="b off"
            if xboxControlId == 8 and value == 0 :
                command="x off"
            if xboxControlId == 9 and value == 0 :
                command="y off"
		
		#triggers off commands
            if xboxControlId == 2 and value == 0 :
                command="lT off"
            if xboxControlId == 10 and value == 0 :
                command="lB off"
            if xboxControlId == 5 and value == 0 :
                command="rT off"
            if xboxControlId == 11 and value == 0 :
                command="rB off"
		#dpad off commands
            if value ==(0, 0):
                print("Off")
                command='off'
                
		
			#send info to client
                #message = str(xboxControlId)
               # message2= str(value)
            sock.sendall(command)			
            #sock.sendall(message2
        

	
    #specific callbacks for the left thumb (X & Y)
    def leftThumbX(xValue):
        print "LX {}".format(xValue)
    def leftThumbY(yValue):
        print "LY {}".format(yValue)

    #setup xbox controller, set out the deadzone and scale, also invert the Y Axis (for some reason in Pygame negative is up - wierd! 
    xboxCont = XboxController(controlCallBack, deadzone = 30, scale = 100, invertYAxis = True)

    #setup the left thumb (X & Y) callbacks
    xboxCont.setupControlCallback(xboxCont.XboxControls.LTHUMBX, leftThumbX)
    xboxCont.setupControlCallback(xboxCont.XboxControls.LTHUMBY, leftThumbY)

    try:
        #start the controller
        xboxCont.start()
        print "xbox controller running"
        while True:
            time.sleep(1)

    #Ctrl C
    except KeyboardInterrupt:
        print "User cancelled"
    
    #error        
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
        
    finally:
        #stop the controller
        xboxCont.stop()
