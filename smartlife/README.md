# Smart Life Desktop

Windows test release 0.1.4 for temperature sensors, switches, dimmers, blinds and air purifiers. Reads Smart Life home membership and per-device room assignments. Capability-driven controls, read-only sensor values, scenes and a Windows update button.

Download: [Windows setup](downloads/SmartLife-Desktop-0.1.4-Setup.zip). Extract the ZIP and run `Installieren.cmd`. The small setup downloads pinned, hash-verified official Python/PyPI dependencies once. A fully bundled Windows package is supplied separately in the conversation.

## Authentication

User Code + QR confirmation in Smart Life on iPhone. Uses Tuya's official `tuya-device-sharing-sdk` and the public Home Assistant device-sharing registration (`HA_3y9q4ak7g4ephrvke`, `haauthorize`). This is an independent desktop client, not Home Assistant or an official Tuya product. The authorization may appear as Home Assistant in Smart Life. No Home Assistant installation or personal cloud developer project is required. Third-party registration availability for this standalone app is not guaranteed; real account authentication remains unverified.

Tokens are protected using current-user Windows DPAPI. Credentials never enter this repository. macOS Keychain support is present in the core; the Mac package is pending. SmartScreen behavior is not guaranteed: the Python runtime comes from python.org, but this application has no publisher signing certificate.

## Current scope and limits

Homes and rooms with devices are imported. Tuya's sharing SDK only offers per-device room lookup, so empty rooms cannot be reproduced. Device data refreshes every 30 seconds; explicit reload rereads room assignments and specifications. Functions are generated from device specs. Unknown raw/JSON functions are read-only. Existing Smart Life scenes can run and their supplied actions are displayed. Own desktop scenes can be created, edited and executed; they are stored on this PC and do not modify cloud scenes. Fully mapped cloud actions can be copied into a desktop scene. Cloud scene editing and schedule editing remain unavailable through the QR-sharing SDK. Firmware and router management from the Shelly app do not apply to this client.

Checked on Linux: unit tests, mocked cloud responses and offscreen Qt widget interaction. Not yet checked: execution of the Windows runtime, DPAPI on Windows, real QR authentication and the user's devices. The macOS channel explicitly advertises `not_released`.

## Source and updates

- `app/`: cross-platform Python/Qt client and Windows updater.
- `updates/windows.json`, `updates/macos.json`: separate platform manifests.
- `updates/windows/`: versioned app-only ZIPs.
- `runtime-lock.json`: exact Python/PyPI dependency sources and hashes.
- `build/assemble.py`: constructs fully bundled Windows distribution.
- `tests/`: protocol/model, archive and UI tests.

Run tests with dependencies installed: `python -m unittest discover -s tests -v`.
Run preview: `python app/main.py --demo`.

For a release, bump `app/core.py` VERSION, run tests, package `app/` into a versioned ZIP, calculate its SHA-256 and publish the package before its manifest. Do not include `session.dat`, logs or personal data. Future macOS builds need signing, notarization and a tested Mac updater before changing the channel to `available`.

## Third-party notices

Tuya device-sharing SDK: MIT, https://github.com/tuya/tuya-device-sharing-sdk . Public registration reference: https://github.com/home-assistant/core/tree/dev/homeassistant/components/tuya . Python PSF license. PySide6/Qt distributed under LGPLv3/GPLv3 or commercial terms, license notices included in runtime wheel metadata; library binaries remain dynamically replaceable. Other dependencies retain their wheel license metadata. This project does not claim affiliation with Tuya or Home Assistant.

## 0.1.1
Climate-only overview, room tabs in Rooms, Tuya-reported IP addresses, actual blind position separate from target, short follow-up refreshes after blind commands. 23 local tests pass; live blind feedback is pending.

## 0.1.2
Persistently reorderable room tabs, climate-only sensor rows with one temperature per sensor, German numbered function labels and enum values. A targeted read-only device probe exports schema/status metadata while excluding credentials and network addresses. This is diagnostic support, not a verified repair for the user's blind, whose standard schema and status are currently empty. 27 local tests pass.

## 0.1.3
Independent update worker with startup, 60-second and explicit-click checks; cache-busted manifest queries, visible progress/version indicator, and retained manual intent while a check runs. Installation launch exceptions are shown and restore the button state. Future updates use the verified incoming runner. 31 local tests pass, including an update check while the device worker is blocked. Windows installation remains unverified locally.

## 0.1.4
Red update text appears only when a newer version exists. The current-version result leaves the sidebar message empty. Progress and error messages use neutral text. The 60-second check remains enabled.

### Scenes in 0.1.4
German desktop scene editor with device/function/value selection, ordered actions, save/edit/delete, and preflight validation before execution. Cloud scene actions are retained and displayed, and can be copied only when all actions are supported. No undocumented cloud write endpoint is called. Desktop scene execution requires the app to be running; cloud automation continues independently. 39 unit/UI tests and an editor save smoke check pass.
