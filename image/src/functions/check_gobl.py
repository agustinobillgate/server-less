from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.allot_overbookbl import allot_overbookbl
import re
from functions.check_complimentbl import check_complimentbl
from functions.res_czinrbl import res_czinrbl
from models import Res_line, Bediener, Arrangement, Guest, Htparam, Zimkateg, Segment, Waehrung, Bill, Bill_line, Zimmer, Outorder, Guest_pr, Ratecode, Reslin_queasy, Kontline, Zimplan, Queasy

def check_gobl(pvilanguage:int, user_init:str, gastno:int, res_mode:str, curr_segm:str, curr_source:str, currency:str, zikat_screen:str, memo_zinr:str, guestname:str, origcontcode:str, contcode:str, marknr:int, rm_bcol:int, inactive_flag:bool, reslin_list:[Reslin_list], prev_resline:[Prev_resline], zikatstr:str):
    error_number = 0
    still_error = False
    msg_str = ""
    pswd_str = ""
    flag1 = False
    ci_date1 = None
    lvcarea:str = "mk_resline"
    ci_date:date = None
    min_stay:int = 0
    max_stay:int = 0
    min_adv:int = 0
    max_adv:int = 0
    msg_str1:str = ""
    zinr_ecode:str = ""
    res_line = bediener = arrangement = guest = htparam = zimkateg = segment = waehrung = bill = bill_line = zimmer = outorder = guest_pr = ratecode = reslin_queasy = kontline = zimplan = queasy = None

    reslin_list = prev_resline = now_resline = rline = arr = gmember = res_line1 = zimplan1 = resline = res_line2 = res_line3 = None

    reslin_list_list, Reslin_list = create_model_like(Res_line)
    prev_resline_list, Prev_resline = create_model_like(Res_line)
    now_resline_list, Now_resline = create_model_like(Res_line)

    Rline = Res_line
    Arr = Arrangement
    Gmember = Guest
    Res_line1 = Res_line
    Zimplan1 = Zimplan
    Resline = Res_line
    Res_line2 = Res_line
    Res_line3 = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_number, still_error, msg_str, pswd_str, flag1, ci_date1, lvcarea, ci_date, min_stay, max_stay, min_adv, max_adv, msg_str1, zinr_ecode, res_line, bediener, arrangement, guest, htparam, zimkateg, segment, waehrung, bill, bill_line, zimmer, outorder, guest_pr, ratecode, reslin_queasy, kontline, zimplan, queasy
        nonlocal rline, arr, gmember, res_line1, zimplan1, resline, res_line2, res_line3


        nonlocal reslin_list, prev_resline, now_resline, rline, arr, gmember, res_line1, zimplan1, resline, res_line2, res_line3
        nonlocal reslin_list_list, prev_resline_list, now_resline_list
        return {"error_number": error_number, "still_error": still_error, "msg_str": msg_str, "pswd_str": pswd_str, "flag1": flag1, "ci_date1": ci_date1}

    def check_go():

        nonlocal error_number, still_error, msg_str, pswd_str, flag1, ci_date1, lvcarea, ci_date, min_stay, max_stay, min_adv, max_adv, msg_str1, zinr_ecode, res_line, bediener, arrangement, guest, htparam, zimkateg, segment, waehrung, bill, bill_line, zimmer, outorder, guest_pr, ratecode, reslin_queasy, kontline, zimplan, queasy
        nonlocal rline, arr, gmember, res_line1, zimplan1, resline, res_line2, res_line3


        nonlocal reslin_list, prev_resline, now_resline, rline, arr, gmember, res_line1, zimplan1, resline, res_line2, res_line3
        nonlocal reslin_list_list, prev_resline_list, now_resline_list

        qty:int = 0
        max_comp:int = 0
        com_rm:int = 0
        max_com:int = 0
        max_rate:decimal = 0
        exchg_rate:decimal = 1
        check_allotment:bool = False
        its_wrong:bool = False
        wrong_room:bool = False
        datum:date = None
        from_date:date = None
        to_date:date = None
        diff_str:str = ""
        error_code:int = 0
        incl_allotment:bool = False
        b_dummy:bool = False
        overbook:bool = False
        overmax:bool = False
        overanz:int = 0
        overdate:date = None
        billdate:date = None
        Rline = Res_line
        Arr = Arrangement
        Gmember = Guest

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        billdate = htparam.fdate

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1108)).first()
        max_rate = htparam.fdecimal

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 87)).first()
        ci_date = htparam.fdate

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == reslin_list.resnr) &  (Res_line.reslinnr == reslin_list.reslinnr)).first()

        if res_mode.lower()  == "new" or res_mode.lower()  == "insert" or res_mode.lower()  == "qci":
            qty = reslin_list.zimmeranz
        else:

            if res_mode.lower()  == "inhouse":
                qty = 0

                if reslin_list.resstatus == 6 and res_line.resstatus == 6:
                    qty = reslin_list.zimmeranz - res_line.zimmeranz

                elif reslin_list.resstatus == 6 and res_line.resstatus == 13:
                    qty = reslin_list.zimmeranz
            else:
                qty = 0

                if (reslin_list.resstatus <= 2 or reslin_list.resstatus == 5) and (res_line.resstatus <= 2 or res_line.resstatus == 5):
                    qty = reslin_list.zimmeranz - res_line.zimmeranz

                elif (reslin_list.resstatus <= 2 or reslin_list.resstatus == 5) and (res_line.resstatus == 3 or res_line.resstatus == 4 or res_line.resstatus == 11):
                    qty = reslin_list.zimmeranz

        if reslin_list.erwachs > 0 and reslin_list.gratis > 0:
            error_number = 1

            return

        if (res_mode.lower()  == "inhouse" or res_mode.lower().lower()  == "qci") and reslin_list.zinr == "":
            msg_str = translateExtended ("Room Number not yet selected.", lvcarea, "")
            error_number = 30

            return

        arrangement = db_session.query(Arrangement).filter(
                (Arrangement == reslin_list.arrangement)).first()

        if not arrangement:
            msg_str = translateExtended ("No such Arrangement Code:", lvcarea, "") +\
                    " " + reslin_list.arrangement


            error_number = 34

            return

        if arrangement.waeschewechsel != 0 and reslin_list.erwachs != arrangement.waeschewechsel:
            msg_str = translateExtended ("Wrong Arrangement / Adult", lvcarea, "")
            error_number = 41

            return

        if arrangement.handtuch != 0 and reslin_list.anztage != arrangement.handtuch:
            msg_str = translateExtended ("Wrong Arrangement / Night of Stay", lvcarea, "")
            error_number = 42

            return

        zimkateg = db_session.query(Zimkateg).filter(
                (func.lower(Zimkateg.kurzbez) == (zikatstr).lower())).first()

        if not zimkateg:
            msg_str = translateExtended ("No such Room Type.", lvcarea, "")
            error_number = 43

            return

        if (reslin_list.active_flag == 0) and (reslin_list.ankunft < ci_date):
            msg_str = translateExtended ("Wrong check_in date!", lvcarea, "")
            error_number = 2

            return

        if reslin_list.abreise < ci_date:
            msg_str = translateExtended ("Wrong check_out date!", lvcarea, "")
            error_number = 3

            return

        if reslin_list.abreise < reslin_list.ankunft:
            msg_str = translateExtended ("Wrong date!", lvcarea, "")
            error_number = 4

            return

        if curr_segm == "":
            msg_str = translateExtended ("Segment Code not defined.", lvcarea, "")
            error_number = 6

            return

        segment = db_session.query(Segment).filter(
                (Segment.segmentcode == to_int(substring(curr_segm, 0,1 + get_index(curr_segm, " "))))).first()

        if segment and segment.betriebsnr > 0:

            if reslin_list.erwachs > 0:
                msg_str = translateExtended ("Compliment / HU Segment but adult > 0.", lvcarea, "")
                error_number = 7

                return

            rline = db_session.query(Rline).filter(
                    (Rline.resnr == reslin_list.resnr) &  (Rline.reslinnr != reslin_list.reslinnr) &  (Rline.active_flag <= 1) &  (Rline.zipreis > 0)).first()

            if rline or reslin_list.zipreis > 0:
                msg_str = translateExtended ("Reservation member found with Rate > 0.", lvcarea, "")
                error_number = 8

                return

        if curr_source == "":
            msg_str = translateExtended ("Source of Booking not defined.", lvcarea, "")
            error_number = 9

            return

        if reslin_list.zimmeranz == 0:
            msg_str = translateExtended ("Wrong Room Quantity!", lvcarea, "")
            error_number = 10

            return

        elif reslin_list.zimmeranz > 1 and reslin_list.zinr != "":
            msg_str = translateExtended ("Room number already assigned.", lvcarea, "")
            error_number = 11

            return

        if max_rate != 0 and reslin_list.zipreis > 0:

            if reslin_list.betriebsnr > 0:

                waehrung = db_session.query(Waehrung).filter(
                        (Waehrungsnr == reslin_list.betriebsnr)).first()
            else:

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 144)).first()

                waehrung = db_session.query(Waehrung).filter(
                        (Waehrung.wabkurz == htparam.fchar)).first()

            if waehrung:
                exchg_rate = waehrung.ankauf / waehrung.einheit

            if reslin_list.zipreis * exchg_rate > max_rate:
                msg_str = translateExtended ("Room Rate incorrect / too large! Check currency.", lvcarea, "")
                error_number = 12

                return

        if inactive_flag:

            if reslin_list.zipreis > 0:
                msg_str = translateExtended ("Inactive Room! Room Rate must be 0.", lvcarea, "")
                error_number = 45

                return

        if reslin_list.resstatus == 6:

            bill = db_session.query(Bill).filter(
                    (Bill.resnr == res_line.resnr) &  (Bill.reslinnr == res_line.reslinnr)).first()

            if bill:

                bill_line = db_session.query(Bill_line).filter(
                        (Bill_line.rechnr == bill.rechnr) &  (Bill_line.bill_datum == billdate) &  (Bill_line.zinr == reslin_list.zinr) &  (Bill_line.artnr == 99)).first()

                if bill_line and bill_line.betrag != reslin_list.zipreis:
                    msg_str = translateExtended ("Room charge has been posted for this Rsv.", lvcarea, "")
                    error_number = 46

                    return

        if reslin_list.zimmerfix and reslin_list.resstatus != 13:

            if reslin_list.zinr != "":

                rline = db_session.query(Rline).filter(
                        (Rline.resnr == reslin_list.resnr) &  (Rline.reslinnr != reslin_list.reslinnr) &  (Rline.resstatus == 6) &  (Rline.zinr == reslin_list.zinr)).first()
                its_wrong = None != rline

                if not its_wrong:

                    rline = db_session.query(Rline).filter(
                            (Rline.zinr == reslin_list.zinr) &  (Rline.active_flag == 1) &  (Rline.resnr != reslin_list.resnr)).first()
                    its_wrong = None != rline

            if its_wrong:
                msg_str = translateExtended ("Wrong Status as Room sharer.", lvcarea, "")
                error_number = 13

                return

        if (reslin_list.resstatus == 11 or reslin_list.resstatus == 13) and (reslin_list.erwachs > 0) and (reslin_list.zipreis == 0):
            msg_str = translateExtended ("Number of Adult for Room sharer should be 0.", lvcarea, "")
            error_number = 14

            return

        if currency == "":
            msg_str = translateExtended ("currency not defined.", lvcarea, "")
            error_number = 15

            return

        if (reslin_list.zipreis > 0) and (reslin_list.gratis > 0):
            msg_str = translateExtended ("Rate > 0 can not be applied to compliment guest.", lvcarea, "")
            error_number = 17

            return

        if reslin_list.erwachs == 0 and reslin_list.kind1 == 0 and reslin_list.kind2 == 0 and reslin_list.zipreis > 0:
            msg_str = translateExtended ("Input incorrect: Adult  ==  0 but Room_Rate > 0.", lvcarea, "")
            error_number = 18

            return

        if (reslin_list.erwachs == 0 and reslin_list.kind1 == 0 and reslin_list.kind2 == 0 and reslin_list.gratis == 0) and reslin_list.resstatus != 11 and reslin_list.resstatus != 13:
            msg_str = translateExtended ("Input of PAX incorrect.", lvcarea, "")
            error_number = 44

            return

        if reslin_list.gratis > 0 and reslin_list.zipreis > 0:
            msg_str = translateExtended ("Input incorrect: Compliment guest but Room_Rate > 0.", lvcarea, "")
            error_number = 19

            return

        if memo_zinr != "":

            zimmer = db_session.query(Zimmer).filter(
                    (func.lower(Zimmer.zinr) == (memo_zinr).lower())).first()

            if not zimmer:
                msg_str = translateExtended ("Wrong Memo RmNo / no such room number.", lvcarea, "")
                error_number = 20

                return

        if rm_bcol != 15 and reslin_list.zinr == "":
            msg_str = translateExtended ("Off_Market Room number can not be changed.", lvcarea, "")
            error_number = 21

            return

        elif rm_bcol != 15 and reslin_list.ankunft != res_line.ankunft:

            outorder = db_session.query(Outorder).filter(
                    (Outorder.zinr == reslin_list.zinr) &  (Outorder.betriebsnr == reslin_list.resnr)).first()

            if outorder and outorder.gespstart < outorder.gespend:
                from_date = reslin_list.ankunft - outorder.gespende + outorder.gespstart
                to_date = reslin_list.abreise

                if from_date != to_date:

                    rline = db_session.query(Rline).filter(
                            (Rline.active_flag <= 1) &  (Rline.resnr != reslin_list.resnr) &  (((Rline.ankunft >= from_date) &  (Rline.ankunft <= to_date)) |  ((Rline.abreise >= from_date) &  (Rline.abreise <= to_date)) |  ((Rline.from_date >= Rline.ankunft) &  (Rline.to_date <= Rline.abreise))) &  (Rline.zinr == reslin_list.zinr)).first()
                else:

                    rline = db_session.query(Rline).filter(
                            (Rline.active_flag <= 1) &  (Rline.resnr != reslin_list.resnr) &  ((Rline.from_date > Rline.ankunft) &  (Rline.from_date < Rline.abreise)) &  (Rline.zinr == reslin_list.zinr)).first()

                if rline:
                    msg_str = translateExtended ("Attention RmNo : ", lvcarea, "") + to_string(rline.zinr) + chr(10) +\
                            translateExtended ("Reservation exists under ResNo  ==  ", lvcarea, "") +\
                            to_string(rline.resnr) + chr(10) +\
                            translateExtended ("Guest name  ==  ", lvcarea, "") + rline.name + chr(10) +\
                            translateExtended ("Arrival / Departure : ", lvcarea, "") +\
                            to_string(rline.ankunft) + " / " + to_string(rline.abreise) + chr(10)
                    error_number = 22

                    return

        if zikatstr == "":
            msg_str = translateExtended ("Room Type not yet defined.", lvcarea, "")
            error_number = 23

            return

        if reslin_list.arrangement == "":
            msg_str = translateExtended ("Arrangement not yet defined.", lvcarea, "")
            error_number = 24

            return

        guest_pr = db_session.query(Guest_pr).filter(
                (Guest_pr.gastnr == gastno)).first()

        if guest_pr and reslin_list.reserve_int == 0:

            ratecode = db_session.query(Ratecode).filter(
                    (Ratecode.code == guest_pr.CODE) &  (reslin_list.ankunft >= Ratecode.startperiode) &  (reslin_list.ankunft <= Ratecode.endperiode)).first()

            if ratecode:
                msg_str = translateExtended ("Market Segment not yet defined.", lvcarea, "")
                error_number = 25

                return
        check_min_maxstay()

        if error_number > 0:

            return

        if reslin_list.active_flag == 0:

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                    (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == reslin_list.resnr) &  (Reslin_queasy.reslinnr == reslin_list.reslinnr) &  (Reslin_queasy.date1 <= reslin_list.ankunft) &  (Reslin_queasy.date2 >= reslin_list.ankunft)).first()

            if reslin_queasy and reslin_queasy.char1 != "" and reslin_queasy.char1 != reslin_list.arrangement:
                msg_str = msg_str + chr(2) +\
                        translateExtended ("Wrong arrangement in AdHoc Rate setup, fix it now.", lvcarea, "")
                error_number = 26

                return

        if res_mode.lower()  == "inhouse":

            rline = db_session.query(Rline).filter(
                    (Rline.active_flag == 0) &  (Rline.zinr == reslin_list.zinr) &  (Rline.ankunft >= reslin_list.ankunft) &  (Rline.ankunft < reslin_list.abreise) &  (Rline.resnr != reslin_list.resnr) &  (Rline.resstatus != 11)).first()

            if rline:
                msg_str = msg_str + chr(2) +\
                        translateExtended ("Reservation found for the same room within the period of stay:", lvcarea, "") + chr(10) +\
                        rline.name + " - " + translateExtended ("RmNo", lvcarea, "") + " " + rline.zinr + chr(10) +\
                        to_string(rline.ankunft) + " - " + to_string(rline.abreise) + chr(10)
                error_number = 27

                return

        if reslin_list.ankunft < reslin_list.abreise:

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                    (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

            if reslin_queasy:
                datum = reslin_list.abreise - 1

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.datum >= Reslin_queasy.date1) &  (Reslin_queasy.datum <= Reslin_queasy.date2)).first()

                if not reslin_queasy:
                    msg_str = msg_str + chr(2) +\
                            translateExtended ("Fixed_Rate Period incorrect, re_check it.", lvcarea, "")
                    error_number = 28

                    return

        if reslin_list.kontignr != 0 and reslin_list.resstatus != 11 and reslin_list.resstatus != 13:

            if reslin_list.kontignr != res_line.kontignr:
                check_allotment = True

            if reslin_list.ankunft < res_line.ankunft:
                check_allotment = True

            if reslin_list.ankunft >= res_line.abreise:
                check_allotment = True

            if reslin_list.abreise <= res_line.ankunft:
                check_allotment = True

            if reslin_list.abreise > res_line.abreise:
                check_allotment = True

            if reslin_list.zimmeranz > res_line.zimmeranz:
                check_allotment = True

            if reslin_list.kontignr > 0:

                kontline = db_session.query(Kontline).filter(
                        (Kontline.kontignr == reslin_list.kontignr)).first()
            else:

                kontline = db_session.query(Kontline).filter(
                        (Kontline.kontignr == - reslin_list.kontignr)).first()

            if kontline and kontline.zikatnr != 0 and (reslin_list.zikatnr != res_line.zikatnr):
                check_allotment = True

        if check_allotment:

            if res_mode.lower()  == "inhouse":
                its_wrong, msg_str = get_output(allot_overbookbl(pvilanguage, res_mode, reslin_list.resnr, reslin_list.reslinnr, reslin_list.kontignr, reslin_list.zikatnr, reslin_list.setup, reslin_list.arrangement, reslin_list.erwachs, ci_date, reslin_list.abreise, reslin_list.zimmeranz, user_init))
            else:
                its_wrong, msg_str = get_output(allot_overbookbl(pvilanguage, res_mode, reslin_list.resnr, reslin_list.reslinnr, reslin_list.kontignr, reslin_list.zikatnr, reslin_list.setup, reslin_list.arrangement, reslin_list.erwachs, reslin_list.ankunft, reslin_list.abreise, reslin_list.zimmeranz, user_init))

            if its_wrong:

                if not re.match(".*&Q.*",msg_str):
                    error_number = 29


                else:
                    error_number = 50

                return

        if zikat_screen.lower()  != (zikatstr).lower() :
            check_bedsetup()

            return

        if res_mode.lower()  == "new" or res_mode.lower()  == "insert" or res_mode.lower()  == "qci" or ((res_mode.lower()  == "modify" or res_mode.lower()  == "split" or res_mode.lower()  == "inhouse") and (res_line.zipreis != 0 and reslin_list.zipreis == 0) or (res_line.zimmeranz != reslin_list.zimmeranz)):
            its_wrong, com_rm, max_comp, pswd_str, msg_str = get_output(check_complimentbl(pvilanguage, reslin_list.resnr, reslin_list.reslinnr, reslin_list.gastnr, reslin_list.ankunft, marknr, reslin_list.zikatnr, reslin_list.arrangement, reslin_list.zimmeranz, reslin_list.zipreis))

            if its_wrong or pswd_str != "" or msg_str != "":
                error_number = 33

                return

        if reslin_list.active_flag == 0:

            rline = db_session.query(Rline).filter(
                    (Rline.resnr == reslin_list.resnr) &  (Rline.reslinnr == reslin_list.reslinnr)).first()

            if rline.active_flag == 1:
                msg_str = msg_str + chr(2) +\
                        translateExtended ("Guest checked_in, cancel your changes.", lvcarea, "")
                error_number = 35

                return

        if reslin_list.zinr != "":
            zikatstr, error_code, msg_str1 = get_output(res_czinrbl(pvilanguage, reslin_list.ankunft, reslin_list.abreise, (reslin_list.resstatus == 11 or reslin_list.resstatus == 13), reslin_list.resnr, reslin_list.reslinnr, zikatstr, reslin_list.zinr))

            if msg_str1 != "":
                msg_str = msg_str + chr(2) + msg_str1

            if error_code != 0:
                msg_str = msg_str + chr(2) +\
                        translateExtended ("Room Assignment not possible.", lvcarea, "") + chr(10) +\
                        translateExtended (zinr_ecode[- error_code - 1], lvcarea, "")
                error_number = 39

                return
            else:

                if (res_mode.lower()  == "modify" or res_mode.lower().lower()  == "split"):
                    release_zinr(res_line.zinr)

                elif res_mode.lower()  == "inhouse" and (reslin_list.zinr != res_line.zinr):
                    release_zinr(res_line.zinr)

                if (res_mode.lower()  == "modify" or res_mode.lower().lower()  == "split" or res_mode.lower().lower()  == "new" or res_mode.lower().lower()  == "insert" or res_mode.lower().lower()  == "qci" or (res_mode.lower()  == "inhouse" and (reslin_list.zinr != res_line.zinr))):
                    wrong_room = assign_zinr(res_line._recid, reslin_list.ankunft, reslin_list.abreise, reslin_list.zinr, reslin_list.resstatus, reslin_list.gastnrmember, reslin_list.bemerk, guestname)

                    if wrong_room:

                        if res_line.zinr != "":
                            b_dummy = assign_zinr(res_line._recid, res_line.ankunft, res_line.abreise, res_line.zinr, res_line.resstatus, res_line.gastnrmember, res_line.bemerk, res_line.name)
                        error_number = 40

                        return

        if res_mode.lower()  == "qci":

            gmember = db_session.query(Gmember).filter(
                    (Gmember.gastnr == reslin_list.gastnrmember)).first()

            if gmember and gmember.karteityp > 0:
                msg_str = msg_str + chr(2) + "&W" + translateExtended ("Do not forget to CHANGE the guest name.", lvcarea, "")

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 253)).first()

            if htparam.flogical:

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 87)).first()

                if reslin_list.ankunft < htparam.fdate:
                    flag1 = True
                    ci_date1 = htparam.fdate

        if reslin_list.erwachs != 0 and reslin_list.zipreis == 0:

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                    (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == reslin_list.resnr) &  (Reslin_queasy.reslinnr == reslin_list.reslinnr)).first()

            if not reslin_queasy:
                msg_str = msg_str + chr(2) + "&Q" +\
                        translateExtended ("RoomRate  ==  0, change it?", lvcarea, "") + chr(10)
                error_number = None


        still_error = False

    def check_bedsetup():

        nonlocal error_number, still_error, msg_str, pswd_str, flag1, ci_date1, lvcarea, ci_date, min_stay, max_stay, min_adv, max_adv, msg_str1, zinr_ecode, res_line, bediener, arrangement, guest, htparam, zimkateg, segment, waehrung, bill, bill_line, zimmer, outorder, guest_pr, ratecode, reslin_queasy, kontline, zimplan, queasy
        nonlocal rline, arr, gmember, res_line1, zimplan1, resline, res_line2, res_line3


        nonlocal reslin_list, prev_resline, now_resline, rline, arr, gmember, res_line1, zimplan1, resline, res_line2, res_line3
        nonlocal reslin_list_list, prev_resline_list, now_resline_list

        if reslin_list.setup != 0:

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zikatnr == zimkateg.zikatnr) &  (Zimmer.setup == reslin_list.setup)).first()

            if not zimmer:
                msg_str = msg_str + chr(2) +\
                        translateExtended ("Bed Setup not found, click HELP_Button to choose", lvcarea, "")
                error_number = 31


            else:
                error_number = 32

            return
        else:
            msg_str = msg_str + chr(2) +\
                    translateExtended ("Bed Setup not found, click HELP_Button to choose", lvcarea, "")
            error_number = 31

    def assign_zinr(resline_recid:int, ankunft:date, abreise:date, zinr:str, resstatus:int, gastnrmember:int, bemerk:str, name:str):

        nonlocal error_number, still_error, msg_str, pswd_str, flag1, ci_date1, lvcarea, ci_date, min_stay, max_stay, min_adv, max_adv, msg_str1, zinr_ecode, res_line, bediener, arrangement, guest, htparam, zimkateg, segment, waehrung, bill, bill_line, zimmer, outorder, guest_pr, ratecode, reslin_queasy, kontline, zimplan, queasy
        nonlocal rline, arr, gmember, res_line1, zimplan1, resline, res_line2, res_line3


        nonlocal reslin_list, prev_resline, now_resline, rline, arr, gmember, res_line1, zimplan1, resline, res_line2, res_line3
        nonlocal reslin_list_list, prev_resline_list, now_resline_list

        room_blocked = False
        sharer:bool = False
        curr_datum:date = None
        beg_datum:date = None
        res_recid:int = 0

        def generate_inner_output():
            return room_blocked
        Res_line1 = Res_line
        Zimplan1 = Zimplan
        Resline = Res_line

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 87)).first()
        sharer = (resstatus == 11) or (resstatus == 13)

        if zinr != "" and not sharer:

            if res_mode.lower()  == "inhouse":
                beg_datum = htparam.fdate
            else:
                beg_datum = ankunft
            room_blocked = False
            for curr_datum in range(beg_datum,(abreise - 1)  + 1) :

                zimplan1 = db_session.query(Zimplan1).filter(
                        (Zimplan1.datum == curr_datum) &  (func.lower(Zimplan1.(zinr).lower()) == (zinr).lower())).first()

                if (not zimplan1) and (not room_blocked):
                    zimplan = Zimplan()
                    db_session.add(zimplan)

                    zimplan.datum = curr_datum
                    zimplan.zinr = zinr
                    zimplan.res_recid = resline_recid
                    zimplan.gastnrmember = gastnrmember
                    zimplan.bemerk = bemerk
                    zimplan.resstatus = resstatus
                    zimplan.name = name

                    zimplan = db_session.query(Zimplan).first()

                else:

                    if zimplan1 and (zimplan1.res_recid != resline_recid):

                        resline = db_session.query(Resline).filter(
                                (Resline._recid == zimplan1.res_recid)).first()

                        if resline and resline.(zinr).lower().lower()  == (zinr).lower()  and resline.active_flag < 2 and resline.ankunft <= zimplan1.datum and resline.abreise > zimplan1.datum:
                            curr_datum = abreise
                            room_blocked = True
                        else:

                            zimplan1 = db_session.query(Zimplan1).first()
                            zimplan1.res_recid = resline_recid
                            zimplan1.gastnrmember = gastnrmember
                            zimplan1.bemerk = bemerk
                            zimplan1.resstatus = resstatus
                            zimplan1.name = name

                            zimplan1 = db_session.query(Zimplan1).first()


            if room_blocked:
                for curr_datum in range(beg_datum,(abreise - 1)  + 1) :

                    zimplan = db_session.query(Zimplan).filter(
                            (Zimplan.datum == curr_datum) &  (func.lower(Zimplan.(zinr).lower()) == (zinr).lower()) &  (Zimplan.res_recid == resline_recid)).first()

                    if zimplan:
                        db_session.delete(zimplan)

                        zimplan = db_session.query(Zimplan).first()

                msg_str = msg_str + chr(2) + translateExtended ("Room Number", lvcarea, "") + " " + zinr + " " + translateExtended ("already blocked.", lvcarea, "") + chr(10) + translateExtended ("Room assignment not possible.", lvcarea, "")
            else:

                if resstatus == 6 or resstatus == 13:

                    zimmer = db_session.query(Zimmer).filter(
                            (func.lower(Zimmer.(zinr).lower()) == (zinr).lower())).first()

                    if abreise > htparam.fdate and zimmer.zistatus == 0:
                        zimmer.zistatus = 5

                    elif abreise > htparam.fdate and zimmer.zistatus == 3:
                        zimmer.zistatus = 4
                    else:

                        if abreise == htparam.fdate:

                            res_line1 = db_session.query(Res_line1).filter(
                                    (Res_line1._recid != resline_recid) &  (Res_line1.abreise == abreise) &  (Res_line1.zinr == zimmer.zinr) &  ((Res_line1.resstatus == 6) |  (Res_line1.resstatus == 13))).first()

                            if not res_line1:
                                zimmer.zistatus = 3

                    zimmer = db_session.query(Zimmer).first()

        return generate_inner_output()

    def release_zinr(new_zinr:str):

        nonlocal error_number, still_error, msg_str, pswd_str, flag1, ci_date1, lvcarea, ci_date, min_stay, max_stay, min_adv, max_adv, msg_str1, zinr_ecode, res_line, bediener, arrangement, guest, htparam, zimkateg, segment, waehrung, bill, bill_line, zimmer, outorder, guest_pr, ratecode, reslin_queasy, kontline, zimplan, queasy
        nonlocal rline, arr, gmember, res_line1, zimplan1, resline, res_line2, res_line3


        nonlocal reslin_list, prev_resline, now_resline, rline, arr, gmember, res_line1, zimplan1, resline, res_line2, res_line3
        nonlocal reslin_list_list, prev_resline_list, now_resline_list

        res_recid1:int = 0
        beg_datum:date = None
        answer:bool = False
        parent_nr:int = 0
        Res_line1 = Res_line
        Res_line2 = Res_line
        Res_line3 = Res_line
        Rline = Res_line

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 87)).first()

        rline = db_session.query(Rline).filter(
                (Rline.resnr == resnr) &  (Rline.reslinnr == reslinnr)).first()

        if rline.zinr != "":
            beg_datum = rline.ankunft
            res_recid1 = 0

            if res_mode.lower()  == "delete" or res_mode.lower()  == "cancel" and rline.resstatus == 1:

                res_line1 = db_session.query(Res_line1).filter(
                        (Res_line1.resnr == reslin_list.resnr) &  (Res_line1.zinr == rline.zinr) &  (Res_line1.resstatus == 11)).first()

                if res_line1:

                    res_line1 = db_session.query(Res_line1).first()
                    res_line1.resstatus = 1

                    res_line1 = db_session.query(Res_line1).first()
                    res_recid1 = res_line1._recid

        if res_mode.lower()  == "inhouse":
            answer = True
            beg_datum = htparam.fdate

            if rline.resstatus == 6 and (rline.zinr != new_zinr):

                res_line1 = db_session.query(Res_line1).filter(
                        (Res_line1.resnr == reslin_list.resnr) &  (Res_line1.zinr == rline.zinr) &  (Res_line1.resstatus == 13)).first()

                if res_line1:

                    for res_line3 in db_session.query(Res_line3).filter(
                            (Res_line3.resnr == resnr) &  (Res_line3.zinr == rline.zinr) &  (Res_line3.resstatus == 13)).all():

                        res_line2 = db_session.query(Res_line2).filter(
                                (Res_line2._recid == res_line3._recid)).first()

                        if res_line2:

                            bill = db_session.query(Bill).filter(
                                    (Bill.resnr == res_line2.resnr) &  (Bill.reslinnr == res_line2.reslinnr) &  (Bill.flag == 0) &  (Bill.zinr == res_line2.zinr)).first()
                            bill.zinr = new_zinr
                            parent_nr = bill.parent_nr

                            bill = db_session.query(Bill).first()

                            for bill in db_session.query(Bill).filter(
                                    (Bill.resnr == res_line2.resnr) &  (Bill.parent_nr == parent_nr) &  (Bill.flag == 0) &  (Bill.zinr == res_line2.zinr)).all():
                                bill.zinr = new_zinr

                            res_line2.zinr = new_zinr

                            res_line2 = db_session.query(Res_line2).first()

                    zimmer = db_session.query(Zimmer).filter(
                            (Zimmer.zinr == rline.zinr)).first()
                    zimmer.zistatus = 2

                    zimmer = db_session.query(Zimmer).first()

    def check_min_maxstay():

        nonlocal error_number, still_error, msg_str, pswd_str, flag1, ci_date1, lvcarea, ci_date, min_stay, max_stay, min_adv, max_adv, msg_str1, zinr_ecode, res_line, bediener, arrangement, guest, htparam, zimkateg, segment, waehrung, bill, bill_line, zimmer, outorder, guest_pr, ratecode, reslin_queasy, kontline, zimplan, queasy
        nonlocal rline, arr, gmember, res_line1, zimplan1, resline, res_line2, res_line3


        nonlocal reslin_list, prev_resline, now_resline, rline, arr, gmember, res_line1, zimplan1, resline, res_line2, res_line3
        nonlocal reslin_list_list, prev_resline_list, now_resline_list

        error_flag1:int = 0
        error_flag2:int = 0
        error_flag3:int = 0
        error_flag4:int = 0
        i:int = 0
        prev_contcode:str = ""
        prev_origcode:str = ""
        str:str = ""

        arr = db_session.query(Arr).filter(
                (Arr.arrangement == reslin_list.arrangement)).first()

        if arr:
            min_stay = arr.intervall

        if contcode != "":

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 2) &  (func.lower(Queasy.char1) == (contcode).lower())).first()

            if queasy and queasy.number2 > min_stay:
                min_stay = queasy.number2

            if queasy:
                max_stay = queasy.deci2
                min_adv = queasy.number3
                max_adv = queasy.deci3

        if origcontcode != "":

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 2) &  (func.lower(Queasy.char1) == (origcontcode).lower())).first()

            if queasy and queasy.number2 > min_stay:
                min_stay = queasy.number2

            if queasy:
                max_stay = queasy.deci2
                min_adv = queasy.number3
                max_adv = queasy.deci3

        if min_stay > (reslin_list.abreise - reslin_list.ankunft):

            if substring(res_mode.lower() , 0, 3) == "new" or res_mode.lower()  == "insert" or res_mode.lower()  == "qci":
                error_flag1 = 2
            else:
                error_flag1 = 1
                for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 6) == "$CODE$":
                        prev_contcode = substring(str, 6)

                    if substring(str, 0, 10) == "$OrigCode$":
                        prev_origcode = substring(str, 10)

                if reslin_list.abreise != res_line.abreise or reslin_list.ankunft != res_line.ankunft:
                    error_flag1 = 2

                elif reslin_list.arrangement != res_line.arrangement:
                    error_flag1 = 2

                elif prev_contcode.lower()  != (contcode).lower() :
                    error_flag1 = 2

                elif prev_origcode != origcontcode:
                    error_flag1 = 2

        if max_stay != 0 and max_stay < (reslin_list.abreise - reslin_list.ankunft):

            if substring(res_mode.lower() , 0, 3) == "new" or res_mode.lower()  == "insert" or res_mode.lower()  == "qci":
                error_flag2 = 2
            else:
                error_flag2 = 3
                for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 6) == "$CODE$":
                        prev_contcode = substring(str, 6)

                    if substring(str, 0, 10) == "$OrigCode$":
                        prev_origcode = substring(str, 10)

                if reslin_list.abreise != res_line.abreise or reslin_list.ankunft != res_line.ankunft:
                    error_flag2 = 4

                elif reslin_list.arrangement != res_line.arrangement:
                    error_flag2 = 2

                elif prev_contcode.lower()  != (contcode).lower() :
                    error_flag2 = 2

                elif prev_origcode != origcontcode:
                    error_flag2 = 2

        if min_adv != 0 and (substring(res_mode.lower() , 0, 3) == "new" or res_mode.lower()  == "insert" or res_mode.lower()  == "qci"):

            if (reslin_list.ankunft - ci_date) < min_adv:
                error_flag3 = 2

        if max_adv != 0 and (substring(res_mode.lower() , 0, 3) == "new" or res_mode.lower()  == "insert" or res_mode.lower()  == "qci"):

            if (reslin_list.ankunft - ci_date) > max_adv:
                error_flag4 = 2

        if error_flag1 == 2:
            msg_str = msg_str + chr(2) + translateExtended ("Booking nights", lvcarea, "") + to_string((reslin_list.abreise - reslin_list.ankunft) , ">>9 ") + translateExtended ("LESS than minimum stay  == ", lvcarea, "") + " " + to_string(min_stay, ">>9")
            error_number = 3

        elif error_flag1 == 1:
            msg_str = msg_str + chr(2) + "&W" + translateExtended ("Booking nights", lvcarea, "") + to_string((reslin_list.abreise - reslin_list.ankunft) , ">>9 ") + chr(10) + translateExtended ("LESS than minimum stay  == ", lvcarea, "") + " " + to_string(min_stay, ">>9")

        if error_flag2 == 2:
            msg_str = msg_str + chr(2) + translateExtended ("Booking nights", lvcarea, "") + to_string((reslin_list.abreise - reslin_list.ankunft) , ">>9 ") + translateExtended ("MORE than maximum stay  == ", lvcarea, "") + " " + to_string(max_stay, ">>9")
            error_number = 3

        elif error_flag2 == 1:
            msg_str = msg_str + chr(2) + "&W" + translateExtended ("Booking nights", lvcarea, "") + to_string((reslin_list.abreise - reslin_list.ankunft) , ">>9 ") + chr(10) + translateExtended ("MORE than maximum stay  == ", lvcarea, "") + " " + to_string(max_stay, ">>9")

        if error_flag3 == 2:
            msg_str = msg_str + chr(2) + translateExtended ("Minimum Advance Booking (in days):", lvcarea, "") + " " + to_string(min_adv)
            error_number = 3

        if error_flag4 == 2:
            msg_str = msg_str + chr(2) + translateExtended ("Maximum Advance Booking (in days):", lvcarea, "") + " " + to_string(max_adv)
            error_number = 3


    zinr_ecode[0] = translateExtended ("Wrong room number for selected room catagory", lvcarea, "")
    zinr_ecode[1] = translateExtended ("Room status: Out_of_order", lvcarea, "")
    zinr_ecode[2] = translateExtended ("Room already blocked", lvcarea, "")
    zinr_ecode[3] = translateExtended ("Room status: Vacant dirty", lvcarea, "")
    zinr_ecode[4] = translateExtended ("Room status: Off_Market", lvcarea, "")
    zinr_ecode[5] = translateExtended ("Room sharer already checked_in.", lvcarea, "")

    reslin_list = query(reslin_list_list, first=True)

    prev_resline = query(prev_resline_list, first=True)

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()
    check_go()

    for zimplan in db_session.query(Zimplan).filter(
                (Zimplan.zinr == rline.zinr) &  (Zimplan.datum >= beg_datum) &  (Zimplan.datum < rline.abreise)).all():

        if res_recid1 != 0:
            zimplan.res_recid = res_recid1
        else:
            db_session.delete(zimplan)

    return generate_output()