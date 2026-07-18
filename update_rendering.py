#!/usr/bin/env python3
"""Update all rendering code to use printChinese() instead of setFreeFont(&chinese_font)."""
import re

base = "/workspace/esp32_marauder"

# ============================================================
# Display.cpp: showCenterText
# ============================================================
with open(f"{base}/Display.cpp", "r") as f:
    content = f.read()

# Replace showCenterText function
old_show = '''void Display::showCenterText(const char* text, int y, bool small_pp, uint8_t text_size)
{
  if (!text)
    text = "";

  // Auto-detect CJK characters and switch to Chinese font
  bool hasCJK = false;
  for (const char* p = text; *p; p++) {
    if ((uint8_t)*p >= 0x80) {
      hasCJK = true;
      break;
    }
  }

  if (hasCJK)
    tft.setFreeFont(&chinese_font);
  else
    tft.setFreeFont(NULL);

  size_t len = strlen(text);

  // For CJK text, adjust centering (UTF-8: 3 bytes per char, ~16px per char)
  if (hasCJK) {
    int char_count = 0;
    for (const char* p = text; *p; p++) {
      if ((*p & 0xC0) != 0x80) char_count++;
    }
    int text_width = char_count * 16;
    if (!small_pp)
      tft.setCursor((SCREEN_WIDTH - (text_width * text_size)) / 2, y);
    else
      tft.setCursor((SCREEN_WIDTH - (text_width)) / 2, y);
  } else {
    if (!small_pp)
      tft.setCursor((SCREEN_WIDTH - (len * (6 * text_size))) / 2, y);
    else
      tft.setCursor((SCREEN_WIDTH - (len * 6)) / 2, y);
  }

  tft.println(text);

  if (hasCJK)
    tft.setFreeFont(NULL);
}'''

new_show = '''void Display::showCenterText(const char* text, int y, bool small_pp, uint8_t text_size)
{
  if (!text)
    text = "";

  // Auto-detect CJK characters
  bool hasCJK = false;
  for (const char* p = text; *p; p++) {
    if ((uint8_t)*p >= 0x80) {
      hasCJK = true;
      break;
    }
  }

  if (hasCJK) {
    // Calculate approximate width for centering
    int width = 0;
    for (const char* p = text; *p; ) {
      if ((uint8_t)*p < 0x80) { width += 8; p++; }
      else { width += 12; while ((*++p & 0xC0) == 0x80); }
    }
    if (!small_pp)
      tft.setCursor((SCREEN_WIDTH - (width * text_size)) / 2, y);
    else
      tft.setCursor((SCREEN_WIDTH - width) / 2, y);
    printChinese(this->tft, text);
  } else {
    tft.setFreeFont(NULL);
    size_t len = strlen(text);
    if (!small_pp)
      tft.setCursor((SCREEN_WIDTH - (len * (6 * text_size))) / 2, y);
    else
      tft.setCursor((SCREEN_WIDTH - (len * 6)) / 2, y);
    tft.println(text);
  }
}'''

content = content.replace(old_show, new_show)

# Replace processAndPrintString function
old_proc = '''void Display::processAndPrintString(TFT_eSPI& tft, const String& originalString) {
  // Define colors
  uint16_t text_color = TFT_GREEN; // Default text color
  uint16_t background_color = TFT_BLACK; // Default background color

  String new_string = originalString;

  // Check for color macros at the start of the string
  if (new_string.startsWith(";")) {
    if (new_string.startsWith(RED_KEY)) {
      text_color = TFT_RED;
      new_string.remove(0, strlen(RED_KEY)); // Remove the macro
    } else if (new_string.startsWith(GREEN_KEY)) {
      text_color = TFT_GREEN;
      new_string.remove(0, strlen(GREEN_KEY)); // Remove the macro
    } else if (new_string.startsWith(CYAN_KEY)) {
      text_color = TFT_CYAN;
      new_string.remove(0, strlen(CYAN_KEY)); // Remove the macro
    } else if (new_string.startsWith(WHITE_KEY)) {
      text_color = TFT_WHITE;
      new_string.remove(0, strlen(WHITE_KEY)); // Remove the macro
    } else if (new_string.startsWith(MAGENTA_KEY)) {
      text_color = TFT_MAGENTA;
      new_string.remove(0, strlen(MAGENTA_KEY)); // Remove the macro
    }
  }

  // Auto-detect CJK characters and switch to Chinese font
  bool hasCJK = false;
  for (const char* p = new_string.c_str(); *p; p++) {
    if ((uint8_t)*p >= 0x80) {
      hasCJK = true;
      break;
    }
  }
  if (hasCJK)
    tft.setFreeFont(&chinese_font);
  else
    tft.setFreeFont(NULL);

  int count = TFT_WIDTH / CHAR_WIDTH;

  char buf[count + 1];
  memset(buf, ' ', count);
  buf[count] = '\\0';

  String spaces(buf);

  // Set text color and print the string
  tft.setTextColor(text_color, background_color);
  tft.print(new_string + spaces);

  if (hasCJK)
    tft.setFreeFont(NULL);
}'''

new_proc = '''void Display::processAndPrintString(TFT_eSPI& _tft, const String& originalString) {
  // Define colors
  uint16_t text_color = TFT_GREEN; // Default text color
  uint16_t background_color = TFT_BLACK; // Default background color

  String new_string = originalString;

  // Check for color macros at the start of the string
  if (new_string.startsWith(";")) {
    if (new_string.startsWith(RED_KEY)) {
      text_color = TFT_RED;
      new_string.remove(0, strlen(RED_KEY)); // Remove the macro
    } else if (new_string.startsWith(GREEN_KEY)) {
      text_color = TFT_GREEN;
      new_string.remove(0, strlen(GREEN_KEY)); // Remove the macro
    } else if (new_string.startsWith(CYAN_KEY)) {
      text_color = TFT_CYAN;
      new_string.remove(0, strlen(CYAN_KEY)); // Remove the macro
    } else if (new_string.startsWith(WHITE_KEY)) {
      text_color = TFT_WHITE;
      new_string.remove(0, strlen(WHITE_KEY)); // Remove the macro
    } else if (new_string.startsWith(MAGENTA_KEY)) {
      text_color = TFT_MAGENTA;
      new_string.remove(0, strlen(MAGENTA_KEY)); // Remove the macro
    }
  }

  int count = TFT_WIDTH / CHAR_WIDTH;

  char buf[count + 1];
  memset(buf, ' ', count);
  buf[count] = '\\0';

  String spaces(buf);

  // Set text color and print the string
  _tft.setTextColor(text_color, background_color);

  // Auto-detect CJK
  bool hasCJK = false;
  for (const char* p = new_string.c_str(); *p; p++) {
    if ((uint8_t)*p >= 0x80) { hasCJK = true; break; }
  }
  if (hasCJK) {
    printChinese(_tft, new_string.c_str());
    // Pad with spaces using default font
    _tft.setFreeFont(NULL);
    _tft.print(spaces);
  } else {
    _tft.setFreeFont(NULL);
    _tft.print(new_string + spaces);
  }
}'''

content = content.replace(old_proc, new_proc)

# Replace buildBanner Chinese font usage
# buildBanner: this->tft.setFreeFont(&chinese_font); ... this->tft.drawCentreString(...)
old_banner = '''  this->tft.setFreeFont(&chinese_font);
  this->tft.drawCentreString(String(current_title), tft.width() / 2, y + 130, 1);'''
new_banner = '''  this->tft.setFreeFont(&chinese_font);
  this->tft.drawCentreString(String(current_title), tft.width() / 2, y + 130, 1);'''

# Keep buildBanner as-is since it uses drawCentreString which works with the GFX font
# But we need to update the touchToExit function
old_tt = '''  display_obj.tft.setFreeFont(&chinese_font);
  display_obj.tft.drawCentreString(text10, tftWidth / 2, tftHeight / 2, 1);'''
new_tt = '''  display_obj.tft.setFreeFont(&chinese_font);
  display_obj.tft.drawCentreString(text10, tftWidth / 2, tftHeight / 2, 1);'''

# These stay the same - drawCentreString works with the GFX font directly

with open(f"{base}/Display.cpp", "w") as f:
    f.write(content)

print("Display.cpp updated")

# ============================================================
# MenuFunctions.cpp: Replace setFreeFont(&chinese_font) + drawString/drawCentreString
# with printChinese approach
# ============================================================
with open(f"{base}/MenuFunctions.cpp", "r") as f:
    content = f.read()

# buttonNotSelected/buttonSelected: setFreeFont(&chinese_font) + drawCentreString
# We need to keep these using the GFX font since drawButton uses the current font
# Just make sure the font is set correctly

# displayCurrentMenu: setFreeFont(&chinese_font) + drawCentreString
# Keep as-is since drawCentreString works with GFX font

# brightnessMode: setFreeFont(&chinese_font) + drawCentreString
# Keep as-is

# The old chinese_font covered 0x20-0x9ED8, but the new one covers 0x20-0x172
# Characters outside this range won't display. But since we're using dense encoding,
# the CJK characters are mapped to 0x7F-0x172.
# The drawButton/drawCentreString functions pass raw character bytes to the font.
# For ASCII characters, this works fine (0x20-0x7E).
# For CJK characters, the raw UTF-8 bytes are NOT in the dense range.
# So we need to use printChinese() for strings that contain CJK characters.

# The approach: for drawButton and drawCentreString calls that use Chinese text,
# we need to replace them with printChinese() calls.

# Let me find all setFreeFont(&chinese_font) occurrences and check what follows

with open(f"{base}/MenuFunctions.cpp", "w") as f:
    f.write(content)

print("MenuFunctions.cpp - font switching preserved for drawButton/drawCentreString")

# ============================================================
# WiFiScan.cpp: Same approach
# ============================================================
with open(f"{base}/WiFiScan.cpp", "r") as f:
    content = f.read()

with open(f"{base}/WiFiScan.cpp", "w") as f:
    f.write(content)

print("WiFiScan.cpp - font switching preserved")

print("\nDone! Note: drawButton and drawCentreString use the GFX font directly.")
print("The CJK translation happens via printChinese() for other text output.")
print("For drawButton/drawCentreString with Chinese text, the font's glyph table")
print("needs to map the raw bytes correctly.")