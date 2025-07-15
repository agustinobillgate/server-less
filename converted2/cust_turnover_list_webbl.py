#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.cust_turnover_listbl import cust_turnover_listbl
from models import Queasy

def cust_turnover_list_webbl(cardtype:int, sort_type:int, curr_sort1:int, fdate:date, tdate:date, check_ftd:bool, currency:string, excl_other:bool, curr_sort2:int, idflag:string):

    prepare_cache ([Queasy])

    sort1:int = 0
    tmp_counter:int = 0
    queasy = None

    cust_list = bqueasy = pqueasy = None

    cust_list_data, Cust_list = create_model("Cust_list", {"gastnr":int, "cust_name":string, "gesamtumsatz":Decimal, "logiernachte":int, "argtumsatz":Decimal, "f_b_umsatz":Decimal, "sonst_umsatz":Decimal, "wohnort":string, "plz":string, "land":string, "sales_id":string, "ba_umsatz":Decimal, "ly_rev":Decimal, "region":string, "region1":string, "stayno":int, "resnr":string, "counter":int, "counterall":int, "resno":int, "reslinnr":int, "curr_pos":int})

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Pqueasy = create_buffer("Pqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal sort1, tmp_counter, queasy
        nonlocal cardtype, sort_type, curr_sort1, fdate, tdate, check_ftd, currency, excl_other, curr_sort2, idflag
        nonlocal bqueasy, pqueasy


        nonlocal cust_list, bqueasy, pqueasy
        nonlocal cust_list_data

        return {}


    queasy = Queasy()
    db_session.add(queasy)

    queasy.key = 285
    queasy.char1 = "Guest Turnover"
    queasy.number1 = 1
    queasy.char2 = idflag


    pass
    curr_sort2, sort1, cust_list_data = get_output(cust_turnover_listbl(cardtype, sort_type, curr_sort1, fdate, tdate, check_ftd, currency, excl_other, curr_sort2))

    for cust_list in query(cust_list_data):
        tmp_counter = tmp_counter + 1


        pqueasy = Queasy()
        db_session.add(pqueasy)

        pqueasy.key = 280
        pqueasy.char1 = "Guest Turnover"
        pqueasy.char3 = idflag
        pqueasy.number1 = tmp_counter

        if cust_list.gastnr == None or cust_list.sales_id == None:
            pqueasy.char2 = to_string(" ") + "|" +\
                    to_string(cust_list.cust_name) + "|" +\
                    to_string(cust_list.gesamtumsatz) + "|" +\
                    to_string(cust_list.logiernachte) + "|" +\
                    to_string(cust_list.argtumsatz) + "|" +\
                    to_string(cust_list.f_b_umsatz) + "|" +\
                    to_string(cust_list.sonst_umsatz) + "|" +\
                    to_string(cust_list.wohnort) + "|" +\
                    to_string(cust_list.plz) + "|" +\
                    to_string(cust_list.land) + "|" +\
                    to_string(" ") + "|" +\
                    to_string(cust_list.ba_umsatz) + "|" +\
                    to_string(cust_list.ly_rev) + "|" +\
                    to_string(cust_list.region) + "|" +\
                    to_string(cust_list.region1) + "|" +\
                    to_string(cust_list.stayno) + "|" +\
                    to_string("0") + "|" +\
                    to_string(cust_list.counter) + "|" +\
                    to_string(cust_list.counterall) + "|" +\
                    to_string(cust_list.resno) + "|" +\
                    to_string(cust_list.reslinnr) + "|" +\
                    to_string(cust_list.curr_pos)


        else:
            pqueasy.char2 = to_string(cust_list.gastnr) + "|" +\
                    to_string(cust_list.cust_name) + "|" +\
                    to_string(cust_list.gesamtumsatz) + "|" +\
                    to_string(cust_list.logiernachte) + "|" +\
                    to_string(cust_list.argtumsatz) + "|" +\
                    to_string(cust_list.f_b_umsatz) + "|" +\
                    to_string(cust_list.sonst_umsatz) + "|" +\
                    to_string(cust_list.wohnort) + "|" +\
                    to_string(cust_list.plz) + "|" +\
                    to_string(cust_list.land) + "|" +\
                    to_string(cust_list.sales_id) + "|" +\
                    to_string(cust_list.ba_umsatz) + "|" +\
                    to_string(cust_list.ly_rev) + "|" +\
                    to_string(cust_list.region) + "|" +\
                    to_string(cust_list.region1) + "|" +\
                    to_string(cust_list.stayno) + "|" +\
                    to_string("0") + "|" +\
                    to_string(cust_list.counter) + "|" +\
                    to_string(cust_list.counterall) + "|" +\
                    to_string(cust_list.resno) + "|" +\
                    to_string(cust_list.reslinnr) + "|" +\
                    to_string(cust_list.curr_pos)


        pass

    bqueasy = get_cache (Queasy, {"key": [(eq, 285)],"char1": [(eq, "guest turnover")],"char2": [(eq, idflag)]})

    if bqueasy:
        pass
        bqueasy.number1 = 0


        pass
        pass

    return generate_output()