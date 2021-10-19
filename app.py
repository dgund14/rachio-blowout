import requests
import json
import time

token = ""

person = requests.get("https://api.rach.io/1/public/person/info", 
    headers={"Authorization":token})

person_id = person.json().get("id")
print(f'Person: {id_id}')
r = requests.get(f'https://api.rach.io/1/public/person/{person_id}', 
    headers={"Authorization":token})
json = json.loads(r.text)
exit
print(r.json().get("username"))
devices = r.json().get("devices")

def start(id):
    url = "https://api.rach.io/1/public/zone/start"
    payload = {
        "id": id,
        "duration": 120
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }
    requests.request("PUT", url, json=payload, headers=headers)


for device in devices:
    print(f'{device.get("name")} - {device.get("id")}')
    zones = device.get("zones")
    for zone in zones:
        if (zone.get("enabled")):
            for i in range(3):
                id = zone.get("id")
                name = zone.get("name")
                print(f'Starting run {i} - {name} for 2 minutes...')
                start(id)
                time.sleep(2 * 60)
                print("Sleeping for 4 minutes...")
                #TODO: Don't sleep on the last run
                time.sleep(4 * 60)
    print('Run completed!')
