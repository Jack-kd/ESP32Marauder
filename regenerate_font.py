#!/usr/bin/env python3
"""
Regenerate Chinese font with dense encoding.
Maps CJK characters to contiguous indices after ASCII to keep the glyph table small.
"""
from PIL import Image, ImageDraw, ImageFont
import re, os

FONT_SIZE = 12
FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
OUTPUT_FILE = "esp32_marauder/chinese_font.h"

source_files = [
    "esp32_marauder/lang_var.h",
    "esp32_marauder/MenuFunctions.cpp",
    "esp32_marauder/WiFiScan.cpp",
    "esp32_marauder/EvilPortal.cpp",
    "esp32_marauder/Display.cpp",
    "esp32_marauder/esp32_marauder.ino",
    "esp32_marauder/CommandLine.cpp",
    "esp32_marauder/TouchKeyboard.cpp",
]

all_chinese = set()
for filepath in source_files:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        for ch in content:
            cp = ord(ch)
            if 0x4E00 <= cp <= 0x9FFF:
                all_chinese.add(ch)
        print(f"  {filepath}: found {len([c for c in content if 0x4E00 <= ord(c) <= 0x9FFF])} CJK chars")

all_chinese = sorted(all_chinese)
print(f"\nTotal unique CJK characters: {len(all_chinese)}")

# ASCII characters (0x20-0x7E)
ascii_chars = [chr(i) for i in range(0x20, 0x7F)]

# Dense encoding: ASCII stays at their code points (0x20-0x7E)
# CJK characters are mapped to 0x7F, 0x80, 0x81, ...
# Create translation table
cjk_to_dense = {}
for i, ch in enumerate(all_chinese):
    cjk_to_dense[ord(ch)] = 0x7F + i

# Render characters at their dense code points
all_chars = ascii_chars + all_chinese
dense_codes = list(range(0x20, 0x7F)) + [0x7F + i for i in range(len(all_chinese))]

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
all_bitmap = bytearray([0x00])

for ch, dc in zip(all_chars, dense_codes):
    result = render_char(ch, font)
    if result[0] is not None:
        bm, w, h = result
        offset = len(all_bitmap)
        glyph_data[dc] = (offset, w, h)
        all_bitmap.extend(bm)

min_cp = 0x20
max_cp = 0x7F + len(all_chinese) - 1
range_size = max_cp - min_cp + 1  # 95 ASCII + N CJK

print(f"Dense range: U+{min_cp:04X} to U+{max_cp:04X} ({range_size} entries)")
print(f"Bitmap data: {len(all_bitmap)} bytes ({len(all_bitmap)/1024:.1f} KB)")
glyph_table_bytes = range_size * 7  # GFXglyph is 7 bytes
print(f"Glyph table: {glyph_table_bytes} bytes ({glyph_table_bytes/1024:.1f} KB)")
total = len(all_bitmap) + glyph_table_bytes + 12
print(f"Total PROGMEM: {total} bytes ({total/1024:.1f} KB)")

# Build translation table (sorted array of Unicode code points)
translation = []
for i, ch in enumerate(all_chinese):
    translation.append((ord(ch), 0x7F + i))

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write('// Auto-generated Chinese GFX font for TFT_eSPI (dense encoding)\n')
    f.write(f'// {len(all_chars)} characters, ASCII (0x20-0x7E) + CJK (0x7F-0x{max_cp:04X})\n')
    f.write(f'// Total PROGMEM: {total} bytes ({total/1024:.1f} KB)\n')
    f.write(f'// Font size: {FONT_SIZE}px\n')
    f.write('#pragma once\n\n')
    f.write('#include <TFT_eSPI.h>\n\n')

    f.write(f'// Bitmap data ({len(all_bitmap)} bytes)\n')
    f.write('PROGMEM const uint8_t chinese_font_bitmap[] = {\n')
    for i in range(0, len(all_bitmap), 16):
        chunk = all_bitmap[i:i+16]
        f.write('  ' + ', '.join(f'0x{b:02X}' for b in chunk) + ',\n')
    f.write('};\n\n')

    f.write(f'// Glyph table ({range_size} entries, dense encoding)\n')
    f.write('PROGMEM const GFXglyph chinese_font_glyphs[] = {\n')
    for cp in range(min_cp, max_cp + 1):
        if cp in glyph_data:
            off, w, h = glyph_data[cp]
            if cp < 0x7F:
                ch_repr = chr(cp)
                f.write(f'  {{ {off:5d}, {w:2d}, {h:2d}, {w:2d}, 0, 0 }}, // U+{cp:04X} \'{ch_repr}\'\n')
            else:
                # Find the original CJK character
                orig_cp = None
                for oc, dc in cjk_to_dense.items():
                    if dc == cp:
                        orig_cp = oc
                        break
                ch_repr = chr(orig_cp) if orig_cp else '?'
                f.write(f'  {{ {off:5d}, {w:2d}, {h:2d}, {w:2d}, 0, 0 }}, // U+{cp:04X} {ch_repr} (orig U+{orig_cp:04X})\n')
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

    f.write('// CJK translation table: maps Unicode code points to dense font indices\n')
    f.write(f'// {len(translation)} entries, sorted by Unicode code point for binary search\n')
    f.write(f'PROGMEM const uint16_t cjk_translate[][2] = {{\n')
    for orig_cp, dense_cp in translation:
        f.write(f'  {{ 0x{orig_cp:04X}, 0x{dense_cp:04X} }},  // {chr(orig_cp)}\n')
    f.write('};\n')
    f.write(f'#define CJK_TRANSLATE_COUNT {len(translation)}\n\n')

    f.write('// Convert UTF-8 character to dense font index\n')
    f.write('// Returns 0 if character is ASCII, dense index if CJK\n')
    f.write('inline uint16_t cjk_to_font_index(const char* utf8) {\n')
    f.write('  if ((uint8_t)*utf8 < 0x80) return (uint16_t)(uint8_t)*utf8;  // ASCII passthrough\n')
    f.write('  // Decode UTF-8 to Unicode code point\n')
    f.write('  uint32_t cp = 0;\n')
    f.write('  if ((*utf8 & 0xE0) == 0xC0) { cp = ((*utf8 & 0x1F) << 6) | (utf8[1] & 0x3F); }\n')
    f.write('  else if ((*utf8 & 0xF0) == 0xE0) { cp = ((*utf8 & 0x0F) << 12) | ((utf8[1] & 0x3F) << 6) | (utf8[2] & 0x3F); }\n')
    f.write('  else if ((*utf8 & 0xF8) == 0xF0) { cp = ((*utf8 & 0x07) << 18) | ((utf8[1] & 0x3F) << 12) | ((utf8[2] & 0x3F) << 6) | (utf8[3] & 0x3F); }\n')
    f.write('  // Binary search in translation table\n')
    f.write('  int lo = 0, hi = CJK_TRANSLATE_COUNT - 1;\n')
    f.write('  while (lo <= hi) {\n')
    f.write('    int mid = (lo + hi) / 2;\n')
    f.write('    uint16_t mc = pgm_read_word(&cjk_translate[mid][0]);\n')
    f.write('    if (cp == mc) return pgm_read_word(&cjk_translate[mid][1]);\n')
    f.write('    if (cp < mc) hi = mid - 1;\n')
    f.write('    else lo = mid + 1;\n')
    f.write('  }\n')
    f.write('  return 0;  // Not found\n')
    f.write('}\n\n')

    f.write('// Print a UTF-8 string using the Chinese font with CJK translation\n')
    f.write('inline void printChinese(TFT_eSPI& _tft, const char* str) {\n')
    f.write('  _tft.setFreeFont(&chinese_font);\n')
    f.write('  while (*str) {\n')
    f.write('    if ((uint8_t)*str < 0x80) {\n')
    f.write('      _tft.write(*str++);\n')
    f.write('    } else {\n')
    f.write('      uint16_t idx = cjk_to_font_index(str);\n')
    f.write('      if (idx) _tft.write(idx);\n')
    f.write('      // Skip UTF-8 bytes\n')
    f.write('      if ((*str & 0xE0) == 0xC0) str += 2;\n')
    f.write('      else if ((*str & 0xF0) == 0xE0) str += 3;\n')
    f.write('      else if ((*str & 0xF8) == 0xF0) str += 4;\n')
    f.write('      else str++;\n')
    f.write('    }\n')
    f.write('  }\n')
    f.write('  _tft.setFreeFont(NULL);\n')
    f.write('}\n\n')

    f.write('// Calculate pixel width of a UTF-8 string when rendered with Chinese font\n')
    f.write('inline int chineseStringWidth(const char* str) {\n')
    f.write('  int w = 0;\n')
    f.write('  for (const char* p = str; *p; ) {\n')
    f.write('    if ((uint8_t)*p < 0x80) { w += 8; p++; }\n')
    f.write('    else { w += 12; while ((*++p & 0xC0) == 0x80); }\n')
    f.write('  }\n')
    f.write('  return w;\n')
    f.write('}\n\n')

    f.write('// Draw a centred Chinese string (replaces drawCentreString for CJK text)\n')
    f.write('inline void drawCentreStringChinese(TFT_eSPI& _tft, const char* str, int x, int y) {\n')
    f.write('  int w = chineseStringWidth(str);\n')
    f.write('  _tft.setCursor(x - w / 2, y);\n')
    f.write('  printChinese(_tft, str);\n')
    f.write('}\n\n')

    f.write('// Draw a Chinese button (replaces drawButton for CJK labels)\n')
    f.write('inline void drawChineseButton(TFT_eSPI& _tft, int x, int y, int w, int h, const char* label, uint16_t outline, uint16_t fill, uint16_t textcolor) {\n')
    f.write('  _tft.fillRoundRect(x, y, w, h, 4, fill);\n')
    f.write('  _tft.drawRoundRect(x, y, w, h, 4, outline);\n')
    f.write('  int lw = chineseStringWidth(label);\n')
    f.write('  _tft.setTextColor(textcolor);\n')
    f.write('  _tft.setCursor(x + (w - lw) / 2, y + (h - 14) / 2);\n')
    f.write('  printChinese(_tft, label);\n')
    f.write('}\n\n')

    f.write('// Helper macros\n')
    f.write('extern TFT_eSPI tft;\n')
    f.write('#define setChineseFont() tft.setFreeFont(&chinese_font)\n')
    f.write('#define setEnglishFont()  tft.setFreeFont(MENU_FONT)\n')
    f.write('#define setDefaultFont()  tft.setFreeFont(NULL)\n')

print(f"\nFont regenerated: {OUTPUT_FILE}")