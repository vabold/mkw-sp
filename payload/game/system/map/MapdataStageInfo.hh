#pragma once

#include <Common.hh>

namespace System {

class MapdataStageInfo {
public:
    struct SData {
        u8 _0[0x1 - 0x0];
        u8 polePosition;
        u8 _2[0xc - 0x2];
    };

    u8 getPolePosition() const {
        return m_data->polePosition;
    }

private:
    SData *m_data;
};

} // namespace System
