#include <Common.S>

PATCH_REPLACE_START(EGG_DrawPathDOF_drawSetup, 0x5c8)
    lis r9,0x3000
PATCH_REPLACE_END(EGG_DrawPathDOF_drawSetup, 0x5c8)
