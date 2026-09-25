#include "Web.h"

#ifdef HAS_WEB

#include "CommandLine.h"
#include "WebPage.h"

Web web_obj;

// ============ 状态 JSON ============
String Web::buildStatusJson() {
  StaticJsonDocument<1024> doc;
  doc["version"]       = version_number;
  doc["scanMode"]      = wifi_scan_obj.currentScanMode;
  doc["scanning"]      = wifi_scan_obj.scanning();
  doc["channel"]       = wifi_scan_obj.set_channel;
  doc["apCount"]       = access_points->size();
  doc["stationCount"]  = stations->size();
  doc["ssidCount"]     = ssids->size();
  doc["bleCount"]      = ble_devices->size();
  doc["heapFree"]      = ESP.getFreeHeap();
  doc["ip"]            = WiFi.softAPIP().toString();
  String out; serializeJson(doc, out); return out;
}

// ============ AP 列表 JSON ============
String Web::buildApListJson() {
  StaticJsonDocument<8192> doc;
  JsonArray arr = doc.createNestedArray("aps");
  for (int i = 0; i < access_points->size(); i++) {
    AccessPoint ap = access_points->get(i);
    JsonObject o = arr.createNestedObject();
    o["id"]=i; o["ssid"]=ap.ssid; o["bssid"]=macToString(ap.bssid);
    o["channel"]=ap.channel; o["rssi"]=ap.rssi; o["security"]=ap.security; o["selected"]=ap.selected;
  }
  String out; serializeJson(doc, out); return out;
}

// ============ Station 列表 JSON ============
String Web::buildStationListJson() {
  StaticJsonDocument<8192> doc;
  JsonArray arr = doc.createNestedArray("stations");
  for (int i = 0; i < stations->size(); i++) {
    Station st = stations->get(i);
    JsonObject o = arr.createNestedObject();
    o["id"]=i; o["mac"]=macToString(st); o["packets"]=st.packets; o["ap"]=st.ap; o["selected"]=st.selected;
  }
  String out; serializeJson(doc, out); return out;
}

// ============ SSID 列表 JSON ============
String Web::buildSsidListJson() {
  StaticJsonDocument<8192> doc;
  JsonArray arr = doc.createNestedArray("ssids");
  for (int i = 0; i < ssids->size(); i++) {
    JsonObject o = arr.createNestedObject();
    o["id"]=i; o["essid"]=ssids->get(i).essid; o["selected"]=ssids->get(i).selected; o["requests"]=ssids->get(i).requests;
  }
  String out; serializeJson(doc, out); return out;
}

// ============ BLE 列表 JSON ============
String Web::buildBleListJson() {
  StaticJsonDocument<8192> doc;
  JsonArray arr = doc.createNestedArray("bles");
  for (int i = 0; i < ble_devices->size(); i++) {
    BleDevice d = ble_devices->get(i);
    JsonObject o = arr.createNestedObject();
    o["id"]=i; o["mac"]=macToString(d.mac); o["name"]=d.name; o["rssi"]=d.rssi; o["selected"]=d.selected;
  }
  String out; serializeJson(doc, out); return out;
}

// ============ 命令处理 ============
void Web::handleCommand(AsyncWebServerRequest *request) {
  String c = request->hasParam("c") ? request->getParam("c")->value() : "";
  String response;
  if (c.length() == 0) {
    response = "{\"ok\":false,\"msg\":\"empty\"}";
  } else {
    // 复用命令行接口执行命令（写入串口流，由 main 处理）
    Serial.println("web:" + c);
    response = "{\"ok\":true,\"cmd\":\"" + c + "\"}";
  }
  request->send(200, "application/json", response);
}

// ============ 初始化 ============
void Web::RunSetup() {
  // 启动 SoftAP 热点
  WiFi.mode(WIFI_AP);
  WiFi.softAP(WEB_AP_SSID, WEB_AP_PASS, 1, 0, 4);
  delay(100);

  Serial.print("Web AP: ");
  Serial.println(WiFi.softAPIP());

  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/html", FPSTR(INDEX_HTML));
  });
  server.on("/api/status", HTTP_GET, [this](AsyncWebServerRequest *request){
    request->send(200, "application/json", this->buildStatusJson());
  });
  server.on("/api/aps", HTTP_GET, [this](AsyncWebServerRequest *request){
    request->send(200, "application/json", this->buildApListJson());
  });
  server.on("/api/stations", HTTP_GET, [this](AsyncWebServerRequest *request){
    request->send(200, "application/json", this->buildStationListJson());
  });
  server.on("/api/ssids", HTTP_GET, [this](AsyncWebServerRequest *request){
    request->send(200, "application/json", this->buildSsidListJson());
  });
  server.on("/api/bles", HTTP_GET, [this](AsyncWebServerRequest *request){
    request->send(200, "application/json", this->buildBleListJson());
  });
  server.on("/api/command", HTTP_POST, [this](AsyncWebServerRequest *request){
    this->handleCommand(request);
  });

  server.begin();
}

#endif // HAS_WEB
