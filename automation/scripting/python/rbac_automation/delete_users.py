import requests
from azure.identity import DefaultAzureCredential

cred = DefaultAzureCredential()
token = cred.get_token("https://graph.microsoft.com/.default").token
header={
    "Authorization": f"Bearer {token}"
}
user_id="mike.ross@ursghp12gmail.onmicrosoft.com"
response = requests.delete(f"https://graph.microsoft.com/v1.0/users/{user_id}",headers=header)
print(response.status_code)
if response.status_code in [200,201,204]:
    print("user deleted")
else:
    print(response.text)