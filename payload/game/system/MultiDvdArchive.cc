#include "MultiDvdArchive.hh"

namespace System {

int MultiDvdArchive::getEntryID(const char *filename) {
    for (int i = 0; i < m_archiveCount; ++i) {
        DvdArchive &archive = m_archives[i];

        if (!archive.isLoaded()) {
            continue;
        }

        return archive.getEntryID(filename);
    }

    return -1;
}

} // namespace System
