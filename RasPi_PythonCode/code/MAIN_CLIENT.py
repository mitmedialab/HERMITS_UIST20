#!/usr/bin/env python
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from __future__ import print_function

from twisted.internet import task, reactor, threads
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol, ReconnectingClientFactory, ClientFactory
from twisted.protocols.basic import LineReceiver
import socket
from sys import stdout
from twisted.logger import Logger
from datetime import datetime
from twisted.internet.task import LoopingCall

import Constants

import io_cube
import utility
import math

import time
import bluepy

log = Logger()

IOcube = io_cube.io_Cube()

class Echo(Protocol):
    def dataReceived(self, data):
        stdout.write(data)


class EchoClient(LineReceiver):
    end = b"Bye-bye!"
    # _isConnected = false

    def connectionMade(self):
        # self.transport.write(b"Hello server, I am the client!\r\n")
        # for i in range(0,2):
            # self.sendToServer(b"toio31::move::203::120")
        starttime = time.time()

        hostname_msg = "hostname::"+socket.gethostname()
        self.sendToServer(hostname_msg.encode('utf-8'))

        '''
        IOcube.setup()

        for i in range (IOcube.numCubesPerPi):
            print("registring toio"+str(utility.getIDfromADDR(IOcube.toio_addr[i])))
            register_msg = "register::toio" + str(utility.getIDfromADDR(IOcube.toio_addr[i])) +"::"+socket.gethostname()
            self.sendToServer(register_msg.encode('utf-8'))


        IOcube.initiated = True
        print("client, start your loop...")
        '''

        print("test loop")
        reactor.callLater(1, self.aSillyBlockingMethodTwo) #without a parameter
        #reactor.callLater(0,self.aSillyBlockingMethodOne,('hehe')) #with a parameter

        # self.sendLine(b"What a fine day it is.")
        # self.sendLine(self.end)


    def lineReceived(self, line):
        print("line received!:", line)
        if line == self.end:
            self.transport.loseConnection()

    def dataReceived(self, data): # receiving
        print("data received!: ", data)
        msg = (data.decode()).split('::')

        for t in msg:
            t.replace('::','')
            print("data received!: ", t)
            s = t.split(",")
            if s[0] == "cmd":
              if s[2] == "disconnect":
                  self.transport.loseConnection()
              elif s[2] == "lightOn" or s[2] == "lightOff":
                self.sendToServer(b"gotit")
              elif s[2] == "greeting":
                self.sendToServer(b"hi")

            elif s[0] == "setFrameRate":
                print("setFrameRate to "+s[1] )
                IOcube.targetFPS = int(s[1])

            elif s[0] == "motor":
                print("this is MOTOR comand:")
                toioID = int(s[1].replace('toio',''))
                left = int(s[2])
                right = int(s[3])
                dur = int(s[4])
                IOcube.commandMotor(toioID, left, right, dur);

            elif s[0] == "moveto":
                print("this is MOVETO comand:")
                toioID = int(s[1].replace('toio',''))
                tx = int(s[2])
                ty = int(s[3])
                dM = int(s[4])
                oM = int(s[5])
                IOcube.commandMoveto(toioID, tx, ty, dM, oM);

            elif s[0] == "vibrate":
                print("this is vibrate comand:")
                toioID = int(s[1].replace('toio',''))
                dur = int(s[2])
                amp = int(s[3])
                fps = int(s[4])
                IOcube.commandVibrate(toioID, dur, amp, fps);

            elif s[0] == "rotateto":
                print("this is ROTATETO comand:")
                toioID = int(s[1].replace('toio',''))
                ta = int(s[2])
                rM = int(s[3])
                oR = int(s[4])
                IOcube.commandRotateto(toioID, ta, rM, oR);


            elif s[0] == "stop":
                print("this is STOP comand:")
                toioID = int(s[1].replace('toio',''))
                IOcube.commandStop(toioID)

            elif s[0] == "led":
                print("this is LED comand:")
                toioID = int(s[1].replace('toio',''))
                r = int(s[2])
                g = int(s[3])
                b = int(s[4])
                dur = int(s[5])
                IOcube.commandLed(toioID, r, g, b, dur)
            elif s[0] == "midi":
                print("this is Sound comand:")
                toioID = int(s[1].replace('toio',''))
                midi = int(s[2])
                amp = int(s[3])
                dur = int(s[4])
                IOcube.commandSound(toioID, dur, midi)
            elif s[0] == "ADDR":
                print("received ADDR ")
                for i in range(Constants.numCubes):
                    IOcube.toio_index[i] = int(s[i+1])
                    print("%d toio is %s"%(i, int(s[i+1])))
                    IOcube.initiated = 1

            elif s[0] == "MATCONFIG":
               print("received MATCONFIG ")
               minCoordX = int(s[1])
               maxCoordX = int(s[2])
               minCoordY = int(s[3])
               maxCoordY = int(s[4])
               matCol = int(s[5])
               matRow = int(s[6])

               IOcube.setMatConfig(minCoordX, maxCoordX, minCoordY, maxCoordY, matCol, matRow)
#             elif s[0] == "RECONN":
#                 print("received RECONN command ")
#                 IOcube.initiated = 0
#                 IOcube.reSetup() #



    def sendToServer(self, msg):
        #print("Send: ", msg)
        self.sendLine(msg)

    def aSillyBlockingMethodTwo(self): # no parameter example
        #time.sleep(10)
        #print (IOcube.initiated)

        if IOcube.initiated == 0: # waiting for server
            print("waiting from server to set the address")

        elif IOcube.initiated == 1: #  make BT connection with toio
            try:
                IOcube.setup() #stop often during connect()
            except bluepy.btle.BTLEException as e:
                print('error caught in client2 high level INITIAL SETUP! Error message is:')
                print(e)
                error_msg = "error::message " + str(e)
                self.sendToServer(error_msg.encode('utf-8'))
                IOcube.reSetup()
            #except bluepy.btle.BTLEDisconnectError as e:
                #print('Annoying new error')
                #print(e)
                #error_msg = "error::message " + str(e)
                #self.sendToServer(error_msg.encode('utf-8'))
                #IOcube.reSetup()


            for i in range (IOcube.numCubesPerPi):
                print("registring toio"+str(utility.getIDfromADDR(IOcube.toio_addr[i])))
                register_msg = "register::toio" + str(utility.getIDfromADDR(IOcube.toio_addr[i])) +"::"+socket.gethostname()
                self.sendToServer(register_msg.encode('utf-8'))


            IOcube.initiated = 2
            IOcube.isResetupped = False 
            print("client, start your loop...")

        elif IOcube.initiated == 2: # the loop

            try:
                IOcube.loop()
            except bluepy.btle.BTLEException as e:
                print('error caught in client2 high level! Error message is:')
                print(e)
                error_msg = "error::message " + str(e)
                self.sendToServer(error_msg.encode('utf-8'))
                IOcube.reSetup()


            if IOcube.isCommandtoServerUpdated():
                commandMsg = IOcube.getCommandtoSendtoServer()
                self.sendToServer(commandMsg.encode('utf-8'))


            register_msg = "hello::"+ str(round(IOcube.currentFPS, 1))
            self.sendToServer(register_msg.encode('utf-8'))

            elapsedTime = time.time() - IOcube.starttime
            #print("ElapsedTime: " + str(elapsedTime))

        reactor.callLater(0,self.aSillyBlockingMethodTwo)



class EchoClientFactory(ClientFactory): #ClientFactory #ReconnectingClientFactory
    protocol = EchoClient

    def __init__(self):
        self.done = Deferred()

    def startedConnecting(self, connector):
        print('Started to connect.')

    def buildProtocol(self, addr):
        print('Connected.')
        print('Resetting reconnection delay')
        #self.resetDelay() #ReconnectingClientFactory
        return EchoClient()


    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())
        IOcube.disconnectAlltoios()

        #ReconnectingClientFactory.clientConnectionLost(self, connector, reason) #https://twisted.readthedocs.io/en/twisted-18.4.0/core/howto/clients.html
        connector.connect()

        # ReconnectingClientFactory.retry()
        # self.done.callback(None)

    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())
        IOcube.disconnectAlltoios()
        #ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
        connector.connect()
        # self.done.errback(reason)


def main(reactor):
    factory = EchoClientFactory()
    reactor.connectTCP(Constants.serverADDR, 8000, factory) #thread
    return factory.done

#starts here
if __name__ == '__main__':
    task.react(main)
