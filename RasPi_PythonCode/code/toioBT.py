import bluepy

scaner = bluepy.btle.Scanner(0)
devices = scaner.scan(3)       # scan時間は3秒

for device in devices:
  for (adType, desc, value) in device.getScanData():
    if "toio Core Cube" in value:
      print('toio Core Cube  Address=%s ,  RSSI=%s' % (device.addr, device.rssi))