resource "azurerm_storage_account" "adls" {
  resource_group_name = "${var.env}-${var.name}"
  name = lower("${var.env}${var.res_type}${var.name}")
  location = var.loc
  account_replication_type = "LRS"
  account_tier = "Standard"
  is_hns_enabled = true
}



resource "azurerm_storage_container" "adls" {
  storage_account_id = azurerm_storage_account.adls.id
  name = lower("${var.env}-output")
  container_access_type = "private"
}