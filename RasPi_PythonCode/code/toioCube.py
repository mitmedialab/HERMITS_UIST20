import bluepy
import binascii
import time
import sys

class CoreCube(bluepy.btle.Peripheral):
  HANDLE_TOIO_MTR = 0x11
  HANDLE_TOIO_LED = 0x14
  HANDLE_TOIO_SND = 0x17

  def __init__(self):
    bluepy.btle.Peripheral.__init__(self)

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

  def lightSequence(self, times, operations):
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

  def soundSequence(self, times, operations):
    data = "03{:02x}".format(times)
    data = data + "{:02x}".format(len(operations))
    for ope in operations:
      data = data + "{:02x}{:02x}FF".format(ope[0], ope[1])
    self.writeCharacteristic(self.HANDLE_TOIO_SND, binascii.a2b_hex(data))

  def soundStop(self):
    data = "01"
    self.writeCharacteristic(self.HANDLE_TOIO_SND, binascii.a2b_hex(data))

if __name__ == "__main__":

  if len(sys.argv) == 1:
    print('Usage: sample_coreCube1.py BLE_DEVICE_ADDRESS')
    sys.exit()

  TOIO_ADDR  = sys.argv[1]

  try:
    toio = CoreCube()
    toio.connect(TOIO_ADDR, bluepy.btle.ADDR_TYPE_RANDOM)
  except:
    print("device connect error")
    sys.exit()
  time.sleep(1)

  # Light は、(300ms, Red), (300ms, Green) を3回繰り返す
  toio.lightSequence( 3, ( (30,(255,0,0)), (30,(0,255,0)) ) )
  # Sound は、(300ms,ド), (300ms,レ), (300ms,ミ) を2回繰り返す
  toio.soundSequence( 2, ( (30,60), (30,62), (30,64) ) )
  time.sleep(2)

  # Light は Redを点灯
  # Sound は、id = 0 を再生
  toio.lightOn((255,0,0), 0)
  toio.soundId(0)
  time.sleep(1)

  # Light は Greenを点灯
  # Sound は、id = 1 を再生
  toio.lightOn((0,255,0), 0)
  toio.soundId(1)
  time.sleep(1)

  # Light は Blueを点灯
  # Sound は、id = 2 を再生
  toio.lightOn((0,0,255), 0)
  toio.soundId(2)
  time.sleep(1)

  toio.lightOff()

  # 左右=(50,50)で進む
  # 左右=(-50,-50)で進む（後退する）
  # 左右=(50, -50)で進む（その場で回転する）
  toio.motor((50, 50), 0)
  time.sleep(1)
  toio.motor((-50, -50), 0)
  time.sleep(1)
  toio.motor((50, -50), 0)
  time.sleep(1)
  toio.motor((0, 0), 0)
  time.sleep(1)

  toio.disconnect()