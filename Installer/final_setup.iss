[Setup]
AppName=Vision+® Medical Imaging
AppVersion=1.0.0
AppPublisher=Dr. Tariq Alagha
AppPublisherURL=https://mednextapp.com
DefaultDirName={autopf}\Vision+
DefaultGroupName=Vision+
OutputDir={userdesktop}\Vision
OutputBaseFilename=Vision+_Setup
Compression=lzma2/ultra64
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64

[Files]
Source: "{userdesktop}\Vision\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\Vision+"; Filename: "{app}\Vision+.exe"
Name: "{commondesktop}\Vision+"; Filename: "{app}\Vision+.exe"