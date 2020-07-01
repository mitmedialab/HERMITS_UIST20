//receiving data from APP

void appReceive(Client c) {
  if (c !=null) {
    String whatClientSaid = c.readString();

    //println(whatClientSaid);

    String[] s = split(whatClientSaid, "\n");
    for (int i = 0; i<s.length; i++) {
      String[] m = split(s[i], ",");
      if (m[0].intern() == ("lost").intern() && m.length > 0) { //register.charAt(0) == m[0].charAt(0)){
        //if (pcount != count) {
        //int(m[1])
      } else if (m[0].intern() == ("led").intern() && m.length > 5) { //register.charAt(0) == m[0].charAt(0)){
        int cubeId = getIndextoToioID(int(m[1]));
        int r = int(m[2]);
        int g = int(m[3]);
        int b = int(m[4]);
        int dur =int(m[5]);

        serverToio.ledCommand("toio"+str(cubeId), r, g, b, dur);
      } else if (m[0].intern() == ("motor").intern()) { // && m.length > 4) { //register.charAt(0) == m[0].charAt(0)){
        int cubeId = getIndextoToioID(int(m[1]));
        int left = constrain(int(m[2]), -100, 100);
        int right = constrain(int(m[3]), -100, 100);
        int dur = int(m[4]);
        //println("[Server received from App] motor: id " + cubeId + ", dur " + dur + ", left, right " + left + ", "+ right);

        serverToio.motorCommand("toio"+str(cubeId), left, right, dur);
      } else if (m[0].intern() == ("moveto").intern() && m.length > 5) { //register.charAt(0) == m[0].charAt(0)){
        int cubeId = getIndextoToioID(int(m[1])); //msg.get(0).intValue();
        int tx = int(m[2]); 
        int ty = int(m[3]); 
        int distanceMap = int(m[4]); 
        int offsetMove = int(m[5]); 

        //println("[Server received from App] moveto: id " + cubeId + ", tx,ty " + tx+ ", "  + ty+ ", distanceMap, offsetMove " + distanceMap + ", "+ offsetMove);

        serverToio.movetoCommand("toio"+str(cubeId), tx, ty, distanceMap, offsetMove);
      } else if (m[0].intern() == ("rotateto").intern() && m.length > 4) { //register.charAt(0) == m[0].charAt(0)){
        int cubeId = getIndextoToioID(int(m[1])); //msg.get(0).intValue();
        int ta = int(m[2]); 
        int rotateMap = int(m[3]); 
        int offsetRotate = int(m[4]); 

        //println("[Server received from App] moveto: id " + cubeId + ", tx,ty " + tx+ ", "  + ty+ ", distanceMap, offsetMove " + distanceMap + ", "+ offsetMove);

        serverToio.rotatetoCommand("toio"+str(cubeId), ta, rotateMap, offsetRotate);
      } else if (m[0].intern() == ("vibrate").intern() && m.length > 4) { //register.charAt(0) == m[0].charAt(0)){
        int cubeId = getIndextoToioID(int(m[1]));
        int dur = int(m[2]);
        int amp = int(m[3]);
        int fps = int(m[4]);

        //println("[Server received from App] moveto: id " + cubeId + ", tx,ty " + tx+ ", "  + ty+ ", distanceMap, offsetMove " + distanceMap + ", "+ offsetMove);

        serverToio.vibrateCommand("toio"+str(cubeId), dur, amp, fps);
      } else if (m[0].intern() == ("stop").intern() && m.length > 1) { //register.charAt(0) == m[0].charAt(0)){
        int cubeId = getIndextoToioID(int(m[1]));
        //println("[Server received from App] moveto: id " + cubeId + ", tx,ty " + tx+ ", "  + ty+ ", distanceMap, offsetMove " + distanceMap + ", "+ offsetMove);

        serverToio.stopCommand("toio"+str(cubeId));
      } else if (m[0].intern() == ("midi").intern() && m.length > 4) { //register.charAt(0) == m[0].charAt(0)){
        int cubeId = getIndextoToioID(int(m[1]));
        int midi = int(m[2]);
        int amp = int(m[3]);
        int dur = int(m[4]);

        //println("toio"+str(cubeId), midi, amp, dur);

        serverToio.playSound("toio"+str(cubeId), midi, amp, dur);
      }
    }
  }
}

int getIndextoToioID(int index) {
  int pi = index / cubePerPi;
  int cube = index % cubePerPi;


  return cubeID[pi][cube];
}

int getToioIDtoIndex(int toioID) {
  int x = 0;

  int k = 0;
  boolean flag = false;
  for (int i = 0; i < numPi; i++) {
    for (int j = 0; j < cubePerPi; j++) {
      if (cubeID[i][j] == toioID && !flag) {
        x = k;
        flag = true;
        break;
      }
      k++;
    }
  }


  return x;
}
