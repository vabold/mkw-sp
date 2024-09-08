#include <Common.S>

PATCH_BL_START(KartCollide_handleFallBoundary, 0xb8)
    // Original instruction, but without the zero compare bit
    rlwinm r0, r0, 0x0, 0x1c, 0x1c

    // If the metadata section is present in the KMP, we instead check its value
    // No need to do a nullptr check, we're guaranteed initialization
    lis r3, CourseMap_s_instance@ha
    lwz r3, CourseMap_s_instance@l(r3)

    // Check if MapdataMetaDataAccessor is present
    lwz r3, 0x50(r3)
    cmpwi r3, 0x0
    beq- end

    // If it is, we're guaranteed to have one point correctly initialized
    lwz r3, 0x0(r3)
    lwz r3, 0x0(r3)
    lwz r3, 0x0(r3)

    // Compare against the bool in MapdataMetaData instead
    lbz r0, 0x0(r3)

end:
    cmpwi r0, 0x0
PATCH_BL_END(KartCollide_handleFallBoundary, 0xb8)
