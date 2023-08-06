from database.dao_mask import MaskDao, MaskConditions, MaskConditionProcessor
from database.dao_pharmacy import PharmacyDao, PharmacyConditionProcessor


class MaskService:
    def find_by_name(self, conditions: MaskConditions):
        if conditions.search_keyword == None:
            raise Exception('keyword cannot be None')
        
        where_clause = MaskConditionProcessor.get_where_clause(conditions, satisfy_all_conditions=True)
        query_result = MaskDao().query_by_fulltext(where_clause, keyword=conditions.search_keyword)

        result = list()
        for row in query_result:
            result.append({
                'mask_id': getattr(row, MaskDao._alias_mask_id),
                'mask_name': getattr(row, MaskDao._alias_mask_name)
            })
        
        return result
    
    def find_by_pharmacy(self, conditions):
        if conditions.pharmacy_id == None:
            raise Exception('pharmacy_id cannot be None')
        
        where_clause = PharmacyConditionProcessor.get_where_clause(conditions, satisfy_all_conditions=True)
        query_result = PharmacyDao().query_pharmacy_join_product_list_and_mask(where_clause)

        result = list()
        for row in query_result:
            result.append({
                'mask_id': getattr(row, PharmacyDao._alias_mask_id),
                'mask_name': getattr(row, PharmacyDao._alias_mask_name),
                'mask_price': getattr(row, PharmacyDao._alias_product_sales_price)
            })

        return result