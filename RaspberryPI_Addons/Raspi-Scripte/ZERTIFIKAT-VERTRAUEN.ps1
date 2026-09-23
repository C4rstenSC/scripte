$ErrorActionPreference = 'Stop'
$certificatePath = Join-Path $PSScriptRoot 'Carsten-Schulte-CodeSigning.cer'
if (-not (Test-Path $certificatePath)) {
    throw 'Carsten-Schulte-CodeSigning.cer fehlt im selben Ordner.'
}
$certificate = [System.Security.Cryptography.X509Certificates.X509Certificate2]::new($certificatePath)
try {
    foreach ($storeName in @('Root', 'TrustedPublisher')) {
        $store = [System.Security.Cryptography.X509Certificates.X509Store]::new(
            $storeName, [System.Security.Cryptography.X509Certificates.StoreLocation]::CurrentUser)
        try {
            $store.Open([System.Security.Cryptography.X509Certificates.OpenFlags]::ReadWrite)
            if ($store.Certificates.Find(
                    [System.Security.Cryptography.X509Certificates.X509FindType]::FindByThumbprint,
                    $certificate.Thumbprint, $false).Count -eq 0) {
                $store.Add($certificate)
            }
        }
        finally { $store.Dispose() }
    }
    Write-Host "Zertifikat vertraut: $($certificate.Thumbprint)" -ForegroundColor Green
}
finally { $certificate.Dispose() }
