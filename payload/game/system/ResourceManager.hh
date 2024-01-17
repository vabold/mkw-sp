#pragma once

#include "game/system/MultiDvdArchive.hh"

namespace System {

class ResourceManager {
public:
    REPLACE MultiDvdArchive *load(int channelId, void *archiveHeap, const char *filename);
    MultiDvdArchive *REPLACED(load)(int channelId, void *archiveHeap, const char *filename);

    void tryLogCommonArchive(MultiDvdArchive *arc) const;
};

} // namespace System
