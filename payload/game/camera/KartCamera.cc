#include "KartCamera.hh"

namespace Camera {

void KartCamera::reconfigure(u32 /* configuration */) {
    if constexpr (!FIX_POS) {
        return;
    }

    constexpr size_t CAMERA_FLAG_BACKWARDS = 0x20;
    if (m_flags ^ CAMERA_FLAG_BACKWARDS) {
        return;
    }

    // TODO handle multiple courses and configurations

    constexpr f32 x = 3579.7817f;
    constexpr f32 y = 14012.504f;
    constexpr f32 z = 7648.6045f;

    const EGG::Vector3f pos = EGG::Vector3f(x, y, z);
    const EGG::Vector3f target = EGG::Vector3f(x + 100.0f, y - 10.0f, z);

    m_position = pos;
    m_target = target;
    m_up = EGG::Vector3f::ey;
    m_fov = 55.0f;
    m_fovMult = 0.0f;
}

void KartCamera::setFovMult(f32 mult) {
    if constexpr (FIX_POS) {
        return;
    }

    if (mult * 12.0f > m_fovMult) {
        m_fovMult = mult * 12.0f;
    }
}

void KartCamera::getMatrixCopy(f32 scalar, EGG::Matrix34f &matrix, EGG::Vector3f *position) {
    EGG::Vector3f pos = m_position;
    EGG::Vector3f target = m_target;
    EGG::Vector3f up = m_up;

    if constexpr (FIX_POS) {
        constexpr size_t CAMERA_FLAG_BACKWARDS = 0x20;
        if (m_flags & CAMERA_FLAG_BACKWARDS) {
            constexpr f32 x = 3579.7817f + 400.0f;
            constexpr f32 y = 14012.504f;
            constexpr f32 z = 7648.6045f;

            pos = EGG::Vector3f(x, y, z);
            target = EGG::Vector3f(x + 100.0f, y - 10.0f, z);
            up = EGG::Vector3f::ey;
        }
    }

    const EGG::Vector3f configuredPos = pos + ((target - pos) * scalar);

    if (position) {
        *position = configuredPos;
    }

    EGG::LookAtCamera camera;
    camera.setPosition(configuredPos);
    camera.setTarget(target);
    camera.setUp(EGG::Vector3f::ey);
    camera.doUpdateMatrix();
    matrix = camera.getViewMatrix();
}

} // namespace Camera

extern "C" void KartCamera_reconfigure(Camera::KartCamera *self, u32 configuration) {
    self->reconfigure(configuration);
}
