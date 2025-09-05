terraform {
#   backend "azurerm" {
#     key = "value"
#     subscription_id = "value"
#     tenant_id = "value"
#     client_id = "value"
#   }

    backend "local" {
    }
  
}

provider "azurerm" {
    subscription_id = "606e824b-aaf7-4b4e-9057-b459f6a4436d"
    features {
      
    }
}