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
    String led = ESPEssentials::WebServer.arg("led");
    String color_r = ESPEssentials::WebServer.arg("r");
    String color_g = ESPEssentials::WebServer.arg("g");
    String color_b = ESPEssentials::WebServer.arg("b");

    leds[led.toInt()].r = color_r.toInt();
    leds[led.toInt()].g = color_g.toInt();
    leds[led.toInt()].b = color_b.toInt();
    Serial.println("LED: " + led);
    FastLED.show();

    ESPEssentials::WebServer.send(200, "text/plain", led);
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