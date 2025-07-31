---
title: Custom Windows Images
description: How to make Windows more usable.
---
Beim Bereitstellen von multiplen Maschinen mit Windows-Betriebssytem, wird man beim Durchleben von hohem zeitlichen Aufwand und der
damit einhergehenden Lethargie, irgendwann anfangen nach Automatisierungs-Möglichkeiten zu forschen.
Mit modifizierten Windows-Images kann man sich widerkehrende Installationsroutinen und Konfigurationen ersparen, und somit der Lethargie enfliehen.

- Doku von Mircosoft: https://learn.microsoft.com/de-de/windows-hardware/manufacture/desktop/windows-setup-automation-overview?view=windows-11

## TL;DR
1. Rechner mit jeglicher Software ausstatten
2. Abbild des gesamten Systems erfassen
3. ISO mit dem Abbild bauen
4. System-Abbild auf weiteren Rechnern installieren


## Antwortdatien (`unattend.xml`,`autounattend.xml`)
Um Einstellungen bei der Installation vorzudefinieren, kann man sich eine Antwortdatei (z.B.: `autounattend.xml`, `unattend.xml`) bauen. 
Diese wird in der ISO neben der `setup.exe` platziert. Da eine ISO ein fixe Größe hat, muss man jene entpacken, die Antwortdatei platzieren
und danach mit `oscdimg` die ISO erneut gebaut werden.
Hat man die standard Windows ISO auf `C:\` exthrahiert, muss die `autounattend.xml` hier liegen: `C:\Win10_22H2_German_x64v1\autounattend.xml`.

Zur Verifizierung der Antwortdatei kann der _Windows System Image Manager_ (SIM) hilfreich sein.

Mir persönlich hat beim Erstellen von Antwort-Dateien folgende Website sehr geholfen:

- https://schneegans.de/windows/unattend-generator/

### Aufbau
Im Grund ist eine Antwortdatei wie folgt strukturiert:
```xml
<?xml version="1.0" encoding="utf-8"?>
<unattend xmlns="urn:schemas-microsoft-com:unattend" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State">
	<settings pass="offlineServicing"></settings>
	<settings pass="windowsPE"></settings>
	<settings pass="generalize"></settings>
	<settings pass="specialize"></settings>
	<settings pass="auditSystem"></settings>
	<settings pass="auditUser"></settings>
	<settings pass="oobeSystem"></settings>
</unattend>
```
In diesen Blöcken kann jeweils Konfiguration zu den 7 Phasen des Windows Setups deklariert werden.
- `windowsPE`: In der _Preinstallation Environment_ kann z.B. die Partitionierung des Systems oder auch das zu installierende Image angegeben werden.
- `oobeSystem`: Hier kann man Nutzer anlegen oder auch die verschiedenen Prompts (Telemetrie usw.) verstecken, die beim Windows Setup nerven.

Unter diesem Link findet man die offizielle Dokumentation mit hilfreichem Schaubild: https://learn.microsoft.com/de-de/windows-hardware/manufacture/desktop/how-configuration-passes-work?view=windows-11&source=recommendations


### Beispiel
Eine `autounattend.xml` kann wie folgt aussehen:
```xml
<?xml version="1.0" encoding="utf-8"?>
<unattend xmlns="urn:schemas-microsoft-com:unattend" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State">
	<!--https://schneegans.de/windows/unattend-generator/?LanguageMode=Unattended&UILanguage=de-DE&Locale=de-DE&Keyboard=00000407&GeoLocation=94&ProcessorArchitecture=amd64&ComputerNameMode=Random&CompactOsMode=Default&TimeZoneMode=Explicit&TimeZone=W.+Europe+Standard+Time&PartitionMode=Interactive&DiskAssertionMode=Skip&WindowsEditionMode=Generic&WindowsEdition=pro&UserAccountMode=Unattended&AccountName0=AdminLocal&AccountDisplayName0=AdminLocal&AccountPassword0=abelliocbc&AccountGroup0=Administrators&AccountName1=&AccountName2=&AccountName3=&AccountName4=&AutoLogonMode=Own&PasswordExpirationMode=Unlimited&LockoutMode=Disabled&HideFiles=Hidden&TaskbarSearch=Box&TaskbarIconsMode=Default&StartTilesMode=Default&StartPinsMode=Default&DisableDefender=true&DisableWindowsUpdate=true&TurnOffSystemSounds=true&DisableAppSuggestions=true&EffectsMode=Default&DesktopIconsMode=Default&WifiMode=Skip&ExpressSettings=DisableAll&KeysMode=Skip&ColorMode=Default&WallpaperMode=Default&WdacMode=Skip-->
	<settings pass="offlineServicing"></settings>
	<settings pass="windowsPE">
		<component name="Microsoft-Windows-International-Core-WinPE" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS">
			<SetupUILanguage>
				<UILanguage>de-DE</UILanguage>
			</SetupUILanguage>
			<InputLocale>0407:00000407</InputLocale>
			<SystemLocale>de-DE</SystemLocale>
			<UILanguage>de-DE</UILanguage>
			<UserLocale>de-DE</UserLocale>
		</component>
		<component name="Microsoft-Windows-Setup" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS">
			<UserData>
				<ProductKey>
					<Key>VK7JG-NPHTM-C97JM-9MPGT-3V66T</Key>
					<WillShowUI>OnError</WillShowUI>
				</ProductKey>
				<AcceptEula>true</AcceptEula>
			</UserData>
			<ImageInstall>
				<OSImage>
					<InstallFrom>
					  <MetaData wcm:action="add">
						<Key>/IMAGE/INDEX</Key>
						<Value>1</Value>
					  </MetaData>
					</InstallFrom>
					<WillShowUI>OnError</WillShowUI>
				</OSImage>
			</ImageInstall>
			<UseConfigurationSet>false</UseConfigurationSet>
		</component>
	</settings>
	<settings pass="generalize"></settings>
	<settings pass="specialize">
		<component name="Microsoft-Windows-Shell-Setup" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS">
			<TimeZone>W. Europe Standard Time</TimeZone>
		</component>
	</settings>
	<settings pass="auditSystem"></settings>
	<settings pass="auditUser"></settings>
	<settings pass="oobeSystem">
		<component name="Microsoft-Windows-International-Core" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS">
			<InputLocale>0407:00000407</InputLocale>
			<SystemLocale>de-DE</SystemLocale>
			<UILanguage>de-DE</UILanguage>
			<UserLocale>de-DE</UserLocale>
		</component>
		<component name="Microsoft-Windows-Shell-Setup" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS">
			<UserAccounts>
				<LocalAccounts>
					<LocalAccount wcm:action="add">
						<Name>AdminLocal</Name>
						<DisplayName>AdminLocal</DisplayName>
						<Group>Administrators</Group>
						<Password>
							<Value>supersecretpassword</Value>
							<PlainText>true</PlainText>
						</Password>
					</LocalAccount>
				</LocalAccounts>
			</UserAccounts>
			<OOBE>
				<ProtectYourPC>3</ProtectYourPC>
				<HideEULAPage>true</HideEULAPage>
				<HideWirelessSetupInOOBE>true</HideWirelessSetupInOOBE>
				<HideOnlineAccountScreens>false</HideOnlineAccountScreens>
			</OOBE>
			<FirstLogonCommands>
				<SynchronousCommand wcm:action="add">
					<Order>1</Order>
					<CommandLine>powershell.exe -WindowStyle Normal -NoProfile -Command "Get-Content -LiteralPath 'C:\Windows\Setup\Scripts\FirstLogon.ps1' -Raw | Invoke-Expression;"</CommandLine>
				</SynchronousCommand>
			</FirstLogonCommands>
		</component>
	</settings>
</unattend>
```

## Referenzen

- [sysprep]({{% ref path="sysprep" %}})
- [dism]({{% ref path="dism" %}})
- [oscdimg]({{% ref path="oscdimg" %}})

## FAQ

- Wie kommt man in die `cmd` während der Installation?
    - `SHIFT+F10`

## Interessante Projekte

- https://github.com/ntdevlabs/tiny11builder/blob/main/tiny11maker.ps1


## Troubleshooting
### Das Abbild konnte nicht gefunden werden
Die Setup.exe findet nicht das passende Abbild. Dieses muss daher extra angegeben werden. Die Info welchen Index unser Abbild hat bekommt man wie folgt:
```cmd
dism /Get-WimInfo /WimFile:install.wim

## Tool zur Imageverwaltung für die Bereitstellung
## Version: 10.0.19041.3636
## 
## Details für Abbild: "install.wim"
## 
## Index: "1"
## Name: "Werkstatt Windows 10"
## Beschreibung: "<nicht definiert>"
## Größe: 32.922.249.198 Bytes
## 
## Der Vorgang wurde erfolgreich beendet.
```
Unter dem Key `/IMAGE/INDEX` kann man den Index als Value eintragen.

```xml
  <component name="Microsoft-Windows-Setup" ...>
			<ImageInstall>
				<OSImage>
					<InstallFrom>
					  <MetaData wcm:action="add">
						<Key>/IMAGE/INDEX</Key>
						<Value>1</Value>
					  </MetaData>
					</InstallFrom>
					<WillShowUI>OnError</WillShowUI>
				</OSImage>
			</ImageInstall>
```
