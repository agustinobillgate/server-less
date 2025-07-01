#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.create_forecast_history_detail_cldbl import create_forecast_history_detail_cldbl
from models import Sourccod

def cr_fproduct_showdetail_webbl(v_key:string, v_value:string, cardtype:int, stattype:int, fr_date:date, to_date:date, excl_comp:bool, vhp_limited:bool, scin:bool):

    prepare_cache ([Sourccod])

    fcasthist_detail_list_list = []
    query_string:string = ""
    sob_number:int = 0
    tot_room:int = 0
    tot_pax:int = 0
    tot_rev:Decimal = to_decimal("0.0")
    tot_expectrev:Decimal = to_decimal("0.0")
    tot_rmrev:Decimal = to_decimal("0.0")
    tot_bfast:Decimal = to_decimal("0.0")
    tot_lunch:Decimal = to_decimal("0.0")
    tot_dinner:Decimal = to_decimal("0.0")
    tot_othrev:Decimal = to_decimal("0.0")
    tot_fix_cost:Decimal = to_decimal("0.0")
    sourccod = None

    fcasthist_detail_list = t_list = None

    fcasthist_detail_list_list, Fcasthist_detail_list = create_model("Fcasthist_detail_list", {"flag":int, "res_number":string, "display_value":string, "avrg_roomrev":string, "reserve_name":string, "guest_name":string, "pax":int, "room":int, "expected_revenue":string, "currency":string, "total_revenue":string, "room_revenue":string, "bfast_amount":string, "lunch_amount":string, "dinneramount":string, "other_revenue":string, "fix_cost":string})
    t_list_list, T_list = create_model("T_list", {"resnr":int, "reslinnr":int, "logis_guaranteed":Decimal, "bfast_guaranteed":Decimal, "lunch_guaranteed":Decimal, "dinner_guaranteed":Decimal, "misc_guaranteed":Decimal, "pax_guaranteed":int, "room_guaranteed":int, "logis_tentative":Decimal, "bfast_tentative":Decimal, "lunch_tentative":Decimal, "dinner_tentative":Decimal, "misc_tentative":Decimal, "pax_tentative":int, "room_tentative":int, "rsv_karteityp":int, "rsv_name":string, "rsv_nationnr":int, "guest_karteityp":int, "guest_name":string, "guest_nationnr":int, "sob":int, "resstatus":int, "currency":string, "zipreis":Decimal, "flag_history":bool, "firmen_nr":int, "steuernr":string, "segmentcode":int, "segmentbez":string, "fcost":Decimal, "argtcode":string, "argtbez":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fcasthist_detail_list_list, query_string, sob_number, tot_room, tot_pax, tot_rev, tot_expectrev, tot_rmrev, tot_bfast, tot_lunch, tot_dinner, tot_othrev, tot_fix_cost, sourccod
        nonlocal v_key, v_value, cardtype, stattype, fr_date, to_date, excl_comp, vhp_limited, scin


        nonlocal fcasthist_detail_list, t_list
        nonlocal fcasthist_detail_list_list, t_list_list

        return {"fcasthist-detail-list": fcasthist_detail_list_list}

    t_list_list = get_output(create_forecast_history_detail_cldbl(fr_date, to_date, excl_comp, vhp_limited, scin))

    if v_key.lower()  == ("SOB").lower() :

        sourccod = get_cache (Sourccod, {"bezeich": [(eq, v_value)]})

        if sourccod:
            sob_number = sourccod.source_code

        if stattype == 0:
            query_string = "FOR EACH t-list WHERE t-list.sob EQ " + to_string(sob_number) + "NO-LOCK BY t-list.guest-name:"

        elif stattype == 1:
            query_string = "FOR EACH t-list WHERE t-list.sob EQ " + to_string(sob_number) + " AND t-list.resstatus NE 3 NO-LOCK BY t-list.guest-name:"

        elif stattype == 3:
            query_string = "FOR EACH t-list WHERE t-list.sob EQ " + to_string(sob_number) + " AND t-list.resstatus EQ 3 NO-LOCK BY t-list.guest-name:"
        qh:SET_BUFFERS (BUFFER t_list:HANDLE)
        qh:QUERY_PREPARE (query_string)
        qh:QUERY_OPEN
        while True:
            qh:GET_NEXT()

            if not t_list:
                break
            fcasthist_detail_list = Fcasthist_detail_list()
            fcasthist_detail_list_list.append(fcasthist_detail_list)

            fcasthist_detail_list.res_number = to_string(t_list.resnr) + "/" + to_string(t_list.reslinnr)
            fcasthist_detail_list.display_value = v_value
            fcasthist_detail_list.reserve_name = t_list.rsv_name
            fcasthist_detail_list.guest_name = t_list.guest_name
            fcasthist_detail_list.currency = t_list.currency

            if stattype == 0:
                fcasthist_detail_list.pax = t_list.pax_guaranteed + t_list.pax_tentative
                fcasthist_detail_list.room = t_list.room_guaranteed + t_list.room_tentative
                fcasthist_detail_list.expected_revenue = to_string(t_list.zipreis, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist_detail_list.total_revenue = to_string(t_list.logis_guaranteed + t_list.logis_tentative + t_list.bfast_guaranteed + t_list.bfast_tentative +\
                        t_list.lunch_guaranteed + t_list.lunch_tentative + t_list.dinner_guaranteed + t_list.dinner_tentative +\
                        t_list.misc_tentative + t_list.misc_guaranteed, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist_detail_list.room_revenue = to_string(t_list.logis_guaranteed + t_list.logis_tentative, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist_detail_list.bfast_amount = to_string(t_list.bfast_guaranteed + t_list.bfast_tentative, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist_detail_list.lunch_amount = to_string(t_list.lunch_guaranteed + t_list.lunch_tentative, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist_detail_list.dinneramount = to_string(t_list.dinner_guaranteed + t_list.dinner_tentative, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist_detail_list.other_revenue = to_string(t_list.misc_guaranteed + t_list.misc_tentative, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist_detail_list.fix_cost = to_string(t_list.fcost, "->>,>>>,>>>,>>>,>>9.99")


                tot_room = tot_room + t_list.pax_guaranteed + t_list.pax_tentative
                tot_pax = tot_pax + t_list.room_guaranteed + t_list.room_tentative
                tot_rev =  to_decimal(tot_rev) + to_decimal(t_list.zipreis)
                tot_expectrev =  to_decimal(tot_expectrev) + to_decimal(t_list.logis_guaranteed) + to_decimal(t_list.logis_tentative) + to_decimal(t_list.bfast_guaranteed) +\
                        t_list.bfast_tentative + to_decimal(t_list.lunch_guaranteed) + to_decimal(t_list.lunch_tentative) + to_decimal(t_list.dinner_guaranteed) +\
                        t_list.dinner_tentative + to_decimal(t_list.misc_tentative) + to_decimal(t_list.misc_guaranteed)
                tot_rmrev =  to_decimal(tot_rmrev) + to_decimal(t_list.logis_guaranteed) + to_decimal(t_list.logis_tentative)
                tot_bfast =  to_decimal(tot_bfast) + to_decimal(t_list.bfast_guaranteed) + to_decimal(t_list.bfast_tentative)
                tot_lunch =  to_decimal(tot_lunch) + to_decimal(t_list.lunch_guaranteed) + to_decimal(t_list.lunch_tentative)
                tot_dinner =  to_decimal(tot_dinner) + to_decimal(t_list.dinner_guaranteed) + to_decimal(t_list.dinner_tentative)
                tot_othrev =  to_decimal(tot_othrev) + to_decimal(t_list.misc_guaranteed) + to_decimal(t_list.misc_tentative)
                tot_fix_cost =  to_decimal(tot_fix_cost) + to_decimal(t_list.fcost)

            elif stattype == 1:
                fcasthist_detail_list.pax = t_list.pax_guaranteed
                fcasthist_detail_list.room = t_list.room_guaranteed
                fcasthist_detail_list.expected_revenue = to_string(t_list.zipreis, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist_detail_list.total_revenue = to_string(t_list.logis_guaranteed + t_list.bfast_guaranteed + t_list.lunch_guaranteed +\
                        t_list.dinner_guaranteed + t_list.misc_guaranteed, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist_detail_list.room_revenue = to_string(t_list.logis_guaranteed, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist_detail_list.bfast_amount = to_string(t_list.bfast_guaranteed, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist_detail_list.lunch_amount = to_string(t_list.lunch_guaranteed, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist_detail_list.dinneramount = to_string(t_list.dinner_guaranteed, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist_detail_list.other_revenue = to_string(t_list.misc_guaranteed, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist_detail_list.fix_cost = to_string(t_list.fcost, "->>,>>>,>>>,>>>,>>9.99")


                tot_room = tot_room + t_list.pax_guaranteed
                tot_pax = tot_pax + t_list.room_guaranteed
                tot_rev =  to_decimal(tot_rev) + to_decimal(t_list.zipreis)
                tot_expectrev =  to_decimal(tot_expectrev) + to_decimal(t_list.logis_guaranteed) + to_decimal(t_list.bfast_guaranteed) + to_decimal(t_list.lunch_guaranteed) +\
                        t_list.dinner_guaranteed + to_decimal(t_list.misc_guaranteed)
                tot_rmrev =  to_decimal(tot_rmrev) + to_decimal(t_list.logis_guaranteed)
                tot_bfast =  to_decimal(tot_bfast) + to_decimal(t_list.bfast_guaranteed)
                tot_lunch =  to_decimal(tot_lunch) + to_decimal(t_list.lunch_guaranteed)
                tot_dinner =  to_decimal(tot_dinner) + to_decimal(t_list.dinner_guaranteed)
                tot_othrev =  to_decimal(tot_othrev) + to_decimal(t_list.misc_guaranteed)
                tot_fix_cost =  to_decimal(tot_fix_cost) + to_decimal(t_list.fcost)

            elif stattype == 3:
                fcasthist_detail_list.pax = t_list.pax_tentative
                fcasthist_detail_list.room = t_list.room_tentative
                fcasthist_detail_list.expected_revenue = to_string(t_list.zipreis, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist_detail_list.total_revenue = to_string(t_list.logis_tentative + t_list.bfast_tentative + t_list.lunch_tentative +\
                        t_list.dinner_tentative + t_list.misc_tentative, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist_detail_list.room_revenue = to_string(t_list.logis_tentative, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist_detail_list.bfast_amount = to_string(t_list.bfast_tentative, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist_detail_list.lunch_amount = to_string(t_list.lunch_tentative, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist_detail_list.dinneramount = to_string(t_list.dinner_tentative, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist_detail_list.other_revenue = to_string(t_list.misc_tentative, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist_detail_list.fix_cost = to_string(t_list.fcost, "->>,>>>,>>>,>>>,>>9.99")


                tot_room = tot_room + t_list.pax_tentative
                tot_pax = tot_pax + t_list.room_tentative
                tot_rev =  to_decimal(tot_rev) + to_decimal(t_list.zipreis)
                tot_expectrev =  to_decimal(tot_expectrev) + to_decimal(t_list.logis_tentative) + to_decimal(t_list.bfast_tentative) + to_decimal(t_list.lunch_tentative) +\
                        t_list.dinner_tentative + to_decimal(t_list.misc_tentative)
                tot_rmrev =  to_decimal(tot_rmrev) + to_decimal(t_list.logis_tentative)
                tot_bfast =  to_decimal(tot_bfast) + to_decimal(t_list.bfast_tentative)
                tot_lunch =  to_decimal(tot_lunch) + to_decimal(t_list.lunch_tentative)
                tot_dinner =  to_decimal(tot_dinner) + to_decimal(t_list.dinner_tentative)
                tot_othrev =  to_decimal(tot_othrev) + to_decimal(t_list.misc_tentative)
                tot_fix_cost =  to_decimal(tot_fix_cost) + to_decimal(t_list.fcost)


        qh:QUERY_CLOSE()


        fcasthist_detail_list = query(fcasthist_detail_list_list, first=True)

        if fcasthist_detail_list:
            fcasthist_detail_list = Fcasthist_detail_list()
            fcasthist_detail_list_list.append(fcasthist_detail_list)

            fcasthist_detail_list.reserve_name = "T O T A L"
            fcasthist_detail_list.pax = tot_room
            fcasthist_detail_list.room = tot_pax
            fcasthist_detail_list.expected_revenue = to_string(tot_rev , "->>,>>>,>>>,>>>,>>9.99")
            fcasthist_detail_list.total_revenue = to_string(tot_expectrev, "->>,>>>,>>>,>>>,>>9.99")
            fcasthist_detail_list.room_revenue = to_string(tot_rmrev , "->>,>>>,>>>,>>>,>>9.99")
            fcasthist_detail_list.bfast_amount = to_string(tot_bfast , "->>,>>>,>>>,>>>,>>9.99")
            fcasthist_detail_list.lunch_amount = to_string(tot_lunch , "->>,>>>,>>>,>>>,>>9.99")
            fcasthist_detail_list.dinneramount = to_string(tot_dinner , "->>,>>>,>>>,>>>,>>9.99")
            fcasthist_detail_list.other_revenue = to_string(tot_othrev , "->>,>>>,>>>,>>>,>>9.99")
            fcasthist_detail_list.fix_cost = to_string(tot_fix_cost , "->>,>>>,>>>,>>>,>>9.99")

    return generate_output()