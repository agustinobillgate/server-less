#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Prmarket, Queasy, Prtable

margt_list_list, Margt_list = create_model_like(Prmarket)
mrmcat_list_list, Mrmcat_list = create_model_like(Prmarket)

def prtable_admin_chgbl(margt_list_list:[Margt_list], mrmcat_list_list:[Mrmcat_list], market_bezeich:string, fix_rate:bool, curr_sen:bool, s:string, rec_id:int, nr:int):

    prepare_cache ([Prmarket, Queasy, Prtable])

    prmarket = queasy = prtable = None

    margt_list = mrmcat_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal prmarket, queasy, prtable
        nonlocal market_bezeich, fix_rate, curr_sen, s, rec_id, nr


        nonlocal margt_list, mrmcat_list

        return {}

    def update_array():

        nonlocal prmarket, queasy, prtable
        nonlocal market_bezeich, fix_rate, curr_sen, s, rec_id, nr


        nonlocal margt_list, mrmcat_list

        i:int = 0

        prtable = get_cache (Prtable, {"_recid": [(eq, rec_id)]})

        if prtable:
            pass
            for i in range(1,99 + 1) :
                prtable.zikatnr[i - 1] = 0
                prtable.argtnr[i - 1] = 0
            i = 0

            for mrmcat_list in query(mrmcat_list_list):
                i = i + 1
                prtable.zikatnr[i - 1] = mrmcat_list.nr
            i = 0

            for margt_list in query(margt_list_list):
                i = i + 1
                prtable.argtnr[i - 1] = margt_list.nr
            pass
            pass

    prmarket = get_cache (Prmarket, {"nr": [(eq, nr)]})

    if prmarket:
        pass
        prmarket.bezeich = market_bezeich
        pass
        pass

        queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, nr)]})

        if queasy:
            pass
            queasy.logi3 = fix_rate

            if curr_sen:
                queasy.char3 = s
            pass
            pass
        update_array()

    return generate_output()