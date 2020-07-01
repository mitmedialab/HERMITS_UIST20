from coreCube import CoreCube
import time
import bluepy
import sys
import struct
import Constants
#import send command?

class MyDelegate(bluepy.btle.DefaultDelegate):


    def __init__(self, params, ptoio, toioID):             # コンストラクタで対応するtoioを指定する
        bluepy.btle.DefaultDelegate.__init__(self)
        self.ctoio = ptoio
        #self.addr = address
        self.toio_id = toioID

        self.updated = False
        self.commandStore = ""

    # notify callback: cHandle で何のNotifyかを見分けて処理分岐
    def handleNotification(self, cHandle, data):
        #print(cHandle)
        # ------------- ボタン // button Input
        if cHandle == CoreCube.HANDLE_TOIO_BTN:

          id, stat = struct.unpack('BB', data[0:2])
          if Constants.debugPRINT:
              print("ID={:02x} | BUTTON: STAT={:02x}".format(self.toio_id, stat))
          #self.toio_id.button = stat

          st = int(stat)
          if st == 128:
              self.ctoio.button = False
              st = 0
          else:
              self.ctoio.button = True
              st = 1

          print("but,toio"+ str(self.toio_id) + "," + str(st))
          self.commandStore += "button::toio"+ str(self.toio_id) + "::" + str(st) + "\n"
          self.updated = True;

        # ------------- モーションセンサー Motion Sensor
        if cHandle == CoreCube.HANDLE_TOIO_SEN:
          id, horizon, collision = struct.unpack('BBB', data[0:3])
          if Constants.debugPRINT:
              print("ID={:02x} | SENSOR:  HORIZON={:02x}, COLLISION={:02x}".format(self.toio_id, horizon, collision))
          print("acc,toio"+ str(self.toio_id) + "," + str(horizon)+"," + str(collision))
          self.commandStore += "acc::toio"+ str(self.toio_id) + "::" + str(horizon)+"::" + str(collision) + "\n"

          self.updated = True;
          #if collision:
            #self.ctoio.soundId(6)
        # ------------- IDセンサー Position Reader
        if cHandle == CoreCube.HANDLE_TOIO_ID:
          id = struct.unpack('b', data[0:1])[0]
          if id == 0x01:
            x, y, dir = struct.unpack('hhh', data[1:7])
            if Constants.debugPRINT:
                print("ID={%d} |X,Y,dir = (%d,%d), %d" % (self.toio_id, x,y,dir))

            self.ctoio.toioUpdatePos(x,y)
            self.ctoio.dir = dir

            if self.ctoio.isLost == False:
                self.commandStore += "pos::toio"+ str(self.toio_id) + "::" + str(self.ctoio.x)+"::" + str(self.ctoio.y) + "::" + str(dir) +"\n"
                self.updated = True;

          elif id == 0x02:
            stdid = struct.unpack('i', data[1:5])[0]
            dir = struct.unpack('h', data[5:7])[0]

            if Constants.debugPRINT:
                print("ID = %d,  dir = %d" % (stdid,dir))
        # ------------- battery
        if cHandle == CoreCube.HANDLE_TOIO_BAT:

          stat = int(data[0])

          print("bat,toio"+ str(self.toio_id) + "," + str(stat))
          self.commandStore += "bat::toio"+ str(self.toio_id) + "::" + str(stat) + "\n"
          #self.updated = True;

    def clear(self):
        self.commandStore = ""
        self.updated = False
