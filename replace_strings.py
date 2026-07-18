#!/usr/bin/env python3
"""Replace hardcoded English strings in source files with Chinese translations."""

import re

# Translation table from translate.py
HARDCODED = {
    "Scanners": "扫描器",
    "Save/Load Files": "保存/加载文件",
    "Save SSIDs": "保存SSID",
    "Load SSIDs": "加载SSID",
    "Save APs": "保存AP",
    "Load APs": "加载AP",
    "Save Airtags": "保存Airtag",
    "Load Airtags": "加载Airtag",
    "Bluetooth Attacks": "蓝牙攻击",
    "Select": "选择",
    "Active IPs": "活跃IP",
    "AP Info": "AP信息",
    "Set MACs": "设置MAC",
    "Generate AP MAC": "生成AP MAC",
    "Select Stations": "选择终端",
    "Upload Logs": "上传日志",
    "Upload All?": "全部上传?",
    "Delete All?": "全部删除?",
    "Destination": "目标位置",
    "GPS Data": "GPS数据",
    "EP HTML List": "EP网页列表",
    "Mini Keyboard": "迷你键盘",
    "Delete SD Files": "删除SD文件",
    "Probe Requests": "探测请求",
    "Evil Portal": "邪恶门户",
    "SSIDs": "SSID",
    "GPS POI": "GPS兴趣点",
    "Fox Hunt": "信号追踪",
    "Wardrive": "Wardrive",
    "Ping Scan": "Ping扫描",
    "ARP Scan": "ARP扫描",
    "Port Scan All": "全端口扫描",
    "SSH Scan": "SSH扫描",
    "Telnet Scan": "Telnet扫描",
    "SMTP Scan": "SMTP扫描",
    "DNS Scan": "DNS扫描",
    "HTTP Scan": "HTTP扫描",
    "HTTPS Scan": "HTTPS扫描",
    "RDP Scan": "RDP扫描",
    "Packet Count": "数据包计数",
    "Channel Analyzer": "频道分析",
    "Channel Summary": "频道摘要",
    "Scan AP/STA": "扫描AP/STA",
    "MAC Monitor": "MAC监控",
    "SAE Commit": "SAE提交",
    "Karma": "Karma攻击",
    "Bad Msg": "恶意消息",
    "Bad Msg Targeted": "定向恶意消息",
    "Assoc Sleep": "关联休眠",
    "Assoc Sleep Targ": "定向关联休眠",
    "SAE Commit Flood": "SAE提交洪水",
    "Channel Switch": "频道切换",
    "Quiet Time": "静默时间",
    "Access Points": "接入点",
    "User SSIDs": "用户SSID",
    "Select EP HTML File": "选择EP网页文件",
    "Select APs": "选择AP",
    "View AP Info": "查看AP信息",
    "Select ALL": "全选",
    "Max": "最大",
    "Average": "平均",
    "Channel Marker": "频道标记",
    "Frames/": "帧/",
    "BLE Beacons/": "BLE信标/",
    " Evil Portal ": " 邪恶门户 ",
    "EAPOL Sniff": "EAPOL嗅探",
    " Packet Rate": " 数据包速率",
    " Wardrive": " Wardrive",
    " Fox Hunt": " 信号追踪",
    "Touch to exit...": "触摸退出...",
    "Could not find /": "找不到 /",
    "BRIGHTNESS": "亮度",
    "TAP TOP = BRIGHTER": "点按上方=更亮",
    "TAP BOTTOM = DIMMER": "点按下方=更暗",
    "Enter SSID": "输入SSID",
    "Filter Active": "过滤已激活",
    " - Beacons": " - 信标",
    " - Probes": " - 探测",
}

# Files to process
FILES = [
    "esp32_marauder/MenuFunctions.cpp",
    "esp32_marauder/WiFiScan.cpp",
    "esp32_marauder/EvilPortal.cpp",
    "esp32_marauder/Display.cpp",
]

for filepath in FILES:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        changed_count = 0
        
        # Sort by length (longest first) to avoid partial matches
        for eng, chn in sorted(HARDCODED.items(), key=lambda x: -len(x[0])):
            if eng == chn:
                continue
            # Only replace exact string matches in quotes or as identifiers
            # Use word boundary matching
            if f'"{eng}"' in content:
                content = content.replace(f'"{eng}"', f'"{chn}"')
                changed_count += 1
                print(f"  [{filepath}] \"{eng}\" -> \"{chn}\"")
            elif f"\"{eng} " in content:
                # Handle strings with trailing spaces
                pass
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {filepath} ({changed_count} changes)")
        else:
            print(f"No changes in {filepath}")
    except FileNotFoundError:
        print(f"File not found: {filepath}")

print("\nHardcoded string replacements complete!")