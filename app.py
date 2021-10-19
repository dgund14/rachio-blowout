import requests
import time

# get your key here https://rachio.readme.io/docs/authentication
token = ""

sprinkler_duration_seconds = 2 * 60
sleep_seconds = 4 * 60
runs_per_zone = 3
headers = {
    "Content-Type": "application/json",
    "Authorization": token
}
zone_start_payload = {
    "id": id,
    "duration": sprinkler_duration_seconds
}


def get_person_id():
    p = requests.get("https://api.rach.io/1/public/person/info",
                     headers=headers)
    return p.json().get("id")


def get_devices(person_id):
    r = requests.get(
        f'https://api.rach.io/1/public/person/{person_id}', headers=headers)
    print(r.json().get("username"))
    return r.json().get("devices")


def start(id):
    url = "https://api.rach.io/1/public/zone/start"
    requests.request("PUT", url, json=zone_start_payload, headers=headers)


person_id = get_person_id()

for device in get_devices(person_id):
    for zone in device.get("zones"):
        if (zone.get("enabled")):
            for i in range(runs_per_zone):
                print(
                    f'Starting #{i + 1} on {zone.get("name")} for {sprinkler_duration_seconds / 60} minutes.')
                start(zone.get("id"))
                time.sleep(sprinkler_duration_seconds)
                if (i + 1 == runs_per_zone):
                    print("Run complete!")
                else:
                    print(f'Sleeping for {sleep_seconds / 60} minutes.')
                    time.sleep(4 * 60)
