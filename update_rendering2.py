#!/usr/bin/env python3
"""Replace all font-switching + draw calls with printChinese/drawCentreStringChinese/drawChineseButton."""
import re

base = "/workspace/esp32_marauder"

# ============================================================
# MenuFunctions.cpp
# ============================================================
with open(f"{base}/MenuFunctions.cpp", "r") as f:
    content = f.read()

# Pattern 1: setFreeFont(&chinese_font); ... drawCentreString(...); setFreeFont(MENU_FONT);
# Replace with drawCentreStringChinese
pattern1 = re.compile(
    r'(display_obj\.)?tft\.setFreeFont\(&chinese_font\);\s*\n'
    r'(\s*)(display_obj\.)?tft\.drawCentreString\(([^;]+);\s*\n'
    r'\s*(display_obj\.)?tft\.setFreeFont\(MENU_FONT\);'
)

def replace_draw_centre(match):
    indent = match.group(2) or ''
    args = match.group(4).strip()
    tft_obj = match.group(1) or match.group(3) or ''
    tft_ref = f'{tft_obj}tft' if tft_obj else 'tft'
    return f'{indent}drawCentreStringChinese({tft_ref}, {args});'

content = pattern1.sub(replace_draw_centre, content)
print(f"MenuFunctions.cpp: drawCentreString replacements: {len(pattern1.findall(content))}")

# Pattern 2: drawButton calls with Chinese text
# Find buttonNotSelected/buttonSelected functions that use setFreeFont(&chinese_font)
# These call display_obj.tft.drawButton(..., name, ...)
# Replace with drawChineseButton

# Find all places where setFreeFont(&chinese_font) is followed by drawButton
# First, let me find the button drawing functions
# buttonNotSelected: display_obj.tft.drawButton(x, y, w, h, outline, fill, textcolor, name, 1);
# buttonSelected: display_obj.tft.drawButton(x, y, w, h, outline, fill, textcolor, (name + " ").c_str(), 1);

# Approach: For each setFreeFont(&chinese_font) occurrence, check if the next drawButton is nearby
# and replace the whole block

# More targeted approach: find the buttonNotSelected and buttonSelected functions
# and replace setFreeFont(&chinese_font) + drawButton with drawChineseButton

# Let me find the exact patterns
lines = content.split('\n')
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    if 'setFreeFont(&chinese_font)' in line:
        # Look ahead for drawButton
        j = i + 1
        found_draw = False
        while j < len(lines) and j < i + 5:
            if 'drawButton' in lines[j]:
                found_draw = True
                break
            j += 1
        
        if found_draw:
            # Extract the drawButton call
            draw_line = lines[j]
            # Parse: display_obj.tft.drawButton(x, y, w, h, outline, fill, textcolor, name, 1);
            m = re.search(r'(\w+\.)?(\w+\.)?drawButton\(([^)]+)\)', draw_line)
            if m:
                prefix = m.group(1) or ''
                tft_ref = f'{prefix}tft'
                args = m.group(3)
                # Extract: x, y, w, h, outline, fill, textcolor, label, fontsize
                parts = [p.strip() for p in args.split(',')]
                if len(parts) >= 8:
                    x, y, w, h, outline, fill, tc, label = parts[:8]
                    # Replace with drawChineseButton
                    new_lines.append(f'      drawChineseButton({tft_ref}, {x}, {y}, {w}, {h}, {label}, {outline}, {fill}, {tc});')
                    i = j + 1
                    continue
        # Also check for drawCentreString
        elif j < len(lines) and 'drawCentreString' in lines[j] and j < i + 5:
            draw_line = lines[j]
            m = re.search(r'(\w+\.)?(\w+\.)?drawCentreString\(([^)]+)\)', draw_line)
            if m:
                prefix = m.group(1) or ''
                tft_ref = f'{prefix}tft'
                args = m.group(3)
                new_lines.append(f'      drawCentreStringChinese({tft_ref}, {args});')
                i = j + 1
                continue
    
    new_lines.append(line)
    i += 1

content = '\n'.join(new_lines)

# Now handle brightnessMode and displayCurrentMenu drawCentreString calls
# These are already handled by the pattern1 replacement above

# Also handle the setFreeFont(MENU_FONT) that follows Chinese text
# Remove orphaned setFreeFont(MENU_FONT) calls that are no longer needed
# (They were the restore calls after the Chinese font)

with open(f"{base}/MenuFunctions.cpp", "w") as f:
    f.write(content)

print("MenuFunctions.cpp updated")

# ============================================================
# WiFiScan.cpp
# ============================================================
with open(f"{base}/WiFiScan.cpp", "r") as f:
    content = f.read()

# Replace setFreeFont(&chinese_font); ... drawCentreString(...); with drawCentreStringChinese
pattern_wifi = re.compile(
    r'(display_obj\.)?tft\.setFreeFont\(&chinese_font\);\s*\n'
    r'(\s*)(display_obj\.)?tft\.drawCentreString\(([^;]+);\s*\n'
    r'\s*(display_obj\.)?tft\.setFreeFont\(NULL\);'
)

def replace_wifi(match):
    indent = match.group(2) or ''
    args = match.group(4).strip()
    tft_obj = match.group(1) or match.group(3) or ''
    tft_ref = f'{tft_obj}tft' if tft_obj else 'tft'
    return f'{indent}drawCentreStringChinese({tft_ref}, {args});'

content = re.sub(pattern_wifi, replace_wifi, content)

# Also handle pattern without the restore font call
pattern_wifi2 = re.compile(
    r'(display_obj\.)?tft\.setFreeFont\(&chinese_font\);\s*\n'
    r'(\s*)(display_obj\.)?tft\.drawCentreString\(([^;]+);'
)

def replace_wifi2(match):
    indent = match.group(2) or ''
    args = match.group(4).strip()
    tft_obj = match.group(1) or match.group(3) or ''
    tft_ref = f'{tft_obj}tft' if tft_obj else 'tft'
    return f'{indent}drawCentreStringChinese({tft_ref}, {args});'

content = re.sub(pattern_wifi2, replace_wifi2, content)

with open(f"{base}/WiFiScan.cpp", "w") as f:
    f.write(content)

print("WiFiScan.cpp updated")

# ============================================================
# Display.cpp: buildBanner and touchToExit
# ============================================================
with open(f"{base}/Display.cpp", "r") as f:
    content = f.read()

# buildBanner: this->tft.setFreeFont(&chinese_font); ... this->tft.drawCentreString(...)
# Replace with drawCentreStringChinese
pattern_disp = re.compile(
    r'this->tft\.setFreeFont\(&chinese_font\);\s*\n'
    r'(\s*)this->tft\.drawCentreString\(([^;]+);'
)

def replace_disp(match):
    indent = match.group(1) or ''
    args = match.group(2).strip()
    return f'{indent}drawCentreStringChinese(this->tft, {args});'

content = re.sub(pattern_disp, replace_disp, content)

# touchToExit: display_obj.tft.setFreeFont(&chinese_font); ... display_obj.tft.drawCentreString(...)
pattern_tt = re.compile(
    r'display_obj\.tft\.setFreeFont\(&chinese_font\);\s*\n'
    r'(\s*)display_obj\.tft\.drawCentreString\(([^;]+);'
)

def replace_tt(match):
    indent = match.group(1) or ''
    args = match.group(2).strip()
    return f'{indent}drawCentreStringChinese(display_obj.tft, {args});'

content = re.sub(pattern_tt, replace_tt, content)

with open(f"{base}/Display.cpp", "w") as f:
    f.write(content)

print("Display.cpp updated")

# ============================================================
# TouchKeyboard.cpp
# ============================================================
with open(f"{base}/TouchKeyboard.cpp", "r") as f:
    content = f.read()

# Replace setFreeFont(&chinese_font); ... drawCentreString(...); with drawCentreStringChinese
pattern_kb = re.compile(
    r'(display_obj\.)?tft\.setFreeFont\(&chinese_font\);\s*\n'
    r'(\s*)(display_obj\.)?tft\.drawCentreString\(([^;]+);\s*\n'
    r'\s*(display_obj\.)?tft\.setFreeFont\(NULL\);'
)

def replace_kb(match):
    indent = match.group(2) or ''
    args = match.group(4).strip()
    tft_obj = match.group(1) or match.group(3) or ''
    tft_ref = f'{tft_obj}tft' if tft_obj else 'tft'
    return f'{indent}drawCentreStringChinese({tft_ref}, {args});'

content = re.sub(pattern_kb, replace_kb, content)

with open(f"{base}/TouchKeyboard.cpp", "w") as f:
    f.write(content)

print("TouchKeyboard.cpp updated")

print("\nAll rendering code updated to use dense-font helpers!")