param(
    [parameter(Mandatory = $true)] [string] $databricksworkspaceurl,
    [parameter(Mandatory = $true)] [string] $databricksworkspaceresId,
    [parameter(Mandatory = $false)] [int] $timetolive = 300
)

try {
    $accessTokenToAzure = (az account get-access-token --resource "https://management.azure.com" | ConvertFrom-Json).accessToken 
    Write-Host "Token acquired successfully"
}
catch {
    Write-Host "Error while getting the token"
    throw $_
}

$azuredatabricksprincipalId = "2ff814a6-3304-4ab8-85cb-cd0e6f879c1d"  

$headers = @{
    "Authorization"                        = "Bearer $((az account get-access-token --resource $azuredatabricksprincipalId | ConvertFrom-Json).accessToken)"
    "X-Databricks-Azure-SP-Management-Token" = $accessTokenToAzure
    "X-Databricks-Azure-Workspace-Resource-Id" = $databricksworkspaceresId
    "Content-Type"                         = "application/json"
}

$json = @{
    "lifetime_seconds" = $timetolive
}

$req = Invoke-WebRequest -Uri "https://$databricksworkspaceurl/api/2.0/token/create" `
    -Headers $headers `
    -Body ($json | ConvertTo-Json -Depth 5) `
    -Method POST

$bearerToken = ($req.Content | ConvertFrom-Json).token_value
return $bearerToken
