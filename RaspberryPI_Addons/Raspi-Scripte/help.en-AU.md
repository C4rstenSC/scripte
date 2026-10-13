# Raspi-Scripte 0.8.7 – User guide

Updated: 13 October 2026

## Connection and discovery

Enter the hostname or IP address, user and SSH credentials. Local discovery continues to display active address checks until they finish. Closing the discovery window cancels the scan.

After a restart requested by the application, including GPS changes, it retries the connection automatically for up to three minutes. Manual disconnect cancels reconnection.

## Program and Witty updates

Use the program update button. Packages are checked and decrypted automatically; the updater restarts the application. Connection profiles and activation are retained. Program changes require a program update; the content package updates texts and other resources.

Use “Witty Addon Software update” for the Raspberry add-on. Terminal release notes include only changes newer than the installed version and build, including skipped intermediate releases. Add-on, manufacturer software and board firmware are separate versions.

## Write an SD card

1. Select the Raspberry model and operating system, then choose the dated offline or online image.
2. Offline uses a checked cached image. Online downloads the selected official release. “Linux-Image einbinden” allows a custom IMG or supported compressed image.
3. Select the target card. Refresh and select again if it cannot be identified reliably.
4. Open the configuration assistant and enter hostname, account, Wi-Fi, SSH and region.
5. Check the target and confirm deletion. Windows requests elevation for the card worker even when your account belongs to Administrators.

Writing overwrites the selected medium. System disks are excluded. Raspberry Pi Imager is not required. Image payload is written before partition discovery areas are restored. The entire written image is then read back and compared. Completion requires successful verification.

Cancel stops the operation. An interrupted target must be written again in full. If Windows denies access again, retain the exact byte offset and Windows error code. Software tests cannot validate your physical card reader.

## Create an IMG backup

Select the card, a destination on another disk and a new IMG filename. The backup is compared with the source. Cancelled partial backups are removed and their progress is cleared.

A supported reduced MBR layout is backed up through the last partition end. A full-size partition requires confirmation before a full-card backup. Existing maintenance results and failure logs are read from the boot partition. Reducing only the filesystem does not produce a smaller partition-based backup. Other layouts are backed up in full.

Provide sufficient free space. FAT32 cannot store files larger than 4 GiB; use NTFS, exFAT or a suitable network destination.

## Shrink or expand the Raspberry SD card

Micro SD options check partitions and ext4 separately. Shrinking reboots into RAM with the root filesystem unmounted. Checks run before and after resizing, with 512 MiB reserve. Normal boot configuration is restored and the boot partition is synchronised and unmounted.

For Witty Pi 5, maintenance sends manufacturer heartbeats to complete STARTING and service the watchdog. Shutdown requires the actual STOPPING state, rather than an echoed command value. The Pi halts afterwards. Physical power removal and successful shrinking must be checked on the device.

Failures are recorded on the boot partition. Inspect the result before retrying. Expansion uses a one-time boot job for supported images and preserves accounts and networks.

## Witty, GPS and applications

Status separates add-on version, manufacturer software and actual board firmware. Firmware detection does not need a GPS fix. The active GPS source is shown separately from your future installation choice. USB and Waveshare L76X GPS remain distinct configurations; valid data is required before time or position is used. Explicit RTC actions update the named clock.

Shutdown uses the configured manufacturer Witty hook. Loss of SSH alone does not confirm that electrical power has been removed.

Install, update and uninstall WURB, WIRC and Allsky through Windows. Necessary prompts appear in the SSH terminal. Web pages operate installed services. Allsky can use the offered archive releases or official online version. Restore a configuration only to its original software version and Git build.

Select the IMX296 option for a GS camera. Day and night exposures are configured separately with a 15-second limit. Allsky Setup also manages backups and image storage.

## Help and release notes

Help uses the current application version. Current changes are grouped by topic; older releases remain in version history. The Witty website includes its own guide to schedules, services and recordings.

## Changes in 0.8.6

After verified shrinking, a dedicated systemd target starts the installed manufacturer daemon and requests shutdown through its poweroff hook. Normal applications and known expansion services are excluded from this completion boot. Existing special first-boot commands block preparation. Boot/root identities and partition geometry are checked again. Physical power removal still needs device verification. Invalid Witty state 10 remains an error.

SD writing now requests Windows safe eject after complete readback. Progress and target selection reset on success. The backup panel reads the actual ext4 hostname. Setup defaults are wurbi-neu and wURbi, both editable.

## Expansion and removal

Expansion preserves other partition fields and grows ext4 online or through a validated one-shot boot service. Maintenance reboot suppresses an additional manufacturer power cycle. A visible reconnect Cancel button stops retries and closes the connection. Removal updates the backend first and shows live terminal output; partial projects under different users are archived while external settings remain.
