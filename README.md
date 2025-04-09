
# 🛰️ Ozone Monitoring System for Drones (ESP8266 + GPS + SD + O3)

This project is a compact onboard data logger designed to measure and record atmospheric ozone concentrations during drone flights.

## 🎯 Objective

- Record real-time ozone concentrations
- Log precise GPS coordinates (lat, lon, altitude)
- Save data locally on a microSD card
- Send data via Wi-Fi to a local Flask server (when available)

## 🧰 Hardware Used

| Component              | Description                          |
|------------------------|--------------------------------------|
| ESP8266 NodeMCU        | Main controller                      |
| Gravity Ozone Sensor   | O₃ concentration via I2C             |
| GNSS Module (TEL0157)  | GPS coordinates & UTC timestamp      |
| MicroSD Card Module    | Data logging via SPI                 |

## ⚡ Wiring Diagram

*(Insert wiring_diagram.png here)*

## 🔌 Wiring Summary

| Module        | ESP8266 Pins         |
|---------------|----------------------|
| SD Card       | D8 (CS), D7, D6, D5   |
| Ozone Sensor  | D2 (SDA), D1 (SCL)    |
| GPS Module    | D4 (TX), D3 (RX)      |

## 📂 Data Format (CSV)

## 📤 Flask Integration

When Wi-Fi is available, the ESP8266 sends the same payload to a local Flask endpoint via HTTP POST.

## ⚠️ Disclaimer

This project is for **experimental and educational purposes**.  
The ozone sensor used is **not calibrated for professional air quality assessments**.

## 📄 License

IMT Nord Europe - Feel free to use, modify, and improve this project!
