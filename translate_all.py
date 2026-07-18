#!/usr/bin/env python3
"""Translate all remaining English display strings to Chinese in the ESP32 Marauder project."""

import os
import re

BASE = "/workspace/esp32_marauder"

# ============================================================
# MenuFunctions.cpp translations
# ============================================================
menu_replacements = [
    # showCenterText calls - Connecting messages
    ('String("Connecting to " + ssid)', 'String("正在连接 " + ssid)'),
    # showCenterText calls - WiGLE
    ('"WiGLE OK"', '"WiGLE上传成功"'),
    ('"WiGLE failed"', '"WiGLE上传失败"'),
    # showCenterText calls - WDG
    ('"WDG OK"', '"WDG上传成功"'),
    ('"WDG failed"', '"WDG上传失败"'),
    # showCenterText calls - Both
    # "Upload OK" and "Upload failed" already translated
    # Delete logs
    ('"Deleting logs..."', '"正在删除日志..."'),
    ('"Logs removed"', '"日志已删除"'),
    # WiFi credentials
    ('"WiFi Credentials Empty."', '"WiFi凭据为空"'),
    ('"Returning..."', '"返回中..."'),
    ('"Could not connect to WiFi."', '"无法连接WiFi"'),
    # POI
    ('"POI Logged"', '"POI已记录"'),
    ('"POI Log Failed"', '"POI记录失败"'),
]

# ============================================================
# WiFiScan.cpp translations
# ============================================================
wifiscan_replacements = [
    # showNetworkInfo
    ('"Connected!"', '"已连接!"'),
    ('"IP address: "', '"IP地址: "'),
    ('"Gateway: "', '"网关: "'),
    ('"Netmask: "', '"子网掩码: "'),
    # MAC: keep as is
    ('"Returning..."', '"返回中..."'),
    # joinWiFi
    ('"Connecting"', '"正在连接"'),
    ('"Failed to connect"', '"连接失败"'),
    # startAP
    ('"Starting"', '"正在启动"'),
    # displayTargetFilter
    ('"Transmitting..."', '"正在发送..."'),
    ('"Targeted Networks"', '"目标网络"'),
    ('"No Networks Selected"', '"未选择网络"'),
    # uploadFile
    ('"WDG Upload..."', '"WDG上传中..."'),
    ('" not found"', '" 未找到"'),
    ('"No WDG API key"', '"无WDG API密钥"'),
    ('"Could not open file"', '"无法打开文件"'),
    ('"WDG connect fail"', '"WDG连接失败"'),
    ('"Waiting for response..."', '"等待响应中..."'),
    ('"WDG OK"', '"WDG上传成功"'),
    ('"WDG Failed"', '"WDG上传失败"'),
    # wigleUpload
    ('"Wigle Upload..."', '"Wigle上传中..."'),
    ('"No wigle creds"', '"无Wigle凭据"'),
    ('"Could not connect"', '"无法连接"'),
    ('"WIGLE OK"', '"WIGLE上传成功"'),
    ('"WIGLE Failed"', '"WIGLE上传失败"'),
    # Filtered
    ('"(Filtered)"', '"（已过滤）"'),
]

# ============================================================
# CommandLine.cpp translations
# ============================================================
cmdline_replacements = [
    ('"POI Logged"', '"POI已记录"'),
    ('"POI Log Failed"', '"POI记录失败"'),
]

def do_replacements(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    for old, new in replacements:
        count = content.count(old)
        if count > 0:
            content = content.replace(old, new)
            print(f"  [{filepath}] '{old}' -> '{new}' ({count} occurrence(s))")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Apply all replacements
print("=== MenuFunctions.cpp ===")
do_replacements(os.path.join(BASE, "MenuFunctions.cpp"), menu_replacements)

print("\n=== WiFiScan.cpp ===")
do_replacements(os.path.join(BASE, "WiFiScan.cpp"), wifiscan_replacements)

print("\n=== CommandLine.cpp ===")
do_replacements(os.path.join(BASE, "CommandLine.cpp"), cmdline_replacements)

print("\nDone!")