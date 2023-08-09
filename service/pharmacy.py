from database.enums import DayOfWeek
from database.dao_pharmacy import PharmacyDao, PharmacyConditions, PharmacyConditionProcessor


class PharmacyService:
    def find_by_name(self, conditions: PharmacyConditions):
        if conditions.search_keyword == None:
            raise Exception('keyword cannot be None')

        where_clause = PharmacyConditionProcessor.get_where_clause(conditions, satisfy_all_conditions=True)
        query_result = PharmacyDao().query_by_fulltext(where_clause, keyword=conditions.search_keyword)

        result = list()
        for row in query_result:
            result.append({
                'pharmacy_id': getattr(row, PharmacyDao._alias_pharmacy_id),
                'pharmacy_name': getattr(row, PharmacyDao._alias_pharmacy_name),
                'pharmacy_balance': getattr(row, PharmacyDao._alias_pharmacy_balance)
            })

        return result
    
    def find_pharmacy_opening_hour(self, conditions: PharmacyConditions):
        if conditions.opening_hour == None and conditions.day_of_week == None:
            raise Exception('time and day_of_week cannot be both None')
        
        where_clause = PharmacyConditionProcessor.get_where_clause(conditions, satisfy_all_conditions=True)
        query_result = PharmacyDao().query_pharmacy_join_opening_hour(where_clause)

        # 整理營業時間格式
        dict_opening_hour = dict()
        for row in query_result:
            pharmacy_id = getattr(row, PharmacyDao._alias_pharmacy_id)
            open_time_string = str(getattr(row, PharmacyDao._alias_pharmacy_open_time))[:5] # 取出 HH:MM
            close_time_string = str(getattr(row, PharmacyDao._alias_pharmacy_close_time))[:5] # 取出 HH:MM
            opening_time_string = f'{open_time_string} - {close_time_string}' # 組合成 HH:MM - HH:MM
            
            # 每個 藥局 的 營業時間 
            if dict_opening_hour.get(pharmacy_id) == None:
                dict_opening_hour[pharmacy_id] = dict()

            # 每個 藥局 的 營業時間 在星期幾有營業
            if dict_opening_hour.get(pharmacy_id).get(opening_time_string) == None:
                dict_opening_hour[pharmacy_id][opening_time_string] = list()

            day_of_week = DayOfWeek(getattr(row, PharmacyDao._alias_Pharmacy_business_day_of_week)).name
            dict_opening_hour[pharmacy_id][opening_time_string].append(day_of_week)

        # response
        result = list()
        for row in query_result:
            pharmacy_id = getattr(row, PharmacyDao._alias_pharmacy_id)

            if dict_opening_hour.get(pharmacy_id):
                dict_opening_hour_info = dict_opening_hour[pharmacy_id]
                opening_hour_list = list()
                
                for opening_time_string in dict_opening_hour_info:
                    open_day_list = dict_opening_hour_info[opening_time_string]
                    open_day_string = ', '.join(open_day_list)
                    opening_hour_list.append(f'{open_day_string} {opening_time_string}')

                opening_hour_string = ' / '.join(opening_hour_list)
            else:
                opening_hour_string = '無營業時間資訊'
            
            result.append({
                'pharmacy_id': pharmacy_id,
                'pharmacy_name': getattr(row, PharmacyDao._alias_pharmacy_name),
                'pharmacy_balance': getattr(row, PharmacyDao._alias_pharmacy_balance),
                "opening_hour": opening_hour_string
            })

        return result
    
    def find_pharmacy_products(self, conditions: PharmacyConditions):
        if conditions.min_price == None and conditions.max_price == None:
            raise Exception('min_price and max_price cannot be both None')
        
        where_clause = PharmacyConditionProcessor.get_where_clause(conditions, satisfy_all_conditions=True)
        query_result = PharmacyDao().query_pharmacy_join_product_list_and_mask(where_clause)

        result = list()
        for row in query_result:
            result.append({
                'pharmacy_id': getattr(row, PharmacyDao._alias_pharmacy_id),
                'pharmacy_name': getattr(row, PharmacyDao._alias_pharmacy_name),
                'pharmacy_balance': getattr(row, PharmacyDao._alias_pharmacy_balance),
                'mask_id': getattr(row, PharmacyDao._alias_mask_id),
                'mask_name': getattr(row, PharmacyDao._alias_mask_name),
                'mask_price': getattr(row, PharmacyDao._alias_product_sales_price)
            })

        return result
