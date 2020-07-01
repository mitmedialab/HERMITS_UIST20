// anonymous credit for submission to UIST2020
import processing.net.*; 
Client myClient;

//we'll keep the cubes here
Cube[] cubes;
int nCubes =  4;

int appFrameRate = 30;

void setup() {
  size(500, 500);
  myClient = new Client(this, "localhost", 8000); 

  //create cubes
  cubes = new Cube[nCubes];
  for (int i = 0; i< cubes.length; ++i) {
    cubes[i] = new Cube(i, true);
  }

  frameRate(appFrameRate);
  textSize(10);
  
}

void draw() {
  serverReceive();

  displayDebug();

  ////** do something to control cube **////
  myCustomFunction();

  if (mouseDrive) {  
    mouseDrive_();
  } else {
    for (int i = 0; i < nCubes; i++) {
      //println(i, cubes[i].isLost);
      //if (!cubes[i].isLost) {
        float mm = map(mouseX, 0, width, -100, 100);
        // println("motorControl from App", i);
        if (abs(mm) > 10) {
          motorControl(i, int(mm), -int(mm), 10);
     //   }
      }
    }
  }
  
  checkLostCube();
  serverSend();
}


void keyPressed() {
  switch(key) {
  //CONTROL toio Motion with ARROW Key
  //motorControl(int cubeId, float left, float right, int duration)
  case CODED: 
    if (keyCode == UP) { 
      motorControl(0, 50, 50, 40); 
    } else if (keyCode == LEFT) {
      motorControl(0, -100, 100, 40);
    } else if (keyCode == RIGHT) {
      motorControl(0, 100, -100, 40);
    } else if (keyCode == DOWN) {
      motorControl(0, -100, -100, 40);
    }
    break;

  //PLAY SOUND and Light LED
  //ledControl(int cubeId, int r, int g, int b, int duration)
  //playSound(int cubeId, int MIDINoteNum, int loudness, int duration)
  case '1': //DO & RED
    playSound(0, 48, 255, 100);
    ledControl(0, 255, 0, 0, 100);
    break;
  case '2': // RE & GREEN
    playSound(1, 50, 255, 100);
    ledControl(1, 0, 255, 0, 100);
    break;
  case '3': // MI & BLUE
    playSound(2, 52, 255, 100);
    ledControl(2, 0, 0, 255, 100);
    break;

  //SET LEDs to the DEFAULT COLOR (light blue)
  case 'l': 
    for (int i = 0; i < nCubes; i++) {
      ledControl(i, 0, 10, 10, 0);
    }
    break;

  //TOGGLE mouseDrive to test aiming function
  case 'm':
    mouseDrive = !mouseDrive;
    break;




  //CONTROL toio target Rotation
  case 'r':
    rotateTo(0, 0, 2, 10);
    break;
  case 'R':
    rotateTo(0, 180, 2, 10);
    break;

  //STOP active control
  case 's': //stop
    for (int i = 0; i < nCubes; i++) {
      pose(i);
    }
    break;

  case ' ':
    myClient =new Client(this, "localhost", 8000); // reconnect
    break;
  default:
    break;
  }
}



void checkLostCube() {
  //did we lost some cubes?
  long now = System.currentTimeMillis();
  for (int i = 0; i< nCubes; ++i) {
    // 500ms since last update
    if (cubes[i].lastUpdate < now - 500 && cubes[i].isLost==false) {
      cubes[i].isLost= true;
    }
  }
}


void myCustomFunction() {
 //WRITE YOUR CODE HERE//
}
