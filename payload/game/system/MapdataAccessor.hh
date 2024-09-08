#pragma once

#include <Common.hh>

namespace System {

struct MapdataSection {
    u32 signature;
    u16 count;
};
static_assert(sizeof(MapdataSection) == 0x8);

class MapdataMetaData {
public:
    struct SData {
        bool disableOOBinAction;
    };

    MapdataMetaData(const SData *data) : m_data(data) {}

private:
    const SData *m_data;
};

class MapdataCourseAccessor {
public:
    MapdataSection *findSection(u32 sectionName);
};

template <typename T, typename TData>
class MapdataAccessorBase {
public:
    MapdataAccessorBase(const MapdataSection *section)
        : m_entries(nullptr), m_count(0), m_section(section) {}

    inline void init(const TData *start, u16 count) {
        if (count != 0) {
            m_count = count;
            m_entries = new T *[count];
        }

        for (u16 i = 0; i < count; i++) {
            m_entries[i] = new T(&start[i]);
        }
    }

    T **m_entries;
    u16 m_count;
    const MapdataSection *m_section;
};

class MapdataMetaDataAccessor
    : public MapdataAccessorBase<MapdataMetaData, MapdataMetaData::SData> {
public:
    MapdataMetaDataAccessor(const MapdataSection *section)
        : MapdataAccessorBase<MapdataMetaData, MapdataMetaData::SData>(section) {
        assert(section->count == 1);
        init(reinterpret_cast<const MapdataMetaData::SData *>(section + 1), 1);
    }
};

} // namespace System
