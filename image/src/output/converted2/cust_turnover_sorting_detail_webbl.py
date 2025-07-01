#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.cust_turnover_sorting_detail_cldbl import cust_turnover_sorting_detail_cldbl
from models import Queasy

def cust_turnover_sorting_detail_webbl(cardtype:int, sort_type:int, fdate:date, tdate:date, check_ftd:bool, currency:string, excl_other:bool, curr_sort2:int, idflag:string):

    prepare_cache ([Queasy])

    arrive_date:string = ""
    depart_date:string = ""
    counter:int = 0
    queasy = None

    b_list = bqueasy = pqueasy = None

    b_list_list, B_list = create_model("B_list", {"gastnr":int, "cust_name":string, "gname":string, "gesamtumsatz":string, "logiernachte":string, "argtumsatz":string, "f_b_umsatz":string, "sonst_umsatz":string, "wohnort":string, "plz":string, "land":string, "sales_id":string, "ba_umsatz":string, "ly_rev":string, "region":string, "region1":string, "stayno":string, "resnr":string, "counter":int, "counterall":int, "resno":int, "reslinnr":int, "curr_pos":int, "count_room":string, "rm_sharer":string, "arrival":date, "depart":date, "gastnrmember":int})

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Pqueasy = create_buffer("Pqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal arrive_date, depart_date, counter, queasy
        nonlocal cardtype, sort_type, fdate, tdate, check_ftd, currency, excl_other, curr_sort2, idflag
        nonlocal bqueasy, pqueasy


        nonlocal b_list, bqueasy, pqueasy
        nonlocal b_list_list

        return {}


    queasy = Queasy()
    db_session.add(queasy)

    queasy.key = 285
    queasy.char1 = "Guest Turnover Detail"
    queasy.number1 = 1
    queasy.char2 = idflag


    pass
    curr_sort2, b_list_list = get_output(cust_turnover_sorting_detail_cldbl(cardtype, sort_type, fdate, tdate, check_ftd, currency, excl_other, curr_sort2))

    for b_list in query(b_list_list):
        pqueasy = Queasy()
        db_session.add(pqueasy)

        counter = counter + 1
        pqueasy.key = 280
        pqueasy.char1 = "Guest Turnover Detail"
        pqueasy.char3 = idflag
        pqueasy.number1 = counter

        if b_list.arrival == None:
            arrive_date = ""


        else:
            arrive_date = to_string(b_list.arrival)

        if b_list.depart == None:
            depart_date = ""


        else:
            depart_date = to_string(b_list.depart)

        if b_list.gastnr == None:
            pqueasy.char2 = to_string(" ") + "|" +\
                    to_string(b_list.cust_name) + "|" +\
                    to_string(b_list.gesamtumsatz) + "|" +\
                    to_string(b_list.logiernachte) + "|" +\
                    to_string(b_list.argtumsatz) + "|" +\
                    to_string(b_list.f_b_umsatz) + "|" +\
                    to_string(b_list.sonst_umsatz) + "|" +\
                    to_string(b_list.wohnort) + "|" +\
                    to_string(b_list.plz) + "|" +\
                    to_string(b_list.land) + "|" +\
                    to_string(b_list.sales_id) + "|" +\
                    to_string(b_list.ba_umsatz) + "|" +\
                    to_string(b_list.ly_rev) + "|" +\
                    to_string(b_list.region) + "|" +\
                    to_string(b_list.region1) + "|" +\
                    to_string(b_list.stayno) + "|" +\
                    to_string("0") + "|" +\
                    to_string(b_list.counter) + "|" +\
                    to_string(b_list.counterall) + "|" +\
                    to_string(b_list.resno) + "|" +\
                    to_string(b_list.reslinnr) + "|" +\
                    to_string(b_list.curr_pos) + "|" +\
                    to_string(b_list.count_room) + "|" +\
                    to_string(b_list.rm_sharer) + "|" +\
                    to_string(arrive_date) + "|" +\
                    to_string(depart_date)

        elif b_list.gastnr == None and b_list.cust_name == " ":
            pqueasy.char2 = to_string(" ") + "|" +\
                    to_string("") + "|" +\
                    to_string("") + "|" +\
                    to_string("") + "|" +\
                    to_string("") + "|" +\
                    to_string("") + "|" +\
                    to_string("") + "|" +\
                    to_string("") + "|" +\
                    to_string("") + "|" +\
                    to_string("") + "|" +\
                    to_string("") + "|" +\
                    to_string("") + "|" +\
                    to_string("") + "|" +\
                    to_string("") + "|" +\
                    to_string("") + "|" +\
                    to_string("") + "|" +\
                    to_string("") + "|" +\
                    to_string("") + "|" +\
                    to_string("") + "|" +\
                    to_string("") + "|" +\
                    to_string("") + "|" +\
                    to_string("") + "|" +\
                    to_string("") + "|" +\
                    to_string("") + "|" +\
                    to_string("") + "|" +\
                    to_string("")


        else:
            pqueasy.char2 = to_string(b_list.gastnr) + "|" +\
                    to_string(b_list.cust_name) + "|" +\
                    to_string(b_list.gesamtumsatz) + "|" +\
                    to_string(b_list.logiernachte) + "|" +\
                    to_string(b_list.argtumsatz) + "|" +\
                    to_string(b_list.f_b_umsatz) + "|" +\
                    to_string(b_list.sonst_umsatz) + "|" +\
                    to_string(b_list.wohnort) + "|" +\
                    to_string(b_list.plz) + "|" +\
                    to_string(b_list.land) + "|" +\
                    to_string(b_list.sales_id) + "|" +\
                    to_string(b_list.ba_umsatz) + "|" +\
                    to_string(b_list.ly_rev) + "|" +\
                    to_string(b_list.region) + "|" +\
                    to_string(b_list.region1) + "|" +\
                    to_string(b_list.stayno) + "|" +\
                    to_string("0") + "|" +\
                    to_string(b_list.counter) + "|" +\
                    to_string(b_list.counterall) + "|" +\
                    to_string(b_list.resno) + "|" +\
                    to_string(b_list.reslinnr) + "|" +\
                    to_string(b_list.curr_pos) + "|" +\
                    to_string(b_list.count_room) + "|" +\
                    to_string(b_list.rm_sharer) + "|" +\
                    to_string(arrive_date) + "|" +\
                    to_string(depart_date)


        pass

    bqueasy = get_cache (Queasy, {"key": [(eq, 285)],"char1": [(eq, "guest turnover detail")],"char2": [(eq, idflag)]})

    if bqueasy:
        pass
        bqueasy.number1 = 0


        pass
        pass

    return generate_output()