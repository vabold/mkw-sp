#include <Common.S>

PATCH_REPLACE_START(ObjKinoko_ct, 0x160)
    stw r10, 0x140(r29)
PATCH_REPLACE_END(ObjKinoko_ct, 0x160)
