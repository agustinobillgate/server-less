#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
import re
from functions.ratecode_rate import ratecode_rate
from functions.pricecod_rate import pricecod_rate
from functions.calc_servtaxesbl import calc_servtaxesbl
from sqlalchemy import func
from models import Reservation, Res_line, Guest, Bill, Htparam, Master, Exrate, Waehrung, Bill_line, Artikel, Zimkateg, Arrangement, Reslin_queasy, Guest_pr, Queasy, Fixleist, Billjournal

def arl_list_run_mi_invoice_22_webbl(resnr:int, curr_resnr:int, arl_list_reslinnr:int, t_active_flag:int, printtype:int, split_bill:bool):

    prepare_cache ([Reservation, Res_line, Bill, Htparam, Master, Exrate, Waehrung, Bill_line, Artikel, Zimkateg, Arrangement, Reslin_queasy, Guest_pr, Fixleist, Billjournal])

    err_flag = 0
    avail_master = False
    avail_bill = False
    reslinnr = 1
    master_rechnr = 0
    bill_rechnr = 0
    mainres_gastnr = 0
    t_reservation_data = []
    t_res_line_data = []
    t_guest_data = []
    t_list_data = []
    new_contrate:bool = False
    resline_exrate:Decimal = to_decimal("0.0")
    billdate:date = None
    bonus_array:List[bool] = create_empty_list(999, False)
    tot_amt:Decimal = to_decimal("0.0")
    serv1:Decimal = to_decimal("0.0")
    vat1:Decimal = to_decimal("0.0")
    vat3:Decimal = to_decimal("0.0")
    fact1:Decimal = to_decimal("0.0")
    netto:Decimal = to_decimal("0.0")
    bill_receiver:string = ""
    currency:string = " "
    local_currency:string = " "
    frate:Decimal = 1
    waehrungsnr:int = 1
    price_decimal:int = 0
    tot_deposit:Decimal = to_decimal("0.0")
    t_char:string = ""
    t_resnr:int = 0
    reservation = res_line = guest = bill = htparam = master = exrate = waehrung = bill_line = artikel = zimkateg = arrangement = reslin_queasy = guest_pr = queasy = fixleist = billjournal = None

    s_list = t_list = t_reservation = t_res_line = t_guest = rline = mbill = mainres = b_bill = None

    s_list_data, S_list = create_model("S_list", {"nr":int, "ankunft":date, "abreise":date, "bezeich":string, "rmcat":string, "preis":Decimal, "lrate":Decimal, "datum":date, "qty":int, "erwachs":int, "kind1":int, "kind2":int, "zinr":string, "wabkurz":string}, {"wabkurz": " "})
    t_list_data, T_list = create_model("T_list", {"nr":int, "ankunft":date, "abreise":date, "bezeich":string, "rmcat":string, "preis":Decimal, "lrate":Decimal, "tage":int, "date1":date, "date2":date, "qty":int, "betrag":Decimal, "erwachs":int, "kind1":int, "kind2":int, "vat":Decimal, "svc":Decimal, "zinr":string, "depo_billjour":bool, "resno_billjour":int, "wabkurz":string}, {"wabkurz": " "})
    t_reservation_data, T_reservation = create_model_like(Reservation, {"bill_receiver":string})
    t_res_line_data, T_res_line = create_model_like(Res_line)
    t_guest_data, T_guest = create_model_like(Guest)

    Rline = create_buffer("Rline",Res_line)
    Mbill = create_buffer("Mbill",Bill)
    Mainres = create_buffer("Mainres",Reservation)
    B_bill = create_buffer("B_bill",Bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, avail_master, avail_bill, reslinnr, master_rechnr, bill_rechnr, mainres_gastnr, t_reservation_data, t_res_line_data, t_guest_data, t_list_data, new_contrate, resline_exrate, billdate, bonus_array, tot_amt, serv1, vat1, vat3, fact1, netto, bill_receiver, currency, local_currency, frate, waehrungsnr, price_decimal, tot_deposit, t_char, t_resnr, reservation, res_line, guest, bill, htparam, master, exrate, waehrung, bill_line, artikel, zimkateg, arrangement, reslin_queasy, guest_pr, queasy, fixleist, billjournal
        nonlocal resnr, curr_resnr, arl_list_reslinnr, t_active_flag, printtype, split_bill
        nonlocal rline, mbill, mainres, b_bill


        nonlocal s_list, t_list, t_reservation, t_res_line, t_guest, rline, mbill, mainres, b_bill
        nonlocal s_list_data, t_list_data, t_reservation_data, t_res_line_data, t_guest_data

        return {"err_flag": err_flag, "avail_master": avail_master, "avail_bill": avail_bill, "reslinnr": reslinnr, "master_rechnr": master_rechnr, "bill_rechnr": bill_rechnr, "mainres_gastnr": mainres_gastnr, "t-reservation": t_reservation_data, "t-res-line": t_res_line_data, "t-guest": t_guest_data, "t-list": t_list_data}

    def read_proforma_inv(resnr:int, rechnr:int):

        nonlocal err_flag, avail_master, avail_bill, reslinnr, master_rechnr, bill_rechnr, mainres_gastnr, t_reservation_data, t_res_line_data, t_guest_data, t_list_data, new_contrate, resline_exrate, billdate, bonus_array, tot_amt, serv1, vat1, vat3, fact1, netto, bill_receiver, currency, local_currency, frate, waehrungsnr, price_decimal, tot_deposit, t_char, t_resnr, reservation, res_line, guest, bill, htparam, master, exrate, waehrung, bill_line, artikel, zimkateg, arrangement, reslin_queasy, guest_pr, queasy, fixleist, billjournal
        nonlocal curr_resnr, arl_list_reslinnr, t_active_flag, printtype, split_bill
        nonlocal rline, mbill, mainres, b_bill


        nonlocal s_list, t_list, t_reservation, t_res_line, t_guest, rline, mbill, mainres, b_bill
        nonlocal s_list_data, t_list_data, t_reservation_data, t_res_line_data, t_guest_data

        datum:date = None
        co_date:date = None
        add_it:bool = False
        ankunft:date = None
        abreise:date = None
        rm_rate:Decimal = to_decimal("0.0")
        argt_rate:Decimal = to_decimal("0.0")
        argt_defined:bool = False
        delta:int = 0
        start_date:date = None
        fixed_rate:bool = False
        qty:int = 0
        it_exist:bool = False
        exrate1:Decimal = 1
        ex2:Decimal = 1
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
        depo_flag:bool = False
        w1 = None
        resline = None
        buff_bill_line = None
        buff_art = None
        i:int = 0
        j:int = 0
        qty1:int = 0
        ct:string = ""
        contcode:string = ""
        W1 =  create_buffer("W1",Waehrung)
        Resline =  create_buffer("Resline",Res_line)
        Buff_bill_line =  create_buffer("Buff_bill_line",Bill_line)
        Buff_art =  create_buffer("Buff_art",Artikel)

        for resline in db_session.query(Resline).filter(
                 (Resline.resnr == resnr) & (Resline.active_flag < 2) & (Resline.resstatus != 12) & (Resline.resstatus != 9) & (Resline.resstatus != 10) & (Resline.resstatus != 99)).order_by(Resline._recid).all():
            ebdisc_flag = matches(resline.zimmer_wunsch, ("*ebdisc*"))
            kbdisc_flag = matches(resline.zimmer_wunsch, ("*kbdisc*"))

            if resline.l_zuordnung[0] != 0:
                curr_zikatnr = resline.l_zuordnung[0]
            else:
                curr_zikatnr = resline.zikatnr

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, resline.zikatnr)]})

            arrangement = get_cache (Arrangement, {"arrangement": [(eq, resline.arrangement)]})
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

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, resline.resnr)],"reslinnr": [(eq, resline.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if reslin_queasy:
                        rm_rate =  to_decimal(reslin_queasy.deci1)

                        if reslin_queasy.number3 != 0:
                            pax = reslin_queasy.number3
                else:

                    guest = get_cache (Guest, {"gastnr": [(eq, resline.gastnr)]})

                    guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, guest.gastnr)]})

                    if guest_pr:

                        queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, resline.reserve_int)]})

                        if queasy and queasy.logi3:
                            bill_date = resline.ankunft

                        if new_contrate:

                            if resline_exrate != 0:
                                rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, resline.resnr, resline.reslinnr, guest_pr.code, None, bill_date, resline.ankunft, resline.abreise, resline.reserve_int, arrangement.argtnr, curr_zikatnr, resline.erwachs, resline.kind1, resline.kind2, resline_exrate, resline.betriebsnr))
                            else:
                                rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, resline.resnr, resline.reslinnr, guest_pr.code, None, bill_date, resline.ankunft, resline.abreise, resline.reserve_int, arrangement.argtnr, curr_zikatnr, resline.erwachs, resline.kind1, resline.kind2, resline.reserve_dec, resline.betriebsnr))
                        else:
                            rm_rate, rate_found = get_output(pricecod_rate(resline.resnr, resline.reslinnr, guest_pr.code, bill_date, resline.ankunft, resline.abreise, resline.reserve_int, arrangement.argtnr, curr_zikatnr, resline.erwachs, resline.kind1, resline.kind2, resline.reserve_dec, resline.betriebsnr))

                            if it_exist:
                                rate_found = True

                            if not it_exist and bonus_array[datum - resline.ankunft + 1 - 1] :
                                rm_rate =  to_decimal("0")

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, resline.betriebsnr)]})

                if waehrung:
                    currency = waehrung.wabkurz
                    frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                    waehrungsnr = waehrung.waehrungsnr

                s_list = query(s_list_data, filters=(lambda s_list: s_list.bezeich == arrangement.argt_rgbez and s_list.rmcat == zimkateg.kurzbez and s_list.preis == rm_rate and s_list.datum == datum and s_list.ankunft == resline.ankunft and s_list.abreise == resline.abreise and s_list.erwachs == pax and s_list.kind1 == resline.kind1 and s_list.kind2 == resline.kind2 and s_list.wabkurz.lower()  == (currency).lower()), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.bezeich = arrangement.argt_rgbez
                    s_list.rmcat = zimkateg.kurzbez
                    s_list.preis =  to_decimal(rm_rate)
                    s_list.datum = datum
                    s_list.ankunft = resline.ankunft
                    s_list.abreise = resline.abreise
                    s_list.erwachs = pax
                    s_list.kind1 = resline.kind1
                    s_list.kind2 = resline.kind2
                    s_list.zinr = resline.zinr
                    s_list.wabkurz = currency
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

                        artikel = get_cache (Artikel, {"artnr": [(eq, fixleist.artnr)],"departement": [(eq, fixleist.departement)]})
                        argt_rate =  to_decimal(fixleist.betrag) * to_decimal(fixleist.number)

                        if not fixed_rate and guest_pr:
                            contcode = guest_pr.code
                            ct = resline.zimmer_wunsch

                            if matches(ct,r"*$CODE$*"):
                                ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                                contcode = substring(ct, 0, get_index(ct, ";") - 1)

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, resline.reserve_int)],"number2": [(eq, arrangement.argtnr)],"reslinnr": [(eq, resline.zikatnr)],"number3": [(eq, fixleist.artnr)],"resnr": [(eq, fixleist.departement)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

                            if reslin_queasy:
                                argt_rate =  to_decimal(reslin_queasy.deci1) * to_decimal(fixleist.number)

                    if argt_rate != 0:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.bezeich == artikel.bezeich and s_list.preis == (argt_rate / fixleist.number) and s_list.datum == datum and s_list.ankunft == resline.ankunft and s_list.abreise == resline.abreise and s_list.erwachs == pax and s_list.kind1 == resline.kind1 and s_list.kind2 == resline.kind2 and s_list.wabkurz.lower()  == (currency).lower()), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.nr = artikel.artnr
                            s_list.bezeich = artikel.bezeich
                            s_list.preis =  to_decimal(argt_rate) / to_decimal(fixleist.number)
                            s_list.datum = datum
                            s_list.ankunft = resline.ankunft
                            s_list.abreise = resline.abreise
                            s_list.erwachs = pax
                            s_list.kind1 = resline.kind1
                            s_list.kind2 = resline.kind2
                            s_list.wabkurz = currency
                        s_list.qty = s_list.qty + (fixleist.number * resline.zimmeranz)

        for s_list in query(s_list_data, sort_by=[("ankunft",False),("datum",False),("bezeich",False),("erwachs",False)]):

            if s_list.nr == 0:

                t_list = query(t_list_data, filters=(lambda t_list: t_list.bezeich == s_list.bezeich and t_list.rmcat == s_list.rmcat and t_list.preis == s_list.preis and t_list.ankunft == s_list.ankunft and t_list.abreise == s_list.abreise and t_list.erwachs == s_list.erwachs and t_list.kind1 == s_list.kind1 and t_list.kind2 == s_list.kind2 and t_list.wabkurz == s_list.wabkurz), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_data.append(t_list)

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
                    t_list.zinr = s_list.zinr
                    t_list.wabkurz = s_list.wabkurz

                if s_list.qty >= t_list.qty:
                    t_list.tage = t_list.tage + 1
                t_list.date2 = s_list.datum

                if s_list.datum == t_list.date1:
                    t_list.qty = t_list.qty + s_list.qty

                if s_list.qty != t_list.qty and s_list.preis == t_list.preis:
                    qty1 = t_list.qty
                    t_list = T_list()
                    t_list_data.append(t_list)

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
                    t_list.zinr = s_list.zinr
                    t_list.wabkurz = s_list.wabkurz

                    if s_list.qty > qty1:
                        j = s_list.qty - qty1
                        t_list.qty = j


                    else:
                        j = qty1 - s_list.qty
                        t_list.qty = s_list.qty


            else:

                t_list = query(t_list_data, filters=(lambda t_list: t_list.bezeich == s_list.bezeich and t_list.preis == s_list.preis and t_list.ankunft == s_list.ankunft and t_list.abreise == s_list.abreise and t_list.erwachs == s_list.erwachs and t_list.kind1 == s_list.kind1 and t_list.kind2 == s_list.kind2 and t_list.wabkurz == s_list.wabkurz), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.nr = s_list.nr
                    t_list.bezeich = s_list.bezeich
                    t_list.preis =  to_decimal(s_list.preis)
                    t_list.date1 = s_list.datum
                    t_list.ankunft = s_list.ankunft
                    t_list.abreise = s_list.abreise
                    t_list.erwachs = s_list.erwachs
                    t_list.kind1 = s_list.kind1
                    t_list.kind2 = s_list.kind2
                    t_list.wabkurz = s_list.wabkurz
                t_list.tage = t_list.tage + 1
                t_list.date2 = s_list.datum

                if s_list.datum == t_list.date1:
                    t_list.qty = t_list.qty + s_list.qty
            s_list_data.remove(s_list)
        tot_amt =  to_decimal("0")

        for t_list in query(t_list_data):
            t_list.betrag =  to_decimal(t_list.qty) * to_decimal(t_list.tage) * to_decimal(t_list.preis)
            tot_amt =  to_decimal(tot_amt) + to_decimal(t_list.betrag)

        if rechnr > 0:

            bill_line_obj_list = {}
            bill_line = Bill_line()
            artikel = Artikel()
            for bill_line.bezeich, bill_line.betrag, bill_line.bill_datum, bill_line._recid, artikel.bezeich, artikel.artnr, artikel.departement, artikel.epreis, artikel.artart, artikel._recid in db_session.query(Bill_line.bezeich, Bill_line.betrag, Bill_line.bill_datum, Bill_line._recid, Artikel.bezeich, Artikel.artnr, Artikel.departement, Artikel.epreis, Artikel.artart, Artikel._recid).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement)).filter(
                     (Bill_line.rechnr == rechnr)).order_by(Bill_line.bill_datum, Bill_line.zeit).all():
                if bill_line_obj_list.get(bill_line._recid):
                    continue
                else:
                    bill_line_obj_list[bill_line._recid] = True


                do_it = True
                serv1 =  to_decimal("0")
                vat1 =  to_decimal("0")
                vat3 =  to_decimal("0")
                fact1 =  to_decimal("0")

                if artikel.artart == 9:

                    arrangement = get_cache (Arrangement, {"argt_artikelnr": [(eq, artikel.artnr)]})

                    if not arrangement or arrangement.segmentcode == 0:
                        do_it = False

                if do_it:

                    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

                    if matches(artikel.bezeich,r"Heritage Fee*"):

                        t_list = query(t_list_data, filters=(lambda t_list: t_list.bezeich == bill_line.bezeich), first=True)

                        if not t_list:
                            t_list = T_list()
                            t_list_data.append(t_list)

                        count_heritage = count_heritage + 1
                        dept = artikel.departement
                        t_list.ankunft = res_line.ankunft
                        t_list.abreise = res_line.abreise
                        t_list.preis =  to_decimal(bill_line.betrag)
                        t_list.qty = t_list.qty + 1
                        t_list.tage = t_list.tage + 1
                        t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(bill_line.betrag)


                    else:
                        t_list = T_list()
                        t_list_data.append(t_list)

                        t_list.preis =  to_decimal("0")
                        t_list.betrag =  to_decimal(bill_line.betrag)
                        t_list.ankunft = res_line.ankunft
                        t_list.abreise = res_line.abreise


                    curr_no = curr_no + 1
                    t_list.nr = curr_no
                    t_list.bezeich = bill_line.bezeich
                    t_list.date1 = bill_line.bill_datum


                    serv1, vat1, vat3, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_line.bill_datum))
                    netto =  to_decimal(bill_line.betrag) / to_decimal(fact1)
                    t_list.vat =  to_decimal(netto) * to_decimal((vat1) + to_decimal(vat3) )


        else:

            billjournal_obj_list = {}
            billjournal = Billjournal()
            artikel = Artikel()
            for billjournal.bezeich, billjournal.betrag, billjournal.bill_datum, billjournal._recid, artikel.bezeich, artikel.artnr, artikel.departement, artikel.epreis, artikel.artart, artikel._recid in db_session.query(Billjournal.bezeich, Billjournal.betrag, Billjournal.bill_datum, Billjournal._recid, Artikel.bezeich, Artikel.artnr, Artikel.departement, Artikel.epreis, Artikel.artart, Artikel._recid).join(Artikel,(Artikel.artnr == Billjournal.artnr) & (Artikel.departement == Billjournal.departement)).filter(
                     (Billjournal.rechnr == 0) & (Billjournal.anzahl != 0) & (matches(Billjournal.bezeich,"*Deposit #*"))).order_by(Billjournal._recid).all():
                if billjournal_obj_list.get(billjournal._recid):
                    continue
                else:
                    billjournal_obj_list[billjournal._recid] = True


                t_char = entry(1, billjournal.bezeich, "#")
                t_resnr = to_int(entry(0, t_char, "]"))

                if t_resnr == resnr:
                    serv1 =  to_decimal("0")
                    vat1 =  to_decimal("0")
                    vat3 =  to_decimal("0")
                    fact1 =  to_decimal("0")

                    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})
                    t_list = T_list()
                    t_list_data.append(t_list)

                    curr_no = curr_no + 1
                    t_list.nr = curr_no
                    t_list.betrag =  to_decimal(billjournal.betrag)
                    t_list.bezeich = billjournal.bezeich
                    t_list.date1 = billjournal.bill_datum
                    t_list.ankunft = res_line.ankunft
                    t_list.abreise = res_line.abreise


                    serv1, vat1, vat3, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, billjournal.bill_datum))
                    netto =  to_decimal(billjournal.betrag) / to_decimal(fact1)
                    t_list.vat =  to_decimal(netto) * to_decimal((vat1) + to_decimal(vat3) )


                    t_list.depo_billjour = True
                    t_list.resno_billjour = t_resnr

            billjournal = db_session.query(Billjournal).filter(
                     (Billjournal.billjou_ref == t_resnr) & (matches(Billjournal.bezeich,"*Refund #*"))).first()

            for t_list in query(t_list_data, filters=(lambda t_list: t_list.depo_billjour), sort_by=[("nr",False)]):
                tot_deposit =  to_decimal(tot_deposit) + to_decimal(t_list.betrag)

                if billjournal:

                    if (t_list.betrag + billjournal.betrag) == 0:
                        t_list_data.remove(t_list)
                        tot_deposit =  to_decimal("0")

                        curr_recid = billjournal._recid
                        billjournal = db_session.query(Billjournal).filter(
                                 (Billjournal.billjou_ref == t_resnr) & (matches(Billjournal.bezeich,"*Refund #*")) & (Billjournal._recid > curr_recid)).first()

                    elif (tot_deposit + billjournal.betrag) == 0:

                        for buff_t in query(t_list_data, filters=(lambda buff_t: buff_t.depo_billjour  and buff_t.nr <= t_list.nr), sort_by=[("nr",False)]):
                            t_list_data.remove(buff_t)
                        tot_deposit =  to_decimal("0")

                        curr_recid = billjournal._recid
                        billjournal = db_session.query(Billjournal).filter(
                                 (Billjournal.billjou_ref == t_resnr) & (matches(Billjournal.bezeich,"*Refund #*")) & (Billjournal._recid > curr_recid)).first()

        res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

        if res_line:
            count_night = (res_line.abreise - res_line.ankunft).days

        if count_heritage < count_night:
            for loopi in range((count_heritage + 1),count_night + 1) :

                artikel = db_session.query(Artikel).filter(
                         (matches(Artikel.bezeich,"Heritage Fee*")) & (Artikel.departement == dept)).first()

                if artikel:

                    bill_line = get_cache (Bill_line, {"rechnr": [(eq, bill.rechnr)],"artnr": [(eq, artikel.artnr)]})

                    if bill_line:

                        t_list = query(t_list_data, filters=(lambda t_list: t_list.bezeich == bill_line.bezeich), first=True)

                        if t_list:
                            pass
                            t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(bill_line.betrag)


                            pass

                        elif not t_list:
                            t_list = T_list()
                            t_list_data.append(t_list)

                            curr_no = curr_no + 1
                            t_list.nr = curr_no
                            t_list.bezeich = bill_line.bezeich
                            t_list.preis =  to_decimal(artikel.epreis)
                            t_list.date1 = res_line.ankunft
                            t_list.betrag =  to_decimal(bill_line.betrag)
                            t_list.ankunft = res_line.ankunft
                            t_list.abreise = res_line.abreise


                    else:

                        t_list = query(t_list_data, filters=(lambda t_list: t_list.bezeich == artikel.bezeich), first=True)

                        if t_list:
                            pass
                            t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(artikel.epreis)


                            pass

                        elif not t_list:
                            t_list = T_list()
                            t_list_data.append(t_list)

                            curr_no = curr_no + 1
                            t_list.nr = curr_no
                            t_list.bezeich = artikel.bezeich
                            t_list.preis =  to_decimal(artikel.epreis)
                            t_list.date1 = res_line.ankunft
                            t_list.betrag =  to_decimal(artikel.epreis)
                            t_list.betrag =  to_decimal(artikel.epreis)
                            t_list.ankunft = res_line.ankunft
                            t_list.abreise = res_line.abreise

            for t_list in query(t_list_data, filters=(lambda t_list: matches(t_list.bezeich,r"Heritage Fee*"))):
                t_list.qty = res_line.zimmeranz
                t_list.tage = count_night
                t_list.betrag =  to_decimal(t_list.betrag) * to_decimal(t_list.qty)


    def read_proforma_inv1(resnr:int, reslinnr:int, rechnr:int):

        nonlocal err_flag, avail_master, avail_bill, master_rechnr, bill_rechnr, mainres_gastnr, t_reservation_data, t_res_line_data, t_guest_data, t_list_data, new_contrate, resline_exrate, billdate, bonus_array, tot_amt, serv1, vat1, vat3, fact1, netto, bill_receiver, currency, local_currency, frate, waehrungsnr, price_decimal, tot_deposit, t_char, t_resnr, reservation, res_line, guest, bill, htparam, master, exrate, waehrung, bill_line, artikel, zimkateg, arrangement, reslin_queasy, guest_pr, queasy, fixleist, billjournal
        nonlocal curr_resnr, arl_list_reslinnr, t_active_flag, printtype, split_bill
        nonlocal rline, mbill, mainres, b_bill


        nonlocal s_list, t_list, t_reservation, t_res_line, t_guest, rline, mbill, mainres, b_bill
        nonlocal s_list_data, t_list_data, t_reservation_data, t_res_line_data, t_guest_data

        datum:date = None
        co_date:date = None
        add_it:bool = False
        ankunft:date = None
        abreise:date = None
        rm_rate:Decimal = to_decimal("0.0")
        argt_rate:Decimal = to_decimal("0.0")
        argt_defined:bool = False
        delta:int = 0
        start_date:date = None
        fixed_rate:bool = False
        qty:int = 0
        it_exist:bool = False
        exrate1:Decimal = 1
        ex2:Decimal = 1
        pax:int = 0
        child1:int = 0
        bill_date:date = None
        curr_zikatnr:int = 0
        curr_no:int = 1000
        do_it:bool = False
        curr_date:date = None
        lrate:Decimal = to_decimal("0.0")
        ebdisc_flag:bool = False
        kbdisc_flag:bool = False
        rate_found:bool = False
        early_flag:bool = False
        kback_flag:bool = False
        count_heritage:int = 0
        count_night:int = 0
        dept:int = 0
        loopi:int = 0
        depo_flag:bool = False
        w1 = None
        resline = None
        buff_bill_line = None
        buff_art = None
        ct:string = ""
        contcode:string = ""
        W1 =  create_buffer("W1",Waehrung)
        Resline =  create_buffer("Resline",Res_line)
        Buff_bill_line =  create_buffer("Buff_bill_line",Bill_line)
        Buff_art =  create_buffer("Buff_art",Artikel)

        for resline in db_session.query(Resline).filter(
                 (Resline.resnr == resnr) & (Resline.reslinnr == reslinnr)).order_by(Resline._recid).all():
            ebdisc_flag = matches(resline.zimmer_wunsch, ("*ebdisc*"))
            kbdisc_flag = matches(resline.zimmer_wunsch, ("*kbdisc*"))

            if resline.l_zuordnung[0] != 0:
                curr_zikatnr = resline.l_zuordnung[0]
            else:
                curr_zikatnr = resline.zikatnr

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, resline.zikatnr)]})

            arrangement = get_cache (Arrangement, {"arrangement": [(eq, resline.arrangement)]})
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

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, resline.resnr)],"reslinnr": [(eq, resline.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if reslin_queasy:
                        rm_rate =  to_decimal(reslin_queasy.deci1)

                        if reslin_queasy.number3 != 0:
                            pax = reslin_queasy.number3
                else:

                    guest = get_cache (Guest, {"gastnr": [(eq, resline.gastnr)]})

                    guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, guest.gastnr)]})

                    if guest_pr:

                        queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, resline.reserve_int)]})

                        if queasy and queasy.logi3:
                            bill_date = resline.ankunft

                        if new_contrate:

                            if resline_exrate != 0:
                                rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, resline.resnr, resline.reslinnr, guest_pr.code, None, bill_date, resline.ankunft, resline.abreise, resline.reserve_int, arrangement.argtnr, curr_zikatnr, resline.erwachs, resline.kind1, resline.kind2, resline_exrate, resline.betriebsnr))
                            else:
                                rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, resline.resnr, resline.reslinnr, guest_pr.code, None, bill_date, resline.ankunft, resline.abreise, resline.reserve_int, arrangement.argtnr, curr_zikatnr, resline.erwachs, resline.kind1, resline.kind2, resline.reserve_dec, resline.betriebsnr))
                        else:
                            rm_rate, rate_found = get_output(pricecod_rate(resline.resnr, resline.reslinnr, guest_pr.code, bill_date, resline.ankunft, resline.abreise, resline.reserve_int, arrangement.argtnr, curr_zikatnr, resline.erwachs, resline.kind1, resline.kind2, resline.reserve_dec, resline.betriebsnr))

                            if it_exist:
                                rate_found = True

                            if not it_exist and bonus_array[datum - resline.ankunft + 1 - 1] :
                                rm_rate =  to_decimal("0")
                lrate =  to_decimal(rm_rate)

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, resline.betriebsnr)]})

                if waehrung:
                    currency = waehrung.wabkurz
                    frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                    waehrungsnr = waehrung.waehrungsnr

                s_list = query(s_list_data, filters=(lambda s_list: s_list.bezeich == arrangement.argt_rgbez and s_list.rmcat == zimkateg.kurzbez and s_list.preis == rm_rate and s_list.lrate == lrate and s_list.datum == datum and s_list.ankunft == resline.ankunft and s_list.abreise == resline.abreise and s_list.erwachs == pax and s_list.kind1 == resline.kind1 and s_list.kind2 == resline.kind2 and s_list.wabkurz.lower()  == (currency).lower()), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

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
                    s_list.zinr = resline.zinr
                    s_list.wabkurz = currency


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

                        artikel = get_cache (Artikel, {"artnr": [(eq, fixleist.artnr)],"departement": [(eq, fixleist.departement)]})
                        argt_rate =  to_decimal(fixleist.betrag) * to_decimal(fixleist.number)

                        if not fixed_rate and guest_pr:
                            contcode = guest_pr.code
                            ct = resline.zimmer_wunsch

                            if matches(ct,r"*$CODE$*"):
                                ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                                contcode = substring(ct, 0, get_index(ct, ";") - 1)

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, resline.reserve_int)],"number2": [(eq, arrangement.argtnr)],"reslinnr": [(eq, resline.zikatnr)],"number3": [(eq, fixleist.artnr)],"resnr": [(eq, fixleist.departement)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

                            if reslin_queasy:
                                argt_rate =  to_decimal(reslin_queasy.deci1) * to_decimal(fixleist.number)

                    if argt_rate != 0:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.bezeich == artikel.bezeich and s_list.preis == (argt_rate / fixleist.number) and s_list.datum == datum and s_list.ankunft == resline.ankunft and s_list.abreise == resline.abreise and s_list.erwachs == pax and s_list.kind1 == resline.kind1 and s_list.kind2 == resline.kind2 and s_list.wabkurz.lower()  == (currency).lower()), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

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
                            s_list.wabkurz = currency


                        s_list.qty = s_list.qty + (fixleist.number * resline.zimmeranz)

        for s_list in query(s_list_data, sort_by=[("ankunft",False),("datum",False),("bezeich",False),("erwachs",False)]):

            if s_list.nr == 0:

                t_list = query(t_list_data, filters=(lambda t_list: t_list.bezeich == s_list.bezeich and t_list.rmcat == s_list.rmcat and t_list.preis == s_list.preis and t_list.lrate == s_list.lrate and t_list.ankunft == s_list.ankunft and t_list.abreise == s_list.abreise and t_list.erwachs == s_list.erwachs and t_list.kind1 == s_list.kind1 and t_list.kind2 == s_list.kind2 and t_list.wabkurz == s_list.wabkurz), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_data.append(t_list)

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
                    t_list.zinr = s_list.zinr
                    t_list.wabkurz = s_list.wabkurz


                t_list.tage = t_list.tage + 1
                t_list.date2 = s_list.datum

                if s_list.datum == t_list.date1:
                    t_list.qty = t_list.qty + s_list.qty
            else:

                t_list = query(t_list_data, filters=(lambda t_list: t_list.bezeich == s_list.bezeich and t_list.preis == s_list.preis and t_list.lrate == s_list.lrate and t_list.ankunft == s_list.ankunft and t_list.abreise == s_list.abreise and t_list.erwachs == s_list.erwachs and t_list.kind1 == s_list.kind1 and t_list.kind2 == s_list.kind2 and t_list.wabkurz == s_list.wabkurz), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_data.append(t_list)

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
                    t_list.wabkurz = s_list.wabkurz


                t_list.tage = t_list.tage + 1
                t_list.date2 = s_list.datum

                if s_list.datum == t_list.date1:
                    t_list.qty = t_list.qty + s_list.qty
            s_list_data.remove(s_list)

        for t_list in query(t_list_data):
            t_list.betrag =  to_decimal(t_list.qty) * to_decimal(t_list.tage) * to_decimal(t_list.lrate)

        if rechnr > 0:

            if not split_bill:

                bill_line_obj_list = {}
                bill_line = Bill_line()
                artikel = Artikel()
                for bill_line.bezeich, bill_line.betrag, bill_line.bill_datum, bill_line._recid, artikel.bezeich, artikel.artnr, artikel.departement, artikel.epreis, artikel.artart, artikel._recid in db_session.query(Bill_line.bezeich, Bill_line.betrag, Bill_line.bill_datum, Bill_line._recid, Artikel.bezeich, Artikel.artnr, Artikel.departement, Artikel.epreis, Artikel.artart, Artikel._recid).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement)).filter(
                         (Bill_line.rechnr == rechnr)).order_by(Bill_line.bill_datum, Bill_line.zeit).all():
                    if bill_line_obj_list.get(bill_line._recid):
                        continue
                    else:
                        bill_line_obj_list[bill_line._recid] = True


                    do_it = True
                    serv1 =  to_decimal("0")
                    vat1 =  to_decimal("0")
                    vat3 =  to_decimal("0")
                    fact1 =  to_decimal("0")

                    if artikel.artart == 9:

                        arrangement = get_cache (Arrangement, {"argt_artikelnr": [(eq, artikel.artnr)]})

                        if not arrangement or arrangement.segmentcode == 0:
                            do_it = False

                    if do_it:

                        res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

                        if matches(artikel.bezeich,r"Heritage Fee*"):

                            t_list = query(t_list_data, filters=(lambda t_list: t_list.bezeich == bill_line.bezeich), first=True)

                            if not t_list:
                                t_list = T_list()
                                t_list_data.append(t_list)

                            count_heritage = count_heritage + 1
                            dept = artikel.departement
                            t_list.preis =  to_decimal(bill_line.betrag)
                            t_list.qty = t_list.qty + 1
                            t_list.tage = t_list.tage + 1
                            t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(bill_line.betrag)
                            t_list.ankunft = res_line.ankunft
                            t_list.abreise = res_line.abreise


                        else:
                            t_list = T_list()
                            t_list_data.append(t_list)

                            t_list.preis =  to_decimal("0")
                            t_list.betrag =  to_decimal(bill_line.betrag)
                            t_list.ankunft = res_line.ankunft
                            t_list.abreise = res_line.abreise


                        curr_no = curr_no + 1
                        t_list.nr = curr_no
                        t_list.bezeich = bill_line.bezeich
                        t_list.date1 = bill_line.bill_datum


                        serv1, vat1, vat3, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_line.bill_datum))
                        netto =  to_decimal(bill_line.betrag) / to_decimal(fact1)
                        t_list.vat =  to_decimal(netto) * to_decimal((vat1) + to_decimal(vat3) )


            else:

                for b_bill in db_session.query(B_bill).filter(
                         (B_bill.resnr == resnr)).order_by(B_bill._recid).all():

                    bill_line_obj_list = {}
                    bill_line = Bill_line()
                    artikel = Artikel()
                    for bill_line.bezeich, bill_line.betrag, bill_line.bill_datum, bill_line._recid, artikel.bezeich, artikel.artnr, artikel.departement, artikel.epreis, artikel.artart, artikel._recid in db_session.query(Bill_line.bezeich, Bill_line.betrag, Bill_line.bill_datum, Bill_line._recid, Artikel.bezeich, Artikel.artnr, Artikel.departement, Artikel.epreis, Artikel.artart, Artikel._recid).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement)).filter(
                             (Bill_line.rechnr == b_bill.rechnr)).order_by(Bill_line.bill_datum, Bill_line.zeit).all():
                        if bill_line_obj_list.get(bill_line._recid):
                            continue
                        else:
                            bill_line_obj_list[bill_line._recid] = True


                        do_it = True
                        serv1 =  to_decimal("0")
                        vat1 =  to_decimal("0")
                        vat3 =  to_decimal("0")
                        fact1 =  to_decimal("0")

                        if artikel.artart == 9:

                            arrangement = get_cache (Arrangement, {"argt_artikelnr": [(eq, artikel.artnr)]})

                            if not arrangement or arrangement.segmentcode == 0:
                                do_it = False

                        if do_it:

                            res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

                            if matches(artikel.bezeich,r"Heritage Fee*"):

                                t_list = query(t_list_data, filters=(lambda t_list: t_list.bezeich == bill_line.bezeich), first=True)

                                if not t_list:
                                    t_list = T_list()
                                    t_list_data.append(t_list)

                                count_heritage = count_heritage + 1
                                dept = artikel.departement
                                t_list.preis =  to_decimal(bill_line.betrag)
                                t_list.qty = t_list.qty + 1
                                t_list.tage = t_list.tage + 1
                                t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(bill_line.betrag)
                                t_list.ankunft = res_line.ankunft
                                t_list.abreise = res_line.abreise


                            else:
                                t_list = T_list()
                                t_list_data.append(t_list)

                                t_list.preis =  to_decimal("0")
                                t_list.betrag =  to_decimal(bill_line.betrag)
                                t_list.ankunft = res_line.ankunft
                                t_list.abreise = res_line.abreise


                            curr_no = curr_no + 1
                            t_list.nr = curr_no
                            t_list.bezeich = bill_line.bezeich
                            t_list.date1 = bill_line.bill_datum


                            serv1, vat1, vat3, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_line.bill_datum))
                            netto =  to_decimal(bill_line.betrag) / to_decimal(fact1)
                            t_list.vat =  to_decimal(netto) * to_decimal((vat1) + to_decimal(vat3) )


        else:

            billjournal_obj_list = {}
            billjournal = Billjournal()
            artikel = Artikel()
            for billjournal.bezeich, billjournal.betrag, billjournal.bill_datum, billjournal._recid, artikel.bezeich, artikel.artnr, artikel.departement, artikel.epreis, artikel.artart, artikel._recid in db_session.query(Billjournal.bezeich, Billjournal.betrag, Billjournal.bill_datum, Billjournal._recid, Artikel.bezeich, Artikel.artnr, Artikel.departement, Artikel.epreis, Artikel.artart, Artikel._recid).join(Artikel,(Artikel.artnr == Billjournal.artnr) & (Artikel.departement == Billjournal.departement)).filter(
                     (Billjournal.rechnr == 0) & (Billjournal.anzahl != 0) & (matches(Billjournal.bezeich,"*Deposit #*"))).order_by(Billjournal._recid).all():
                if billjournal_obj_list.get(billjournal._recid):
                    continue
                else:
                    billjournal_obj_list[billjournal._recid] = True


                t_char = entry(1, billjournal.bezeich, "#")
                t_resnr = to_int(entry(0, t_char, "]"))

                if t_resnr == resnr:
                    serv1 =  to_decimal("0")
                    vat1 =  to_decimal("0")
                    vat3 =  to_decimal("0")
                    fact1 =  to_decimal("0")

                    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})
                    t_list = T_list()
                    t_list_data.append(t_list)

                    curr_no = curr_no + 1
                    t_list.nr = curr_no
                    t_list.betrag =  to_decimal(billjournal.betrag)
                    t_list.bezeich = billjournal.bezeich
                    t_list.date1 = billjournal.bill_datum
                    t_list.ankunft = res_line.ankunft
                    t_list.abreise = res_line.abreise


                    serv1, vat1, vat3, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, billjournal.bill_datum))
                    netto =  to_decimal(billjournal.betrag) / to_decimal(fact1)
                    t_list.vat =  to_decimal(netto) * to_decimal((vat1) + to_decimal(vat3) )


                    t_list.depo_billjour = True
                    t_list.resno_billjour = t_resnr

            billjournal = db_session.query(Billjournal).filter(
                     (Billjournal.billjou_ref == t_resnr) & (matches(Billjournal.bezeich,"*Refund #*"))).first()

            for t_list in query(t_list_data, filters=(lambda t_list: t_list.depo_billjour), sort_by=[("nr",False)]):
                tot_deposit =  to_decimal(tot_deposit) + to_decimal(t_list.betrag)

                if billjournal:

                    if (t_list.betrag + billjournal.betrag) == 0:
                        t_list_data.remove(t_list)
                        tot_deposit =  to_decimal("0")

                        curr_recid = billjournal._recid
                        billjournal = db_session.query(Billjournal).filter(
                                 (Billjournal.billjou_ref == t_resnr) & (matches(Billjournal.bezeich,"*Refund #*")) & (Billjournal._recid > curr_recid)).first()

                    elif (tot_deposit + billjournal.betrag) == 0:

                        for buff_t in query(buff_t_data, filters=(lambda buff_t: buff_t.depo_billjour  and buff_t.NR <= t_list.nr), sort_by=[("nr",False)]):
                            buff_t_data.remove(buff_t)
                        tot_deposit =  to_decimal("0")

                        curr_recid = billjournal._recid
                        billjournal = db_session.query(Billjournal).filter(
                                 (Billjournal.billjou_ref == t_resnr) & (matches(Billjournal.bezeich,"*Refund #*")) & (Billjournal._recid > curr_recid)).first()

        res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

        if res_line:
            count_night = (res_line.abreise - res_line.ankunft).days

        if count_heritage < count_night:
            for loopi in range((count_heritage + 1),count_night + 1) :

                artikel = db_session.query(Artikel).filter(
                         (matches(Artikel.bezeich,"Heritage Fee*")) & (Artikel.departement == dept)).first()

                if artikel:

                    bill_line = get_cache (Bill_line, {"rechnr": [(eq, bill.rechnr)],"artnr": [(eq, artikel.artnr)]})

                    if bill_line:

                        t_list = query(t_list_data, filters=(lambda t_list: t_list.bezeich == bill_line.bezeich), first=True)

                        if t_list:
                            pass
                            t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(bill_line.betrag)


                            pass

                        elif not t_list:
                            t_list = T_list()
                            t_list_data.append(t_list)

                            curr_no = curr_no + 1
                            t_list.nr = curr_no
                            t_list.bezeich = bill_line.bezeich
                            t_list.preis =  to_decimal(artikel.epreis)
                            t_list.date1 = res_line.ankunft
                            t_list.betrag =  to_decimal(bill_line.betrag)
                            t_list.ankunft = res_line.ankunft
                            t_list.abreise = res_line.abreise


                    else:

                        t_list = query(t_list_data, filters=(lambda t_list: t_list.bezeich == artikel.bezeich), first=True)

                        if t_list:
                            pass
                            t_list.betrag =  to_decimal(t_list.betrag) + to_decimal(artikel.epreis)


                            pass

                        elif not t_list:
                            t_list = T_list()
                            t_list_data.append(t_list)

                            curr_no = curr_no + 1
                            t_list.nr = curr_no
                            t_list.bezeich = artikel.bezeich
                            t_list.preis =  to_decimal(artikel.epreis)
                            t_list.date1 = res_line.ankunft
                            t_list.betrag =  to_decimal(artikel.epreis)
                            t_list.ankunft = res_line.ankunft
                            t_list.abreise = res_line.abreise

            for t_list in query(t_list_data, filters=(lambda t_list: matches(t_list.bezeich,r"Heritage Fee*"))):
                t_list.qty = res_line.zimmeranz
                t_list.tage = count_night
                t_list.betrag =  to_decimal(t_list.betrag) * to_decimal(t_list.qty)


    def create_bonus():

        nonlocal err_flag, avail_master, avail_bill, reslinnr, master_rechnr, bill_rechnr, mainres_gastnr, t_reservation_data, t_res_line_data, t_guest_data, t_list_data, new_contrate, resline_exrate, billdate, bonus_array, tot_amt, serv1, vat1, vat3, fact1, netto, bill_receiver, currency, local_currency, frate, waehrungsnr, price_decimal, tot_deposit, t_char, t_resnr, reservation, res_line, guest, bill, htparam, master, exrate, waehrung, bill_line, artikel, zimkateg, arrangement, reslin_queasy, guest_pr, queasy, fixleist, billjournal
        nonlocal resnr, curr_resnr, arl_list_reslinnr, t_active_flag, printtype, split_bill
        nonlocal rline, mbill, mainres, b_bill


        nonlocal s_list, t_list, t_reservation, t_res_line, t_guest, rline, mbill, mainres, b_bill
        nonlocal s_list_data, t_list_data, t_reservation_data, t_res_line_data, t_guest_data

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

    t_reservation_data.clear()
    t_res_line_data.clear()
    t_guest_data.clear()
    s_list_data.clear()
    t_list_data.clear()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 550)]})

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    billdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})
    local_currency = htparam.fchar

    mainres = get_cache (Reservation, {"resnr": [(eq, resnr)]})
    mainres_gastnr = mainres.gastnr

    rline = get_cache (Res_line, {"resnr": [(eq, resnr)],"active_flag": [(le, 1)]})

    if curr_resnr == resnr:
        reslinnr = arl_list_reslinnr
    else:
        reslinnr = rline.reslinnr

    master = get_cache (Master, {"resnr": [(eq, resnr)]})

    if master:
        master_rechnr = master.rechnr
        avail_master = True

    bill = get_cache (Bill, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

    if bill:
        bill_rechnr = bill.rechnr
        avail_bill = True

    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)]})

    if res_line:

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})

        if guest:
            bill_receiver = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
        else:
            bill_receiver = ""

    reservation = get_cache (Reservation, {"resnr": [(eq, resnr)]})

    if reservation:
        t_reservation = T_reservation()
        t_reservation_data.append(t_reservation)

        buffer_copy(reservation, t_reservation)
        t_reservation.bill_receiver = bill_receiver

    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

    if res_line:
        t_res_line = T_res_line()
        t_res_line_data.append(t_res_line)

        buffer_copy(res_line, t_res_line)

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

        if guest:
            t_guest = T_guest()
            t_guest_data.append(t_guest)

            buffer_copy(guest, t_guest)

    if printtype == 2 or printtype == 3:

        if avail_master:
            read_proforma_inv(resnr, master.rechnr)
        else:

            if avail_bill:
                read_proforma_inv1(resnr, reslinnr, bill.rechnr)
            else:
                read_proforma_inv1(resnr, reslinnr, 0)

        if currency.lower()  != (local_currency).lower() :

            for t_list in query(t_list_data, filters=(lambda t_list: trim(t_list.wabkurz.lower() ) == "" or t_list.wabkurz.lower()  == (local_currency).lower())):
                t_list.wabkurz = currency

                if t_list.date1 < billdate:

                    exrate = get_cache (Exrate, {"artnr": [(eq, waehrungsnr)],"datum": [(eq, t_list.date1)]})

                    if exrate:
                        t_list.betrag =  to_decimal(t_list.betrag) / to_decimal(exrate.betrag)
                else:
                    t_list.betrag =  to_decimal(t_list.betrag) / to_decimal(frate)

                if price_decimal != 0:
                    t_list.betrag = to_decimal(round(t_list.betrag , price_decimal))
        else:

            for t_list in query(t_list_data, filters=(lambda t_list: trim(t_list.wabkurz) == "")):
                t_list.wabkurz = local_currency

    return generate_output()