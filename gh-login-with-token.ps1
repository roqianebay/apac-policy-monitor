# Paste a GitHub PAT when gh device login Authorize button is disabled.
$ErrorActionPreference = "Stop"
$Gh = "$env:ProgramFiles\GitHub CLI\gh.exe"
if (-not (Test-Path $Gh)) { throw "GitHub CLI not found. Run: winget install GitHub.cli" }

Write-Host "Create a token: https://github.com/settings/tokens"
Write-Host "Scopes: repo (classic) or fine-grained write access to this repo."
Write-Host "If your org uses SSO, click Configure SSO -> Authorize on the token."
Write-Host ""

$secure = Read-Host "Paste token (input hidden)" -AsSecureString
$bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
$token = [Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)
[Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)

if ([string]::IsNullOrWhiteSpace($token)) { throw "Empty token." }

$token | & $Gh auth login --with-token
& $Gh auth status
Write-Host "OK. Next: .\publish-github.ps1"