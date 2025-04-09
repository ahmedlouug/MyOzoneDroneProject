// If you are on espn8266, do not install any other SD card library, use the native to avoid problems with principal pins 

#include <Wire.h>
#include <SPI.h>
#include <SD.h>
#include <DFRobot_OzoneSensor.h>
#include <DFRobot_GNSS.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <SoftwareSerial.h>

// === 🧠 Configuration des broches ===
const int CS_PIN = D8;      // Carte SD - Chip Select
const int SDA_PIN = D2;     // I2C - SDA (capteur ozone)
const int SCL_PIN = D1;     // I2C - SCL (capteur ozone)

// === 🌫️ Capteur d'ozone ===
DFRobot_OzoneSensor Ozone;

// === 📡 Module GPS ===
SoftwareSerial mySerial(D4, D3);  // D4 = RX GPS (entrée ESP), D3 = TX GPS (sortie ESP)
DFRobot_GNSS_UART gnss(&mySerial, 9600);

// === 💾 SD ===
File file;

// === 🌐 Wi-Fi et serveur Flask ===
const char* ssid = "wifi ";
const char* password = "wificode";
const char* server_url = "IP ADRESS from the host comupter";

void setup() {
  Serial.begin(115200);
  delay(2000);

  // === 🔌 Initialisation carte SD ===
  Serial.println("🔌 Initialisation carte SD...");
  if (!SD.begin(CS_PIN)) {
    Serial.println("❌ Erreur SD !");
  } else {
    file = SD.open("/log.csv", FILE_WRITE);
    if (file) {
      file.println("timestamp,ozone_ppb,lat,lon,alt,sats");  // entête CSV
      file.close();
    }
    Serial.println("✅ Carte SD prête");
  }

  // === 🌫️ Initialisation capteur ozone ===
  Wire.begin(SDA_PIN, SCL_PIN);
  if (!Ozone.begin(0x73)) {
    Serial.println("❌ Capteur O₃ non détecté !");
    while (1);
  }
  Ozone.setModes(0x01);
  Serial.println("✅ Capteur O₃ prêt.");

  // === 📡 Initialisation GPS ===
  mySerial.begin(9600);
  while (!gnss.begin()) {
    Serial.println("❌ GPS non détecté !");
    delay(1000);
  }
  gnss.enablePower();
  gnss.setGnss(eGPS_BeiDou_GLONASS);
  gnss.setRgbOn();
  Serial.println("✅ GPS prêt.");

  // === 🌐 Connexion Wi-Fi ===
  WiFi.begin(ssid, password);
  Serial.print("Connexion Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ Connecté !");
}

void loop() {
  // === 🔁 Mesures
  int ozone = Ozone.readOzoneData();
  double lat = gnss.getLat().latitudeDegree;
  double lon = gnss.getLon().lonitudeDegree;
  double alt = gnss.getAlt();
  int sats = gnss.getNumSatUsed();

  // === 🕒 Timestamp GPS
  sTim_t utc = gnss.getUTC();
  char timestamp[25];
  sprintf(timestamp, "%04d-%02d-%02d %02d:%02d:%02d",
          utc.year, utc.month, utc.date,
          utc.hour, utc.minute, utc.second);

  // === 🖥️ Affichage console
  Serial.printf("🕒 %s | O₃: %d ppb | Lat: %.6f | Lon: %.6f | Alt: %.2f | Sats: %d\n",
                timestamp, ozone, lat, lon, alt, sats);

  // === 💾 Écriture carte SD
  file = SD.open("/log.csv", FILE_WRITE);
  if (file) {
    file.printf("%s,%d,%.6f,%.6f,%.2f,%d\n",
                timestamp, ozone, lat, lon, alt, sats);
    file.close();
  } else {
    Serial.println("❌ Erreur écriture SD !");
  }

  // === 🌐 Envoi HTTP vers serveur Flask
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    HTTPClient http;
    http.begin(client, server_url);
    http.addHeader("Content-Type", "text/plain");

    String payload = "timestamp=" + String(timestamp) +
                     ",ozone_ppb=" + String(ozone) +
                     ",lat=" + String(lat, 6) +
                     ",lng=" + String(lon, 6) +
                     ",alt=" + String(alt, 2) +
                     ",sats=" + String(sats);

    int code = http.POST(payload);
    if (code > 0) {
      Serial.print("📤 POST HTTP : ");
      Serial.println(code);
    } else {
      Serial.print("❌ POST erreur : ");
      Serial.println(http.errorToString(code));
    }
    http.end();
  }

  delay(5000);  // nouvelle mesure toutes les 5 secondes
}
