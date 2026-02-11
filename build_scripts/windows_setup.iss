[Setup]
AppName=Bogas Bogas Go
AppVersion={#AppVersion}
DefaultDirName={autopf}\BogasBogasGo
OutputDir=Output
OutputBaseFilename=bogasbogasgo_installer_v{#AppVersion}-win_x64
SetupIconFile=assets/icon.ico

[Files]
; Copy everything PyInstaller built
Source: "dist\BogasBogasGo\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
; Create the desktop icon
Name: "{autodesktop}\Bogas Bogas Go"; Filename: "{app}\BogasBogasGo.exe"