
data "azurerm_key_vault_secret" "kv_password" {
  key_vault_id = "/subscriptions/606e824b-aaf7-4b4e-9057-b459f6a4436d/resourceGroups/dev-hari/providers/Microsoft.KeyVault/vaults/${var.env}kvsecrectsadfhari"
  name = "password"
}

resource "azurerm_mssql_server" "mssql_server" {
  name = "${var.env}-${var.res_type1}-${var.name}"
  resource_group_name = "${var.env}-${var.name}"
  location = var.loc
  version = "12.0"
  administrator_login = "hari" 
  administrator_login_password = "Testing@1412"
}

resource "azurerm_mssql_database" "mssql_db" {
  name = "${var.env}-${var.res_type2}-${var.name}"
  server_id = azurerm_mssql_server.mssql_server.id
  sku_name = "Basic"
  max_size_gb = 2
  sample_name = "AdventureWorksLT"
  
  storage_account_type = "Local"   

  
}

resource "azurerm_mssql_firewall_rule" "mssql_firewall_rule" {
  name = "rule1"
  server_id = azurerm_mssql_server.mssql_server.id
   start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}