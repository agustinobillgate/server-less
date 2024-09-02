from functions.additional_functions import *
import decimal
from models import L_order

def ins_pr_b1bl(t_recid:int, quality:str, bez:str):
    l_order = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_order


        return {}


    where = query(where_list, filters=(lambda where :l_order._recid == t_recid), l_order=True)
    l_order.quality = to_string(substring(quality, 0, 11) , "x(11)") + bez

    l_order = db_session.query(L_order).first()

    return generate_output()