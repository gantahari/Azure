#!/bin/bash
# Backup and Restore Certificates between two Azure Key Vaults with conflict handling + purge wait
# Author: Hari

set -e

SOURCE_VAULT="keyvault01westus2"
DEST_VAULT="keyvault01eastus2"
BACKUP_DIR="./kv-cert-backups"

mkdir -p $BACKUP_DIR

echo "=== Starting certificate backup from $SOURCE_VAULT ==="

# ========================
# Backup Certificates
# ========================
cert_list=$(az keyvault certificate list --vault-name $SOURCE_VAULT --query "[].name" -o tsv)

if [ -z "$cert_list" ]; then
    echo "No certificates found in $SOURCE_VAULT"
else
    for certname in $cert_list; do
        echo "Backing up certificate: $certname"
        az keyvault certificate backup \
          --vault-name $SOURCE_VAULT \
          --name $certname \
          --file "$BACKUP_DIR/$certname.backup"
    done
    echo "=== Certificate backup completed. Files saved in $BACKUP_DIR ==="
fi

# ========================
# Restore Certificates
# ========================
echo "=== Restoring certificates into $DEST_VAULT ==="

shopt -s nullglob  # prevents *.backup from being literal if no files
for backupfile in $BACKUP_DIR/*.backup; do
    certname=$(basename "$backupfile" .backup)

    echo "Checking if certificate '$certname' exists in $DEST_VAULT..."
    if az keyvault certificate show --vault-name $DEST_VAULT --name $certname &>/dev/null; then
        echo "Certificate '$certname' already exists in $DEST_VAULT. Deleting and purging..."
        az keyvault certificate delete --vault-name $DEST_VAULT --name $certname
        sleep 10
        az keyvault certificate purge --vault-name $DEST_VAULT --name $certname

        echo "Waiting 10 seconds for delete operation to settle..."
        sleep 10

        echo "Polling until purge of certificate '$certname' is complete..."
        while az keyvault certificate show --vault-name $DEST_VAULT --name $certname &>/dev/null; do
            sleep 5
        done
        echo "Certificate '$certname' purged."
    fi

    echo "Restoring certificate from $backupfile"
    az keyvault certificate restore \
      --vault-name $DEST_VAULT \
      --file "$backupfile"
    echo "Certificate '$certname' restored successfully."
done
shopt -u nullglob

echo "=== Certificate restore completed successfully ==="
