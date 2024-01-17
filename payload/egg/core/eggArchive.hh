#pragma once

#include <Common.hh>

namespace EGG {

class Archive {
public:
    int convertPathToEntryID(const char *filename);
};

} // namespace EGG
