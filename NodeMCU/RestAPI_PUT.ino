#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "*****";
const char* password = "*****!";

WiFiServer server(80);

void setup() {
  Serial.begin(115200);

  // Connexion au WiFi
  Serial.println();
  Serial.println();
  Serial.print("Connexion a ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connecté");

  // Start the server
  server.begin();
  Serial.println("Serveur démarré");

  // Donne l'URL du serveur: ");
  Serial.print("http://");
  Serial.print(WiFi.localIP());
  Serial.println("/");

}

void loop() {
  // Si client connecté
  WiFiClient client = server.available();
  if (!client) {
    return;
  }

  // Attente des données du client
  Serial.println("Nouveau client");
  while (!client.available()) {
    delay(1);
  }

  // Lecture de la première ligne
  String request = client.readStringUntil('\r');
  Serial.println(request);
  client.flush();

 
  //Client HTTP 
  String reponse ="";
  String infos = "ville=Quebec&temperature=25&humidite=70";
  HTTPClient http; 
  http.begin("http://10.0.0.36:5000/mabase/10?" + infos);
  http.addHeader("Content-Type", "text/plain");

  
  int httpCode = http.PUT("requete");

  if (httpCode == 201) {
    reponse = http.getString();
    Serial.println("Reponse : ");
    Serial.println(reponse);


  }



  http.end(); //Close connection



  // Retourne la réponse
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println(""); //  Doit être là.
  client.println("<!DOCTYPE HTML>");
  client.println("<head>");
  client.println("<meta charset=\"UTF-8\">");
  client.println("<html>");
  client.println("</head>");
  client.println("<h1>" + reponse + "</h1>");
  client.println("</html>");

  delay(1);
  Serial.println("Client déconnecté");
  Serial.println("");


}
