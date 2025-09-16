
import requests
import pandas as pd
from azure.identity import DefaultAzureCredential

cred = DefaultAzureCredential()
token=cred.get_token("https://graph.microsoft.com/.default").token
header={
    "Authorization":f"Bearer {token}",
    "Content-Type":"application/json"
}

df = pd.read_csv("users.csv")

for i,row in df.iterrows():
    user_data={
    "accountEnabled": True,
    "displayName": row["displayName"],
    "mailNickname": row["mailNickname"],
    "userPrincipalName": row["userPrincipalName"],
    "passwordProfile" : {
        "forceChangePasswordNextSignIn": True,
        "password": row["password"],
        }
    }
    
    response = requests.post("https://graph.microsoft.com/v1.0/users",json=user_data,headers=header)
    if response.status_code==201:
        print("user created")
    else:
        print(f"error while creating user {row['displayName']}, {response.text}")
        


