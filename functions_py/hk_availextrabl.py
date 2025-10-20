#using conversion tools version: 1.0.0.117

# =======================================
# Rulita, 20-10-2025 
# Tiket ID : 7AC143 | New compile program
# =======================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Res_line, Htparam, Fixleist, Arrangement, Guest_pr, Argt_line, Genstat, Reslin_queasy, Zwkum

def hk_availextrabl(pvilanguage:int, art_nr:int, fdate:date, tdate:date):

    prepare_cache ([Htparam, Fixleist, Arrangement, Guest_pr, Argt_line, Genstat, Reslin_queasy])

    tmp_extra_data = []
    bdate:date = None
    edate:date = None
    eposdate:date = None
    bill_date:date = None
    bill_fdate:date = None
    bill_tdate:date = None
    curr_zikatnr:int = 0
    rm_rate:Decimal = to_decimal("0.0")
    pax:int = 0
    argt_pax:int = 0
    post_it:bool = False
    argt_betrag:Decimal = to_decimal("0.0")
    argt_found:bool = False
    contcode:string = ""
    ct:string = ""
    ci_date:date = None
    lvcarea:string = "hk-availextra"
    res_line = htparam = fixleist = arrangement = guest_pr = argt_line = genstat = reslin_queasy = zwkum = None

    tmp_resline = tmp_extra = argt_list = None

    tmp_resline_data, Tmp_resline = create_model_like(Res_line)
    tmp_extra_data, Tmp_extra = create_model("Tmp_extra", {"reihe":int, "typ_pos":string, "pos_from":string, "cdate":date, "room":string, "qty":int, "rsvno":int})
    argt_list_data, Argt_list = create_model("Argt_list", {"argtnr":int, "argt_artnr":int, "departement":int, "is_charged":bool, "period":int, "vt_percnt":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tmp_extra_data, bdate, edate, eposdate, bill_date, bill_fdate, bill_tdate, curr_zikatnr, rm_rate, pax, argt_pax, post_it, argt_betrag, argt_found, contcode, ct, ci_date, lvcarea, res_line, htparam, fixleist, arrangement, guest_pr, argt_line, genstat, reslin_queasy, zwkum
        nonlocal pvilanguage, art_nr, fdate, tdate


        nonlocal tmp_resline, tmp_extra, argt_list
        nonlocal tmp_resline_data, tmp_extra_data, argt_list_data

        return {"tmp-extra": tmp_extra_data}

    def create_data():

        nonlocal tmp_extra_data, bdate, edate, eposdate, bill_date, bill_fdate, bill_tdate, curr_zikatnr, rm_rate, pax, argt_pax, post_it, argt_betrag, argt_found, contcode, ct, ci_date, lvcarea, res_line, htparam, fixleist, arrangement, guest_pr, argt_line, genstat, reslin_queasy, zwkum
        nonlocal pvilanguage, art_nr, fdate, tdate


        nonlocal tmp_resline, tmp_extra, argt_list
        nonlocal tmp_resline_data, tmp_extra_data, argt_list_data

        do_it:bool = False
        argtnr:int = 0
        tmp_resline_data.clear()
        tmp_extra_data.clear()

        for res_line in db_session.query(Res_line).filter(
                 (not_ (Res_line.abreise < fdate)) & (not_ (Res_line.ankunft > tdate)) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr).all():
            tmp_resline = Tmp_resline()
            tmp_resline_data.append(tmp_resline)

            buffer_copy(res_line, tmp_resline)

        for tmp_resline in query(tmp_resline_data, sort_by=[("resnr",False)]):

            for fixleist in db_session.query(Fixleist).filter(
                     (Fixleist.resnr == tmp_resline.resnr) & (Fixleist.reslinnr == tmp_resline.reslinnr) & (Fixleist.artnr == art_nr) & (Fixleist.departement == 0)).order_by(Fixleist._recid).all():

                if tmp_resline.ankunft == tmp_resline.abreise:

                    if fixleist.sequenz == 1 or fixleist.sequenz == 2 or fixleist.sequenz == 6:
                        create_tmpextra(0, "Fix-cost line", to_string(fixleist.sequenz), tmp_resline.ankunft, tmp_resline.zinr, fixleist.number)

                    elif fixleist.sequenz == 4:

                        if get_day(tmp_resline.ankunft) == 1:
                            create_tmpextra("Fix-cost line", to_string(fixleist.sequenz), tmp_resline.ankunft, tmp_resline.zinr, fixleist.number)

                    elif fixleist.sequenz == 5:

                        if get_day(tmp_resline.ankunft + 1) == 1:
                            create_tmpextra(0, "Fix-cost line", to_string(fixleist.sequenz), tmp_resline.ankunft, tmp_resline.zinr, fixleist.number)
                else:

                    if fixleist.sequenz == 1 or fixleist.sequenz == 2 or fixleist.sequenz == 4 or fixleist.sequenz == 5:

                        if tmp_resline.ankunft < fdate:
                            bdate = fdate
                        else:
                            bdate = tmp_resline.ankunft

                        if tmp_resline.abreise > tdate:
                            edate = tdate
                        else:
                            edate = tmp_resline.abreise

                    if fixleist.sequenz == 1:
                        while bdate <= edate :

                            if tmp_resline.abreise > bdate:
                                create_tmpextra(0, "Fix-cost line", to_string(fixleist.sequenz), bdate, tmp_resline.zinr, fixleist.number)

                            elif tmp_resline.abreise == bdate and tmp_resline.abreisezeit >= (18 * 3600):
                                create_tmpextra(1, "Dayuse", "1", bdate, tmp_resline.zinr + " " + translateExtended ("DayUse till", lvcarea, "") + " " + to_string(tmp_resline.abreisezeit, "HH:MM"), 0)
                            bdate = bdate + timedelta(days=1)

                    elif fixleist.sequenz == 2:
                        create_tmpextra(0, "Fix-cost line", to_string(fixleist.sequenz), tmp_resline.ankunft, tmp_resline.zinr, fixleist.number)

                    elif fixleist.sequenz == 4:
                        while bdate <= edate :

                            if get_day(bdate) == 1 and tmp_resline.abreise > bdate:
                                create_tmpextra(0, "Fix-cost line", to_string(fixleist.sequenz), bdate, tmp_resline.zinr, fixleist.number)

                            elif get_day(bdate) == 1 and tmp_resline.abreise == bdate and tmp_resline.abreisezeit >= (18 * 3600):
                                create_tmpextra(1, "Dayuse", "1", bdate, tmp_resline.zinr + " " + translateExtended ("DayUse till", lvcarea, "") + " " + to_string(tmp_resline.abreisezeit, "HH:MM"), 0)
                            bdate = bdate + timedelta(days=1)

                    elif fixleist.sequenz == 5:
                        while bdate <= edate :

                            if get_day(bdate + 1) == 1 and tmp_resline.abreise < bdate:
                                create_tmpextra(0, "Fix-cost line", to_string(fixleist.sequenz), bdate, tmp_resline.zinr, fixleist.number)

                            elif get_day(bdate + 1) == 1 and tmp_resline.abreise == bdate and tmp_resline.abreisezeit >= (18 * 3600):
                                create_tmpextra(1, "Dayuse", "1", bdate, tmp_resline.zinr + " " + translateExtended ("DayUse till", lvcarea, "") + " " + to_string(tmp_resline.abreisezeit, "HH:MM"), 0)
                            bdate = bdate + timedelta(days=1)

                    elif fixleist.sequenz == 6:
                        eposdate = (fixleist.lfakt + timedelta(days=fixleist.dekade - 1))

                        if fixleist.lfakt <= fdate:
                            bdate = fdate
                        else:
                            bdate = fixleist.lfakt

                        if eposdate > tdate:
                            edate = tdate

                        elif eposdate <= tdate:

                            if eposdate >= tmp_resline.abreise:
                                edate = tmp_resline.abreise
                            else:
                                edate = eposdate
                        while bdate <= edate :

                            if tmp_resline.abreise > bdate:
                                create_tmpextra(0, "Fix-cost line", to_string(fixleist.sequenz), bdate, tmp_resline.zinr, fixleist.number)

                            elif tmp_resline.abreise == bdate and tmp_resline.abreisezeit >= (18 * 3600):
                                create_tmpextra(1, "Dayuse", "1", bdate, tmp_resline.zinr + " " + translateExtended ("DayUse till", lvcarea, "") + " " + to_string(tmp_resline.abreisezeit, "HH:MM"), 0)
                            bdate = bdate + timedelta(days=1)

            arrangement = get_cache (Arrangement, {"arrangement": [(eq, tmp_resline.arrangement)]})

            if arrangement:
                argtnr = arrangement.argtnr
                contcode = ""

                guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, tmp_resline.gastnr)]})

                if guest_pr:
                    contcode = guest_pr.code
                    ct = tmp_resline.zimmer_wunsch

                    if matches(ct,r"*$CODE$*"):
                        ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                        contcode = substring(ct, 0, get_index(ct, ";") - 1)

            if tmp_resline.ankunft <= fdate:
                bill_fdate = fdate
            else:
                bill_fdate = tmp_resline.ankunft

            if tmp_resline.abreise >= tdate:
                bill_tdate = tdate
            else:
                bill_tdate = tmp_resline.abreise - timedelta(days=1)
            rm_rate =  to_decimal(tmp_resline.zipreis)

            for argt_line in db_session.query(Argt_line).filter(
                     (Argt_line.argtnr == argtnr) & (Argt_line.argt_artnr == art_nr)).order_by(Argt_line._recid).all():
                for bill_date in date_range(tmp_resline.ankunft,(tmp_resline.abreise - 1)) :
                    pax = tmp_resline.erwachs

                    if bill_date < ci_date:
                        rm_rate =  to_decimal(None)

                        genstat = get_cache (Genstat, {"datum": [(eq, bill_date)],"resnr": [(eq, res_line.resnr)],"res_int[0]": [(eq, res_line.reslinnr)]})

                        if genstat:
                            rm_rate =  to_decimal(genstat.zipreis)
                            pax = genstat.erwachs

                    if (bill_date >= ci_date) or rm_rate == None:

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

                        if reslin_queasy:

                            if reslin_queasy.number3 != 0:
                                pax = reslin_queasy.number3

                    if argt_line.vt_percnt == 0:

                        if argt_line.betriebsnr == 0:
                            argt_pax = pax
                        else:
                            argt_pax = argt_line.betriebsnr

                    elif argt_line.vt_percnt == 1:
                        argt_pax = tmp_resline.kind1

                    elif argt_line.vt_percnt == 2:
                        argt_pax = tmp_resline.kind2
                    argt_betrag =  to_decimal(argt_line.betrag)

                    if argt_pax > 0:

                        if argt_line.fakt_modus == 6:

                            argt_list = query(argt_list_data, filters=(lambda argt_list: argt_list.argtnr == argt_line.argtnr and argt_list.departement == argt_line.departement and argt_list.argt_artnr == argt_line.argt_artnr and argt_list.vt_percnt == argt_line.vt_percnt and argt_list.is_charged == argt_line.kind1), first=True)

                            if not argt_list:
                                argt_list = Argt_list()
                                argt_list_data.append(argt_list)

                                argt_list.argtnr = argt_line.argtnr
                                argt_list.departement = argt_line.departement
                                argt_list.argt_artnr = argt_line.argt_artnr
                                argt_list.vt_percnt = argt_line.vt_percnt
                                argt_list.is_charged = argt_line.kind1
                                argt_list.period = 0

                            if argt_list.period < argt_line.intervall:

                                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, tmp_resline.resnr)],"reslinnr": [(eq, tmp_resline.reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, tmp_resline.abreise)],"date2": [(ge, tmp_resline.ankunft)]})

                                if reslin_queasy:

                                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, tmp_resline.resnr)],"reslinnr": [(eq, tmp_resline.reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

                                    if reslin_queasy:
                                        argt_betrag =  to_decimal("0")

                                        if reslin_queasy.char2.lower()  != "" and reslin_queasy.char2.lower()  != ("0").lower() :

                                            zwkum = db_session.query(Zwkum).filter(
                                                     (Zwkum.zknr == artikel.zwkum) & (Zwkum.departement == artikel.departement) & (matches(Zwkum.bezeich,"*DISCOUNT*"))).first()

                                            if zwkum:
                                                argt_betrag =  to_decimal(rm_rate) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal("100") * to_decimal(-1)
                                            else:
                                                argt_betrag =  to_decimal(rm_rate) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal("100")
                                        else:

                                            if reslin_queasy.deci1 != 0 and argt_line.vt_percnt == 0:
                                                argt_betrag =  to_decimal(reslin_queasy.deci1)

                                            elif reslin_queasy.deci2 != 0 and argt_line.vt_percnt == 1:
                                                argt_betrag =  to_decimal(reslin_queasy.deci2)

                                            elif reslin_queasy.deci3 != 0 and argt_line.vt_percnt == 2:
                                                argt_betrag =  to_decimal(reslin_queasy.deci3)
                                        post_it = check_argt_post(argt_line.argt_artnr, argt_line.departement, argt_line.fakt_modus, argt_line.intervall, reslin_queasy.date1, bill_date)
                                    else:
                                        post_it = False
                                else:

                                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, tmp_resline.reserve_int)],"number2": [(eq, argtnr)],"reslinnr": [(eq, curr_zikatnr)],"number3": [(eq, argt_line.argt_artnr)],"resnr": [(eq, argt_line.departement)],"date1": [(le, tmp_resline.abreise)],"date2": [(ge, tmp_resline.ankunft)]})

                                    if reslin_queasy:

                                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, tmp_resline.reserve_int)],"number2": [(eq, argtnr)],"reslinnr": [(eq, curr_zikatnr)],"number3": [(eq, argt_line.argt_artnr)],"resnr": [(eq, argt_line.departement)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

                                        if reslin_queasy:
                                            argt_betrag =  to_decimal("0")

                                            if reslin_queasy.char2.lower()  != "" and reslin_queasy.char2.lower()  != ("0").lower() :

                                                zwkum = db_session.query(Zwkum).filter(
                                                         (Zwkum.zknr == artikel.zwkum) & (Zwkum.departement == artikel.departement) & (matches(Zwkum.bezeich,"*DISCOUNT*"))).first()

                                                if zwkum:
                                                    argt_betrag =  to_decimal(rm_rate) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal("100") * to_decimal(-1)
                                                else:
                                                    argt_betrag =  to_decimal(rm_rate) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal("100")
                                            else:

                                                if reslin_queasy.deci1 != 0 and argt_line.vt_percnt == 0:
                                                    argt_betrag =  to_decimal(reslin_queasy.deci1)

                                                elif reslin_queasy.deci2 != 0 and argt_line.vt_percnt == 1:
                                                    argt_betrag =  to_decimal(reslin_queasy.deci2)

                                                elif reslin_queasy.deci3 != 0 and argt_line.vt_percnt == 2:
                                                    argt_betrag =  to_decimal(reslin_queasy.deci3)
                                            post_it = check_argt_post(argt_line.argt_artnr, argt_line.departement, argt_line.fakt_modus, argt_line.intervall, reslin_queasy.date1, bill_date)
                                        else:
                                            post_it = False
                                    else:
                                        post_it = check_argt_post(argt_line.argt_artnr, argt_line.departement, argt_line.fakt_modus, argt_line.intervall, tmp_resline.ankunft, bill_date)
                            else:
                                post_it = False

                            if post_it  and argt_betrag != 0:

                                if bill_date >= fdate and bill_date <= tdate:
                                    create_tmpextra(art_nr, "argt-line", "0", bill_date, tmp_resline.zinr, argt_pax)
                                argt_list.period = argt_list.period + 1
                        else:

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, tmp_resline.resnr)],"reslinnr": [(eq, tmp_resline.reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, tmp_resline.abreise)],"date2": [(ge, tmp_resline.ankunft)]})

                            if reslin_queasy:

                                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, tmp_resline.resnr)],"reslinnr": [(eq, tmp_resline.reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

                                if reslin_queasy:
                                    argt_betrag =  to_decimal("0")

                                    if reslin_queasy.char2.lower()  != "" and reslin_queasy.char2.lower()  != ("0").lower() :

                                        zwkum = db_session.query(Zwkum).filter(
                                                 (Zwkum.zknr == artikel.zwkum) & (Zwkum.departement == artikel.departement) & (matches(Zwkum.bezeich,"*DISCOUNT*"))).first()

                                        if zwkum:
                                            argt_betrag =  to_decimal(rm_rate) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal("100") * to_decimal(-1)
                                        else:
                                            argt_betrag =  to_decimal(rm_rate) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal("100")
                                    else:

                                        if reslin_queasy.deci1 != 0 and argt_line.vt_percnt == 0:
                                            argt_betrag =  to_decimal(reslin_queasy.deci1)

                                        elif reslin_queasy.deci2 != 0 and argt_line.vt_percnt == 1:
                                            argt_betrag =  to_decimal(reslin_queasy.deci2)

                                        elif reslin_queasy.deci3 != 0 and argt_line.vt_percnt == 2:
                                            argt_betrag =  to_decimal(reslin_queasy.deci3)
                                    post_it = check_argt_post(argt_line.argt_artnr, argt_line.departement, argt_line.fakt_modus, argt_line.intervall, tmp_resline.ankunft, bill_date)
                                else:
                                    post_it = False
                            else:

                                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, tmp_resline.reserve_int)],"number2": [(eq, argtnr)],"reslinnr": [(eq, curr_zikatnr)],"number3": [(eq, argt_line.argt_artnr)],"resnr": [(eq, argt_line.departement)],"date1": [(le, tmp_resline.abreise)],"date2": [(ge, tmp_resline.ankunft)]})

                                if reslin_queasy:

                                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, tmp_resline.reserve_int)],"number2": [(eq, argtnr)],"reslinnr": [(eq, curr_zikatnr)],"number3": [(eq, argt_line.argt_artnr)],"resnr": [(eq, argt_line.departement)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

                                    if reslin_queasy:
                                        argt_betrag =  to_decimal("0")

                                        if reslin_queasy.char2.lower()  != "" and reslin_queasy.char2.lower()  != ("0").lower() :

                                            zwkum = db_session.query(Zwkum).filter(
                                                     (Zwkum.zknr == artikel.zwkum) & (Zwkum.departement == artikel.departement) & (matches(Zwkum.bezeich,"*DISCOUNT*"))).first()

                                            if zwkum:
                                                argt_betrag =  to_decimal(rm_rate) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal("100") * to_decimal(-1)
                                            else:
                                                argt_betrag =  to_decimal(rm_rate) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal("100")
                                        else:

                                            if reslin_queasy.deci1 != 0 and argt_line.vt_percnt == 0:
                                                argt_betrag =  to_decimal(reslin_queasy.deci1)

                                            elif reslin_queasy.deci2 != 0 and argt_line.vt_percnt == 1:
                                                argt_betrag =  to_decimal(reslin_queasy.deci2)

                                            elif reslin_queasy.deci3 != 0 and argt_line.vt_percnt == 2:
                                                argt_betrag =  to_decimal(reslin_queasy.deci3)
                                        post_it = check_argt_post(argt_line.argt_artnr, argt_line.departement, argt_line.fakt_modus, argt_line.intervall, tmp_resline.ankunft, bill_date)
                                    else:
                                        post_it = False
                                else:
                                    post_it = check_argt_post(argt_line.argt_artnr, argt_line.departement, argt_line.fakt_modus, argt_line.intervall, tmp_resline.ankunft, bill_date)

                            if post_it  and argt_betrag != 0 and bill_date >= fdate and bill_date <= tdate:
                                create_tmpextra(art_nr, "argt-line", "0", bill_date, tmp_resline.zinr, argt_pax)


    def create_tmpextra(reihe:int, typ_pos:string, pos_from:string, cdate:date, room:string, qty:int):

        nonlocal tmp_extra_data, bdate, edate, eposdate, bill_date, bill_fdate, bill_tdate, curr_zikatnr, rm_rate, pax, argt_pax, post_it, argt_betrag, argt_found, contcode, ct, ci_date, lvcarea, res_line, htparam, fixleist, arrangement, guest_pr, argt_line, genstat, reslin_queasy, zwkum
        nonlocal pvilanguage, art_nr, fdate, tdate


        nonlocal tmp_resline, tmp_extra, argt_list
        nonlocal tmp_resline_data, tmp_extra_data, argt_list_data


        tmp_extra = Tmp_extra()
        tmp_extra_data.append(tmp_extra)

        tmp_extra.typ_pos = typ_pos
        tmp_extra.pos_from = pos_from
        tmp_extra.cdate = cdate
        tmp_extra.room = room
        tmp_extra.qty = qty
        tmp_extra.reihe = reihe
        tmp_extra.rsvno = tmp_resline.resnr


    def check_argt_post(artnr:int, dept:int, fakt_modus:int, intervall:int, start_date:date, curr_date:date):

        nonlocal tmp_extra_data, bdate, edate, eposdate, bill_date, bill_fdate, bill_tdate, curr_zikatnr, rm_rate, pax, argt_pax, post_it, argt_betrag, argt_found, contcode, ct, ci_date, lvcarea, res_line, htparam, fixleist, arrangement, guest_pr, argt_line, genstat, reslin_queasy, zwkum
        nonlocal pvilanguage, art_nr, fdate, tdate


        nonlocal tmp_resline, tmp_extra, argt_list
        nonlocal tmp_resline_data, tmp_extra_data, argt_list_data

        post_it = False

        def generate_inner_output():
            return (post_it)


        if fakt_modus == 1:
            post_it = True

        elif fakt_modus == 2:

            if start_date == curr_date:
                post_it = True

        elif fakt_modus == 3:

            if (start_date + 1) == curr_date:
                post_it = True

        elif fakt_modus == 4:

            if get_day(curr_date) == 1:
                post_it = True

        elif fakt_modus == 5:

            if get_day(curr_date + 1) == 1:
                post_it = True

        elif fakt_modus == 6:

            if curr_date <= (start_date + timedelta(days=(intervall - 1))) and curr_date >= start_date:
                post_it = True

        return generate_inner_output()


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    create_data()

    return generate_output()