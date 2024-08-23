#include <Common.S>

// Enable collision with item objects in time trials
PATCH_REPLACE_START(ItemDirector_checkKartCollision, 0x1c)
    li r0, 0x0
PATCH_REPLACE_END(ItemDirector_checkKartCollision, 0x1c)
