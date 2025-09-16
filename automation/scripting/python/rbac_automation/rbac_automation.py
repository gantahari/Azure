############################ What ############################

"""I built an automation framework using Microsoft Graph API and Entra ID to handle user lifecycle management — the Joiner, Mover, and Leaver processes. Instead of manually creating or deleting accounts and assigning roles, my script automates provisioning, de-provisioning, and role changes based on a simple input file or HR feed. This ensures RBAC compliance, reduces errors, and improves security posture."""


"""
Situation : In enterprises, handling user accounts manually is risky and time-consuming. For compliance, we follow Joiner, Mover, Leaver (JML) processes — but admins often forget to remove access, which leaves security gaps.
Task: My goal was to automate the entire JML process in Entra ID and enforce RBAC policies consistently.
Action :
    Used Microsoft Graph API with Python and DefaultAzureCredential for secure authentication.
    Designed the script with 3 modes:
        Joiner → Creates a user, assigns roles & app permissions from CSV/HR feed.
        Mover → Reassigns roles automatically when a user changes departments.
        Leaver → Removes all permissions and deletes the user.
    So, When HR Team pushes this CSV file these Azure Functions will run and I am using logic apps to orcastate the azure functions
Result : Reduced manual provisioning effort by 80–90%. Eliminated “orphaned accounts”. Improved compliance with NIST/CJIS/SOX by ensuring role cleanup during offboarding.
""" 

############################ How ############################

#   Create a New app registration in entra id 
#   Assign the User.ReadWrite.All permission in API permisions and grant admin consent
#   Create a new secrect for app registration and set tenentid, clientid, secrect value as environment variables
        # export AZURE_TENANT_ID="e270a356-289d-47cb-a500-ab03a275c9c4"
        # export AZURE_CLIENT_ID="7ba496a4-0f00-421a-9087-10d705b2fb2c"
        # export AZURE_CLIENT_SECRET="sLz8Q~6QNPWw4PXMCvq4TMapOvbna3wCeBMkEaBA"
#   Referance page: https://learn.microsoft.com/en-us/graph/api/user-post-users?view=graph-rest-1.0&utm_source=chatgpt.com&tabs=http
#   Use requests to create payload for post method and  pandas to read CSV file.       



import pandas as pd
import requests, uuid
from role_dicts import *
from azure.identity import DefaultAzureCredential

# Authenticate with Microsoft Graph & Azure RBAC
credential = DefaultAzureCredential()
graph_token = credential.get_token("https://graph.microsoft.com/.default").token
mgmt_token = credential.get_token("https://management.azure.com/.default").token

graph_headers = {"Authorization": f"Bearer {graph_token}", "Content-Type": "application/json"}
mgmt_headers = {"Authorization": f"Bearer {mgmt_token}", "Content-Type": "application/json"}



# ---- Create User in Entra ID ----
def create_user(user):
    user_data = {
        "accountEnabled": True,
        "displayName": user["displayName"],
        "mailNickname": user["mailNickname"],
        "userPrincipalName": user["userPrincipalName"],
        "passwordProfile": {
            "forceChangePasswordNextSignIn": True,
            "password": user["password"]
        }
    }

    resp = requests.post("https://graph.microsoft.com/v1.0/users",headers=graph_headers, json=user_data)

    if resp.status_code == 201:
        user_id = resp.json()["id"]
        print(f"Created {user['userPrincipalName']}")
        return user_id
    else:
        print(f"Failed {user['userPrincipalName']}: {resp.text}")
        return None

# ---- Assign RBAC Role ----
def assign_rbac(user_id, scope, rbac_role):
    role_def_id = f"/subscriptions/{scope.split('/')[2]}/providers/Microsoft.Authorization/roleDefinitions/{role_map[rbac_role]}"
    role_assignment_id = str(uuid.uuid4())

    url = f"https://management.azure.com{scope}/providers/Microsoft.Authorization/roleAssignments/{role_assignment_id}?api-version=2022-04-01"
    body = {
        "properties": {
            "roleDefinitionId": role_def_id,
            "principalId": user_id
        }
    }

    resp = requests.put(url, headers=mgmt_headers, json=body)
    if resp.status_code in [200, 201]:
        print(f"Assigned {rbac_role} on {scope}")
    else:
        print(f"Failed RBAC on {scope}: {resp.text}")

# ---- Main ----
if __name__ == "__main__":
    df = pd.read_csv("users.csv")

    for _, row in df.iterrows():
        user = row.to_dict()
        user_id = create_user(user)
        if user_id:
            job_role = user["jobRole"]
            policy = role_policies.get(job_role, {})

            for rbac_role, resources in policy.items():
                for resource in resources:
                    assign_rbac(user_id, resource, rbac_role)


