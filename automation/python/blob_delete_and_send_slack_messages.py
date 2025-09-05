# This python code will delete the blobs(real-time energy usage data from industrial IoT sensors, including power, voltage, and temperature metrics.) which are been so long from the sepecifed containers
# and will send a slack message about the deleted blobs and it will also insert record into the cosmos db.
# Future enhancement. Need to update this data to cosmos db also.


from azure.identity import DefaultAzureCredential
from azure.storage.blob import ContainerClient
from azure.storage.queue import QueueClient
from datetime import datetime, timezone
from slack_sdk import WebClient

res_group_name ="hari-fun-rg"
sub_id="606e824b-aaf7-4b4e-9057-b459f6a4436d"
loc="eastus"
container_name="input"
account_name="sahari23432"
account_blob_url=f"https://{account_name}.blob.core.windows.net/"
account_queue_url=f"https://{account_name}.queue.core.windows.net/"

cred=DefaultAzureCredential()
blobClient=ContainerClient(account_url=account_blob_url,container_name=container_name,credential=cred)
blobClient.upload_blob(name="requirements1.txt", data="Hello World",overwrite=True)
blobClient.upload_blob(name="requirements2.txt", data="Hello World",overwrite=True)

queueClient=QueueClient(account_url=account_queue_url,queue_name="queue1",credential=cred)

current_datetime=datetime.now(timezone.utc)
for blobs in blobClient.list_blobs():
    creation_datetime =blobs.creation_time.astimezone(timezone.utc)
    diff=current_datetime-creation_datetime
    if diff.seconds>100:
        blobClient.delete_blob(blobs["name"])
        queueClient.send_message(blobs["name"])
    

slack_token = "xoxb-9083927654419-9104319687745-XVY3rAG4g0TNHwjeMzgAS9N6"
client = WebClient(token=slack_token)
channel_id = "C092FTAJRQT"

all_messages=[]
while True:
    messages = queueClient.receive_messages(messages_per_page=32)
    batch = list(messages)
    if not batch:
        break  

    for msg in batch:
        all_messages.append(msg.content)
        queueClient.delete_message(msg) 

message=f"the files are deleted {all_messages}"
response = client.chat_postMessage(channel=channel_id, text=message)
print(f"Message sent successfully: {response['message']['text']}")