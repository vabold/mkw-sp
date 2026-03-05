#pragma once

#include <Common.hh>

namespace System {

class RaceInputState {};
class UIInputState {};

class GhostButtonsStream {
public:
    u8 _00[0x14 - 0x00];
    u32 state;
};
static_assert(sizeof(GhostButtonsStream) == 0x18);

class KPadGhostController {
public:
    REPLACE void calcInner(RaceInputState *inputState, UIInputState *uiInputState);
    void REPLACED(calcInner)(RaceInputState *inputState, UIInputState *uiInputState);

private:
    u8 _00[0x94 - 0x00];
    GhostButtonsStream *buttonsStreams[3];
    u8 _a0[0xa8 - 0xa0];
};
static_assert(sizeof(KPadGhostController) == 0xa8);

} // namespace System
