//OSC message handling (receive)

void serverReceive() {
  if (myClient.available() > 0) { 

    String data = myClient.readString();
    //println(data);
    processClientMessage(data);
  }
}

void processClientMessage(String msg) {
  String[] s = split(msg, "\n");

  for (int i = 0; i<s.length; i++) {
    String[] m = split(s[i], "::");
    if (m[0].intern() == ("pos").intern() && m.length > 4) { //get position (x, y, and deg)
      //if (pcount != count) {

      int id = int(m[1]);
      int x = int(m[2]);
      int y = int(m[3]);
      int deg = int(m[4]);

      if (id < nCubes) {

        if (id < cubes.length) {
          cubes[id].count++;
          cubes[id].prex = cubes[id].x;
          cubes[id].prey = cubes[id].y;


          cubes[id].x = x;
          cubes[id].y = y;

          cubes[id].deg = deg;

          cubes[id].lastUpdate = System.currentTimeMillis();
        }
        cubes[id].isLost = false;
      }
    } else if (m[0].intern() == ("but").intern() && m.length > 1) {  //get button input 0 or 1
      // button


      int id = int(m[1]);
      int pressValue = int(m[2]);//ID, buttonState

      if (id < nCubes) {
        println("[App Message] Button pressed for id : "+id + ", val = " + pressValue);
        if (pressValue == 1) {
          cubes[id].buttonState = false;
        } else {
          cubes[id].buttonState = true;
        }
      }
    } else if (m[0].intern() == ("acc").intern() && m.length > 3) { 
      // acc
      int id = int(m[1]);
      int isFlat = int(m[2]);
      //int orientation = msg.get(2).intValue();
      int collision = int(m[3]);
      if (id < nCubes) {
        if (collision == 1) {
          println("[App Message] Collision Detected for id : " + id );

          cubes[id].collisionState = true;
        }

        if (isFlat == 1) {
          cubes[id].tiltState = true;
        } else {
          cubes[id].tiltState = false;
        }
      }
    }
  }
}
