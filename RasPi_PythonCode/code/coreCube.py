import bluepy
import binascii
import time
import struct
import codecs
import os
import sys
import math
import utility
import Constants

class CoreCube(bluepy.btle.Peripheral):
  HANDLE_TOIO_ID  = 0x0d
  HANDLE_TOIO_MTR = 0x11
  HANDLE_TOIO_LED = 0x14
  HANDLE_TOIO_SND = 0x17
  HANDLE_TOIO_SEN = 0x1a
  HANDLE_TOIO_BTN = 0x1e
  HANDLE_TOIO_BAT = 0x22
  HANDLE_TOIO_CFG = 0x26

  def __init__(self):
    bluepy.btle.Peripheral.__init__(self)
    self.x = 0
    self.y = 0
    self.x_p = 0
    self.y_p = 0
    self.lastUpdatedPos = time.time()

    self.dir = 0

    #static parameter for Mat Config
    self.minCoordX = 45
    self.maxCoordX = 455
    self.minCoordY = 45
    self.maxCoordY = 455
    self.matWidth = 410
    self.matHeight = 410
    self.matCol = 1
    self.matRow = 1

    #dynamic
    self.currentCol = 0
    self.currentRow = 0

    #self.stdid = 0
    self.button = False
    self.horizon = 0
    self.collision = 0

    self.mode = 'stop' # motor / moveto / rotate / vibrate
    self.cubeUpdateFPS = Constants.toioFPS #FPS to update cube
    self.lastUpdated = time.time()
    self.offsetLosttimeSec = 0.5

    #moveto command#
    self.targetX = 220 #
    self.targetY = 220 #
    self.distanceMap = 100 #
    self.offsetMove = 10 #

    #rotateto command#
    self.targetDeg = 0
    self.offsetRotate = 10
    self.z = 14

    #simple motor actuation: mode 'motor'
    self.MotorLeft = 0
    self.MotorRight = 0
    self.MotorDuration = 0

    #vibration control: mode 'vibrate'
    self.vibrateDuration = 3 #0.0 - 1.0
    #self.vibrateFrequency = 0 #use cubeUpdateFPS instead of this
    self.vibrateAmplitude = 30 # 10-100
    self.vibrationCycle = 0 #switch between 0 and 1
    self.vibrateMode = 'circular' # linear or circular


    self.isDataStored = False
    self.isLost = True

  def toioUpdate(self):
      #print(self.mode)
      currentTime = time.time()
      deltaTime = currentTime - self.lastUpdated


      #print(deltaTime)
      if self.mode != 'vibrate':
          self.cubeUpdateFPS = Constants.toioFPS

      if deltaTime > 1./self.cubeUpdateFPS: #update depending on FPS
          if self.mode == 'stop':
              pass
          elif self.mode =='moveto':
              self.moveToStep()
          elif self.mode =='rotateto':
              self.rotateToStep()
          elif self.mode == 'motor':
              self.motor( (self.MotorLeft, self.MotorRight), self.MotorDuration)
              self.mode ='stop'
          elif self.mode == 'vibrate':
              self.vibrate()
          self.lastUpdated = time.time()

  def toioUpdatePos(self, x_, y_):


      currentTime = time.time()
      deltaTime = currentTime - self.lastUpdatedPos
      self.lastUpdatedPos = currentTime

      xx = x_ - self.minCoordX
      yy = y_ - self.minCoordY

      '''if deltaTime > self.offsetLosttimeSec :
        self.currentCol = 0
        self.currentRow = 0'''
      if xx > 500: #reset if placed on the RESET BOARD (back of toio mat)
        self.currentCol = 0
        self.currentRow = 0
        self.isLost = True
      else:
        matTransThres = 55

        #X coordinate
        if self.x_p > self.matWidth - matTransThres and xx < matTransThres and self.currentCol < self.matCol-1:
            self.currentCol = self.currentCol + 1
        elif xx > self.matWidth - matTransThres and self.x_p < matTransThres and  self.currentCol > 0:
            self.currentCol = self.currentCol - 1


        #Y coordinate
        if self.y_p > self.matHeight - matTransThres and yy <  matTransThres and  self.currentRow < self.matRow-1:
            self.currentRow = self.currentRow + 1
        elif yy > self.matHeight - matTransThres and self.y_p < matTransThres and  self.currentRow > 0:
            self.currentRow = self.currentRow - 1

        self.x = xx + (self.matWidth) * self.currentCol
        self.y = yy + (self.matHeight) * self.currentRow

        self.x_p = xx
        self.y_p = yy

        self.isLost = False




  #  ---------------- connect
  def connect(self, deviceAddr, addrType=bluepy.btle.ADDR_TYPE_RANDOM):
      #try:
          print('connecting to %s'%deviceAddr)
          bluepy.btle.Peripheral.connect(self, deviceAddr, addrType)


  def moveToStep(self): #move toio to target position  xy from current position xy
      currentTime = time.time()
      deltaTime = currentTime - self.lastUpdatedPos
      if deltaTime > self.offsetLosttimeSec:
        self.isLost = True


      dist =  math.sqrt((self.targetX - self.x)**2 + (self.targetY - self.y)**2)

      dd = dist / self.distanceMap
      dd = min(dd, 1)

      left = 0
      right = 0

      angleToTarget = math.atan2(self.targetY - self.y, self.targetX - self.x)

      thisAngle = (self.dir)* math.pi/180
      diffAngle = thisAngle - angleToTarget

      if diffAngle > math.pi: diffAngle -= math.pi*2
      if diffAngle < -math.pi: diffAngle += math.pi*2

      if abs(diffAngle) < math.pi/2 :
          # in fron
          frac = math.cos(diffAngle)
          if diffAngle > 0:
              #left = math.floor(100*math.pow(frac,2)) # original
              left = math.floor(100*frac)
              right = 100
          else:
              left = 100
              #right = math.floor(100*math.pow(frac,2)) # original
              right = math.floor(100*frac)

      else:
          frac = -math.cos(diffAngle)
          if diffAngle > 0:
              left = -math.floor(100*frac) #original
              #left = -math.floor(100*math.pow(frac,2))
              right = -100
          else:
              left = -100
              right = -math.floor(100*frac) #original
              #right = -math.floor(100*math.pow(frac,2))

      ll = math.floor(left*dd)
      rr = math.floor(right*dd)

      if self.isLost == True or dist < self.offsetMove: #if its within the offeset for target coordinate
          self.motor( (0, 0), 0 )
      else:
          #pass
          duration = math.floor(1000./self.cubeUpdateFPS)
          self.motor((ll, rr), duration)

  def rotateToStep(self):
    diff_dir = self.targetDeg - self.dir
    if (abs(diff_dir) <= 15 ):
      self.motor( (0, 0), 0)
    else:
      if diff_dir > 180: diff_dir -= 360
      if diff_dir < -180: diff_dir += 360
      sp = max(int(diff_dir/4), 10) if diff_dir > 0 else min(int(diff_dir/4), -10)
      duration = math.floor(1000./self.cubeUpdateFPS)
      self.motor( (sp, -sp), duration)
      #time.sleep(0.02)


  def vibrate(self):
      duration = self.vibrateDuration #math.floor(self.vibrateDuration * 1./self.cubeUpdateFPS)
      amp = self.vibrateAmplitude

      if self.vibrationCycle == 0: #switch between 0 and 1
          if self.vibrateMode == 'linear': # linear or circular
              self.motor( (amp, amp), duration)
          elif self.vibrateMode == 'circular':
              self.motor( (-amp, amp), duration)
          self.vibrationCycle = 1
      elif self.vibrationCycle == 1: #switch between 0 and 1
          if self.vibrateMode == 'linear': # linear or circular
              self.motor( (-amp, -amp), duration)
          elif self.vibrateMode == 'circular':
              self.motor( (amp, -amp), duration)
          self.vibrationCycle = 0


  #  ---------------- ID Information
  def id(self):
    data = self.readCharacteristic(self.HANDLE_TOIO_ID)
    id = struct.unpack('b', data[0:1])[0]
    if id == 0x01:
      self.x, self.y, self.dir = struct.unpack('hhh', data[1:7])
    elif id == 0x02:
      self.stdid = struct.unpack('i', data[1:5])[0]
      self.dir = struct.unpack('h', data[5:7])[0]
    return id

  #  ---------------- Sensor Information
  def sensor(self):
    data = self.readCharacteristic(self.HANDLE_TOIO_SEN)
    id = struct.unpack('b', data[0:1])[0]
    if id == 0x01:
      self.horizon = struct.unpack('b', data[1:2])[0]
      self.collision = struct.unpack('b', data[2:3])[0]
    return id

  #  ---------------- Battery Information
  def battery(self):
    data = self.readCharacteristic(self.HANDLE_TOIO_BAT)
    return struct.unpack('b', data)[0]

  #  ---------------- Motor Control
  def motor(self, speeds, duration):
    data = "01" if duration == 0 else "02"
    data = data + "01" + ("01" if speeds[0] >= 0 else "02") + ("{:02x}".format(abs(speeds[0])))
    data = data + "02" + ("01" if speeds[1] >= 0 else "02") + ("{:02x}".format(abs(speeds[1])))
    if duration != 0:
      data = data + ("{:02x}".format(duration))
    self.writeCharacteristic(self.HANDLE_TOIO_MTR, binascii.a2b_hex(data))

  #  ---------------- Light Control
  def lightOn(self, color, duration):
    data = "03{:02x}0101{:02x}{:02x}{:02x}".format(duration, color[0], color[1], color[2])
    self.writeCharacteristic(self.HANDLE_TOIO_LED, binascii.a2b_hex(data))

  def lightSequence(self, times, operations):    # operations = ( (duration,(r,g,b)), (d,(r,g,b)), ... )
    data = "04{:02x}".format(times)
    data = data + "{:02x}".format(len(operations))
    for ope in operations:
      data = data + "{:02x}0101{:02x}{:02x}{:02x}".format(ope[0], ope[1][0], ope[1][1], ope[1][2])
    self.writeCharacteristic(self.HANDLE_TOIO_LED, binascii.a2b_hex(data))

  def lightOff(self):
    data = "01"
    self.writeCharacteristic(self.HANDLE_TOIO_LED, binascii.a2b_hex(data))

  #  ---------------- Sound Control
  def soundId(self, id):
    data = "02{:02x}FF".format(id)
    self.writeCharacteristic(self.HANDLE_TOIO_SND, binascii.a2b_hex(data))

  def soundSequence(self, times, operations):     # operations = ( (duration,note), (d,n), ... )
    data = "03{:02x}".format(times)
    data = data + "{:02x}".format(len(operations))
    for ope in operations:
      data = data + "{:02x}{:02x}FF".format(ope[0], ope[1])
    self.writeCharacteristic(self.HANDLE_TOIO_SND, binascii.a2b_hex(data))

  def soundMono(self, duration, note):
    data = "030101{:02x}{:02x}FF".format(duration, note)
    self.writeCharacteristic(self.HANDLE_TOIO_SND, binascii.a2b_hex(data))

  def soundStop(self):
    data = "01"
    self.writeCharacteristic(self.HANDLE_TOIO_SND, binascii.a2b_hex(data))

  #  ---------------- Configuration  ( BLE Version )
  def bleVersion(self):
    data = "0100"
    self.writeCharacteristic(self.HANDLE_TOIO_CFG, binascii.a2b_hex(data))
    time.sleep(0.1)
    data = self.readCharacteristic(self.HANDLE_TOIO_CFG)
    return codecs.decode(data[2:8], encoding='utf-8')

  # ----------------- Utility

  # いちばん近いcoreCube のアドレスを返す。ただし、root で実行する必要がある。
  # （既にconnect中のものがあるとdisconnectされるので注意）
  @classmethod
  def cubeFinder(self):
    if os.environ.get('USER') == 'root':
      scaner = bluepy.btle.Scanner(0)
      devices = scaner.scan(3)

      finds = []
      for device in devices:
        for (adType, desc, value) in device.getScanData():
          if "toio Core Cube" in value:
            finds.append((device.rssi, device.addr))
      if len(finds):
        finds.sort(key = lambda rssi:rssi[0], reverse=True)
        return finds[0][1]
      else:
        raise FileNotFoundError('toio core cube is not found.')
    else:
      raise PermissionError('You need to execute this command as root')

  # coreCube を探して、アドレスを返す。ただし、root で実行する必要がある。
  # 戻り値は、近い順にソートされている
  # （既にconnect中のものがあるとdisconnectされるので注意）
  @classmethod
  def cubeSearch(self):
    if os.environ.get('USER') == 'root':
      scaner = bluepy.btle.Scanner(0)
      devices = scaner.scan(2)

      finds = []
      for device in devices:
        for (adType, desc, value) in device.getScanData():
          if "toio Core Cube" in value:
            finds.append((device.rssi, device.addr))
            print("RSSI: %s, ADDR: %s"%(device.rssi, device.addr))
      ret = []
      if len(finds) != 0:
        finds.sort(key = lambda rssi:rssi[0], reverse=True)
        for i in finds:
          ret.append(i[1])
      return ret
    else:
      raise PermissionError('You need to execute this command as root')

  # 指定角度を向く
  #    細かいパラメータ:
  def turnTo(self, tdir):
    for i in range(20):
      self.id()
      diff_dir = tdir - self.dir
      if (abs(diff_dir) <= 15 ):
        self.motor( (0, 0), 0)
        break
      else:
        if diff_dir > 180: diff_dir -= 360
        if diff_dir < -180: diff_dir += 360
        sp = max(int(diff_dir/4), 10) if diff_dir > 0 else min(int(diff_dir/4), -10)
        self.motor( (sp, -sp), 10)
        time.sleep(0.02)
