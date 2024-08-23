#include "ItemSlotTable.hh"

namespace Item {

ItemSlotTable *ItemSlotTable::CreateInstance() {
    // Pull last place items in time trials
    s_playerScaleTable[0][0] = 12;

    return REPLACED(CreateInstance)();
}

} // namespace Item
