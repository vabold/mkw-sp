#pragma once

#include "egg/math/eggVector.hh"

namespace EGG {

struct Quatf {
    void fromRPY(f32 _x, f32 _y, f32 _z);
    void fromRPY(const Vector3f &v) {
        fromRPY(v.x, v.y, v.z);
    }

    Vector3f rotateVector(const EGG::Vector3f &v);

    f32 x, y, z, w;
};

} // namespace EGG
