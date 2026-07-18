#!/usr/bin/env python3
"""
Generate a TFT_eSPI GFX font file for Chinese characters.
Creates a proper GFXfont that works with tft.drawString, drawCentreString, drawButton, etc.

The font covers the Unicode range of the Chinese characters used in translations.
Unused code points get zero-width glyphs to save bitmap space.
"""

from PIL import Image, ImageDraw, ImageFont
import os

FONT_SIZE = 15  # Font size in pixels
FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
OUTPUT_FILE = "esp32_marauder/chinese_font.h"

def collect_chars(translations):
    """Collect all unique Chinese characters from translations."""
    chars = set()
    for _, text in translations:
        for ch in text:
            cp = ord(ch)
            # CJK Unified Ideographs
            if 0x4E00 <= cp <= 0x9FFF:
                chars.add(ch)
            # CJK Symbols and Punctuation
            elif 0x3000 <= cp <= 0x303F:
                chars.add(ch)
            # Fullwidth Forms
            elif 0xFF00 <= cp <= 0xFFEF:
                chars.add(ch)
    return sorted(chars)

def render_char(ch, font):
    """Render a single character. Returns (bitmap_list, width, height)."""
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
    
    # Convert to bitmap bytes (1 bit per pixel, MSB first per row)
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

def generate_font(translations):
    """Generate the GFX font C header file."""
    chars = collect_chars(translations)
    
    if not chars:
        print("ERROR: No Chinese characters found!")
        return None
    
    print(f"Unique Chinese characters: {len(chars)}")
    
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    
    # Render all characters
    glyph_data = {}  # codepoint -> (bitmap, width, height)
    all_bitmap = bytearray()
    all_bitmap.append(0x00)  # Empty bitmap byte for zero-width glyphs
    
    for ch in chars:
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
    
    print(f"Unicode range: U+{min_cp:04X} ({chr(min_cp)}) to U+{max_cp:04X} ({chr(max_cp)})")
    print(f"Range size: {range_size} entries")
    print(f"Bitmap data: {len(all_bitmap)} bytes")
    print(f"Glyph table: {range_size * 6} bytes")
    print(f"Total overhead: {len(all_bitmap) + range_size * 6 + 12} bytes")
    
    # Generate C header
    lines = []
    lines.append('// Auto-generated Chinese GFX font for TFT_eSPI')
    lines.append(f'// {len(chars)} unique characters, range U+{min_cp:04X}-U+{max_cp:04X}')
    lines.append('#pragma once')
    lines.append('')
    lines.append('#include <TFT_eSPI.h>')
    lines.append('')
    
    # Bitmap data
    lines.append(f'// Bitmap data ({len(all_bitmap)} bytes)')
    lines.append('PROGMEM const uint8_t chinese_font_bitmap[] = {')
    for i in range(0, len(all_bitmap), 16):
        chunk = all_bitmap[i:i+16]
        lines.append('  ' + ', '.join(f'0x{b:02X}' for b in chunk) + ',')
    lines.append('};')
    lines.append('')
    
    # Glyph table
    lines.append(f'// Glyph table ({range_size} entries)')
    lines.append('PROGMEM const GFXglyph chinese_font_glyphs[] = {')
    
    for cp in range(min_cp, max_cp + 1):
        if cp in glyph_data:
            off, w, h = glyph_data[cp]
            lines.append(f'  {{ {off:5d}, {w:2d}, {h:2d}, {w:2d}, 0, 0 }}, // U+{cp:04X} {chr(cp)}')
        else:
            # Zero-width glyph pointing to empty bitmap
            lines.append(f'  {{     0,  0,  0,  0, 0, 0 }}, // U+{cp:04X} (unused)')
    
    lines.append('};')
    lines.append('')
    
    # Font structure
    lines.append('// Font structure')
    lines.append('const GFXfont chinese_font = {')
    lines.append('  (uint8_t*)chinese_font_bitmap,')
    lines.append('  (GFXglyph*)chinese_font_glyphs,')
    lines.append(f'  0x{min_cp:04X}, 0x{max_cp:04X},')
    lines.append(f'  {FONT_SIZE + 2}')
    lines.append('};')
    lines.append('')
    
    # Helper macros
    lines.append('// Helper macros')
    lines.append('extern TFT_eSPI tft;')
    lines.append('#define setChineseFont() tft.setFreeFont(&chinese_font)')
    lines.append('#define setEnglishFont()  tft.setFreeFont(MENU_FONT)')
    lines.append('#define setDefaultFont()  tft.setFreeFont(NULL)')
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"\nFont generated: {OUTPUT_FILE}")
    return chars

if __name__ == '__main__':
    test = [
        ("t1", "SSID列表"),
        ("t2", "添加SSID"),
        ("t3", "扫描接入点"),
        ("t4", "蓝牙嗅探"),
        ("t5", "取消"),
        ("t6", "设置"),
        ("t7", "返回"),
        ("t8", "保存"),
        ("t9", "退出"),
        ("t10", "重启"),
        ("t11", "攻击"),
        ("t12", "通用"),
        ("t13", "嗅探器"),
        ("t14", "设备信息"),
        ("t15", "固件更新"),
        ("t16", "语言"),
        ("t17", "关"),
        ("t18", "开"),
        ("t19", "加载"),
        ("t20", "另存为"),
        ("t21", "关闭"),
        ("t22", "是"),
        ("t23", "否"),
        ("t24", "频道"),
        ("t25", "已连接"),
        ("t26", "连接失败"),
        ("t27", "正在更新"),
        ("t28", "更新完成"),
    ]
    generate_font(test)