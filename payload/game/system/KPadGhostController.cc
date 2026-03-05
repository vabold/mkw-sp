#include "KPadGhostController.hh"

#include "game/kart/KartObjectManager.hh"

#include "game/system/KPadDirector.hh"
#include "game/system/RaceManager.hh"

extern "C" {
#include <revolution.h>
}

namespace System {

void KPadGhostController::calcInner(RaceInputState *inputState, UIInputState *uiInputState) {
    REPLACED(calcInner)(inputState, uiInputState);

    if (this != &KPadDirector::Instance()->ghostController(0)) {
        return;
    }

    // End KRKG generation if all 3 input streams have reached the end of input
    // This handles ghosts created with instant finish code
    if (RaceManager::Instance() && RaceManager::Instance()->isStageReached(2)) {
        bool endOfInput = buttonsStreams[0]->state == 2;
        endOfInput = endOfInput && buttonsStreams[1]->state == 2;
        endOfInput = endOfInput && buttonsStreams[2]->state == 2;

        if (endOfInput) {
            Kart::KartObjectManager::Instance()->end(0);
        }
    }
}

} // namespace System
