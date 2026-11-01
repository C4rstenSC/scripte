param([string]$Programmordner = '', [string]$Paket = '')
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2
$expectedZip = '1fa142ba4e9b82f72b60e99a69438b6a8e2102ad2eace1d870ea3919de2ec36b'
$stage = $null
try {
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    if (-not $Paket) {
        $cache = Join-Path $env:LOCALAPPDATA 'Raspi-Scripte\Update'
        $candidates = @(Get-ChildItem -LiteralPath $cache -Filter 'Raspi-Scripte-Module.zip' -Recurse -ErrorAction SilentlyContinue)
        foreach ($candidate in $candidates) {
            if ((Get-FileHash -LiteralPath $candidate.FullName -Algorithm SHA256).Hash -eq $expectedZip) { $Paket = $candidate.FullName; break }
        }
    }
    if (-not $Paket -or -not (Test-Path -LiteralPath $Paket)) {
        throw 'Bitte zuerst im Windows-Programm das Update auf 1.1.3.7 herunterladen. Die bekannte Fehlermeldung danach schliessen und Raspi-Scripte beenden. Anschliessend dieses Reparaturscript erneut starten.'
    }
    if ((Get-FileHash -LiteralPath $Paket -Algorithm SHA256).Hash -ne $expectedZip) { throw 'Falsches oder unvollstaendiges Paket. Erwartet wird exakt das Modulpaket 1.1.3.7.' }
    if (-not $Programmordner) {
        $dialog = New-Object System.Windows.Forms.OpenFileDialog
        $dialog.Title = 'Vorhandene Raspi-Scripte.exe im Programmordner auswaehlen'
        $dialog.Filter = 'Raspi-Scripte.exe|Raspi-Scripte.exe'
        if ($dialog.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) { throw 'Abgebrochen. Keine Programmdatei wurde geaendert.' }
        $Programmordner = Split-Path -Parent $dialog.FileName
    }
    $Programmordner = (Resolve-Path -LiteralPath $Programmordner).Path
    foreach ($name in @('Raspi-Scripte.exe','Raspi-Scripte-Updater.exe','Raspi-Scripte.dll')) {
        if (-not (Test-Path -LiteralPath (Join-Path $Programmordner $name) -PathType Leaf)) { throw "Programmordner unvollstaendig: $name fehlt." }
    }
    if (@(Get-Process -Name 'Raspi-Scripte','Raspi-Scripte-Updater' -ErrorAction SilentlyContinue).Count -gt 0) { throw 'Bitte Raspi-Scripte und dessen Updater vollstaendig beenden und das Reparaturscript erneut starten.' }
    try {
        $probe = [IO.File]::Open((Join-Path $Programmordner 'Raspi-Scripte.dll'), [IO.FileMode]::Open, [IO.FileAccess]::Write, [IO.FileShare]::Read)
        $probe.Dispose()
    } catch [UnauthorizedAccessException] {
        # Preserve the resolved paths if UAC runs under a different profile.
        $arguments = '-NoProfile -ExecutionPolicy Bypass -File "' + $PSCommandPath + '" -Programmordner "' + $Programmordner + '" -Paket "' + $Paket + '"'
        Start-Process -FilePath 'powershell.exe' -Verb RunAs -ArgumentList $arguments -Wait
        exit
    }
    $stage = Join-Path ([IO.Path]::GetTempPath()) ('Raspi-Modulreparatur-' + [Guid]::NewGuid().ToString('N'))
    [IO.Directory]::CreateDirectory($stage) | Out-Null
    $archive = [IO.Compression.ZipFile]::OpenRead($Paket)
    try {
        $names = @('Raspi-Scripte.dll','Raspi-Scripte.deps.json','Raspi-Scripte.runtimeconfig.json','Raspi-Scripte-Updater.dll','Raspi-Scripte-Updater.deps.json','Raspi-Scripte-Updater.runtimeconfig.json')
        $allowed = @($names) + 'module-update.json'
        if ($archive.Entries.Count -ne 7) { throw 'Unerwarteter Paketinhalt.' }
        foreach ($entry in $archive.Entries) {
            if ($allowed -cnotcontains $entry.FullName -or $entry.Length -eq 0) { throw 'Unerwartete oder leere Paketdatei.' }
        }
        foreach ($name in $allowed) {
            $matches = @($archive.Entries | Where-Object { $_.FullName -ceq $name })
            if ($matches.Count -ne 1) { throw "Paketdatei fehlt oder ist doppelt: $name" }
            [IO.Compression.ZipFileExtensions]::ExtractToFile($matches[0], (Join-Path $stage $name), $false)
        }
    } finally { $archive.Dispose() }
    $manifest = Get-Content -LiteralPath (Join-Path $stage 'module-update.json') -Raw | ConvertFrom-Json
    if ($manifest.Version -ne '1.1.3.7') { throw 'Falsche Modulversion.' }
    if (@($manifest.Files.PSObject.Properties).Count -ne 6) { throw 'Unvollstaendiges Modulmanifest.' }
    foreach ($name in $names) {
        $hash = (Get-FileHash -LiteralPath (Join-Path $stage $name) -Algorithm SHA256).Hash
        if ($hash -ne $manifest.Files.$name) { throw "Pruefsumme stimmt nicht: $name" }
    }
    $backup = Join-Path $env:LOCALAPPDATA ('Raspi-Scripte\ReparaturBackup\' + [Guid]::NewGuid().ToString('N'))
    [IO.Directory]::CreateDirectory($backup) | Out-Null
    $existing = @{}
    foreach ($name in $names) {
        $destination = Join-Path $Programmordner $name
        $existing[$name] = Test-Path -LiteralPath $destination -PathType Leaf
        if ($existing[$name]) { Copy-Item -LiteralPath $destination -Destination (Join-Path $backup $name) }
    }
    $written = New-Object 'System.Collections.Generic.List[string]'
    try {
        foreach ($name in $names) {
            $written.Add($name)
            Copy-Item -LiteralPath (Join-Path $stage $name) -Destination (Join-Path $Programmordner $name) -Force
            if ((Get-FileHash -LiteralPath (Join-Path $Programmordner $name) -Algorithm SHA256).Hash -ne $manifest.Files.$name) { throw "Kopierpruefung fehlgeschlagen: $name" }
        }
    } catch {
        $originalError = $_
        $rollbackErrors = @()
        foreach ($name in $written) {
            try {
                if ($existing[$name]) { Copy-Item -LiteralPath (Join-Path $backup $name) -Destination (Join-Path $Programmordner $name) -Force }
                else { Remove-Item -LiteralPath (Join-Path $Programmordner $name) -Force -ErrorAction Stop }
            } catch { $rollbackErrors += $_.Exception.Message }
        }
        throw ($originalError.Exception.Message + "`nSicherung: " + $backup + "`nRuecknahmefehler: " + ($rollbackErrors -join '; '))
    }
    [Windows.Forms.MessageBox]::Show("Windows-Modul 1.1.3.7 wurde geprueft eingespielt. Bitte Raspi-Scripte jetzt selbst starten. Die passenden Inhalte werden beim Start geladen. Keine EXE wurde ersetzt; am Raspberry wurde nichts veraendert.`n`nSicherung: $backup", 'Modulreparatur erfolgreich') | Out-Null
} catch {
    [Windows.Forms.MessageBox]::Show($_.Exception.Message, 'Modulreparatur nicht abgeschlossen') | Out-Null
    exit 1
} finally {
    if ($stage -and (Test-Path -LiteralPath $stage)) { Remove-Item -LiteralPath $stage -Recurse -Force -ErrorAction SilentlyContinue }
}
