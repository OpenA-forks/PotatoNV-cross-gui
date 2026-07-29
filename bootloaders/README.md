## Decrypt Internal Storage Data

EMUI User Storage file system is encrypted by default.

Before flashing unoficial AOSP-based firmwares:

1. Boot phone in to TWRP Reovery
2. Mount
    * [x] Vendor
    * [ ] ...
    * [x] Micro SD Card
3. Copy **decrypt_data_mount.sh** in to SD-Card (from PC)
4. Open (in TWRP) Advanced > Terminal
5. Run `bash /external_sd/decrypt_data_mount.sh` -> **Remove encryption**
6. Reboot TWRP Reovery (again)
7. Run `bash /external_sd/decrypt_data_mount.sh` ->  **Non encrypted**
8. Do Wipe > Format Data
9. Reboot TWRP Reovery (again)
10. Go Wipe > Advanced Wipe and select:
    * [x] Dalvik / ART Cache
    * [x] Cache
    * [x] Data
    * [x] System
11. Wipe this partitions.
12. Reboot into fastboot mode and flash `system.img`

If fstab restores all encription params after first rebooting, just try (after runs script) power off device from TWRP menu and start in to recovery via buttons.

## HiSiBootloaders

Imported from https://github.com/kitsuned/HiSiBootloaders

Compressed with GNU Tar + lzma
