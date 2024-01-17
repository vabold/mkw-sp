#pragma once

#include <egg/core/eggArchive.hh>

namespace System {

class DvdArchive {
public:
    bool isLoaded() const {
        return m_status == 4 || m_status == 5;
    }
    int getEntryID(const char *filename);

private:
    u8 _00[0x04 - 0x00];
    EGG::Archive *m_handle;
    u8 _08[0x20 - 0x08];
    int m_status;
};
static_assert(sizeof(DvdArchive) == 0x24);

} // namespace System
