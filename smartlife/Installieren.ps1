$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem
$source = $PSScriptRoot
$target = Join-Path $env:LOCALAPPDATA 'Programs\SmartLifeDesktop'
$stage = Join-Path $env:TEMP ('SmartLife-setup-' + [guid]::NewGuid().ToString('N'))
try {
 New-Item -ItemType Directory -Force -Path $target,$stage | Out-Null
 $runtime = Join-Path $target 'runtime'
 if (!(Test-Path (Join-Path $runtime 'pythonw.exe'))) {
  if (Test-Path (Join-Path $source 'runtime\pythonw.exe')) {
   Copy-Item (Join-Path $source 'runtime') $target -Recurse -Force
  } else {
   $lock = Get-Content (Join-Path $source 'runtime-lock.json') -Raw | ConvertFrom-Json
   $items = @($lock.python) + @($lock.wheels)
   foreach ($item in $items) {
    Write-Host ('Lade ' + $item.file)
    $file = Join-Path $stage $item.file
    Invoke-WebRequest -UseBasicParsing -Uri $item.url -OutFile $file
    if ((Get-FileHash $file -Algorithm SHA256).Hash.ToLowerInvariant() -ne $item.sha256) {throw ('Pruefsumme falsch: ' + $item.file)}
   }
   $newRuntime=Join-Path $stage 'runtime'
   [IO.Compression.ZipFile]::ExtractToDirectory((Join-Path $stage $lock.python.file),$newRuntime)
   $site=Join-Path $newRuntime 'Lib\site-packages';New-Item -ItemType Directory -Path $site -Force | Out-Null
   foreach ($item in $lock.wheels) { [IO.Compression.ZipFile]::ExtractToDirectory((Join-Path $stage $item.file),$site) }
   [IO.File]::WriteAllText((Join-Path $newRuntime 'python313._pth'),"python313.zip`r`n.`r`nLib/site-packages`r`nimport site`r`n")
   if (Test-Path $runtime) {Remove-Item $runtime -Recurse -Force}
   Move-Item $newRuntime $runtime
  }
 }
 # Only our application folder; credentials remain in LocalAppData\SmartLifeDesktop.
 if ((Get-Process pythonw -ErrorAction SilentlyContinue | Where-Object {$_.Path -eq (Join-Path $runtime 'pythonw.exe')})) {throw 'Bitte Smart Life Desktop vor der Installation schliessen.'}
 $newApp=Join-Path $stage 'app';Copy-Item (Join-Path $source 'app') $newApp -Recurse -Force
 $oldApp=Join-Path $target 'app';$backup=Join-Path $target 'app.setup-backup'
 if (Test-Path $backup) {Remove-Item $backup -Recurse -Force}
 if (Test-Path $oldApp) {Move-Item $oldApp $backup}
 try {
  Move-Item $newApp $oldApp
  foreach ($name in @('launcher.pyw','Starten.vbs','Anleitung.txt','runtime-lock.json')) {Copy-Item (Join-Path $source $name) $target -Force}
 } catch {
  if (Test-Path $oldApp) {Remove-Item $oldApp -Recurse -Force}
  if (Test-Path $backup) {Move-Item $backup $oldApp}
  throw
 }
 $shell=New-Object -ComObject WScript.Shell
 $link=$shell.CreateShortcut((Join-Path ([Environment]::GetFolderPath('Desktop')) 'Smart Life Desktop.lnk'))
 $link.TargetPath=Join-Path $runtime 'pythonw.exe';$link.Arguments='"'+(Join-Path $target 'launcher.pyw')+'"';$link.WorkingDirectory=$target;$link.Save()
 Start-Process -FilePath (Join-Path $runtime 'pythonw.exe') -ArgumentList ('"'+(Join-Path $target 'launcher.pyw')+'"') -WorkingDirectory $target
} catch {Write-Host $_.Exception.Message -ForegroundColor Red;exit 1}
finally {if (Test-Path $stage) {Remove-Item $stage -Recurse -Force -ErrorAction SilentlyContinue}}
