#include "DvdArchive.hh"

#include <stdio.h>

namespace System {

int DvdArchive::getEntryID(const char *filename) {
    assert(isLoaded());
    char buffer[256];

    if (filename[0] == '/') {
        snprintf(buffer, sizeof(buffer), "%s", filename);
    } else {
        snprintf(buffer, sizeof(buffer), "/%s", filename);
    }

    return m_handle->convertPathToEntryID(buffer);
}

} // namespace System
