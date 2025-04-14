---
title: Custom Windows Images
description: How to make Windows more usable.
---
Beim Bereitstellen von multiplen Maschinen mit Windows-Betriebssytem, wird man beim Durchleben von hohem zeitlichen Aufwand und der
damit einhergehenden Lethargie, irgendwann anfangen nach Automatisierungs-Möglichkeiten zu forschen.
Mit modifizierten Windows-Images kann man sich widerkehrende Installationsroutinen und Konfigurationen ersparen, und somit der Lethargie enfliehen.

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

#### Aufbau
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


#### Beispiel
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
		<component name="Microsoft-Windows-Deployment" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS">
			<RunSynchronous>
				<RunSynchronousCommand wcm:action="add">
					<Order>1</Order>
					<Path>powershell.exe -WindowStyle Normal -NoProfile -Command "$xml = [xml]::new(); $xml.Load('C:\Windows\Panther\unattend.xml'); $sb = [scriptblock]::Create( $xml.unattend.Extensions.ExtractScript ); Invoke-Command -ScriptBlock $sb -ArgumentList $xml;"</Path>
				</RunSynchronousCommand>
				<RunSynchronousCommand wcm:action="add">
					<Order>2</Order>
					<Path>powershell.exe -WindowStyle Normal -NoProfile -Command "Get-Content -LiteralPath 'C:\Windows\Setup\Scripts\Specialize.ps1' -Raw | Invoke-Expression;"</Path>
				</RunSynchronousCommand>
				<RunSynchronousCommand wcm:action="add">
					<Order>3</Order>
					<Path>reg.exe load "HKU\DefaultUser" "C:\Users\Default\NTUSER.DAT"</Path>
				</RunSynchronousCommand>
				<RunSynchronousCommand wcm:action="add">
					<Order>4</Order>
					<Path>powershell.exe -WindowStyle Normal -NoProfile -Command "Get-Content -LiteralPath 'C:\Windows\Setup\Scripts\DefaultUser.ps1' -Raw | Invoke-Expression;"</Path>
				</RunSynchronousCommand>
				<RunSynchronousCommand wcm:action="add">
					<Order>5</Order>
					<Path>reg.exe unload "HKU\DefaultUser"</Path>
				</RunSynchronousCommand>
			</RunSynchronous>
		</component>
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
	<Extensions xmlns="https://schneegans.de/windows/unattend-generator/">
		<ExtractScript>
param(
    [xml] $Document
);

foreach( $file in $Document.unattend.Extensions.File ) {
    $path = [System.Environment]::ExpandEnvironmentVariables( $file.GetAttribute( 'path' ) );
    mkdir -Path( $path | Split-Path -Parent ) -ErrorAction 'SilentlyContinue';
    $encoding = switch( [System.IO.Path]::GetExtension( $path ) ) {
        { $_ -in '.ps1', '.xml' } { [System.Text.Encoding]::UTF8; }
        { $_ -in '.reg', '.vbs', '.js' } { [System.Text.UnicodeEncoding]::new( $false, $true ); }
        default { [System.Text.Encoding]::Default; }
    };
    $bytes = $encoding.GetPreamble() + $encoding.GetBytes( $file.InnerText.Trim() );
    [System.IO.File]::WriteAllBytes( $path, $bytes );
}
		</ExtractScript>
		<File path="C:\Windows\Setup\Scripts\PauseWindowsUpdate.ps1">
$formatter = {
	$args[0].ToString( "yyyy'-'MM'-'dd'T'HH':'mm':'ssK" );
};
$now = [datetime]::UtcNow;
$start = &amp; $formatter $now;
$end = &amp; $formatter $now.AddDays( 7 );

$params = @{
	LiteralPath = 'Registry::HKLM\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings';
	Type = 'String';
	Force = $true;
};

Set-ItemProperty @params -Name 'PauseFeatureUpdatesStartTime' -Value $start;
Set-ItemProperty @params -Name 'PauseFeatureUpdatesEndTime' -Value $end;
Set-ItemProperty @params -Name 'PauseQualityUpdatesStartTime' -Value $start;
Set-ItemProperty @params -Name 'PauseQualityUpdatesEndTime' -Value $end;
Set-ItemProperty @params -Name 'PauseUpdatesStartTime' -Value $start;
Set-ItemProperty @params -Name 'PauseUpdatesExpiryTime' -Value $end;
		</File>
		<File path="C:\Windows\Setup\Scripts\PauseWindowsUpdate.xml">
&lt;Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task"&gt;
	&lt;Triggers&gt;
		&lt;BootTrigger&gt;
			&lt;Repetition&gt;
				&lt;Interval&gt;P1D&lt;/Interval&gt;
				&lt;StopAtDurationEnd&gt;false&lt;/StopAtDurationEnd&gt;
			&lt;/Repetition&gt;
			&lt;Enabled&gt;true&lt;/Enabled&gt;
		&lt;/BootTrigger&gt;
	&lt;/Triggers&gt;
	&lt;Principals&gt;
		&lt;Principal id="Author"&gt;
			&lt;UserId&gt;S-1-5-19&lt;/UserId&gt;
			&lt;RunLevel&gt;LeastPrivilege&lt;/RunLevel&gt;
		&lt;/Principal&gt;
	&lt;/Principals&gt;
	&lt;Settings&gt;
		&lt;MultipleInstancesPolicy&gt;IgnoreNew&lt;/MultipleInstancesPolicy&gt;
		&lt;DisallowStartIfOnBatteries&gt;false&lt;/DisallowStartIfOnBatteries&gt;
		&lt;StopIfGoingOnBatteries&gt;false&lt;/StopIfGoingOnBatteries&gt;
		&lt;AllowHardTerminate&gt;true&lt;/AllowHardTerminate&gt;
		&lt;StartWhenAvailable&gt;false&lt;/StartWhenAvailable&gt;
		&lt;RunOnlyIfNetworkAvailable&gt;false&lt;/RunOnlyIfNetworkAvailable&gt;
		&lt;IdleSettings&gt;
			&lt;StopOnIdleEnd&gt;true&lt;/StopOnIdleEnd&gt;
			&lt;RestartOnIdle&gt;false&lt;/RestartOnIdle&gt;
		&lt;/IdleSettings&gt;
		&lt;AllowStartOnDemand&gt;true&lt;/AllowStartOnDemand&gt;
		&lt;Enabled&gt;true&lt;/Enabled&gt;
		&lt;Hidden&gt;false&lt;/Hidden&gt;
		&lt;RunOnlyIfIdle&gt;false&lt;/RunOnlyIfIdle&gt;
		&lt;WakeToRun&gt;false&lt;/WakeToRun&gt;
		&lt;ExecutionTimeLimit&gt;PT72H&lt;/ExecutionTimeLimit&gt;
		&lt;Priority&gt;7&lt;/Priority&gt;
	&lt;/Settings&gt;
	&lt;Actions Context="Author"&gt;
		&lt;Exec&gt;
			&lt;Command&gt;C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe&lt;/Command&gt;
			&lt;Arguments&gt;-Command "Get-Content -LiteralPath 'C:\Windows\Setup\Scripts\PauseWindowsUpdate.ps1' -Raw | Invoke-Expression;"&lt;/Arguments&gt;
		&lt;/Exec&gt;
	&lt;/Actions&gt;
&lt;/Task&gt;
		</File>
		<File path="C:\Windows\Setup\Scripts\TurnOffSystemSounds.ps1">
$excludes = Get-ChildItem -LiteralPath 'Registry::HKU\DefaultUser\AppEvents\EventLabels' |
    Where-Object -FilterScript { ($_ | Get-ItemProperty).ExcludeFromCPL -eq 1; } |
    Select-Object -ExpandProperty 'PSChildName';
Get-ChildItem -Path 'Registry::HKU\DefaultUser\AppEvents\Schemes\Apps\*\*' |
    Where-Object -Property 'PSChildName' -NotIn $excludes |
    Get-ChildItem -Include '.Current' | Set-ItemProperty -Name '(Default)' -Value '';
		</File>
		<File path="C:\Windows\Setup\Scripts\Specialize.ps1">
$scripts = @(
	{
		net.exe accounts /lockoutthreshold:0;
	};
	{
		net.exe accounts /maxpwage:UNLIMITED;
	};
	{
		Register-ScheduledTask -TaskName 'PauseWindowsUpdate' -Xml $( Get-Content -LiteralPath 'C:\Windows\Setup\Scripts\PauseWindowsUpdate.xml' -Raw );
	};
	{
		reg.exe add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender Security Center\Notifications" /v DisableNotifications /t REG_DWORD /d 1 /f;
	};
	{
		reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\LogonUI\BootAnimation" /v DisableStartupSound /t REG_DWORD /d 1 /f;
		reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\EditionOverrides" /v UserSetting_DisableStartupSound /t REG_DWORD /d 1 /f;
	};
	{
		reg.exe add "HKLM\Software\Policies\Microsoft\Windows\CloudContent" /v "DisableWindowsConsumerFeatures" /t REG_DWORD /d 1 /f;
	};
);

&amp; {
  [float] $complete = 0;
  [float] $increment = 100 / $scripts.Count;
  foreach( $script in $scripts ) {
    Write-Progress -Activity 'Running scripts to customize your Windows installation. Do not close this window.' -PercentComplete $complete;
    '*** Will now execute command &#xAB;{0}&#xBB;.' -f $(
      $str = $script.ToString().Trim() -replace '\s+', ' ';
      $max = 100;
      if( $str.Length -le $max ) {
        $str;
      } else {
        $str.Substring( 0, $max - 1 ) + '&#x2026;';
      }
    );
    $start = [datetime]::Now;
    &amp; $script;
    '*** Finished executing command after {0:0} ms.' -f [datetime]::Now.Subtract( $start ).TotalMilliseconds;
    "`r`n" * 3;
    $complete += $increment;
  }
} *&gt;&amp;1 &gt;&gt; "C:\Windows\Setup\Scripts\Specialize.log";
		</File>
		<File path="C:\Windows\Setup\Scripts\UserOnce.ps1">
$scripts = @(
	{
		Set-ItemProperty -LiteralPath 'Registry::HKCU\AppEvents\Schemes' -Name '(Default)' -Type 'String' -Value '.None';
	};
);

&amp; {
  [float] $complete = 0;
  [float] $increment = 100 / $scripts.Count;
  foreach( $script in $scripts ) {
    Write-Progress -Activity 'Running scripts to configure this user account. Do not close this window.' -PercentComplete $complete;
    '*** Will now execute command &#xAB;{0}&#xBB;.' -f $(
      $str = $script.ToString().Trim() -replace '\s+', ' ';
      $max = 100;
      if( $str.Length -le $max ) {
        $str;
      } else {
        $str.Substring( 0, $max - 1 ) + '&#x2026;';
      }
    );
    $start = [datetime]::Now;
    &amp; $script;
    '*** Finished executing command after {0:0} ms.' -f [datetime]::Now.Subtract( $start ).TotalMilliseconds;
    "`r`n" * 3;
    $complete += $increment;
  }
} *&gt;&amp;1 &gt;&gt; "$env:TEMP\UserOnce.log";
		</File>
		<File path="C:\Windows\Setup\Scripts\DefaultUser.ps1">
$scripts = @(
	{
		Get-Content -LiteralPath 'C:\Windows\Setup\Scripts\TurnOffSystemSounds.ps1' -Raw | Invoke-Expression;
	};
	{
		$names = @(
		  'ContentDeliveryAllowed';
		  'FeatureManagementEnabled';
		  'OEMPreInstalledAppsEnabled';
		  'PreInstalledAppsEnabled';
		  'PreInstalledAppsEverEnabled';
		  'SilentInstalledAppsEnabled';
		  'SoftLandingEnabled';
		  'SubscribedContentEnabled';
		  'SubscribedContent-310093Enabled';
		  'SubscribedContent-338387Enabled';
		  'SubscribedContent-338388Enabled';
		  'SubscribedContent-338389Enabled';
		  'SubscribedContent-338393Enabled';
		  'SubscribedContent-353698Enabled';
		  'SystemPaneSuggestionsEnabled';
		);
		
		foreach( $name in $names ) {
		  reg.exe add "HKU\DefaultUser\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" /v $name /t REG_DWORD /d 0 /f;
		}
	};
	{
		reg.exe add "HKU\DefaultUser\Software\Microsoft\Windows\CurrentVersion\RunOnce" /v "UnattendedSetup" /t REG_SZ /d "powershell.exe -WindowStyle Normal -NoProfile -Command \""Get-Content -LiteralPath 'C:\Windows\Setup\Scripts\UserOnce.ps1' -Raw | Invoke-Expression;\""" /f;
	};
);

&amp; {
  [float] $complete = 0;
  [float] $increment = 100 / $scripts.Count;
  foreach( $script in $scripts ) {
    Write-Progress -Activity 'Running scripts to modify the default user&#x2019;&#x2019;s registry hive. Do not close this window.' -PercentComplete $complete;
    '*** Will now execute command &#xAB;{0}&#xBB;.' -f $(
      $str = $script.ToString().Trim() -replace '\s+', ' ';
      $max = 100;
      if( $str.Length -le $max ) {
        $str;
      } else {
        $str.Substring( 0, $max - 1 ) + '&#x2026;';
      }
    );
    $start = [datetime]::Now;
    &amp; $script;
    '*** Finished executing command after {0:0} ms.' -f [datetime]::Now.Subtract( $start ).TotalMilliseconds;
    "`r`n" * 3;
    $complete += $increment;
  }
} *&gt;&amp;1 &gt;&gt; "C:\Windows\Setup\Scripts\DefaultUser.log";
		</File>
		<File path="C:\Windows\Setup\Scripts\FirstLogon.ps1">
$scripts = @(
	{
		Set-ItemProperty -LiteralPath 'Registry::HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon' -Name 'AutoLogonCount' -Type 'DWord' -Force -Value 0;
	};
);

&amp; {
  [float] $complete = 0;
  [float] $increment = 100 / $scripts.Count;
  foreach( $script in $scripts ) {
    Write-Progress -Activity 'Running scripts to finalize your Windows installation. Do not close this window.' -PercentComplete $complete;
    '*** Will now execute command &#xAB;{0}&#xBB;.' -f $(
      $str = $script.ToString().Trim() -replace '\s+', ' ';
      $max = 100;
      if( $str.Length -le $max ) {
        $str;
      } else {
        $str.Substring( 0, $max - 1 ) + '&#x2026;';
      }
    );
    $start = [datetime]::Now;
    &amp; $script;
    '*** Finished executing command after {0:0} ms.' -f [datetime]::Now.Subtract( $start ).TotalMilliseconds;
    "`r`n" * 3;
    $complete += $increment;
  }
} *&gt;&amp;1 &gt;&gt; "C:\Windows\Setup\Scripts\FirstLogon.log";
		</File>
	</Extensions>
</unattend>
```

## Referenzen

- [sysprep]({{% ref path="sysprep" %}})
- [dism]({{% ref path="dism" %}})
- [oscdimg]({{% ref path="oscdimg" %}})

## FAQ

- Wie kommt man in die `cmd` während der Installation?
    - `SHIFT+F10`


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
