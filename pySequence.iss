
;This file is part of pySequence
;
; Copyright (C) 2011 Cédrick FAURY
;
;pySequence is free software; you can redistribute it and/or modify
;it under the terms of the GNU General Public License as published by
;the Free Software Foundation; either version 3 of the License, or
;(at your option) any later version.
;
;pySyLiC is distributed in the hope that it will be useful,
;but WITHOUT ANY WARRANTY; without even the implied warranty of
;MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;GNU General Public License for more details.
;
;You should have received a copy of the GNU General Public License
;along with pySequence; if not, write to the Free Software
;Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

[Setup]
;Informations générales sur l'application

AppName=pySequence
AppVersion=1.9
AppVerName=pySequence 1.9

AppPublisher=Cédrick Faury
AppCopyright=Copyright © 2011-2012 Cédrick Faury
VersionInfoVersion = 1.9.0.0

;Répertoire de base contenant les fichiers
SourceDir=D:\Developpement\Sequence

;Repertoire d'installation
DefaultDirName={pf}\pySequence
DefaultGroupName=pySequence
LicenseFile=src\gpl.txt

;Paramètres de compression
;lzma ou zip
Compression=lzma/max
SolidCompression=yes

;Par défaut, pas besoin d'être administrateur pour installer
PrivilegesRequired=none

;Nom du fichier généré et répertoire de destination
OutputBaseFilename=pySequence_1.9
OutputDir=releases

UninstallDisplayIcon={app}\logo.ico

;Fenêtre en background
WindowResizable=false
WindowStartMaximized=true
WindowShowCaption=true
BackColorDirection=lefttoright
;WizardImageFile = D:\Documents\Developpement\PyVot 0.6\Images\grand_logo.bmp
;WizardSmallImageFile = D:\Documents\Developpement\PyVot 0.6\Images\petit_logo.bmp

AlwaysUsePersonalGroup=no



[Messages]
BeveledLabel=pySequence 1.9 installation

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
fr.AssocFileExtension=&Associer le programme pySequence à l'extension .seq
fr.CreateQuickLaunchIcon=Créer un icône dans la barre de lancement rapide
fr.FileExtensionName=Séquence pédagogique STI2D
fr.FileExtension=pySequence.sequence
fr.InstallFor=Installer pour :
fr.AllUsers=Tous les utilisateurs
fr.JustMe=Seulement moi
fr.ShortCut=Raccourcis :
fr.Association=Association de fichier :
version = 1.9


[Files]
;
; Fichiers de la distribution
;
Source: src\dist\*.*; DestDir: {app}\bin; Flags : ignoreversion recursesubdirs;
;Source: *.txt; DestDir: {app}; Flags : ignoreversion;
;Source: Images\*.ico; DestDir: {app}\Images; Flags : ignoreversion;
;Source: Images\*.png; DestDir: {app}\Images; Flags : ignoreversion;
;Source: locale\en\LC_MESSAGES\*.mo; DestDir: {app}\locale\en\LC_MESSAGES; Flags : ignoreversion;

;
; Fichiers exemples
;
Source: Exemples\*.seq; DestDir: {app}\Exemples; Flags : ignoreversion;
;Source: Exemples\*.csv; DestDir: {app}\Exemples; Flags : ignoreversion;


; les dll C++
;Source: src\msvcr90.dll; DestDir: {app}\bin; Flags : ignoreversion;
;Source: src\*.manifest; DestDir: {app}\bin; Flags : ignoreversion;

; des fichiers à mettre dans le dossier "Application data"
;Source: {src};  DestDir: {code:DefAppDataFolder}\Test\;

[Tasks]
Name: desktopicon2; Description: {cm:CreateDesktopIcon} pySequence ;GroupDescription: {cm:ShortCut}; MinVersion: 4,4
Name: fileassoc; Description: {cm:AssocFileExtension};GroupDescription: {cm:Association};
Name: common; Description: {cm:AllUsers}; GroupDescription: {cm:InstallFor}; Flags: exclusive
Name: local;  Description: {cm:JustMe}; GroupDescription: {cm:InstallFor}; Flags: exclusive unchecked

[Icons]
Name: {group}\pySequence;Filename: {app}\bin\Sequence.exe; WorkingDir: {app}\bin; IconFileName: {app}\bin\Sequence.exe
Name: {group}\{cm:uninstall} pySequence; Filename: {app}\unins000.exe;IconFileName: {app}\unins000.exe
;
; On ajoute sur le Bureau l'icône pySequence
;
Name: {code:DefDesktop}\pySequence 1.9;   Filename: {app}\bin\Sequence.exe; WorkingDir: {app}\bin; MinVersion: 4,4; Tasks: desktopicon2; IconFileName: {app}\bin\Sequence.exe


[_ISTool]
Use7zip=true


[Registry]
; Tout ce qui concerne les fichiers .seq
Root: HKCR; SubKey: .seq; ValueType: string; ValueData: {cm:FileExtension}; Flags: uninsdeletekey
Root: HKCR; SubKey: {cm:FileExtension}; ValueType: string; Flags: uninsdeletekey; ValueData: {cm:FileExtensionName}
Root: HKCR; SubKey: {cm:FileExtension}\Shell\Open\Command; ValueType: string; ValueData: """{app}\bin\Sequence.exe"" ""%1"""; Flags: uninsdeletekey;
Root: HKCR; Subkey: {cm:FileExtension}\DefaultIcon; ValueType: string; ValueData: {app}\bin\logo.ico,0; Flags: uninsdeletekey;

; Pour stocker le style d'installation : "All users" ou "Current user"
Root: HKLM; Subkey: SOFTWARE\pySequence; ValueType: string; ValueName: DataFolder; ValueData: {code:DefAppDataFolder}\pySequence ; Flags: uninsdeletekey;



[Code]
Procedure URLLabelOnClick(Sender: TObject);
var
  ErrorCode: Integer;
begin
  ShellExec('open', 'http://code.google.com/p/pysequence/', '', '', SW_SHOWNORMAL, ewNoWait, ErrorCode);
end;

{*** INITIALISATION ***}
Procedure InitializeWizard;
var
  URLLabel: TNewStaticText;
begin
  URLLabel := TNewStaticText.Create(WizardForm);
  URLLabel.Caption := 'http://code.google.com/p/pysequence/';
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






















