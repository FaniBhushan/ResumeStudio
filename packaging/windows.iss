#define AppName "Resume Studio"
#define AppVersion GetEnv("APP_VERSION")
#define AppPublisher "Fani Bhushan"

[Setup]
AppId={{7C3512F9-251E-48D0-9EBB-3F46F2F3A845}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={autopf}\Resume Studio
DefaultGroupName={#AppName}
OutputDir=dist-installer
OutputBaseFilename=ResumeStudio-Setup-Windows
ArchitecturesInstallIn64BitMode=x64
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
UninstallDisplayIcon={app}\ResumeStudio.exe

[Files]
Source: "dist\ResumeStudio\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\ResumeStudio.exe"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\ResumeStudio.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\ResumeStudio.exe"; Description: "Launch {#AppName}"; Flags: postinstall nowait skipifsilent
