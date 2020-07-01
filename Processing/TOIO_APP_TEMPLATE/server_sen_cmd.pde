//OSC messages (send)

String sendCommand = "";

void serverSend() {


    if (sendCommand != "") {
      myClient.write(sendCommand);
    }

  sendCommand = "";
}

void ledControl(int cubeId, int r, int g, int b, int duration) {
  // command to control led
  // r, g, b => 0-255 (color control)
  // duration => duration of motor command  0-255 (val*10 millisec)

  String msg = "led,"+cubeId+ "," + r+"," + g+"," + b+","+duration+"\n";

  sendCommand += msg;
}

void motorControl(int cubeId, float left, float right, int duration) {
  // command to directly control the motor
  // left, right => speed of Motor: in range of -100 and 100 (motor will not move under ±10, 10 = 43rpm, 100 = 430rpm)
  // duration => duration of motor command  0-255 (val*10 millisec)
  String msg = "motor,"+cubeId+ "," + (int)left +"," + (int)right +"," + duration+"\n";
  //println(msg);
  sendCommand += msg;
}




void playSound(int cubeId, int MIDINoteNum, int loudness, int duration) {
  // command to make sound 
  // MIDINoteNum =>  1-127 -> https://toio.github.io/toio-spec/docs/ble_sound
  // loudness => 0-255 // *currently not working //
  // duration => 1-255 (val*10 millisec)

  String msg = "midi,"+cubeId+ "," + MIDINoteNum +"," + loudness +"," + duration +"\n";
  sendCommand += msg;
}


// advanced motor control

void moveTo(int cubeId, int tx, int ty, int dM, int oM) {
  // command to make cube move to target coordinate
  // tx, ty => target coordinate
  // dM (distanceMap) => Ratio of Distance mapped to speed  (around 100 is good)
  // oM (offsetMotion) => offset for target position (around 10 is good)
  String msg = "moveto,"+cubeId+ "," + tx +"," + ty +"," + dM +"," + oM+"\n";
  sendCommand += msg;



  //draw target point
  pushMatrix();
  translate(tx, ty);
  stroke(255);
  fill(255, 0, 0);
  ellipse(0, 0, 10, 10);
  
  fill(255, 0, 0);
  textSize(11);
  text(""+int(tx)+", "+ int(ty)+".", 10, 15); 

  popMatrix();

  stroke(255, 0, 0);
  line(cubes[cubeId].x, cubes[cubeId].y, tx, ty);
  
}


void rotateTo(int cubeId, int targetDeg, int offsetRotate, int rotateMap) { //
  // command to rotate cube to target angle
  // targetDeg => target angle in degrees
  // offsetRotate => Ratio of Angle Difference mapped to rotation speed  (*currently not used)
  // rotateMap => offset for target angle (*currently not used)
  String msg = "rotateto,"+cubeId+ "," + targetDeg +"," + offsetRotate +"," + rotateMap + "\n";
  sendCommand += msg;
}

void vibrate(int cubeId, int dur, int amp, int fps) {
  // command to vibrate cube
  // dur: duration of each vibration (val*10 millisec)
  // amp: speed of motor, amplitude of vibration
  // fps: frame per second (around 1-30 would be good?)

  String msg = "vibrate,"+cubeId+ "," +dur +"," + amp +"," + fps +"\n";
  sendCommand += msg;
}

void pose(int cubeId) {
  // command to stop

  String msg = "stop,"+cubeId+"\n";
  sendCommand += msg;
}
