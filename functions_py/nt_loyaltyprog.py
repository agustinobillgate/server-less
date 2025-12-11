
#-----------------------------------------
# Rd 15/8/2025
# erwach -> erwachs
#-----------------------------------------

# ==========================================================
# Rulita, 10-12-2025
# - Added with_for_update before delete query

# Rulita, 11-12-2025
# - Fixing timezone calculation to use local timezone offset
# ==========================================================

from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.htpint import htpint
from functions.calc_servvat import calc_servvat
from models import H_bill_line, Queasy, Nightaudit, Htparam, Nitehist, Guest, Res_line, Mc_guest, Reservation, Segment, Bill_line, Bill, Artikel, Zimkateg, Ratecode, H_bill, H_artikel

from datetime import datetime, timezone, timedelta


def nt_loyaltyprog():
    bill_datum:date = None
    line_nr:int = 0
    serv:decimal = to_decimal("0.0")
    vat:decimal = to_decimal("0.0")
    netto:decimal = to_decimal("0.0")
    serv_betrag:decimal = to_decimal("0.0")
    vat_proz:decimal = 10
    do_it:bool = False
    allocated_point:int = None
    ci_date:date = None
    s_arttype:List[str] = ["Room", "Food", "Beverage", "Other", "other"]
    reihenfolge:int = 0
    outstr:str = ""
    tprice:decimal = to_decimal("0.0")
    tservis:int = 0
    disc_food_art:int = 0
    disc_bev_art:int = 0
    disc_other_art:int = 0
    progname:str = "nt-loyaltyprog.p"
    h_bill_line = queasy = nightaudit = htparam = nitehist = guest = res_line = mc_guest = reservation = segment = bill_line = bill = artikel = zimkateg = ratecode = h_bill = h_artikel = None

    res_list = tline_list = tlist = hbill_list = hbill_buff = bqueasy = bres_list = bres_list = tline_buff = None

    res_list_list, Res_list = create_model("Res_list", {"gastnr":int, "gastpay":int, "resnr":int, "reslinnr":int, "s_reslin":int, "ankunft":date, "abreise":date, "cardnum":str})
    tline_list_list, Tline_list = create_model("Tline_list", {"datum":date, "artnr":int, "arttype":int, "rechnr":int, "reslinnr":int, "s_reslin":int, "dept":int, "bezeich":str, "price":decimal, "email":str, "pax":int, "zeit":int, "checkin":date, "checkout":date, "rcode":str, "rtype":str, "ankzeit":int, "abrezeit":int, "resnr":int, "breslin":int, "gastnr":int, "gastpay":int})
    tlist_list, Tlist = create_model("Tlist", {"departement":int, "rechnr":int, "reslinnr":int, "s_reslin":int, "saldo":decimal, "discount":decimal, "created":str, "pax":int, "usr":str, "checkin":str, "checkout":str, "ankzeit":int, "abrezeit":int, "service":int, "resnr":int, "breslin":int, "gastnr":int, "gastpay":int})
    hbill_list_list, Hbill_list = create_model("Hbill_list", {"dept":int, "rechnr":int, "i_fact":int, "do_it":bool, "tot_sales":decimal, "i_ledger":int, "resnr":int, "reslinnr":int, "pax":int, "cardnum":str}, {"do_it": True, "pax": 1})

    Hbill_buff = create_buffer("Hbill_buff",H_bill_line)
    Bqueasy = create_buffer("Bqueasy",Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_datum, line_nr, serv, vat, netto, serv_betrag, vat_proz, do_it, allocated_point, ci_date, s_arttype, reihenfolge, outstr, tprice, tservis, disc_food_art, disc_bev_art, disc_other_art, progname, h_bill_line, queasy, nightaudit, htparam, nitehist, guest, res_line, mc_guest, reservation, segment, bill_line, bill, artikel, zimkateg, ratecode, h_bill, h_artikel
        nonlocal hbill_buff, bqueasy


        nonlocal res_list, tline_list, tlist, hbill_list, hbill_buff, bqueasy, bres_list, bres_list, tline_buff
        nonlocal res_list_list, tline_list_list, tlist_list, hbill_list_list

        return {}

    def add_line(s:str, bill_date:date):

        nonlocal bill_datum, line_nr, serv, vat, netto, serv_betrag, vat_proz, do_it, allocated_point, ci_date, s_arttype, reihenfolge, outstr, tprice, tservis, disc_food_art, disc_bev_art, disc_other_art, progname, h_bill_line, queasy, nightaudit, htparam, nitehist, guest, res_line, mc_guest, reservation, segment, bill_line, bill, artikel, zimkateg, ratecode, h_bill, h_artikel
        nonlocal hbill_buff, bqueasy


        nonlocal res_list, tline_list, tlist, hbill_list, hbill_buff, bqueasy, bres_list, bres_list, tline_buff
        nonlocal res_list_list, tline_list_list, tlist_list, hbill_list_list


        line_nr = 0

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == bill_date) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            line_nr = line_nr + 1
        nitehist = Nitehist()
        db_session.add(nitehist)

        nitehist.datum = bill_date
        nitehist.reihenfolge = reihenfolge
        nitehist.line_nr = line_nr + 1
        nitehist.line = s


    def fo_point0():

        nonlocal bill_datum, line_nr, serv, vat, netto, serv_betrag, vat_proz, do_it, allocated_point, ci_date, s_arttype, reihenfolge, outstr, tprice, tservis, disc_food_art, disc_bev_art, disc_other_art, progname, h_bill_line, queasy, nightaudit, htparam, nitehist, guest, res_line, mc_guest, reservation, segment, bill_line, bill, artikel, zimkateg, ratecode, h_bill, h_artikel
        nonlocal hbill_buff, bqueasy


        nonlocal res_list, tline_list, tlist, hbill_list, hbill_buff, bqueasy, bres_list, bres_list, tline_buff
        nonlocal res_list_list, tline_list_list, tlist_list, hbill_list_list

        from_date:date = None
        curr_rechnr:int = None
        do_flag:int = 0
        art_type:int = 0
        bill_doflag:bool = False
        bill_cardnum:str = ""
        curr_cardnum:str = ""
        i:int = 0
        str_param:str = ""
        ratecd:str = ""
        sob_number:int = 0
        bguest = None
        Bguest =  create_buffer("Bguest",Guest)

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 278)).first()

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 316)).first()
        sob_number = htparam.finteger

        if sob_number > 0:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.resstatus == 8) & (Res_line.abreise == bill_datum) & (Res_line.erwachs > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.ankunft).all():

                bguest = db_session.query(Bguest).filter(
                         (Bguest.gastnr == res_line.gastnrpay) & (Bguest.karteityp > 0) & (Bguest.segment3 == sob_number)).first()

                if bguest:

                    guest = db_session.query(Guest).filter(
                             (Guest.gastnr == res_line.gastnrmember)).first()

                    mc_guest = db_session.query(Mc_guest).filter(
                             (Mc_guest.gastnr == guest.gastnr) & (Mc_guest.cardnum != "") & (Mc_guest.activeflag)).first()

                    if mc_guest:
                        res_list = Res_list()
                        res_list_list.append(res_list)

                        res_list.gastnr = res_line.gastnrmember
                        res_list.resnr = res_line.resnr
                        res_list.reslinnr = res_line.reslinnr
                        res_list.ankunft = res_line.ankunft
                        res_list.abreise = res_line.abreise
                        res_list.cardnum = mc_guest.cardnum
                        bill_cardnum = mc_guest.cardnum

                        if from_date == None:
                            from_date = res_line.ankunft

        elif queasy:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.resstatus == 8) & (Res_line.abreise == bill_datum) & (Res_line.erwachs > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.ankunft).all():

                reservation = db_session.query(Reservation).filter(
                         (Reservation.resnr == res_line.resnr)).first()

                if reservation:

                    segment = db_session.query(Segment).filter(
                             (Segment.segmentcode == reservation.segmentcode) & (func.lower(not Segment.bezeich).op("~")((("*$$0".lower().replace("*",".*")))))).first()

                    if segment:

                        bqueasy = db_session.query(Bqueasy).filter(
                                 (Bqueasy.key == 316) & (Bqueasy.number1 == segment.segmentcode)).first()

                        if bqueasy:
                            do_it = True
                        else:
                            do_it = False
                    else:
                        do_it = False

                if do_it:

                    guest = db_session.query(Guest).filter(
                             (Guest.gastnr == res_line.gastnrmember)).first()

                    mc_guest = db_session.query(Mc_guest).filter(
                             (Mc_guest.gastnr == guest.gastnr) & (Mc_guest.cardnum != "") & (Mc_guest.activeflag)).first()

                    if mc_guest:
                        res_list = Res_list()
                        res_list_list.append(res_list)

                        res_list.gastnr = res_line.gastnrmember
                        res_list.resnr = res_line.resnr
                        res_list.reslinnr = res_line.reslinnr
                        res_list.ankunft = res_line.ankunft
                        res_list.abreise = res_line.abreise
                        res_list.cardnum = mc_guest.cardnum
                        bill_cardnum = mc_guest.cardnum

                        if from_date == None:
                            from_date = res_line.ankunft
        else:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.resstatus == 8) & (Res_line.abreise == bill_datum) & (Res_line.erwachs > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.ankunft).all():

                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == res_line.gastnrmember)).first()

                mc_guest = db_session.query(Mc_guest).filter(
                         (Mc_guest.gastnr == guest.gastnr) & (Mc_guest.cardnum != "") & (Mc_guest.activeflag)).first()

                if mc_guest:
                    res_list = Res_list()
                    res_list_list.append(res_list)

                    res_list.gastnr = res_line.gastnrmember
                    res_list.resnr = res_line.resnr
                    res_list.reslinnr = res_line.reslinnr
                    res_list.ankunft = res_line.ankunft
                    res_list.abreise = res_line.abreise
                    res_list.cardnum = mc_guest.cardnum
                    bill_cardnum = mc_guest.cardnum

                    if from_date == None:
                        from_date = res_line.ankunft

        if from_date == None:
            from_date = bill_datum
        do_it = False

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.bill_datum >= from_date) & (Bill_line.bill_datum <= bill_datum)).order_by(Bill_line.rechnr).all():

            if curr_rechnr != bill_line.rechnr:
                bill_cardnum = ""
                curr_rechnr = bill_line.rechnr
                bill_doflag = False

                bill = db_session.query(Bill).filter(
                         (Bill.rechnr == bill_line.rechnr)).first()

                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == bill.gastnr)).first()
                pass

                mc_guest = db_session.query(Mc_guest).filter(
                         (Mc_guest.gastnr == guest.gastnr) & (Mc_guest.cardnum != "")).first()

                if bill.resnr > 0 and bill.reslinnr > 0:

                    res_list = query(res_list_list, filters=(lambda res_list: res_list.resnr == bill.resnr and res_list.reslinnr == bill.parent_nr), first=True)
                    bill_doflag = None != res_list

                    if bill_doflag:
                        bill_cardnum = res_list.cardnum
                else:
                    bill_doflag = None != mc_guest and guest.karteityp == 0

                    if bill_doflag:
                        bill_cardnum = mc_guest.cardnum

            artikel = db_session.query(Artikel).filter(
                     (Artikel.artnr == bill_line.artnr) & (Artikel.departement == bill_line.departement)).first()
            do_it = None != artikel

            if do_it:
                do_it = (artikel.artart == 0 or artikel.artart == 8 or artikel.artart == 9 or artikel.artart == 1)

            if do_it:

                if artikel.artart == 9 and artikel.artgrp == 0:

                    res_list = query(res_list_list, filters=(lambda res_list: res_list.resnr == bill_line.massnr and res_list.reslinnr == bill_line.billin_nr), first=True)
                    do_it = None != res_list

                    if do_it:
                        curr_cardnum = res_list.cardnum
                else:

                    if bill.resnr > 0 and bill.reslinnr > 0:
                        do_it = bill_doflag

                        if do_it:
                            curr_cardnum = bill_cardnum

                    elif bill.resnr > 0 and bill.reslinnr == 0:

                        if bill_line.massnr > 0 and bill_line.billin_nr > 0:

                            res_list = query(res_list_list, filters=(lambda res_list: res_list.resnr == bill_line.massnr and res_list.reslinnr == bill_line.billin_nr), first=True)
                            do_it = None != res_list

                            if do_it:
                                curr_cardnum = res_list.cardnum
                        else:
                            do_it = bill_doflag and bill_line.bill_datum == bill_datum

                            if do_it:
                                curr_cardnum = bill_cardnum

                    elif bill_doflag:

                        if bill_line.massnr > 0 and bill_line.billin_nr > 0:

                            res_list = query(res_list_list, filters=(lambda res_list: res_list.resnr == bill_line.massnr and res_list.reslinnr == bill_line.billin_nr), first=True)
                            do_it = None != res_list

                            if do_it:
                                curr_cardnum = bill_cardnum
                        else:
                            do_it = (bill_line.bill_datum == bill_datum)

                            if do_it:
                                curr_cardnum = bill_cardnum

            if do_it and re.match(r".*Remain.*",artikel.bezeich, re.IGNORECASE) and re.match(r".*Balance.*",artikel.bezeich, re.IGNORECASE):
                do_it = False

            if do_it:
                serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, bill_line.bill_datum, artikel.service_code, artikel.mwst_code))

                if serv == 1:
                    art_type = 1

                elif vat == 1:
                    art_type = 1

                elif artikel.artart == 1:
                    art_type = 2

                elif artikel.artart == 8:
                    art_type = 1

                elif artikel.artart == 9:

                    if artikel.artgrp == 0:
                        art_type = 1
                    else:
                        art_type = 5

                elif artikel.artart == 0:

                    if artikel.umsatzart == 1:
                        art_type = 1
                    elif artikel.umsatzart == 2:
                        art_type = 1
                    elif artikel.umsatzart == 4:
                        art_type = 4
                    elif artikel.umsatzart == 5:
                        art_type = 2
                    elif artikel.umsatzart == 6:
                        art_type = 3
                    else:
                        art_type = 4

                if art_type == 5:

                    if bill.resnr > 0 and bill.reslinnr == 0 and bill_line.billin_nr > 0:

                        tline_list = query(tline_list_list, filters=(lambda tline_list: tline_list.rechnr == bill_line.rechnr and tline_list.reslinnr == bill_line.billin_nr and tline_list.arttype == art_type and tline_list.bezeich == bill_line.bezeich), first=True)
                    else:

                        tline_list = query(tline_list_list, filters=(lambda tline_list: tline_list.rechnr == bill_line.rechnr and tline_list.arttype == art_type and tline_list.bezeich == bill_line.bezeich), first=True)

                    if not tline_list:
                        tline_list = Tline_list()
                        tline_list_list.append(tline_list)

                        tline_list.arttype = art_type
                        tline_list.rechnr = bill_line.rechnr
                        tline_list.datum = bill_datum
                        tline_list.zeit = 0
                        tline_list.bezeich = bill_line.bezeich
                        tline_list.dept = 0
                        tline_list.email = curr_cardnum
                        tline_list.pax = 1

                        if bill.resnr > 0 and bill.reslinnr == 0 and bill_line.billin_nr > 0:
                            tline_list.reslinnr = bill_line.billin_nr
                            tline_list.s_reslin = tline_list.reslinnr *\
                                10000000

                        if bill.resnr > 0 and bill.reslinnr > 0:

                            res_line = db_session.query(Res_line).filter(
                                     (Res_line.resnr == bill.resnr) & (Res_line.reslinnr == bill.parent_nr)).first()

                            zimkateg = db_session.query(Zimkateg).filter(
                                     (Zimkateg.zikatnr == res_line.zikatnr)).first()

                            ratecode = db_session.query(Ratecode).filter(
                                     (Ratecode.zikatnr == res_line.zikatnr)).first()
                            for i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
                                str_param = entry(i - 1, res_line.zimmer_wunsch, ";")

                                if re.match(r".*\$CODE\$.*",str_param, re.IGNORECASE):
                                    ratecd = entry(2, str_param, "$")

                            if res_line:
                                tline_list.resnr = res_line.resnr
                                tline_list.reslinnr = res_line.reslinnr
                                tline_list.checkin = res_line.ankunft
                                tline_list.checkout = res_line.abreise
                                tline_list.ankzeit = res_line.ankzeit
                                tline_list.abrezeit = res_line.abreisezeit
                                tline_list.rcode = ratecd
                                tline_list.rtype = zimkateg.kurzbez
                                tline_list.gastnr = res_line.gastnrmember


                    tline_list.price =  to_decimal(tline_list.price) + to_decimal(bill_line.betrag)


                else:

                    if bill.resnr > 0 and bill.reslinnr == 0 and bill_line.billin_nr > 0:

                        tline_list = query(tline_list_list, filters=(lambda tline_list: tline_list.rechnr == bill_line.rechnr and tline_list.reslinnr == bill_line.billin_nr and tline_list.arttype == art_type and tline_list.bezeich == bill_line.bezeich), first=True)
                    else:

                        tline_list = query(tline_list_list, filters=(lambda tline_list: tline_list.rechnr == bill_line.rechnr and tline_list.email.lower()  == (curr_cardnum).lower()  and tline_list.arttype == art_type), first=True)

                    if not tline_list:
                        tline_list = Tline_list()
                        tline_list_list.append(tline_list)

                        tline_list.arttype = art_type
                        tline_list.rechnr = bill_line.rechnr
                        tline_list.datum = bill_datum
                        tline_list.zeit = 0
                        tline_list.bezeich = s_arttype[art_type - 1]
                        tline_list.dept = 0
                        tline_list.email = curr_cardnum

                        if bill.resnr > 0 and bill.reslinnr == 0 and bill_line.billin_nr > 0:
                            tline_list.reslinnr = bill_line.billin_nr
                            tline_list.s_reslin = tline_list.reslinnr *\
                                    10000000

                        if bill.resnr > 0 and bill.reslinnr > 0:

                            res_line = db_session.query(Res_line).filter(
                                     (Res_line.resnr == bill.resnr) & (Res_line.reslinnr == bill.parent_nr)).first()

                            zimkateg = db_session.query(Zimkateg).filter(
                                     (Zimkateg.zikatnr == res_line.zikatnr)).first()

                            ratecode = db_session.query(Ratecode).filter(
                                     (Ratecode.zikatnr == res_line.zikatnr)).first()
                            for i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
                                str_param = entry(i - 1, res_line.zimmer_wunsch, ";")

                                if re.match(r".*\$CODE\$.*",str_param, re.IGNORECASE):
                                    ratecd = entry(2, str_param, "$")

                            if res_line:
                                # Rd 15/8/2025
                                # tline_list.pax = res_line.erwach + res_line.kind1 + res_line.kind2
                                tline_list.pax = res_line.erwachs + res_line.kind1 + res_line.kind2

                                tline_list.resnr = res_line.resnr
                                tline_list.reslinnr = res_line.reslinnr
                                tline_list.checkin = res_line.ankunft
                                tline_list.checkout = res_line.abreise
                                tline_list.ankzeit = res_line.ankzeit
                                tline_list.abrezeit = res_line.abreisezeit
                                tline_list.rcode = ratecd
                                tline_list.rtype = zimkateg.kurzbez
                                tline_list.gastnr = res_line.gastnrmember


                    tline_list.price =  to_decimal(tline_list.price) + to_decimal(bill_line.betrag)


    def fo_point1():

        nonlocal bill_datum, line_nr, serv, vat, netto, serv_betrag, vat_proz, do_it, allocated_point, ci_date, s_arttype, reihenfolge, outstr, tprice, tservis, disc_food_art, disc_bev_art, disc_other_art, progname, h_bill_line, queasy, nightaudit, htparam, nitehist, guest, res_line, mc_guest, reservation, segment, bill_line, bill, artikel, zimkateg, ratecode, h_bill, h_artikel
        nonlocal hbill_buff, bqueasy


        nonlocal res_list, tline_list, tlist, hbill_list, hbill_buff, bqueasy, bres_list, bres_list, tline_buff
        nonlocal res_list_list, tline_list_list, tlist_list, hbill_list_list

        from_date:date = None
        curr_rechnr:int = None
        do_flag:int = 0
        art_type:int = 0
        bill_doflag:bool = False
        bill_cardnum:str = ""
        curr_cardnum:str = ""
        i:int = 0
        str_param:str = ""
        ratecd:str = ""

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resstatus == 8) & (Res_line.abreise == bill_datum) & (Res_line.erwachs > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.ankunft).all():

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == res_line.gastnrpay)).first()

            mc_guest = db_session.query(Mc_guest).filter(
                     (Mc_guest.gastnr == guest.gastnr) & (Mc_guest.cardnum != "") & (Mc_guest.activeflag)).first()

            if mc_guest:
                res_list = Res_list()
                res_list_list.append(res_list)

                res_list.gastnr = res_line.gastnrpay
                res_list.resnr = res_line.resnr
                res_list.reslinnr = res_line.reslinnr
                res_list.ankunft = res_line.ankunft
                res_list.abreise = res_line.abreise
                res_list.cardnum = mc_guest.cardnum
                bill_cardnum = mc_guest.cardnum

                if from_date == None:
                    from_date = res_line.ankunft

        if from_date == None:
            from_date = bill_datum

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.bill_datum >= from_date) & (Bill_line.bill_datum <= bill_datum)).order_by(Bill_line.rechnr).all():

            if curr_rechnr != bill_line.rechnr:
                curr_rechnr = bill_line.rechnr
                bill_doflag = False

                bill = db_session.query(Bill).filter(
                         (Bill.rechnr == bill_line.rechnr)).first()

                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == bill.gastnr)).first()
                pass

                mc_guest = db_session.query(Mc_guest).filter(
                         (Mc_guest.gastnr == guest.gastnr) & (Mc_guest.cardnum != "")).first()

                if bill.resnr > 0 and bill.reslinnr > 0:

                    res_list = query(res_list_list, filters=(lambda res_list: res_list.resnr == bill.resnr and res_list.reslinnr == bill.parent_nr), first=True)
                    bill_doflag = None != res_list
                else:
                    bill_doflag = None != mc_guest and guest.karteityp > 0

                if bill_doflag:
                    bill_cardnum = mc_guest.cardnum

            artikel = db_session.query(Artikel).filter(
                     (Artikel.artnr == bill_line.artnr) & (Artikel.departement == bill_line.departement)).first()
            do_it = None != artikel

            if do_it:
                do_it = (artikel.artart == 0 or artikel.artart == 8 or artikel.artart == 9 or artikel.artart == 1)

            if do_it:

                if bill_line.massnr > 0 and bill_line.billin_nr > 0:

                    res_list = query(res_list_list, filters=(lambda res_list: res_list.resnr == bill_line.massnr and res_list.reslinnr == bill_line.billin_nr), first=True)
                    do_it = None != res_list

                    if do_it:
                        curr_cardnum = bill_cardnum
                else:

                    if bill.resnr > 0 and bill.reslinnr > 0 and bill_doflag:
                        curr_cardnum = bill_cardnum
                    else:
                        do_it = bill_line.bill_datum == bill_datum

                        if do_it:
                            do_it = bill_doflag

                            if do_it:
                                curr_cardnum = bill_cardnum

            if do_it and re.match(r".*Remain.*",artikel.bezeich, re.IGNORECASE) and re.match(r".*Balance.*",artikel.bezeich, re.IGNORECASE):
                do_it = False

            if do_it:
                serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, bill_line.bill_datum, artikel.service_code, artikel.mwst_code))

                if serv == 1:
                    art_type = 1

                elif vat == 1:
                    art_type = 1

                elif artikel.artart == 1:
                    art_type = 2

                elif artikel.artart == 8:
                    art_type = 1

                elif artikel.artart == 9:

                    if artikel.artgrp == 0:
                        art_type = 1
                    else:
                        art_type = 5

                elif artikel.artart == 0:

                    if artikel.umsatzart == 1:
                        art_type = 1
                    elif artikel.umsatzart == 2:
                        art_type = 1
                    elif artikel.umsatzart == 4:
                        art_type = 4
                    elif artikel.umsatzart == 5:
                        art_type = 2
                    elif artikel.umsatzart == 6:
                        art_type = 3
                    else:
                        art_type = 4

                if art_type == 5:

                    tline_list = query(tline_list_list, filters=(lambda tline_list: tline_list.rechnr == bill_line.rechnr and tline_list.arttype == art_type and tline_list.bezeich == bill_line.bezeich), first=True)

                    if not tline_list:
                        tline_list = Tline_list()
                        tline_list_list.append(tline_list)

                        tline_list.arttype = art_type
                        tline_list.rechnr = bill_line.rechnr
                        tline_list.datum = bill_datum
                        tline_list.zeit = 0
                        tline_list.bezeich = bill_line.bezeich
                        tline_list.dept = 0
                        tline_list.email = curr_cardnum
                        tline_list.pax = 1


                    tline_list.price =  to_decimal(tline_list.price) + to_decimal(bill_line.betrag)


                else:

                    tline_list = query(tline_list_list, filters=(lambda tline_list: tline_list.rechnr == bill_line.rechnr and tline_list.arttype == art_type), first=True)

                    if not tline_list:
                        tline_list = Tline_list()
                        tline_list_list.append(tline_list)

                        tline_list.arttype = art_type
                        tline_list.rechnr = bill_line.rechnr
                        tline_list.datum = bill_datum
                        tline_list.zeit = 0
                        tline_list.bezeich = s_arttype[art_type - 1]
                        tline_list.dept = 0
                        tline_list.email = curr_cardnum

                        if bill.resnr > 0 and bill.reslinnr > 0:

                            res_line = db_session.query(Res_line).filter(
                                     (Res_line.resnr == bill.resnr) & (Res_line.reslinnr == bill.parent_nr)).first()

                            zimkateg = db_session.query(Zimkateg).filter(
                                     (Zimkateg.zikatnr == res_line.zikatnr)).first()

                            ratecode = db_session.query(Ratecode).filter(
                                     (Ratecode.zikatnr == res_line.zikatnr)).first()
                            for i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
                                str_param = entry(i - 1, res_line.zimmer_wunsch, ";")

                                if re.match(r".*\$CODE\$.*",str_param, re.IGNORECASE):
                                    ratecd = entry(2, str_param, "$")

                            if res_line:
                                # tline_list.pax = res_line.erwach + res_line.kind1 + res_line.kind2
                                tline_list.pax = res_line.erwachs + res_line.kind1 + res_line.kind2

                                tline_list.reslinnr = res_line.reslinnr
                                tline_list.checkin = res_line.ankunft
                                tline_list.checkout = res_line.abreise
                                tline_list.ankzeit = res_line.ankzeit
                                tline_list.abrezeit = res_line.abreisezeit
                                tline_list.rcode = ratecd
                                tline_list.rtype = zimkateg.kurzbez


                    tline_list.price =  to_decimal(tline_list.price) + to_decimal(bill_line.betrag)


    def fo_point2():

        nonlocal bill_datum, line_nr, serv, vat, netto, serv_betrag, vat_proz, do_it, allocated_point, ci_date, s_arttype, reihenfolge, outstr, tprice, tservis, disc_food_art, disc_bev_art, disc_other_art, progname, h_bill_line, queasy, nightaudit, htparam, nitehist, guest, res_line, mc_guest, reservation, segment, bill_line, bill, artikel, zimkateg, ratecode, h_bill, h_artikel
        nonlocal hbill_buff, bqueasy


        nonlocal res_list, tline_list, tlist, hbill_list, hbill_buff, bqueasy, bres_list, bres_list, tline_buff
        nonlocal res_list_list, tline_list_list, tlist_list, hbill_list_list

        from_date:date = None
        curr_rechnr:int = None
        do_flag:int = 0
        art_type:int = 0
        bill_doflag:bool = False
        bill_cardnum:str = ""
        curr_cardnum:str = ""
        i:int = 0
        str_param:str = ""
        ratecd:str = ""
        sob_number:int = 0
        bguest = None
        Bguest =  create_buffer("Bguest",Guest)
        Bres_list = Res_list
        bres_list_list = res_list_list

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resstatus == 8) & (Res_line.abreise == bill_datum) & (Res_line.erwachs > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.ankunft).all():

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == res_line.gastnrmember)).first()

            mc_guest = db_session.query(Mc_guest).filter(
                     (Mc_guest.gastnr == guest.gastnr) & (Mc_guest.cardnum != "") & (Mc_guest.activeflag)).first()

            if mc_guest:
                res_list = Res_list()
                res_list_list.append(res_list)

                res_list.gastnr = res_line.gastnrmember
                res_list.gastpay = res_line.gastnrpay
                res_list.resnr = res_line.resnr
                res_list.reslinnr = res_line.reslinnr
                res_list.ankunft = res_line.ankunft
                res_list.abreise = res_line.abreise
                res_list.cardnum = mc_guest.cardnum
                bill_cardnum = mc_guest.cardnum

                if from_date == None:
                    from_date = res_line.ankunft

        if from_date == None:
            from_date = bill_datum

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.bill_datum >= from_date) & (Bill_line.bill_datum <= bill_datum)).order_by(Bill_line.rechnr).all():

            if curr_rechnr != bill_line.rechnr:
                bill_cardnum = ""
                curr_rechnr = bill_line.rechnr
                bill_doflag = False

                bill = db_session.query(Bill).filter(
                         (Bill.rechnr == bill_line.rechnr)).first()

                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == bill.gastnr)).first()
                pass

                mc_guest = db_session.query(Mc_guest).filter(
                         (Mc_guest.gastnr == guest.gastnr) & (Mc_guest.cardnum != "") & (Mc_guest.activeflag)).first()

                if bill.resnr > 0 and bill.reslinnr > 0:

                    res_list = query(res_list_list, filters=(lambda res_list: res_list.resnr == bill.resnr and res_list.reslinnr == bill.parent_nr), first=True)
                    bill_doflag = None != res_list

                    if bill_doflag:
                        bill_cardnum = res_list.cardnum
                else:
                    bill_doflag = None != mc_guest and guest.karteityp == 0

                    if bill_doflag:
                        bill_cardnum = mc_guest.cardnum
            else:

                bill = db_session.query(Bill).filter(
                         (Bill.rechnr == bill_line.rechnr)).first()

            if bill_doflag:

                res_list = query(res_list_list, filters=(lambda res_list: res_list.resnr == bill_line.massnr and res_list.reslinnr == bill_line.billin_nr), first=True)

                if not res_list:

                    res_line = db_session.query(Res_line).filter(
                             (Res_line.resnr == bill_line.massnr) & (Res_line.reslinnr == bill_line.billin_nr) & (Res_line.erwachs > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.resstatus == 8)).first()

                    if res_line:

                        mc_guest = db_session.query(Mc_guest).filter(
                                 (Mc_guest.gastnr == res_line.gastnrmember) & (Mc_guest.cardnum != "") & (Mc_guest.activeflag)).first()

                        if mc_guest:
                            res_list = Res_list()
                            res_list_list.append(res_list)

                            res_list.gastnr = res_line.gastnrmember
                            res_list.gastpay = res_line.gastnrpay
                            res_list.resnr = res_line.resnr
                            res_list.reslinnr = res_line.reslinnr
                            res_list.ankunft = res_line.ankunft
                            res_list.abreise = res_line.abreise
                            res_list.cardnum = mc_guest.cardnum

            artikel = db_session.query(Artikel).filter(
                     (Artikel.artnr == bill_line.artnr) & (Artikel.departement == bill_line.departement)).first()
            do_it = None != artikel

            if do_it:
                do_it = (artikel.artart == 0 or artikel.artart == 8 or artikel.artart == 9 or artikel.artart == 1)

            if do_it:

                if artikel.artart == 9 and artikel.artgrp == 0:

                    res_list = query(res_list_list, filters=(lambda res_list: res_list.resnr == bill_line.massnr and res_list.reslinnr == bill_line.billin_nr), first=True)
                    do_it = None != res_list and bill_doflag

                    if do_it:
                        curr_cardnum = res_list.cardnum
                else:

                    if bill.resnr > 0 and bill.reslinnr > 0:
                        do_it = bill_doflag

                        if do_it:
                            curr_cardnum = bill_cardnum

                    elif bill.resnr > 0 and bill.reslinnr == 0:

                        if bill_line.massnr > 0 and bill_line.billin_nr > 0:

                            res_list = query(res_list_list, filters=(lambda res_list: res_list.resnr == bill_line.massnr and res_list.reslinnr == bill_line.billin_nr), first=True)
                            do_it = None != res_list

                            if do_it:
                                curr_cardnum = res_list.cardnum
                        else:
                            do_it = bill_doflag and bill_line.bill_datum == bill_datum

                            if do_it:
                                curr_cardnum = bill_cardnum

                    elif bill_doflag:

                        if bill_line.massnr > 0 and bill_line.billin_nr > 0:

                            res_list = query(res_list_list, filters=(lambda res_list: res_list.resnr == bill_line.massnr and res_list.reslinnr == bill_line.billin_nr), first=True)
                            do_it = None != res_list

                            if do_it:
                                curr_cardnum = bill_cardnum
                        else:
                            do_it = (bill_line.bill_datum == bill_datum)

                            if do_it:
                                curr_cardnum = bill_cardnum

            if do_it and re.match(r".*Remain.*",artikel.bezeich, re.IGNORECASE) and re.match(r".*Balance.*",artikel.bezeich, re.IGNORECASE):
                do_it = False

            if do_it:
                serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, bill_line.bill_datum, artikel.service_code, artikel.mwst_code))

                if serv == 1:
                    art_type = 1

                elif vat == 1:
                    art_type = 1

                elif artikel.artart == 1:
                    art_type = 2

                elif artikel.artart == 8:
                    art_type = 1

                elif artikel.artart == 9:

                    if artikel.artgrp == 0:
                        art_type = 1
                    else:
                        art_type = 5

                elif artikel.artart == 0:

                    if artikel.umsatzart == 1:
                        art_type = 1
                    elif artikel.umsatzart == 2:
                        art_type = 1
                    elif artikel.umsatzart == 4:
                        art_type = 4
                    elif artikel.umsatzart == 5:
                        art_type = 2
                    elif artikel.umsatzart == 6:
                        art_type = 3
                    else:
                        art_type = 4

                if art_type == 5:

                    if bill.resnr > 0 and bill.reslinnr == 0 and bill_line.billin_nr > 0:

                        tline_list = query(tline_list_list, filters=(lambda tline_list: tline_list.rechnr == bill_line.rechnr and tline_list.reslinnr == bill_line.billin_nr and tline_list.arttype == art_type and tline_list.bezeich == bill_line.bezeich), first=True)
                    else:

                        tline_list = query(tline_list_list, filters=(lambda tline_list: tline_list.rechnr == bill_line.rechnr and tline_list.arttype == art_type and tline_list.bezeich == bill_line.bezeich), first=True)

                    if not tline_list:
                        tline_list = Tline_list()
                        tline_list_list.append(tline_list)

                        tline_list.arttype = art_type
                        tline_list.rechnr = bill_line.rechnr
                        tline_list.datum = bill_datum
                        tline_list.zeit = 0
                        tline_list.bezeich = bill_line.bezeich
                        tline_list.dept = 0
                        tline_list.email = curr_cardnum
                        tline_list.pax = 1

                        if bill.resnr > 0 and bill.reslinnr == 0 and bill_line.billin_nr > 0:
                            tline_list.reslinnr = bill_line.billin_nr
                            tline_list.s_reslin = tline_list.reslinnr *\
                                10000000

                        if bill.resnr > 0 and bill.reslinnr > 0 and bill_line.billin_nr > 0:

                            res_line = db_session.query(Res_line).filter(
                                     (Res_line.resnr == bill.resnr) & (Res_line.reslinnr == bill.parent_nr)).first()

                            zimkateg = db_session.query(Zimkateg).filter(
                                     (Zimkateg.zikatnr == res_line.zikatnr)).first()

                            ratecode = db_session.query(Ratecode).filter(
                                     (Ratecode.zikatnr == res_line.zikatnr)).first()
                            for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                                str_param = entry(i - 1, res_line.zimmer_wunsch, ";")

                                if re.match(r".*\$CODE\$.*",str_param, re.IGNORECASE):
                                    ratecd = entry(2, str_param, "$")

                            if res_line:
                                tline_list.reslinnr = res_line.reslinnr
                                tline_list.checkin = res_line.ankunft
                                tline_list.checkout = res_line.abreise
                                tline_list.ankzeit = res_line.ankzeit
                                tline_list.abrezeit = res_line.abreisezeit
                                tline_list.rcode = ratecd
                                tline_list.rtype = zimkateg.kurzbez
                                tline_list.resnr = res_line.resnr
                                tline_list.breslin = bill.reslinnr
                                tline_list.gastnr = res_line.gastnrmember

                    if bill.parent_nr > 0:

                        res_list = query(res_list_list, filters=(lambda res_list: res_list.resnr == bill.resnr and res_list.reslinnr == bill.parent_nr), first=True)
                    else:

                        res_list = query(res_list_list, filters=(lambda res_list: res_list.resnr == bill.resnr), first=True)

                    if res_list:
                        tline_list.gastpay = res_list.gastpay
                    else:
                        tline_list.gastpay = bill.gastnr
                    tline_list.price =  to_decimal(tline_list.price) + to_decimal(bill_line.betrag)


                else:

                    if bill.resnr > 0 and bill.reslinnr == 0 and bill_line.billin_nr > 0:

                        tline_list = query(tline_list_list, filters=(lambda tline_list: tline_list.rechnr == bill_line.rechnr and tline_list.reslinnr == bill_line.billin_nr and tline_list.arttype == art_type and tline_list.bezeich == bill_line.bezeich), first=True)
                    else:

                        tline_list = query(tline_list_list, filters=(lambda tline_list: tline_list.rechnr == bill_line.rechnr and tline_list.resnr == bill_line.massnr and tline_list.reslinnr == bill_line.billin_nr and tline_list.arttype == art_type), first=True)

                    if not tline_list:
                        tline_list = Tline_list()
                        tline_list_list.append(tline_list)

                        tline_list.arttype = art_type
                        tline_list.rechnr = bill_line.rechnr
                        tline_list.datum = bill_datum
                        tline_list.zeit = 0
                        tline_list.bezeich = s_arttype[art_type - 1]
                        tline_list.dept = 0
                        tline_list.email = curr_cardnum

                        if bill.resnr > 0 and bill.reslinnr > 0 and bill_line.billin_nr > 0:

                            if artikel.artart == 9 and artikel.artgrp == 0:

                                res_line = db_session.query(Res_line).filter(
                                         (Res_line.resnr == bill_line.massnr) & (Res_line.reslinnr == bill_line.billin_nr)).first()
                            else:

                                res_line = db_session.query(Res_line).filter(
                                         (Res_line.resnr == bill.resnr) & (Res_line.reslinnr == bill.parent_nr)).first()

                            zimkateg = db_session.query(Zimkateg).filter(
                                     (Zimkateg.zikatnr == res_line.zikatnr)).first()

                            ratecode = db_session.query(Ratecode).filter(
                                     (Ratecode.zikatnr == res_line.zikatnr)).first()
                            for i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
                                str_param = entry(i - 1, res_line.zimmer_wunsch, ";")

                                if re.match(r".*\$CODE\$.*",str_param, re.IGNORECASE):
                                    ratecd = entry(2, str_param, "$")

                            if res_line:
                                # tline_list.pax = res_line.erwach + res_line.kind1 + res_line.kind2
                                tline_list.pax = res_line.erwachs + res_line.kind1 + res_line.kind2

                                tline_list.reslinnr = res_line.reslinnr
                                tline_list.checkin = res_line.ankunft
                                tline_list.checkout = res_line.abreise
                                tline_list.ankzeit = res_line.ankzeit
                                tline_list.abrezeit = res_line.abreisezeit
                                tline_list.rcode = ratecd
                                tline_list.rtype = zimkateg.kurzbez
                                tline_list.resnr = res_line.resnr
                                tline_list.breslin = bill.reslinnr
                                tline_list.gastnr = res_line.gastnrmember

                        elif bill.resnr > 0 and bill.reslinnr == 0 and bill_line.billin_nr > 0:

                            if artikel.artart == 9 and artikel.artgrp == 0:

                                res_line = db_session.query(Res_line).filter(
                                         (Res_line.resnr == bill_line.massnr) & (Res_line.reslinnr == bill_line.billin_nr)).first()
                            else:

                                res_line = db_session.query(Res_line).filter(
                                         (Res_line.resnr == bill.resnr) & (Res_line.reslinnr == bill.parent_nr)).first()

                            zimkateg = db_session.query(Zimkateg).filter(
                                     (Zimkateg.zikatnr == res_line.zikatnr)).first()

                            ratecode = db_session.query(Ratecode).filter(
                                     (Ratecode.zikatnr == res_line.zikatnr)).first()
                            for i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
                                str_param = entry(i - 1, res_line.zimmer_wunsch, ";")

                                if re.match(r".*\$CODE\$.*",str_param, re.IGNORECASE):
                                    ratecd = entry(2, str_param, "$")

                            if res_line:
                                # tline_list.pax = res_line.erwach + res_line.kind1 + res_line.kind2
                                tline_list.pax = res_line.erwachs + res_line.kind1 + res_line.kind2

                                tline_list.checkin = res_line.ankunft
                                tline_list.checkout = res_line.abreise
                                tline_list.ankzeit = res_line.ankzeit
                                tline_list.abrezeit = res_line.abreisezeit
                                tline_list.rcode = ratecd
                                tline_list.rtype = zimkateg.kurzbez
                                tline_list.resnr = res_line.resnr
                                tline_list.breslin = bill.reslinnr
                                tline_list.gastnr = res_line.gastnrmember
                                tline_list.reslinnr = bill_line.billin_nr
                                tline_list.s_reslin = tline_list.reslinnr *\
                                        10000000

                    if bill.parent_nr > 0:

                        res_list = query(res_list_list, filters=(lambda res_list: res_list.resnr == bill.resnr and res_list.reslinnr == bill.parent_nr), first=True)
                    else:

                        res_list = query(res_list_list, filters=(lambda res_list: res_list.resnr == bill.resnr), first=True)

                    if res_list:
                        tline_list.gastpay = res_list.gastpay
                    else:
                        tline_list.gastpay = bill.gastnr
                    tline_list.price =  to_decimal(tline_list.price) + to_decimal(bill_line.betrag)


    def fo_point3():

        nonlocal bill_datum, line_nr, serv, vat, netto, serv_betrag, vat_proz, do_it, allocated_point, ci_date, s_arttype, reihenfolge, outstr, tprice, tservis, disc_food_art, disc_bev_art, disc_other_art, progname, h_bill_line, queasy, nightaudit, htparam, nitehist, guest, res_line, mc_guest, reservation, segment, bill_line, bill, artikel, zimkateg, ratecode, h_bill, h_artikel
        nonlocal hbill_buff, bqueasy


        nonlocal res_list, tline_list, tlist, hbill_list, hbill_buff, bqueasy, bres_list, bres_list, tline_buff
        nonlocal res_list_list, tline_list_list, tlist_list, hbill_list_list

        from_date:date = None
        curr_rechnr:int = None
        do_flag:int = 0
        art_type:int = 0
        bill_doflag:bool = False
        bill_cardnum:str = ""
        curr_cardnum:str = ""
        i:int = 0
        str_param:str = ""
        ratecd:str = ""
        bguest = None
        Bguest =  create_buffer("Bguest",Guest)
        Bres_list = Res_list
        bres_list_list = res_list_list

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resstatus == 8) & (Res_line.abreise == bill_datum) & (Res_line.erwachs > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.ankunft).all():

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == res_line.gastnrmember)).first()

            mc_guest = db_session.query(Mc_guest).filter(
                     (Mc_guest.gastnr == guest.gastnr) & (Mc_guest.cardnum != "") & (Mc_guest.activeflag)).first()

            if mc_guest:
                res_list = Res_list()
                res_list_list.append(res_list)

                res_list.gastnr = res_line.gastnrmember
                res_list.gastpay = res_line.gastnrpay
                res_list.resnr = res_line.resnr
                res_list.reslinnr = res_line.reslinnr
                res_list.ankunft = res_line.ankunft
                res_list.abreise = res_line.abreise
                res_list.cardnum = mc_guest.cardnum
                bill_cardnum = mc_guest.cardnum

                if from_date == None:
                    from_date = res_line.ankunft
            else:
                res_list = Res_list()
                res_list_list.append(res_list)

                res_list.gastnr = res_line.gastnrmember
                res_list.gastpay = res_line.gastnrpay
                res_list.resnr = res_line.resnr
                res_list.reslinnr = res_line.reslinnr
                res_list.ankunft = res_line.ankunft
                res_list.abreise = res_line.abreise
                res_list.cardnum = "0001"
                bill_cardnum = "0001"

                if from_date == None:
                    from_date = res_line.ankunft

        if from_date == None:
            from_date = bill_datum

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.bill_datum >= from_date) & (Bill_line.bill_datum <= bill_datum)).order_by(Bill_line.rechnr).all():

            if curr_rechnr != bill_line.rechnr:
                bill_cardnum = ""
                curr_rechnr = bill_line.rechnr
                bill_doflag = False

                bill = db_session.query(Bill).filter(
                         (Bill.rechnr == bill_line.rechnr)).first()

                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == bill.gastnr)).first()
                pass

                mc_guest = db_session.query(Mc_guest).filter(
                         (Mc_guest.gastnr == guest.gastnr) & (Mc_guest.cardnum != "") & (Mc_guest.activeflag)).first()

                if bill.resnr > 0 and bill.reslinnr > 0:

                    res_list = query(res_list_list, filters=(lambda res_list: res_list.resnr == bill.resnr and res_list.reslinnr == bill.parent_nr), first=True)
                    bill_doflag = None != res_list

                    if bill_doflag:
                        bill_cardnum = res_list.cardnum
                else:
                    bill_doflag = None != mc_guest and guest.karteityp == 0

                    if bill_doflag:
                        bill_cardnum = mc_guest.cardnum
                    else:
                        bill_cardnum = "0001"
            else:

                bill = db_session.query(Bill).filter(
                         (Bill.rechnr == bill_line.rechnr)).first()

            if bill_doflag:

                res_list = query(res_list_list, filters=(lambda res_list: res_list.resnr == bill_line.massnr and res_list.reslinnr == bill_line.billin_nr), first=True)

                if not res_list:

                    res_line = db_session.query(Res_line).filter(
                             (Res_line.resnr == bill_line.massnr) & (Res_line.reslinnr == bill_line.billin_nr) & (Res_line.erwachs > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.resstatus == 8)).first()

                    if res_line:

                        mc_guest = db_session.query(Mc_guest).filter(
                                 (Mc_guest.gastnr == res_line.gastnrmember) & (Mc_guest.cardnum != "") & (Mc_guest.activeflag)).first()

                        if mc_guest:
                            res_list = Res_list()
                            res_list_list.append(res_list)

                            res_list.gastnr = res_line.gastnrmember
                            res_list.gastpay = res_line.gastnrpay
                            res_list.resnr = res_line.resnr
                            res_list.reslinnr = res_line.reslinnr
                            res_list.ankunft = res_line.ankunft
                            res_list.abreise = res_line.abreise
                            res_list.cardnum = mc_guest.cardnum


                        else:
                            res_list = Res_list()
                            res_list_list.append(res_list)

                            res_list.gastnr = res_line.gastnrmember
                            res_list.gastpay = res_line.gastnrpay
                            res_list.resnr = res_line.resnr
                            res_list.reslinnr = res_line.reslinnr
                            res_list.ankunft = res_line.ankunft
                            res_list.abreise = res_line.abreise
                            res_list.cardnum = "0001"

            artikel = db_session.query(Artikel).filter(
                     (Artikel.artnr == bill_line.artnr) & (Artikel.departement == bill_line.departement)).first()
            do_it = None != artikel

            if do_it:
                do_it = (artikel.artart == 0 or artikel.artart == 8 or artikel.artart == 9 or artikel.artart == 1)

            if do_it:

                if artikel.artart == 9 and artikel.artgrp == 0:

                    res_list = query(res_list_list, filters=(lambda res_list: res_list.resnr == bill_line.massnr and res_list.reslinnr == bill_line.billin_nr), first=True)
                    do_it = None != res_list and bill_doflag

                    if do_it:
                        curr_cardnum = res_list.cardnum
                else:

                    if bill.resnr > 0 and bill.reslinnr > 0:
                        do_it = bill_doflag

                        if do_it:
                            curr_cardnum = bill_cardnum

                    elif bill.resnr > 0 and bill.reslinnr == 0:

                        if bill_line.massnr > 0 and bill_line.billin_nr > 0:

                            res_list = query(res_list_list, filters=(lambda res_list: res_list.resnr == bill_line.massnr and res_list.reslinnr == bill_line.billin_nr), first=True)
                            do_it = None != res_list

                            if do_it:
                                curr_cardnum = res_list.cardnum
                        else:
                            do_it = bill_doflag and bill_line.bill_datum == bill_datum

                            if do_it:
                                curr_cardnum = bill_cardnum

                    elif bill_doflag:

                        if bill_line.massnr > 0 and bill_line.billin_nr > 0:

                            res_list = query(res_list_list, filters=(lambda res_list: res_list.resnr == bill_line.massnr and res_list.reslinnr == bill_line.billin_nr), first=True)
                            do_it = None != res_list

                            if do_it:
                                curr_cardnum = bill_cardnum
                        else:
                            do_it = (bill_line.bill_datum == bill_datum)

                            if do_it:
                                curr_cardnum = bill_cardnum

            if do_it and re.match(r".*Remain.*",artikel.bezeich, re.IGNORECASE) and re.match(r".*Balance.*",artikel.bezeich, re.IGNORECASE):
                do_it = False

            if do_it:
                serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, bill_line.bill_datum, artikel.service_code, artikel.mwst_code))

                if serv == 1:
                    art_type = 1

                elif vat == 1:
                    art_type = 1

                elif artikel.artart == 1:
                    art_type = 4

                elif artikel.artart == 8:
                    art_type = 1

                elif artikel.artart == 9:

                    if artikel.artgrp == 0:
                        art_type = 1
                    else:
                        art_type = 5

                elif artikel.artart == 0:

                    if artikel.umsatzart == 1:
                        art_type = 1
                    elif artikel.umsatzart == 2:
                        art_type = 1
                    elif artikel.umsatzart == 4:
                        art_type = 4
                    elif artikel.umsatzart == 5:
                        art_type = 2
                    elif artikel.umsatzart == 6:
                        art_type = 3
                    else:
                        art_type = 4

                if art_type == 5:

                    if bill.resnr > 0 and bill.reslinnr == 0 and bill_line.billin_nr > 0:

                        tline_list = query(tline_list_list, filters=(lambda tline_list: tline_list.rechnr == bill_line.rechnr and tline_list.reslinnr == bill_line.billin_nr and tline_list.arttype == art_type and tline_list.bezeich == bill_line.bezeich), first=True)
                    else:

                        tline_list = query(tline_list_list, filters=(lambda tline_list: tline_list.rechnr == bill_line.rechnr and tline_list.arttype == art_type and tline_list.bezeich == bill_line.bezeich), first=True)

                    if not tline_list:
                        tline_list = Tline_list()
                        tline_list_list.append(tline_list)

                        tline_list.arttype = art_type
                        tline_list.rechnr = bill_line.rechnr
                        tline_list.datum = bill_datum
                        tline_list.zeit = 0
                        tline_list.bezeich = bill_line.bezeich
                        tline_list.dept = 0
                        tline_list.email = curr_cardnum
                        tline_list.pax = 1

                        if bill.resnr > 0 and bill.reslinnr == 0 and bill_line.billin_nr > 0:
                            tline_list.reslinnr = bill_line.billin_nr
                            tline_list.s_reslin = tline_list.reslinnr *\
                                10000000

                        if bill.resnr > 0 and bill.reslinnr > 0 and bill_line.billin_nr > 0:

                            res_line = db_session.query(Res_line).filter(
                                     (Res_line.resnr == bill.resnr) & (Res_line.reslinnr == bill.parent_nr)).first()

                            zimkateg = db_session.query(Zimkateg).filter(
                                     (Zimkateg.zikatnr == res_line.zikatnr)).first()

                            ratecode = db_session.query(Ratecode).filter(
                                     (Ratecode.zikatnr == res_line.zikatnr)).first()
                            for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                                str_param = entry(i - 1, res_line.zimmer_wunsch, ";")

                                if re.match(r".*\$CODE\$.*",str_param, re.IGNORECASE):
                                    ratecd = entry(2, str_param, "$")

                            if res_line:
                                tline_list.reslinnr = res_line.reslinnr
                                tline_list.checkin = res_line.ankunft
                                tline_list.checkout = res_line.abreise
                                tline_list.ankzeit = res_line.ankzeit
                                tline_list.abrezeit = res_line.abreisezeit
                                tline_list.rcode = ratecd
                                tline_list.rtype = zimkateg.kurzbez
                                tline_list.resnr = res_line.resnr
                                tline_list.gastnr = res_line.gastnrmember

                    if bill.parent_nr > 0:

                        res_list = query(res_list_list, filters=(lambda res_list: res_list.resnr == bill.resnr and res_list.reslinnr == bill.parent_nr), first=True)
                    else:

                        res_list = query(res_list_list, filters=(lambda res_list: res_list.resnr == bill.resnr), first=True)

                    if res_list:
                        tline_list.gastpay = res_list.gastpay
                    else:
                        tline_list.gastpay = bill.gastnr

                    bguest = db_session.query(Bguest).filter(
                             (Bguest.gastnr == tline_list.gastpay)).first()

                    if bguest:
                        tline_list.breslin = bguest.karteityp
                    tline_list.price =  to_decimal(tline_list.price) + to_decimal(bill_line.betrag)


                else:

                    if bill.resnr > 0 and bill.reslinnr == 0 and bill_line.billin_nr > 0:

                        tline_list = query(tline_list_list, filters=(lambda tline_list: tline_list.rechnr == bill_line.rechnr and tline_list.reslinnr == bill_line.billin_nr and tline_list.arttype == art_type and tline_list.bezeich == bill_line.bezeich), first=True)
                    else:

                        tline_list = query(tline_list_list, filters=(lambda tline_list: tline_list.rechnr == bill_line.rechnr and tline_list.resnr == bill_line.massnr and tline_list.reslinnr == bill_line.billin_nr and tline_list.arttype == art_type), first=True)

                    if not tline_list:
                        tline_list = Tline_list()
                        tline_list_list.append(tline_list)

                        tline_list.arttype = art_type
                        tline_list.rechnr = bill_line.rechnr
                        tline_list.datum = bill_datum
                        tline_list.zeit = 0
                        tline_list.bezeich = s_arttype[art_type - 1]
                        tline_list.dept = 0
                        tline_list.email = curr_cardnum

                        if bill.resnr > 0 and bill.reslinnr > 0 and bill_line.billin_nr > 0:

                            if artikel.artart == 9 and artikel.artgrp == 0:

                                res_line = db_session.query(Res_line).filter(
                                         (Res_line.resnr == bill_line.massnr) & (Res_line.reslinnr == bill_line.billin_nr)).first()
                            else:

                                res_line = db_session.query(Res_line).filter(
                                         (Res_line.resnr == bill.resnr) & (Res_line.reslinnr == bill.parent_nr)).first()

                            zimkateg = db_session.query(Zimkateg).filter(
                                     (Zimkateg.zikatnr == res_line.zikatnr)).first()

                            ratecode = db_session.query(Ratecode).filter(
                                     (Ratecode.zikatnr == res_line.zikatnr)).first()
                            for i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
                                str_param = entry(i - 1, res_line.zimmer_wunsch, ";")

                                if re.match(r".*\$CODE\$.*",str_param, re.IGNORECASE):
                                    ratecd = entry(2, str_param, "$")

                            if res_line:
                                # tline_list.pax = res_line.erwach + res_line.kind1 + res_line.kind2
                                tline_list.pax = res_line.erwachs + res_line.kind1 + res_line.kind2

                                tline_list.reslinnr = res_line.reslinnr
                                tline_list.checkin = res_line.ankunft
                                tline_list.checkout = res_line.abreise
                                tline_list.ankzeit = res_line.ankzeit
                                tline_list.abrezeit = res_line.abreisezeit
                                tline_list.rcode = ratecd
                                tline_list.rtype = zimkateg.kurzbez
                                tline_list.resnr = res_line.resnr
                                tline_list.gastnr = res_line.gastnrmember

                        elif bill.resnr > 0 and bill.reslinnr == 0 and bill_line.billin_nr > 0:

                            if artikel.artart == 9 and artikel.artgrp == 0:

                                res_line = db_session.query(Res_line).filter(
                                         (Res_line.resnr == bill_line.massnr) & (Res_line.reslinnr == bill_line.billin_nr)).first()
                            else:

                                res_line = db_session.query(Res_line).filter(
                                         (Res_line.resnr == bill.resnr) & (Res_line.reslinnr == bill.parent_nr)).first()

                            zimkateg = db_session.query(Zimkateg).filter(
                                     (Zimkateg.zikatnr == res_line.zikatnr)).first()

                            ratecode = db_session.query(Ratecode).filter(
                                     (Ratecode.zikatnr == res_line.zikatnr)).first()
                            for i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
                                str_param = entry(i - 1, res_line.zimmer_wunsch, ";")

                                if re.match(r".*\$CODE\$.*",str_param, re.IGNORECASE):
                                    ratecd = entry(2, str_param, "$")

                            if res_line:
                                # tline_list.pax = res_line.erwach + res_line.kind1 + res_line.kind2
                                tline_list.pax = res_line.erwachs + res_line.kind1 + res_line.kind2

                                tline_list.checkin = res_line.ankunft
                                tline_list.checkout = res_line.abreise
                                tline_list.ankzeit = res_line.ankzeit
                                tline_list.abrezeit = res_line.abreisezeit
                                tline_list.rcode = ratecd
                                tline_list.rtype = zimkateg.kurzbez
                                tline_list.resnr = res_line.resnr
                                tline_list.gastnr = res_line.gastnrmember
                                tline_list.reslinnr = bill_line.billin_nr
                                tline_list.s_reslin = tline_list.reslinnr *\
                                        10000000

                    if bill.parent_nr > 0:

                        res_list = query(res_list_list, filters=(lambda res_list: res_list.resnr == bill.resnr and res_list.reslinnr == bill.parent_nr), first=True)
                    else:

                        res_list = query(res_list_list, filters=(lambda res_list: res_list.resnr == bill.resnr), first=True)

                    if res_list:
                        tline_list.gastpay = res_list.gastpay
                    else:
                        tline_list.gastpay = bill.gastnr

                    bguest = db_session.query(Bguest).filter(
                             (Bguest.gastnr == tline_list.gastpay)).first()

                    if bguest:
                        tline_list.breslin = bguest.karteityp
                    tline_list.price =  to_decimal(tline_list.price) + to_decimal(bill_line.betrag)


    def resto_points():

        nonlocal bill_datum, line_nr, serv, vat, netto, serv_betrag, vat_proz, do_it, allocated_point, ci_date, s_arttype, reihenfolge, outstr, tprice, tservis, disc_food_art, disc_bev_art, disc_other_art, progname, h_bill_line, queasy, nightaudit, htparam, nitehist, guest, res_line, mc_guest, reservation, segment, bill_line, bill, artikel, zimkateg, ratecode, h_bill, h_artikel
        nonlocal hbill_buff, bqueasy


        nonlocal res_list, tline_list, tlist, hbill_list, hbill_buff, bqueasy, bres_list, bres_list, tline_buff
        nonlocal res_list_list, tline_list_list, tlist_list, hbill_list_list

        art_type:int = 0

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr > 0) & (H_bill_line.bill_datum == bill_datum) & (H_bill_line.zeit >= 0) & (H_bill_line.artnr > 0) & (H_bill_line.betrag != 0)).order_by(H_bill_line.departement, H_bill_line.rechnr, H_bill_line.sysdate.desc(), H_bill_line.zeit.desc()).all():

            hbill_list = query(hbill_list_list, filters=(lambda hbill_list: hbill_list.dept == h_bill_line.departement and hbill_list.rechnr == h_bill_line.rechnr), first=True)

            if not hbill_list:

                h_bill = db_session.query(H_bill).filter(
                         (H_bill.rechnr == h_bill_line.rechnr) & (H_bill.departement == h_bill_line.departement)).first()
                hbill_list = Hbill_list()
                hbill_list_list.append(hbill_list)

                hbill_list.dept = h_bill_line.departement
                hbill_list.rechnr = h_bill_line.rechnr
                hbill_list.resnr = h_bill.resnr
                hbill_list.reslinnr = h_bill.reslinnr

                if h_bill.belegung > 0:
                    hbill_list.pax = h_bill.belegung

        for hbill_list in query(hbill_list_list, filters=(lambda hbill_list: hbill_list.resnr > 0)):

            if hbill_list.reslinnr > 0:

                res_line = db_session.query(Res_line).filter(
                         (Res_line.resnr == hbill_list.resnr) & (Res_line.reslinnr == hbill_list.reslinnr)).first()

                if res_line:

                    if allocated_point == 0:

                        guest = db_session.query(Guest).filter(
                                 (Guest.gastnr == res_line.gastnrmember)).first()

                    elif allocated_point == 1:

                        guest = db_session.query(Guest).filter(
                                 (Guest.gastnr == res_line.gastnr)).first()

                    mc_guest = db_session.query(Mc_guest).filter(
                             (Mc_guest.gastnr == guest.gastnr) & (Mc_guest.cardnum != "")).first()

                    if mc_guest:
                        hbill_list.cardnum = mc_guest.cardnum
            else:

                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == hbill_list.resnr)).first()

                if guest:

                    mc_guest = db_session.query(Mc_guest).filter(
                             (Mc_guest.gastnr == guest.gastnr) & (Mc_guest.cardnum != "")).first()

                    if mc_guest:

                        if allocated_point == 0 and guest.karteityp == 0:
                            hbill_list.cardnum = mc_guest.cardnum

                        elif allocated_point == 1 and guest.karteityp > 0:
                            hbill_list.cardnum = mc_guest.cardnum

        for hbill_list in query(hbill_list_list, filters=(lambda hbill_list: hbill_list.cardnum == "")):
            hbill_list_list.remove(hbill_list)

        for hbill_list in query(hbill_list_list, filters=(lambda hbill_list: hbill_list.do_it)):

            h_bill_line_obj_list = []
            for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.departement == H_bill_line.departement) & (H_artikel.artnr == H_bill_line.artnr) & (H_artikel.artart == 0)).filter(
                     (H_bill_line.departement == hbill_list.dept) & (H_bill_line.rechnr == hbill_list.rechnr) & (H_bill_line.artnr > 0)).order_by(H_bill_line._recid).all():
                if h_bill_line._recid in h_bill_line_obj_list:
                    continue
                else:
                    h_bill_line_obj_list.append(h_bill_line._recid)


                hbill_list.tot_sales =  to_decimal(hbill_list.tot_sales) + to_decimal(h_bill_line.betrag)

        for hbill_list in query(hbill_list_list, filters=(lambda hbill_list: hbill_list.do_it  and hbill_list.tot_sales > 0)):

            for h_bill_line in db_session.query(H_bill_line).filter(
                     (H_bill_line.departement == hbill_list.dept) & (H_bill_line.rechnr == hbill_list.rechnr) & (H_bill_line.bill_datum == bill_datum)).order_by(H_bill_line._recid).all():

                if h_bill_line.artnr == 0:

                    if hbill_list.tot_sales * h_bill_line.betrag <= 0:

                        if hbill_list.i_fact <= 0:
                            hbill_list.i_fact = hbill_list.i_fact + 1
                    else:

                        if hbill_list.i_fact >= 0:
                            hbill_list.i_fact = hbill_list.i_fact - 1
                else:

                    h_artikel = db_session.query(H_artikel).filter(
                             (H_artikel.departement == h_bill_line.departement) & (H_artikel.artnr == h_bill_line.artnr)).first()

                    if h_artikel.artart == 2 or h_artikel.artart == 6 or h_artikel.artart == 7:

                        if not re.match(r".*(Change).*",h_bill_line.bezeich, re.IGNORECASE):

                            if h_artikel.artart == 2:

                                if h_bill_line.betrag < 0:
                                    hbill_list.i_ledger = hbill_list.i_ledger + 1
                                else:
                                    hbill_list.i_ledger = hbill_list.i_ledger - 1

                            if hbill_list.tot_sales * h_bill_line.betrag <= 0:

                                if hbill_list.i_fact <= 0:
                                    hbill_list.i_fact = hbill_list.i_fact + 1
                            else:

                                if hbill_list.i_fact >= 0:
                                    hbill_list.i_fact = hbill_list.i_fact - 1

        for hbill_list in query(hbill_list_list, filters=(lambda hbill_list: hbill_list.do_it and hbill_list.i_fact > 0)):

            h_bill_line_obj_list = []
            for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.artart == 0)).filter(
                     (H_bill_line.departement == hbill_list.dept) & (H_bill_line.rechnr == hbill_list.rechnr) & (H_bill_line.artnr > 0)).order_by(H_bill_line._recid).all():
                if h_bill_line._recid in h_bill_line_obj_list:
                    continue
                else:
                    h_bill_line_obj_list.append(h_bill_line._recid)

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement)).first()

                if artikel.artart == 9:
                    art_type = 5

                elif artikel.artart == 0:

                    if artikel.umsatzart == 1:
                        art_type = 1
                    elif artikel.umsatzart == 2:
                        art_type = 1
                    elif artikel.umsatzart == 4:
                        art_type = 4
                    elif artikel.umsatzart == 5:
                        art_type = 2
                    elif artikel.umsatzart == 6:
                        art_type = 3
                    else:
                        art_type = 4

                if h_bill_line.artnr == disc_food_art or h_bill_line.artnr == disc_bev_art or h_bill_line.artnr == disc_food_art:

                    tline_list = query(tline_list_list, filters=(lambda tline_list: tline_list.rechnr == h_bill_line.rechnr and tline_list.artnr == disc_food_art and tline_list.dept == h_bill_line.departement), first=True)

                    if not tline_list:
                        tline_list = Tline_list()
                        tline_list_list.append(tline_list)

                        tline_list.arttype = art_type
                        tline_list.rechnr = h_bill_line.rechnr
                        tline_list.artnr = disc_food_art
                        tline_list.dept = h_bill_line.departement
                        tline_list.bezeich = "Discount"
                        tline_list.datum = bill_datum
                        tline_list.zeit = h_bill_line.zeit
                        tline_list.email = hbill_list.cardnum
                        tline_list.pax = hbill_list.pax


                    tline_list.price =  to_decimal(tline_list.price) - to_decimal(h_bill_line.betrag)


                else:

                    tline_list = query(tline_list_list, filters=(lambda tline_list: tline_list.rechnr == h_bill_line.rechnr and tline_list.artnr == h_bill_line.artnr and tline_list.bezeich == h_bill_line.bezeich and tline_list.dept == h_bill_line.departement), first=True)

                    if not tline_list:
                        tline_list = Tline_list()
                        tline_list_list.append(tline_list)

                        tline_list.arttype = art_type
                        tline_list.rechnr = h_bill_line.rechnr
                        tline_list.artnr = h_bill_line.artnr
                        tline_list.dept = h_bill_line.departement
                        tline_list.bezeich = h_bill_line.bezeich
                        tline_list.datum = bill_datum
                        tline_list.zeit = h_bill_line.zeit
                        tline_list.email = hbill_list.cardnum
                        tline_list.pax = hbill_list.pax


                    tline_list.price =  to_decimal(tline_list.price) + to_decimal(h_bill_line.betrag)


    def create_nitehis():

        nonlocal bill_datum, line_nr, serv, vat, netto, serv_betrag, vat_proz, do_it, allocated_point, ci_date, s_arttype, reihenfolge, outstr, tprice, tservis, disc_food_art, disc_bev_art, disc_other_art, progname, h_bill_line, queasy, nightaudit, htparam, nitehist, guest, res_line, mc_guest, reservation, segment, bill_line, bill, artikel, zimkateg, ratecode, h_bill, h_artikel
        nonlocal hbill_buff, bqueasy


        nonlocal res_list, tline_list, tlist, hbill_list, hbill_buff, bqueasy, bres_list, bres_list, tline_buff
        nonlocal res_list_list, tline_list_list, tlist_list, hbill_list_list

        date1:date = None
        time1:int = 0
        date2:date = None
        time2:str = ""
        date3:date = None
        time3:int = 0
        date4:date = None
        time4:str = ""
        date5:date = None
        time5:int = 0
        date6:date = None
        time6:str = ""
        nbuff = None
        Nbuff =  create_buffer("Nbuff",Nitehist)
        Tline_buff = Tline_list
        tline_buff_list = tline_list_list

        nitehist = db_session.query(Nitehist).filter(
                 (Nitehist.datum == bill_datum) & (Nitehist.reihenfolge == reihenfolge)).first()
        while None != nitehist:

            nbuff = db_session.query(Nbuff).filter(
                         (Nbuff._recid == Nbuff._recid)).with_for_update().first()
            db_session.delete(nbuff)
            pass


            curr_recid = nitehist._recid
            nitehist = db_session.query(Nitehist).filter(
                     (Nitehist.datum == bill_datum) & (Nitehist.reihenfolge == reihenfolge) & (Nitehist._recid > curr_recid)).first()

        if allocated_point == 3:

            for tline_list in query(tline_list_list, filters=(lambda tline_list: tline_list.price > 0 and tline_list.dept == 0), sort_by=[("rechnr",False)]):

                tline_buff = query(tline_buff_list, filters=(lambda tline_buff: tline_buff.price > 0 and tline_buff.rechnr == tline_list.rechnr and tline_buff.arttype == tline_list.arttype and tline_buff.gastpay == tline_buff.gastnr and tline_buff.dept == tline_list.dept), first=True)

                if tline_buff:

                    if tline_buff.email != tline_list.email:
                        tline_buff.price =  to_decimal(tline_buff.price) + to_decimal(tline_list.price)

        for tline_list in query(tline_list_list, filters=(lambda tline_list: tline_list.price > 0), sort_by=[("dept",False),("rechnr",False)]):
            tline_list.bezeich = replace_str(tline_list.bezeich, "|", "")

            if allocated_point == 3 and tline_list.dept == 0 and tline_list.gastnr != tline_list.gastpay and tline_list.breslin == 0:
                tline_list.price =  to_decimal("0")
            outstr = "L" + "|" + to_string(tline_list.rechnr + tline_list.s_reslin) + "|" + to_string(tline_list.dept) + "|" + tline_list.bezeich + "|" + to_string(tline_list.price) + "|" + tline_list.rcode + "|" + tline_list.rtype + "|" + to_string(tline_list.resnr) + "|" + to_string(tline_list.reslinnr, "999") + "|" + to_string(tline_list.breslin) + "|" + to_string(tline_list.gastnr) + "|" + to_string(tline_list.gastpay) + "|" + to_string(tline_list.email)
            add_line(outstr, bill_datum)

            if allocated_point == 2 or allocated_point == 3:

                tlist = query(tlist_list, filters=(lambda tlist: tlist.resnr == tline_list.resnr and tlist.reslinnr == tline_list.reslinnr and tlist.departement == tline_list.dept and tlist.rechnr == tline_list.rechnr), first=True)
            else:

                tlist = query(tlist_list, filters=(lambda tlist: tlist.usr == tline_list.email and tlist.departement == tline_list.dept and tlist.rechnr == tline_list.rechnr), first=True)

            if not tlist:
                date1 = get_current_date()
                time1 = get_current_time_in_seconds()
                date3 = tline_list.checkin
                time3 = tline_list.ankzeit
                date5 = tline_list.checkout
                time5 = tline_list.abrezeit


                date2, time2 = convert_time(date1, time1)
                date4, time4 = convert_time(date3, time3)
                date6, time6 = convert_time(date5, time5)
                tlist = Tlist()
                tlist_list.append(tlist)

                tlist.departement = tline_list.dept
                tlist.rechnr = tline_list.rechnr
                tlist.resnr = tline_list.resnr
                tlist.reslinnr = tline_list.reslinnr
                tlist.s_reslin = tline_list.s_reslin
                tlist.breslin = tline_list.breslin
                tlist.gastnr = tline_list.gastnr
                tlist.gastpay = tline_list.gastpay
                tlist.usr = tline_list.email
                tlist.departement = tline_list.dept
                tlist.created = to_string(get_year(date2) , "9999") + "-" + to_string(get_month(date2) , "99") + "-" +\
                        to_string(get_day(date2) , "99") + "-T" + time2
                tlist.checkin = to_string(get_year(date4) , "9999") + "-" + to_string(get_month(date4) , "99") +\
                        "-" + to_string(get_day(date4) , "99") + "-T" + time4
                tlist.checkout = to_string(get_year(date6) , "9999") + "-" + to_string(get_month(date6) , "99") +\
                        "-" + to_string(get_day(date6) , "99") + "-T" + time6
                tlist.pax = tline_list.pax

            if tline_list.dept >= 1 and tline_list.bezeich.lower()  == ("Discount").lower() :
                tlist.discount =  to_decimal(tlist.discount) + to_decimal(tline_list.price)
                tlist.saldo =  to_decimal(tlist.saldo) - to_decimal(tline_list.price)


            else:
                tlist.saldo =  to_decimal(tlist.saldo) + to_decimal(tline_list.price)


                tlist.service = tlist.saldo * 0.1

        for tlist in query(tlist_list):
            outstr = "H|SEND=0|" + to_string(tlist.rechnr + tlist.s_reslin) + "|" + tlist.usr + "|" + to_string(tlist.saldo) + "|" + to_string(tlist.departement) + "|" + to_string(tlist.created) + "|" + to_string(tlist.checkin) + "|" + to_string(tlist.checkout) + "|" + to_string(tlist.pax, "999") + "|" + to_string(tlist.discount) + "|" + to_string(tlist.reslinnr, "999") + "|" + to_string(tlist.service) + "|" + to_string(tlist.resnr) + "|" + to_string(tlist.breslin) + "|" + to_string(tlist.gastnr) + "|" + to_string(tlist.gastpay)
            add_line(outstr, bill_datum)


    def convert_time(inp_date:date, inp_time:int):

        nonlocal bill_datum, line_nr, serv, vat, netto, serv_betrag, vat_proz, do_it, allocated_point, ci_date, s_arttype, reihenfolge, outstr, tprice, tservis, disc_food_art, disc_bev_art, disc_other_art, progname, h_bill_line, queasy, nightaudit, htparam, nitehist, guest, res_line, mc_guest, reservation, segment, bill_line, bill, artikel, zimkateg, ratecode, h_bill, h_artikel
        nonlocal hbill_buff, bqueasy


        nonlocal res_list, tline_list, tlist, hbill_list, hbill_buff, bqueasy, bres_list, bres_list, tline_buff
        nonlocal res_list_list, tline_list_list, tlist_list, hbill_list_list

        out_date = None
        out_time = ""
        dtstoredtime = None
        newdatetime = None
        tmp_time:str = ""
        tz:int = 0
        d:int = 0
        m:int = 0
        yy:int = 0
        hh:int = 0
        mm:int = 0
        ss:int = 0
        str_yy:int = 0

        def generate_inner_output():
            return (out_date, out_time)

        tmp_time = to_string(inp_time, "hh:mm:ss")
        str_yy = to_int(to_string(get_year(inp_date)))
        d = to_int(to_string(get_day(inp_date)))
        m = to_int(to_string(get_month(inp_date)))
        yy = to_int(to_string(get_year(inp_date)))
        hh = to_int(entry(0, to_string(tmp_time) , chr(58)))
        mm = to_int(entry(1, to_string(tmp_time) , chr(58)))
        ss = to_int(entry(2, to_string(tmp_time) , chr(58)))

        # Rulita, 11-12-2025
        # - Fixing timezone calculation to use local timezone offset
        # tz = to_int(entry(1, to_string(get_current_time_in_seconds(), 'hh:mm:ss') , chr(58)))
        # dtstoredtime = DATETIME_TZ (m, d, yy, hh, mm, ss, 0, 0)
        # newdatetime = DATETIME_TZ (dtstoredtime, - (tz * 60))

        _local_offset = datetime.now().astimezone().utcoffset()
        tz = int((_local_offset.total_seconds() if _local_offset else 0) // 3600)

        dtstoredtime = datetime(yy, m, d, hh, mm, ss, tzinfo=timezone.utc)

        newdatetime = dtstoredtime - timedelta(minutes=tz * 60)

        out_date = date_mdy(entry(0, to_string(newdatetime) , chr(32)))
        out_time = entry(0, entry(1, to_string(newdatetime) , chr(32)) , chr(46))

        return generate_inner_output()

    nightaudit = db_session.query(Nightaudit).filter(
             (func.lower(Nightaudit.programm) == (progname).lower())).first()

    if not nightaudit:

        return generate_output()
    reihenfolge = nightaudit.reihenfolge

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 87)).first()

    if htparam:
        ci_date = htparam.fdate
    bill_datum = ci_date - timedelta(days=1)

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 41)).first()

    if htparam:
        allocated_point = htparam.finteger

    if allocated_point == None:

        return generate_output()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 1)).first()

    if htparam.fdecimal != 0:
        vat_proz =  to_decimal(htparam.fdecimal)
    disc_other_art = get_output(htpint(556))
    disc_food_art = get_output(htpint(557))
    disc_bev_art = get_output(htpint(596))

    if allocated_point == 0:
        fo_point0()

    elif allocated_point == 1:
        fo_point1()

    elif allocated_point == 2:
        fo_point2()

    elif allocated_point == 3:
        fo_point3()
    create_nitehis()

    return generate_output()