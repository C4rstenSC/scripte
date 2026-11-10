# Raspi-Scripte 1.5 – User guide

Updated: 10 November 2026 · Windows program and Witty homepage · Australian English

## Connect and select a device

Enter the hostname or IP address, username and SSH credentials. Local discovery lists reachable Raspberry Pis. When an IP address is selected, the connection uses that address and refreshes the actual hostname after login. This is especially useful after changing SD cards. Different users retain separate connection profiles.

The program reconnects automatically after a requested restart. Disconnecting manually cancels reconnection. The terminal shows the active operation, progress and errors.

## Update Windows and the Witty Add-on

Update the Windows program to 1.5 first, then the Witty Add-on. The full program package includes the program, updater, content and matching bundled add-on. Manufacturer software and Witty firmware have their own versions and separate update actions.

Update messages take the installed version and build into account and show subsequent changes. Missing or failed device status does not confirm a successful update. Reconnect afterwards and check the reported versions.

Before a base installation or Witty update, the PC time is automatically applied to the Raspberry system clock only when the difference exceeds 48 hours. This preliminary check does not write either RTC or change the time zone. Pressing the PC time button is a separate, explicit action.

## Windows time settings

The UTC selector beside Fixed UTC offset sizes to its content. It contains only:

UTC 00:00, UTC +01:00, UTC +02:00, UTC +06:30, UTC +07:00, UTC +08:00, UTC +08:45, UTC +09:30, UTC +10:00, UTC +10:30, UTC +11:00, UTC +12:00

+06:30 covers the Cocos (Keeling) Islands; +07:00 Christmas Island; +08:00 Western Australia; +08:45 Eucla; +09:30 the Northern Territory/South Australia; +10:00 eastern states; +10:30 South Australian summer time or Lord Howe standard time; +11:00 eastern/Lord Howe daylight time or Norfolk standard time; and +12:00 Norfolk daylight time. Shared offsets appear only once.

Arrows mark +01:00, +02:00, +10:00 and +11:00 for reference. They do not indicate the active mode. Select an offset and press Fixed UTC offset to apply it. A fixed offset stays the same throughout the year.

Automatic daylight saving opens the region selector. Choose, for example, Australia/Sydney for NSW or Australia/Adelaide for South Australia. The region determines clock changes in automatic mode. In fixed mode, the explicitly selected offset takes precedence. A GPS suggestion does not replace an active fixed offset.

The confirmed active mode appears in green. Unknown or stale status leaves the buttons neutral. On connection, a supported reported offset is selected. Repeated unchanged status reports preserve a pending selection. If an older Raspberry reports an excluded offset, the selector remains empty until an allowed value is explicitly chosen; its running time zone is not changed by this display behaviour.

PC time => RPI and Witty RTC transfers and verifies the PC's current UTC instant on the Raspberry and Witty. Existing time-zone rules are retained. The PC clock must be correct.

## Homepage status, clocks and GPS

The homepage displays Linux system time, Witty RTC and, where available, the internal Pi RTC, GPS time, position and satellite counts. Receiver traffic without a position fix is distinct from a valid fix. A visible GPS time does not guarantee a position suitable for solar calculations.

GPS => system time + Witty Pi RTC and GPS => Witty Pi RTC require valid current GPS time. On Witty Pi 5, the current backend runs both as a verified joint Linux/Witty clock synchronisation and also updates an active internal Pi RTC. The second label therefore does not mean an isolated RTC-only correction on this backend. Read the result for the clocks actually synchronised. Allsky continues to use Witty as its automatic startup time source; manual GPS actions are separate.

No GPS, USB GPS and Waveshare L76X are separate configurations. The choice for a future installation and the currently active receiver are different indicators. Check reception and source if there is no fix. GPS does not automatically replace a fixed UTC offset with daylight time.

Additional Witty settings contain power-on at supply, preferred power input, electrical status and the internal Raspberry RTC. RPI - reboot and RPI - shut down appear at the end. Loss of SSH alone does not confirm that power has been disconnected.

## Schedules and script editor

Load an active or saved WPI script directly into the editor. Loading and editing do not change the running schedule. Check BEGIN, END, filename, preview and size validation. Uploading is separate from activation. Replacing an active file of the same name first deactivates it.

Activate is hidden after the END date, using the Witty RTC as the reference. The file can still be loaded or deleted. After activation or deactivation, check the confirmation and next startup/shutdown times. An error message is not a success confirmation.

## WURB, WIRC and recordings

Installation, update, uninstall and homepage buttons apply to the named application. Witty navigation supplements the original pages. WURB uses port 8080, Witty 8081 and WIRC 8082. Manual coordinates accept a decimal comma and N/S/E/W. Wait for saving and verify the position read back; position source and startup profile may be configured separately.

In Recordings, the folder icon and name toggle a folder. File selection and ZIP download remain separate actions. Check the selected files and folders before deleting them.

## Allsky installation and live view

Base installation offers archived sources and current upstream. Choose the source before starting. An interrupted installer is not a completed installation; read the exact terminal error. Back up existing settings before switching software.

Live Video Image in Allsky Setup opens the camera view for manual focusing. The process coordinates camera access with Allsky. Close the popup afterwards and check that a previously running Allsky service has resumed. A previously stopped service should remain stopped. Avoid starting another camera application at the same time.

English is the default for the mobile page on Allsky installations. An explicitly selected German language is remembered. A fixed UTC offset retains priority; automatic daylight saving applies only after automatic mode is selected.

## Write, back up and shrink an SD card

Check the model, OS/image, target card and configuration before writing. The target is overwritten and Windows may request elevated access. Wait for the complete read-back comparison. Rewrite an interrupted card.

Save card images to another drive with enough space. FAT32 cannot hold files larger than 4 GiB. Shrinking uses a RAM maintenance environment with the root filesystem unmounted. The filesystem and partition are checked. A small filesystem alone does not guarantee a small card image. Confirm maintenance completion and actual shutdown at the device. After reinserting the card, allow the intended normal boot or expansion operation to finish.

## Backups, updates and errors

Back up application settings before major changes. Allsky backups include version information and may require the same source revision for restoration. Update backups lists retained backups and old installations; delete only explicitly selected and confirmed entries. Delete Allsky-OLD also removes old captures and settings stored there.

For errors, retain the complete final terminal lines together with the version, action and message. Do not run installation/update jobs in parallel. The SSH console remains available after an update and can be collapsed. Clear Terminal clears only its display. Software checks do not replace testing with the connected Raspberry, Witty, GPS receiver or Windows card reader.

## Release notes

The current release is 1.5, dated 10 November 2026. Separate German and Australian English release notes describe each version/build. The homepage provides version history and Windows Help provides the matching change information. The restricted UTC list in this release applies to the Windows selector.
