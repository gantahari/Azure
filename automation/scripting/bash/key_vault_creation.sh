
// Create resource group 
az group create --resource-group hari-rg-key-automation --location eastus

// Create key vault1
az keyvault create --name keyvault01westus2 --location westus2 --resource-group hari-rg-key-automation --enable-rbac-authorization false

// Create key vault2
az keyvault create --name keyvault01eastus2 --location eastus2 --resource-group hari-rg-key-automation --enable-rbac-authorization false
