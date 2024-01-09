#include "MapdataStartPoint.hh"

#include "game/system/CourseMap.hh"
#include "game/system/RaceConfig.hh"
#include "game/system/map/MapdataStageInfo.hh"

#include <egg/math/eggQuat.hh>

#include <nw4r/math/arithmetic.hh>

extern "C" {
#include <revolution.h>
}

namespace System {

void MapdataStartPoint::getInitialPhysicsValues(EGG::Vector3f &pos, EGG::Vector3f &angles,
        u8 placement, u8 playerCount) {
    REPLACED(getInitialPhysicsValues)(pos, angles, placement, playerCount);

    // Despite having two callers, we only need to check the gamemode
    // CtrlRace2DMap::load always calls this function with start point index 0
    // RaceManager::getInitialPhysicsValues calls this function with fixed values for the gamemode
    if (!RaceConfig::Instance()->raceScenario().isTimeAttack()) {
        return;
    }

    // We now have the derived position and euler angles - let's log them
    pos.log("POS");
    angles.log("ANG");

    // A transformation is applied generically across all positions - let's see if it was changed
    auto *point = CourseMap::Instance()->getStartPoint(0);
    assert(point == this && point->data());

    EGG::Vector3f newPos;
    EGG::Vector3f newAngles;
    tryRecomputeInitialPhysicsValues(newPos, newAngles, placement, playerCount);

    if (pos == newPos && angles == newAngles) {
        SP_LOG("UNCHANGED!");
    } else {
        newPos.log("NEWPOS");
        newAngles.log("NEWANG");
        SP_LOG("CHANGED!");
    }
}

void MapdataStartPoint::tryRecomputeInitialPhysicsValues(EGG::Vector3f &pos, EGG::Vector3f &angles,
        u8 placement, u8 playerCount) {
    constexpr f32 MATH_PI = 3.1415927f;
    constexpr f32 DEG_TO_RAD = MATH_PI / 180.0f;
    constexpr f32 DEG_TO_FIDX = 256.0f / 360.0f;

    // Create a rotation quaternion from euler angles
    EGG::Quatf rotation;
    rotation.fromRPY(m_data->rot * DEG_TO_RAD);

    EGG::Vector3f zAxis = rotation.rotateVector(-EGG::Vector3f::ez);
    EGG::Vector3f xAxis = rotation.rotateVector(-EGG::Vector3f::ex);

    const auto *stageInfo = CourseMap::Instance()->getStageInfo();
    assert(stageInfo);
    int translationDirection = stageInfo->getPolePosition() == 1 ? -1 : 1;

    f32 cos = nw4r::math::CosFIdx(CourseMap::Angle() * DEG_TO_FIDX);
    f32 sin = translationDirection * nw4r::math::SinFIdx(CourseMap::Angle() * DEG_TO_FIDX);

    int xTranslation = translationDirection * s_xTranslationTable[playerCount - 1][0];
    f32 xScalar =
            sin * (CourseMap::Tmp0() * (static_cast<f32>(xTranslation) + 10.0f) / 10.0f) / cos;
    EGG::Vector3f xTmp = -zAxis * xScalar;

    int zTranslation = s_zTranslationTable[playerCount - 1][placement];
    f32 zScalar = CourseMap::Tmp2() * static_cast<f32>(zTranslation / 2) +
            CourseMap::Tmp1() * static_cast<f32>(zTranslation) +
            CourseMap::Tmp3() * static_cast<f32>((zTranslation + 1) / 2);
    EGG::Vector3f zTmp = zAxis * zScalar;

    EGG::Vector3f tmp0 = xTmp + zTmp;
    EGG::Vector3f tmp1 = xAxis * CourseMap::Tmp0();
    EGG::Vector3f tmp2 = tmp0 - tmp1;
    EGG::Vector3f tmpPos = tmp2 + m_data->pos;

    EGG::Vector3f vCos = xAxis * cos;
    EGG::Vector3f vSin = zAxis * sin;
    EGG::Vector3f vRes = vCos + vSin;

    int tmpTranslation = translationDirection * s_xTranslationTable[playerCount - 1][placement];
    f32 tmpScalar = CourseMap::Tmp0() * (static_cast<f32>(tmpTranslation) + 10.0f) / (cos * 10.0f);
    EGG::Vector3f tmpRes = vRes * tmpScalar;

    pos = tmpPos + tmpRes;
    angles = m_data->rot;
}

} // namespace System
