#pragma once

#include <Common.hh>

namespace Item {

class ItemSlotTable {
public:
    REPLACE static ItemSlotTable *CreateInstance();
    static ItemSlotTable *REPLACED(CreateInstance)();

private:
    static std::array<std::array<u16, 12>, 12> s_playerScaleTable;
};

} // namespace Item
