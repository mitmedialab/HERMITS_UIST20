//Constants for Configurations

int numPi = 14; 
int cubePerPi = 5;

int[][] cubeID = new int[numPi][cubePerPi];

// set your toio ID HERE, 0 is used for empty
int[][] SET_ID = {{2,13,23, 0, 0}}; 

boolean cubeIDinOrder = true;

int fps = 100;

int toioFps = 100; // fps to control toio on pi

void assignCubeIDinOrder() {
  if (cubeIDinOrder) {
    int id = 1;
    for (int i = 0; i < numPi; i++) {
      for (int j = 0; j < cubePerPi; j++) {
        cubeID[i][j] = id;
        id++;
      }
    }

    for (int i = 0; i < cubePerPi; i++) {
      cubeID[0][i] = SET_ID[0][i];
    }
  }
}
