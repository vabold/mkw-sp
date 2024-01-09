#pragma once

#include <Common.hh>

namespace EGG {

struct Vector3f {
    void log(const char *name) const;

    Vector3f() {}
    Vector3f(f32 _x, f32 _y, f32 _z) : x(_x), y(_y), z(_z) {}

    Vector3f operator+(const Vector3f &rhs) const {
        return Vector3f(x + rhs.x, y + rhs.y, z + rhs.z);
    }

    Vector3f operator-(const Vector3f &rhs) const {
        return Vector3f(x - rhs.x, y - rhs.y, z - rhs.z);
    }

    Vector3f operator-() const {
        return Vector3f(-x, -y, -z);
    }

    Vector3f operator*(const f32 scalar) const {
        return Vector3f(x * scalar, y * scalar, z * scalar);
    }

    bool operator==(const Vector3f &rhs) const {
        return x == rhs.x && y == rhs.y && z == rhs.z;
    }

    f32 x, y, z;

    static const Vector3f zero;
    static const Vector3f ex;
    static const Vector3f ey;
    static const Vector3f ez;
};

} // namespace EGG
