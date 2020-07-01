#sample_moveto.py

from  coreCube import CoreCube
import time
import bluepy
import sys
import Constants
from myDelegate import MyDelegate
import datetime
import utility
import struct

class io_Cube:

    def __init__(self):
        self.starttime = time.time()
        self.numCubesPerPi = Constants.numCubes
        self.targetFPS = Constants.mainFPS
        self.delegates = []
        self.toio_addr = []
        self.toios = []
        self.currentFPS = 5
        self.isDataStored = False
        self.toio_addr = [None]*Constants.numCubes
        self.toio_index = [None]*Constants.numCubes

        self.initiated = 0 #0 is not at all, 1 is received address, 2 is connected
        self.isResetupped = False

        #MATCONFIG
        self.minCoordX = 45
        self.maxCoordX = 455
        self.minCoordY = 45
        self.maxCoordY = 455
        self.matWidth = 410
        self.matHeight = 410
        self.matCol = 1
        self.matRow = 1
        self.currentCol = 0
        self.currentRow = 0

    def setup(self):
        self.toios = []
        self.toio_addr = []
        self.delegates = []

        #search for toio address
        self.toio_addr = [None]*5
        #self.toio_addr = CoreCube.cubeSearch()

        #print("%d toios found!"%(len(self.toio_addr)))
        #if len(self.toio_addr) < self.numCubesPerPi:
          #print("turn on the cube")
          #sys.exit()

        # manually assign

        for i in range(Constants.numCubes):
            self.toio_addr[i] = Constants.toioADDR[self.toio_index[i]]
        #self.toio_addr[1] = Constants.toioADDR[24]
        #self.toio_addr[2] = Constants.toioADDR[26]
        #self.toio_addr[3] = Constants.toioADDR[25]
        #self.toio_addr[4] = Constants.toioADDR[28]

        #create instances from CoreCube Class and add to toios ARRAY
        for i in range(self.numCubesPerPi):
            self.toios.append(CoreCube())

        #connect each cube with ADDRESS
        for i, cube in enumerate(self.toios):
            try:
                time.sleep(0.01)
                if self.toio_index[i] != 0:
                    id = utility.getIDfromADDR(self.toio_addr[i])
                    print("connect to # %d"%(id))
                    cube.connect(self.toio_addr[i], bluepy.btle.ADDR_TYPE_RANDOM) #
            except bluepy.btle.BTLEException as e:
                print("Connection error caught in io_cube setup!")
                print(e)
                self.disconnectAlltoios()
                self.setup()
                #if i == self.toios.len()-1:
                #    break;
                if not self.isResetupped:
                    raise

                #self.disconnectAlltoios()
                #self.setup()
            ''' bluepy.btle.BTLEDisconnectError as e:
                print("Annoying new Error")
                print(e)
                self.reSetup()'''

        #set mat config
        for i, cube in enumerate(self.toios):
            cube.minCoordX = self.minCoordX
            cube.maxCoordX= self.maxCoordX
            cube.minCoordY = self.minCoordY
            cube.maxCoordY = self.maxCoordY
            cube.matCol = self.matCol
            cube.matRow = self.matRow

            cube.matWidth = self.matWidth
            cube.matHeight = self.matHeight

        for i, cubes in enumerate(self.toios):
            # --- Notifyを受け取るクラスの設定 set Class to activate when receive Notify
            id = utility.getIDfromADDR(self.toio_addr[i])
            self.delegates.append(MyDelegate(bluepy.btle.DefaultDelegate, cubes, id))
            cubes.setDelegate(self.delegates[i])

            try:
                # --- Notifyを要求 set Class to activate when receive Notify
                if self.toio_index[i] != 0:
                    cubes.writeCharacteristic(cubes.HANDLE_TOIO_ID  + 1, b'\x01\x00', False) #here
                    cubes.writeCharacteristic(cubes.HANDLE_TOIO_SEN + 1, b'\x01\x00', False)
                    cubes.writeCharacteristic(cubes.HANDLE_TOIO_BTN + 1, b'\x01\x00', False)
                    cubes.writeCharacteristic(cubes.HANDLE_TOIO_BAT + 1, b'\x01\x00', False)
            except Exception as e:
                print("A toio thought to be connected is not. Will try to setup again.")
                self.disconnectAlltoios()
                self.setup()


            #name = cubes.readCharacteristic(cubes.HANDLE_TOIO_BAT + 1, b'\x01\x00')
            #print(name)

        #time.sleep(1)
        for i, cubes in enumerate(self.toios):
            if self.toio_index[i] != 0:
                cubes.lightOn((0,10, 10),0)
            #cubes.mode = 'vibrate'


    def loop(self):
        '''
        for cubes in self.toios:
            data = cubes.readCharacteristic(cubes.HANDLE_TOIO_ID + 1) #, b'\x01\x00')

            print(data)
            #if data != b'\x01\x00':
            id = struct.unpack('b', data[0:1])[0]
            if id == 0x01:
                x, y, dir = struct.unpack('hhh', data[1:7])
                #if Constants.debugPRINT:
                print("ID={%d} |X,Y,dir = (%d,%d), %d" % (self.toio_id, x,y,dir))
                #self.ctoio.x = x
                #self.ctoio.y = y
                #self.ctoio.dir = dir

                #self.commandStore += "pos::toio"+ str(self.toio_id) + "::" + str(x)+"::" + str(y) + "::" + str(dir) +"\n"
                #self.updated = True;
        '''

        try:


            start_time = time.time()
            #previous_time, current_time = current_time, time.clock()



            ts = datetime.datetime.now().timestamp()
            #print(ts) #Print Timestamp


            ## Listen to toios
            for i, cubes in enumerate(self.toios):
                if self.toio_index[i] != 0:
                    if cubes.waitForNotifications(0.000000000001):
                        continue

            ## pass the sensor data to coreCube


            ## send sensor data to server



            ## update toio


            for i, cubes in enumerate(self.toios):
                if self.toio_index[i] != 0:
                    cubes.toioUpdate()
                    pass
                #print("ID = %d | x, y, dir = %d, %d, %d"%(i,cubes.x,cubes.y,cubes.dir))



            #Adjust the FPS
            time_delta = (time.time() - start_time)
            loop_delta = 1./self.targetFPS
            if loop_delta > time_delta:
                time.sleep(loop_delta - time_delta)

            time_delta = (time.time() - start_time)
            #print("%f, %f"%(loop_delta,time_delta))
            self.currentFPS = round(1.0 / time_delta,2)
            #print("FPS: ", self.currentFPS)
        except bluepy.btle.BTLEException as e:
            print('An error was caught by me in io_cube loop!') 
            print(e)
            raise
            #self.disconnectAlltoios()
            #self.setup()




    def commandMotor(self, cubeId, left, right, dur):
        i = self.getNumfromID(cubeId)
        self.toios[i].mode = 'motor'
        self.toios[i].MotorLeft = left
        self.toios[i].MotorRight = right
        self.toios[i].MotorDuration = dur



    def commandMoveto(self, cubeId, tx, ty, dM, oM):
        i = self.getNumfromID(cubeId)
        self.toios[i].mode = 'moveto'
        self.toios[i].targetX = tx
        self.toios[i].targetY = ty
        self.toios[i].distanceMap = dM
        self.toios[i].offsetMap = oM

    def commandRotateto(self, cubeId, targetDeg, rM, oR):
        i = self.getNumfromID(cubeId)
        self.toios[i].mode = 'rotateto'
        self.toios[i].targetDeg = targetDeg
        self.toios[i].rotateMap = rM
        self.toios[i].offsetRotate = oR

    def commandVibrate(self, cubeId, dur, amp, fps):
        i = self.getNumfromID(cubeId)
        self.toios[i].mode = 'vibrate'
        self.toios[i].vibrateDuration = dur
        self.toios[i].vibrateAmplitude = amp
        self.toios[i].cubeUpdateFPS = fps

    def commandLed(self, cubeId, r, g, b, dur):
        i = self.getNumfromID(cubeId)
        color = [r, g, b]
        self.toios[i].lightOn((r,g,b),dur)

    def commandSound(self, cubeId, dur, midi):
        i = self.getNumfromID(cubeId)
        self.toios[i].soundMono(dur, midi)

    def commandStop(self, cubeId):
        i = self.getNumfromID(cubeId)
        self.toios[i].mode = 'stop'

    def setMatConfig(self, minX, maxX, minY, maxY, matCol, matRow):
        print("in cubes ")


        self.minCoordX = minX
        self.maxCoordX = maxX
        self.minCoordY = minY
        self.maxCoordY = maxY
        self.matCol = matCol
        self.matRow = matRow

        self.matWidth = maxX - minX
        self.matHeight = maxY - minY


    def disconnectAlltoios(self):

        for i, cubes in enumerate(self.toios):
            print("disconnecting"+self.toio_addr[i])
            cubes.disconnect()


    def getNumfromID(self,ID):
        for x, add in enumerate(self.toio_addr):
            if add == Constants.toioADDR[ID]:
                return x

        print("unknown ID with address of toio: " + ID)

    def isCommandtoServerUpdated(self):
        iS = False
        for dele in self.delegates:
            if dele.updated:
                iS = True
                break

        return iS




    def getCommandtoSendtoServer(self):
        msg = ""

        for dele in self.delegates:
            msg += dele.commandStore
            dele.clear()


        return msg

    def reSetup(self):
        self.isResetupped = True
        self.disconnectAlltoios()
        self.setup()
