output "adf_system_identity" {
  value = azurerm_data_factory.adf.identity[0].principal_id
}