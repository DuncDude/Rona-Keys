import os, sys
import socket
import threading
from pynput.keyboard import Key, Controller
keyboard = Controller()
#Variables for holding information about connections
connections = []
total_connections = 0

#global place holder for the last button pressed

#Client class, new instance created for each connected client
#Each instance has the socket and address that is associated with items
#Along with an assigned ID and a name chosen by the client
class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal
    
    def __str__(self):
        return str(self.id) + " " + str(self.address)
    
    #Attempt to get data from client
    #If unable to, assume client has disconnected and remove him from server data
    #If able to and we get data back, print it in the server and send it back to every
    #client aside from the client that has sent it
    #.decode is used to convert the byte data into a printable string
    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(32)
            except:
                print("Client " + str(self.address) + " has disconnected")
                self.signal = False
                connections.remove(self)
                break
            if data != "":
                xboxControlId = str(data.decode("utf-8"))
                print("recieved msg: " + xboxControlId)
                
                if xboxControlId == 's' :
                    print("START(enter)")
                    keyboard.press(Key.enter)

           # keyboard.release(Key.enter)
                if xboxControlId == 'a' :
                    print("A(SHIT_L)")
                    keyboard.press(Key.shift_l)
               # keyboard.release('z')
                if xboxControlId == 'b':
                    print("B(ctrl_l)")
                    keyboard.press(Key.ctrl_l)
               # keyboard.release('')
                if xboxControlId == 'x':
                    print("X(z)")
                    keyboard.press('z')
               # keyboard.release('z')
                if xboxControlId == 'y':
                    print("Y(y)")
                    keyboard.press('y')
               # keyboard.release('y')
                if xboxControlId == 'lT':
                    print("LT")
               # keyboard.press('l')
                if xboxControlId == 'lB':
                    print("LB")
                #keyboard.press('l')
                if xboxControlId == 'rT':
                    print("RT")
               # keyboard.press('r')
                if xboxControlId == 'rB':
                    print("rB(c)")
                    keyboard.press('c')
                #keyboard.press('r')
	#gettin tricking reading the dpad for direction
                if xboxControlId == 'up':
                    print("UP")
                    keyboard.press(Key.up)
                    #keyboard.release('w')
                if xboxControlId == 'down':
                    print("DOWN")
                    keyboard.press(Key.down)
                   # keyboard.release('s')
                if xboxControlId == 'right':
                    print("RIGHT")
                    keyboard.press(Key.right)
                   # keyboard.release('d')
                if xboxControlId == 'left':
                    print("LEFT")
                    keyboard.press(Key.left)
                    #keyboard.release('a')
            		
					
  
					
					
					#TURN THIS SHIT OFF IF ITS NOT PRESSED!-------------------------
            if xboxControlId == 's off' :
                print("START(enter)off")
                #keyboard.press(Key.enter)
                keyboard.release(Key.enter)
            if  xboxControlId == 'a off':
                print("A(shift_l)off")
                #keyboard.press('z')
                keyboard.release(Key.shift_l)
        	if xboxControlId == 'b off' :
        		print("B(b)off")
    	    	#keyboard.press('b')
                keyboard.release(Key.ctrl_l)
        	if xboxControlId == 'x off' :
        		print("X(z)off")
        		#keyboard.press('z')
    	    	keyboard.release('z')
        	if xboxControlId == 'rB off' :
        		print("rB(c)off")
        		#keyboard.press('z')
    	    	keyboard.release('c')
            if xboxControlId == 'off' :
                print("Y,OFF")
               # keyboard.press('y')
                keyboard.release('y')
            if xboxControlId == 'off' :
                print("LT,OFF")
            if xboxControlId == 'off' :
                print("LB,OFF")
            if xboxControlId == 'off' :
                print("RT,OFF")
            if xboxControlId == 'off' :
                print("RB,OFF")
	#gettin tricking reading the dpad for direction
	
            if xboxControlId == 'off': 
                print("D-Pad released")
                keyboard.release(Key.up)
                keyboard.release(Key.down)
                keyboard.release(Key.right)
                keyboard.release(Key.left)
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				

#Wait for new connections
def newConnections(socket):
    while True:
        sock, address = socket.accept()
        global total_connections
        connections.append(Client(sock, address, total_connections, "Name", True))
        connections[len(connections) - 1].start()
        print("New connection at ID " + str(connections[len(connections) - 1]))
        total_connections += 1

		
def Banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("__________                                ____  __.                   ")
    print("\______   \ ____   ____ _____            |    |/ _|____ ___.__. ______")
    print(" |       _//  _ \ /    \\__  \    ______ |      <_/ __ <   |  |/  ___/")
    print(" |    |   (  <_> )   |  \/ __ \_ /_____/ |    |  \  ___/\___  |\___ \ ")
    print(" |____|_  /\____/|___|  (____  /         |____|__ \___  > ____/____  >")
    print("        \/            \/     \/                  \/   \/\/         \/ ")
    print("SERVER")
    print("------------------------------------------------------------------------")
    return
		
def main():
    #Get host and port
    Banner()
    host = 'localhost'
    #host = input("Host: ")
    port = int(input("Port: "))

    #Create new server socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)

    #Create new thread to wait for connections
    newConnectionsThread = threading.Thread(target = newConnections, args = (sock,))
    newConnectionsThread.start()
    
main()