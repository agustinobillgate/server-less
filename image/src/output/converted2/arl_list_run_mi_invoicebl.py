from functions.additional_functions import *
import decimal
from datetime import date
import re
from sqlalchemy import func
from functions.ratecode_rate import ratecode_rate
from functions.pricecod_rate import pricecod_rate
from functions.".\\_rate" import ".\\_rate"
from models import Reservation, Res_line, Guest, Bill, Htparam, Master, Waehrung, Zimkateg, Arrangement, Reslin_queasy, Guest_pr, Queasy, Fixleist, Artikel, Bill_line, Genstat, Exrate

def arl_list_run_mi_invoicebl(resnr:int, curr_resnr:int, arl_list_reslinnr:int, t_active_flag:int, printtype:int):
    err_flag = 0
    avail_master = False
    avail_bill = False
    reslinnr = 1
    master_rechnr = 0
    bill_rechnr = 0
    mainres_gastnr = 0
    t_reservation_list = []
    t_res_line_list = []
    t_guest_list = []
    t_list_list = []
    new_contrate:bool = False
    resline_exrate:decimal = to_decimal("0.0")
    billdate:date = None
    bonus_array:List[bool] = create_empty_list(999, False)
    tot_amt:decimal = to_decimal("0.0")
    reservation = res_line = guest = bill = htparam = master = waehrung = zimkateg = arrangement = reslin_queasy = guest_pr = queasy = fixleist = artikel = bill_line = genstat = exrate = None

    s_list = t_list = t_reservation = t_res_line = t_guest = rline = mbill = mainres = None

    s_list_list, S_list = create_model("S_list", {"nr":int, "ankunft":date, "abreise":date, "bezeich":str, "rmcat":str, "preis":decimal, "lrate":decimal, "datum":date, "qty":int, "erwachs":int, "kind1":int, "kind2":int})
    t_list_list, T_list = create_model("T_list", {"nr":int, "ankunft":date, "abreise":date, "bezeich":str, "rmcat":str, "preis":decimal, "lrate":decimal, "tage":int, "date1":date, "date2":date, "qty":int, "betrag":decimal, "erwachs":int, "kind1":int, "kind2":int})
    t_reservation_list, T_reservation = create_model_like(Reservation)
    t_res_line_list, T_res_line = create_model_like(Res_line)
    t_guest_list, T_guest = create_model_like(Guest)

    Rline = create_buffer("Rline",Res_line)
    Mbill = create_buffer("Mbill",Bill)
    Mainres = create_buffer("Mainres",Reservation)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, avail_master, avail_bill, reslinnr, master_rechnr, bill_rechnr, mainres_gastnr, t_reservation_list, t_res_line_list, t_guest_list, t_list_list, new_contrate, resline_exrate, billdate, bonus_array, tot_amt, reservation, res_line, guest, bill, htparam, master, waehrung, zimkateg, arrangement, reslin_queasy, guest_pr, queasy, fixleist, artikel, bill_line, genstat, exrate
        nonlocal resnr, curr_resnr, arl_list_reslinnr, t_active_flag, printtype
        nonlocal rline, mbill, mainres


        nonlocal s_list, t_list, t_reservation, t_res_line, t_guest, rline, mbill, mainres
        nonlocal s_list_list, t_list_list, t_reservation_list, t_res_line_list, t_guest_list
        return {"err_flag": err_flag, "avail_master": avail_master, "avail_bill": avail_bill, "reslinnr": reslinnr, "master_rechnr": master_rechnr, "bill_rechnr": bill_rechnr, "mainres_gastnr": mainres_gastnr, "t-reservation": t_reservation_list, "t-res-line": t_res_line_list, "t-guest": t_guest_list, "t-list": t_list_list}

    def read_proforma_inv(resnr:int, rechnr:int):

        nonlocal err_flag, avail_master, avail_bill, reslinnr, master_rechnr, bill_rechnr, mainres_gastnr, t_reservation_list, t_res_line_list, t_guest_list, t_list_list, new_contrate, resline_exrate, billdate, bonus_array, tot_amt, reservation, res_line, guest, bill, htparam, master, waehrung, zimkateg, arrangement, reslin_queasy, guest_pr, queasy, fixleist, artikel, bill_line, genstat, exrate
        nonlocal curr_resnr, arl_list_reslinnr, t_active_flag, printtype
        nonlocal rline, mbill, mainres


        nonlocal s_list, t_list, t_reservation, t_res_line, t_guest, rline, mbill, mainres
        nonlocal s_list_list, t_list_list, t_reservation_list, t_res_line_list, t_guest_list

        datum:date = None
        co_date:date = None
        add_it:bool = False
        ankunft:date = None
        abreise:date = None
        rm_rate:decimal = to_decimal("0.0")
        argt_rate:decimal = to_decimal("0.0")
        argt_defined:bool = False
        delta:int = 0
        start_date:date = None
        fixed_rate:bool = False
        qty:int = 0
        it_exist:bool = False
        exrate1:decimal = 1
        ex2:decimal = 1
        pax:int = 0
        child1:int = 0
        bill_date:date = None
        curr_zikatnr:int = 0
        ebdisc_flag:bool = False
        kbdisc_flag:bool = False
        rate_found:bool = False
        early_flag:bool = False
        kback_flag:bool = False
        count_heritage:int = 0
        count_night:int = 0
        dept:int = 0
        loopi:int = 0
        curr_no:int = 1000
        do_it:bool = False
        w1 = None
        resline = None
        i:int = 0
        j:int = 0
        qty1:int = 0
        ct:str = ""
        contcode:str = ""
        W1 =  create_buffer("W1",Waehrung)
        Resline =  create_buffer("Resline",Res_line)

        for resline in db_session.query(Resline).filter(
                 (Resline.resnr == resnr) & (Resline.active_flag < 2) & (Resline.resstatus != 12) & (Resline.resstatus != 9) & (Resline.resstatus != 10) & (Resline.resstatus != 99)).order_by(Resline._recid).all():
            ebdisc_flag = re.match(".*ebdisc.*",resline.zimmer_wunsch)
            kbdisc_flag = re.match(".*kbdisc.*",resline.zimmer_wunsch)

            if resline.l_zuordnung[0] != 0:
                curr_zikatnr = resline.l_zuordnung[0]
            else:
                curr_zikatnr = resline.zikatnr

            zimkateg = db_session.query(Zimkateg).filter(
                     (Zimkateg.zikatnr == resline.zikatnr)).first()

            arrangement = db_session.query(Arrangement).filter(
                     (Arrangement.arrangement == resline.arrangement)).first()
            ankunft = resline.ankunft
            abreise = resline.abreise
            fixed_rate = False

            if resline.was_status == 1:
                fixed_rate = True
            co_date = resline.abreise

            if co_date > resline.ankunft:
                co_date = co_date - timedelta(days=1)
            create_bonus()
            for datum in date_range(resline.ankunft,co_date) :
                bill_date = datum
                argt_rate =  to_decimal("0")
                rm_rate =  to_decimal(resline.zipreis)
                pax = resline.erwachs

                if fixed_rate:

                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                             (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == resline.resnr) & (Reslin_queasy.reslinnr == resline.reslinnr) & (datum >= Reslin_queasy.date1) & (datum <= Reslin_queasy.date2)).first()

                    if reslin_queasy:
                        rm_rate =  to_decimal(reslin_queasy.deci1)

                        if reslin_queasy.number3 != 0:
                            pax = reslin_queasy.number3
                    rm_rate, it_exist = usr_prog1(datum, rm_rate)
                else:

                    guest = db_session.query(Guest).filter(
                             (Guest.gastnr == resline.gastnr)).first()

                    guest_pr = db_session.query(Guest_pr).filter(
                             (Guest_pr.gastnr == guest.gastnr)).first()

                    if guest_pr:

                        queasy = db_session.query(Queasy).filter(
                                 (Queasy.key == 18) & (Queasy.number1 == resline.reserve_int)).first()

                        if queasy and queasy.logi3:
                            bill_date = resline.ankunft

                        if new_contrate:

                            if resline_exrate != 0:
                                rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, resline.resnr, resline.reslinnr, guest_pr.code, None, bill_date, resline.ankunft, resline.abreise, resline.reserve_int, arrangement.argtnr, curr_zikatnr, resline.erwachs, resline.kind1, resline.kind2, resline_exrate, resline.betriebsnr))
                            else:
                                rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, resline.resnr, resline.reslinnr, guest_pr.code, None, bill_date, resline.ankunft, resline.abreise, resline.reserve_int, arrangement.argtnr, curr_zikatnr, resline.erwachs, resline.kind1, resline.kind2, resline.reserve_dec, resline.betriebsnr))
                        else:
                            rm_rate, rate_found = get_output(pricecod_rate(resline.resnr, resline.reslinnr, guest_pr.code, bill_date, resline.ankunft, resline.abreise, resline.reserve_int, arrangement.argtnr, curr_zikatnr, resline.erwachs, resline.kind1, resline.kind2, resline.reserve_dec, resline.betriebsnr))
                            rm_rate, it_exist = usr_prog2(datum, rm_rate)

                            if it_exist:
                                rate_found = True

                            if not it_exist and bonus_array[datum - resline.ankunft + 1 - 1] :
                                rm_rate =  to_decimal("0")

                s_list = query(s_list_list, filters=(lambda s_list: s_list.bezeich == arrangement.argt_rgbez and s_list.rmcat == zimkateg.kurzbez and s_list.preis == rm_rate and s_list.datum == datum and s_list.ankunft == resline.ankunft and s_list.abreise == resline.abreise and s_list.erwachs == pax and s_list.kind1 == resline.kind1 and s_list.kind2 == resline.kind2), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.bezeich = arrangement.argt_rgbez
                    s_list.rmcat = zimkateg.kurzbez
                    s_list.preis =  to_decimal(rm_rate)
                    s_list.datum = datum
                    s_list.ankunft = resline.ankunft
                    s_list.abreise = resline.abreise
                    s_list.erwachs = pax
                    s_list.kind1 = resline.kind1
                    s_list.kind2 = resline.kind2
                s_list.qty = s_list.qty + resline.zimmeranz

                for fixleist in db_session.query(Fixleist).filter(
                         (Fixleist.resnr == resline.resnr) & (Fixleist.reslinnr == resline.reslinnr)).order_by(Fixleist._recid).all():
                    add_it = False
                    argt_rate =  to_decimal("0")

                    if fixleist.sequenz == 1:
                        add_it = True

                    elif fixleist.sequenz == 2 or fixleist.sequenz == 3:

                        if resline.ankunft == datum:
                            add_it = True

                    elif fixleist.sequenz == 4 and get_day(datum) == 1:
                        add_it = True

                    elif fixleist.sequenz == 5 and get_day(datum + 1) == 1:
                        add_it = True

                    elif fixleist.sequenz == 6:

                        if fixleist.lfakt == None:
                            delta = 0
                        else:
                            delta = fixleist.lfakt - resline.ankunft

                            if delta < 0:
                                delta = 0
                        start_date = resline.ankunft + timedelta(days=delta)

                        if (resline.abreise - start_date) < fixleist.dekade:
                            start_date = resline.ankunft

                        if datum <= (start_date + timedelta(days=(fixleist.dekade - 1))):
                            add_it = True

                        if datum < start_date:
                            add_it = False

                    if add_it:

                        artikel = db_session.query(Artikel).filter(
                                 (Artikel.artnr == fixleist.artnr) & (Artikel.departement == fixleist.departement)).first()
                        argt_rate =  to_decimal(fixleist.betrag) * to_decimal(fixleist.number)

                        if not fixed_rate and guest_pr:
                            contcode = guest_pr.code
                            ct = resline.zimmer_wunsch

                            if re.match(r".*\$CODE\$.*",ct, re.IGNORECASE):
                                ct = substring(ct, 0 + get_index(ct, "$CODE$") + 6)
                                contcode = substring(ct, 0, 1 + get_index(ct, ";") - 1)

                            reslin_queasy = db_session.query(Reslin_queasy).filter(
                                     (func.lower(Reslin_queasy.key) == ("argt-line").lower()) & (func.lower(Reslin_queasy.char1) == (contcode).lower()) & (Reslin_queasy.number1 == resline.reserve_int) & (Reslin_queasy.number2 == arrangement.argtnr) & (Reslin_queasy.reslinnr == resline.zikatnr) & (Reslin_queasy.number3 == fixleist.artnr) & (Reslin_queasy.resnr == fixleist.departement) & (bill_date >= Reslin_queasy.date1) & (bill_date <= Reslin_queasy.date2)).first()

                            if reslin_queasy:
                                argt_rate =  to_decimal(reslin_queasy.deci1) * to_decimal(fixleist.number)

                    if argt_rate != 0:

                        s_list = query(s_list_list, filters=(lambda s_list: s_list.bezeich == artikel.bezeich and s_list.preis == (argt_rate / fixleist.number) and s_list.datum == datum and s_list.ankunft == resline.ankunft and s_list.abreise == resline.abreise and s_list.erwachs == pax and s_list.kind1 == resline.kind1 and s_list.kind2 == resline.kind2), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.nr = artikel.artnr
                            s_list.bezeich = artikel.bezeich
                            s_list.preis =  to_decimal(argt_rate) / to_decimal(fixleist.number)
                            s_list.datum = datum
                            s_list.ankunft = resline.ankunft
                            s_list.abreise = resline.abreise
                            s_list.erwachs = pax
                            s_list.kind1 = resline.kind1
                            s_list.kind2 = resline.kind2
                        s_list.qty = s_list.qty + (fixleist.number * resline.zimmeranz)

        for s_list in query(s_list_list, sort_by=[("ankunft",False),("datum",False),("bezeich",False),("erwachs",False)]):

            if s_list.nr == 0:

                t_list = query(t_list_list, filters=(lambda t_list: t_list.bezeich == s_list.bezeich and t_list.rmcat == s_list.rmcat and t_list.preis == s_list.preis and t_list.ankunft == s_list.ankunft and t_list.abreise == s_list.abreise and t_list.erwachs == s_list.erwachs and t_list.kind1 == s_list.kind1 and t_list.kind2 == s_list.kind2), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.nr = s_list.nr
                    t_list.bezeich = s_list.bezeich
                    t_list.rmcat = s_list.rmcat
                    t_list.preis =  to_decimal(s_list.preis)
                    t_list.date1 = s_list.datum
                    t_list.ankunft = s_list.ankunft
                    t_list.abreise = s_list.abreise
                    t_list.erwachs = s_list.erwachs
                    t_list.kind1 = s_list.kind1
                    t_list.kind2 = s_list.kind2

                if s_list.qty >= t_list.qty:
                    t_list.tage = t_list.tage + 1
                t_list.date2 = s_list.datum

                if s_list.datum == t_list.date1:
                    t_list.qty = t_list.qty + s_list.qty

                if s_list.qty != t_list.qty and s_list.preis == t_list.preis:
                    qty1 = t_list.qty
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.nr = s_list.nr
                    t_list.bezeich = s_list.bezeich
                    t_list.rmcat = s_list.rmcat
                    t_list.preis =  to_decimal(s_list.preis)
                    t_list.date1 = s_list.datum
                    t_list.ankunft = s_list.ankunft
                    t_list.abreise = s_list.abreise
                    t_list.erwachs = s_list.erwachs
                    t_list.kind1 = s_list.kind1
                    t_list.kind2 = s_list.kind2
                    t_list.date1 = s_list.datum
                    t_list.date2 = s_list.datum
                    t_list.tage = 1

                    if s_list.qty > qty1:
                        j = s_list.qty - qty1
                        t_list.qty = j


                    else:
                        j = qty1 - s_list.qty
                        t_list.qty = s_list.qty


            else:

                t_list = query(t_list_list, filters=(lambda t_list: t_list.bezeich == s_list.bezeich and t_list.preis == s_list.preis and t_list.ankunft == s_list.ankunft and t_list.abreise == s_list.abreise and t_list.erwachs == s_list.erwachs and t_list.kind1 == s_list.kind1 and t_list.kind2 == s_list.kind2), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.nr = s_list.nr
                    t_list.bezeich = s_list.bezeich
                    t_list.preis =  to_decimal(s_list.preis)
                    t_list.date1 = s_list.datum
                    t_list.ankunft = s_list.ankunft
                    t_list.abreise = s_list.abreise
                    t_list.erwachs = s_list.erwachs
                    t_list.kind1 = s_list.kind1
                    t_list.kind2 = s_list.kind2
                t_list.tage = t_list.tage + 1
                t_list.date2 = s_list.datum

                if s_list.datum == t_list.date1:
                    t_list.qty = t_list.qty + s_list.qty
            s_list_list.remove(s_list)
        tot_amt =  to_decimal("0")

        for t_list in query(t_list_list):
            t_list.betrag =  to_decimal(t_list.qty) * to_decimal(t_list.tage) * to_decimal(t_list.preis)
            tot_amt =  to_decimal(tot_amt) + to_decimal(t_list.betrag)

        if rechnr > 0:

            bill_line_obj_list = []
            for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement)).filter(
                     (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line.bill_datum, Bill_line.zeit).all():
                if bill_line._recid in bill_line_obj_list:
                    continue
                else:
                    bill_line_obj_list.append(bill_line._recid)


                do_it = True

                if artikel.artart == 9:

                    arrangement = db_session.query(Arrangement).filter(
                             (Arrangement.argt_artikelnr == artikel.artnr)).first()

                    if not arrangement or arrangement.segmentcode == 0:
                        do_it = False

                if do_it:

                    if re.match(r"Heritage Fee.*",artikel.bezeich, re.IGNORECASE):

                        t_list = query(t_list_list, filters=(lambda t_list: t_list.bezeich == bill_line.bezeich), first=True)

                        if not t_list:
                            t_list = T_list()
                        t_list_list.append(t_list)

                        count_heritage = count_heritage + 1
                        dept = artikel.departement
                        t_list.preis =  to_decimal(bill_line.betrag)
                        t_list.qty = t_list.qty + 1
                        t_list.tage = t_list.tage + 1
                        t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(bill_line.betrag)


                    else:
                        t_list = T_list()
                        t_list_list.append(t_list)

                        t_list.preis =  to_decimal("0")
                        t_list.betrag =  to_decimal(bill_line.betrag)


                    curr_no = curr_no + 1
                    t_list.nr = curr_no
                    t_list.bezeich = bill_line.bezeich
                    t_list.date1 = bill_line.bill_datum

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == resnr) & (Res_line.reslinnr == reslinnr)).first()

        if res_line:
            count_night = res_line.abreise - res_line.ankunft

        if count_heritage < count_night:
            for loopi in range((count_heritage + 1),count_night + 1) :

                artikel = db_session.query(Artikel).filter(
                         (func.lower(Artikel.bezeich).op("~")(("Heritage Fee*".lower().replace("*",".*")))) & (Artikel.departement == dept)).first()

                if artikel:

                    bill_line = db_session.query(Bill_line).filter(
                             (Bill_line.rechnr == bill.rechnr) & (Bill_line.artnr == artikel.artnr)).first()

                    if bill_line:

                        t_list = query(t_list_list, filters=(lambda t_list: t_list.bezeich == bill_line.bezeich), first=True)

                        if t_list:
                            t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(bill_line.betrag)

                        elif not t_list:
                            t_list = T_list()
                            t_list_list.append(t_list)

                            curr_no = curr_no + 1
                            t_list.nr = curr_no
                            t_list.bezeich = bill_line.bezeich
                            t_list.preis =  to_decimal(artikel.epreis)
                            t_list.date1 = res_line.ankunft
                            t_list.betrag =  to_decimal(bill_line.betrag)


                    else:

                        t_list = query(t_list_list, filters=(lambda t_list: t_list.bezeich == artikel.bezeich), first=True)

                        if t_list:
                            t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(artikel.epreis)

                        elif not t_list:
                            t_list = T_list()
                            t_list_list.append(t_list)

                            curr_no = curr_no + 1
                            t_list.nr = curr_no
                            t_list.bezeich = artikel.bezeich
                            t_list.preis =  to_decimal(artikel.epreis)
                            t_list.date1 = res_line.ankunft
                            t_list.betrag =  to_decimal(artikel.epreis)

            for t_list in query(t_list_list, filters=(lambda t_list: t_list.re.match(r"Heritage Fee.*",t_list.bezeich, re.IGNORECASE))):
                t_list.qty = res_line.zimmeranz
                t_list.tage = count_night
                t_list.betrag =  to_decimal(t_list.betrag) * to_decimal(t_list.qty)


    def read_proforma_inv1(resnr:int, reslinnr:int, rechnr:int):

        nonlocal err_flag, avail_master, avail_bill, master_rechnr, bill_rechnr, mainres_gastnr, t_reservation_list, t_res_line_list, t_guest_list, t_list_list, new_contrate, resline_exrate, billdate, bonus_array, tot_amt, reservation, res_line, guest, bill, htparam, master, waehrung, zimkateg, arrangement, reslin_queasy, guest_pr, queasy, fixleist, artikel, bill_line, genstat, exrate
        nonlocal curr_resnr, arl_list_reslinnr, t_active_flag, printtype
        nonlocal rline, mbill, mainres


        nonlocal s_list, t_list, t_reservation, t_res_line, t_guest, rline, mbill, mainres
        nonlocal s_list_list, t_list_list, t_reservation_list, t_res_line_list, t_guest_list

        datum:date = None
        co_date:date = None
        add_it:bool = False
        ankunft:date = None
        abreise:date = None
        rm_rate:decimal = to_decimal("0.0")
        argt_rate:decimal = to_decimal("0.0")
        argt_defined:bool = False
        delta:int = 0
        start_date:date = None
        fixed_rate:bool = False
        qty:int = 0
        it_exist:bool = False
        exrate1:decimal = 1
        ex2:decimal = 1
        pax:int = 0
        child1:int = 0
        bill_date:date = None
        curr_zikatnr:int = 0
        curr_no:int = 1000
        do_it:bool = False
        curr_date:date = None
        lrate:decimal = to_decimal("0.0")
        ebdisc_flag:bool = False
        kbdisc_flag:bool = False
        rate_found:bool = False
        early_flag:bool = False
        kback_flag:bool = False
        count_heritage:int = 0
        count_night:int = 0
        dept:int = 0
        loopi:int = 0
        w1 = None
        resline = None
        ct:str = ""
        contcode:str = ""
        W1 =  create_buffer("W1",Waehrung)
        Resline =  create_buffer("Resline",Res_line)

        for resline in db_session.query(Resline).filter(
                 (Resline.resnr == resnr) & (Resline.reslinnr == reslinnr)).order_by(Resline._recid).all():
            ebdisc_flag = re.match(".*ebdisc.*",resline.zimmer_wunsch)
            kbdisc_flag = re.match(".*kbdisc.*",resline.zimmer_wunsch)

            if resline.l_zuordnung[0] != 0:
                curr_zikatnr = resline.l_zuordnung[0]
            else:
                curr_zikatnr = resline.zikatnr

            zimkateg = db_session.query(Zimkateg).filter(
                     (Zimkateg.zikatnr == resline.zikatnr)).first()

            arrangement = db_session.query(Arrangement).filter(
                     (Arrangement.arrangement == resline.arrangement)).first()
            ankunft = resline.ankunft
            abreise = resline.abreise
            fixed_rate = False

            if resline.was_status == 1:
                fixed_rate = True
            co_date = resline.abreise

            if co_date > resline.ankunft:
                co_date = co_date - timedelta(days=1)
            create_bonus()
            for datum in date_range(resline.ankunft,co_date) :
                bill_date = datum
                argt_rate =  to_decimal("0")
                rm_rate =  to_decimal(resline.zipreis)
                pax = resline.erwachs

                if fixed_rate:

                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                             (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == resline.resnr) & (Reslin_queasy.reslinnr == resline.reslinnr) & (datum >= Reslin_queasy.date1) & (datum <= Reslin_queasy.date2)).first()

                    if reslin_queasy:
                        rm_rate =  to_decimal(reslin_queasy.deci1)

                        if reslin_queasy.number3 != 0:
                            pax = reslin_queasy.number3
                    rm_rate, it_exist = usr_prog1(datum, rm_rate)
                else:

                    guest = db_session.query(Guest).filter(
                             (Guest.gastnr == resline.gastnr)).first()

                    guest_pr = db_session.query(Guest_pr).filter(
                             (Guest_pr.gastnr == guest.gastnr)).first()

                    if guest_pr:

                        queasy = db_session.query(Queasy).filter(
                                 (Queasy.key == 18) & (Queasy.number1 == resline.reserve_int)).first()

                        if queasy and queasy.logi3:
                            bill_date = resline.ankunft

                        if new_contrate:

                            if resline_exrate != 0:
                                rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, resline.resnr, resline.reslinnr, guest_pr.code, None, bill_date, resline.ankunft, resline.abreise, resline.reserve_int, arrangement.argtnr, curr_zikatnr, resline.erwachs, resline.kind1, resline.kind2, resline_exrate, resline.betriebsnr))
                            else:
                                rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, resline.resnr, resline.reslinnr, guest_pr.code, None, bill_date, resline.ankunft, resline.abreise, resline.reserve_int, arrangement.argtnr, curr_zikatnr, resline.erwachs, resline.kind1, resline.kind2, resline.reserve_dec, resline.betriebsnr))
                        else:
                            rm_rate, rate_found = get_output(pricecod_rate(resline.resnr, resline.reslinnr, guest_pr.code, bill_date, resline.ankunft, resline.abreise, resline.reserve_int, arrangement.argtnr, curr_zikatnr, resline.erwachs, resline.kind1, resline.kind2, resline.reserve_dec, resline.betriebsnr))
                            rm_rate, it_exist = usr_prog2(datum, rm_rate)

                            if it_exist:
                                rate_found = True

                            if not it_exist and bonus_array[datum - resline.ankunft + 1 - 1] :
                                rm_rate =  to_decimal("0")
                lrate =  to_decimal(rm_rate)

                if datum < billdate:

                    genstat = db_session.query(Genstat).filter(
                             (Genstat.resnr == resnr) & (Genstat.res_int[inc_value(0)] == reslinnr) & (Genstat.datum == datum)).first()

                    if genstat:
                        rm_rate =  to_decimal(genstat.rateLocal)
                    else:

                        exrate = db_session.query(Exrate).filter(
                                 (Exrate.artnr == resline.betriebsnr) & (Exrate.datum == datum)).first()

                        if exrate:
                            lrate =  to_decimal(rm_rate) * to_decimal(exrate.betrag)
                else:

                    waehrung = db_session.query(Waehrung).filter(
                             (Waehrung.waehrungsnr == resline.betriebsnr)).first()

                    if waehrung:
                        lrate =  to_decimal(rm_rate) * to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

                s_list = query(s_list_list, filters=(lambda s_list: s_list.bezeich == arrangement.argt_rgbez and s_list.rmcat == zimkateg.kurzbez and s_list.preis == rm_rate and s_list.lrate == lrate and s_list.datum == datum and s_list.ankunft == resline.ankunft and s_list.abreise == resline.abreise and s_list.erwachs == pax and s_list.kind1 == resline.kind1 and s_list.kind2 == resline.kind2), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.bezeich = arrangement.argt_rgbez
                    s_list.rmcat = zimkateg.kurzbez
                    s_list.preis =  to_decimal(rm_rate)
                    s_list.lrate =  to_decimal(lrate)
                    s_list.datum = datum
                    s_list.ankunft = resline.ankunft
                    s_list.abreise = resline.abreise
                    s_list.erwachs = pax
                    s_list.kind1 = resline.kind1
                    s_list.kind2 = resline.kind2


                s_list.qty = s_list.qty + resline.zimmeranz

                for fixleist in db_session.query(Fixleist).filter(
                         (Fixleist.resnr == resline.resnr) & (Fixleist.reslinnr == resline.reslinnr)).order_by(Fixleist._recid).all():
                    add_it = False
                    argt_rate =  to_decimal("0")

                    if fixleist.sequenz == 1:
                        add_it = True

                    elif fixleist.sequenz == 2 or fixleist.sequenz == 3:

                        if resline.ankunft == datum:
                            add_it = True

                    elif fixleist.sequenz == 4 and get_day(datum) == 1:
                        add_it = True

                    elif fixleist.sequenz == 5 and get_day(datum + 1) == 1:
                        add_it = True

                    elif fixleist.sequenz == 6:

                        if fixleist.lfakt == None:
                            delta = 0
                        else:
                            delta = fixleist.lfakt - resline.ankunft

                            if delta < 0:
                                delta = 0
                        start_date = resline.ankunft + timedelta(days=delta)

                        if (resline.abreise - start_date) < fixleist.dekade:
                            start_date = resline.ankunft

                        if datum <= (start_date + timedelta(days=(fixleist.dekade - 1))):
                            add_it = True

                        if datum < start_date:
                            add_it = False

                    if add_it:

                        artikel = db_session.query(Artikel).filter(
                                 (Artikel.artnr == fixleist.artnr) & (Artikel.departement == fixleist.departement)).first()
                        argt_rate =  to_decimal(fixleist.betrag) * to_decimal(fixleist.number)

                        if not fixed_rate and guest_pr:
                            contcode = guest_pr.code
                            ct = resline.zimmer_wunsch

                            if re.match(r".*\$CODE\$.*",ct, re.IGNORECASE):
                                ct = substring(ct, 0 + get_index(ct, "$CODE$") + 6)
                                contcode = substring(ct, 0, 1 + get_index(ct, ";") - 1)

                            reslin_queasy = db_session.query(Reslin_queasy).filter(
                                     (func.lower(Reslin_queasy.key) == ("argt-line").lower()) & (func.lower(Reslin_queasy.char1) == (contcode).lower()) & (Reslin_queasy.number1 == resline.reserve_int) & (Reslin_queasy.number2 == arrangement.argtnr) & (Reslin_queasy.reslinnr == resline.zikatnr) & (Reslin_queasy.number3 == fixleist.artnr) & (Reslin_queasy.resnr == fixleist.departement) & (bill_date >= Reslin_queasy.date1) & (bill_date <= Reslin_queasy.date2)).first()

                            if reslin_queasy:
                                argt_rate =  to_decimal(reslin_queasy.deci1) * to_decimal(fixleist.number)

                    if argt_rate != 0:

                        s_list = query(s_list_list, filters=(lambda s_list: s_list.bezeich == artikel.bezeich and s_list.preis == (argt_rate / fixleist.number) and s_list.datum == datum and s_list.ankunft == resline.ankunft and s_list.abreise == resline.abreise and s_list.erwachs == pax and s_list.kind1 == resline.kind1 and s_list.kind2 == resline.kind2), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.nr = artikel.artnr
                            s_list.bezeich = artikel.bezeich
                            s_list.preis =  to_decimal(argt_rate) / to_decimal(fixleist.number)
                            s_list.lrate =  to_decimal(argt_rate) / to_decimal(fixleist.number)
                            s_list.datum = datum
                            s_list.ankunft = resline.ankunft
                            s_list.abreise = resline.abreise
                            s_list.erwachs = pax
                            s_list.kind1 = resline.kind1
                            s_list.kind2 = resline.kind2


                        s_list.qty = s_list.qty + (fixleist.number * resline.zimmeranz)

        for s_list in query(s_list_list, sort_by=[("ankunft",False),("datum",False),("bezeich",False),("erwachs",False)]):

            if s_list.nr == 0:

                t_list = query(t_list_list, filters=(lambda t_list: t_list.bezeich == s_list.bezeich and t_list.rmcat == s_list.rmcat and t_list.preis == s_list.preis and t_list.lrate == s_list.lrate and t_list.ankunft == s_list.ankunft and t_list.abreise == s_list.abreise and t_list.erwachs == s_list.erwachs and t_list.kind1 == s_list.kind1 and t_list.kind2 == s_list.kind2), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.nr = s_list.nr
                    t_list.bezeich = s_list.bezeich
                    t_list.rmcat = s_list.rmcat
                    t_list.preis =  to_decimal(s_list.preis)
                    t_list.lrate =  to_decimal(s_list.lrate)
                    t_list.date1 = s_list.datum
                    t_list.ankunft = s_list.ankunft
                    t_list.abreise = s_list.abreise
                    t_list.erwachs = s_list.erwachs
                    t_list.kind1 = s_list.kind1
                    t_list.kind2 = s_list.kind2


                t_list.tage = t_list.tage + 1
                t_list.date2 = s_list.datum

                if s_list.datum == t_list.date1:
                    t_list.qty = t_list.qty + s_list.qty
            else:

                t_list = query(t_list_list, filters=(lambda t_list: t_list.bezeich == s_list.bezeich and t_list.preis == s_list.preis and t_list.lrate == s_list.lrate and t_list.ankunft == s_list.ankunft and t_list.abreise == s_list.abreise and t_list.erwachs == s_list.erwachs and t_list.kind1 == s_list.kind1 and t_list.kind2 == s_list.kind2), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.nr = s_list.nr
                    t_list.bezeich = s_list.bezeich
                    t_list.preis =  to_decimal(s_list.preis)
                    t_list.lrate =  to_decimal(s_list.lrate)
                    t_list.date1 = s_list.datum
                    t_list.ankunft = s_list.ankunft
                    t_list.abreise = s_list.abreise
                    t_list.erwachs = s_list.erwachs
                    t_list.kind1 = s_list.kind1
                    t_list.kind2 = s_list.kind2


                t_list.tage = t_list.tage + 1
                t_list.date2 = s_list.datum

                if s_list.datum == t_list.date1:
                    t_list.qty = t_list.qty + s_list.qty
            s_list_list.remove(s_list)

        for t_list in query(t_list_list):
            t_list.betrag =  to_decimal(t_list.qty) * to_decimal(t_list.tage) * to_decimal(t_list.lrate)

        if rechnr > 0:

            bill_line_obj_list = []
            for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement)).filter(
                     (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line.bill_datum, Bill_line.zeit).all():
                if bill_line._recid in bill_line_obj_list:
                    continue
                else:
                    bill_line_obj_list.append(bill_line._recid)


                do_it = True

                if artikel.artart == 9:

                    arrangement = db_session.query(Arrangement).filter(
                             (Arrangement.argt_artikelnr == artikel.artnr)).first()

                    if not arrangement or arrangement.segmentcode == 0:
                        do_it = False

                if do_it:

                    if re.match(r"Heritage Fee.*",artikel.bezeich, re.IGNORECASE):

                        t_list = query(t_list_list, filters=(lambda t_list: t_list.bezeich == bill_line.bezeich), first=True)

                        if not t_list:
                            t_list = T_list()
                        t_list_list.append(t_list)

                        count_heritage = count_heritage + 1
                        dept = artikel.departement
                        t_list.preis =  to_decimal(bill_line.betrag)
                        t_list.qty = t_list.qty + 1
                        t_list.tage = t_list.tage + 1
                        t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(bill_line.betrag)


                    else:
                        t_list = T_list()
                        t_list_list.append(t_list)

                        t_list.preis =  to_decimal("0")
                        t_list.betrag =  to_decimal(bill_line.betrag)


                    curr_no = curr_no + 1
                    t_list.nr = curr_no
                    t_list.bezeich = bill_line.bezeich
                    t_list.date1 = bill_line.bill_datum

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == resnr) & (Res_line.reslinnr == reslinnr)).first()

        if res_line:
            count_night = res_line.abreise - res_line.ankunft

        if count_heritage < count_night:
            for loopi in range((count_heritage + 1),count_night + 1) :

                artikel = db_session.query(Artikel).filter(
                         (func.lower(Artikel.bezeich).op("~")(("Heritage Fee*".lower().replace("*",".*")))) & (Artikel.departement == dept)).first()

                if artikel:

                    bill_line = db_session.query(Bill_line).filter(
                             (Bill_line.rechnr == bill.rechnr) & (Bill_line.artnr == artikel.artnr)).first()

                    if bill_line:

                        t_list = query(t_list_list, filters=(lambda t_list: t_list.bezeich == bill_line.bezeich), first=True)

                        if t_list:
                            t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(bill_line.betrag)

                        elif not t_list:
                            t_list = T_list()
                            t_list_list.append(t_list)

                            curr_no = curr_no + 1
                            t_list.nr = curr_no
                            t_list.bezeich = bill_line.bezeich
                            t_list.preis =  to_decimal(artikel.epreis)
                            t_list.date1 = res_line.ankunft
                            t_list.betrag =  to_decimal(bill_line.betrag)


                    else:

                        t_list = query(t_list_list, filters=(lambda t_list: t_list.bezeich == artikel.bezeich), first=True)

                        if t_list:
                            t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(artikel.epreis)

                        elif not t_list:
                            t_list = T_list()
                            t_list_list.append(t_list)

                            curr_no = curr_no + 1
                            t_list.nr = curr_no
                            t_list.bezeich = artikel.bezeich
                            t_list.preis =  to_decimal(artikel.epreis)
                            t_list.date1 = res_line.ankunft
                            t_list.betrag =  to_decimal(artikel.epreis)

            for t_list in query(t_list_list, filters=(lambda t_list: t_list.re.match(r"Heritage Fee.*",t_list.bezeich, re.IGNORECASE))):
                t_list.qty = res_line.zimmeranz
                t_list.tage = count_night
                t_list.betrag =  to_decimal(t_list.betrag) * to_decimal(t_list.qty)


    def usr_prog1(bill_date:date, roomrate:decimal):

        nonlocal err_flag, avail_master, avail_bill, reslinnr, master_rechnr, bill_rechnr, mainres_gastnr, t_reservation_list, t_res_line_list, t_guest_list, t_list_list, new_contrate, resline_exrate, billdate, bonus_array, tot_amt, reservation, res_line, guest, bill, htparam, master, waehrung, zimkateg, arrangement, reslin_queasy, guest_pr, queasy, fixleist, artikel, bill_line, genstat, exrate
        nonlocal resnr, curr_resnr, arl_list_reslinnr, t_active_flag, printtype
        nonlocal rline, mbill, mainres


        nonlocal s_list, t_list, t_reservation, t_res_line, t_guest, rline, mbill, mainres
        nonlocal s_list_list, t_list_list, t_reservation_list, t_res_line_list, t_guest_list

        it_exist = False
        prog_str:str = ""
        i:int = 0

        def generate_inner_output():
            return (roomrate, it_exist)


        reslin_queasy = db_session.query(Reslin_queasy).filter(
                 (func.lower(Reslin_queasy.key) == ("rate-prog").lower()) & (Reslin_queasy.number1 == resnr) & (Reslin_queasy.number2 == 0) & (Reslin_queasy.char1 == "") & (Reslin_queasy.reslinnr == 1)).first()

        if reslin_queasy:
            prog_str = reslin_queasy.char3

        if prog_str != "":
            OUTPUT STREAM s1 TO ".\\_rate.p"
            for i in range(1,len(prog_str)  + 1) :
            OUTPUT STREAM s1 CLOSE
            compile value (".\\_rate.p")
            dos silent "del .\\_rate.p"

            if not compiler:ERROR:
                roomrate = get_output(run_program(".\\_rate",(0, resnr, reslinnr, bill_date, roomrate, False)))
                it_exist = True

        return generate_inner_output()


    def usr_prog2(bill_date:date, roomrate:decimal):

        nonlocal err_flag, avail_master, avail_bill, reslinnr, master_rechnr, bill_rechnr, mainres_gastnr, t_reservation_list, t_res_line_list, t_guest_list, t_list_list, new_contrate, resline_exrate, billdate, bonus_array, tot_amt, reservation, res_line, guest, bill, htparam, master, waehrung, zimkateg, arrangement, reslin_queasy, guest_pr, queasy, fixleist, artikel, bill_line, genstat, exrate
        nonlocal resnr, curr_resnr, arl_list_reslinnr, t_active_flag, printtype
        nonlocal rline, mbill, mainres


        nonlocal s_list, t_list, t_reservation, t_res_line, t_guest, rline, mbill, mainres
        nonlocal s_list_list, t_list_list, t_reservation_list, t_res_line_list, t_guest_list

        it_exist = False
        prog_str:str = ""
        i:int = 0

        def generate_inner_output():
            return (roomrate, it_exist)


        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 2) & (Queasy.char1 == guest_pr.code)).first()

        if queasy:
            prog_str = queasy.char3

        if prog_str != "":
            OUTPUT STREAM s1 TO ".\\_rate.p"
            for i in range(1,len(prog_str)  + 1) :
            OUTPUT STREAM s1 CLOSE
            compile value (".\\_rate.p")
            dos silent "del .\\_rate.p"

            if not compiler:ERROR:
                roomrate = get_output(run_program(".\\_rate",(0, resnr, reslinnr, bill_date, roomrate, False)))
                it_exist = True

        return generate_inner_output()


    def create_bonus():

        nonlocal err_flag, avail_master, avail_bill, reslinnr, master_rechnr, bill_rechnr, mainres_gastnr, t_reservation_list, t_res_line_list, t_guest_list, t_list_list, new_contrate, resline_exrate, billdate, bonus_array, tot_amt, reservation, res_line, guest, bill, htparam, master, waehrung, zimkateg, arrangement, reslin_queasy, guest_pr, queasy, fixleist, artikel, bill_line, genstat, exrate
        nonlocal resnr, curr_resnr, arl_list_reslinnr, t_active_flag, printtype
        nonlocal rline, mbill, mainres


        nonlocal s_list, t_list, t_reservation, t_res_line, t_guest, rline, mbill, mainres
        nonlocal s_list_list, t_list_list, t_reservation_list, t_res_line_list, t_guest_list

        i:int = 0
        j:int = 1
        k:int = 0
        n:int = 0
        stay:int = 0
        pay:int = 0
        num_bonus:int = 0
        for i in range(1,999 + 1) :
            bonus_array[i - 1] = False
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

    t_reservation_list.clear()
    t_res_line_list.clear()
    t_guest_list.clear()
    s_list_list.clear()
    t_list_list.clear()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 550)).first()

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    billdate = htparam.fdate

    mainres = db_session.query(Mainres).filter(
             (Mainres.resnr == resnr)).first()
    mainres_gastnr = mainres.gastnr

    rline = db_session.query(Rline).filter(
             (Rline.resnr == resnr) & (Rline.active_flag <= 1)).first()

    if curr_resnr == resnr:
        reslinnr = arl_list_reslinnr
    else:
        reslinnr = rline.reslinnr

    master = db_session.query(Master).filter(
             (Master.resnr == resnr)).first()

    if master:
        master_rechnr = master.rechnr
        avail_master = True

    bill = db_session.query(Bill).filter(
             (Bill.resnr == resnr) & (Bill.reslinnr == reslinnr)).first()

    if bill:
        bill_rechnr = bill.rechnr
        avail_bill = True

    reservation = db_session.query(Reservation).filter(
             (Reservation.resnr == resnr)).first()

    if reservation:
        t_reservation = T_reservation()
        t_reservation_list.append(t_reservation)

        buffer_copy(reservation, t_reservation)

    res_line = db_session.query(Res_line).filter(
             (Res_line.resnr == resnr) & (Res_line.reslinnr == reslinnr)).first()

    if res_line:
        t_res_line = T_res_line()
        t_res_line_list.append(t_res_line)

        buffer_copy(res_line, t_res_line)

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == res_line.gastnr)).first()

        if guest:
            t_guest = T_guest()
            t_guest_list.append(t_guest)

            buffer_copy(guest, t_guest)

    if printtype == 2 or printtype == 3:

        if avail_master:
            read_proforma_inv(resnr, master.rechnr)
        else:

            if avail_bill:
                read_proforma_inv1(resnr, reslinnr, bill.rechnr)
            else:
                read_proforma_inv1(resnr, reslinnr, 0)

    return generate_output()