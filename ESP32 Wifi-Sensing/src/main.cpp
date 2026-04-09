#include "esp_wifi.h"
#include <Arduino.h>
// This function runs every time a Wi-Fi packet hits your ESP32
void csi_cb(void *ctx, wifi_csi_info_t *data) {
    // data->len contains the number of subcarriers
    // data->buf contains the actual signal data (Amplitude and Phase)
    
    Serial.print("CSI_DATA,");
    for (int i = 0; i < data->len; i++) {
        Serial.print(data->buf[i]); // Printing raw signal numbers
        Serial.print(",");
    }
    Serial.println("");
}

void setup() {
    Serial.begin(115200);
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    esp_wifi_init(&cfg);
    esp_wifi_set_mode(WIFI_MODE_STA);
    esp_wifi_start();

    // The Magic Lines:
    esp_wifi_set_csi(1); // Enable CSI collection
    esp_wifi_set_csi_cb(csi_cb, NULL); // Link it to our function above
}

void loop() {
    // Everything happens in the background (callback)
}