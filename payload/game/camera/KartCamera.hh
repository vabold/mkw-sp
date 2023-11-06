#pragma once

#include <egg/gfx/eggCamera.hh>

namespace Camera {

class KartCamera : public EGG::LookAtCamera {
public:
    void reconfigure(u32);

    REPLACE void setFovMult(f32);
    REPLACE void getMatrixCopy(f32, EGG::Matrix34f &, EGG::Vector3f *);

private:
    static constexpr bool FIX_POS = true;

    u8 _088[0x11c - 0x088];
    f32 m_fov;
    f32 m_fovMult;
    u8 _124[0x334 - 0x124];
    u16 m_flags;
    u8 _336[0x348 - 0x336];
};
static_assert(sizeof(KartCamera) == 0x348);

} // namespace Camera
