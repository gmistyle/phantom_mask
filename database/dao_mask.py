import datetime
from sqlalchemy import select, desc, and_, or_, text
from dataclasses import dataclass
from engine import ENGINE
from tables import DB_mask


@dataclass
class MaskConditions:
    search_keyword: str = None
    # mask
    specific_mask_id: int = None
    
class MaskConditionProcessor:
    @staticmethod
    def get_where_clause(condition: MaskConditions, satisfy_all_conditions=False):
        filters = list()

        # keyword
        if condition.search_keyword:
            filters.append(text("MATCH (name) AGAINST (:keyword IN NATURAL LANGUAGE MODE)").bindparams(keyword=condition.search_keyword))

        # id
        if condition.specific_mask_id:
            filters.append(DB_mask.c.id == condition.specific_mask_id)

        filters.append(DB_mask.c.is_deleted == False)

        
        if satisfy_all_conditions == True:
            return and_(*filters)
        else:
            return or_(*filters)

class MaskDao:
    _alias_mask_id = "mask_id"
    _alias_mask_name = "mask_name"
    _alias_product_sales_price = "mask_price"

    def query_by_fulltext(self, where_clause, keyword):
        fulltext_search = text("MATCH (name) AGAINST (:keyword IN NATURAL LANGUAGE MODE)").bindparams(keyword=keyword)

        # 執行全文檢索並按照關聯性排序
        with ENGINE.connect() as cnx:
            query = cnx.execute(select([
                DB_mask.c.id.label(self._alias_mask_id),
                DB_mask.c.name.label(self._alias_mask_name)
            ]).where(where_clause).order_by(
                desc(fulltext_search)
            )).fetchall()

        return query
