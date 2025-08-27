resource "azurerm_storage_account" "sa" {
  resource_group_name = "${var.env}-${var.name}"
  name = lower("${var.env}${var.res_type}${var.name}")
  location = var.loc
  account_replication_type = "LRS"
  account_tier = "Standard"
}

resource "azurerm_storage_container" "sa" {
  name = lower("${var.env}-input")
  storage_account_name = azurerm_storage_account.sa.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "name" {
  storage_account_id = azurerm_storage_account.sa.id
  name = lower("${var.env}-output")
  container_access_type = "private"
}