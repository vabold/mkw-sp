#pragma once

#include "game/kart/KartObject.hh"

namespace Kart {

class KartObjectManager {
public:
    REPLACE static void end(u32 playerIdx);
    static void REPLACED(end)(u32 playerIdx);

    const KartObject *object(size_t idx) const;

    static REPLACE KartObjectManager *CreateInstance();
    static KartObjectManager *REPLACED(CreateInstance)();

    static KartObjectManager *Instance();

private:
    u8 _00[0x20 - 0x00];
    KartObject **m_objects;

    static KartObjectManager *s_instance;
};

} // namespace Kart
