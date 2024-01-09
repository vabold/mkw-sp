#pragma once

#include <egg/math/eggVector.hh>

namespace System {

class MapdataStartPoint {
public:
    struct SData {
        EGG::Vector3f pos;
        EGG::Vector3f rot;
    };

    REPLACE void getInitialPhysicsValues(EGG::Vector3f &pos, EGG::Vector3f &angles, u8 placement,
            u8 playerCount);
    void REPLACED(getInitialPhysicsValues)(EGG::Vector3f &pos, EGG::Vector3f &angles, u8 placement,
            u8 playerCount);

    void tryRecomputeInitialPhysicsValues(EGG::Vector3f &pos, EGG::Vector3f &angles, u8 placement,
            u8 playerCount);

    const SData *data() const {
        return m_data;
    }

private:
    SData *m_data;

    static s8 s_xTranslationTable[12][12];
    static s8 s_zTranslationTable[12][12];
};

} // namespace System
