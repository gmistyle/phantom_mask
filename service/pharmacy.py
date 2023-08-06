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
    
    def find_pharmacy_business_hour(self, conditions: PharmacyConditions):
        if conditions.business_hour == None and conditions.day_of_week == None:
            raise Exception('time and day_of_week cannot be both None')
        
        where_clause = PharmacyConditionProcessor.get_where_clause(conditions, satisfy_all_conditions=True)
        query_result = PharmacyDao().query_pharmacy_join_business_hour(where_clause)

        result = list()
        for row in query_result:
            result.append({
                'pharmacy_id': getattr(row, PharmacyDao._alias_pharmacy_id),
                'pharmacy_name': getattr(row, PharmacyDao._alias_pharmacy_name),
                'pharmacy_balance': getattr(row, PharmacyDao._alias_pharmacy_balance),
                'day_of_week': DayOfWeek(getattr(row, PharmacyDao._alias_Pharmacy_business_day_of_week)).name,
                'open_time': getattr(row, PharmacyDao._alias_pharmacy_open_time),
                'close_time': getattr(row, PharmacyDao._alias_pharmacy_close_time)
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

    # Search for pharmacies or masks by name, ranked by relevance to the search term.
