#pragma once

#include <Common.hh>

namespace System {

class RaceConfig {
public:
    enum class GameMode {
        TimeTrial = 0x2,
        GhostRace = 0x5,
    };

    struct Scenario {
        constexpr bool isTimeAttack() const {
            return gamemode == GameMode::TimeTrial || gamemode == GameMode::GhostRace;
        }

        u8 _000[0xb50 - 0x000];
        GameMode gamemode;
        u8 _b54[0xbf0 - 0xb54];
    };
    static_assert(sizeof(Scenario) == 0xbf0);

    const Scenario &raceScenario() const {
        return m_raceScenario;
    }

    static RaceConfig *Instance() {
        return s_instance;
    }

private:
    u8 _0000[0x0020 - 0x0000];
    Scenario m_raceScenario;
    u8 _0c10[0x73f0 - 0x0c10];

    static RaceConfig *s_instance;
};

} // namespace System
