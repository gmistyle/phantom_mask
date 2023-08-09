import json, re
from sqlalchemy.sql import func, text, insert, select
from database.enums import DayOfWeek
from database.engine import ENGINE
from database.tables import *


def get_next_auto_increment(Table) -> int:
    '''
    get next auto increment number from table status
    '''
    with ENGINE.connect() as cnx:
        query = cnx.execute(text(f"SHOW TABLE STATUS LIKE '{Table.name}';")).fetchone()

    return query.Auto_increment

def get_quantity_per_pec(mask_name: str):
    '''
    get quantity per pack from mask name
    '''
    pattern = re.compile(r'\((\d+) per pack\)')
    result = pattern.search(mask_name)
    
    return result.group(1)

def process_opening_hour_data(pharmacy_id: int, opening_hour_string: str):
    '''
    process business hour string to structured data and prepare for insert into DB
    '''
    def get_open_day_list(open_day_string: str):
        '''
        recognize open day string format type and return as available open day info list
        '''
        if open_day_string.count('-') == 1:
            start_to_end = open_day_string.split('-')
            start = DayOfWeek[start_to_end[0]].value
            end = DayOfWeek[start_to_end[1]].value
            
            open_day_list = [ DayOfWeek(i).name for i in range(start, end + 1) ]
        else:
            open_day_list = open_day_list + open_day_string.split(',')
        
        return open_day_list
    
    # clean string
    tmp = opening_hour_string.strip()
    tmp = tmp.replace(' ', '')
    opening_hour_list = tmp.split('/')

    prepare_list_to_insert_db = list()
    
    for opening_hour in opening_hour_list:
        open_day_string = opening_hour[:-11] # 取出所有的星期幾資訊
        open_time_string = opening_hour[-11:] # 取出 open, close 時間資訊

        open_day_list = get_open_day_list(open_day_string)
        open_time_list = open_time_string.split('-')

        for day in open_day_list:
            prepare_list_to_insert_db.append({
                'pharmacy_id' : pharmacy_id,
                'day_of_week' : DayOfWeek[day].value,
                'opening_time' : open_time_list[0],
                'closing_time' : open_time_list[1],
                'created_at' : func.now(),
                'is_deleted' : False
            })

    return prepare_list_to_insert_db

def import_pharmacies_data():
    # load json data
    with open(r'./data/pharmacies.json', 'r') as json_file:
        pharmacies_json_data = json.load(json_file)
    
    # primary key id
    cur_pharmacy_id = get_next_auto_increment(DB_pharmacy)
    cur_mask_id = get_next_auto_increment(DB_mask)

    # key-value for mask name to mask_id
    dict_mask_name_to_id = dict()

    # insert value for each table
    insert_pharmacy_list = list()
    insert_opening_hour_list = list()
    insert_mask_list = list
    insert_product_list = list()

    for pharmacy in pharmacies_json_data:
        pharmacy_id = cur_pharmacy_id
        
        #1 table - pharmacy
        insert_pharmacy_list.append({
            'id' : pharmacy_id,
            'name' : pharmacy['name'],
            'cash_balance' : pharmacy['cashBalance'],
            'created_at' : func.now(),
            'is_deleted' : False
        })
        cur_pharmacy_id += 1

        #2 table - business hour
        insert_opening_hour_list.extend(process_opening_hour_data(pharmacy_id, pharmacy['openingHours']))

        # process mask
        for mask in pharmacy['masks']:
            mask_name = mask['name']
            
            #3 table - mask (if not exist )
            if mask_name not in dict_mask_name_to_id:
                mask_id = cur_mask_id
                insert_mask_list.append({
                    'mask_id' : mask_id,
                    'name' : mask_name,
                    'quantity_per_pac' : get_quantity_per_pec(mask_name),
                    'created_at' : func.now(),
                    'is_deleted' : False
                })
                dict_mask_name_to_id[mask_name] = mask_id
                cur_mask_id += 1

            #4 table - product list
            insert_product_list.append({
                'mask_id' : dict_mask_name_to_id[mask_name],
                'pharmacy_id' : pharmacy_id,
                'sales_price' : mask['price'],
                'created_at' : func.now(),
                'is_deleted' : False
            })

    # insert into Database
    if len(insert_pharmacy_list) > 0:
        with ENGINE.connect() as cnx:
            cnx.execute(insert(DB_pharmacy).values(insert_pharmacy_list))

    if len(insert_opening_hour_list) > 0:
        with ENGINE.connect() as cnx:
            cnx.execute(insert(DB_pharmacy_opening_hours).values(insert_opening_hour_list))
            
    if len(insert_mask_list) > 0:
        with ENGINE.connect() as cnx:
            cnx.execute(insert(DB_mask).values(insert_mask_list))
            
    if len(insert_product_list) > 0:
        with ENGINE.connect() as cnx:
            cnx.execute(insert(DB_product_list).values(insert_product_list))
    
    return

def import_users_data():
    # load json data
    with open(r'./data/users.json', 'r') as json_file:
        users_json_data = json.load(json_file)

    # primary key id
    cur_user_id = get_next_auto_increment(DB_users)
    cur_pharmacy_id = get_next_auto_increment(DB_pharmacy)
    cur_mask_id = get_next_auto_increment(DB_mask)

    # key-value for pharmacy name to pharmacy_id and mask name to mask_id
    with ENGINE.connect() as cnx:
        query_pharmacy = cnx.execute(select([
            DB_pharmacy.c.name,
            DB_pharmacy.c.id
        ])).fetchall()
        query_mask = cnx.execute(select([
            DB_mask.c.name,
            DB_mask.c.id
        ])).fetchall()
        
    dict_pharmacy_name_to_id = dict(query_pharmacy)
    dict_mask_name_to_id = dict(query_mask)

    # insert value for each table
    insert_user_list = list()
    insert_transaction_history_list = list()
    insert_pharmacy_list = list()
    insert_mask_list = list

    for users in users_json_data:
        user_id = cur_user_id

        #5 table - users
        insert_user_list.append({
            'id' : user_id,
            'name' : users['name'],
            'cash_balance' : users['cashBalance'],
            'created_at' : func.now(),
            'is_deleted' : False
        })

        for tx_history in users['purchaseHistories']:
            pharmacy_name = tx_history['pharmacyName']
            mask_name = tx_history['maskName']

            # check if pharmacy exist
            if pharmacy_name not in dict_pharmacy_name_to_id:
                pharmacy_id = cur_pharmacy_id
                insert_pharmacy_list.append({
                    'id' : pharmacy_id,
                    'name' : pharmacy_name,
                    'cash_balance' : 0,
                    'created_at' : func.now(),
                    'is_deleted' : False
                })
                dict_pharmacy_name_to_id[pharmacy_name] = pharmacy_id
                cur_pharmacy_id += 1

            # check if mask exist
            if mask_name not in dict_mask_name_to_id:
                mask_id = cur_mask_id
                insert_mask_list.append({
                    'id' : mask_id,
                    'name' : mask_name,
                    'quantity_per_pac' : get_quantity_per_pec(mask_name),
                    'created_at' : func.now(),
                    'is_deleted' : False
                })
                dict_mask_name_to_id[mask_name] = mask_id
                cur_mask_id += 1

            #6 table - transaction history
            insert_transaction_history_list.append({
                'user_id' : user_id,
                'mask_id' : dict_mask_name_to_id[mask_name],
                'pharmacy_id' : dict_pharmacy_name_to_id[pharmacy_name],
                'transaction_amount' : tx_history['transactionAmount'],
                'transaction_date' : tx_history['transactionDate'],
                'created_at' : func.now(),
                'is_deleted' : False
            })

    # insert into Database
    if len(insert_pharmacy_list) > 0:
        with ENGINE.connect() as cnx:
            cnx.execute(insert(DB_pharmacy).values(insert_pharmacy_list))

    if len(insert_mask_list) > 0:
        with ENGINE.connect() as cnx:
            cnx.execute(insert(DB_mask).values(insert_mask_list))

    if len(insert_user_list) > 0:
        with ENGINE.connect() as cnx:
            cnx.execute(insert(DB_users).values(insert_user_list))

    if len(insert_transaction_history_list) > 0:
        with ENGINE.connect() as cnx:
            cnx.execute(insert(DB_transaction_history).values(insert_transaction_history_list))

    return

if __name__ == '__main__':
    create_tables()
    import_pharmacies_data()
    import_users_data()

    print('import success!')