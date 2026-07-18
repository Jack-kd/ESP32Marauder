# ESP32 Marauder - Code Wiki

## 1. 项目概览

**ESP32 Marauder** 是一套基于 ESP32/ESP32-S2/ESP32-S3/ESP32-C5/ESP32-C6 系列芯片的 WiFi/蓝牙安全测试工具套件。项目由 [justcallmekoko](https://github.com/justcallmekoko) 开发，版本号为 **v1.14.0**。

**在线资源：**
- 仓库地址：https://github.com/justcallmekoko/ESP32Marauder
- 官方 Wiki：https://github.com/justcallmekoko/ESP32Marauder/wiki
- 官方网站：https://justcallmekokollc.com

**核心功能：**
- WiFi 嗅探（AP 扫描、信标嗅探、探测请求嗅探、Deauth 嗅探、EAPOL/PMKID 扫描、Pineapple 检测、MultiSSID 检测）
- WiFi 攻击（Deauth 洪水、信标垃圾攻击/列表攻击、RickRoll 信标、探测请求洪水、AP 克隆攻击、BadMsg 攻击、睡眠攻击、SAE 攻击、CSA 攻击、Quiet 攻击）
- 蓝牙嗅探（BLE 扫描、刷卡器检测、AirTag 检测、Flock 相机检测、Meta 设备检测）
- 蓝牙攻击（Sour Apple、AppleJuice、SwiftPair 垃圾信息、Samsung/Google/Windows BLE 垃圾信息）
- Evil Portal（强制门户/钓鱼页面）
- GPS 支持（Wardriving、NMEA 解析、GPS 追踪、POI 标记）
- 数据包监控（图形化频谱分析、信道活动分析）
- 无线/有线网络扫描（Ping 扫描、端口扫描、ARP 扫描、DNS/HTTP/HTTPS/SMTP/RDP 扫描）
- CLI 命令行接口（通过串口）
- 支持 30+ 种硬件平台

---

## 2. 项目目录结构

```
/workspace/
├── esp32_marauder/              # ★ 核心固件源代码（Arduino/PlatformIO 项目）
│   ├── esp32_marauder.ino       # 主入口文件（setup/loop）
│   ├── configs.h                # 全局配置（硬件定义、板级特性、编译宏）
│   ├── WiFiScan.h / .cpp        # WiFi/BT 扫描、嗅探、攻击核心类
│   ├── CommandLine.h / .cpp     # 串口命令行接口
│   ├── EvilPortal.h / .cpp      # 强制门户/钓鱼页面
│   ├── MenuFunctions.h / .cpp   # 菜单系统（UI 交互）
│   ├── Display.h / .cpp         # 显示屏驱动（TFT_eSPI 封装）
│   ├── SDInterface.h / .cpp     # SD 卡文件系统操作 / OTA 更新
│   ├── Buffer.h / .cpp          # 双缓冲 PCAP/日志文件写入
│   ├── settings.h / .cpp        # 持久化设置（JSON/SPIFFS）
│   ├── BatteryInterface.h/.cpp  # 电池电量管理（多芯片支持）
│   ├── GpsInterface.h / .cpp    # GPS 接口（NMEA 解析）
│   ├── LedInterface.h / .cpp    # NeoPixel LED 控制
│   ├── Switches.h / .cpp        # 物理按键去抖
│   ├── Keyboard.h / .cpp        # M5Cardputer 键盘驱动
│   ├── Keyboard_def.h           # 键盘键值定义
│   ├── TouchKeyboard.h / .cpp   # 触摸屏虚拟键盘
│   ├── chinese_font.h           # 中文字体资源
│   ├── lang_var.h               # 中文本地化字符串表
│   ├── utils.h                  # 工具函数（MAC 转换、RSSI 颜色等）
│   ├── Assets.h                 # 图片/图标资源（XBM 格式）
│   ├── flipperLED.h / .cpp      # Flipper Zero RGB LED 驱动
│   ├── stickcLED.h / .cpp       # M5StickC LED 驱动
│   ├── xiaoLED.h / .cpp         # XIAO ESP32S3 LED 驱动
│   ├── AXP192.h / .cpp          # AXP192 电源管理芯片驱动
│   ├── ft6336.h                 # 电容触摸屏驱动
│   ├── data/                    # 图片资源
│   └── PreviousVersions/        # 历史固件版本
│
├── libraries/                   # 本地库
│   ├── ESPAsyncWebServer/       # 异步 Web 服务器（Evil Portal 使用）
│   │   └── src/                 # 包含 AsyncWebSocket, AsyncEventSource, WebHandlers 等
│   └── Adafruit_TCA8418/        # TCA8418 键盘矩阵芯片驱动（Cardputer ADV）
│
├── .github/workflows/           # CI/CD 构建矩阵
│   ├── build_parallel.yml       # 主构建流水线（30+ 平台并行构建）
│   ├── nightly_build.yml        # 夜间构建
│   └── close_stale.yml          # 过期 Issue 自动关闭
│
├── FlashFiles/                  # 烧录工具和通用固件
│   ├── FlipperZeroDevBoard/     # Flipper Zero 开发板固件
│   ├── FlipperZeroMultiBoardS3/ # Flipper 多板 S3 固件
│   ├── MarauderV4/              # V4 硬件固件
│   ├── esptool.exe              # esptool 烧录工具
│   └── flash_cmd.txt            # 烧录命令参考
│
├── C5_Py_Flasher_for_adapter/   # C5 适配器 Python 烧录工具
├── C5_Py_Flasher_for_mini_v3/   # Mini v3 Python 烧录工具
├── C5_Py_Flasher_for_v8/        # V8 Python 烧录工具
│
├── PCBs/                        # 硬件设计（KiCad 项目）
│   ├── FlipperZero/WiFi-Devboard-Pro/  # Flipper 开发板 Pro PCB
│   ├── Kit/                     # 套件 PCB
│   ├── v4(OG)/                  # V4 原始硬件 PCB
│   └── v6/                      # V6 硬件 PCB
│
├── mechanical/                  # 3D 外壳模型（STL/STEP/F3Z）
│   ├── Flipper Zero WiFi Dev Board/
│   ├── FlipperZero-WiFi-Devboard-Pro/
│   ├── Marauder-Mini/
│   ├── Marauder Mini v3/
│   ├── OG-Marauder/
│   ├── V6/ V7/ V8/
│   ├── C5 Adapter/
│   └── Flipper Zero BFFB/
│
├── pictures/                    # 图片资源（bmp/XBM 图标、产品照片）
│   ├── icons/                   # 22x22 BMP 菜单图标
│   └── xbm/                     # XBM 格式图标
│
├── Release Bins/                # 发布固件二进制文件
├── MarauderOTA/                 # OTA 更新 Arduino 项目
├── TestFile/                    # CI 测试用 Arduino 项目
├── schematics/                  # 电路原理图
├── tools/                       # 辅助脚本
│   └── check_battery_driver_macros.ps1
├── Drivers/                     # CH340 USB 串口驱动
├── bootloaders/                 # 引导加载程序
├── User_Setup*.h               # TFT_eSPI 各平台显示配置
├── generate_all.py             # 全平台构建脚本
├── translate.py / translate_all.py  # 翻译辅助脚本
├── regenerate_font.py           # 字体生成脚本
├── replace_strings.py           # 字符串替换脚本
├── update_rendering.py          # 渲染更新脚本
├── .travis.yml                  # 旧版 Travis CI 配置
└── README.md                    # 项目说明
```

---

## 3. 系统架构

### 3.1 整体架构图

```
┌─────────────────────────────────────────────────────────────────────┐
│                        esp32_marauder.ino                           │
│                    (setup / loop 主控制器)                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │  Display  │  │  Menu    │  │  WiFiScan │  │  CommandLine     │   │
│  │  (TFT)    │  │ Functions│  │  (核心)    │  │  (CLI)           │   │
│  └────┬─────┘  └────┬─────┘  └─────┬─────┘  └────────┬─────────┘   │
│       │              │              │                  │             │
│  ┌────┴─────┐  ┌────┴─────┐  ┌─────┴──────────────────┴──────┐     │
│  │  TouchKB  │  │ Keyboard │  │        核心功能模块            │     │
│  │  Switches │  │ (CardP)  │  │  EvilPortal / Buffer /       │     │
│  └──────────┘  └──────────┘  │  SDInterface / Settings       │     │
│                               │  BatteryInterface /          │     │
│  ┌──────────┐  ┌──────────┐  │  GpsInterface / LedInterface │     │
│  │flipperLED│  │stickcLED │  └───────────────────────────────┘     │
│  └──────────┘  └──────────┘                                        │
│  ┌──────────┐  ┌──────────┐                                        │
│  │ xiaoLED  │  │ LedIface │                                        │
│  └──────────┘  └──────────┘                                        │
├─────────────────────────────────────────────────────────────────────┤
│                       外部库依赖                                     │
│  TFT_eSPI | NimBLE | ESPAsyncWebServer | AsyncTCP | ArduinoJson    │
│  MicroNMEA | LinkedList | Adafruit_NeoPixel | ESP32Ping | DNSServer│
│  XPowersLib | Adafruit_MAX1704X | Adafruit_BusIO | JPEGDecoder      │
│  lv_arduino | XPT2046_Touchscreen | EspSoftwareSerial              │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 模块依赖关系

```
esp32_marauder.ino
  ├── configs.h (全局配置，被所有模块引用)
  ├── WiFiScan.h/cpp ────────────→ Display, SDInterface, Buffer, Settings,
  │                                 GpsInterface, BatteryInterface,
  │                                 EvilPortal, LedInterface, flipperLED,
  │                                 xiaoLED, stickcLED, utils.h
  ├── CommandLine.h/cpp ────────→ WiFiScan, SDInterface, Settings,
  │                                 MenuFunctions, Display, LedInterface
  ├── EvilPortal.h/cpp ─────────→ ESPAsyncWebServer, AsyncTCP, DNSServer,
  │                                 SDInterface, Buffer, Display, Settings
  ├── MenuFunctions.h/cpp ──────→ WiFiScan, BatteryInterface, SDInterface,
  │                                 Settings, Switches, Display,
  │                                 Keyboard, TouchKeyboard
  ├── Display.h/cpp ────────────→ TFT_eSPI, XPT2046_Touchscreen, ft6336
  ├── SDInterface.h/cpp ────────→ SD, SPI, Buffer, Display, Settings
  ├── settings.h/cpp ───────────→ SPIFFS, ArduinoJson, Display
  ├── Buffer.h/cpp ─────────────→ FS, Settings
  ├── BatteryInterface.h/cpp ───→ Wire, Adafruit_MAX1704X, XPowersLib, AXP192
  ├── GpsInterface.h/cpp ───────→ MicroNMEA, SoftwareSerial
  ├── LedInterface.h/cpp ───────→ Adafruit_NeoPixel, Settings
  ├── Switches.h/cpp ───────────→ Arduino (独立)
  ├── Keyboard.h/cpp ───────────→ Adafruit_TCA8418 (Cardputer ADV)
  ├── TouchKeyboard.h/cpp ──────→ Display
  ├── flipperLED.h/cpp ─────────→ Settings (独立)
  ├── stickcLED.h/cpp ──────────→ Settings (独立)
  ├── xiaoLED.h/cpp ────────────→ Settings (独立)
  ├── lang_var.h ───────────────→ (字符串表，独立)
  ├── chinese_font.h ───────────→ (字体数据，独立)
  ├── utils.h ──────────────────→ (内联工具函数，独立)
  └── Assets.h ─────────────────→ (图片资源，独立)
```

---

## 4. 核心模块详细说明

### 4.1 主入口：[esp32_marauder.ino](file:///workspace/esp32_marauder/esp32_marauder.ino)

这是整个项目的入口点，负责系统初始化和主循环调度。

**关键全局对象：**

| 对象 | 类型 | 说明 |
|------|------|------|
| `wifi_scan_obj` | `WiFiScan` | WiFi/BT 扫描和攻击核心 |
| `evil_portal_obj` | `EvilPortal` | 强制门户/钓鱼页面 |
| `buffer_obj` | `Buffer` | PCAP/日志文件双缓冲写入 |
| `settings_obj` | `Settings` | 持久化设置管理 |
| `cli_obj` | `CommandLine` | 串口命令行 |
| `display_obj` | `Display` | TFT 显示驱动封装 |
| `menu_function_obj` | `MenuFunctions` | 菜单 UI 系统 |
| `sd_obj` | `SDInterface` | SD 卡文件系统 |
| `battery_obj` | `BatteryInterface` | 电池电量管理 |
| `gps_obj` | `GpsInterface` | GPS 接口 |
| `led_obj` / `flipper_led` / `stickc_led` / `xiao_led` | LED 驱动 | 平台特定 LED 控制 |

**setup() 初始化流程：**
1. 随机数种子初始化，抑制 ESP 日志（非开发模式）
2. 初始化 PSRAM（如配置）
3. 串口初始化（115200 baud）
4. 配置 SPI 总线、CS 引脚
5. 初始化显示屏（TFT）
6. 背光 PWM 初始化
7. 检查 stealth mode（按住中心按钮启动）
8. 加载设置（SPIFFS JSON）
9. 初始化 SD 卡
10. 初始化 WiFiScan
11. 初始化 EvilPortal
12. 初始化电池、GPS、LED
13. 初始化菜单系统
14. 启动 CLI

**loop() 主循环（约 1ms/50ms 周期）：**
1. 检查触摸屏禁用/启用切换
2. 更新 CLI（`cli_obj.main()`）
3. 更新 WiFiScan（`wifi_scan_obj.main()`）
4. 更新 GPS（`gps_obj.main()`）
5. 刷新缓冲区到 SD 卡
6. 更新电池状态
7. 更新菜单 UI（非包监控模式）
8. 更新 LED 状态

---

### 4.2 全局配置：[configs.h](file:///workspace/esp32_marauder/configs.h)

这是项目最核心的配置文件，定义了所有硬件平台的条件编译宏。

**支持的硬件平台（30+）：**

| 宏定义 | 硬件名称 | 芯片 |
|--------|----------|------|
| `MARAUDER_M5STICKC` | M5Stick-C Plus | ESP32 |
| `MARAUDER_M5STICKCP2` | M5Stick-C Plus2 | ESP32 |
| `MARAUDER_M5_NANO_C6` | M5 Nano C6 | ESP32-C6 |
| `MARAUDER_CARDPUTER` | M5 Cardputer | ESP32-S3 |
| `MARAUDER_CARDPUTER_ADV` | M5 Cardputer ADV | ESP32-S3 |
| `MARAUDER_MINI` | Marauder Mini | ESP32 |
| `MARAUDER_MINI_V3` | Marauder Mini v3 | ESP32-C5 |
| `MARAUDER_V4` | Marauder v4 (OG) | ESP32 |
| `MARAUDER_V6` / `V6_1` | Marauder v6/v6.1 | ESP32 |
| `MARAUDER_V7` / `V7_1` | Marauder v7/v7.1 | ESP32 |
| `MARAUDER_V8` | Marauder v8 | ESP32-C5 |
| `MARAUDER_PANCAKE` | Pancake Marauder V8 | ESP32-C5 |
| `MARAUDER_KIT` | Marauder Kit | ESP32 |
| `MARAUDER_FLIPPER` | Flipper Zero Dev Board | ESP32-S2 |
| `MARAUDER_MULTIBOARD_S3` | Flipper Multi Board S3 | ESP32-S3 |
| `MARAUDER_DEV_BOARD_PRO` | Flipper Dev Board Pro | ESP32 |
| `MARAUDER_REV_FEATHER` | Adafruit Feather ESP32-S2 Reverse TFT | ESP32-S2 |
| `MARAUDER_CYD_MICRO` | CYD 2432S028 | ESP32 |
| `MARAUDER_CYD_2USB` | CYD 2432S028 2USB | ESP32 |
| `MARAUDER_CYD_GUITION` | CYD 2432S024 GUITION | ESP32 |
| `MARAUDER_CYD_3_5_INCH` | CYD 3.5inch | ESP32 |
| `ESP32_LDDB` | ESP32 LDDB | ESP32 |
| `GENERIC_ESP32` | 通用 ESP32 | ESP32 |
| `XIAO_ESP32_S3` | XIAO ESP32 S3 | ESP32-S3 |
| `MARAUDER_C5` | ESP32-C5 DevKit | ESP32-C5 |
| `DUAL_MINI_C5` | Dual Mini C5 | ESP32-C5 |

**硬件特性宏（按平台选择性定义）：**

| 宏 | 含义 |
|----|------|
| `HAS_SCREEN` | 有显示屏 |
| `HAS_TOUCH` | 有触摸屏 |
| `HAS_BT` | 有蓝牙功能 |
| `HAS_BT_REMOTE` | 有蓝牙远程功能 |
| `HAS_SD` | 有 SD 卡 |
| `USE_SD` | 启用 SD 卡 |
| `HAS_BATTERY` | 有电池管理 |
| `HAS_GPS` | 有 GPS 模块 |
| `HAS_NEOPIXEL_LED` | 有 NeoPixel LED |
| `HAS_FLIPPER_LED` | 有 Flipper 风格 RGB LED |
| `HAS_BUTTONS` | 有物理按键 |
| `HAS_MINI_KB` | 有迷你键盘导航 |
| `HAS_PSRAM` | 有 PSRAM |
| `HAS_DUAL_BAND` | 支持双频 (2.4GHz + 5GHz) |
| `HAS_NIMBLE_2` | 使用 NimBLE 2.x |
| `HAS_IDF_3` | 使用 ESP-IDF 3.x |
| `HAS_C5_SD` | 使用 C5 独立 SPI SD 总线 |
| `HAS_DIRECT_UPLOAD` | 支持直接上传到 Wigle/WDG |
| `HAS_ACT_LED` | 有活动指示灯 |

**关键常量：**

| 常量 | 值 | 说明 |
|------|-----|------|
| `MARAUDER_VERSION` | `"v1.14.0"` | 固件版本 |
| `GRAPH_REFRESH` | 100 | 图表刷新间隔 (ms) |
| `TRACK_EVICT_SEC` | 90 | MAC 跟踪过期时间 (秒) |
| `DUAL_BAND_CHANNELS` | 51 | 双频信道数 |
| `DISPLAY_BUFFER_LIMIT` | 20 | 显示缓冲区大小 |
| `JSON_SETTING_SIZE` | 2048 | JSON 设置字符串最大长度 |
| `MAX_HTML_SIZE` | 30000 (PSRAM) / 11400 (无 PSRAM) | Evil Portal HTML 最大尺寸 |
| `BUF_SIZE` | 8KB (PSRAM) / 3KB (无 PSRAM) | PCAP 缓冲区大小 |
| `SNAP_LEN` | 4096 (PSRAM) / 2324 (无 PSRAM) | 最大捕获包长度 |

---

### 4.3 WiFiScan - WiFi/蓝牙扫描与攻击核心：[WiFiScan.h](file:///workspace/esp32_marauder/WiFiScan.h)

**职责：** 这是整个项目最核心和最大的模块，负责所有 WiFi 和蓝牙的扫描、嗅探和攻击功能。

**扫描模式常量（30+ 种）：**

| 模式 | 值 | 说明 |
|------|-----|------|
| `WIFI_SCAN_OFF` | 0 | 关闭扫描 |
| `WIFI_SCAN_PROBE` | 1 | 探测请求嗅探 |
| `WIFI_SCAN_AP` | 2 | AP 扫描 |
| `WIFI_SCAN_PWN` | 3 | Pwnagotchi 检测 |
| `WIFI_SCAN_EAPOL` | 4 | EAPOL/PMKID 扫描 |
| `WIFI_SCAN_DEAUTH` | 5 | Deauth 嗅探 |
| `WIFI_SCAN_ALL` | 6 | 全量扫描 |
| `WIFI_PACKET_MONITOR` | 7 | 数据包监控器 |
| `WIFI_ATTACK_BEACON_SPAM` | 8 | 随机信标攻击 |
| `WIFI_ATTACK_RICK_ROLL` | 9 | RickRoll 信标 |
| `BT_SCAN_ALL` | 10 | 蓝牙全量扫描 |
| `BT_SCAN_SKIMMERS` | 11 | 蓝牙刷卡器检测 |
| `WIFI_ATTACK_BEACON_LIST` | 15 | 信标列表攻击 |
| `WIFI_ATTACK_DEAUTH` | 20 | Deauth 洪水 |
| `WIFI_ATTACK_AP_SPAM` | 21 | AP 克隆攻击 |
| `WIFI_SCAN_RAW_CAPTURE` | 25 | 原始抓包 |
| `WIFI_SCAN_EVIL_PORTAL` | 30 | Evil Portal |
| `WIFI_SCAN_WAR_DRIVE` | 32 | Wardriving |
| `BT_ATTACK_SOUR_APPLE` | 36 | Sour Apple 攻击 |
| `BT_ATTACK_SWIFTPAIR_SPAM` | 37 | SwiftPair 垃圾信息 |
| `BT_ATTACK_SPAM_ALL` | 38 | 全量 BLE 垃圾信息 |
| `WIFI_SCAN_PINESCAN` | 50 | Pineapple 检测 |
| `WIFI_SCAN_MULTISSID` | 51 | 多 SSID 检测 |
| `WIFI_PING_SCAN` | 53 | Ping 扫描 |
| `WIFI_PORT_SCAN_ALL` | 54 | 端口扫描 |
| `GPS_TRACKER` | 55 | GPS 追踪 |
| `BT_SCAN_FLOCK` | 72 | Flock 相机检测 |
| `BT_SCAN_AIRTAG_MON` | 70 | AirTag 持续监控 |
| `BT_SCAN_FOX_HUNT` | 84 | 蓝牙 Fox Hunt (信号强度追逐) |
| `BT_FINDMY_SOUND` | 85 | FindMy 追踪器声音触发 |

**关键数据结构：**

- `MacEntry`：MAC 地址跟踪条目（MAC、最后出现时间、帧数、GPS 坐标、RSSI）
- `AccessPoint`：WiFi 接入点信息（ESSID、信道、BSSID、安全类型、WPS、客户端列表）
- `Station`：WiFi 客户端信息
- `AirTag`：AirTag/FindMy 追踪器信息
- `BleDevice`：BLE 设备信息
- `PineScanTracker`：Pineapple 检测追踪器
- `MultiSSIDTracker`：多 SSID 检测追踪器

**关键方法：**

| 方法 | 说明 |
|------|------|
| `RunSetup()` | 初始化 WiFi/BT 栈 |
| `main(currentTime)` | 主循环调度 |
| `StartScan(scan_mode)` | 启动指定扫描模式 |
| `StopScan(scan_mode)` | 停止扫描 |
| `channelHop()` | 信道跳频 |
| `RunAPScan()` | 运行 AP 扫描 |
| `RunBeaconScan()` | 运行信标嗅探 |
| `RunProbeScan()` | 运行探测请求嗅探 |
| `RunEapolScan()` | 运行 PMKID 扫描 |
| `RunDeauthScan()` | 运行 Deauth 嗅探 |
| `RunPacketMonitor()` | 运行数据包监控 |
| `RunBluetoothScan()` | 运行 BLE 扫描 |
| `RunSourApple()` | 运行 Sour Apple 攻击 |
| `RunSwiftpairSpam()` | 运行 SwiftPair 攻击 |
| `RunEvilPortal()` | 运行 Evil Portal |
| `RunPineScan()` | 运行 Pineapple 检测 |
| `RunMultiSSIDScan()` | 运行多 SSID 检测 |
| `startWiFi(ssid, pass)` | 连接 WiFi 网络 |
| `shutdownWiFi()` | 关闭 WiFi |
| `shutdownBLE()` | 关闭 BLE |
| `sendDeauthFrame()` | 发送 Deauth 帧 |
| `broadcastSetSSID()` | 广播指定 SSID 信标 |
| `wigleUpload()` | 上传到 Wigle.net |
| `wdgwarsUpload()` | 上传到 WDG Wars |
| `addSSID()` | 添加 SSID 到列表 |
| `generateSSIDs()` | 生成随机 SSID |
| `RunGPSInfo()` | 获取 GPS 信息 |
| `tagPOI()` | 标记 GPS POI |
| `pingScan()` | Ping 扫描 |
| `portScan()` | 端口扫描 |
| `fullARP()` | ARP 扫描 |
| `runFoxHunt()` | 蓝牙 Fox Hunt |

**WiFi 嗅探回调函数：**
- `beaconSnifferCallback()` - 信标帧处理
- `apSnifferCallbackFull()` - AP 帧处理
- `eapolSnifferCallback()` - EAPOL 帧处理
- `wifiSnifferCallback()` - 通用 WiFi 帧处理
- `pineScanSnifferCallback()` - Pineapple 检测帧处理
- `multiSSIDSnifferCallback()` - 多 SSID 检测帧处理

---

### 4.4 CommandLine - 串行命令行接口：[CommandLine.h](file:///workspace/esp32_marauder/CommandLine.h)

**职责：** 为设备提供完整的串行命令行接口，支持所有 WiFi/蓝牙操作的远程控制。

**命令分类：**

**管理命令：**
| 命令 | 说明 |
|------|------|
| `channel -s <ch>` | 设置 WiFi 信道 |
| `clearlist -a/-c/-s` | 清除 AP/客户端/SSID 列表 |
| `reboot` | 重启设备 |
| `update -s/-w` | SD 卡/Web 更新 |
| `help` | 显示帮助 |
| `settings -s <setting> enable/disable` | 修改设置 |
| `ls <directory>` | 列出 SD 卡文件 |
| `led -s <hex>/-p <rainbow>` | 设置 LED 颜色 |
| `gpsdata` | 显示 GPS 数据 |
| `gps -t/-g <属性>` | 查询 GPS 信息 |
| `gpspoi -s/-m/-e` | GPS POI 管理 |
| `gpstracker -c start/stop` | GPS 追踪 |
| `brightness -c/-s` | 屏幕亮度控制 |

**WiFi 嗅探/扫描命令：**
| 命令 | 说明 |
|------|------|
| `evilportal -c start/-w html` | Evil Portal 控制 |
| `scanall` | 全量扫描 |
| `sniffraw` | 原始抓包 |
| `sniffbeacon` | 信标嗅探 |
| `sniffprobe` | 探测请求嗅探 |
| `sniffpwn` | Pwnagotchi 探测 |
| `sniffpinescan` | Pineapple 检测 |
| `sniffmultissid` | 多 SSID 检测 |
| `sniffdeauth` | Deauth 嗅探 |
| `sniffpmkid -c <ch> -d -l` | PMKID 扫描 |
| `stopscan -f` | 停止扫描 |
| `wardrive` | Wardriving |
| `pingscan` | Ping 扫描 |
| `portscan -a/-s` | 端口扫描 |
| `arpscan -f` | ARP 扫描 |
| `mactrack` | MAC 跟踪 |
| `sniffsae` | SAE 嗅探 |
| `foxhunt -b/-w` | Fox Hunt |

**WiFi 攻击命令：**
| 命令 | 说明 |
|------|------|
| `attack -t deauth -c` | Deauth 攻击 |
| `attack -t beacon -l/-r/-a` | 信标攻击 |
| `attack -t probe` | 探测洪水攻击 |
| `attack -t rickroll` | RickRoll 攻击 |
| `attack -t badmsg -c` | BadMsg 攻击 |
| `attack -t sleep -c` | 睡眠攻击 |
| `attack -t sae` | SAE 攻击 |
| `attack -t csa` | CSA 攻击 |
| `attack -t quiet` | Quiet 攻击 |

**蓝牙命令：**
| 命令 | 说明 |
|------|------|
| `sniffbt -t airtag/flipper/flock/meta` | 蓝牙嗅探 |
| `blespam -t sourapple/applejuice/google/samsung/windows/flipper/all` | 蓝牙垃圾信息 |
| `spoofat -t <index>` | 伪装 AirTag |
| `sniffskim` | 刷卡器检测 |

**WiFi 辅助命令：**
| 命令 | 说明 |
|------|------|
| `list -a/-s/-c/-t/-i/-p/-b` | 列出 AP/SSID/客户端/终端/信息/Pineapple/BLE |
| `info -a <index>` | AP 详细信息 |
| `select -a/-s/-c <index>` | 选择 AP/SSID/客户端 |
| `ssid -a -g <count>/-n <name>` | 添加 SSID / 生成 SSID |
| `save -a/-s` | 保存 AP/SSID 列表 |
| `load -a/-s` | 加载 AP/SSID 列表 |
| `join -a <index> -p <password>` | 加入 WiFi 网络 |
| `randapmac` / `randstamac` | 随机生成 MAC 地址 |
| `cloneapmac -a <index>` | 克隆 AP MAC |
| `upload -d wdg/wigle/both` | 上传扫描数据 |

**关键方法：**

| 方法 | 说明 |
|------|------|
| `RunSetup()` | 初始化 CLI，显示欢迎信息 |
| `main(currentTime)` | 主循环，读取串口输入 |
| `runCommand(input)` | 解析并执行命令 |
| `parseCommand(input, delim)` | 命令解析为链表 |
| `argSearch(cmd_args, key)` | 参数搜索 |
| `filterAccessPoints(filter)` | 按关键字过滤 AP |
| `startScanFromCLI()` | 从 CLI 启动扫描 |

---

### 4.5 EvilPortal - 强制门户：[EvilPortal.h](file:///workspace/esp32_marauder/EvilPortal.h)

**职责：** 实现强制门户（Captive Portal）功能，可用于 WiFi 钓鱼安全测试。

**核心数据结构：**
- `ssid`：SSID 条目（ESSID、信道、BSSID、选中状态）
- `AccessPoint`：接入点信息（ESSID、信道、BSSID、安全类型、WPS、客户端列表、制造商）
- `CaptiveRequestHandler`：捕获所有 HTTP 请求的异步处理器

**关键方法：**

| 方法 | 说明 |
|------|------|
| `setup()` | 初始化 EvilPortal，从 SD 卡加载 HTML |
| `begin(ssids, access_points)` | 启动强制门户 AP |
| `main(scan_mode)` | 主循环处理 |
| `setHtml()` | 从 SD 卡设置 HTML 内容 |
| `setAP(essid)` | 设置模拟 AP 的 SSID |
| `startPortal()` | 启动 DNS 重定向和 Web 服务器 |
| `setHtmlFromSerial()` | 通过串口接收 HTML |
| `get_user_name()` | 获取捕获的用户名 |
| `get_password()` | 获取捕获的密码 |
| `cleanup()` | 清理资源 |

**工作原理：**
1. 创建一个与目标 AP 同名或通用的 WiFi 热点
2. 启动 DNS 服务器，将所有 DNS 请求重定向到本地 IP
3. 启动异步 Web 服务器，对所有 HTTP 请求返回自定义 HTML 页面
4. 通过 POST 请求收集用户输入的用户名和密码
5. 通过串口回传捕获的凭据

---

### 4.6 MenuFunctions - 菜单系统：[MenuFunctions.h](file:///workspace/esp32_marauder/MenuFunctions.h)

**职责：** 管理所有屏幕菜单的显示和交互。

**核心数据结构：**
- `MenuNode`：菜单节点（名称、是否为命令、颜色、图标、选中状态、回调函数）
- `Menu`：完整菜单（名称、节点链表、父菜单、当前选中索引）

**菜单层级结构：**
```
mainMenu
├── wifiMenu
│   ├── wifiSnifferMenu (嗅探器)
│   │   ├── 探测请求嗅探
│   │   ├── 信标嗅探
│   │   ├── Deauth 嗅探
│   │   ├── 数据包监视器
│   │   ├── EAPOL/PMKID 扫描
│   │   ├── 检测 Pwnagotchi
│   │   ├── 检测 Espressif
│   │   ├── 检测 Pineapple
│   │   ├── 检测多 SSID
│   │   └── 原始抓包
│   ├── wifiScannerMenu (扫描器)
│   │   ├── 扫描 AP
│   │   ├── 扫描终端
│   │   └── 信号强度分析
│   ├── wifiAttackMenu (攻击)
│   │   ├── 信标列表攻击
│   │   ├── 随机信标攻击
│   │   ├── RickRoll 信标
│   │   ├── 趣味信标
│   │   ├── 探测请求洪水
│   │   ├── Deauth 洪水
│   │   ├── 定向 Deauth
│   │   ├── AP 克隆攻击
│   │   ├── BadMsg 攻击
│   │   ├── 睡眠攻击
│   │   ├── SAE 攻击
│   │   ├── CSA 攻击
│   │   └── Quiet 攻击
│   └── wifiGeneralMenu (通用)
│       ├── 加入 WiFi
│       ├── WiFi 扫描/网络扫描
│       ├── Evil Portal
│       ├── Wardriving
│       ├── SSID 管理
│       ├── MAC 管理
│       └── 设置
├── bluetoothMenu
│   ├── bluetoothSnifferMenu (蓝牙嗅探)
│   │   ├── 蓝牙嗅探
│   │   ├── 检测刷卡器
│   │   ├── AirTag 检测
│   │   ├── Flock 相机检测
│   │   ├── Meta 设备检测
│   │   └── Fox Hunt
│   └── bluetoothAttackMenu (蓝牙攻击)
│       ├── Sour Apple
│       ├── AppleJuice
│       ├── SwiftPair 垃圾信息
│       ├── Samsung BLE 垃圾信息
│       ├── Google BLE 垃圾信息
│       ├── Windows BLE 垃圾信息
│       └── 全量 BLE 垃圾信息
├── gpsMenu (GPS)
│   ├── GPS 信息
│   ├── GPS 追踪
│   ├── Wardriving
│   └── POI 管理
├── badusbMenu (BadUSB)
│   ├── 测试 BadUSB
│   └── 运行 Ducky 脚本
└── deviceMenu (设备)
    ├── 设备信息
    ├── 设置
    ├── 通用应用
    ├── 更新
    ├── 重启
    └── 关机
```

**关键方法：**

| 方法 | 说明 |
|------|------|
| `RunSetup()` | 构建菜单树 |
| `main(currentTime)` | 主循环，处理按键/触摸输入 |
| `changeMenu(menu)` | 切换当前菜单 |
| `displayCurrentMenu()` | 渲染当前菜单 |
| `buildButtons()` | 构建菜单按钮 |
| `updateStatusBar()` | 更新状态栏（电量/SD/WiFi/GPS 图标） |
| `drawGraph()` | 绘制图表（信号强度/信道活动） |
| `drawStatusBar()` | 绘制状态栏 |
| `miniKeyboard()` | 迷你键盘输入（小型屏幕） |
| `battery()` | 更新电池图标 |
| `buttonSelected()` / `buttonNotSelected()` | 按钮选中/取消选中渲染 |

---

### 4.7 Display - 显示驱动：[Display.h](file:///workspace/esp32_marauder/Display.h)

**职责：** 封装 TFT_eSPI 库，管理屏幕渲染、触摸输入和显示缓冲区。

**关键特性：**
- 支持多种 TFT 控制器（ILI9341、ST7789、ST7796）
- 触摸屏支持（XPT2046 电阻式、FT6336 电容式）
- 屏幕缓冲区（滚动显示文本）
- 图形化频段分析（包监控器）
- 横幅（Banner）动画

**关键方法：**

| 方法 | 说明 |
|------|------|
| `RunSetup()` | 初始化 TFT 和触摸屏 |
| `init()` | 初始化 SPI 和显示 |
| `menuButton()` | 检测菜单按钮触摸 |
| `updateTouch()` | 更新触摸坐标 |
| `isTouchHeld()` | 检测触摸长按 |
| `tftDrawGraphObjects()` | 绘制图表对象 |
| `tftDrawColorKey()` | 绘制颜色图例 |
| `tftDrawXScaleButtons()` / `tftDrawYScaleButtons()` | 绘制缩放按钮 |
| `tftDrawChannelScaleButtons()` | 绘制信道选择按钮 |
| `tftDrawChanHopButton()` | 绘制信道跳转按钮 |
| `buildBanner()` | 构建横幅文字 |
| `clearScreen()` | 清屏 |
| `displayBuffer()` | 显示缓冲区内容 |
| `showCenterText()` | 居中显示文本 |
| `touchToExit()` | 触摸退出显示 |
| `twoPartDisplay()` | 双区域显示 |
| `updateBanner()` | 更新横幅 |
| `setCalData()` | 设置触摸校准数据 |

---

### 4.8 SDInterface - SD 卡接口：[SDInterface.h](file:///workspace/esp32_marauder/SDInterface.h)

**职责：** 管理 SD 卡文件系统操作和固件 OTA 更新。

**关键方法：**

| 方法 | 说明 |
|------|------|
| `initSD()` | 初始化 SD 卡 |
| `listDir(str_dir)` | 列出目录内容 |
| `listDirToLinkedList()` | 列出目录到链表 |
| `getFile(path)` | 获取文件对象 |
| `runUpdate(file_name)` | 从 SD 卡执行 OTA 更新 |
| `performUpdate(stream, size)` | 执行固件更新写入 |
| `removeFile(file_path)` | 删除文件 |

**OTA 更新流程：**
1. 检查 `update.bin` 文件是否存在
2. 打开文件并验证大小
3. 使用 `Update` 库写入分区
4. 完成后重启设备

**注意：** 对于 C5 和部分触摸屏设备，SD 卡使用独立 SPI 总线，通过 `SPIClass` 参数传递。

---

### 4.9 Buffer - 双缓冲写入：[Buffer.h](file:///workspace/esp32_marauder/Buffer.h)

**职责：** 实现双缓冲 PCAP/日志文件写入机制，避免数据丢失。

**关键方法：**

| 方法 | 说明 |
|------|------|
| `pcapOpen(file_name, fs, serial)` | 打开 PCAP 文件写入 |
| `logOpen(file_name, fs, serial)` | 打开日志文件写入 |
| `gpxOpen(file_name, fs, serial)` | 打开 GPX 文件写入 |
| `append(packet, len)` | 追加 PCAP 数据包 |
| `append(log)` | 追加日志文本 |
| `save()` | 刷新缓冲区到 SD 卡/串口 |

**工作原理：** 使用两个缓冲区（bufA/bufB），一个用于接收数据，另一个用于写入 SD 卡。当写入缓冲区满时自动切换，避免数据丢失。

---

### 4.10 Settings - 持久化设置：[settings.h](file:///workspace/esp32_marauder/settings.h)

**职责：** 管理设备设置的持久化存储（SPIFFS + JSON）。

**设置项：**

| 设置键 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `ForcePMKID` | bool | false | 强制 PMKID 捕获 |
| `ForceProbe` | bool | false | 强制探测请求 |
| `SavePCAP` | bool | true | 保存 PCAP 文件 |
| `EnableLED` | bool | true | 启用 LED |
| `EPDeauth` | bool | false | Evil Portal Deauth |
| `ChanHop` | bool | false | 信道跳频 |
| `ClientSSID` | String | "" | 客户端 WiFi SSID |
| `ClientPW` | String | "" | 客户端 WiFi 密码 |
| `wdg_key` | String | "" | WDG Wars API 密钥 |

**关键方法：**

| 方法 | 说明 |
|------|------|
| `begin()` | 从 SPIFFS 加载设置 |
| `loadSetting<T>(key)` | 读取设置值（模板） |
| `saveSetting<T>(key, value)` | 保存设置值（模板） |
| `toggleSetting(key)` | 切换布尔设置 |
| `getSettingType(key)` | 获取设置类型（用于验证） |
| `createDefaultSettings(fs)` | 创建默认设置 |
| `getSettingsString()` | 获取完整 JSON 设置字符串 |
| `printJsonSettings()` | 打印 JSON 设置 |

**内部缓存机制：** 使用 `SettingsCache` 结构体在内存中缓存所有设置值，避免每次读取都解析 JSON。`begin()` 时一次性解析 JSON 填充缓存，`saveSetting()` 同时更新缓存和 SPIFFS。

---

### 4.11 BatteryInterface - 电池管理：[BatteryInterface.h](file:///workspace/esp32_marauder/BatteryInterface.h)

**职责：** 统一管理多种电池/电源管理芯片的接口。

**支持的芯片：**

| 芯片 | 宏 | 设备 |
|------|------|------|
| AXP192 | `HAS_AXP192` | M5StickC |
| IP5306 | `HAS_IP5306` | V4/V6/V7/Kit |
| AXP2101 | `HAS_AXP2101` | M5StickC Plus2 |
| MAX17048 | `HAS_MAX1704X` | Rev Feather, Pancake |
| ADC 直读 | `BATTERY_ADC_PIN` | Cardputer ADV |
| TP4057 | `HAS_TP4057` | M5StickC Plus2 |

**关键方法：**

| 方法 | 说明 |
|------|------|
| `RunSetup()` | 初始化对应芯片的 I2C 通信 |
| `main(currentTime)` | 定期更新电量 |
| `getBatteryLevel()` | 获取电量百分比 (0-100) |

---

### 4.12 GpsInterface - GPS 接口：[GpsInterface.h](file:///workspace/esp32_marauder/GpsInterface.h)

**职责：** 管理 GPS 模块的 NMEA 数据解析和位置信息获取。

**关键方法：**

| 方法 | 说明 |
|------|------|
| `begin()` | 初始化 GPS 串口通信 |
| `main()` | 主循环，读取 GPS 数据 |
| `getFixStatus()` | 获取定位状态 |
| `getNumSats()` | 获取卫星数量 |
| `getLat()` / `getLon()` | 获取经纬度（字符串） |
| `getLatInt()` / `getLonInt()` | 获取经纬度（整数，微度） |
| `getAlt()` | 获取海拔高度 |
| `getAccuracy()` | 获取定位精度 |
| `getDatetime()` | 获取日期时间 |
| `getNmea()` | 获取原始 NMEA 数据 |
| `sendSentence()` | 发送配置指令到 GPS 模块 |
| `enqueue()` | NMEA 句子入队 |
| `generateGXgga()` / `generateGXrmc()` | 生成 GPS 语句 |

**GPS 类型支持：** 原生、GPS、GLONASS、Galileo、NAVIC、QZSS、北斗

---

### 4.13 LED 控制模块

**四种 LED 实现：**

| 类 | 文件 | 适用平台 |
|----|------|----------|
| `LedInterface` | [LedInterface.h](file:///workspace/esp32_marauder/LedInterface.h) | NeoPixel LED（大部分硬件） |
| `flipperLED` | [flipperLED.h](file:///workspace/esp32_marauder/flipperLED.h) | Flipper Zero RGB LED（R/G/B 三引脚） |
| `stickcLED` | [stickcLED.h](file:///workspace/esp32_marauder/stickcLED.h) | M5StickC 内置 LED |
| `xiaoLED` | [xiaoLED.h](file:///workspace/esp32_marauder/xiaoLED.h) | XIAO ESP32S3 内置 LED |

**LED 模式：**

| 模式 | 值 | 说明 |
|------|-----|------|
| `MODE_OFF` | 0 | 关闭 |
| `MODE_RAINBOW` | 1 | 彩虹循环 |
| `MODE_ATTACK` | 2 | 攻击模式（红色/闪烁） |
| `MODE_SNIFF` | 3 | 嗅探模式（蓝色） |
| `MODE_CUSTOM` | 4 | 自定义颜色 |

---

### 4.14 Switches - 按键去抖：[Switches.h](file:///workspace/esp32_marauder/Switches.h)

**关键方法：**

| 方法 | 说明 |
|------|------|
| `justPressed()` | 检测按键刚按下 |
| `justReleased()` | 检测按键刚释放 |
| `isHeld()` | 检测按键长按 |

---

### 4.15 Keyboard - 键盘输入：[Keyboard.h](file:///workspace/esp32_marauder/Keyboard.h)

**职责：** M5 Cardputer 和 Cardputer ADV 的物理键盘驱动。

**Cardputer 键盘矩阵：** 7 输入引脚 × 3 输出引脚 = 最大 21 键（实际标准 4 行 × 14 列）

**Cardputer ADV 键盘：** 使用 TCA8418 I2C 键盘矩阵芯片

**关键方法：**

| 方法 | 说明 |
|------|------|
| `begin()` | 初始化键盘引脚 |
| `isPressed()` | 检测当前按下的键数量 |
| `isKeyPressed(char)` | 检查特定键是否被按下 |
| `getPressedKeysString()` | 获取按下的键字符串 |
| `updateKeyList()` | 扫描键盘矩阵 |
| `updateKeysState()` | 更新按键状态（修饰键处理） |

---

### 4.16 TouchKeyboard - 触摸键盘：[TouchKeyboard.h](file:///workspace/esp32_marauder/TouchKeyboard.h)

**关键函数：**

```cpp
bool keyboardInput(char *buffer, size_t bufLen, const char *title = nullptr);
```

在触摸屏上显示虚拟键盘，支持大小写切换、布局切换，返回用户输入。

---

### 4.17 语言支持：[lang_var.h](file:///workspace/esp32_marauder/lang_var.h)

**职责：** 提供中文本地化字符串表，所有界面文本通过 `text_table` 数组索引引用。

- `text_table0`：启动窗口文本
- `text_table1`：菜单函数文本
- `text_table2`：SD 接口文本
- `text_table3`：Web 更新文本
- `text_table4`：WiFi 扫描文本

---

### 4.18 工具函数：[utils.h](file:///workspace/esp32_marauder/utils.h)

**关键函数：**

| 函数 | 说明 |
|------|------|
| `getDRAMUsagePercent()` | 获取 DRAM 使用率 |
| `getPSRAMUsagePercent()` | 获取 PSRAM 使用率 |
| `macToString()` | MAC 地址 → 字符串 |
| `convertMacStringToUint8()` | 字符串 → MAC 地址 |
| `generateRandomMac()` | 生成随机 MAC 地址 |
| `generateRandomName()` | 生成随机名称 |
| `rssiToMenuColor()` | RSSI → 菜单颜色 |
| `rssiToColorScaled()` | RSSI → RGB565 颜色 |
| `hexDump()` | 十六进制转储 |
| `base64Encode()` | Base64 编码 |
| `getNextIP()` / `getPrevIP()` | IP 地址上下遍历 |

---

## 5. 外部库依赖

| 库 | 版本 | 用途 |
|----|------|------|
| **TFT_eSPI** | 2.5.34 / ESP32-C5 fork | 显示屏驱动 |
| **NimBLE-Arduino** | 1.3.8 / 2.3.8 | BLE 蓝牙栈 |
| **ESPAsyncWebServer** | v3.8.1 | Evil Portal 异步 Web 服务器 |
| **AsyncTCP** | v3.4.8 | TCP 异步通信 |
| **ArduinoJson** | v6.18.2 | JSON 解析（设置存储） |
| **MicroNMEA** | v2.0.6 | GPS NMEA 数据解析 |
| **LinkedList** | v1.3.3 | 链表数据结构 |
| **Adafruit_NeoPixel** | 1.12.0 | NeoPixel LED 控制 |
| **ESP32Ping** | 1.6 | ICMP Ping 支持 |
| **XPT2046_Touchscreen** | v1.4 | 电阻式触摸屏驱动 |
| **lv_arduino** | 3.0.0 | LVGL 图形库 |
| **JPEGDecoder** | 1.8.0 | JPEG 图片解码 |
| **EspSoftwareSerial** | 8.1.0 | 软件串口（GPS） |
| **Adafruit_BusIO** | 1.15.0 | I2C/SPI 总线抽象 |
| **Adafruit_MAX1704X** | 1.0.2 | MAX17048 电池电量计 |
| **Adafruit_TCA8418** | 本地 | TCA8418 键盘矩阵芯片 |
| **XPowersLib** | - | AXP2101 电源管理 |
| **DNSServer** | 内置 | Evil Portal DNS 劫持 |

---

## 6. 项目运行方式

### 6.1 构建方式

项目使用 **Arduino CLI** 进行构建，通过 GitHub Actions 自动化构建多个平台。

**本地构建步骤：**

1. 安装 Arduino CLI
2. 安装 ESP32 开发板支持：
   ```bash
   arduino-cli core update-index
   arduino-cli core install esp32:esp32@2.0.11  # 或 3.3.4
   ```
3. 安装所需库（见上方依赖表）
4. 配置 TFT_eSPI：复制对应 `User_Setup_*.h` 到 TFT_eSPI 目录
5. 编译指定平台：
   ```bash
   arduino-cli compile --fqbn esp32:esp32:d32:PartitionScheme=min_spiffs \
     --build-property compiler.cpp.extra_flags='-DMARAUDER_V6' \
     esp32_marauder/esp32_marauder.ino
   ```

### 6.2 烧录方式

**方式一：Python 烧录工具（推荐）**
- `C5_Py_Flasher_for_adapter/c5_flasher.py` - 自动检测端口并烧录
- 自动检测 bootloader、分区表和应用固件
- 自动安装依赖（esptool、pyserial、colorama）

**方式二：esptool 命令行**
```bash
python -m esptool --chip esp32 --port /dev/ttyUSB0 --baud 921600 \
  write_flash -z 0x1000 bootloader.bin 0x8000 partitions.bin 0x10000 firmware.bin
```
- 对于 ESP32-C5：启动地址为 `0x2000`，应用地址为 `0x10000`
- 对于 ESP32-S2/S3：启动地址为 `0x1000`

**方式三：M5 Burner**
- M5Cardputer 可通过 M5 Burner 直接烧录

**方式四：Web 更新**
- 设备启动后，可通过 Web 界面进行 OTA 固件更新

**方式五：SD 卡更新**
- 将 `update.bin` 放入 SD 卡根目录，通过菜单选择 SD 卡更新

---

## 7. CI/CD 构建系统

配置文件：[build_parallel.yml](file:///workspace/.github/workflows/build_parallel.yml)

**构建矩阵：** 约 23 个硬件平台并行构建

**构建流程：**
1. 检出代码
2. 安装 Arduino CLI 和 ESP32 核心
3. 安装所有外部库依赖
4. 配置 TFT_eSPI 的 `User_Setup_Select.h`
5. 修改 `platform.txt`（编译器标志适配）
6. 编译指定平台的固件
7. 重命名并上传构建产物
8. 当 workflow_dispatch 触发时，创建 Release 草稿

**触发条件：**
- Push 到 master 分支
- 推送 Tag
- Pull Request
- 手动触发（workflow_dispatch）

---

## 8. 数据流图

```
┌──────────────────────────────────────────────────────────────────┐
│                         数据流概览                                │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐                                                    │
│  │  WiFi    │──→ 信标帧/探测帧/Deauth帧 ──→ 嗅探回调 ──→ 列表    │
│  │  Radio   │──→ EAPOL 帧 ──→ PMKID 提取 ──→ 列表              │
│  │          │──→ 数据包 ──→ PCAP Buffer ──→ SD 卡文件           │
│  └──────────┘                                                    │
│                                                                  │
│  ┌──────────┐                                                    │
│  │  BLE     │──→ 广播数据 ──→ 设备列表 ──→ 显示                 │
│  │  Radio   │──→ AirTag 数据 ──→ 追踪器列表                     │
│  └──────────┘                                                    │
│                                                                  │
│  ┌──────────┐                                                    │
│  │  GPS     │──→ NMEA 数据 ──→ MicroNMEA 解析 ──→ 坐标/时间     │
│  │  Module  │──→ Wardriving 数据 ──→ Wigle CSV ──→ SD 卡        │
│  └──────────┘                                                    │
│                                                                  │
│  ┌──────────┐                                                    │
│  │  Serial  │──→ CLI 命令 ──→ CommandLine 解析 ──→ 功能执行     │
│  │  (USB)   │←── 输出/日志 ──→ 串口回显                         │
│  └──────────┘                                                    │
│                                                                  │
│  ┌──────────┐                                                    │
│  │  SD Card │←── PCAP 写入 / 日志写入 / Wigle CSV 写入          │
│  │          │──→ 固件更新读取 / HTML 模板读取 / 设置加载          │
│  └──────────┘                                                    │
│                                                                  │
│  ┌──────────┐                                                    │
│  │  SPIFFS  │←── JSON 设置保存 ──→ JSON 设置加载                │
│  └──────────┘                                                    │
│                                                                  │
│  ┌──────────┐                                                    │
│  │  Evil    │──→ DNS 劫持 ──→ 强制门户页面                      │
│  │  Portal  │←── HTTP POST ──→ 凭据收集 ──→ 串口回显            │
│  └──────────┘                                                    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 9. 关键设计模式与注意事项

### 9.1 条件编译架构
整个项目使用大量 `#ifdef` / `#if defined()` 宏来支持 30+ 种硬件平台。`configs.h` 是核心枢纽，通过单一平台宏（如 `MARAUDER_V6`）自动推导出所有硬件特性宏（`HAS_SCREEN`、`HAS_BATTERY` 等）。

### 9.2 全局对象模式
所有核心模块使用全局对象（在 `esp32_marauder.ino` 中定义，通过 `extern` 在其他模块中引用），避免复杂的依赖注入。

### 9.3 双缓冲写入
`Buffer` 类使用双缓冲区（bufA/bufB）实现无锁的 PCAP 数据写入，确保在高速数据包捕获时不会丢失数据。

### 9.4 回调驱动架构
WiFi 嗅探功能通过注册 `wifi_promiscuous_cb_t` 回调函数实现，不同的扫描模式使用不同的回调（`beaconSnifferCallback`、`eapolSnifferCallback` 等）。

### 9.5 内存管理
项目运行在资源受限的嵌入式设备上，需要特别注意：
- 有 PSRAM 的设备使用更大的缓冲区（PCAP 8KB vs 3KB）
- 无 PSRAM 的设备限制 HTML 大小（11400 字节）
- MAC 历史记录长度根据 PSRAM 调整（500 vs 100）
- 内存下限检查（`MEM_LOWER_LIM` 10000 字节）

### 9.6 多芯片支持
- **ESP32**：主力平台，Arduino-ESP32 2.0.11 或 3.3.4
- **ESP32-S2**：用于 Flipper Zero 开发板
- **ESP32-S3**：用于 Multiboard S3、Cardputer
- **ESP32-C5**：双频支持（2.4GHz + 5GHz），使用 3.3.4 核心
- **ESP32-C6**：用于 M5 Nano C6

---

## 10. 版本历史

| 版本 | 日期 | 主要变更 |
|------|------|----------|
| v0.1 | 2019-12 | 初始版本 |
| v0.3.0 | 2020-01 | 引入 WiFi 扫描 |
| v0.4.0 | 2020-01 | 添加 Deauth 功能 |
| v0.5.0 | 2020-03 | 添加信标攻击 |
| v0.6.0 | 2020-03 | 添加 PMKID 捕获 |
| v0.7.0 | 2020-07 | 添加蓝牙支持 |
| v0.8.0 | 2020-08 | 新旧硬件分叉 |
| v0.9.0 | 2021-05 | 重大重构 |
| v0.9.6 | 2022-05 | Flipper Zero 支持 |
| v0.9.13 | 2022-08 | 多平台支持 |
| v1.0.0 | 2024-06 | 稳定版本，多平台统一 |
| v1.14.0 | 最新 | 当前版本 |

---

*本文档由自动化 Code Wiki 生成器基于项目源代码分析生成。*