public int MAT_WIDTH = 415;
public int MAT_HEIGHT = 415;

void displayDebug(){
  
  background(0);
  stroke(255);

  fill(255);
  textSize(12);
  text("FPS = " + frameRate, 10, height-10);//Displays how many clients have connected to the server

  //draw the "mat"
  noFill();
  rect(45, 45, MAT_WIDTH, MAT_HEIGHT);

  //draw the cubes
  for (int i = 0; i < cubes.length; ++i) {
    pushMatrix();
    translate(cubes[i].x, cubes[i].y);
    
    int alpha = 255;
    if (cubes[i].isLost) {
      alpha = 50;
    }
    
    fill(0, 255, 255, alpha);
    text("#"+i + " ["+cubes[i].x+", "+cubes[i].y+"]", 10, -10); 
    noFill();

    rotate(cubes[i].deg * PI/180);

    

    if (cubes[i].buttonState) {
      stroke(0, 255, 255, alpha);
    } else {
      stroke(255, alpha);
    }
    rect(-11, -11, 22, 22);
    rect(0, -5, 20, 10);

    stroke(255, 0, 0, alpha);
    line(-5, -5, 5, 5);
    line(5, -5, -5, 5);

    popMatrix();
  }
  
  
}
