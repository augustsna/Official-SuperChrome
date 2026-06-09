# SuperChrome Local Signing Script
# This script creates a local self-signed certificate and signs the EXE
# Run this if Smart App Control or Defender keeps blocking the program

$exePath = Join-Path $PSScriptRoot "SuperChrome.exe"

if (-not (Test-Path $exePath)) {
    Write-Host "Error: SuperChrome.exe not found in $PSScriptRoot" -ForegroundColor Red
    exit
}

Write-Host "Creating local self-signed certificate..." -ForegroundColor Cyan
$cert = New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=SuperChrome-Local-Dev" -KeyLength 2048 -NotAfter (Get-Date).AddYears(5) -CertStoreLocation "Cert:\CurrentUser\My"

Write-Host "Signing executable..." -ForegroundColor Cyan
Set-AuthenticodeSignature -FilePath $exePath -Certificate $cert

Write-Host "Trusting the certificate locally..." -ForegroundColor Cyan
$certPath = Join-Path $PSScriptRoot "SuperChromeLocal.cer"
Export-Certificate -Cert $cert -FilePath $certPath
Import-Certificate -FilePath $certPath -CertStoreLocation "Cert:\CurrentUser\Root"

Write-Host "`nSuccess! SuperChrome.exe has been signed and the certificate trusted." -ForegroundColor Green
Write-Host "If Windows still blocks it, right-click SuperChrome.exe -> Properties -> Check 'Unblock'." -ForegroundColor Yellow
Pause