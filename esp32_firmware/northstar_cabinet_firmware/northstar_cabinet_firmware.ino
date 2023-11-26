#include <Arduino.h>
#include <ESPEssentials.h>
#include <FastLED.h>
#include <string.h>

#define NUM_LEDS 255
#define DATA_PIN 14
#define BRIGHTNESS  64
#define LED_TYPE    WS2811
#define COLOR_ORDER GRB
CRGB leds[NUM_LEDS];

void setup()
{
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
  FastLED.clear();
  FastLED.show();

  ESPEssentials::init("Cabinet");
  // On first boot, spinup an AP to configure WIFI
  ESPEssentials::Wifi.autoConnect("Cabinet-Setup");

  // Returns a 200 and GOOD if the device is up and running
  ESPEssentials::WebServer.on("/healthcheck", HTTP_GET, [&]() {
    ESPEssentials::WebServer.send(200, "text/plain", "GOOD");
  });

  // Turn on a specific LED
  ESPEssentials::WebServer.on("/led_on", HTTP_POST, [&]() {
    // Get the LED list
    String led_list = ESPEssentials::WebServer.arg("led_list");
    char buffer[led_list.length() + 1];
    led_list.toCharArray(buffer, led_list.length() + 1);

    char *token = strtok(buffer, ",");

    while (token != NULL) {
      int led = atoi(token);
      leds[led] = CRGB::Red;
      Serial.println(token);
      token = strtok(NULL, ",");
    }
    FastLED.show();

    ESPEssentials::WebServer.send(200, "text/plain", led_list);
  });

  // Turn off all LEDs
  ESPEssentials::WebServer.on("/all_led_off", HTTP_GET, [&]() {
    FastLED.clear();
    FastLED.show();
    ESPEssentials::WebServer.send(200, "text/plain", "GOOD");
  });
}

void loop()
{
    ESPEssentials::handle();
}