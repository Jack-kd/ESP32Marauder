#pragma once
// Boot logo for ESP32 Marauder
#include "configs.h"

#ifdef HAS_SCREEN

// Include the appropriate boot logo image based on screen type
#if defined(HAS_FULL_SCREEN)
  #include "boot_logo_full_rgb565.h"
  #define BOOT_LOGO_WIDTH  240
  #define BOOT_LOGO_HEIGHT 320
#elif defined(HAS_MINI_SCREEN)
  #include "boot_logo_small_rgb565.h"
  #define BOOT_LOGO_WIDTH  135
  #define BOOT_LOGO_HEIGHT 240
#endif

#if defined(BOOT_LOGO_WIDTH) && defined(BOOT_LOGO_HEIGHT)
  // Draw the boot logo centered on screen
  // Returns true if logo was drawn
  inline bool drawBootLogo(TFT_eSPI &tft) {
    int x = (TFT_WIDTH  - BOOT_LOGO_WIDTH)  / 2;
    int y = (TFT_HEIGHT - BOOT_LOGO_HEIGHT) / 2;
    if (x < 0) x = 0;
    if (y < 0) y = 0;

  #if defined(HAS_FULL_SCREEN)
    tft.pushImage(x, y, BOOT_LOGO_WIDTH, BOOT_LOGO_HEIGHT, boot_logo_full);
  #elif defined(HAS_MINI_SCREEN)
    tft.pushImage(x, y, BOOT_LOGO_WIDTH, BOOT_LOGO_HEIGHT, boot_logo_small);
  #endif
    return true;
  }
#endif

#endif