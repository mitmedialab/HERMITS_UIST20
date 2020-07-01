//Anonymous credit for submission to UIST2020

TCPServer serverToio;
Server serverApp;

Boolean printDebug = false;

int count =0;
float TimeStamp = 0;

void setup() {

  size(550, 1000);
  serverToio = new TCPServer(this);
  serverApp = new Server(this, 5204);

  frameRate(fps);

  assignCubeIDinOrder();
}

void draw() {
  count++;

  // process received data from Pis
  serverToio.update();

  displayStats();

  if (serverToio.appClient != null ) {
    serverSend(serverToio.appClient);
  }
}

void displayStats() {
  int minorSp = 10;
  int majorSp = 16;
  //just some output in the main window
  background(0);
  textAlign(LEFT);
  textSize(12);


  int x = 10, y = 20;
  text("FPS = " + frameRate, x, y);//Displays how many clients have connected to the server

  TimeStamp = float(millis())/1000.0;
  text("| TimeStamp = " + TimeStamp, x+110, y);

  y+=minorSp;
  text("Num of Pi Clients = " + serverToio.getNumberOfClients(), x, y);//Displays how many clients have connected to the server

  textSize(11);
  x+=minorSp;
  y+=majorSp;
  
    if (serverToio._map_ip_client.size()>0) {
      for (String k : serverToio._map_ip_client.keySet()) { //Client c: serverToio._map_ip_client.values()) { //ConcurrentModificationException
        //for (Client c: serverToio._map_ip_client.values()) {
        // print(c.ip());

        text("#" + serverToio._map_client_index.get(serverToio._map_ip_client.get(k)) + " RaspberryPi | name: " + serverToio._map_ip_hostname.get(k), x, y);//Displays how many clients have connected to the server
        y+=minorSp;

        //float f = float(floor(f*pow(10,n)))/pow(10,n)
        text("IP:" + k + ", active: " + serverToio._map_ip_client.get(k).active() + " | " + (serverToio._map_ip_fps.get(k)), x, y);//Displays how many clients have connected to the server
        y+=minorSp;
        x+=minorSp;



        String list[][] = serverToio.getCubeID_ParameterList(serverToio._map_ip_client.get(k));
        // index(i) cube: #1, fps, pos(x:, y:, z:), // #1, fps
        for (int j = 0; j < list[0].length; j++) {
          text(list[0][j], x, y);
          text("| " + list[1][j], x+250, y);
          y+=minorSp;
        }
        x-=minorSp;
        text(serverToio._map_ip_errormsg.get(k), x, y);


        y+=majorSp;

      }
    }
}

void keyPressed() {

  if (key == 'q') {
    serverToio.disconnectClients();
  }
  if (key == 'p') {
    printDebug = !printDebug;
  }
  if (key == ' ') {
    serverToio.reconnectToios();
  }
}
