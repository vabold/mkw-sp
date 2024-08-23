#include <Common.S>

// Construct item box objects in time trials
PATCH_REPLACE_START(ObjectDirector_createObjects, 0x6f0)
    li r0, 0x0
PATCH_REPLACE_END(ObjectDirector_createObjects, 0x6f0)

// Subsequently, disable bomb cars in time trials
PATCH_B_START(ObjectDirector_createObjects, 0x7ec)
    lbz r0, 0x55(r15)
    cmpwi r0, 0x0
    beq- end

    lwz r3, 0xc(r18)
    addi r4, r31, 0xad9
    lwz r5, 0x8(r18)
    lhax r0, r3, r17
    mulli r0, r0, 0x74
    add r3, r5, r0
    addi r3, r3, 0x2
    bl strcmp
    cmpwi r3, 0x0
    bne- end

    b ObjectDirector_createObjects + 0xab8

    end:
    lwz r0, 0xb68(r19)
    b ObjectDirector_createObjects + 0x7f0
PATCH_B_END(ObjectDirector_createObjects, 0x7ec)
