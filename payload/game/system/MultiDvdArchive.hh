#pragma once

#include "game/system/DvdArchive.hh"

namespace System {

class MultiDvdArchive {
public:
    bool isLoaded() const;
    int getEntryID(const char *filename);

private:
    u8 _00[0x04 - 0x00];
    DvdArchive *m_archives;
    u16 m_archiveCount;
    u8 _0a[0x1c - 0x0a];
};
static_assert(sizeof(MultiDvdArchive) == 0x1c);

} // namespace System
