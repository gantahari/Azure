resource "azurerm_resource_group" "adf" {
    name = local.rg_name
    location = var.loc
  
}

resource "azurerm_data_factory" "adf" {
    name = local.adf_name
    resource_group_name = azurerm_resource_group.adf.name
    location = azurerm_resource_group.adf.location

    github_configuration {
      account_name = "gantahari"
      repository_name = "Azure"
      branch_name = "main"
      root_folder = "/dataengineering/adf"
    }
    global_parameter {
      name = "env"
      type = "String"
      value = "${var.env}"
    }
    

    identity {
      type = "SystemAssigned"
    }
  
}