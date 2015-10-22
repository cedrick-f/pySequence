
;This file is part of pySequence
;
; Copyright (C) 2012-2015 Cédrick FAURY
;
;pySequence is free software; you can redistribute it and/or modify
;it under the terms of the GNU General Public License as published by
;the Free Software Foundation; either version 3 of the License, or
;(at your option) any later version.
;
;pySequence is distributed in the hope that it will be useful,
;but WITHOUT ANY WARRANTY; without even the implied warranty of
;MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;GNU General Public License for more details.
;
;You should have received a copy of the GNU General Public License
;along with pySequence; if not, write to the Free Software
;Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

[ISPP]
#define AppName "pySequence"
#define AppVersion "6.0-beta.29"
#define AppVersionInfo "6.0.0.29"
#define AppVersionBase "6"

#define AppURL "https://github.com/cedrick-f/pySequence"

[Setup]
;Informations générales sur l'application

AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}

AppPublisher=Cédrick Faury
AppCopyright=Copyright © 2011-2015 Cédrick Faury
VersionInfoVersion = {#AppVersionInfo}

;Répertoire de base contenant les fichiers
SourceDir=D:\Developpement\pySequence

;Repertoire d'installation
DefaultDirName={pf}\{#AppName}
DefaultGroupName={#AppName}
LicenseFile=LICENSE.txt

;Paramètres de compression
;lzma ou zip
Compression=lzma/max
SolidCompression=yes

;Par défaut, pas besoin d'être administrateur pour installer
PrivilegesRequired=none

;Nom du fichier généré et répertoire de destination
OutputBaseFilename=setup_pySequence_{#AppVersion}_win32
OutputDir=releases

UninstallDisplayIcon={app}\logo.ico

;Fenêtre en background
WindowResizable=false
WindowStartMaximized=true
WindowShowCaption=true
BackColorDirection=lefttoright

AlwaysUsePersonalGroup=no
ChangesAssociations=yes



[Messages]
BeveledLabel=pySequence {#AppVersion} installation

[Languages]
Name: fr; MessagesFile: "compiler:Languages\French.isl"

[CustomMessages]
;
; French
;
fr.uninstall=Désinstaller
fr.gpl_licence=Prendre connaissance du contrat de licence pour le logiciel
fr.fdl_licence=Prendre connaissance du contrat de licence pour la documentation associée
fr.CreateDesktopIcon=Créer un raccourci sur le bureau vers
fr.AssocFileExtension=&Associer le programme pySequence aux extensions .seq et .prj
fr.CreateQuickLaunchIcon=Créer un icône dans la barre de lancement rapide
fr.FileExtensionNameSeq=Fiche de Séquence pédagogique
fr.FileExtensionSeq=pySequence.sequence
fr.FileExtensionNamePrj=Fiche de validation de Projet
fr.FileExtensionPrj=pySequence.projet
fr.InstallFor=Installer pour :
fr.AllUsers=Tous les utilisateurs
fr.JustMe=Seulement moi
fr.ShortCut=Raccourcis :
fr.Association=Association de fichier :


[Files]
;
; Fichiers de la distribution
;
Source: src\build\*.*; DestDir: {app}; Flags : ignoreversion recursesubdirs;
;Source: *.txt; DestDir: {app}; Flags : ignoreversion;
;Source: Images\*.ico; DestDir: {app}\Images; Flags : ignoreversion;
;Source: Images\*.png; DestDir: {app}\Images; Flags : ignoreversion;
;Source: locale\en\LC_MESSAGES\*.mo; DestDir: {app}\locale\en\LC_MESSAGES; Flags : ignoreversion;

;
; Fichiers exemples
;
;Source: Exemples\*.seq; DestDir: {app}\Exemples; Flags : ignoreversion;
;Source: Exemples\*.prj; DestDir: {app}\Exemples; Flags : ignoreversion;


; les dll C++
;Source: src\msvcr90.dll; DestDir: {app}\bin; Flags : ignoreversion;
;Source: src\*.manifest; DestDir: {app}\bin; Flags : ignoreversion;

; des fichiers à mettre dans le dossier "Application data"
;Source: {src};  DestDir: {code:DefAppDataFolder}\Test\;

[Tasks]
Name: desktopicon2; Description: {cm:CreateDesktopIcon} {#AppName} ;GroupDescription: {cm:ShortCut}; MinVersion: 4,4
Name: fileassoc; Description: {cm:AssocFileExtension};GroupDescription: {cm:Association};
Name: common; Description: {cm:AllUsers}; GroupDescription: {cm:InstallFor}; Flags: exclusive
Name: local;  Description: {cm:JustMe}; GroupDescription: {cm:InstallFor}; Flags: exclusive unchecked

[Icons]
Name: {group}\{#AppName}; Filename: {app}\bin\Sequence.exe; WorkingDir: {app}\bin; IconFileName: {app}\bin\Sequence.exe
Name: {group}\{cm:uninstall} {#AppName}; Filename: {app}\unins000.exe;  IconFileName: {app}\unins000.exe
;
; On ajoute sur le Bureau l'icône pySequence
;
Name: {code:DefDesktop}\{#AppName} {#AppVersionBase};   Filename: {app}\bin\Sequence.exe; WorkingDir: {app}\bin; MinVersion: 4,4; Tasks: desktopicon2; IconFileName: {app}\bin\Sequence.exe


[_ISTool]
Use7zip=true


[Registry]
; Tout ce qui concerne les fichiers .seq et .prj
Root: HKCR; SubKey: "{cm:FileExtensionSeq}"; ValueType: string;  ValueName: ""; ValueData: "{cm:FileExtensionNameSeq}";  Flags: uninsdeletekey
Root: HKCR; Subkey: "{cm:FileExtensionSeq}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\bin\fichier_seq.ico,0"; Flags: uninsdeletekey
Root: HKCR; SubKey: "{cm:FileExtensionSeq}\Shell\Open"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\bin\Sequence.exe"; Flags: uninsdeletekey
Root: HKCR; SubKey: "{cm:FileExtensionSeq}\Shell\Open\Command"; ValueType: string; ValueName: ""; ValueData: """{app}\bin\Sequence.exe"" ""%1"""; Flags: uninsdeletekey
Root: HKCR; Subkey: ".seq"; ValueType: string; ValueName: ""; ValueData: "{cm:FileExtensionSeq}"; Flags: uninsdeletevalue

Root: HKCR; SubKey: .prj; ValueType: string; ValueData: {cm:FileExtensionPrj}; Flags: uninsdeletevalue
Root: HKCR; SubKey: {cm:FileExtensionPrj}; ValueType: string; ValueData: "{cm:FileExtensionNamePrj}";  Flags: uninsdeletekey 
Root: HKCR; SubKey: {cm:FileExtensionPrj}\Shell\Open\Command; ValueType: string; ValueData: """{app}\bin\Sequence.exe"" ""%1"""; Flags: uninsdeletekey
Root: HKCR; Subkey: {cm:FileExtensionPrj}\DefaultIcon; ValueType: string; ValueData: "{app}\bin\fichier_prj.ico,0"; Flags: uninsdeletekey


; Pour stocker le style d'installation : "All users" ou "Current user"
Root: HKLM; Subkey: SOFTWARE\{#AppName}; Flags: uninsdeletekey
Root: HKLM; Subkey: SOFTWARE\{#AppName}; ValueType: string; ValueName: DataFolder; ValueData: {code:DefAppDataFolder}\{#AppName} ; Flags: uninsdeletekey
Root: HKLM; Subkey: SOFTWARE\{#AppName}; ValueType: string; ValueName: UninstallPath ; ValueData: {uninstallexe}; Flags: uninsdeletekey



[Code]
Procedure URLLabelOnClick(Sender: TObject);
var
  ErrorCode: Integer;
begin
  ShellExec('open', 'http://fauryc.free.fr/spip.php?rubrique7', '', '', SW_SHOWNORMAL, ewNoWait, ErrorCode);
end;

{*** INITIALISATION ***}
Procedure InitializeWizard;
var
  URLLabel: TNewStaticText;
begin
  URLLabel := TNewStaticText.Create(WizardForm);
  URLLabel.Caption := 'http://fauryc.free.fr';
  URLLabel.Cursor := crHand;
  URLLabel.OnClick := @URLLabelOnClick;
  URLLabel.Parent := WizardForm;
  { Alter Font *after* setting Parent so the correct defaults are inherited first }
  URLLabel.Font.Style := URLLabel.Font.Style + [fsUnderline];
  URLLabel.Font.Color := clBlue;
  URLLabel.Top := WizardForm.ClientHeight - URLLabel.Height - 15;
  URLLabel.Left := ScaleX(20);
end;


{ Renvoie le dossier "Application Data" à utiliser }
function DefAppDataFolder(Param: String): String;
begin
  if IsTaskSelected('common') then
    Result := ExpandConstant('{commonappdata}')
  else
    Result := ExpandConstant('{localappdata}')
end;


{ Renvoie le bureau sur lequel placer le raccourci de pySequence }
function DefDesktop(Param: String): String;
begin
  if IsTaskSelected('common') then
    Result := ExpandConstant('{commondesktop}')
  else
    Result := ExpandConstant('{userdesktop}')
end;






















