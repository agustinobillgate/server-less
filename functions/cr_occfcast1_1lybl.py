#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Htparam, Waehrung, Genstat, Segment, Res_line

room_list_data, Room_list = create_model("Room_list", {"wd":int, "datum":date, "bezeich":string, "room":[Decimal,17], "coom":[string,17], "k_pax":int, "t_pax":int, "lodg":[Decimal,7], "avrglodg":Decimal, "avrglodg2":Decimal, "avrgrmrev":Decimal, "avrgrmrev2":Decimal, "others":[Decimal,8], "ly_fcast":string, "ly_actual":string, "ly_avlodge":string, "room_exccomp":int, "room_comp":int, "fixleist":Decimal, "fixleist2":Decimal, "rmrate":Decimal, "rmrate2":Decimal, "revpar":Decimal, "revpar2":Decimal})
segm_list_data, Segm_list = create_model("Segm_list", {"selected":bool, "segm":int, "bezeich":string})
argt_list_data, Argt_list = create_model("Argt_list", {"selected":bool, "argtnr":int, "argt":string, "bezeich":string})
zikat_list_data, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "bezeich":string})

def cr_occfcast1_1lybl(curr_from_date:date, curr_to_date:date, all_segm:bool, all_argt:bool, all_zikat:bool, room_list_data:[Room_list], segm_list_data:[Segm_list], argt_list_data:[Argt_list], zikat_list_data:[Zikat_list]):

    prepare_cache ([Htparam, Waehrung, Genstat, Res_line])

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
    htparam = waehrung = genstat = segment = res_line = None

    room_list = segm_list = argt_list = zikat_list = s_list = None

    s_list_data, S_list = create_model("S_list", {"datum":date, "ly_fcast":int, "ly_actual":int, "ly_logis":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal date_1, date_2, curr_ci_date, ci_date, from_date, to_date, exchg_rate, tot_fcast, tot_actual, tot_logis, htparam, waehrung, genstat, segment, res_line
        nonlocal curr_from_date, curr_to_date, all_segm, all_argt, all_zikat


        nonlocal room_list, segm_list, argt_list, zikat_list, s_list
        nonlocal s_list_data

        return {"room-list": room_list_data}

    def calculate_1():

        nonlocal date_1, date_2, curr_ci_date, ci_date, from_date, to_date, exchg_rate, tot_fcast, tot_actual, tot_logis, htparam, waehrung, genstat, segment, res_line
        nonlocal curr_from_date, curr_to_date, all_segm, all_argt, all_zikat


        nonlocal room_list, segm_list, argt_list, zikat_list, s_list
        nonlocal s_list_data

        do_it:bool = False
        rmsharer:bool = False
        datum1:date = None

        for genstat in db_session.query(Genstat).filter(
                 (Genstat.datum >= date_1) & (Genstat.datum <= date_2) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
            rmsharer = (genstat.resstatus == 13)
            do_it = not rmsharer

            if do_it:

                if genstat.res_date[0] < genstat.datum and genstat.res_date[1] == genstat.datum and genstat.resstatus == 8:
                    do_it = False

            if do_it:

                segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})
                do_it = None != segment and segment.vip_level == 0

            if do_it and not all_segm:

                segm_list = query(segm_list_data, filters=(lambda segm_list: segm_list.segm == genstat.segmentcode and segm_list.selected), first=True)
                do_it = None != segm_list

            if do_it and not all_argt:

                argt_list = query(argt_list_data, filters=(lambda argt_list: argt_list.argt == genstat.argt and argt_list.selected), first=True)
                do_it = None != argt_list

            if do_it and not all_zikat:

                zikat_list = query(zikat_list_data, filters=(lambda zikat_list: zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected), first=True)
                do_it = None != zikat_list

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
            datum1 = date_mdy(get_month(datum1) , get_day(datum1) , get_year(datum1) + timedelta(days=1))

            room_list = query(room_list_data, filters=(lambda room_list: room_list.datum == datum1), first=True)

            if room_list:
                tot_logis =  to_decimal(tot_logis) + to_decimal(s_list.ly_logis)
                s_list.ly_logis =  to_decimal(s_list.ly_logis) / to_decimal(s_list.ly_actual)
                room_list.ly_fcast = to_string(s_list.ly_fcast, ">>>>>>9")
                room_list.ly_actual = to_string(s_list.ly_actual, ">>>>>>9")
                room_list.ly_avlodge = to_string(s_list.ly_logis, "->,>>>,>>9.99")
                tot_fcast =  to_decimal(tot_fcast) + to_decimal(s_list.ly_fcast)
                tot_actual =  to_decimal(tot_actual) + to_decimal(s_list.ly_actual)


    def calculate_2():

        nonlocal date_1, date_2, curr_ci_date, ci_date, from_date, to_date, exchg_rate, tot_fcast, tot_actual, tot_logis, htparam, waehrung, genstat, segment, res_line
        nonlocal curr_from_date, curr_to_date, all_segm, all_argt, all_zikat


        nonlocal room_list, segm_list, argt_list, zikat_list, s_list
        nonlocal s_list_data

        do_it:bool = False
        rmsharer:bool = False
        datum1:date = None
        s_list_data.clear()

        for genstat in db_session.query(Genstat).filter(
                 (Genstat.datum >= date_1) & (Genstat.datum <= date_2) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
            rmsharer = (genstat.resstatus == 13)
            do_it = not rmsharer

            if do_it:

                if genstat.res_date[0] < genstat.datum and genstat.res_date[1] == genstat.datum and genstat.resstatus == 8:
                    do_it = False

            if do_it:

                segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})
                do_it = None != segment and segment.vip_level == 0

            if do_it:

                segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})
                do_it = None != segment and segment.vip_level == 0

            if do_it and not all_segm:

                segm_list = query(segm_list_data, filters=(lambda segm_list: segm_list.segm == genstat.segmentcode and segm_list.selected), first=True)
                do_it = None != segm_list

            if do_it and not all_argt:

                argt_list = query(argt_list_data, filters=(lambda argt_list: argt_list.argt == genstat.argt and argt_list.selected), first=True)
                do_it = None != argt_list

            if do_it and not all_zikat:

                zikat_list = query(zikat_list_data, filters=(lambda zikat_list: zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected), first=True)
                do_it = None != zikat_list

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
            datum1 = date_mdy(get_month(datum1) , get_day(datum1) , get_year(datum1) + timedelta(days=1))

            room_list = query(room_list_data, filters=(lambda room_list: room_list.datum == datum1), first=True)

            if room_list:
                tot_logis =  to_decimal(tot_logis) + to_decimal(s_list.ly_logis)
                s_list.ly_logis =  to_decimal(s_list.ly_logis) / to_decimal(s_list.ly_actual)
                room_list.ly_fcast = to_string(s_list.ly_fcast, ">>>>>>9")
                room_list.ly_actual = to_string(s_list.ly_actual, ">>>>>>9")
                room_list.ly_avlodge = to_string(s_list.ly_logis, "->,>>>,>>9.99")
                tot_fcast =  to_decimal(tot_fcast) + to_decimal(s_list.ly_fcast)
                tot_actual =  to_decimal(tot_actual) + to_decimal(s_list.ly_actual)


    def calculate_3():

        nonlocal date_1, date_2, curr_ci_date, ci_date, from_date, to_date, exchg_rate, tot_fcast, tot_actual, tot_logis, htparam, waehrung, genstat, segment, res_line
        nonlocal curr_from_date, curr_to_date, all_segm, all_argt, all_zikat


        nonlocal room_list, segm_list, argt_list, zikat_list, s_list
        nonlocal s_list_data

        curr_date:date = None
        do_it:bool = False
        datum3:date = None
        datum1:date = None
        datum2:date = None
        s_list_data.clear()

        res_line_obj_list = {}
        res_line = Res_line()
        waehrung = Waehrung()
        for res_line.ankunft, res_line.abreise, res_line.resstatus, res_line.zimmerfix, res_line.zimmeranz, res_line._recid, waehrung.ankauf, waehrung.einheit, waehrung._recid in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.resstatus, Res_line.zimmerfix, Res_line.zimmeranz, Res_line._recid, Waehrung.ankauf, Waehrung.einheit, Waehrung._recid).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).filter(
                 ((Res_line.active_flag == 2) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (not_ (Res_line.ankunft > date_2)) & (not_ (Res_line.abreise < date_1))) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.gastnr, Res_line.resnr).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            do_it = True

            if do_it:

                segment = get_cache (Segment, {"segmentcode": [(eq, genfcast.segmentcode)]})
                do_it = None != segment and segment.vip_level == 0

            if do_it and not all_segm:

                segm_list = query(segm_list_data, filters=(lambda segm_list: segm_list.segm == genfcast.segmentcode and segm_list.selected), first=True)
                do_it = None != segm_list

            if do_it and not all_argt:

                argt_list = query(argt_list_data, filters=(lambda argt_list: argt_list.argt == genfcast.argt and argt_list.selected), first=True)
                do_it = None != argt_list

            if do_it and not all_zikat:

                zikat_list = query(zikat_list_data, filters=(lambda zikat_list: zikat_list.zikatnr == genfcast.zikatnr and zikat_list.selected), first=True)
                do_it = None != zikat_list
            datum1 = date_1

            if res_line.ankunft > datum1:
                datum1 = res_line.ankunft
            datum2 = date_2

            if res_line.abreise < datum2:
                datum2 = res_line.abreise
            for curr_date in date_range(datum1,datum2) :

                if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:

                    s_list = query(s_list_data, filters=(lambda s_list: s_list.datum == curr_date), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_data.append(s_list)

                        s_list.datum = curr_date


                    s_list.ly_fcast = s_list.ly_fcast + res_line.zimmeranz

        for s_list in query(s_list_data):
            datum3 = s_list.datum
            datum3 = date_mdy(get_month(datum3) , get_day(datum3) , get_year(datum3) + timedelta(days=1))

            room_list = query(room_list_data, filters=(lambda room_list: room_list.datum == datum3), first=True)

            if room_list:
                room_list.ly_fcast = to_string(s_list.ly_fcast, ">>>>>>9")
                tot_fcast =  to_decimal(tot_fcast) + to_decimal(s_list.ly_fcast)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if waehrung:
        exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
    else:
        exchg_rate =  to_decimal("1")
    curr_ci_date = get_output(htpdate(87))
    ci_date = date_mdy(2, 28, get_year(curr_ci_date) - timedelta(days=1))
    from_date = ci_date
    to_date = ci_date


    ci_date = date_mdy(get_month(curr_ci_date) , get_day(curr_ci_date) , YEAR (curr_ci_date) - timedelta(days=1))


    from_date = date_mdy(get_month(curr_from_date) , get_day(curr_from_date) , YEAR (curr_from_date) - timedelta(days=1))


    to_date = date_mdy(get_month(curr_to_date) , get_day(curr_to_date) , YEAR (curr_to_date) - timedelta(days=1))


    date_1 = from_date
    date_2 = to_date


    calculate_2()

    room_list = query(room_list_data, filters=(lambda room_list: room_list.wd == 0), first=True)
    room_list.ly_fcast = to_string(tot_fcast, ">>>>>>9")
    room_list.ly_actual = to_string(tot_actual, ">>>>>>9")
    room_list.ly_avlodge = to_string(tot_logis / tot_actual, "->,>>>,>>9.99")

    return generate_output()