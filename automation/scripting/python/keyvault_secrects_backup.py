# This python code will take backup of secrets from one keyvault to another
# This will help in DR mostly
# This will check the secrect vaules from soure KV againest the destination KV if both are same then it doesnt do anything
# Otherwise it will insert the secrect value from the source KV to dest KV
# This will run as a azure function when there is a new secrect version is created in source KV with the help of events in KV




from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

class KeyVaultSecrets:
    def __init__(self,oldkv,newkv):
        self.oldkv_url=f'https://{oldkv}.vault.azure.net'
        self.newkv_url=f'https://{newkv}.vault.azure.net'
        self.credentials=DefaultAzureCredential()
        self.oldkv_secret_client=SecretClient(vault_url=self.oldkv_url,credential=self.credentials)
        self.newkv_secret_client=SecretClient(vault_url=self.newkv_url,credential=self.credentials)


    def secret_migration(self):
        print("===== Secrets Migration Started =====")
        for i in self.oldkv_secret_client.list_properties_of_secrets():
            secret_name=i.name
            old_secret_value=self.oldkv_secret_client.get_secret(secret_name).value
            try:
                new_secret_value=self.newkv_secret_client.get_secret(secret_name).value
                if old_secret_value==new_secret_value:
                    print(f"===== Secret value is not changed. So skipping the {secret_name} migration =====")
                    continue
            except:
                pass
            self.newkv_secret_client.set_secret(secret_name,old_secret_value)
            print(f"===== Secret Value is updated for secret {secret_name}")
        print("All secrets migrated successfully")

oldkv = "keyvault01westus2"
newkv = "keyvault01southindia"

obj = KeyVaultSecrets(oldkv,newkv)
obj.secret_migration()