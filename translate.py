#!/usr/bin/env python3
"""
Complete Chinese localization script for ESP32 Marauder - Optimized version.
Only includes CJK Unified Ideographs (U+4E00-U+9FFF) in the font.
Uses ASCII punctuation and numbers throughout.
"""

from PIL import Image, ImageDraw, ImageFont
import re

FONT_SIZE = 15
FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"

# ============================================================
# Complete translation table - using ASCII punctuation
# ============================================================
LANG_VAR_TRANSLATIONS = {
    # Startup texts
    "text0_0": "正在初始化串口...",
    "text0_1": "串口已启动",
    "text0_2": "RAM检查完成",
    "text0_3": "SD卡已初始化",
    "text0_4": "SD卡初始化失败",
    "text0_5": "电池配置已检查",
    "text0_6": "温度接口已初始化",
    "text0_7": "LED接口已初始化",
    "text0_8": "启动中...",
    
    # Common texts
    "text00": "电量变化: ",
    "text01": "文件已关闭",
    "text02": "无法打开文件 '",
    "text03": "开",
    "text04": "关",
    "text05": "加载",
    "text06": "另存为",
    "text07": "退出",
    "text08": "设置",
    "text09": "返回",
    "text10": "频道:",
    "text11": "触摸屏幕退出",
    "text12": "取消",
    "text13": "保存",
    "text14": "是",
    "text15": "正在打开 /update.bin...",
    "text16": "关闭",
    "text17": "失败",
    "text18": "包/秒: ",
    
    # Menu texts
    "text1_0": "SSID列表",
    "text1_1": "添加SSID",
    "text1_2": "SSID: ",
    "text1_3": "密码:",
    "text1_4": "设置已禁用",
    "text1_5": "设置已开启",
    "text1_6": "ESP32 Marauder",
    "text1_7": "WiFi",
    "text1_8": "BadUSB",
    "text1_9": "设备",
    "text1_10": "通用应用",
    "text1_11": "更新中...",
    "text1_12": "选择方式",
    "text1_13": "确认更新",
    "text1_14": "ESP8266更新",
    "text1_15": "固件更新",
    "text1_16": "语言",
    "text1_17": "设备信息",
    "text1_18": "设置",
    "text1_19": "蓝牙",
    "text1_20": "WiFi嗅探器",
    "text1_21": "WiFi攻击",
    "text1_22": "WiFi通用",
    "text1_23": "蓝牙嗅探器",
    "text1_24": "蓝牙通用",
    "text1_25": "关闭WiFi",
    "text1_26": "关闭BLE",
    "text1_27": "生成SSID",
    "text1_28": "清除SSID",
    "text1_29": "清除AP",
    "text1_30": "重启",
    "text1_31": "嗅探器",
    "text1_32": "攻击",
    "text1_33": "通用",
    "text1_34": "蓝牙嗅探",
    "text1_35": "检测刷卡器",
    "text1_36": "测试BadUSB",
    "text1_37": "运行Ducky脚本",
    "text1_38": "绘图",
    "text1_39": "网页更新",
    "text1_40": "SD卡更新",
    "text1_41": "ESP8266更新",
    "text1_42": "探测请求嗅探",
    "text1_43": "信标嗅探",
    "text1_44": "Deauth嗅探",
    "text1_45": "数据包监视器",
    "text1_46": "EAPOL/PMKID扫描",
    "text1_47": "检测Pwnagotchi",
    "text1_48": "检测Espressif",
    "text1_49": "扫描AP",
    "text1_50": "信标列表攻击",
    "text1_51": "随机信标攻击",
    "text1_52": "RickRoll信标",
    "text1_53": "探测请求洪水",
    "text1_54": "Deauth洪水",
    "text1_55": "加入WiFi",
    "text1_56": "选择AP",
    "text1_57": "AP克隆攻击",
    "text1_58": "原始抓包",
    "text1_59": "终端嗅探",
    "text1_60": "清除终端",
    "text1_61": "选择终端",
    "text1_62": "定向Deauth",
    "text1_63": "检测Pineapple",
    "text1_64": "检测多SSID",
    "text1_65": "选择探测SSID",
    "text1_66": "GPS",
    "text1_67": "趣味SSID信标",
    
    # SDInterface.cpp texts
    "text2_0": "错误, 找不到update.bin",
    "text2_1": "开始SD卡更新...",
    "text2_2": "错误, update.bin为空",
    "text2_3": "\n正在重启...\n",
    "text2_4": "无法从/加载update.bin",
    "text2_5": "文件大小: ",
    "text2_6": "正在写入分区...",
    "text2_7": "已写入: ",
    "text2_8": "仅写入: ",
    "text2_9": ". 重试?",
    "text2_10": " 成功",
    "text2_11": "更新完成",
    "text2_12": "更新无法完成",
    "text2_13": "发生错误. 错误号: ",
    "text2_14": "空间不足, 无法开始OTA",
    
    # Web.cpp texts
    "text3_0": "正在配置更新服务器...\n\n",
    "text3_1": "IP地址: ",
    "text3_2": "更新: ",
    "text3_3": "已完成字节: ",
    "text3_4": "更新成功: ",
    "text3_5": "\n更新服务器设置完成",
    
    # WiFiScan.cpp texts
    "text4_0": " 信号强度: ",
    "text4_1": "潜在刷卡器: ",
    "text4_2": "已连接",
    "text4_3": "连接失败",
    "text4_4": "已连接",
    "text4_5": "强制PMKID",
    "text4_6": "强制探测",
    "text4_7": "保存PCAP",
    "text4_8": "探测洪水",
    "text4_9": "正在清除AP...",
    "text4_10": "AP已清除: ",
    "text4_11": "正在清除SSID...",
    "text4_12": "SSID已清除: ",
    "text4_13": "正在生成SSID...",
    "text4_14": "SSID已生成: ",
    "text4_15": "    总SSID数: ",
    "text4_16": "正在关闭WiFi...",
    "text4_17": "WiFi当前未初始化",
    "text4_18": "正在关闭BLE...",
    "text4_19": "BLE当前未初始化",
    "text4_20": "固件: Marauder",
    "text4_21": "版本: ",
    "text4_22": "ESP-IDF: ",
    "text4_23": "WSL绕过: 已启用",
    "text4_24": "WSL绕过: 已禁用",
    "text4_25": "终端MAC: ",
    "text4_26": "AP MAC: ",
    "text4_27": "",
    "text4_28": "SD卡: 已连接",
    "text4_29": "SD卡容量: ",
    "text4_30": "SD卡: 未连接",
    "text4_31": "SD卡容量: 0",
    "text4_32": "电量监控: 支持",
    "text4_33": "电量: ",
    "text4_34": "电量监控: 不支持",
    "text4_35": "内部温度: ",
    "text4_36": " 检测Espressif ",
    "text4_37": " 检测Pwnagotchi ",
    "text4_38": " 信标嗅探器 ",
    "text4_39": " 解除认证嗅探器 ",
    "text4_40": " 探测请求嗅探器 ",
    "text4_41": " 蓝牙嗅探 ",
    "text4_42": " 检测刷卡器 ",
    "text4_43": "正在扫描\n蓝牙刷卡器\nHC-03, HC-05, HC-06...",
    "text4_44": " AP扫描 ",
    "text4_45": "正在清除终端...",
    "text4_46": "终端已清除: ",
    "text4_47": "定向Deauth",
    "text4_48": " 检测Pineapple ",
    "text4_49": " 检测多SSID ",
}

HARDCODED_TRANSLATIONS = {
    # Menu names
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
    "ms": "ms",
    "BLE Beacons/": "BLE信标/",
    
    " Evil Portal ": " 邪恶门户 ",
    "EAPOL Sniff": "EAPOL嗅探",
    " Packet Rate": " 数据包速率",
    " Wardrive": " Wardrive",
    " Fox Hunt": " 信号追踪",
    
    "Touch to exit...": "触摸退出...",
    "Could not find /": "找不到 /",
    
    "GPS": "GPS",
    "SD": "SD",
    "CH: ": "频道:",
    "CH:": "频道:",
    "D:": "内存:",
    "P:": "PSRAM:",
    "X Scale:": "X缩放:",
    "Y Scale:": "Y缩放:",
    "BRIGHTNESS": "亮度",
    "TAP TOP = BRIGHTER": "点按上方=更亮",
    "TAP BOTTOM = DIMMER": "点按下方=更暗",
    "Enter SSID": "输入SSID",
    
    "Filter Active": "过滤已激活",
    " - EAPOL": " - EAPOL",
    " - Beacons": " - 信标",
    " - Deauths": " - Deauth",
    " - Probes": " - 探测",
}

# ============================================================
# Collect Chinese characters (CJK Unified Ideographs only!)
# ============================================================
all_chinese = set()
for text in list(LANG_VAR_TRANSLATIONS.values()) + list(HARDCODED_TRANSLATIONS.values()):
    for ch in text:
        cp = ord(ch)
        # ONLY CJK Unified Ideographs (U+4E00-U+9FFF)
        if 0x4E00 <= cp <= 0x9FFF:
            all_chinese.add(ch)

all_chinese = sorted(all_chinese)
print(f"Total unique CJK characters: {len(all_chinese)}")

# ============================================================
# Generate GFX font
# ============================================================
def render_char(ch, font):
    img = Image.new('1', (FONT_SIZE + 4, FONT_SIZE + 4), 0)
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), ch, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    if w == 0 or h == 0:
        return None, 0, 0
    img2 = Image.new('1', (w, h), 0)
    draw2 = ImageDraw.Draw(img2)
    draw2.text((0, 0), ch, font=font, fill=1)
    bitmap = []
    for y in range(h):
        byte_val = 0
        bit_count = 0
        for x in range(w):
            pixel = img2.getpixel((x, y))
            byte_val = (byte_val << 1) | (1 if pixel else 0)
            bit_count += 1
            if bit_count == 8:
                bitmap.append(byte_val)
                byte_val = 0
                bit_count = 0
        if bit_count > 0:
            byte_val = byte_val << (8 - bit_count)
            bitmap.append(byte_val)
    return bitmap, w, h

font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

glyph_data = {}
all_bitmap = bytearray()
all_bitmap.append(0x00)

for ch in all_chinese:
    cp = ord(ch)
    result = render_char(ch, font)
    if result[0] is not None:
        bm, w, h = result
        offset = len(all_bitmap)
        glyph_data[cp] = (offset, w, h)
        all_bitmap.extend(bm)

codepoints = sorted(glyph_data.keys())
min_cp = codepoints[0]
max_cp = codepoints[-1]
range_size = max_cp - min_cp + 1

print(f"Unicode range: U+{min_cp:04X} to U+{max_cp:04X} ({chr(min_cp)} to {chr(max_cp)})")
print(f"Range size: {range_size} entries")
print(f"Bitmap data: {len(all_bitmap)} bytes")
print(f"Glyph table: {range_size * 6} bytes ({range_size * 6 / 1024:.1f} KB)")
print(f"Total: {len(all_bitmap) + range_size * 6 + 12} bytes ({(len(all_bitmap) + range_size * 6 + 12) / 1024:.1f} KB)")

# Write font
with open('esp32_marauder/chinese_font.h', 'w', encoding='utf-8') as f:
    f.write(f'// Auto-generated Chinese GFX font for TFT_eSPI\n')
    f.write(f'// {len(all_chinese)} unique CJK characters, range U+{min_cp:04X}-U+{max_cp:04X}\n')
    f.write(f'// Total size: {len(all_bitmap) + range_size * 6 + 12} bytes\n')
    f.write('#pragma once\n\n')
    f.write('#include <TFT_eSPI.h>\n\n')
    
    f.write(f'// Bitmap data ({len(all_bitmap)} bytes)\n')
    f.write('PROGMEM const uint8_t chinese_font_bitmap[] = {\n')
    for i in range(0, len(all_bitmap), 16):
        chunk = all_bitmap[i:i+16]
        f.write('  ' + ', '.join(f'0x{b:02X}' for b in chunk) + ',\n')
    f.write('};\n\n')
    
    f.write(f'// Glyph table ({range_size} entries)\n')
    f.write('PROGMEM const GFXglyph chinese_font_glyphs[] = {\n')
    for cp in range(min_cp, max_cp + 1):
        if cp in glyph_data:
            off, w, h = glyph_data[cp]
            f.write(f'  {{ {off:5d}, {w:2d}, {h:2d}, {w:2d}, 0, 0 }}, // U+{cp:04X} {chr(cp)}\n')
        else:
            f.write(f'  {{     0,  0,  0,  0, 0, 0 }}, // U+{cp:04X} (unused)\n')
    f.write('};\n\n')
    
    f.write('// Font structure\n')
    f.write('const GFXfont chinese_font = {\n')
    f.write('  (uint8_t*)chinese_font_bitmap,\n')
    f.write('  (GFXglyph*)chinese_font_glyphs,\n')
    f.write(f'  0x{min_cp:04X}, 0x{max_cp:04X},\n')
    f.write(f'  {FONT_SIZE + 2}\n')
    f.write('};\n\n')
    
    f.write('// Helper macros\n')
    f.write('extern TFT_eSPI tft;\n')
    f.write('#define setChineseFont() tft.setFreeFont(&chinese_font)\n')
    f.write('#define setEnglishFont()  tft.setFreeFont(MENU_FONT)\n')
    f.write('#define setDefaultFont()  tft.setFreeFont(NULL)\n')

print(f"\nFont written to esp32_marauder/chinese_font.h")

# ============================================================
# Generate modified lang_var.h
# ============================================================
print("\nUpdating lang_var.h...")

with open('esp32_marauder/lang_var.h', 'r', encoding='utf-8') as f:
    original = f.read()

new_lines = []
for line in original.split('\n'):
    m = re.match(r'(PROGMEM\s+const\s+char\s+)(\w+)(\[\]\s*=\s*)"(.*)"(\s*;.*)', line)
    if m:
        prefix, var_name, middle, suffix = m.group(1), m.group(2), m.group(3), m.group(5)
        if var_name in LANG_VAR_TRANSLATIONS:
            chinese = LANG_VAR_TRANSLATIONS[var_name]
            new_lines.append(f'{prefix}{var_name}{middle}"{chinese}"{suffix}')
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open('esp32_marauder/lang_var.h', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

print("lang_var.h updated")

# ============================================================
# Print hardcoded string replacements
# ============================================================
print("\n=== Hardcoded strings to replace in source files ===")
for eng, chn in sorted(HARDCODED_TRANSLATIONS.items()):
    if eng != chn:
        print(f'  "{eng}" -> "{chn}"')

print("\nDone!")