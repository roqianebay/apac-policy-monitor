# Register a Windows Scheduled Task that crawls every 14 days.
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = (Get-Command python).Source
$Action = New-ScheduledTaskAction -Execute $Python -Argument "`"$Root\scraper\crawl.py`"" -WorkingDirectory $Root
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).Date.AddHours(9) -RepetitionInterval (New-TimeSpan -Days 14) -RepetitionDuration ([TimeSpan]::MaxValue)
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName "APAC Policy Monitor Crawl" -Action $Action -Trigger $Trigger -Settings $Settings -Description "Refresh APAC employer policy dashboard every 14 days" -Force | Out-Null
Write-Host "Scheduled task created: APAC Policy Monitor Crawl"
Write-Host "Python: $Python"
Write-Host "Working directory: $Root"
Write-Host "Run now with: python `"$Root\scraper\crawl.py`""
