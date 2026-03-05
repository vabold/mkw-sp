#include "KPadDirector.hh"

namespace System {

KPadDirector *KPadDirector::Instance() {
    return s_instance;
}

} // namespace System
