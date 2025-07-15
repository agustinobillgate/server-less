#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Htparam, Waehrung, Genstat, Segment

room_list_data, Room_list = create_model("Room_list", {"wd":int, "datum":date, "bezeich":string, "room":[Decimal,17], "coom":[string,17], "k_pax":int, "t_pax":int, "lodg":[Decimal,7], "avrglodg":Decimal, "avrglodg2":Decimal, "avrgrmrev":Decimal, "avrgrmrev2":Decimal, "others":[Decimal,8], "ly_fcast":string, "ly_actual":string, "ly_avlodge":string, "room_exccomp":int, "room_comp":int, "fixleist":Decimal, "fixleist2":Decimal, "rmrate":Decimal, "rmrate2":Decimal, "revpar":Decimal, "revpar2":Decimal})
segm_list_data, Segm_list = create_model("Segm_list", {"selected":bool, "segm":int, "bezeich":string})
argt_list_data, Argt_list = create_model("Argt_list", {"selected":bool, "argtnr":int, "argt":string, "bezeich":string})
zikat_list_data, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "bezeich":string})

def cr_occfcast1_2lybl(curr_from_date:date, curr_to_date:date, all_segm:bool, all_argt:bool, all_zikat:bool, excl_compl:bool, room_list_data:[Room_list], segm_list_data:[Segm_list], argt_list_data:[Argt_list], zikat_list_data:[Zikat_list]):

    prepare_cache ([Htparam, Waehrung, Genstat])

    date_1:date = None
    date_2:date = None
    curr_ci_date:date = None
    ci_date:date = None
    from_date:date = None
    to_date:date = None
    exchg_rate:Decimal = to_decimal("0.0")
    tot_fcast:Decimal = to_decimal("0.0")
    tot_actual:Decimal = to_decimal("0.0")
    tot_logis:Decimal = to_decimal("0.0")
    num_year:int = 0
    num_year_curr_from_date:int = 0
    num_year_curr_to_date:int = 0
    htparam = waehrung = genstat = segment = None

    room_list = segm_list = argt_list = zikat_list = s_list = None

    s_list_data, S_list = create_model("S_list", {"datum":date, "ly_fcast":int, "ly_actual":int, "ly_logis":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal date_1, date_2, curr_ci_date, ci_date, from_date, to_date, exchg_rate, tot_fcast, tot_actual, tot_logis, num_year, num_year_curr_from_date, num_year_curr_to_date, htparam, waehrung, genstat, segment
        nonlocal curr_from_date, curr_to_date, all_segm, all_argt, all_zikat, excl_compl


        nonlocal room_list, segm_list, argt_list, zikat_list, s_list
        nonlocal s_list_data

        return {"room-list": room_list_data}

    def calculate_2():

        nonlocal date_1, date_2, curr_ci_date, ci_date, from_date, to_date, exchg_rate, tot_fcast, tot_actual, tot_logis, num_year, num_year_curr_from_date, num_year_curr_to_date, htparam, waehrung, genstat, segment
        nonlocal curr_from_date, curr_to_date, all_segm, all_argt, all_zikat, excl_compl


        nonlocal room_list, segm_list, argt_list, zikat_list, s_list
        nonlocal s_list_data

        do_it:bool = False
        rmsharer:bool = False
        datum1:date = None
        num_datum:int = 0
        s_list_data.clear()

        for genstat in db_session.query(Genstat).filter(
                 (Genstat.datum >= date_1) & (Genstat.datum <= date_2) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
            rmsharer = (genstat.resstatus == 13)
            do_it = not rmsharer

            if do_it:

                if genstat.res_date[0] < genstat.datum and genstat.res_date[1] == genstat.datum and genstat.resstatus == 8:
                    do_it = False

            segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

            if do_it and excl_compl:

                if segment and (segment.betriebsnr == 1 or segment.betriebsnr == 2):
                    do_it = False
                else:

                    if genstat.zipreis == 0 and genstat.gratis != 0 and genstat.resstatus == 6 and genstat.res_logic[1] :
                        do_it = False

            if do_it:
                do_it = None != segment and segment.vip_level == 0

            if do_it and not all_segm:

                segm_list = query(segm_list_data, filters=(lambda segm_list: segm_list.segm == genstat.segmentcode and segm_list.selected), first=True)

                if segm_list:
                    do_it = True

            if do_it and not all_argt:

                argt_list = query(argt_list_data, filters=(lambda argt_list: argt_list.argt == genstat.argt and argt_list.selected), first=True)

                if argt_list:
                    do_it = True

            if do_it and not all_zikat:

                zikat_list = query(zikat_list_data, filters=(lambda zikat_list: zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected), first=True)

                if zikat_list:
                    do_it = True

            if do_it:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.datum == genstat.datum), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.datum = genstat.datum


                s_list.ly_fcast = s_list.ly_fcast + 1
                s_list.ly_actual = s_list.ly_actual + 1
                s_list.ly_logis =  to_decimal(s_list.ly_logis) + to_decimal(genstat.logis)

        for s_list in query(s_list_data):
            datum1 = s_list.datum
            num_datum = get_year(datum1) + 1
            datum1 = date_mdy(get_month(datum1) , get_day(datum1) , num_datum)

            room_list = query(room_list_data, filters=(lambda room_list: room_list.datum == datum1), first=True)

            if room_list:
                tot_logis =  to_decimal(tot_logis) + to_decimal(s_list.ly_logis)
                s_list.ly_logis =  to_decimal(s_list.ly_logis) / to_decimal(s_list.ly_actual)
                room_list.ly_fcast = to_string(s_list.ly_fcast, ">>>>>>9")
                room_list.ly_actual = to_string(s_list.ly_actual, ">>>>>>9")
                room_list.ly_avlodge = to_string(s_list.ly_logis, "->,>>>,>>9.99")
                tot_fcast =  to_decimal(tot_fcast) + to_decimal(s_list.ly_fcast)
                tot_actual =  to_decimal(tot_actual) + to_decimal(s_list.ly_actual)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if waehrung:
        exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
    else:
        exchg_rate =  to_decimal("1")
    curr_ci_date = get_output(htpdate(87))
    num_year = get_year(curr_ci_date) - 1
    num_year_curr_from_date = get_year(curr_from_date) - 1
    num_year_curr_to_date = get_year(curr_to_date) - 1
    ci_date = date_mdy(2, 28, num_year)
    from_date = ci_date
    to_date = ci_date


    ci_date = date_mdy(get_month(curr_ci_date) , get_day(curr_ci_date) , num_year)


    from_date = date_mdy(get_month(curr_from_date) , get_day(curr_from_date) , num_year_curr_from_date)


    to_date = date_mdy(get_month(curr_to_date) , get_day(curr_to_date) , num_year_curr_to_date)


    date_1 = from_date
    date_2 = to_date


    calculate_2()

    room_list = query(room_list_data, filters=(lambda room_list: room_list.wd == 0), first=True)
    room_list.ly_fcast = to_string(tot_fcast, ">>>>>>9")
    room_list.ly_actual = to_string(tot_actual, ">>>>>>9")
    room_list.ly_avlodge = to_string(tot_logis / tot_actual, "->,>>>,>>9.99")

    return generate_output()