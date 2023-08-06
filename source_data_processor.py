import os
import json

os.getcwd()


with open(r'./data/pharmacies.json', 'r') as json_file:
    pharmacies_json_data = json.load(json_file)

with open(r'./data/users.json', 'r') as json_file:
    users_json_data = json.load(json_file)

len(pharmacies_json_data)
len(users_json_data)


def insert_into_database(data):
    return