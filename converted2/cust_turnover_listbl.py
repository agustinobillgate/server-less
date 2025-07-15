#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.cust_turnover_2bl import cust_turnover_2bl

def cust_turnover_listbl(cardtype:int, sort_type:int, curr_sort1:int, fdate:date, tdate:date, check_ftd:bool, currency:string, excl_other:bool, curr_sort2:int):
    sort1 = 0
    cust_list_data = []
    t_lyrev:Decimal = to_decimal("0.0")
    t_gesamtumsatz:Decimal = to_decimal("0.0")
    t_logiernachte:int = 0
    t_argtumsatz:Decimal = to_decimal("0.0")
    t_f_b_umsatz:Decimal = to_decimal("0.0")
    t_sonst_umsatz:Decimal = to_decimal("0.0")
    t_ba_umsatz:Decimal = to_decimal("0.0")
    t_stayno:int = 0
    tr_lyrev:Decimal = to_decimal("0.0")
    tr_gesamtumsatz:Decimal = to_decimal("0.0")
    tr_logiernachte:int = 0
    tr_argtumsatz:Decimal = to_decimal("0.0")
    tr_f_b_umsatz:Decimal = to_decimal("0.0")
    tr_sonst_umsatz:Decimal = to_decimal("0.0")
    tr_ba_umsatz:Decimal = to_decimal("0.0")
    tr_stayno:int = 0
    counter:int = 0
    curr_region:string = ""

    cust_list = cust_list1 = None

    cust_list_data, Cust_list = create_model("Cust_list", {"gastnr":int, "cust_name":string, "gesamtumsatz":Decimal, "logiernachte":int, "argtumsatz":Decimal, "f_b_umsatz":Decimal, "sonst_umsatz":Decimal, "wohnort":string, "plz":string, "land":string, "sales_id":string, "ba_umsatz":Decimal, "ly_rev":Decimal, "region":string, "region1":string, "stayno":int, "resnr":string, "counter":int, "counterall":int, "resno":int, "reslinnr":int, "curr_pos":int})
    cust_list1_data, Cust_list1 = create_model("Cust_list1", {"gastnr":int, "cust_name":string, "gesamtumsatz":Decimal, "logiernachte":int, "argtumsatz":Decimal, "f_b_umsatz":Decimal, "sonst_umsatz":Decimal, "wohnort":string, "plz":string, "land":string, "sales_id":string, "ba_umsatz":Decimal, "ly_rev":Decimal, "region":string, "region1":string, "stayno":int, "resnr":string, "counter":int, "counterall":int, "resno":int, "reslinnr":int, "curr_pos":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal sort1, cust_list_data, t_lyrev, t_gesamtumsatz, t_logiernachte, t_argtumsatz, t_f_b_umsatz, t_sonst_umsatz, t_ba_umsatz, t_stayno, tr_lyrev, tr_gesamtumsatz, tr_logiernachte, tr_argtumsatz, tr_f_b_umsatz, tr_sonst_umsatz, tr_ba_umsatz, tr_stayno, counter, curr_region
        nonlocal cardtype, sort_type, curr_sort1, fdate, tdate, check_ftd, currency, excl_other, curr_sort2


        nonlocal cust_list, cust_list1
        nonlocal cust_list_data, cust_list1_data

        return {"curr_sort2": curr_sort2, "sort1": sort1, "cust-list": cust_list_data}

    cust_list_data.clear()
    curr_sort2, cust_list1_data = get_output(cust_turnover_2bl(cardtype, sort_type, curr_sort1, fdate, tdate, check_ftd, currency, excl_other, curr_sort2))

    for cust_list1 in query(cust_list1_data, sort_by=[("curr_pos",False),("region",False)]):
        counter = counter + 1

        if cust_list1.resnr != "":
            cust_list1.stayno = num_entries(cust_list1.resnr, ";") - 1
        t_lyrev =  to_decimal(t_lyrev) + to_decimal(cust_list1.ly_rev)
        t_gesamtumsatz =  to_decimal(t_gesamtumsatz) + to_decimal(cust_list1.gesamtumsatz)
        t_logiernachte = t_logiernachte + cust_list1.logiernachte
        t_argtumsatz =  to_decimal(t_argtumsatz) + to_decimal(cust_list1.argtumsatz)
        t_f_b_umsatz =  to_decimal(t_f_b_umsatz) + to_decimal(cust_list1.f_b_umsatz)
        t_sonst_umsatz =  to_decimal(t_sonst_umsatz) + to_decimal(cust_list1.sonst_umsatz)
        t_ba_umsatz =  to_decimal(t_ba_umsatz) + to_decimal(cust_list1.ba_umsatz)
        t_stayno = t_stayno + cust_list1.stayno

        if counter == 1:
            curr_region = cust_list1.region
            cust_list1.region1 = curr_region

        if curr_region != cust_list1.region:
            cust_list1.region1 = cust_list1.region
            cust_list = Cust_list()
            cust_list_data.append(cust_list)

            cust_list.cust_name = "T O T A L"
            cust_list.ly_rev =  to_decimal(tr_lyrev)
            cust_list.gesamtumsatz =  to_decimal(tr_gesamtumsatz)
            cust_list.logiernachte = tr_logiernachte
            cust_list.argtumsatz =  to_decimal(tr_argtumsatz)
            cust_list.f_b_umsatz =  to_decimal(tr_f_b_umsatz)
            cust_list.sonst_umsatz =  to_decimal(tr_sonst_umsatz)
            cust_list.ba_umsatz =  to_decimal(tr_ba_umsatz)
            cust_list.stayno = tr_stayno
            cust_list.region = "zzr"
            cust_list.counter = counter
            tr_lyrev =  to_decimal(cust_list1.ly_rev)
            tr_gesamtumsatz =  to_decimal(cust_list1.gesamtumsatz)
            tr_logiernachte = cust_list1.logiernachte
            tr_argtumsatz =  to_decimal(cust_list1.argtumsatz)
            tr_f_b_umsatz =  to_decimal(cust_list1.f_b_umsatz)
            tr_sonst_umsatz =  to_decimal(cust_list1.sonst_umsatz)
            tr_ba_umsatz =  to_decimal(cust_list1.ba_umsatz)
            tr_stayno = cust_list1.stayno
            counter = counter + 1
            curr_region = cust_list1.region


        else:
            tr_lyrev =  to_decimal(tr_lyrev) + to_decimal(cust_list1.ly_rev)
            tr_gesamtumsatz =  to_decimal(tr_gesamtumsatz) + to_decimal(cust_list1.gesamtumsatz)
            tr_logiernachte = tr_logiernachte + cust_list1.logiernachte
            tr_argtumsatz =  to_decimal(tr_argtumsatz) + to_decimal(cust_list1.argtumsatz)
            tr_f_b_umsatz =  to_decimal(tr_f_b_umsatz) + to_decimal(cust_list1.f_b_umsatz)
            tr_sonst_umsatz =  to_decimal(tr_sonst_umsatz) + to_decimal(cust_list1.sonst_umsatz)
            tr_ba_umsatz =  to_decimal(tr_ba_umsatz) + to_decimal(cust_list1.ba_umsatz)
            tr_stayno = tr_stayno + cust_list1.stayno


        cust_list = Cust_list()
        cust_list_data.append(cust_list)

        buffer_copy(cust_list1, cust_list)
        cust_list.counter = counter
    counter = counter + 1
    cust_list = Cust_list()
    cust_list_data.append(cust_list)

    cust_list.cust_name = "T O T A L"
    cust_list.ly_rev =  to_decimal(tr_lyrev)
    cust_list.gesamtumsatz =  to_decimal(tr_gesamtumsatz)
    cust_list.logiernachte = tr_logiernachte
    cust_list.argtumsatz =  to_decimal(tr_argtumsatz)
    cust_list.f_b_umsatz =  to_decimal(tr_f_b_umsatz)
    cust_list.sonst_umsatz =  to_decimal(tr_sonst_umsatz)
    cust_list.ba_umsatz =  to_decimal(tr_ba_umsatz)
    cust_list.stayno = tr_stayno
    cust_list.region = "zzr"
    cust_list.counter = counter


    counter = counter + 1
    cust_list = Cust_list()
    cust_list_data.append(cust_list)

    cust_list.cust_name = "T O T A L"
    cust_list.ly_rev =  to_decimal(t_lyrev)
    cust_list.gesamtumsatz =  to_decimal(t_gesamtumsatz)
    cust_list.logiernachte = t_logiernachte
    cust_list.argtumsatz =  to_decimal(t_argtumsatz)
    cust_list.f_b_umsatz =  to_decimal(t_f_b_umsatz)
    cust_list.sonst_umsatz =  to_decimal(t_sonst_umsatz)
    cust_list.ba_umsatz =  to_decimal(t_ba_umsatz)
    cust_list.stayno = t_stayno
    cust_list.region = "zz"
    cust_list.counter = counter
    cust_list.counterall = 1


    sort1 = sort_type
    curr_region = ""

    return generate_output()