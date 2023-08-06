import os
import json

os.getcwd()


with open(r'./data/pharmacies.json', 'r') as json_file:
    pharmacies_json_data = json.load(json_file)

with open(r'./data/users.json', 'r') as json_file:
    users_json_data = json.load(json_file)

len(pharmacies_json_data)
len(users_json_data)


def date_time_converter(date_info_string):
    # remove
    tmp = date_info_string.strip()
    tmp = tmp.replace(' ', '')
    business_hour_list = tmp.split('/')

    for business_hour in business_hour_list:
        day_of_week_info = business_hour[:-11] # 取出所有的星期幾資訊
        time_info = business_hour[-11:] # 取出 open, close 時間資訊

        # *** todo ***

    new_time_info = ''
    return new_time_info

def insert_into_database(data):
    
    
    return