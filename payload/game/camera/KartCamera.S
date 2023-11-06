#include <Common.S>

// Hijack backwards camera position and target
PATCH_B_START(KartCamera_calc, 0x8ec)
    mr r3, r29
    li r4, 0x0
    bl KartCamera_reconfigure
    lwz r12, 0x0(r29) // Original instruction
    b KartCamera_calc + 0x8f0
PATCH_B_END(KartCamera_calc, 0x8ec)
