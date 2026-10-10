# Raspi-Scripte 0.7.1 – User guide (9 October 2026)

## Updates
Use the Windows Update button. The modular program package includes the application DLLs, updater, help and Witty Add-on 0.7.1. Downloads are automatically decrypted and checked against SHA-256 checksums. Connection profiles and an existing activation are retained. Keep the computer and Raspberry Pi powered on until the updater finishes.

Program updates use Raspi-Scripte-Programm.zip.enc; content updates use Raspi-Scripte-Modular-Content.zip.enc and modular-update-manifest.json. A content update cannot replace compiled application code. Older single-EXE installations need a one-time migration: extract the complete small ZIP into a writable folder and run START.cmd, which installs the .NET 8 Desktop Runtime if needed. Normal small updates are available afterwards.

Connect before using the Witty update button. Witty can also update through its web page. The latest package contains all GPS, RTC, web-page and software detection changes through 0.6.62, plus the Allsky source selection in 0.7.0.

## Base installation and Allsky
Connect to the new Raspberry Pi and open Base installation. Check the detected Pi and Witty models, country, timezone, keyboard, GPS and selected applications. Australia defaults to Australia/Sydney; adjust the timezone if you are elsewhere in Australia.

Enable Install Allsky, then select Current version – 01.10.2026 (v2026.10.01) or Previous version – 06.12.2024 (revision 06, v2024.12.06_06). Both are encrypted original snapshots from the author's GitHub. The current release is split into multiple files because of GitHub's size limit; the installer combines and decrypts them automatically. All checksums and the exact original Git commit are verified.

Allsky's official installer runs last. Internet access for dependencies and a supported connected camera are still required. The version selection applies to the base installer, not the separate application manager. A different existing Allsky version is never overwritten. Back up settings before uninstalling or reinstalling. On an already configured system the base installer may be disabled; this selection is then available on a fresh installation. Backups across different Allsky versions are not guaranteed compatible.

## GPS, clocks and software detection
Select USB GPS, Waveshare L76X or No GPS. USB preparation does not require a connected receiver. Pi 4 lets WURB read the USB receiver directly; Pi 5 uses gpsd and the shared NMEA bridge. Complete original NMEA fields, satellite counts, HDOP and fix quality are retained. USB gpsd is read-only and the bridge reconnects after a gpsd restart. No additional USB driver is included.

The Witty page distinguishes no receiver traffic, traffic without a position fix and a valid fix. Visible satellites alone do not imply a position fix. Use GPS diagnostics and inspect the terminal if readings are missing. The absent receiver stream on Dad's actual Raspberry Pi has not yet been proven fixed by the simulated tests.

Use GPS clock synchronisation with valid GPS time. An enabled Pi 5 RTC is included when present. Manually setting Linux time is a separate action. Required package tools, including hwclock where needed, are prepared automatically and package-manager errors are shown in the terminal.

Witty Add-on and manufacturer software have separate status rows. Witty Pi 4 manufacturer software is labelled as Pi 4 even with an unknown version; WP5 is detected outside PATH. An unknown version no longer means the software is missing. Hardware and installed software models are detected separately.

## Backups, help and release notes
Application settings backups can be downloaded and restored from Windows. Allsky backups include overlay layouts, settings, module and website configuration, and the storage path. Captures, dark frames and application files are not part of the settings backup. Check the overlay editor, storage path and service after restoring.

The SSH terminal can be shown or hidden beside its heading. Status panels and installation controls require a connection. German release notes for Windows and Witty are included; Witty has its own version history and an offline bundled copy. Upstream application and manufacturer histories remain separate.

Package encryption, ZIP integrity, both original Allsky snapshots and the Windows x64 build were checked. Native Windows launch and physical Raspberry Pi tests remain pending. New main application files are unsigned.

## Required Allsky backup version match
New backups record the Allsky release and original Git revision. Restore is allowed only on the identical software revision. A mismatch displays the backup and installed versions before any files or services are changed. Old backups without a recorded version are rejected as unknown. This applies to Windows, the Witty web page and automatic post-update restores. Create a new backup after changing Allsky version. A previous-version backup can only be restored to its original matching version.

Standalone Allsky: Sunwait and additional modules are also included in an encrypted support package in the same repository. Installation uses local Git sources. Raspberry Pi OS and Python package repositories are still required.

The third Allsky source downloads the latest default branch directly from Allsky GitHub, including Sunwait. It requires upstream availability; the two encrypted archives remain independent. All sources receive the same camera, Trixie, navigation and first-boot adjustments. Software updates retain the selected source.

Pi 5 GPS: loss of the receiver or fix makes WURB use its saved Default position. A new valid fix automatically restores live GPS coordinates and the real satellite count. The manual position stays saved.

## Micro SD card options and hostname

The red framed group below installation/update contains a green indicator for expanded partitions, red for shrunk partitions and grey for an unknown or unsupported layout. Both partition actions require Yes/No confirmation.

Shrink prepares a verified RAM maintenance image and reboots once. All services stop during this maintenance reboot. The unmounted ext4 filesystem is shrunk first, then the root partition, retaining 512 MiB free space. The Pi powers off afterwards. Do not remove power during maintenance. The boot partition stores the log and original partition table (`witty-sd-result.txt`, `witty-sd-partitions.before`). Normal boot configuration is restored before changes. Only a standard Micro SD with exactly a FAT boot partition and a final ext4 root partition is supported. USB/NVMe/LVM/encrypted root systems are rejected. The installed tools from `initramfs-tools`, `e2fsprogs`, `util-linux` and `fdisk` are required; missing tools stop preparation before changes. Have a current backup.

Expand uses the same `raspi-config` method as the base installer and reboots the Pi. Reconnect to read the actual partition state.

Adjust settings displays the current hostname beside the new hostname field. Apply changes updates hostname and existing managed hotspot SSIDs: WURB `wifi4bats-<hostname>`, Allsky `allskywifi-<hostname>`, otherwise `wifi-<hostname>`. The wireless password and other network settings remain unchanged. Active hotspots adopt the name after a short delay; wireless/SSH may disconnect briefly. Cancel makes no changes.

The actually active GPS receiver is highlighted light green independently of the selection for a future installation.


Both GPS buttons now synchronise Linux, the Witty RTC and the enabled Pi RTC through the same verified procedure. Witty display timing is measured when its RTC line is read, without a fixed seconds offset.


0.7.1: Allsky versions: archive 01.10.2026 and archive 06.12.2024 (Carsten Github); latest (Github ALLSKY). Software install/uninstall is available only in Windows. Web service controls show only installed services.

### Global Shutter camera (IMX296)
Connect the GS camera before installation and select the GS camera checkbox in the base installer or Allsky installation dialog. All three Allsky sources receive the IMX296 camera profile. No temporary replacement camera is required.
Selecting the checkbox caps day/night auto exposure and initial manual exposure at 15,000 ms (15 seconds), preserving shorter values. Allsky uses its own auto-exposure algorithm within those limits. Allsky - Setup provides the same setting and shows actual day/night maximum exposure in seconds. A running service is stopped briefly to apply changes and then restarted. Turning the setting off retains current exposure values. Later manual Allsky changes are preserved, including during Allsky updates.

### Exposure times on Allsky - Setup
Four fields show the actual Allsky manual/starting exposure and maximum automatic exposure for day and night. All inputs use seconds. Separate checkboxes enable or disable day/night automatic exposure. Apply exposure times saves the values to Allsky, reads them back for confirmation and restarts a previously running capture service. A stopped service remains stopped. Startup errors restore the previous settings.
A GS camera displays a red maximum 15 seconds recommended message, including on the native Allsky homepage. GS defaults cap both automatic maxima at 15 seconds. Location/sun-angle day/night switching and Allsky brightness-based exposure calculation use these limits. Later deliberate changes are permitted within camera capability limits.
All four exposure values, automatic mode selection and GS profile flag are included in settings.json/options.json configuration backups and restores via the webpage and Windows, including update restores. Backups remain restricted to the exact same Allsky software version and Git revision.

## Paketinstallation / Package installation

Base installation uses the original foreground APT dialogs. Every 20 seconds the terminal reports package process states. Update directly from the latest 0.7.0 build; no intermediate package is needed.

Micro-SD status checks the partition and ext4 filesystem separately. Green requires both to use available space. Linux updates on a fresh image run directly in the SSH terminal without first installing Witty.

The Raspberry Pi connection is checked over SSH every 5 seconds. Loss turns the indicator red and displays one warning; acknowledging OK disconnects the session. Above the SSH terminal, base installation shows the current step, configured total and package downloads including dependencies. Percentages refer to completed steps, not remaining time.

Base installation no longer expands the SD partition or filesystem. Raspberry Pi OS handles automatic expansion on first boot. Manual expansion remains available under Micro SD card options.

After downloading, package progress also shows preparation, unpacking, configuration and finalisation with package names and counters. Cached packages are counted separately from downloads. Terminal process-group faults fixed in Witty add-on prerequisites, WURB/WIRC repair and individual installation, GPS configuration and Witty Pi 4 installation: outer and inner timed package calls preserve the foreground terminal. Missing Pi 5 hwclock is installed with base dependencies. Automatic expansion remains removed from base installation; manual SD controls are retained.
