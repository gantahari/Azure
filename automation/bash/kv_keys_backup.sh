#!/bin/bash
# Backup and Restore Keys between two Azure Key Vaults with conflict handling + purge wait
# Author: Hari

set -e

SOURCE_VAULT="keyvault01westus2"
DEST_VAULT="keyvault01eastus2"
BACKUP_DIR="./kv-backups"

mkdir -p $BACKUP_DIR


echo "=== Starting backup from $SOURCE_VAULT ==="

# Backup
for keyname in $(az keyvault key list --vault-name $SOURCE_VAULT --query "[].name" -o tsv); do
    echo "Backing up key: $keyname"
    az keyvault key backup \
      --vault-name $SOURCE_VAULT \
      --name $keyname \
      --file "$BACKUP_DIR/$keyname.backup"
done

echo "=== Backup completed. Files saved in $BACKUP_DIR ==="

# Restore
echo "=== Restoring into $DEST_VAULT ==="

for backupfile in $BACKUP_DIR/*.backup; do
    keyname=$(basename "$backupfile" .backup)

    echo "Checking if key '$keyname' exists in $DEST_VAULT..."
    if az keyvault key show --vault-name $DEST_VAULT --name $keyname &>/dev/null; then
        echo "Key '$keyname' already exists in $DEST_VAULT. Deleting and purging..."
        az keyvault key delete --vault-name $DEST_VAULT --name $keyname
	    sleep 10
        az keyvault key purge --vault-name $DEST_VAULT --name $keyname
	    10

        # 🔹 Wait until key is fully purged
        echo "Waiting for purge of key '$keyname'..."
        while az keyvault key show --vault-name $DEST_VAULT --name $keyname &>/dev/null; do
            sleep 5
        done
        echo "Key '$keyname' purged."
    fi

    echo "Restoring key from $backupfile"
    az keyvault key restore \
      --vault-name $DEST_VAULT \
      --file "$backupfile"
    echo "Key '$keyname' restored successfully."
done

echo "=== Restore completed successfully ==="

