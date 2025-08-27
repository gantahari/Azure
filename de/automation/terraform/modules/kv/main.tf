data "azurerm_client_config" "current" {
  
}

resource "azurerm_key_vault" "kv" {
    resource_group_name = "${var.env}-${var.name}"
    name = lower("${var.env}${var.res_type}${var.name}")
    location = var.loc
    tenant_id = var.tenant_id
    sku_name = "standard"

    access_policy {
        tenant_id = data.azurerm_client_config.current.tenant_id
        object_id = data.azurerm_client_config.current.object_id

        secret_permissions = ["Get", "List", "Set", "Delete", "Recover", "Backup", "Restore", "Purge"]
    }
}