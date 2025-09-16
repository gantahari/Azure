# ---- Built-in Azure Role Definition IDs ----
role_map = {
    "Reader": "acdd72a7-3385-48ef-bd42-f606fba81ae7",
    "Contributor": "b24988ac-6180-42a0-ab88-20f7382dd24c",
    "Storage Blob Data Contributor": "ba92f5b4-2d11-453d-a403-e96b0029c9fe"
}

# ---- Job Role Policies ----
devops_dict = {
    "Contributor": [],
    "Reader": [
        "/subscriptions/b82ad015-5330-4877-a82b-c5ed126b244b/resourceGroups/hari-rg/providers/Microsoft.Storage/storageAccounts/sahari2343"
    ]
}

sre_dict = {
    "Reader": [
        "/subscriptions/b82ad015-5330-4877-a82b-c5ed126b244b/resourceGroups/hari-rg/providers/Microsoft.Storage/storageAccounts/sahari2343"
    ]
}

lead_devops_dict = {
    "Contributor": [
        "/subscriptions/b82ad015-5330-4877-a82b-c5ed126b244b/resourceGroups/hari-rg/providers/Microsoft.Storage/storageAccounts/sahari2343"
    ],
    "Reader": [
    ]
}

role_policies = {
    "DevOps Engineer": devops_dict,
    "SRE Engineer": sre_dict,
    "Lead DevOps Engineer": lead_devops_dict
}