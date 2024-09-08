#pragma once

#include "game/system/MapdataAccessor.hh"

namespace System {

class CourseMap {
public:
    REPLACE void init();
    void REPLACED(init)();

private:
    MapdataMetaDataAccessor *parseMetadata(u32 sectionName);

    u8 _00[0x10 - 0x00];
    MapdataCourseAccessor *m_course;
    u8 _14[0x50 - 0x14];
    // We choose offset 0x50 because it's guaranteed to be nullptr otherwise
    MapdataMetaDataAccessor *m_metadata;
};
static_assert(sizeof(CourseMap) == 0x54);

} // namespace System
