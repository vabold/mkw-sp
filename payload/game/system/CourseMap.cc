#include "CourseMap.hh"

namespace System {

void CourseMap::init() {
    REPLACED(init)();

    constexpr u32 MAPDATA_METADATA_SIGNATURE = 0x4d455441; // META
    m_metadata = parseMetadata(MAPDATA_METADATA_SIGNATURE);
}

MapdataMetaDataAccessor *CourseMap::parseMetadata(u32 sectionName) {
    const auto *pSection = m_course->findSection(sectionName);
    return pSection ? new MapdataMetaDataAccessor(pSection) : nullptr;
}

} // namespace System
