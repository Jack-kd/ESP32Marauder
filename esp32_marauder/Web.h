#pragma once

#ifndef Web_h
#define Web_h

#include "configs.h"

#ifdef HAS_WEB

#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <ArduinoJson.h>

#include "WiFiScan.h"
#include "utils.h"

class Web
{
  private:
    AsyncWebServer server;

    // ---- JSON 序列化 ----------------
    String buildStatusJson();
    String buildApListJson();
    String buildStationListJson();
    String buildSsidListJson();
    String buildBleListJson();

    // ---- 命令处理 ----------------
    void handleCommand(AsyncWebServerRequest *request);
    void runWebCommand(String cmd);

  public:
    void RunSetup();
};

extern Web web_obj;

#endif // HAS_WEB
#endif
