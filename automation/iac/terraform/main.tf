module "adf_module" {
  source = "./modules/adf"

  name = var.name
  res_type = var.adf_res
  env = var.env
  loc = var.loc
}

module "sa_module" {
    depends_on = [ module.adf_module ]
  source = "./modules/sa"

    name = var.name
    res_type = var.sa_res
    env = var.env
    loc = var.loc
}

module "kv_module" {
    source = "./modules/kv"

    name = var.name
    res_type = var.kv_res
    env = var.env
    loc = var.loc
}

module "adls_module" {
  source = "./modules/adls"

  name = var.name
  res_type = var.adls_res
  env = var.env
  loc = var.loc
}

module "mssql_db_module" {
  source = "./modules/sqldb"

    name = var.name
    res_type1 = var.mssql_server
    res_type2 = var.mssql_db
    env = var.env
    loc = var.loc2
    # loc2 =var.loc2
}


resource "azurerm_role_assignment" "adf_sa_identity" {
  scope = module.sa_module.sa_id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id = module.adf_module.adf_system_identity
}

resource "azurerm_role_assignment" "adf_kv_identity" {
  scope = module.kv_module.kv_id
  role_definition_name = "Key Vault Secrets User"
  principal_id = module.adf_module.adf_system_identity
}