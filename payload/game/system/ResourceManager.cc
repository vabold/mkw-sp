#include "ResourceManager.hh"

extern "C" {
#include <revolution.h>
}

namespace System {

MultiDvdArchive *ResourceManager::load(int channelId, void *archiveHeap, const char *filename) {
    MultiDvdArchive *arc = REPLACED(load)(channelId, archiveHeap, filename);
    SP_LOG("%d", channelId);
    if (channelId == 0) {
        tryLogCommonArchive(arc);
    }
    return arc;
}

void ResourceManager::tryLogCommonArchive(MultiDvdArchive *arc) const {
    assert(arc->isLoaded());
    constexpr const char *names[] = {"balloon.brres", "banana.brres", "banana_s.brres",
            "battle_camera.bcp", "big_kinoko.brres", "bikePartsDispParam.bin", "bomb.brres",
            "bombCore.brres", "driver.brres", "driverDispParam.bin", "DriverIKParam.bin",
            "driverParam.bin", "GeoHitTableItem.bin", "GeoHitTableItemObj.bin",
            "GeoHitTableKart.bin", "GeoHitTableKartObj.bin", "gesso.brres", "icon_mii.brres",
            "item_killer.brres", "item_light.brres", "itemBoxNiseRtpa.brres", "ItemSlot.bin",
            "jugem_battle.brres", "jugem_flag.brres", "jugem_lamp.brres", "jugem_reverse.brres",
            "jugemu.brres", "jugemu_lap.brres", "jugemu_lapf.brres", "jugemu_signal.brres",
            "kart_killer.brres", "kartAIActionParam.bin", "kartAISpdParam.bin",
            "kartCameraParam.bin", "kartDriverDispParam.bin", "kartParam.bin",
            "kartPartsDispParam.bin", "kinoko.brres", "kinoko_p.brres", "koura_green.brres",
            "koura_red.brres", "koura_s.brres", "kumo.brres", "kumo_s.brres", "lensflare.brres",
            "miiDispParam.bin", "minigame.kmg", "mission_camera.bcp", "ObjFlow.bin",
            "pow_bloc.brres", "pow_bloc_plane.brres", "race_camera.bcp", "ranktimeGP.krt",
            "rod.brres", "star.brres", "start_camera.bcp", "thunder.brres", "tico.brres",
            "togezo_koura.brres", "vibration.krm"};

    OSReport("================ KINOKO HEADER ================\n");

    for (size_t i = 0; i < sizeof(names) / sizeof(char *); ++i) {
        int entryId = arc->getEntryID(names[i]);
        assert(entryId != 0);
        OSReport(">> ENTRY ID: %d; NAME: %s\n", entryId, names[i]);
    }

    OSReport("================ KINOKO FOOTER ================\n");
}

} // namespace System
