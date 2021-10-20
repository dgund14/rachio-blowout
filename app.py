import requests
import time

# get your key here https://rachio.readme.io/docs/authentication
token = ""

sprinkler_duration_seconds = 90
sleep_seconds = 4 * 60
runs_per_zone = 3
headers = {
    "Content-Type": "application/json",
    "Authorization": token
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
    requests.request("PUT", url, json={
        "id": id,
        "duration": sprinkler_duration_seconds
    }, headers=headers)


person_id = get_person_id()

for device in get_devices(person_id):
    zones = device.get("zones")
    zone_count = 0
    for zone in zones:
        if (zone.get("enabled")):
            zone_count = zone_count + 1
    total_runtime_seconds = zone_count * \
        (sprinkler_duration_seconds + sleep_seconds) * runs_per_zone
    print(
        f'Estimated time for {zone_count} zones: {total_runtime_seconds / 60} minutes')
    for zone in zones:
        current_zone_count = 0
        if (zone.get("enabled")):
            current_zone_count = current_zone_count + 1
            for i in range(runs_per_zone):
                print(
                    f'(Zone {current_zone_count}/{zone_count}) Starting {i + 1}/{runs_per_zone} on {zone.get("name")} for {sprinkler_duration_seconds / 60} minutes.')
                start(zone.get("id"))
                time.sleep(sprinkler_duration_seconds)
                if (i + 1 != runs_per_zone and zone_count != current_zone_count):
                    print(f'Sleeping for {sleep_seconds / 60} minutes.')
                    time.sleep(sleep_seconds)
                if (i + 1 == runs_per_zone):
                    print(
                        f'{runs_per_zone} run{"" if runs_per_zone == 1 else "s"} completed for {zone.get("name")}!')
            print('All zones completed!')
