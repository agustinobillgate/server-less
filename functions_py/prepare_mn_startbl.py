#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 20/10/2025
# options -> arrangement.options
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
import re
from functions.ratecode_rate import ratecode_rate
from models import Htparam, Bill, Res_line, Guest, Reslin_queasy, Res_history, Waehrung, Reservation, Arrangement, Artikel, Guest_pr, Queasy, Segment, Zimkateg, Fixleist, Katpreis, Pricecod, Argt_line, Pricegrp, Resplan, Zimplan, Zimmer, Outorder

def prepare_mn_startbl(case_type:int, pvilanguage:int):

    prepare_cache ([Htparam, Bill, Guest, Reslin_queasy, Res_history, Waehrung, Reservation, Arrangement, Guest_pr, Queasy, Segment, Zimkateg, Katpreis, Pricecod, Argt_line, Pricegrp])

    mn_stopped = False
    stop_it = False
    arrival_guest = False
    msg_str = ""
    mess_str = ""
    crm_license = False
    banquet_license = False
    na_list_data = []
    lvcarea:string = "mn-start"
    ci_date:date = None
    new_contrate:bool = False
    contcode:string = ""
    created_date:date = None
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    htparam = bill = res_line = guest = reslin_queasy = res_history = waehrung = reservation = arrangement = artikel = guest_pr = queasy = segment = zimkateg = fixleist = katpreis = pricecod = argt_line = pricegrp = resplan = zimplan = zimmer = outorder = None

    na_list = None

    na_list_data, Na_list = create_model("Na_list", {"reihenfolge":int, "flag":int, "anz":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_data, lvcarea, ci_date, new_contrate, contcode, created_date, wd_array, htparam, bill, res_line, guest, reslin_queasy, res_history, waehrung, reservation, arrangement, artikel, guest_pr, queasy, segment, zimkateg, fixleist, katpreis, pricecod, argt_line, pricegrp, resplan, zimplan, zimmer, outorder
        nonlocal case_type, pvilanguage


        nonlocal na_list
        nonlocal na_list_data

        return {"mn_stopped": mn_stopped, "stop_it": stop_it, "arrival_guest": arrival_guest, "msg_str": msg_str, "mess_str": mess_str, "crm_license": crm_license, "banquet_license": banquet_license, "na-list": na_list_data}

    def get_rackrate(erwachs:int, kind1:int, kind2:int):

        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_data, lvcarea, ci_date, new_contrate, contcode, created_date, wd_array, htparam, bill, res_line, guest, reslin_queasy, res_history, waehrung, reservation, arrangement, artikel, guest_pr, queasy, segment, zimkateg, fixleist, katpreis, pricecod, argt_line, pricegrp, resplan, zimplan, zimmer, outorder
        nonlocal case_type, pvilanguage


        nonlocal na_list
        nonlocal na_list_data

        rate:Decimal = to_decimal("0.0")

        if erwachs >= 1 and erwachs <= 4:
            rate =  to_decimal(rate) + to_decimal(katpreis.perspreis[erwachs - 1])
        rate =  to_decimal(rate) + to_decimal(kind1) * to_decimal(katpreis.kindpreis[0] + kind2) * to_decimal(katpreis.kindpreis[1])
        return rate


    def check_license_date():

        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_data, lvcarea, ci_date, new_contrate, contcode, created_date, wd_array, htparam, bill, res_line, guest, reslin_queasy, res_history, waehrung, reservation, arrangement, artikel, guest_pr, queasy, segment, zimkateg, fixleist, katpreis, pricecod, argt_line, pricegrp, resplan, zimplan, zimmer, outorder
        nonlocal case_type, pvilanguage


        nonlocal na_list
        nonlocal na_list_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 976)]})

        if htparam.fdate != None:

            if htparam.fdate < get_current_date():
                stop_it = True
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Your License was valid until", lvcarea, "") + " " + to_string(htparam.fdate) + " " + translateExtended ("only.", lvcarea, "") + chr_unicode(10) + translateExtended ("Please contact your next Our Technical Support for further information.", lvcarea, "")
        else:
            stop_it = True

        if stop_it:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 999)]})

            if htparam.flogical:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 996)]})
                htparam.fchar = ""
                pass


    def check_today_arrival_guest():

        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_data, lvcarea, ci_date, new_contrate, contcode, created_date, wd_array, htparam, bill, res_line, guest, reslin_queasy, res_history, waehrung, reservation, arrangement, artikel, guest_pr, queasy, segment, zimkateg, fixleist, katpreis, pricecod, argt_line, pricegrp, resplan, zimplan, zimmer, outorder
        nonlocal case_type, pvilanguage


        nonlocal na_list
        nonlocal na_list_data

        answer:bool = False

        res_line = db_session.query(Res_line).filter(
                 (Res_line.active_flag == 0) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 11)) & (Res_line.ankunft == ci_date)).first()

        if res_line:
            msg_str = msg_str + chr_unicode(2) + "&Q" + translateExtended ("Today's arrival guest(s) record found.", lvcarea, "") + chr_unicode(10) + translateExtended ("Are you sure you want to proceed the Midnight Program?", lvcarea, "")
            arrival_guest = True
            stop_it = True

            return


    def check_room_sharers():

        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_data, lvcarea, ci_date, new_contrate, contcode, created_date, wd_array, htparam, bill, res_line, guest, reslin_queasy, res_history, waehrung, reservation, arrangement, artikel, guest_pr, queasy, segment, zimkateg, fixleist, katpreis, pricecod, argt_line, pricegrp, resplan, zimplan, zimmer, outorder
        nonlocal case_type, pvilanguage


        nonlocal na_list
        nonlocal na_list_data

        rbuff = None
        Rbuff =  create_buffer("Rbuff",Res_line)

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag == 1) & (Res_line.resstatus == 13) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

            rbuff = db_session.query(Rbuff).filter(
                     (Rbuff.active_flag == 1) & (Rbuff.zinr == res_line.zinr) & (Rbuff.resstatus == 6)).first()

            if not rbuff:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Difference rate between Reservation and Fixed rate found. The Night Audit process not posibble.", lvcarea, "")
                stop_it = True

                return


    def check_room_rate():

        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_data, lvcarea, ci_date, new_contrate, contcode, created_date, wd_array, htparam, bill, res_line, guest, reslin_queasy, res_history, waehrung, reservation, arrangement, artikel, guest_pr, queasy, segment, zimkateg, fixleist, katpreis, pricecod, argt_line, pricegrp, resplan, zimplan, zimmer, outorder
        nonlocal case_type, pvilanguage


        nonlocal na_list
        nonlocal na_list_data

        rbuff = None
        cdate:date = None
        Rbuff =  create_buffer("Rbuff",Res_line)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
        cdate = htparam.fdate

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag == 1) & (Res_line.resstatus == 6) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, cdate)],"date2": [(ge, cdate)]})

            if reslin_queasy and res_line.zipreis != reslin_queasy.deci1:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Different rate found! Night Audit process not possible.", lvcarea, "")
                stop_it = True

                return


    def midnite_prog():

        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_data, lvcarea, ci_date, new_contrate, contcode, created_date, wd_array, htparam, bill, res_line, guest, reslin_queasy, res_history, waehrung, reservation, arrangement, artikel, guest_pr, queasy, segment, zimkateg, fixleist, katpreis, pricecod, argt_line, pricegrp, resplan, zimplan, zimmer, outorder
        nonlocal case_type, pvilanguage


        nonlocal na_list
        nonlocal na_list_data


        reorg_prog()
        check_cancelled_res_line()
        check_delete_res_line()
        check_cekout_res_line()

        htparam = get_cache (Htparam, {"paramnr": [(eq, 105)]})

        if htparam.fdate < get_current_date():
            htparam.fdate = htparam.fdate + timedelta(days=1)
        ci_date = htparam.fdate
        pass

        htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
        htparam.fdate = ci_date
        pass


    def check_cancelled_res_line():

        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_data, lvcarea, ci_date, new_contrate, contcode, created_date, wd_array, htparam, bill, res_line, guest, reslin_queasy, res_history, waehrung, reservation, arrangement, artikel, guest_pr, queasy, segment, zimkateg, fixleist, katpreis, pricecod, argt_line, pricegrp, resplan, zimplan, zimmer, outorder
        nonlocal case_type, pvilanguage


        nonlocal na_list
        nonlocal na_list_data

        rbuff = None
        Rbuff =  create_buffer("Rbuff",Res_line)

        res_line = get_cache (Res_line, {"resstatus": [(eq, 9)],"active_flag": [(eq, 0)]})
        while None != res_line:

            rbuff = db_session.query(Rbuff).filter(
                         (Rbuff._recid == res_line._recid)).first()
            rbuff.active_flag = 2


            pass
            pass

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.resstatus == 9) & (Res_line.active_flag == 0) & (Res_line._recid > curr_recid)).first()


    def check_delete_res_line():

        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_data, lvcarea, ci_date, new_contrate, contcode, created_date, wd_array, htparam, bill, res_line, guest, reslin_queasy, res_history, waehrung, reservation, arrangement, artikel, guest_pr, queasy, segment, zimkateg, fixleist, katpreis, pricecod, argt_line, pricegrp, resplan, zimplan, zimmer, outorder
        nonlocal case_type, pvilanguage


        nonlocal na_list
        nonlocal na_list_data

        rbuff = None
        Rbuff =  create_buffer("Rbuff",Res_line)

        res_line = get_cache (Res_line, {"resstatus": [(eq, 99)],"active_flag": [(lt, 2)]})
        while None != res_line:

            rbuff = db_session.query(Rbuff).filter(
                         (Rbuff._recid == res_line._recid)).first()
            rbuff.active_flag = 2


            pass
            pass
            res_history = Res_history()
            db_session.add(res_history)

            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Delete ResLine: ResNo " + to_string(res_line.resnr) + " No " +\
                    to_string(res_line.reslinnr) + " - Change ActiveFlag was " +\
                    to_string(res_line.active_flag) + "To 2"
            res_history.action = "Reservation"


            pass
            pass

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.resstatus == 99) & (Res_line.active_flag < 2) & (Res_line._recid > curr_recid)).first()


    def check_cekout_res_line():

        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_data, lvcarea, ci_date, new_contrate, contcode, created_date, wd_array, htparam, bill, res_line, guest, reslin_queasy, res_history, waehrung, reservation, arrangement, artikel, guest_pr, queasy, segment, zimkateg, fixleist, katpreis, pricecod, argt_line, pricegrp, resplan, zimplan, zimmer, outorder
        nonlocal case_type, pvilanguage


        nonlocal na_list
        nonlocal na_list_data

        rbuff = None
        Rbuff =  create_buffer("Rbuff",Res_line)

        res_line = get_cache (Res_line, {"resstatus": [(eq, 8)],"active_flag": [(lt, 2)]})
        while None != res_line:

            rbuff = db_session.query(Rbuff).filter(
                         (Rbuff._recid == res_line._recid)).first()
            rbuff.active_flag = 2


            pass
            pass

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.resstatus == 8) & (Res_line.active_flag < 2) & (Res_line._recid > curr_recid)).first()


    def reorg_prog():

        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_data, lvcarea, ci_date, new_contrate, contcode, created_date, wd_array, htparam, bill, res_line, guest, reslin_queasy, res_history, waehrung, reservation, arrangement, artikel, guest_pr, queasy, segment, zimkateg, fixleist, katpreis, pricecod, argt_line, pricegrp, resplan, zimplan, zimmer, outorder
        nonlocal case_type, pvilanguage


        nonlocal na_list
        nonlocal na_list_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
        ci_date = htparam.fdate
        na_list_data.clear()
        na_list = Na_list()
        na_list_data.append(na_list)

        na_list.reihenfolge = 1
        na_list.bezeich = "Deleting Roomplan Records"
        na_list.flag = 3
        del_roomplan()
        na_list = Na_list()
        na_list_data.append(na_list)

        na_list.reihenfolge = 2
        na_list.bezeich = "Creating Roomplan records"
        na_list.flag = 3
        create_roomplan()
        na_list = Na_list()
        na_list_data.append(na_list)

        na_list.reihenfolge = 3
        na_list.bezeich = "Updating Room Status"
        na_list.flag = 3
        update_rmstatus()


    def rm_charge():

        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_data, lvcarea, ci_date, new_contrate, contcode, created_date, wd_array, htparam, bill, res_line, guest, reslin_queasy, res_history, waehrung, reservation, arrangement, artikel, guest_pr, queasy, segment, zimkateg, fixleist, katpreis, pricecod, argt_line, pricegrp, resplan, zimplan, zimmer, outorder
        nonlocal case_type, pvilanguage


        nonlocal na_list
        nonlocal na_list_data

        double_currency:bool = False
        master_exist:bool = False
        exchg_rate:Decimal = 1
        price_decimal:int = 0
        user_init:string = ""
        ct:string = ""
        st1:string = ""
        st2:string = ""
        segment_flag:bool = False
        bonus:bool = False
        roomrate:Decimal = to_decimal("0.0")
        cid:string = " "
        cdate:string = " "
        argt:string = ""
        c:string = ""
        pax:int = 0
        n:int = 0
        rbuff = None
        rline = None
        Rbuff =  create_buffer("Rbuff",Res_line)
        Rline =  create_buffer("Rline",Res_line)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
        double_currency = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 104)]})
        user_init = htparam.fchar

        htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
        price_decimal = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})

        if htparam.flogical or double_currency:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

            if waehrung:
                exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

        res_line = db_session.query(Res_line).filter(
                 (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & ((Res_line.erwachs != 0) | (Res_line.kind1 != 0) | (Res_line.kind2 != 0)) & (Res_line.l_zuordnung[inc_value(2)] == 0)).first()
        while None != res_line:

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

            arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

            artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)],"departement": [(eq, 0)]})
            n = 0

            if matches(res_line.zimmer_wunsch,r"*DATE,*"):
                n = get_index(res_line.zimmer_wunsch, "Date,")

            if n > 0:
                c = substring(res_line.zimmer_wunsch, n + 5 - 1, 8)
                created_date = date_mdy(to_int(substring(c, 4, 2)) , to_int(substring(c, 6, 2)) , to_int(substring(c, 0, 4)))
            else:
                created_date = reservation.resdat
            contcode = ""
            segment_flag = False

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(ge, ci_date),(le, ci_date)]})

            if reslin_queasy and reslin_queasy.char2 != "":
                segment_flag = True
                contcode = reslin_queasy.char2
                ct = res_line.zimmer_wunsch

                rline = db_session.query(Rline).filter(
                         (Rline._recid == res_line._recid)).first()

                if not matches(ct,r"*$CODE$*"):
                    rline.zimmer_wunsch = ct + "$CODE$" + contcode + ";"
                else:
                    st1 = substring(ct, 0, get_index(ct, "$CODE$") - 1)
                    st2 = substring(ct, length(st1) + 1 - 1)
                    st2 = substring(st2, get_index(st2, ";") + 1 - 1)
                    ct = st1 + "$CODE$" + contcode + ";" + st2
                    rline.zimmer_wunsch = trim(ct)


                pass
            else:

                guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

                if guest_pr:
                    contcode = guest_pr.code
                ct = res_line.zimmer_wunsch

                if matches(ct,r"*$CODE$*"):
                    ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                    contcode = substring(ct, 0, get_index(ct, ";") - 1)

            if segment_flag  and (contcode != ""):

                queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, contcode)]})

                if queasy and entry(0, queasy.char3, ";") != "":

                    segment = get_cache (Segment, {"bezeich": [(eq, entry(0, queasy.char3, ";"))]})

                    if segment:

                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                        reservation.segmentcode = segment.segmentcode
                        pass
            bonus = check_bonus()
            roomrate =  to_decimal(res_line.zipreis)
            argt = res_line.arrangement
            pax = res_line.erwachs

            if bonus:
                roomrate =  to_decimal("0")
            else:

                if new_contrate:
                    roomrate, argt, pax = new_update_zipreis(roomrate, argt, pax)
                else:
                    roomrate, argt, pax = update_zipreis(roomrate, argt, pax)

            if (res_line.zipreis != roomrate) or (res_line.arrangement.lower()  != (argt).lower()) or (res_line.erwachs != pax):
                cid = " "
                cdate = " "

                if trim(res_line.changed_id) != "":
                    cid = res_line.changed_id
                    cdate = to_string(res_line.changed)
                reslin_queasy = Reslin_queasy()
                db_session.add(reslin_queasy)

                reslin_queasy.key = "ResChanges"
                reslin_queasy.resnr = res_line.resnr
                reslin_queasy.reslinnr = res_line.reslinnr
                reslin_queasy.date2 = get_current_date()
                reslin_queasy.number2 = get_current_time_in_seconds()


                reslin_queasy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(pax) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(argt) + ";" + to_string(res_line.zipreis) + ";" + to_string(roomrate) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate) + ";" + to_string(get_current_date()) + ";" + to_string(res_line.name) + ";" + to_string(res_line.name) + ";"

                if res_line.was_status == 0:
                    reslin_queasy.char3 = reslin_queasy.char3 + to_string(" NO") + ";" + to_string("YES") + ";"
                else:
                    reslin_queasy.char3 = reslin_queasy.char3 + to_string("YES") + ";" + to_string("YES") + ";"
                pass
                pass

                rbuff = db_session.query(Rbuff).filter(
                             (Rbuff._recid == res_line._recid)).first()
                rbuff.zipreis =  to_decimal(roomrate)

                if argt != rbuff.arrangement:
                    rbuff.arrangement = argt

                if pax != rbuff.erwachs:
                    rbuff.erwachs = pax
                pass

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & ((Res_line.erwachs != 0) | (Res_line.kind1 != 0) | (Res_line.kind2 != 0)) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line._recid > curr_recid)).first()


    def check_bonus():

        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_data, lvcarea, ci_date, new_contrate, contcode, created_date, wd_array, htparam, bill, res_line, guest, reslin_queasy, res_history, waehrung, reservation, arrangement, artikel, guest_pr, queasy, segment, zimkateg, fixleist, katpreis, pricecod, argt_line, pricegrp, resplan, zimplan, zimmer, outorder
        nonlocal case_type, pvilanguage


        nonlocal na_list
        nonlocal na_list_data

        bonus = False
        bonus_array:List[bool] = create_empty_list(999, False)
        i:int = 0
        j:int = 1
        k:int = 0
        n:int = 0
        stay:int = 0
        pay:int = 0
        num_bonus:int = 0
        curr_zikatnr:int = 0
        rmcat = None

        def generate_inner_output():
            return (bonus)

        Rmcat =  create_buffer("Rmcat",Zimkateg)

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, ci_date)],"date2": [(ge, ci_date)]})

        if reslin_queasy:

            return generate_inner_output()

        if not guest_pr:

            return generate_inner_output()

        if res_line.l_zuordnung[0] != 0:

            rmcat = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.l_zuordnung[0])]})
            curr_zikatnr = rmcat.zikatnr
        else:
            curr_zikatnr = res_line.zikatnr

        if new_contrate:

            return generate_inner_output()

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})
        j = 1
        for i in range(1,4 + 1) :
            stay = to_int(substring(arrangement.options, j - 1, 2))
            pay = to_int(substring(arrangement.options, j + 2 - 1, 2))

            if (stay - pay) > 0:
                n = num_bonus + pay + 1
                for k in range(n,stay + 1) :
                    bonus_array[k - 1] = True
                num_bonus = stay - pay
            j = j + 4
        n = (ci_date - res_line.ankunft + 1).days

        if n >= 1:
            bonus = bonus_array[n - 1]

        return generate_inner_output()


    def new_update_zipreis(roomrate:Decimal, argt:string, pax:int):

        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_data, lvcarea, ci_date, new_contrate, contcode, created_date, wd_array, htparam, bill, res_line, guest, reslin_queasy, res_history, waehrung, reservation, arrangement, artikel, guest_pr, queasy, segment, zimkateg, fixleist, katpreis, pricecod, argt_line, pricegrp, resplan, zimplan, zimmer, outorder
        nonlocal case_type, pvilanguage


        nonlocal na_list
        nonlocal na_list_data

        rm_rate:Decimal = to_decimal("0.0")
        add_it:bool = False
        qty:int = 0
        it_exist:bool = False
        argt_defined:bool = False
        exrate1:Decimal = 1
        ex2:Decimal = 1
        child1:int = 0
        fix_rate:bool = False
        post_date:date = None
        curr_zikatnr:int = 0
        w_day:int = 0
        ebdisc_flag:bool = False
        kbdisc_flag:bool = False
        rate_found:bool = False
        early_flag:bool = False
        kback_flag:bool = False
        w1 = None
        publish_rate:Decimal = to_decimal("0.0")

        def generate_inner_output():
            return (roomrate, argt, pax)

        W1 =  create_buffer("W1",Waehrung)
        rm_rate =  to_decimal(roomrate)
        ebdisc_flag = matches(res_line.zimmer_wunsch, ("*ebdisc*"))
        kbdisc_flag = matches(res_line.zimmer_wunsch, ("*kbdisc*"))

        if res_line.l_zuordnung[0] != 0:
            curr_zikatnr = res_line.l_zuordnung[0]
        else:
            curr_zikatnr = res_line.zikatnr

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, ci_date)],"date2": [(ge, ci_date)]})

        if not reslin_queasy and res_line.abreise <= ci_date:

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, res_line.abreise - timedelta(days=1))],"date2": [(ge, res_line.abreise - timedelta(days=1))]})

        if reslin_queasy:
            roomrate =  to_decimal(reslin_queasy.deci1)

            if reslin_queasy.char1.lower()  != "" and reslin_queasy.char1.lower()  != (argt).lower() :
                argt = reslin_queasy.char1

            if reslin_queasy.number3 != 0:
                pax = reslin_queasy.number3

            return generate_inner_output()
        else:

            if it_exist:

                return generate_inner_output()

        guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

        if guest_pr:
            post_date = ci_date

            queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, res_line.reserve_int)]})

            if queasy and queasy.logi3:
                post_date = res_line.ankunft
            rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, created_date, post_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))

            if rm_rate <= 0.01:
                rm_rate =  to_decimal("0")

            fixleist = get_cache (Fixleist, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})
            while None != fixleist:

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, res_line.reserve_int)],"number2": [(eq, arrangement.argtnr)],"reslinnr": [(eq, res_line.zikatnr)],"number3": [(eq, fixleist.artnr)],"resnr": [(eq, fixleist.departement)],"date1": [(le, post_date)],"date2": [(ge, post_date)]})

                if reslin_queasy:
                    pass
                    fixleist.betrag =  to_decimal(reslin_queasy.deci1)
                    pass

                curr_recid = fixleist._recid
                fixleist = db_session.query(Fixleist).filter(
                         (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr) & (Fixleist._recid > curr_recid)).first()
            roomrate =  to_decimal(rm_rate)

            return generate_inner_output()
        else:
            w_day = wd_array[get_weekday(ci_date - 1) - 1]

            katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, ci_date - timedelta(days=1))],"endperiode": [(ge, ci_date - timedelta(days=1))],"betriebsnr": [(eq, w_day)]})

            if not katpreis:

                katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, ci_date - timedelta(days=1))],"endperiode": [(ge, ci_date - timedelta(days=1))],"betriebsnr": [(eq, 0)]})

            if not katpreis:

                return generate_inner_output()

            if res_line.zipreis != get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2):

                return generate_inner_output()
            w_day = wd_array[get_weekday(ci_date) - 1]

            katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, ci_date)],"endperiode": [(ge, ci_date)],"betriebsnr": [(eq, w_day)]})

            if not katpreis:

                katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, ci_date)],"endperiode": [(ge, ci_date)],"betriebsnr": [(eq, 0)]})

            if katpreis:
                publish_rate =  to_decimal(get_rackrate (res_line.erwachs , res_line.kind1 , res_line.kind2))

                if publish_rate == 0:

                    return generate_inner_output()
                roomrate =  to_decimal(publish_rate)

        return generate_inner_output()


    def update_zipreis(roomrate:Decimal, argt:string, pax:int):

        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_data, lvcarea, ci_date, new_contrate, contcode, created_date, wd_array, htparam, bill, res_line, guest, reslin_queasy, res_history, waehrung, reservation, arrangement, artikel, guest_pr, queasy, segment, zimkateg, fixleist, katpreis, pricecod, argt_line, pricegrp, resplan, zimplan, zimmer, outorder
        nonlocal case_type, pvilanguage


        nonlocal na_list
        nonlocal na_list_data

        rm_rate:Decimal = to_decimal("0.0")
        resline = None
        add_it:bool = False
        qty:int = 0
        it_exist:bool = False
        argt_defined:bool = False
        exrate1:Decimal = 1
        ex2:Decimal = 1
        child1:int = 0
        fix_rate:bool = False
        post_date:date = None
        curr_zikatnr:int = 0
        w_day:int = 0
        w1 = None
        publish_rate:Decimal = to_decimal("0.0")

        def generate_inner_output():
            return (roomrate, argt, pax)

        Resline =  create_buffer("Resline",Res_line)
        W1 =  create_buffer("W1",Waehrung)
        rm_rate =  to_decimal(roomrate)

        if res_line.l_zuordnung[0] != 0:
            curr_zikatnr = res_line.l_zuordnung[0]
        else:
            curr_zikatnr = res_line.zikatnr

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, ci_date)],"date2": [(ge, ci_date)]})

        if reslin_queasy:
            roomrate =  to_decimal(reslin_queasy.deci1)

            if reslin_queasy.char1.lower()  != "" and reslin_queasy.char1.lower()  != (argt).lower() :
                argt = reslin_queasy.char1

            if reslin_queasy.number3 != 0:
                pax = reslin_queasy.number3

            return generate_inner_output()
        else:

            if it_exist:

                return generate_inner_output()

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

        if guest_pr:
            post_date = ci_date

            queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, res_line.reserve_int)]})

            if queasy and queasy.logi3:
                post_date = res_line.ankunft

            pricecod = get_cache (Pricecod, {"code": [(eq, contcode)],"marknr": [(eq, res_line.reserve_int)],"argtnr": [(eq, arrangement.argtnr)],"zikatnr": [(eq, curr_zikatnr)],"startperiode": [(le, post_date)],"endperiode": [(ge, post_date)]})

            if pricecod:

                if res_line.kind1 <= pricecod.betriebsnr:
                    child1 = 0
                else:
                    child1 = res_line.kind1 - pricecod.betriebsnr
                rm_rate =  to_decimal(pricecod.perspreis[res_line.erwachs - 1] + pricecod.kindpreis[0]) * to_decimal(child1 + pricecod.kindpreis[1]) * to_decimal(res_line.kind2)

                w1 = get_cache (Waehrung, {"waehrungsnr": [(eq, arrangement.betriebsnr)]})

                if w1:
                    exrate1 =  to_decimal(w1.ankauf) / to_decimal(w1.einheit)

                if res_line.reserve_dec != 0:
                    ex2 =  to_decimal(ex2) / to_decimal(res_line.reserve_dec)
                else:

                    w1 = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                    if w1:
                        ex2 = ( to_decimal(w1.ankauf) / to_decimal(w1.einheit))

                for argt_line in db_session.query(Argt_line).filter(
                             (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind1) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():
                    add_it = False

                    if argt_line.vt_percnt == 0:

                        if argt_line.betriebsnr == 0:
                            qty = res_line.erwachs
                        else:
                            qty = argt_line.betriebsnr

                    elif argt_line.vt_percnt == 1:
                        qty = child1

                    elif argt_line.vt_percnt == 2:
                        qty = res_line.kind2

                    if qty > 0:

                        if argt_line.fakt_modus == 1:
                            add_it = True

                        elif argt_line.fakt_modus == 2:

                            if res_line.ankunft == post_date:
                                add_it = True

                        elif argt_line.fakt_modus == 3:

                            if (res_line.ankunft + 1) == post_date:
                                add_it = True

                        elif argt_line.fakt_modus == 4 and get_day(post_date) == 1:
                            add_it = True

                        elif argt_line.fakt_modus == 5 and get_day(post_date + 1) == 1:
                            add_it = True

                        elif argt_line.fakt_modus == 6:

                            if (res_line.ankunft + (argt_line.intervall - 1)) >= post_date:
                                add_it = True

                    if add_it:
                        argt_defined = False

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, post_date)],"date2": [(ge, post_date)]})

                        if reslin_queasy:
                            argt_defined = True

                            if argt_line.vt_percnt == 0:
                                rm_rate =  to_decimal(rm_rate) + to_decimal(reslin_queasy.deci1) * to_decimal(qty)

                            elif argt_line.vt_percnt == 1:
                                rm_rate =  to_decimal(rm_rate) + to_decimal(reslin_queasy.deci2) * to_decimal(qty)

                            elif argt_line.vt_percnt == 2:
                                rm_rate =  to_decimal(rm_rate) + to_decimal(reslin_queasy.deci3) * to_decimal(qty)

                        if not argt_defined:

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, pricecod.code)],"number1": [(eq, pricecod.marknr)],"number2": [(eq, pricecod.argtnr)],"reslinnr": [(eq, pricecod.zikatnr)],"number3": [(eq, argt_line.argt_artnr)],"resnr": [(eq, argt_line.departement)],"date1": [(le, post_date)],"date2": [(ge, post_date)]})

                            if reslin_queasy:

                                if argt_line.vt_percnt == 0:
                                    rm_rate =  to_decimal(rm_rate) + to_decimal(reslin_queasy.deci1) * to_decimal(qty)

                                elif argt_line.vt_percnt == 1:
                                    rm_rate =  to_decimal(rm_rate) + to_decimal(reslin_queasy.deci2) * to_decimal(qty)

                                elif argt_line.vt_percnt == 2:
                                    rm_rate =  to_decimal(rm_rate) + to_decimal(reslin_queasy.deci3) * to_decimal(qty)
                            else:
                                rm_rate =  to_decimal(rm_rate) + to_decimal(argt_line.betrag) * to_decimal(qty) * to_decimal(exrate1) / to_decimal(ex2)

                fixleist = get_cache (Fixleist, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})
                while None != fixleist:

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, pricecod.code)],"number1": [(eq, pricecod.marknr)],"number2": [(eq, pricecod.argtnr)],"reslinnr": [(eq, pricecod.zikatnr)],"number3": [(eq, fixleist.artnr)],"resnr": [(eq, fixleist.departement)],"date1": [(le, post_date)],"date2": [(ge, post_date)]})

                    if reslin_queasy:
                        pass
                        fixleist.betrag =  to_decimal(reslin_queasy.deci1)
                        pass

                    curr_recid = fixleist._recid
                    fixleist = db_session.query(Fixleist).filter(
                                 (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr) & (Fixleist._recid > curr_recid)).first()
            else:

                pricegrp = get_cache (Pricegrp, {"code": [(eq, contcode)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, ci_date)],"endperiode": [(ge, ci_date)]})

                if pricegrp:
                    rm_rate =  to_decimal(pricegrp.perspreis[res_line.erwachs - 1])

                if res_line.kind1 == 1 or res_line.kind1 == 2:
                    rm_rate =  to_decimal(rm_rate) + to_decimal(pricecod.kindpreis[res_line.kind1 - 1])
            roomrate =  to_decimal(rm_rate)

            return generate_inner_output()
        else:
            w_day = wd_array[get_weekday(ci_date - 1) - 1]

            katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, ci_date - timedelta(days=1))],"endperiode": [(ge, ci_date - timedelta(days=1))],"betriebsnr": [(eq, w_day)]})

            if not katpreis:

                katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, ci_date - timedelta(days=1))],"endperiode": [(ge, ci_date - timedelta(days=1))],"betriebsnr": [(eq, 0)]})

            if not katpreis:

                return generate_inner_output()

            if res_line.zipreis != get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2):

                return generate_inner_output()
            w_day = wd_array[get_weekday(ci_date) - 1]

            katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, ci_date)],"endperiode": [(ge, ci_date)],"betriebsnr": [(eq, w_day)]})

            if not katpreis:

                katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, ci_date)],"endperiode": [(ge, ci_date)],"betriebsnr": [(eq, 0)]})

            if katpreis:
                publish_rate =  to_decimal(get_rackrate (res_line.erwachs , res_line.kind1 , res_line.kind2))

                if publish_rate == 0:

                    return generate_inner_output()
                roomrate =  to_decimal(publish_rate)

        return generate_inner_output()


    def del_roomplan():

        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_data, lvcarea, ci_date, new_contrate, contcode, created_date, wd_array, htparam, bill, res_line, guest, reslin_queasy, res_history, waehrung, reservation, arrangement, artikel, guest_pr, queasy, segment, zimkateg, fixleist, katpreis, pricecod, argt_line, pricegrp, resplan, zimplan, zimmer, outorder
        nonlocal case_type, pvilanguage


        nonlocal na_list
        nonlocal na_list_data

        i:int = 0

        resplan = get_cache (Resplan, {"datum": [(ge, ci_date)]})

        na_list = query(na_list_data, filters=(lambda na_list: na_list.reihenfolge == 1), first=True)
        while None != resplan:
            i = i + 1
            na_list.anz = na_list.anz + 1
            pass
            db_session.delete(resplan)
            pass

            curr_recid = resplan._recid
            resplan = db_session.query(Resplan).filter(
                     (Resplan.datum >= ci_date) & (Resplan._recid > curr_recid)).first()

        zimplan = get_cache (Zimplan, {"datum": [(ge, ci_date)]})
        while None != zimplan:
            i = i + 1
            na_list.anz = na_list.anz + 1
            pass
            db_session.delete(zimplan)

            curr_recid = zimplan._recid
            zimplan = db_session.query(Zimplan).filter(
                     (Zimplan.datum >= ci_date) & (Zimplan._recid > curr_recid)).first()


    def create_roomplan():

        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_data, lvcarea, ci_date, new_contrate, contcode, created_date, wd_array, htparam, bill, res_line, guest, reslin_queasy, res_history, waehrung, reservation, arrangement, artikel, guest_pr, queasy, segment, zimkateg, fixleist, katpreis, pricecod, argt_line, pricegrp, resplan, zimplan, zimmer, outorder
        nonlocal case_type, pvilanguage


        nonlocal na_list
        nonlocal na_list_data

        i:int = 0
        j:int = 0
        anz:int = 0
        beg_datum:date = None
        end_datum:date = None
        curr_date:date = None

        na_list = query(na_list_data, filters=(lambda na_list: na_list.reihenfolge == 2), first=True)

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag == 0) & (Res_line.resstatus != 11) & (Res_line.ankunft >= ci_date)).order_by(Res_line._recid).all():
            j = res_line.resstatus

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})
            beg_datum = res_line.ankunft
            end_datum = res_line.abreise - timedelta(days=1)

            if zimkateg:
                for curr_date in date_range(beg_datum,end_datum) :

                    resplan = get_cache (Resplan, {"zikatnr": [(eq, zimkateg.zikatnr)],"datum": [(eq, curr_date)]})

                    if not resplan:
                        i = i + 1
                        na_list.anz = na_list.anz + 1
                        resplan = Resplan()
                        db_session.add(resplan)

                        resplan.datum = curr_date
                        resplan.zikatnr = zimkateg.zikatnr
                        resplan.anzzim[j - 1] = res_line.zimmeranz


                    elif resplan:
                        pass
                        resplan.anzzim[j - 1] = resplan.anzzim[j - 1] + res_line.zimmeranz
                        pass
                        pass

            if res_line.zinr != "":
                for curr_date in date_range(beg_datum,end_datum) :

                    zimplan = get_cache (Zimplan, {"datum": [(eq, curr_date)],"zinr": [(eq, res_line.zinr)]})

                    if not zimplan:
                        i = i + 1
                        na_list.anz = na_list.anz + 1
                        zimplan = Zimplan()
                        db_session.add(zimplan)

                        zimplan.datum = curr_date
                        zimplan.zinr = res_line.zinr
                        zimplan.res_recid = res_line._recid
                        zimplan.gastnrmember = res_line.gastnrmember
                        zimplan.bemerk = res_line.bemerk
                        zimplan.resstatus = res_line.resstatus
                        zimplan.name = res_line.name


                        pass

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag == 1) & (Res_line.abreise > ci_date) & (Res_line.resstatus != 12)).order_by(Res_line._recid).all():
            j = res_line.resstatus

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})
            beg_datum = ci_date
            end_datum = res_line.abreise - timedelta(days=1)

            if zimkateg:
                for curr_date in date_range(beg_datum,end_datum) :

                    resplan = get_cache (Resplan, {"zikatnr": [(eq, zimkateg.zikatnr)],"datum": [(eq, curr_date)]})

                    if not resplan:
                        i = i + 1
                        na_list.anz = na_list.anz + 1
                        resplan = Resplan()
                        db_session.add(resplan)

                        resplan.datum = curr_date
                        resplan.zikatnr = zimkateg.zikatnr
                        resplan.anzzim[j - 1] = res_line.zimmeranz


                    elif resplan:
                        pass
                        resplan.anzzim[j - 1] = resplan.anzzim[j - 1] + res_line.zimmeranz
                        pass
                        pass

            if res_line.resstatus == 6:
                for curr_date in date_range(beg_datum,end_datum) :

                    zimplan = get_cache (Zimplan, {"datum": [(eq, curr_date)],"zinr": [(eq, res_line.zinr)]})

                    if not zimplan:
                        i = i + 1
                        na_list.anz = na_list.anz + 1
                        zimplan = Zimplan()
                        db_session.add(zimplan)

                        zimplan.datum = curr_date
                        zimplan.zinr = res_line.zinr
                        zimplan.res_recid = res_line._recid
                        zimplan.gastnrmember = res_line.gastnrmember
                        zimplan.bemerk = res_line.bemerk
                        zimplan.resstatus = res_line.resstatus
                        zimplan.name = res_line.name


                        pass


    def update_rmstatus():

        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_data, lvcarea, new_contrate, contcode, created_date, wd_array, htparam, bill, res_line, guest, reslin_queasy, res_history, waehrung, reservation, arrangement, artikel, guest_pr, queasy, segment, zimkateg, fixleist, katpreis, pricecod, argt_line, pricegrp, resplan, zimplan, zimmer, outorder
        nonlocal case_type, pvilanguage


        nonlocal na_list
        nonlocal na_list_data

        i:int = 0
        ci_date:date = None

        htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
        ci_date = htparam.fdate

        na_list = query(na_list_data, filters=(lambda na_list: na_list.reihenfolge == 3), first=True)

        zimmer = db_session.query(Zimmer).first()
        while None != zimmer:

            if zimmer.personal :
                pass
                zimmer.personal = False
                pass

            if zimmer.zistatus == 0 or zimmer.zistatus == 1 or zimmer.zistatus == 2:

                res_line = get_cache (Res_line, {"zinr": [(eq, zimmer.zinr)],"active_flag": [(eq, 1)],"resstatus": [(eq, 6)]})

                if res_line:
                    i = i + 1
                    na_list.anz = na_list.anz + 1
                    pass

                    if res_line.abreise == ci_date:
                        zimmer.zistatus = 3
                    else:
                        zimmer.zistatus = 5
                    zimmer.bediener_nr_stat = 0
                    pass

            elif zimmer.zistatus == 3:

                res_line = get_cache (Res_line, {"zinr": [(eq, zimmer.zinr)],"active_flag": [(eq, 1)],"resstatus": [(eq, 6)]})

                if res_line and res_line.abreise > ci_date:
                    i = i + 1
                    na_list.anz = na_list.anz + 1
                    pass
                    zimmer.zistatus = 5
                    zimmer.bediener_nr_stat = 0
                    pass

                elif not res_line:
                    i = i + 1
                    na_list.anz = na_list.anz + 1
                    pass
                    zimmer.zistatus = 1
                    zimmer.bediener_nr_stat = 0
                    pass

            elif zimmer.zistatus == 4 or zimmer.zistatus == 5:

                res_line = get_cache (Res_line, {"zinr": [(eq, zimmer.zinr)],"active_flag": [(eq, 1)],"resstatus": [(eq, 6)]})

                if res_line and res_line.abreise == ci_date:
                    i = i + 1
                    na_list.anz = na_list.anz + 1
                    pass
                    zimmer.zistatus = 3
                    zimmer.bediener_nr_stat = 0
                    pass

                elif not res_line:
                    i = i + 1
                    na_list.anz = na_list.anz + 1
                    pass
                    zimmer.zistatus = 1
                    zimmer.bediener_nr_stat = 0
                    pass

            if zimmer.zistatus == 6:

                res_line = get_cache (Res_line, {"zinr": [(eq, zimmer.zinr)],"active_flag": [(eq, 1)],"resstatus": [(eq, 6)]})

                if res_line:
                    i = i + 1
                    na_list.anz = na_list.anz + 1
                    pass

                    if res_line.abreise == ci_date:
                        zimmer.zistatus = 3
                    else:
                        zimmer.zistatus = 5
                    zimmer.bediener_nr_stat = 0
                    pass

                    outorder = get_cache (Outorder, {"zinr": [(eq, zimmer.zinr)]})

                    if outorder:
                        db_session.delete(outorder)

            curr_recid = zimmer._recid
            zimmer = db_session.query(Zimmer).filter(Zimmer._recid > curr_recid).first()

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
            i = 0

            for zimmer in db_session.query(Zimmer).filter(
                     (Zimmer.zikatnr == zimkateg.zikatnr)).order_by(Zimmer._recid).all():
                i = i + 1
            zimkateg.maxzimanz = i


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 985)]})

    if htparam.flogical:
        banquet_license = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 550)]})

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    if case_type == 1:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 105)]})

        if htparam.fdate >= get_current_date():
            mn_stopped = True

            return generate_output()
        check_license_date()

        if stop_it:
            mn_stopped = True

            return generate_output()
        check_room_sharers()

        if stop_it:
            mn_stopped = True

            return generate_output()

        htparam = get_cache (Htparam, {"paramnr": [(eq, 208)]})

        if not htparam.flogical:
            mess_str = translateExtended ("Checking Opened Master Bill.", lvcarea, "")

            for bill in db_session.query(Bill).filter(
                     (Bill.flag == 0) & (Bill.resnr > 0) & (Bill.reslinnr == 0)).order_by(Bill._recid).all():

                res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"active_flag": [(le, 1)],"resstatus": [(ne, 8),(ne, 9),(ne, 10)]})

                if not res_line:

                    guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})
                    msg_str = msg_str + chr_unicode(2) + translateExtended ("Opened master bill found but all guests checked-out:", lvcarea, "") + " " + to_string(bill.rechnr) + " - " + guest.name + chr_unicode(10) + translateExtended ("Midnight Program stopped.", lvcarea, "")
                    mn_stopped = True

                    return generate_output()
        check_room_rate()

        if stop_it:
            mn_stopped = True

            return generate_output()
        check_today_arrival_guest()

        if stop_it:

            return generate_output()
        else:
            case_type = 2

    if case_type == 2:
        midnite_prog()

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1459)]})

        if htparam.paramgruppe == 99 and htparam.flogical:
            crm_license = True

    return generate_output()