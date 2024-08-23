#include <Common.S>

// Allow table scaling in time trials
PATCH_REPLACE_START(ItemSlotTable_init, 0x1a0)
    nop
PATCH_REPLACE_END(ItemSlotTable_init, 0x1a0)
