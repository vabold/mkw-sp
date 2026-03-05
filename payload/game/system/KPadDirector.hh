#pragma once

#include "game/system/KPadGhostController.hh"

class KPadGhostController;

namespace System {

class KPadDirector {
public:
    const KPadGhostController &ghostController(u32 idx) {
        return m_ghostControllers[idx];
    }

    static KPadDirector *Instance();

private:
    u8 _0000[0x3e60 - 0x0000];
    KPadGhostController m_ghostControllers[4];
    u8 _4100[0x415c - 0x4100];

    static KPadDirector *s_instance;
};

} // namespace System
