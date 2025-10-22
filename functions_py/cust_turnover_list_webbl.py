#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 26/9/2025
#
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.cust_turnover_listbl import cust_turnover_listbl
from models import Queasy

def cust_turnover_list_webbl(cardtype:int, sort_type:int, curr_sort1:int, fdate:date, tdate:date, check_ftd:bool, currency:string, excl_other:bool, curr_sort2:int, idflag:string):

    prepare_cache ([Queasy])

    sort1:int = 0
    tmp_counter:int = 0
    gastnr_str:string = ""
    sales_id_str:string = ""
    resno_str:string = ""
    reslinnr_str:string = ""
    queasy = None

    cust_list = bqueasy = pqueasy = None

    cust_list_data, Cust_list = create_model("Cust_list", {"gastnr":int, "cust_name":string, "gesamtumsatz":Decimal, "logiernachte":int, "argtumsatz":Decimal, "f_b_umsatz":Decimal, "sonst_umsatz":Decimal, "wohnort":string, "plz":string, "land":string, "sales_id":string, "ba_umsatz":Decimal, "ly_rev":Decimal, "region":string, "region1":string, "stayno":int, "resnr":string, "counter":int, "counterall":int, "resno":int, "reslinnr":int, "curr_pos":int})

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Pqueasy = create_buffer("Pqueasy",Queasy)


    db_session = local_storage.db_session

    currency = currency.strip()

    def generate_output():
        nonlocal sort1, tmp_counter, gastnr_str, sales_id_str, resno_str, reslinnr_str, queasy
        nonlocal cardtype, sort_type, curr_sort1, fdate, tdate, check_ftd, currency, excl_other, curr_sort2, idflag
        nonlocal bqueasy, pqueasy


        nonlocal cust_list, bqueasy, pqueasy
        nonlocal cust_list_data

        return {}


    # Rd, 1/10/2025 - simpan start flag
    queasy = Queasy()
    db_session.add(queasy)

    queasy.key = 285
    queasy.char1 = "Guest Turnover"
    queasy.number1 = 1      # 1: start, 0: end (Rd, 1/10/2025)
    queasy.char2 = idflag

    curr_sort2, sort1, cust_list_data = get_output(cust_turnover_listbl(cardtype, sort_type, curr_sort1, fdate, tdate, check_ftd, currency, excl_other, curr_sort2))

    for cust_list in query(cust_list_data):
        tmp_counter = tmp_counter + 1

        pqueasy = Queasy()
        db_session.add(pqueasy)

        pqueasy.key = 280
        pqueasy.char1 = "Guest Turnover"
        pqueasy.char3 = idflag
        pqueasy.number1 = tmp_counter

        if cust_list.gastnr == None:
            gastnr_str = " "
        else:
            gastnr_str = to_string(cust_list.gastnr)

        if cust_list.sales_id == None:
            sales_id_str = " "
        else:
            sales_id_str = to_string(cust_list.sales_id)

        if cust_list.resno == None:
            resno_str = " "
        else:
            resno_str = to_string(cust_list.resno)

        if cust_list.reslinnr == None:
            reslinnr_str = " "
        else:
            reslinnr_str = to_string(cust_list.reslinnr)

        if cust_list.cust_name == None:
            cust_list.cust_name = " "

        if cust_list.wohnort == None:
            cust_list.wohnort = " "

        if cust_list.region == None:
            cust_list.region = " "

        if cust_list.region1 == None:
            cust_list.region1 = " "

        if cust_list.plz == None:
            cust_list.plz = " "

        if cust_list.land == None:
            cust_list.land = " "
        pqueasy.char2 = gastnr_str + "|" +\
                to_string(cust_list.cust_name) + "|" +\
                to_string(cust_list.gesamtumsatz) + "|" +\
                to_string(cust_list.logiernachte) + "|" +\
                to_string(cust_list.argtumsatz) + "|" +\
                to_string(cust_list.f_b_umsatz) + "|" +\
                to_string(cust_list.sonst_umsatz) + "|" +\
                to_string(cust_list.wohnort) + "|" +\
                to_string(cust_list.plz) + "|" +\
                to_string(cust_list.land) + "|" +\
                sales_id_str + "|" +\
                to_string(cust_list.ba_umsatz) + "|" +\
                to_string(cust_list.ly_rev) + "|" +\
                to_string(cust_list.region) + "|" +\
                to_string(cust_list.region1) + "|" +\
                to_string(cust_list.stayno) + "|" +\
                to_string("0") + "|" +\
                to_string(cust_list.counter) + "|" +\
                to_string(cust_list.counterall) + "|" +\
                resno_str + "|" +\
                reslinnr_str + "|" +\
                to_string(cust_list.curr_pos)

        
    db_session.commit()
    
    # Process Selesai, simpan end flag
    bqueasy = get_cache (Queasy, {"key": [(eq, 285)],"char1": [(eq, "Guest Turnover")],"char2": [(eq, idflag)]})
    if bqueasy:
        bqueasy.number1 = 0

    db_session.commit()
    return generate_output()