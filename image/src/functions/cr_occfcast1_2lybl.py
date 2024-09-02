from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from models import Htparam, Waehrung, Genstat, Segment, Res_line

def cr_occfcast1_2lybl(curr_from_date:date, curr_to_date:date, all_segm:bool, all_argt:bool, all_zikat:bool, excl_compl:bool, room_list:[Room_list], segm_list:[Segm_list], argt_list:[Argt_list], zikat_list:[Zikat_list]):
    date_1:date = None
    date_2:date = None
    curr_ci_date:date = None
    ci_date:date = None
    from_date:date = None
    to_date:date = None
    exchg_rate:decimal = 0
    tot_fcast:decimal = 0
    tot_actual:decimal = 0
    tot_logis:decimal = 0
    htparam = waehrung = genstat = segment = res_line = None

    room_list = segm_list = argt_list = zikat_list = s_list = None

    room_list_list, Room_list = create_model("Room_list", {"wd":int, "datum":date, "bezeich":str, "room":decimal, "coom":[str, 17], "k_pax":int, "t_pax":int, "lodg":[decimal, 7], "avrglodg":decimal, "avrglodg2":decimal, "avrgrmrev":decimal, "avrgrmrev2":decimal, "others":decimal, "ly_fcast":str, "ly_actual":str, "ly_avlodge":str, "room_exccomp":int, "room_comp":int, "fixleist":decimal, "fixleist2":decimal, "rmrate":decimal, "rmrate2":decimal, "revpar":decimal, "revpar2":decimal})
    segm_list_list, Segm_list = create_model("Segm_list", {"selected":bool, "segm":int, "bezeich":str})
    argt_list_list, Argt_list = create_model("Argt_list", {"selected":bool, "argtnr":int, "argt":str, "bezeich":str})
    zikat_list_list, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "bezeich":str})
    s_list_list, S_list = create_model("S_list", {"datum":date, "ly_fcast":int, "ly_actual":int, "ly_logis":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal date_1, date_2, curr_ci_date, ci_date, from_date, to_date, exchg_rate, tot_fcast, tot_actual, tot_logis, htparam, waehrung, genstat, segment, res_line


        nonlocal room_list, segm_list, argt_list, zikat_list, s_list
        nonlocal room_list_list, segm_list_list, argt_list_list, zikat_list_list, s_list_list
        return {}

    def calculate_1():

        nonlocal date_1, date_2, curr_ci_date, ci_date, from_date, to_date, exchg_rate, tot_fcast, tot_actual, tot_logis, htparam, waehrung, genstat, segment, res_line


        nonlocal room_list, segm_list, argt_list, zikat_list, s_list
        nonlocal room_list_list, segm_list_list, argt_list_list, zikat_list_list, s_list_list

        do_it:bool = False
        rmsharer:bool = False
        datum1:date = None

        for genstat in db_session.query(Genstat).filter(
                (Genstat.datum >= date_1) &  (Genstat.datum <= date_2) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
            rmsharer = (genstat.resstatus == 13)
            do_it = not rmsharer

            if do_it:

                if genstat.res_date[0] < genstat.datum and genstat.res_date[1] == genstat.datum and genstat.resstatus == 8:
                    do_it = False

            if do_it:

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == genstat.segmentcode)).first()
                do_it = None != segment and segment.vip_level == 0

            if do_it and not all_segm:

                segm_list = query(segm_list_list, filters=(lambda segm_list :segm_list.segm == genstat.segmentcode and segm_list.selected), first=True)
                do_it = None != segm_list

            if do_it and not all_argt:

                argt_list = query(argt_list_list, filters=(lambda argt_list :argt_list.argt == genstat.argt and argt_list.selected), first=True)
                do_it = None != argt_list

            if do_it and not all_zikat:

                zikat_list = query(zikat_list_list, filters=(lambda zikat_list :zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected), first=True)
                do_it = None != zikat_list

            if do_it:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.datum == genstat.datum), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.datum = genstat.datum


                s_list.ly_fcast = s_list.ly_fcast + 1
                s_list.ly_actual = s_list.ly_actual + 1
                s_list.ly_logis = s_list.ly_logis + genstat.logis

        for s_list in query(s_list_list):
            datum1 = s_list.datum
            datum1 = date_mdy(get_month(datum1) , get_day(datum1) , get_year(datum1) + 1)

            room_list = query(room_list_list, filters=(lambda room_list :room_list.datum == datum1), first=True)

            if room_list:
                tot_logis = tot_logis + s_list.ly_logis
                s_list.ly_logis = s_list.ly_logis / s_list.ly_actual
                room_list.ly_fcast = to_string(s_list.ly_fcast, ">>>>>>9")
                room_list.ly_actual = to_string(s_list.ly_actual, ">>>>>>9")
                room_list.ly_avlodge = to_string(s_list.ly_logis, "->,>>>,>>9.99")
                tot_fcast = tot_fcast + s_list.ly_fcast
                tot_actual = tot_actual + s_list.ly_actual

    def calculate_2():

        nonlocal date_1, date_2, curr_ci_date, ci_date, from_date, to_date, exchg_rate, tot_fcast, tot_actual, tot_logis, htparam, waehrung, genstat, segment, res_line


        nonlocal room_list, segm_list, argt_list, zikat_list, s_list
        nonlocal room_list_list, segm_list_list, argt_list_list, zikat_list_list, s_list_list

        do_it:bool = False
        rmsharer:bool = False
        datum1:date = None
        s_list_list.clear()

        for genstat in db_session.query(Genstat).filter(
                (Genstat.datum >= date_1) &  (Genstat.datum <= date_2) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
            rmsharer = (genstat.resstatus == 13)
            do_it = not rmsharer

            if do_it:

                if genstat.res_date[0] < genstat.datum and genstat.res_date[1] == genstat.datum and genstat.resstatus == 8:
                    do_it = False

            if do_it and excl_compl:

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == genstat.segmentcode) &  ((Segment.betriebsnr == 1) |  (Segment.betriebsnr == 2))).first()

                if segment:
                    do_it = False


                else:

                    if genstat.zipreis == 0 and genstat.gratis != 0 and genstat.resstatus == 6 and genstat.res_logic[1]:
                        do_it = False

            if do_it:

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == genstat.segmentcode)).first()
                do_it = None != segment and segment.vip_level == 0

            if do_it:

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == genstat.segmentcode)).first()
                do_it = None != segment and segment.vip_level == 0

            if do_it and not all_segm:

                segm_list = query(segm_list_list, filters=(lambda segm_list :segm_list.segm == genstat.segmentcode and segm_list.selected), first=True)
                do_it = None != segm_list

            if do_it and not all_argt:

                argt_list = query(argt_list_list, filters=(lambda argt_list :argt_list.argt == genstat.argt and argt_list.selected), first=True)
                do_it = None != argt_list

            if do_it and not all_zikat:

                zikat_list = query(zikat_list_list, filters=(lambda zikat_list :zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected), first=True)
                do_it = None != zikat_list

            if do_it:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.datum == genstat.datum), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.datum = genstat.datum


                s_list.ly_fcast = s_list.ly_fcast + 1
                s_list.ly_actual = s_list.ly_actual + 1
                s_list.ly_logis = s_list.ly_logis + genstat.logis

        for s_list in query(s_list_list):
            datum1 = s_list.datum
            datum1 = date_mdy(get_month(datum1) , get_day(datum1) , get_year(datum1) + 1)

            room_list = query(room_list_list, filters=(lambda room_list :room_list.datum == datum1), first=True)

            if room_list:
                tot_logis = tot_logis + s_list.ly_logis
                s_list.ly_logis = s_list.ly_logis / s_list.ly_actual
                room_list.ly_fcast = to_string(s_list.ly_fcast, ">>>>>>9")
                room_list.ly_actual = to_string(s_list.ly_actual, ">>>>>>9")
                room_list.ly_avlodge = to_string(s_list.ly_logis, "->,>>>,>>9.99")
                tot_fcast = tot_fcast + s_list.ly_fcast
                tot_actual = tot_actual + s_list.ly_actual

    def calculate_3():

        nonlocal date_1, date_2, curr_ci_date, ci_date, from_date, to_date, exchg_rate, tot_fcast, tot_actual, tot_logis, htparam, waehrung, genstat, segment, res_line


        nonlocal room_list, segm_list, argt_list, zikat_list, s_list
        nonlocal room_list_list, segm_list_list, argt_list_list, zikat_list_list, s_list_list

        curr_date:date = None
        do_it:bool = False
        datum3:date = None
        datum1:date = None
        datum2:date = None
        s_list_list.clear()

        res_line_obj_list = []
        for res_line, waehrung in db_session.query(Res_line, Waehrung).join(Waehrung,(Waehrungsnr == Res_line.betriebsnr)).filter(
                ((Res_line.active_flag == 2) &  (Res_line.resstatus <= 13) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 12) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (not (Res_line.ankunft > date_2)) &  (not (Res_line.abreise < date_1))) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] == 0)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            do_it = True

            if do_it:

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == genfcast.segmentcode)).first()
                do_it = None != segment and segment.vip_level == 0

            if do_it and not all_segm:

                segm_list = query(segm_list_list, filters=(lambda segm_list :segm_list.segm == genfcast.segmentcode and segm_list.selected), first=True)
                do_it = None != segm_list

            if do_it and not all_argt:

                argt_list = query(argt_list_list, filters=(lambda argt_list :argt_list.argt == genfcast.argt and argt_list.selected), first=True)
                do_it = None != argt_list

            if do_it and not all_zikat:

                zikat_list = query(zikat_list_list, filters=(lambda zikat_list :zikat_list.zikatnr == genfcast.zikatnr and zikat_list.selected), first=True)
                do_it = None != zikat_list
            datum1 = date_1

            if res_line.ankunft > datum1:
                datum1 = res_line.ankunft
            datum2 = date_2

            if res_line.abreise < datum2:
                datum2 = res_line.abreise
            for curr_date in range(datum1,datum2 + 1) :

                if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.datum == curr_date), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.datum = curr_date


                    s_list.ly_fcast = s_list.ly_fcast + res_line.zimmeranz

        for s_list in query(s_list_list):
            datum3 = s_list.datum
            datum3 = date_mdy(get_month(datum3) , get_day(datum3) , get_year(datum3) + 1)

            room_list = query(room_list_list, filters=(lambda room_list :room_list.datum == datum3), first=True)

            if room_list:
                room_list.ly_fcast = to_string(s_list.ly_fcast, ">>>>>>9")
                tot_fcast = tot_fcast + s_list.ly_fcast

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()

    if waehrung:
        exchg_rate = waehrung.ankauf / waehrung.einheit
    else:
        exchg_rate = 1
    curr_ci_date = get_output(htpdate(87))
    ci_date = date_mdy(2, 28, get_year(curr_ci_date) - 1)
    from_date = ci_date
    to_date = ci_date


    ci_date = date_mdy(get_month(curr_ci_date) , get_day(curr_ci_date) , YEAR (curr_ci_date) - 1)


    from_date = date_mdy(get_month(curr_from_date) , get_day(curr_from_date) , YEAR (curr_from_date) - 1)


    to_date = date_mdy(get_month(curr_to_date) , get_day(curr_to_date) , YEAR (curr_to_date) - 1)


    date_1 = from_date
    date_2 = to_date


    calculate_2()

    room_list = query(room_list_list, filters=(lambda room_list :room_list.wd == 0), first=True)
    room_list.ly_fcast = to_string(tot_fcast, ">>>>>>9")
    room_list.ly_actual = to_string(tot_actual, ">>>>>>9")
    room_list.ly_avlodge = to_string(tot_logis / tot_actual, "->,>>>,>>9.99")

    return generate_output()