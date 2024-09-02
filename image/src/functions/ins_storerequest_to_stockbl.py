from functions.additional_functions import *
import decimal
from models import L_lager

def ins_storerequest_to_stockbl(to_stock:int, curr_lager:int):
    lager_bez1 = ""
    flag = 0
    l_lager = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lager_bez1, flag, l_lager


        return {"lager_bez1": lager_bez1, "flag": flag}


    l_lager = db_session.query(L_lager).filter(
            (L_lager.lager_nr == to_stock)).first()

    if not l_lager:
        flag = 1

        return generate_output()

    if to_stock == curr_lager:
        flag = 2

        return generate_output()
    lager_bez1 = l_lager.bezeich

    return generate_output()