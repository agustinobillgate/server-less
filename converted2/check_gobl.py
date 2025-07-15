#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.allot_overbookbl import allot_overbookbl
from functions.check_complimentbl import check_complimentbl
from functions.res_czinrbl import res_czinrbl
from models import Res_line, Arrangement, Bediener, Guest, Htparam, Zimkateg, Segment, Waehrung, Bill, Bill_line, Zimmer, Outorder, Guest_pr, Ratecode, Reslin_queasy, Kontline, Zimplan, Queasy

reslin_list_data, Reslin_list = create_model_like(Res_line)
prev_resline_data, Prev_resline = create_model_like(Res_line)

def check_gobl(pvilanguage:int, user_init:string, gastno:int, res_mode:string, curr_segm:string, curr_source:string, currency:string, zikat_screen:string, memo_zinr:string, guestname:string, origcontcode:string, contcode:string, marknr:int, rm_bcol:int, inactive_flag:bool, reslin_list_data:[Reslin_list], prev_resline_data:[Prev_resline], zikatstr:string):

    prepare_cache ([Res_line, Arrangement, Guest, Htparam, Zimkateg, Segment, Waehrung, Bill, Bill_line, Zimmer, Outorder, Guest_pr, Reslin_queasy, Kontline, Queasy])

    error_number = 0
    still_error = True
    msg_str = ""
    pswd_str = ""
    flag1 = False
    ci_date1 = None
    lvcarea:string = "mk-resline"
    ci_date:date = None
    min_stay:int = 0
    max_stay:int = 0
    min_adv:int = 0
    max_adv:int = 0
    msg_str1:string = ""
    zinr_ecode:List[string] = create_empty_list(6,"")
    res_line = arrangement = bediener = guest = htparam = zimkateg = segment = waehrung = bill = bill_line = zimmer = outorder = guest_pr = ratecode = reslin_queasy = kontline = zimplan = queasy = None

    reslin_list = prev_resline = now_resline = buf_arrangement = None

    now_resline_data, Now_resline = create_model_like(Res_line)

    Buf_arrangement = create_buffer("Buf_arrangement",Arrangement)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_number, still_error, msg_str, pswd_str, flag1, ci_date1, lvcarea, ci_date, min_stay, max_stay, min_adv, max_adv, msg_str1, zinr_ecode, res_line, arrangement, bediener, guest, htparam, zimkateg, segment, waehrung, bill, bill_line, zimmer, outorder, guest_pr, ratecode, reslin_queasy, kontline, zimplan, queasy
        nonlocal pvilanguage, user_init, gastno, res_mode, curr_segm, curr_source, currency, zikat_screen, memo_zinr, guestname, origcontcode, contcode, marknr, rm_bcol, inactive_flag, zikatstr
        nonlocal buf_arrangement


        nonlocal reslin_list, prev_resline, now_resline, buf_arrangement
        nonlocal now_resline_data

        return {"error_number": error_number, "still_error": still_error, "msg_str": msg_str, "pswd_str": pswd_str, "zikatstr": zikatstr, "flag1": flag1, "ci_date1": ci_date1}

    def check_go():

        nonlocal error_number, still_error, msg_str, pswd_str, flag1, ci_date1, lvcarea, ci_date, min_stay, max_stay, min_adv, max_adv, msg_str1, zinr_ecode, res_line, arrangement, bediener, guest, htparam, zimkateg, segment, waehrung, bill, bill_line, zimmer, outorder, guest_pr, ratecode, reslin_queasy, kontline, zimplan, queasy
        nonlocal pvilanguage, user_init, gastno, res_mode, curr_segm, curr_source, currency, zikat_screen, memo_zinr, guestname, origcontcode, contcode, marknr, rm_bcol, inactive_flag, zikatstr
        nonlocal buf_arrangement


        nonlocal reslin_list, prev_resline, now_resline, buf_arrangement
        nonlocal now_resline_data

        qty:int = 0
        max_comp:int = 0
        com_rm:int = 0
        max_com:int = 0
        max_rate:Decimal = to_decimal("0.0")
        exchg_rate:Decimal = 1
        check_allotment:bool = False
        its_wrong:bool = False
        wrong_room:bool = False
        datum:date = None
        from_date:date = None
        to_date:date = None
        diff_str:string = ""
        error_code:int = 0
        incl_allotment:bool = False
        b_dummy:bool = False
        overbook:bool = False
        overmax:bool = False
        overanz:int = 0
        overdate:date = None
        billdate:date = None
        tmp_date:date = None
        rline = None
        gmember = None
        Rline =  create_buffer("Rline",Res_line)
        Gmember =  create_buffer("Gmember",Guest)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        billdate = htparam.fdate

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1108)]})
        max_rate =  to_decimal(htparam.fdecimal)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
        ci_date = htparam.fdate

        res_line = get_cache (Res_line, {"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, reslin_list.reslinnr)]})

        if not res_line:

            return

        if res_mode.lower()  == ("inhouse").lower()  and res_line:

            if res_line.resstatus == 8:
                msg_str = translateExtended ("Guest in this reservation already C/O. Update not possible.", lvcarea, "")
                error_number = 51

                return

        if res_mode.lower()  == ("new").lower()  or res_mode.lower()  == ("insert").lower()  or res_mode.lower()  == ("qci").lower() :
            qty = reslin_list.zimmeranz
        else:

            if res_mode.lower()  == ("inhouse").lower() :
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

        if (res_mode.lower()  == ("inhouse").lower()  or res_mode.lower()  == ("qci").lower()) and reslin_list.zinr == "":
            msg_str = translateExtended ("Room Number not yet selected.", lvcarea, "")
            error_number = 30

            return

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, reslin_list.arrangement)]})

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

        zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, zikatstr)]})

        if not zimkateg:
            msg_str = translateExtended ("No such Room Type.", lvcarea, "")
            error_number = 43

            return

        if (reslin_list.active_flag == 0) and (reslin_list.ankunft < ci_date):
            msg_str = translateExtended ("Wrong check-in date!", lvcarea, "")
            error_number = 2

            return

        if reslin_list.abreise < ci_date:
            msg_str = translateExtended ("Wrong check-out date!", lvcarea, "")
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

        segment = get_cache (Segment, {"segmentcode": [(eq, to_int(substring(curr_segm, 0, get_index(curr_segm, " "))))]})

        if segment and segment.betriebsnr > 0:

            if reslin_list.erwachs > 0:
                msg_str = translateExtended ("Compliment / HU Segment but adult > 0.", lvcarea, "")
                error_number = 7

                return

            rline = get_cache (Res_line, {"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(ne, reslin_list.reslinnr)],"active_flag": [(le, 1)],"zipreis": [(gt, 0)]})

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

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, reslin_list.betriebsnr)]})
            else:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

                waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

            if waehrung:
                exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

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

            bill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

            if bill:

                bill_line = get_cache (Bill_line, {"rechnr": [(eq, bill.rechnr)],"bill_datum": [(eq, billdate)],"zinr": [(eq, reslin_list.zinr)],"artnr": [(eq, 99)]})

                if bill_line and bill_line.betrag != reslin_list.zipreis:
                    msg_str = translateExtended ("Room charge has been posted for this Rsv.", lvcarea, "")
                    error_number = 46

                    return

        if reslin_list.zimmerfix and reslin_list.resstatus != 13:

            if reslin_list.zinr != "":

                rline = get_cache (Res_line, {"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(ne, reslin_list.reslinnr)],"resstatus": [(eq, 6)],"zinr": [(eq, reslin_list.zinr)]})
                its_wrong = None != rline

                if not its_wrong:

                    rline = get_cache (Res_line, {"zinr": [(eq, reslin_list.zinr)],"active_flag": [(eq, 1)],"resnr": [(ne, reslin_list.resnr)]})
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
            msg_str = translateExtended ("Input incorrect: Adult = 0 but Room-Rate > 0.", lvcarea, "")
            error_number = 18

            return

        if (reslin_list.erwachs == 0 and reslin_list.kind1 == 0 and reslin_list.kind2 == 0 and reslin_list.gratis == 0) and reslin_list.resstatus != 11 and reslin_list.resstatus != 13:
            msg_str = translateExtended ("Input of PAX incorrect.", lvcarea, "")
            error_number = 44

            return

        if reslin_list.gratis > 0 and reslin_list.zipreis > 0:
            msg_str = translateExtended ("Input incorrect: Compliment guest but Room-Rate > 0.", lvcarea, "")
            error_number = 19

            return

        if memo_zinr != "":

            zimmer = get_cache (Zimmer, {"zinr": [(eq, memo_zinr)]})

            if not zimmer:
                msg_str = translateExtended ("Wrong Memo RmNo / no such room number.", lvcarea, "")
                error_number = 20

                return

        if rm_bcol != 15 and reslin_list.zinr == "":
            msg_str = translateExtended ("Off-Market Room number can not be changed.", lvcarea, "")
            error_number = 21

            return

        elif rm_bcol != 15 and reslin_list.ankunft != res_line.ankunft:

            outorder = get_cache (Outorder, {"zinr": [(eq, reslin_list.zinr)],"betriebsnr": [(eq, reslin_list.resnr)]})

            if outorder and outorder.gespstart < outorder.gespend:
                from_date = reslin_list.ankunft - outorder.gespende + timedelta(days=outorder.gespstart)
                to_date = reslin_list.abreise

                if from_date != to_date:

                    rline = db_session.query(Rline).filter(
                             (Rline.active_flag <= 1) & (Rline.resnr != reslin_list.resnr) & (((Rline.ankunft >= from_date) & (Rline.ankunft <= to_date)) | ((Rline.abreise >= from_date) & (Rline.abreise <= to_date)) | ((from_date >= Rline.ankunft) & (to_date <= Rline.abreise))) & (Rline.zinr == reslin_list.zinr)).first()
                else:

                    rline = db_session.query(Rline).filter(
                             (Rline.active_flag <= 1) & (Rline.resnr != reslin_list.resnr) & ((from_date > Rline.ankunft) & (from_date < Rline.abreise)) & (Rline.zinr == reslin_list.zinr)).first()

                if rline:
                    msg_str = translateExtended ("Attention RmNo : ", lvcarea, "") + to_string(rline.zinr) + chr_unicode(10) +\
                            translateExtended ("Reservation exists under ResNo = ", lvcarea, "") +\
                            to_string(rline.resnr) + chr_unicode(10) +\
                            translateExtended ("Guest name = ", lvcarea, "") + rline.name + chr_unicode(10) +\
                            translateExtended ("Arrival / Departure : ", lvcarea, "") +\
                            to_string(rline.ankunft) + " / " + to_string(rline.abreise) + chr_unicode(10)
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

        guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, gastno)]})

        if guest_pr and reslin_list.reserve_int == 0:

            ratecode = get_cache (Ratecode, {"code": [(eq, guest_pr.code)],"startperiode": [(le, reslin_list.ankunft)],"endperiode": [(ge, reslin_list.ankunft)]})

            if ratecode:
                msg_str = translateExtended ("Market Segment not yet defined.", lvcarea, "")
                error_number = 25

                return
        check_min_maxstay()

        if error_number > 0:

            return

        if reslin_list.active_flag == 0:

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, reslin_list.reslinnr)],"date1": [(le, reslin_list.ankunft)],"date2": [(ge, reslin_list.ankunft)]})

            if reslin_queasy and reslin_queasy.char1 != "" and reslin_queasy.char1 != reslin_list.arrangement:
                msg_str = msg_str + chr_unicode(2) +\
                        translateExtended ("Wrong arrangement in AdHoc Rate setup, fix it now.", lvcarea, "")
                error_number = 26

                return

        if reslin_list.active_flag == 1:

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, reslin_list.reslinnr)],"date1": [(le, ci_date)],"date2": [(ge, ci_date)]})

            if reslin_queasy and reslin_queasy.char1 != "" and reslin_queasy.char1 != reslin_list.arrangement:
                msg_str = msg_str + chr_unicode(2) +\
                        translateExtended ("Wrong arrangement in AdHoc Rate setup, fix it now.", lvcarea, "")
                error_number = 26

                return

        if res_mode.lower()  == ("inhouse").lower() :

            rline = get_cache (Res_line, {"active_flag": [(eq, 0)],"zinr": [(eq, reslin_list.zinr)],"ankunft": [(ge, reslin_list.ankunft),(lt, reslin_list.abreise)],"resnr": [(ne, reslin_list.resnr)],"resstatus": [(ne, 11)]})

            if rline:
                msg_str = msg_str + chr_unicode(2) +\
                        translateExtended ("Reservation found for the same room within the period of stay:", lvcarea, "") + chr_unicode(10) +\
                        rline.name + " - " + translateExtended ("RmNo", lvcarea, "") + " " + rline.zinr + chr_unicode(10) +\
                        to_string(rline.ankunft) + " - " + to_string(rline.abreise) + chr_unicode(10)
                error_number = 27

                return
        tmp_date = reslin_list.abreise - timedelta(days=1)

        if reslin_list.ankunft < reslin_list.abreise:

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

            if reslin_queasy:
                for datum in date_range(reslin_list.ankunft,tmp_date) :

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if not reslin_queasy:
                        msg_str = msg_str + chr_unicode(2) +\
                                translateExtended ("Fixed-Rate Period incorrect, re-check it.", lvcarea, "")
                        error_number = 28

                        return

        if reslin_list.ankunft == reslin_list.abreise:

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

            if reslin_queasy:
                datum = reslin_list.abreise

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                if not reslin_queasy:
                    msg_str = msg_str + chr_unicode(2) +\
                            translateExtended ("Fixed-Rate Period incorrect, re-check it.", lvcarea, "")
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

                kontline = get_cache (Kontline, {"kontignr": [(eq, reslin_list.kontignr)]})
            else:

                kontline = get_cache (Kontline, {"kontignr": [(eq, - reslin_list.kontignr)]})

            if kontline and kontline.zikatnr != 0 and (reslin_list.zikatnr != res_line.zikatnr):
                check_allotment = True

        if check_allotment:

            if res_mode.lower()  == ("inhouse").lower() :
                its_wrong, msg_str = get_output(allot_overbookbl(pvilanguage, res_mode, reslin_list.resnr, reslin_list.reslinnr, reslin_list.kontignr, reslin_list.zikatnr, reslin_list.setup, reslin_list.arrangement, reslin_list.erwachs, ci_date, reslin_list.abreise, reslin_list.zimmeranz, user_init))
            else:
                its_wrong, msg_str = get_output(allot_overbookbl(pvilanguage, res_mode, reslin_list.resnr, reslin_list.reslinnr, reslin_list.kontignr, reslin_list.zikatnr, reslin_list.setup, reslin_list.arrangement, reslin_list.erwachs, reslin_list.ankunft, reslin_list.abreise, reslin_list.zimmeranz, user_init))

            if its_wrong:

                if not matches(msg_str,r"*&Q*"):
                    error_number = 29


                else:
                    error_number = 50

                return

        if zikat_screen.lower()  != (zikatstr).lower() :
            check_bedsetup()

            return

        if res_mode.lower()  == ("new").lower()  or res_mode.lower()  == ("insert").lower()  or res_mode.lower()  == ("qci").lower()  or ((res_mode.lower()  == ("modify").lower()  or res_mode.lower()  == ("split").lower()  or res_mode.lower()  == ("inhouse").lower()) and (res_line.zipreis != 0 and reslin_list.zipreis == 0) or (res_line.zimmeranz != reslin_list.zimmeranz)):
            its_wrong, com_rm, max_comp, pswd_str, msg_str = get_output(check_complimentbl(pvilanguage, reslin_list.resnr, reslin_list.reslinnr, reslin_list.gastnr, reslin_list.ankunft, marknr, reslin_list.zikatnr, reslin_list.arrangement, reslin_list.zimmeranz, reslin_list.zipreis))

            if its_wrong or pswd_str != "" or msg_str != "":
                error_number = 33

                return

        if reslin_list.active_flag == 0:

            rline = get_cache (Res_line, {"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, reslin_list.reslinnr)]})

            if rline.active_flag == 1:
                msg_str = msg_str + chr_unicode(2) +\
                        translateExtended ("Guest checked-in, cancel your changes.", lvcarea, "")
                error_number = 35

                return

        if reslin_list.zinr != "":
            zikatstr, error_code, msg_str1 = get_output(res_czinrbl(pvilanguage, reslin_list.ankunft, reslin_list.abreise, (reslin_list.resstatus == 11 or reslin_list.resstatus == 13), reslin_list.resnr, reslin_list.reslinnr, zikatstr, reslin_list.zinr))

            if msg_str1 != "":
                msg_str = msg_str + chr_unicode(2) + msg_str1

            if error_code != 0:
                msg_str = msg_str + chr_unicode(2) +\
                        translateExtended ("Room Assignment not possible.", lvcarea, "") + chr_unicode(10) +\
                        translateExtended (zinr_ecode[- error_code - 1], lvcarea, "")
                error_number = 39

                return
            else:

                if (res_mode.lower()  == ("modify").lower()  or res_mode.lower()  == ("split").lower()):
                    release_zinr(res_line.zinr)

                elif res_mode.lower()  == ("inhouse").lower()  and (reslin_list.zinr != res_line.zinr):
                    release_zinr(res_line.zinr)

                if (res_mode.lower()  == ("modify").lower()  or res_mode.lower()  == ("split").lower()  or res_mode.lower()  == ("new").lower()  or res_mode.lower()  == ("insert").lower()  or res_mode.lower()  == ("qci").lower()  or (res_mode.lower()  == ("inhouse").lower()  and (reslin_list.zinr != res_line.zinr))):
                    wrong_room = assign_zinr(res_line._recid, reslin_list.ankunft, reslin_list.abreise, reslin_list.zinr, reslin_list.resstatus, reslin_list.gastnrmember, reslin_list.bemerk, guestname)

                    if wrong_room:

                        if res_line.zinr != "":
                            b_dummy = assign_zinr(res_line._recid, res_line.ankunft, res_line.abreise, res_line.zinr, res_line.resstatus, res_line.gastnrmember, res_line.bemerk, res_line.name)
                        error_number = 40

                        return

        if res_mode.lower()  == ("qci").lower() :

            gmember = get_cache (Guest, {"gastnr": [(eq, reslin_list.gastnrmember)]})

            if gmember and gmember.karteityp > 0:
                msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("Do not forget to CHANGE the guest name.", lvcarea, "")

            htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})

            if htparam.flogical:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

                if reslin_list.ankunft < htparam.fdate:
                    flag1 = True
                    ci_date1 = htparam.fdate

        if reslin_list.erwachs != 0 and reslin_list.zipreis == 0:

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, reslin_list.reslinnr)]})

            if not reslin_queasy:
                msg_str = msg_str + chr_unicode(2) + "&Q" +\
                        translateExtended ("RoomRate = 0, change it?", lvcarea, "") + chr_unicode(10)
                error_number = None


        still_error = False


    def check_bedsetup():

        nonlocal error_number, still_error, msg_str, pswd_str, flag1, ci_date1, lvcarea, ci_date, min_stay, max_stay, min_adv, max_adv, msg_str1, zinr_ecode, res_line, arrangement, bediener, guest, htparam, zimkateg, segment, waehrung, bill, bill_line, zimmer, outorder, guest_pr, ratecode, reslin_queasy, kontline, zimplan, queasy
        nonlocal pvilanguage, user_init, gastno, res_mode, curr_segm, curr_source, currency, zikat_screen, memo_zinr, guestname, origcontcode, contcode, marknr, rm_bcol, inactive_flag, zikatstr
        nonlocal buf_arrangement


        nonlocal reslin_list, prev_resline, now_resline, buf_arrangement
        nonlocal now_resline_data

        if reslin_list.setup != 0:

            zimmer = get_cache (Zimmer, {"zikatnr": [(eq, zimkateg.zikatnr)],"setup": [(eq, reslin_list.setup)]})

            if not zimmer:
                msg_str = msg_str + chr_unicode(2) +\
                        translateExtended ("Bed Setup not found, click HELP-Button to choose", lvcarea, "")
                error_number = 31


            else:
                error_number = 32

            return
        else:
            msg_str = msg_str + chr_unicode(2) +\
                    translateExtended ("Bed Setup not found, click HELP-Button to choose", lvcarea, "")
            error_number = 31


    def assign_zinr(resline_recid:int, ankunft:date, abreise:date, zinr:string, resstatus:int, gastnrmember:int, bemerk:string, name:string):

        nonlocal error_number, still_error, msg_str, pswd_str, flag1, ci_date1, lvcarea, ci_date, min_stay, max_stay, min_adv, max_adv, msg_str1, zinr_ecode, res_line, arrangement, bediener, guest, htparam, zimkateg, segment, waehrung, bill, bill_line, zimmer, outorder, guest_pr, ratecode, reslin_queasy, kontline, zimplan, queasy
        nonlocal pvilanguage, user_init, gastno, res_mode, curr_segm, curr_source, currency, zikat_screen, memo_zinr, guestname, origcontcode, contcode, marknr, rm_bcol, inactive_flag, zikatstr
        nonlocal buf_arrangement


        nonlocal reslin_list, prev_resline, now_resline, buf_arrangement
        nonlocal now_resline_data

        room_blocked = False
        sharer:bool = False
        curr_datum:date = None
        beg_datum:date = None
        tmp_datum:date = None
        res_recid:int = 0
        res_line1 = None
        zimplan1 = None
        resline = None

        def generate_inner_output():
            return (room_blocked)

        Res_line1 =  create_buffer("Res_line1",Res_line)
        Zimplan1 =  create_buffer("Zimplan1",Zimplan)
        Resline =  create_buffer("Resline",Res_line)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
        sharer = (resstatus == 11) or (resstatus == 13)

        if zinr != "" and not sharer:

            if res_mode.lower()  == ("inhouse").lower() :
                beg_datum = htparam.fdate
            else:
                beg_datum = ankunft
            room_blocked = False
            tmp_datum = abreise - timedelta(days=1)
            for curr_datum in date_range(beg_datum,tmp_datum) :

                zimplan1 = db_session.query(Zimplan1).filter(
                         (Zimplan1.datum == curr_datum) & (Zimplan1.zinr == (zinr).lower())).first()

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
                    pass
                    pass
                else:

                    if zimplan1 and (zimplan1.res_recid != resline_recid):

                        resline = get_cache (Res_line, {"_recid": [(eq, zimplan1.res_recid)]})

                        if resline and resline.zinr.lower()  == (zinr).lower()  and resline.active_flag < 2 and resline.ankunft <= zimplan1.datum and resline.abreise > zimplan1.datum:
                            curr_datum = abreise
                            room_blocked = True
                        else:
                            pass
                            zimplan1.res_recid = resline_recid
                            zimplan1.gastnrmember = gastnrmember
                            zimplan1.bemerk = bemerk
                            zimplan1.resstatus = resstatus
                            zimplan1.name = name
                            pass
                            pass

            if room_blocked:
                tmp_datum = abreise - timedelta(days=1)
                for curr_datum in date_range(beg_datum,tmp_datum) :

                    zimplan = get_cache (Zimplan, {"datum": [(eq, curr_datum)],"zinr": [(eq, zinr)],"res_recid": [(eq, resline_recid)]})

                    if zimplan:
                        db_session.delete(zimplan)
                        pass
                        pass
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Room Number", lvcarea, "") + " " + zinr + " " + translateExtended ("already blocked.", lvcarea, "") + chr_unicode(10) + translateExtended ("Room assignment not possible.", lvcarea, "")
            else:

                if resstatus == 6 or resstatus == 13:

                    zimmer = get_cache (Zimmer, {"zinr": [(eq, zinr)]})

                    if abreise > htparam.fdate and zimmer.zistatus == 0:
                        zimmer.zistatus = 5

                    elif abreise > htparam.fdate and zimmer.zistatus == 3:
                        zimmer.zistatus = 4

                    elif abreise == htparam.fdate:

                        res_line1 = db_session.query(Res_line1).filter(
                                 (Res_line1._recid != resline_recid) & (Res_line1.abreise == abreise) & (Res_line1.zinr == zimmer.zinr) & ((Res_line1.resstatus == 6) | (Res_line1.resstatus == 13))).first()

                        if not res_line1:
                            zimmer.zistatus = 3
                    pass
                    pass

        return generate_inner_output()


    def release_zinr(new_zinr:string):

        nonlocal error_number, still_error, msg_str, pswd_str, flag1, ci_date1, lvcarea, ci_date, min_stay, max_stay, min_adv, max_adv, msg_str1, zinr_ecode, res_line, arrangement, bediener, guest, htparam, zimkateg, segment, waehrung, bill, bill_line, zimmer, outorder, guest_pr, ratecode, reslin_queasy, kontline, zimplan, queasy
        nonlocal pvilanguage, user_init, gastno, res_mode, curr_segm, curr_source, currency, zikat_screen, memo_zinr, guestname, origcontcode, contcode, marknr, rm_bcol, inactive_flag, zikatstr
        nonlocal buf_arrangement


        nonlocal reslin_list, prev_resline, now_resline, buf_arrangement
        nonlocal now_resline_data

        res_recid1:int = 0
        beg_datum:date = None
        answer:bool = False
        parent_nr:int = 0
        res_line1 = None
        res_line2 = None
        res_line3 = None
        rline = None
        Res_line1 =  create_buffer("Res_line1",Res_line)
        Res_line2 =  create_buffer("Res_line2",Res_line)
        Res_line3 =  create_buffer("Res_line3",Res_line)
        Rline =  create_buffer("Rline",Res_line)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

        rline = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

        if rline and rline.zinr != "":
            beg_datum = rline.ankunft
            res_recid1 = 0

            if res_mode.lower()  == ("delete").lower()  or res_mode.lower()  == ("cancel").lower()  and rline.resstatus == 1:

                res_line1 = get_cache (Res_line, {"resnr": [(eq, reslin_list.resnr)],"zinr": [(eq, rline.zinr)],"resstatus": [(eq, 11)]})

                if res_line1:
                    pass
                    res_line1.resstatus = 1
                    pass
                    res_recid1 = res_line1._recid

            if res_mode.lower()  == ("inhouse").lower() :
                answer = True
                beg_datum = htparam.fdate

                if rline.resstatus == 6 and (rline.zinr.lower()  != (new_zinr).lower()):

                    res_line1 = get_cache (Res_line, {"resnr": [(eq, reslin_list.resnr)],"zinr": [(eq, rline.zinr)],"resstatus": [(eq, 13)]})

                    if res_line1:

                        for res_line3 in db_session.query(Res_line3).filter(
                                 (Res_line3.resnr == res_line.resnr) & (Res_line3.zinr == rline.zinr) & (Res_line3.resstatus == 13)).order_by(Res_line3._recid).all():

                            res_line2 = get_cache (Res_line, {"_recid": [(eq, res_line3._recid)]})

                            if res_line2:

                                bill = get_cache (Bill, {"resnr": [(eq, res_line2.resnr)],"reslinnr": [(eq, res_line2.reslinnr)],"flag": [(eq, 0)],"zinr": [(eq, res_line2.zinr)]})
                                bill.zinr = new_zinr
                                parent_nr = bill.parent_nr
                                pass

                                for bill in db_session.query(Bill).filter(
                                         (Bill.resnr == res_line2.resnr) & (Bill.parent_nr == parent_nr) & (Bill.flag == 0) & (Bill.zinr == res_line2.zinr)).order_by(Bill._recid).all():
                                    bill.zinr = new_zinr
                                    pass
                                res_line2.zinr = new_zinr
                                pass

                        zimmer = get_cache (Zimmer, {"zinr": [(eq, rline.zinr)]})
                        zimmer.zistatus = 2
                        pass

            for zimplan in db_session.query(Zimplan).filter(
                         (Zimplan.zinr == rline.zinr) & (Zimplan.datum >= beg_datum) & (Zimplan.datum < rline.abreise)).order_by(Zimplan._recid).all():

                if res_recid1 != 0:
                    zimplan.res_recid = res_recid1
                else:
                    db_session.delete(zimplan)


    def check_min_maxstay():

        nonlocal error_number, still_error, msg_str, pswd_str, flag1, ci_date1, lvcarea, ci_date, min_stay, max_stay, min_adv, max_adv, msg_str1, zinr_ecode, res_line, arrangement, bediener, guest, htparam, zimkateg, segment, waehrung, bill, bill_line, zimmer, outorder, guest_pr, ratecode, reslin_queasy, kontline, zimplan, queasy
        nonlocal pvilanguage, user_init, gastno, res_mode, curr_segm, curr_source, currency, zikat_screen, memo_zinr, guestname, origcontcode, contcode, marknr, rm_bcol, inactive_flag, zikatstr
        nonlocal buf_arrangement


        nonlocal reslin_list, prev_resline, now_resline, buf_arrangement
        nonlocal now_resline_data

        error_flag1:int = 0
        error_flag2:int = 0
        error_flag3:int = 0
        error_flag4:int = 0
        i:int = 0
        prev_contcode:string = ""
        prev_origcode:string = ""
        str:string = ""
        num_day:int = 0

        buf_arrangement = get_cache (Arrangement, {"arrangement": [(eq, reslin_list.arrangement)]})

        if buf_arrangement:
            min_stay = buf_arrangement.intervall

        if contcode != "":

            queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, contcode)]})

            if queasy and queasy.number2 > min_stay:
                min_stay = queasy.number2

            if queasy:
                max_stay = queasy.deci2
                min_adv = queasy.number3
                max_adv = queasy.deci3

        if origcontcode != "":

            queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, origcontcode)]})

            if queasy and queasy.number2 > min_stay:
                min_stay = queasy.number2

            if queasy:
                max_stay = queasy.deci2
                min_adv = queasy.number3
                max_adv = queasy.deci3


        num_day = (reslin_list.abreise - reslin_list.ankunft).days

        if min_stay > num_day:

            if substring(res_mode.lower() , 0, 3) == ("new").lower()  or res_mode.lower()  == ("insert").lower()  or res_mode.lower()  == ("qci").lower() :
                error_flag1 = 2
            else:
                error_flag1 = 1
                for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 6) == ("$CODE$").lower() :
                        prev_contcode = substring(str, 6)

                    if substring(str, 0, 10) == ("$OrigCode$").lower() :
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

            if substring(res_mode.lower() , 0, 3) == ("new").lower()  or res_mode.lower()  == ("insert").lower()  or res_mode.lower()  == ("qci").lower() :
                error_flag2 = 2
            else:
                error_flag2 = 3
                for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 6) == ("$CODE$").lower() :
                        prev_contcode = substring(str, 6)

                    if substring(str, 0, 10) == ("$OrigCode$").lower() :
                        prev_origcode = substring(str, 10)

                if reslin_list.abreise != res_line.abreise or reslin_list.ankunft != res_line.ankunft:
                    error_flag2 = 4

                elif reslin_list.arrangement != res_line.arrangement:
                    error_flag2 = 2

                elif prev_contcode.lower()  != (contcode).lower() :
                    error_flag2 = 2

                elif prev_origcode != origcontcode:
                    error_flag2 = 2

        if min_adv != 0 and (substring(res_mode.lower() , 0, 3) == ("new").lower()  or res_mode.lower()  == ("insert").lower()  or res_mode.lower()  == ("qci").lower()):

            if (reslin_list.ankunft - ci_date) < min_adv:
                error_flag3 = 2

        if max_adv != 0 and (substring(res_mode.lower() , 0, 3) == ("new").lower()  or res_mode.lower()  == ("insert").lower()  or res_mode.lower()  == ("qci").lower()):

            if (reslin_list.ankunft - ci_date) > max_adv:
                error_flag4 = 2

        if error_flag1 == 2:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Booking nights", lvcarea, "") + to_string((reslin_list.abreise - reslin_list.ankunft) , ">>9 ") + translateExtended ("LESS than minimum stay =", lvcarea, "") + " " + to_string(min_stay, ">>9")
            error_number = 3

        elif error_flag1 == 1:
            msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("Booking nights", lvcarea, "") + to_string((reslin_list.abreise - reslin_list.ankunft) , ">>9 ") + chr_unicode(10) + translateExtended ("LESS than minimum stay =", lvcarea, "") + " " + to_string(min_stay, ">>9")

        if error_flag2 == 2:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Booking nights", lvcarea, "") + to_string((reslin_list.abreise - reslin_list.ankunft) , ">>9 ") + translateExtended ("MORE than maximum stay =", lvcarea, "") + " " + to_string(max_stay, ">>9")
            error_number = 3

        elif error_flag2 == 1:
            msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("Booking nights", lvcarea, "") + to_string((reslin_list.abreise - reslin_list.ankunft) , ">>9 ") + chr_unicode(10) + translateExtended ("MORE than maximum stay =", lvcarea, "") + " " + to_string(max_stay, ">>9")

        if error_flag3 == 2:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Minimum Advance Booking (in days):", lvcarea, "") + " " + to_string(min_adv)
            error_number = 3

        if error_flag4 == 2:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Maximum Advance Booking (in days):", lvcarea, "") + " " + to_string(max_adv)
            error_number = 3

    zinr_ecode[0] = translateExtended ("Wrong room number for selected room catagory", lvcarea, "")
    zinr_ecode[1] = translateExtended ("Room status: Out-of-order", lvcarea, "")
    zinr_ecode[2] = translateExtended ("Room already blocked", lvcarea, "")
    zinr_ecode[3] = translateExtended ("Room status: Vacant dirty", lvcarea, "")
    zinr_ecode[4] = translateExtended ("Room status: Off-Market", lvcarea, "")
    zinr_ecode[5] = translateExtended ("Room sharer already checked-in.", lvcarea, "")

    reslin_list = query(reslin_list_data, first=True)

    prev_resline = query(prev_resline_data, first=True)

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
    check_go()

    return generate_output()