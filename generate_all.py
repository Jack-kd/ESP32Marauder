#!/usr/bin/env python3
"""
Final Chinese font generator for ESP32 Marauder.
Includes both ASCII (0x20-0x7E) and CJK characters in a single font
so that drawString/drawButton/drawCentreString work seamlessly.
"""

from PIL import Image, ImageDraw, ImageFont

FONT_SIZE = 15
FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
OUTPUT_FILE = "esp32_marauder/chinese_font.h"

# Collect all CJK characters from the translations
from translate import LANG_VAR_TRANSLATIONS, HARDCODED_TRANSLATIONS

all_chinese = set()
for text in list(LANG_VAR_TRANSLATIONS.values()) + list(HARDCODED_TRANSLATIONS.values()):
    for ch in text:
        cp = ord(ch)
        if 0x4E00 <= cp <= 0x9FFF:
            all_chinese.add(ch)

all_chinese = sorted(all_chinese)
print(f"Unique CJK characters: {len(all_chinese)}")

# Add ASCII characters (0x20-0x7E)
ascii_chars = [chr(i) for i in range(0x20, 0x7F)]
all_chars = ascii_chars + all_chinese
print(f"Total characters (including ASCII): {len(all_chars)}")

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

for ch in all_chars:
    cp = ord(ch)
    result = render_char(ch, font)
    if result[0] is not None:
        bm, w, h = result
        offset = len(all_bitmap)
        glyph_data[cp] = (offset, w, h)
        all_bitmap.extend(bm)

min_cp = 0x20  # Start from space
max_cp = max(glyph_data.keys())
range_size = max_cp - min_cp + 1

print(f"Unicode range: U+{min_cp:04X} to U+{max_cp:04X}")
print(f"Range size: {range_size} entries")
print(f"Bitmap data: {len(all_bitmap)} bytes")
print(f"Glyph table: {range_size * 6} bytes ({range_size * 6 / 1024:.1f} KB)")
print(f"Total: {len(all_bitmap) + range_size * 6 + 12} bytes ({(len(all_bitmap) + range_size * 6 + 12) / 1024:.1f} KB)")

# Write font
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write('// Auto-generated Chinese GFX font for TFT_eSPI (includes ASCII + CJK)\n')
    f.write(f'// {len(all_chars)} characters, range U+{min_cp:04X}-U+{max_cp:04X}\n')
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
            ch_repr = chr(cp)
            if cp < 0x7F:
                f.write(f'  {{ {off:5d}, {w:2d}, {h:2d}, {w:2d}, 0, 0 }}, // U+{cp:04X} \'{ch_repr}\'\n')
            else:
                f.write(f'  {{ {off:5d}, {w:2d}, {h:2d}, {w:2d}, 0, 0 }}, // U+{cp:04X} {ch_repr}\n')
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

print(f"\nFont written to {OUTPUT_FILE}")