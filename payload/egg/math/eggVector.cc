#include "eggVector.hh"

extern "C" {
#include <revolution.h>
}

namespace EGG {

// Helper function for logging
void Vector3f::log(const char *name) const {
    SP_LOG("%s: [%f, %f, %f]", name, x, y, z);
}

} // namespace EGG
