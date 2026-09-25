#include "Web.h"

#ifdef HAS_WEB

#include "CommandLine.h"

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
    // 复用命令行接口执行命令（打印到串口流，由 main 处理）
    Serial.println("web:" + c);
    response = "{\"ok\":true,\"cmd\":\"" + c + "\"}";
  }
  request->send(200, "application/json", response);
}

#endif // HAS_WEB
