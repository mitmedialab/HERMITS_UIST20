//18.27.126.93
//Connect to Raspberry Pi Server

import processing.net.*;
import java.util.*;

class TCPServer extends Server {
  /***** Fields ********************************************/

  HashMap<String, Client> _map_ip_client = new HashMap<String, Client>(); // string:Client Object

  HashMap<String, String> _map_ip_hostname = new HashMap<String, String>(); // string:Client Object
  HashMap<String, Client> _map_hostname_client = new HashMap<String, Client>();
  HashMap<Client, Integer> _map_client_index = new HashMap<Client, Integer>();
  HashMap<String, String> _map_ip_errormsg = new HashMap<String, String>(); //fps



  HashMap<String, Client> _map_toioname_client = new HashMap<String, Client>();
  HashMap<String, String> _map_toioname_hostname = new HashMap<String, String>();

  int clientNum = 0;


  HashMap<String, Float> _map_ip_fps = new HashMap<String, Float>(); // string:Client Object

  HashMap<String, int[]> _map_toioname_pos = new HashMap<String, int[]>(); // x y dir
  HashMap<String, Integer> _map_toioname_lastupdatedMillis = new HashMap<String, Integer>(); // millis
  HashMap<String, Float> _map_toioname_fps = new HashMap<String, Float>(); //fps
  HashMap<String, Boolean> _map_toioname_lost = new HashMap<String, Boolean>(); //fps



  HashMap<String, Integer> _map_toioname_battery = new HashMap<String, Integer>(); //bat


  Client appClient;
  String appAddress = "127.0.0.1";


  int pcount = 0;
  /***** Constructors **************************************/

  public TCPServer(PApplet applet) {
    super(applet, 8000);
  }

  /***** Destructors ***************************************/

  /***** Getters / Setters *********************************/

  public ArrayList<Client> getClients() {
    ArrayList<Client> clientList = new ArrayList<Client>();
    for (Client c : _map_ip_client.values()) {
      clientList.add(c);
    }
    return clientList;
  }

  public int getNumberOfClients() {
    return _map_ip_client.size();
  }

  /***** Public/Protected Methods **************************/

  public void update() {
    for (Client c : _map_ip_client.values()) { // stopping here ConcurrentModificationException
      if (c.available() > 0) {
        String[] m = split(c.readString(), "\n"); // parsing with multiple lineF
        //println(c.readString());
        for (int i = 0; i < m.length; i++) {
          String data = m[i];
          processClientMessage(c, data);
        }
      }
    }

    if (appClient != null) {
      if (appClient.available() > 0) {
        appReceive(appClient);
      }
    }
  }

  //public void initialize(int[] toioIDs) {
  //  String msg = "initialize";
  //  for (int i = 0; i < numCubesPerPi; i++) {
  //    msg = msg + str(toioIDs[i]) +",";
  //  }

  //  println("Initialize: ", msg);
  //  serverToio.write(msg);
  //}


  public void writeToAllClients(String msg) {
    println("Message To All Clients: ", msg);
    serverToio.write(msg);
  }


  public void motorCommand(String toioName, int left, int right, int dur) {
    Client client = _map_toioname_client.get(toioName);


    String msg = "motor,"+toioName+","+left+","+right+","+dur + "::";

    client.write(msg);
  }

  public void movetoCommand(String toioName, int tx, int ty, int dM, int oM) {
    Client client = _map_toioname_client.get(toioName);

    String msg = "moveto,"+toioName+","+tx+","+ty+","+dM+","+oM + "::";
    client.write(msg);
    println("send moveto command: "+ msg);
  }

  public void rotatetoCommand(String toioName, int ta, int rotateMap, int offsetRotate) {
    Client client = _map_toioname_client.get(toioName);

    String msg = "rotateto,"+toioName+","+ta+","+rotateMap+","+offsetRotate+"::";
    client.write(msg);
    println("send rotateto command: "+ msg);
  }


  public void vibrateCommand(String toioName, int dur, int amp, int fps) {
    Client client = _map_toioname_client.get(toioName);

    String msg = "vibrate,"+toioName+","+dur+","+amp+","+fps+"::";
    client.write(msg);
    println("send vibrate command: "+ msg);
  }

  public void ledCommand(String toioName, int r, int g, int b, int dur) {
    Client client = _map_toioname_client.get(toioName);

    String msg = "led,"+toioName+","+r+","+g+","+b+","+dur + "::";
    client.write(msg);
  }

  public void stopCommand(String toioName) {
    if (_map_toioname_client.get(toioName) != null) {
      Client client = _map_toioname_client.get(toioName);

      String msg = "stop,"+toioName+"::";
      println("send stop command: "+ msg);
      client.write(msg);
    }
  }

  public void playSound(String toioName, int midi, int amp, int dur) {
    Client client = _map_toioname_client.get(toioName);

    String msg = "midi,"+toioName+","+midi+","+amp+","+dur + "::";
    client.write(msg);
  }

  public void setManualADDR(Client c, int index) {
    String msg = "ADDR";
    for (int i = 0; i < cubePerPi; i++) {
      msg += "," + cubeID[index][i];
    }
    msg += "::";
    c.write(msg);
  }


  public void writeToClient(String client_ip, String msg) {
    if (_map_ip_client.containsKey(client_ip)) {
      println("Message To Client at IP (", client_ip, "): ", msg);
      _map_ip_client.get(client_ip).write(msg);
    } else {
      println("Client at IP (", client_ip, ") does not exist");
    }
  }

  public void writeToClientHostname(String hostname, String msg) {
    if (_map_hostname_client.containsKey(hostname)) {
      println("Message To Client (", hostname, "): ", msg);
      _map_hostname_client.get(hostname).write(msg);
    } else {
      println("Client  (", hostname, ") does not exist");
    }
  }

  public void reconnectToios() {
    String msg = "RECONN";

    for (Map.Entry me : _map_ip_client.entrySet()) {
      Client c = _map_ip_client.get(me.getKey());
      c.write(msg);
    }
  }
  public void registerToios() {
    String msg = "REGISTER";

    for (Map.Entry me : _map_ip_client.entrySet()) {
      Client c = _map_ip_client.get(me.getKey());
      c.write(msg);
    }
  }

  //public void writeToClientHostname(String hostname, String msg) {
  //  int clientId = 0;

  //  for (Client c : _clients) {
  //    //HOW do I get the host name??
  //  }


  //  if (_clients.length > clientId) {
  //    println("Message To Client (", clientId, "): ", msg);
  //    _clients[clientId].write(msg);
  //  } else {
  //    println("Client (", clientId, ") does not exist");
  //  }
  //}

  public void disconnectClients() {
    writeToAllClients("cmd,x,disconnect");
    _map_ip_client.clear();
  }

  public String[] getCubeIDList(Client c) {
    String[] IDList = new String[0];

    for (Map.Entry me : _map_toioname_client.entrySet()) {
      if (me.getValue() == c) {
        IDList = append(IDList, me.getKey().toString());
      }
    }


    return IDList;
  }


  public String[][] getCubeID_ParameterList(Client c) {

    String[] ID_ParameterList0 = new String[0];
    int i = 0;
    for (Map.Entry me : _map_toioname_client.entrySet()) {
      if (me.getValue() == c) {
        i++;
        String ID = me.getKey().toString();
        String bat = str(_map_toioname_battery.get(me.getKey().toString()));
        String fps = str(floor(_map_toioname_fps.get(me.getKey().toString())*100.0)/100.0);


        String batAlart = "";
        if (int(bat) < 60) {
          batAlart = "[LOW!]";
        }

        ID_ParameterList0 = append(ID_ParameterList0, "cube: '" + ID +"' bat:" + bat + batAlart+ ", fps: " + fps);
      }
    }

    String[] ID_ParameterList1 = new String[0];
    for (Map.Entry me : _map_toioname_client.entrySet()) {
      if (me.getValue() == c) {
        String[] pos = str(_map_toioname_pos.get(me.getKey().toString()));
        ID_ParameterList1 = append(ID_ParameterList1, "pos(" + pos[0] +", " + pos[1] + ", " + pos[2]+ ")");
      }
    }


    String[][] ID_ParameterList = new String[2][i];

    for (int j = 0; j < i; j++) {
      ID_ParameterList[0][j] = ID_ParameterList0[j];
      ID_ParameterList[1][j] = ID_ParameterList1[j];
    }

    return ID_ParameterList;
  }

  /***** Private Methods ***********************************/

  //called when a client connects.
  private void processServerEvent(Server srvr, Client c)
  {
    //println(c.ip());
    if (c.ip().intern() == appAddress.intern()) { // local app
      println("local connected for App");
      appClient = c;
    } else {

      if (_map_ip_client.get(c.ip()) == null) {
        println("new pi connected!");
        _map_ip_client.put(c.ip(), c);
        _map_client_index.put(c, clientNum);
        _map_ip_errormsg.put(c.ip(), "- no error");
        clientNum++;
      } else {
        int in = _map_client_index.get(_map_ip_client.get(c.ip()));
        _map_ip_client.put(c.ip(), c);
        _map_client_index.put(c, in);
      }
      _map_ip_client.put(c.ip(), c);

      //

      setManualADDR(c, _map_client_index.get(c));
      writeToClient(c.ip(), "setFrameRate,"+str(toioFps));
    }
  }

  private void processClientMessage(Client c, String msg) { //so need to convert hex to string?
    String[] m = split(msg, "::");
    //println("clientmessage", msg);
    if (m[0].intern() == ("hello").intern() && m.length > 1) {
      _map_ip_fps.put(c.ip(), float(m[1]));
    } else if (m[0].intern() == ("hostname").intern() && m.length > 1) {
      _map_hostname_client.put(m[1], c);
      _map_ip_hostname.put(c.ip(), m[1]);
    } else if (m[0].intern() == ("register").intern() && m.length > 2) {
      println(m[1]);
      if (m[1].intern()!="toio0".intern()) { // toio0 will not be registered
        registerTOIO(m[1], m[2], c);
      }
    } else if (m[0].intern() == ("pos").intern() && m.length > 4) { //register.charAt(0) == m[0].charAt(0)){
      //if (pcount != count) {
      if (_map_toioname_lastupdatedMillis.get(m[1]) != null) {
        int ID = int(m[1].replace("toio", ""));
        positionSendToApp(ID, int(m[2]), int(m[3]), int(m[4]));//ID, x, y, degree

        int[] pos = {int(m[2]), int(m[3]), int(m[4])};
        _map_toioname_pos.put(m[1], pos);

        float elapsedTime = (millis() - _map_toioname_lastupdatedMillis.get(m[1])) / 1000.00; // stopping here? zero?
        _map_toioname_fps.put(m[1], 1./elapsedTime);

        pcount = count;
        _map_toioname_lastupdatedMillis.put(m[1], millis());
      }
    } else if (m[0].intern() == ("button").intern() && m.length > 1) { //register.charAt(0) == m[0].charAt(0)){
      // button
      int ID = int(m[1].replace("toio", ""));

      buttonSendToApp(ID, int(m[2]));//ID, buttonState
    } else if (m[0].intern() == ("acc").intern() && m.length > 3) { //register.charAt(0) == m[0].charAt(0)){
      // acc
      int ID = int(m[1].replace("toio", ""));
      accSendToApp(ID, int(m[2]), int(m[3]));//ID, isFlat, collision
    } else if (m[0].intern() == ("bat").intern() && m.length > 1) { //register.charAt(0) == m[0].charAt(0)){
      // bat
      //println(msg);
      _map_toioname_battery.put(m[1], int(m[2]));
    } else if (m[0].intern() == ("error").intern() && m.length > 1) {
      _map_ip_errormsg.put(c.ip(), "[t:" + TimeStamp + "] " + msg);
      println("[" + c.ip() + "] ERROR COMMAND:" + msg);
    }
  }


  private void registerTOIO(String name, String hostname, Client client) {
    if (_map_toioname_client.containsKey(name)) {
      _map_toioname_client.remove(name);
      _map_toioname_hostname.remove(name);
      _map_toioname_pos.remove(name);
      _map_toioname_lastupdatedMillis.remove(name);
      _map_toioname_fps.remove(name);
      _map_toioname_lost.remove(name);
      _map_toioname_battery.remove(name);
    }
    _map_toioname_client.put(name, client);
    _map_toioname_hostname.put(name, hostname);

    int[] pos = {0, 0, 0};
    _map_toioname_pos.put(name, pos);
    _map_toioname_lastupdatedMillis.put(name, 0);
    _map_toioname_fps.put(name, 0.0);
    _map_toioname_lost.put(name, false);
    _map_toioname_battery.put(name, 0);

    serverToio.stopCommand(name);

    //println("Registered a toio!");
    println("Registered Toio (name,hostname): " + name + "," + hostname);
  }
}

//called when a client connects.
//needs to be outside of class definition to be called
void serverEvent(Server srvr, Client clnt)
{
  //as we extended server, we can be sure this here is a TCPServer
  ((TCPServer)srvr).processServerEvent(srvr, clnt);
}

Client[] removeClient(Client[] array, int item) {
  for (int i = item+1; i < array.length; i++) {
    array[i-1] = array[i];
  }
  return array;
}
