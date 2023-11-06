#pragma once

#include "egg/math/eggMatrix.hh"

namespace EGG {

class BaseCamera {
private:
    u8 _00[0x04 - 0x00];

protected:
    Matrix34f m_viewMatrix;
    Matrix34f m_oldMatrix;
};
static_assert(sizeof(BaseCamera) == 0x64);

class LookAtCamera : public BaseCamera {
public:
    LookAtCamera() = default;

    const Matrix34f &getViewMatrix() const;
    void doUpdateMatrix();

    void setPosition(const EGG::Vector3f &pos) {
        m_position = pos;
    }

    void setTarget(const EGG::Vector3f &target) {
        m_target = target;
    }

    void setUp(const EGG::Vector3f &up) {
        m_up = up;
    }

protected:
    Vector3f m_position;
    Vector3f m_target;
    Vector3f m_up;
};
static_assert(sizeof(LookAtCamera) == 0x88);

} // namespace EGG
