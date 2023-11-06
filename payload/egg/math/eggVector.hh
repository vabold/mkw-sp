#pragma once

#include <Common.hh>

namespace EGG {

struct Vector3f {
    Vector3f() {}
    Vector3f(f32 _x, f32 _y, f32 _z) : x(_x), y(_y), z(_z) {}

    void operator=(const Vector3f &rhs) {
        x = rhs.x;
        y = rhs.y;
        z = rhs.z;
    }

    Vector3f operator+(const Vector3f &rhs) const {
        return Vector3f(x + rhs.x, y + rhs.y, z + rhs.z);
    }

    Vector3f operator-(const Vector3f &rhs) const {
        return Vector3f(x - rhs.x, y - rhs.y, z - rhs.z);
    }

    Vector3f operator*(f32 scalar) const {
        return Vector3f(x * scalar, y * scalar, z * scalar);
    }

    f32 x, y, z;

    static const Vector3f zero, ex, ey, ez;
};

} // namespace EGG
