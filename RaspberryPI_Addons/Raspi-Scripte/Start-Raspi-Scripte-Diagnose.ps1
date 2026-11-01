param([string]$Programm = '')
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Windows.Forms
try {
    $contentAssets = Join-Path $env:LOCALAPPDATA 'Raspi-Scripte\Content\Assets'
    $hook = Join-Path $contentAssets 'Raspi-Scripte-Diagnostics.dll'
    if (-not (Test-Path -LiteralPath $hook -PathType Leaf)) {
        throw 'Bitte zuerst im bisherigen Windows-Programm den Inhaltsupdate auf 1.1.3.8 installieren und das Programm danach schliessen.'
    }
    $saved = Join-Path $env:LOCALAPPDATA 'Raspi-Scripte\diagnose-programmpfad.txt'
    if (-not $Programm -and (Test-Path -LiteralPath $saved)) { $Programm = (Get-Content -LiteralPath $saved -Raw).Trim() }
    if (-not $Programm -or -not (Test-Path -LiteralPath $Programm -PathType Leaf)) {
        $dialog = New-Object System.Windows.Forms.OpenFileDialog
        $dialog.Title = 'Vorhandene Raspi-Scripte.exe auswaehlen (wird nicht ersetzt)'
        $dialog.Filter = 'Raspi-Scripte.exe|Raspi-Scripte.exe'
        if ($dialog.ShowDialog() -ne [Windows.Forms.DialogResult]::OK) { exit }
        $Programm = $dialog.FileName
    }
    $Programm = (Resolve-Path -LiteralPath $Programm).Path
    if ([IO.Path]::GetFileName($Programm) -ine 'Raspi-Scripte.exe') { throw 'Bitte die vorhandene Raspi-Scripte.exe auswaehlen.' }
    $sameProgram = @(Get-Process -Name 'Raspi-Scripte' -ErrorAction SilentlyContinue)
    if ($sameProgram.Count -gt 0) { throw 'Bitte Raspi-Scripte vollstaendig schliessen und diesen Starter erneut anklicken. Eine bereits laufende Instanz kann die Inhalts-DLL nicht nachtraeglich laden.' }
    [IO.File]::WriteAllText($saved, $Programm)
    $persistentStarter = Join-Path $contentAssets 'Start-Raspi-Scripte-Diagnose.ps1'
    if (-not (Test-Path -LiteralPath $persistentStarter)) { throw 'Der Starter fehlt im Inhaltspaket 1.1.3.8.' }
    $shell = New-Object -ComObject WScript.Shell
    $link = $shell.CreateShortcut((Join-Path ([Environment]::GetFolderPath('Desktop')) 'Raspi-Scripte mit Diagnose.lnk'))
    $link.TargetPath = Join-Path $PSHOME 'powershell.exe'
    $link.Arguments = '-NoProfile -STA -WindowStyle Hidden -ExecutionPolicy Bypass -File "' + $persistentStarter + '"'
    $link.WorkingDirectory = Split-Path -Parent $Programm
    $link.IconLocation = $Programm + ',0'
    $link.Description = 'Vorhandenes Raspi-Scripte mit Diagnosebuttons aus den Inhaltsdateien starten'
    $link.Save()
    $start = New-Object System.Diagnostics.ProcessStartInfo
    $start.FileName = $Programm
    $start.WorkingDirectory = Split-Path -Parent $Programm
    $start.UseShellExecute = $false
    # Process-scoped only. No registry/global/user environment changes.
    $start.EnvironmentVariables['DOTNET_STARTUP_HOOKS'] = $hook
    [Diagnostics.Process]::Start($start) | Out-Null
} catch {
    [Windows.Forms.MessageBox]::Show($_.Exception.Message, 'Raspi-Scripte Diagnose-Starter') | Out-Null
    exit 1
}
