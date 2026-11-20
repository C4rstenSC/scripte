Option Explicit
Dim sh, fs, folder, exe
Set sh = CreateObject("WScript.Shell")
Set fs = CreateObject("Scripting.FileSystemObject")
folder = fs.GetParentFolderName(WScript.ScriptFullName)
exe = folder & "\runtime\pythonw.exe"
If Not fs.FileExists(exe) Then
 MsgBox "Bitte zuerst Installieren.cmd starten.", 48, "Smart Life Desktop"
Else
 sh.CurrentDirectory = folder
 sh.Run Chr(34) & exe & Chr(34) & " " & Chr(34) & folder & "\launcher.pyw" & Chr(34), 1, False
End If
