; zzluxora v8.0.0 — Inno Setup Script
; Build: ISCC.exe zzluxora.iss
; Output: Output/zzluxora-setup-v8.0.0.exe
;
; Prereqs:
;   1. python tools/make_ico.py   (logo_256.png → zzluxora.ico)
;   2. python build.py            (PyInstaller onedir → results/zzluxora-v8/)
;   3. ISCC.exe installer/zzluxora.iss

#define MyAppName "zzluxora"
#define MyAppVersion "8.0.0"
#define MyAppPublisher "UNNES - Teknik Komputer"
#define MyAppExeName "zzluxora.exe"
#define MyAppIcon "..\assets\zzluxora.ico"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppVerName={#MyAppName} {#MyAppVersion}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=Output
OutputBaseFilename={#MyAppName}-setup-v{#MyAppVersion}
SetupIconFile={#MyAppIcon}
UninstallDisplayIcon={#MyAppIcon}
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
VersionInfoVersion=8.0.0.0
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}

; Clean install: delete old app folder before copy (anti-tumpuk)
[InstallDelete]
Type: filesandordirs; Name: "{app}\*"

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create desktop shortcut"; GroupDescription: "Additional shortcuts:"
Name: "cleandata"; Description: "Remove old settings and data from AppData (clean reset)"; GroupDescription: "Data options:"

[Files]
Source: "..\results\zzluxora-v8\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{#MyAppIcon}"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{#MyAppIcon}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent

[Registry]
Root: HKCR; Subkey: ".zlx"; ValueType: string; ValueName: ""; ValueData: "zzluxora.Project"; Flags: uninsdeletevalue
Root: HKCR; Subkey: "zzluxora.Project"; ValueType: string; ValueName: ""; ValueData: "zzluxora Project File"; Flags: uninsdeletekey
Root: HKCR; Subkey: "zzluxora.Project\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"
Root: HKCR; Subkey: "zzluxora.Project\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""

[UninstallDelete]
Type: dirifempty; Name: "{app}"

[Code]
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  DataDir: String;
begin
  if CurUninstallStep = usPostUninstall then
  begin
    DataDir := ExpandConstant('{userappdata}\zzluxora');
    if DirExists(DataDir) then
    begin
      if MsgBox('Keep your settings, fixtures, and project data?' + #13#10 + #13#10 +
                'Yes = Keep data (for reinstall later)' + #13#10 +
                'No = Delete all data permanently',
                mbConfirmation, MB_YESNO) = IDNO then
        DelTree(DataDir, True, True, True);
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  DataDir: String;
begin
  if CurStep = ssPostInstall then
  begin
    if IsTaskSelected('cleandata') then
    begin
      DataDir := ExpandConstant('{userappdata}\zzluxora');
      if DirExists(DataDir) then
        DelTree(DataDir, True, True, True);
    end;
  end;
end;
