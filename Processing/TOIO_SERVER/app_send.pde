//sending data to APP


String sendCommand = "";

void serverSend(Client c) {
  if (c.active()) {
    if (sendCommand != "") {
      c.write(sendCommand);
    }
  } else {
    for (int i = 0; i < numPi; i++) {
      for (int j = 0; j < cubePerPi; j++) {
        String toioName = "toio" + cubeID[i][j];
        if (serverToio._map_toioname_client.get(toioName) != null) {
          Client client = serverToio._map_toioname_client.get(toioName);
          String msg = "stop,"+toioName+"::";
          client.write(msg);
        }
      }
    }
  }
  sendCommand = "";
}

void positionSendToApp (int cubeId, int x, int y, int deg) {
  cubeId = getToioIDtoIndex(cubeId);
  String msg = "pos::"+cubeId+ "::" + x+"::" + y + "::" +deg +"\n";
  sendCommand += msg;

  if (printDebug) {
    println("position sending to app", cubeId, x, y, deg);
  }
}

void accSendToApp (int cubeId, int isFlat, int collision) {
  cubeId = getToioIDtoIndex(cubeId);
  String msg = "acc::"+cubeId+ "::" + isFlat+"::" + collision +"\n";
  sendCommand += msg;
}

void buttonSendToApp (int cubeId, int PressValue) {
  cubeId = getToioIDtoIndex(cubeId);
  String msg = "but::"+cubeId+ "::" + PressValue+"\n";

  sendCommand += msg;
}
