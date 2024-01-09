#pragma once

#include <Common.hh>

namespace System {

class MapdataStageInfo;
class MapdataStartPoint;

class CourseMap {
public:
    MapdataStageInfo *getStageInfo();
    MapdataStartPoint *getStartPoint(u32 idx);

    static CourseMap *Instance() {
        return s_instance;
    }

    static f32 Angle() {
        return s_angle;
    }

    static f32 Tmp0() {
        return s_tmp0;
    }

    static f32 Tmp1() {
        return s_tmp1;
    }

    static f32 Tmp2() {
        return s_tmp2;
    }

    static f32 Tmp3() {
        return s_tmp3;
    }

private:
    static CourseMap *s_instance;

    static f32 s_angle;
    static f32 s_tmp0;
    static f32 s_tmp1;
    static f32 s_tmp2;
    static f32 s_tmp3;
};

} // namespace System
