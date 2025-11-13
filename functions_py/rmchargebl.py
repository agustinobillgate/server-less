#using conversion tools version: 1.0.0.117

# =========================================================
# Rulita, 21-10-2025
# Issue :
# - Comment VIEW_AS EDITOR INNER_CHARS 17
#   INNER_LINES 1 False_WORD_WRAP
# - Missing table name arrangement

# Rulita, 24-10-2025
# Issue :
# - Fixing round var amount
# - Fixing run program argt_betragbl
# - New compile program argt_betragbl
# - New compile program create_newbillbl
# - New compile program ratecode_compli

# Rulita, 13-11-2025
# - Fixing to_decimal() takes 1 potision argu 2 were given
# =========================================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.argt_betragbl import argt_betragbl
from sqlalchemy import func
from functions.create_newbillbl import create_newbillbl
from functions.ratecode_compli import ratecode_compli
from models import Bill_line, Bill, Artikel, Htparam, Waehrung, Arrangement, Zimmer, Queasy, Counters, Guest, Umsatz, Billjournal, Argt_line, Res_line, Res_history, Exrate, Reservation, Segment, Reslin_queasy, Zwkum, Fixleist, Master, Interface, Mast_art, Zimkateg, Guest_pr

def rmchargebl():

    prepare_cache ([Bill, Artikel, Htparam, Waehrung, Arrangement, Queasy, Counters, Guest, Umsatz, Billjournal, Argt_line, Res_line, Res_history, Exrate, Reservation, Segment, Reslin_queasy, Fixleist, Master, Zimkateg, Guest_pr])

    user_init:string = ""
    new_contrate:bool = False
    billno:int = 0
    userinit:string = ""
    bill_date:date = None
    exchg_rate:Decimal = 1
    ex_rate:Decimal = to_decimal("0.0")
    frate:Decimal = to_decimal("0.0")
    price_decimal:int = 0
    bil_recid:int = 0
    billart:int = 0
    qty:int = 0
    double_currency:bool = False
    foreign_rate:bool = False
    master_str:string = ""
    master_exist:bool = False
    master_rechnr:string = ""
    curr_posting:string = ""
    divered_rental:int = 0
    
    # Rulita,
    # - Comment VIEW_AS EDITOR INNER_CHARS 17 INNER_LINES 1 False_WORD_WRAP
    description:string = "" 
    # VIEW_AS EDITOR INNER_CHARS 17 INNER_LINES 1 False_WORD_WRAP
    amount_foreign:Decimal = to_decimal("0.0")
    price:Decimal = to_decimal("0.0")
    amount:Decimal = to_decimal("0.0")
    curr_amount:Decimal = to_decimal("0.0")
    bill_line = bill = artikel = htparam = waehrung = arrangement = zimmer = queasy = counters = guest = umsatz = billjournal = argt_line = res_line = res_history = exrate = reservation = segment = reslin_queasy = zwkum = fixleist = master = interface = mast_art = zimkateg = guest_pr = None

    art_list = jou_list = bline_list = argt_list = mbill = bartikel = na_list = s_list = None

    art_list_data, Art_list = create_model("Art_list", {"artnr":int})
    jou_list_data, Jou_list = create_model("Jou_list", {"artnr":int, "rechnr":int, "amount":Decimal})
    bline_list_data, Bline_list = create_model_like(Bill_line)
    argt_list_data, Argt_list = create_model("Argt_list", {"argtnr":int, "argt_artnr":int, "departement":int, "is_charged":int, "period":int, "vt_percnt":int})
    na_list_data, Na_list = create_model("Na_list", {"zinr":string, "name":string, "zipreis":Decimal})
    s_list_data, S_list = create_model("S_list", {"s_gastnr":int, "s_rechnr":int})

    Mbill = create_buffer("Mbill",Bill)
    Bartikel = create_buffer("Bartikel",Artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal user_init, new_contrate, billno, userinit, bill_date, exchg_rate, ex_rate, frate, price_decimal, bil_recid, billart, qty, double_currency, foreign_rate, master_str, master_exist, master_rechnr, curr_posting, divered_rental, description, amount_foreign, price, amount, curr_amount, bill_line, bill, artikel, htparam, waehrung, arrangement, zimmer, queasy, counters, guest, umsatz, billjournal, argt_line, res_line, res_history, exrate, reservation, segment, reslin_queasy, zwkum, fixleist, master, interface, mast_art, zimkateg, guest_pr
        nonlocal mbill, bartikel


        nonlocal art_list, jou_list, bline_list, argt_list, mbill, bartikel, na_list, s_list
        nonlocal art_list_data, jou_list_data, bline_list_data, argt_list_data, na_list_data, s_list_data

        return {}

    def create_list():

        nonlocal user_init, new_contrate, billno, userinit, bill_date, exchg_rate, ex_rate, frate, price_decimal, bil_recid, billart, qty, double_currency, foreign_rate, master_str, master_exist, master_rechnr, curr_posting, divered_rental, description, amount_foreign, price, amount, curr_amount, bill_line, bill, artikel, htparam, waehrung, arrangement, zimmer, queasy, counters, guest, umsatz, billjournal, argt_line, res_line, res_history, exrate, reservation, segment, reslin_queasy, zwkum, fixleist, master, interface, mast_art, zimkateg, guest_pr
        nonlocal mbill, bartikel


        nonlocal art_list, jou_list, bline_list, argt_list, mbill, bartikel, na_list, s_list
        nonlocal art_list_data, jou_list_data, bline_list_data, argt_list_data, na_list_data, s_list_data

        do_it:bool = False
        rechnr:int = 0

        for arrangement in db_session.query(Arrangement).filter(
                 (Arrangement.argt_artikelnr > 0)).order_by(Arrangement._recid).all():

            art_list = query(art_list_data, filters=(lambda art_list: art_list.artnr == arrangement.argt_artikelnr), first=True)

            if not art_list:
                art_list = Art_list()
                art_list_data.append(art_list)

                art_list.artnr = arrangement.argt_artikelnr

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.bill_datum == bill_date) & (Bill_line.departement == 0)).order_by(Bill_line._recid).all():

            art_list = query(art_list_data, filters=(lambda art_list: art_list.artnr == bill_line.artnr), first=True)

            if art_list:
                bline_list = Bline_list()
                bline_list_data.append(bline_list)

                buffer_copy(bill_line, bline_list)


    def rm_revenue():

        nonlocal user_init, new_contrate, billno, userinit, bill_date, exchg_rate, ex_rate, frate, price_decimal, bil_recid, billart, qty, double_currency, foreign_rate, master_str, master_exist, master_rechnr, curr_posting, divered_rental, description, amount_foreign, price, amount, curr_amount, bill_line, bill, artikel, htparam, waehrung, arrangement, zimmer, queasy, counters, guest, umsatz, billjournal, argt_line, res_line, res_history, exrate, reservation, segment, reslin_queasy, zwkum, fixleist, master, interface, mast_art, zimkateg, guest_pr
        nonlocal mbill, bartikel


        nonlocal art_list, jou_list, bline_list, argt_list, mbill, bartikel, na_list, s_list
        nonlocal art_list_data, jou_list_data, bline_list_data, argt_list_data, na_list_data, s_list_data

        roomrate:Decimal = to_decimal("0.0")
        i:int = 0
        n:int = 0

        queasy_obj_list = {}
        for queasy, zimmer in db_session.query(Queasy, Zimmer).join(Zimmer,(Zimmer.zinr == Queasy.char1)).filter(
                 (Queasy.key == 14) & (Queasy.deci1 != 0) & (Queasy.date1 <= bill_date) & (Queasy.date2 >= bill_date)).order_by(Queasy.number3).all():
            if queasy_obj_list.get(queasy._recid):
                continue
            else:
                queasy_obj_list[queasy._recid] = True

            s_list = query(s_list_data, filters=(lambda s_list: s_list.s_gastnr == queasy.number3), first=True)

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)

                s_list.s_gastnr = queasy.number3

                bill = get_cache (Bill, {"flag": [(eq, 0)],"billref": [(eq, queasy.number3)],"betriebsnr": [(eq, 0)]})

                if bill:
                    s_list.s_rechnr = bill.rechnr
                else:

                    counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
                    counters.counter = counters.counter + 1
                    s_list.s_rechnr = counters.counter
                    pass

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, queasy.number2)]})
            frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

            arrangement = get_cache (Arrangement, {"arrangement": [(eq, queasy.char2)]})

            guest = get_cache (Guest, {"gastnr": [(eq, queasy.number3)]})

            artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)],"departement": [(eq, 0)]})
            roomrate =  to_decimal(queasy.deci1)
            billart = artikel.artnr
            qty = 1
            description = arrangement.argt_rgbez
            price =  to_decimal(roomrate)

            if foreign_rate or double_currency:
                amount_foreign =  to_decimal(roomrate)
            else:
                amount_foreign =  to_decimal("0")
            amount = round(to_decimal(round(roomrate) * frate), price_decimal)


            if foreign_rate and price_decimal == 0:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 145)]})

                if htparam.finteger != 0:
                    n = 1
                    for i in range(1,htparam.finteger + 1) :
                        n = n * 10
                    amount = to_decimal(round(amount / n , 0) * n)

            bill = get_cache (Bill, {"rechnr": [(eq, s_list.s_rechnr)]})

            if not bill:
                bill = Bill()
                db_session.add(bill)

                bill.rechnr = s_list.s_rechnr
                bill.gastnr = queasy.number3
                bill.billref = queasy.number3
                bill.datum = bill_date
                bill.billtyp = 0
                bill.name = guest.name + ", " + guest.vorname1 + guest.anredefirma
                bill.reslinnr = 1

            bill_line = get_cache (Bill_line, {"rechnr": [(eq, bill.rechnr)],"bill_datum": [(eq, bill_date)],"zinr": [(eq, queasy.char1)],"artnr": [(eq, billart)],"departement": [(eq, artikel.departement)],"betrag": [(eq, amount)]})

            if not bill_line:
                bill.argtumsatz =  to_decimal(bill.argtumsatz) + to_decimal(amount)
                bill.gesamtumsatz =  to_decimal(bill.gesamtumsatz) + to_decimal(amount)
                bill.rgdruck = 0
                bill.datum = bill_date
                bill.saldo =  to_decimal(bill.saldo) + to_decimal(amount)
                bill.mwst[98] = bill.mwst[98] + amount_foreign
                bill_line = Bill_line()
                db_session.add(bill_line)

                bill_line.rechnr = bill.rechnr
                bill_line.artnr = billart
                bill_line.bezeich = description
                bill_line.anzahl = qty
                bill_line.betrag =  to_decimal(amount)
                bill_line.fremdwbetrag =  to_decimal(amount_foreign)
                bill_line.zinr = queasy.char1
                bill_line.departement = artikel.departement
                bill_line.epreis =  to_decimal(price)
                bill_line.zeit = get_current_time_in_seconds()
                bill_line.userinit = userinit
                bill_line.arrangement = queasy.char2
                bill_line.bill_datum = bill_date


                pass

                umsatz = get_cache (Umsatz, {"artnr": [(eq, billart)],"departement": [(eq, artikel.departement)],"datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = billart
                    umsatz.datum = bill_date
                    umsatz.departement = artikel.departement
                umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(amount)
                umsatz.anzahl = umsatz.anzahl + qty
                pass
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = billart
                billjournal.anzahl = qty
                billjournal.betrag =  to_decimal(amount)
                billjournal.fremdwaehrng =  to_decimal(amount_foreign)
                billjournal.bezeich = description
                billjournal.zinr = queasy.char1
                billjournal.departement = artikel.departement
                billjournal.epreis =  to_decimal(price)
                billjournal.zeit = get_current_time_in_seconds()
                billjournal.userinit = userinit
                billjournal.bill_datum = bill_date


                pass

                if amount != 0:
                    tax_service1()
            pass


    def tax_service1():

        nonlocal user_init, new_contrate, billno, userinit, bill_date, exchg_rate, frate, price_decimal, bil_recid, billart, qty, double_currency, foreign_rate, master_str, master_exist, master_rechnr, curr_posting, divered_rental, description, amount_foreign, price, amount, curr_amount, bill_line, bill, artikel, htparam, waehrung, arrangement, zimmer, queasy, counters, guest, umsatz, billjournal, argt_line, res_line, res_history, exrate, reservation, segment, reslin_queasy, zwkum, fixleist, master, interface, mast_art, zimkateg, guest_pr
        nonlocal mbill, bartikel


        nonlocal art_list, jou_list, bline_list, argt_list, mbill, bartikel, na_list, s_list
        nonlocal art_list_data, jou_list_data, bline_list_data, argt_list_data, na_list_data, s_list_data

        service:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        service_foreign:Decimal = to_decimal("0.0")
        vat_foreign:Decimal = to_decimal("0.0")
        artikel1 = None
        argt_betrag0:Decimal = to_decimal("0.0")
        argt_betrag:Decimal = to_decimal("0.0")
        rest_betrag:Decimal = to_decimal("0.0")
        rm_vat:bool = False
        rm_serv:bool = False
        post_it:bool = False
        qty1:int = 0
        ex_rate:Decimal = to_decimal("0.0")
        Artikel1 =  create_buffer("Artikel1",Artikel)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 127)]})
        rm_vat = not htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 128)]})
        rm_serv = not htparam.flogical
        rest_betrag =  to_decimal(amount)

        for argt_line in db_session.query(Argt_line).filter(
                 (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():
            qty1 = queasy.number1
            argt_betrag, ex_rate = get_output(argt_betragbl(res_line._recid, argt_line._recid))

            artikel1 = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})

            if artikel and argt_betrag != 0:
                rest_betrag =  to_decimal(rest_betrag) - to_decimal(argt_betrag)

                artikel1 = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})

                umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel1.artnr)],"departement": [(eq, artikel1.departement)],"datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = artikel1.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = artikel1.departement
                umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(argt_betrag)
                umsatz.anzahl = umsatz.anzahl + qty1
                pass
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = qty1
                billjournal.fremdwaehrng =  to_decimal(argt_line.betrag) * to_decimal(qty1)
                billjournal.betrag =  to_decimal(argt_betrag)
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = queasy.char1
                billjournal.departement = artikel1.departement
                billjournal.epreis =  to_decimal("0")
                billjournal.zeit = get_current_time_in_seconds()
                billjournal.userinit = userinit
                billjournal.bill_datum = bill_date


                pass

        artikel1 = get_cache (Artikel, {"artnr": [(eq, arrangement.artnr_logis)],"departement": [(eq, 0)]})

        umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel1.artnr)],"departement": [(eq, artikel1.departement)],"datum": [(eq, bill_date)]})

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artikel1.artnr
            umsatz.datum = bill_date
            umsatz.departement = artikel1.departement
        curr_amount =  to_decimal(curr_amount) + to_decimal(rest_betrag)


        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(rest_betrag)
        umsatz.anzahl = umsatz.anzahl + qty
        pass
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = bill.rechnr
        billjournal.artnr = artikel1.artnr
        billjournal.anzahl = qty
        billjournal.betrag =  to_decimal(rest_betrag)
        billjournal.bezeich = artikel1.bezeich
        billjournal.zinr = queasy.char1
        billjournal.departement = artikel1.departement
        billjournal.epreis =  to_decimal("0")
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.userinit = userinit
        billjournal.bill_datum = bill_date

        if double_currency or foreign_rate:
            billjournal.fremdwaehrng =  to_decimal(round (rest_betrag) / to_decimal(frate , 2))
        pass

        if rm_serv:

            htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.service_code)]})

            if htparam and htparam.fdecimal != 0:
                service =  to_decimal(htparam.fdecimal)

                htparam = get_cache (Htparam, {"paramnr": [(eq, 133)]})

                artikel1 = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})
                service =  to_decimal(service) * to_decimal(price) / to_decimal("100")
                service_foreign =  to_decimal(round (service , 2)) * to_decimal(qty)
                service =  to_decimal(round (service) * to_decimal(frate , price_decimal)) * to_decimal(qty)
                bill_line = Bill_line()
                db_session.add(bill_line)

                bill_line.rechnr = bill.rechnr
                bill_line.artnr = artikel1.artnr
                bill_line.bezeich = artikel1.bezeich
                bill_line.anzahl = qty
                bill_line.fremdwbetrag =  to_decimal(service_foreign)
                bill_line.betrag =  to_decimal(service)
                bill_line.zinr = queasy.char1
                bill_line.departement = artikel1.departement
                bill_line.epreis =  to_decimal("0")
                bill_line.zeit = get_current_time_in_seconds() + 1
                bill_line.userinit = userinit
                bill_line.arrangement = queasy.char2
                bill_line.bill_datum = bill_date


                pass

                umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel1.artnr)],"departement": [(eq, artikel1.departement)],"datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = artikel1.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = artikel1.departement
                umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(service)
                umsatz.anzahl = umsatz.anzahl + qty
                pass
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = qty
                billjournal.fremdwaehrng =  to_decimal(service_foreign)
                billjournal.betrag =  to_decimal(service)
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = queasy.char1
                billjournal.departement = artikel1.departement
                billjournal.epreis =  to_decimal("0")
                billjournal.zeit = get_current_time_in_seconds()
                billjournal.userinit = userinit
                billjournal.bill_datum = bill_date


                pass

        if rm_vat:

            htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.mwst_code)]})

            if htparam and htparam.fdecimal != 0:
                vat =  to_decimal(htparam.fdecimal)

                htparam = get_cache (Htparam, {"paramnr": [(eq, 132)]})

                artikel1 = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})

                htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})

                if htparam.flogical:
                    vat =  to_decimal(vat) * to_decimal((price) + to_decimal(service_foreign) / to_decimal(qty)) / to_decimal("100")
                else:
                    vat =  to_decimal(vat) * to_decimal(price) / to_decimal("100")
                vat_foreign =  to_decimal(round (vat , 2)) * to_decimal(qty)
                vat =  to_decimal(round (vat) * to_decimal(frate , price_decimal)) * to_decimal(qty)
                bill_line = Bill_line()
                db_session.add(bill_line)

                bill_line.rechnr = bill.rechnr
                bill_line.artnr = artikel1.artnr
                bill_line.bezeich = artikel1.bezeich
                bill_line.anzahl = qty
                bill_line.fremdwbetrag =  to_decimal(vat_foreign)
                bill_line.betrag =  to_decimal(vat)
                bill_line.zinr = queasy.char1
                bill_line.departement = artikel1.departement
                bill_line.epreis =  to_decimal("0")
                bill_line.zeit = get_current_time_in_seconds() + 2
                bill_line.userinit = userinit
                bill_line.arrangement = queasy.char2
                bill_line.bill_datum = bill_date


                pass

                umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel1.artnr)],"departement": [(eq, artikel1.departement)],"datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = artikel1.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = artikel1.departement
                umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(vat)
                umsatz.anzahl = umsatz.anzahl + qty
                pass
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = qty
                billjournal.fremdwaehrng =  to_decimal(vat_foreign)
                billjournal.betrag =  to_decimal(vat)
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = queasy.char1
                billjournal.departement = artikel1.departement
                billjournal.epreis =  to_decimal("0")
                billjournal.zeit = get_current_time_in_seconds()
                billjournal.userinit = userinit
                billjournal.bill_datum = bill_date


                pass
        bill.saldo =  to_decimal(bill.saldo) + to_decimal(vat) + to_decimal(service)
        bill.mwst[98] = bill.mwst[98] + vat_foreign + service_foreign


    def rm_charge():

        nonlocal user_init, new_contrate, billno, userinit, bill_date, exchg_rate, ex_rate, frate, price_decimal, billart, qty, double_currency, foreign_rate, master_str, master_exist, master_rechnr, curr_posting, divered_rental, description, amount_foreign, price, amount, curr_amount, bill_line, bill, artikel, htparam, waehrung, arrangement, zimmer, queasy, counters, guest, umsatz, billjournal, argt_line, res_line, res_history, exrate, reservation, segment, reslin_queasy, zwkum, fixleist, master, interface, mast_art, zimkateg, guest_pr
        nonlocal mbill, bartikel


        nonlocal art_list, jou_list, bline_list, argt_list, mbill, bartikel, na_list, s_list
        nonlocal art_list_data, jou_list_data, bline_list_data, argt_list_data, na_list_data, s_list_data

        posted:bool = False
        post_it:bool = False
        roomrate:Decimal = to_decimal("0.0")
        do_it:bool = False
        bil_recid:int = 0
        limited_flag:bool = False
        post_zerorate:bool = False
        currzeit:int = 0
        argt_betrag:Decimal = to_decimal("0.0")
        argt_buff = None
        buffargtline = None
        i:int = 0
        n:int = 0
        Argt_buff =  create_buffer("Argt_buff",Arrangement)
        Buffargtline =  create_buffer("Buffargtline",Argt_line)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 962)]})

        if htparam.feldtyp == 4 and substring(htparam.bezeichnung, 0, 6) == ("Post 0").lower() :
            post_zerorate = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 975)]})

        if htparam.flogical:
            limited_flag = True

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1052)]})

        if htparam:
            divered_rental = htparam.finteger


        currzeit = get_current_time_in_seconds() - 3

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag == 1) & (Res_line.zinr != "") & (Res_line.ankunft <= bill_date) & (Res_line.resstatus != 12) & (Res_line.resstatus != 8) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.zinr).all():

            bill = get_cache (Bill, {"zinr": [(eq, res_line.zinr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"flag": [(eq, 0)]})

            if not bill:

                bill = get_cache (Bill, {"zinr": [(eq, res_line.zinr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"flag": [(eq, 1)]})
            do_it = None != bill

            if bill:
                pass
                bill.flag = 0
                pass
            else:

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})
                bill = Bill()
                db_session.add(bill)

                bill.flag = 0
                bill.zinr = res_line.zinr
                bill.gastnr = res_line.gastnrpay
                bill.name = guest.name
                bill.resnr = res_line.resnr
                bill.reslinnr = res_line.reslinnr
                bill.parent_nr = res_line.reslinnr
                bill.billnr = 1
                bill.rgdruck = 1

                htparam = get_cache (Htparam, {"paramnr": [(eq, 799)]})

                if htparam.flogical and htparam.feldtyp == 4:

                    counters = get_cache (Counters, {"counter_no": [(eq, 29)]})

                    if not counters:
                        counters = Counters()
                        db_session.add(counters)

                        counters.counter_no = 29
                        counters.counter_bez = "Counter for Registration No"


                    counters.counter = counters.counter + 1
                    pass
                    bill.rechnr2 = counters.counter
                    pass
                pass
                do_it = True

            if res_line.zipreis == 0 and res_line.resstatus == 6:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = 0
                res_history.resnr = res_line.resnr
                res_history.reslinnr = res_line.reslinnr
                res_history.datum = bill_date
                res_history.zeit = 0
                res_history.aenderung = "Compliment"
                res_history.action = "n/A"


                pass
                pass
            frate =  to_decimal(res_line.reserve_dec)

            if res_line.reserve_dec != 0:

                if res_line.ankunft == bill_date:

                    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                    if waehrung:
                        frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                else:

                    exrate = get_cache (Exrate, {"datum": [(eq, res_line.ankunft)],"artnr": [(eq, res_line.betriebsnr)]})

                    if exrate:
                        frate =  to_decimal(exrate.betrag)

            elif res_line.betriebsnr != 0:

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})
                frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
            else:

                if res_line.adrflag:
                    frate =  to_decimal("1")
                else:
                    frate =  to_decimal(exchg_rate)

            if ((res_line.zipreis != 0) or (post_zerorate and res_line.resstatus == 6)) and do_it:

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                if limited_flag:

                    reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                    if segment and segment.vip_level > 0:

                        argt_buff = get_cache (Arrangement, {"segmentcode": [(eq, arrangement.argtnr)]})

                        if argt_buff:

                            arrangement = get_cache (Arrangement, {"_recid": [(eq, argt_buff._recid)]})

                artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)],"departement": [(eq, 0)]})
                posted = check_posted()

                if posted:

                    bline_list = query(bline_list_data, filters=(lambda bline_list: bline_list.artnr == artikel.artnr and bline_list.massnr == res_line.resnr and bline_list.billin_nr == res_line.reslinnr), first=True)

                    if bline_list:

                        if bline_list.betrag != res_line.zipreis:
                            res_history = Res_history()
                            db_session.add(res_history)

                            res_history.nr = 0
                            res_history.resnr = res_line.resnr
                            res_history.reslinnr = res_line.reslinnr
                            res_history.datum = bill_date
                            res_history.zeit = 0
                            res_history.aenderung = "Compliment"
                            res_history.action = "room Charge has been posted before night audit but not equal roomrate :" +\
                                    to_string(bline_list.betrag, "->>>,>>>,>>>,>>9.99") + " <> " +\
                                    to_string(res_line.zipreis, "->>>,>>>,>>>,>>9.99")


                            pass
                            pass

                if not posted:
                    posted = check_bonus()

                if not posted:
                    roomrate =  to_decimal(res_line.zipreis)
                    billart = artikel.artnr
                    qty = 1
                    description = arrangement.argt_rgbez
                    price =  to_decimal(roomrate)

                    if foreign_rate or double_currency:

                        if not res_line.adrflag:
                            amount_foreign =  to_decimal(roomrate)
                        else:
                            amount_foreign =  to_decimal(roomrate) / to_decimal(exchg_rate)
                    else:
                        amount_foreign =  to_decimal("0")
                    amount = round(to_decimal(round(roomrate) * frate), price_decimal)

                    if foreign_rate and price_decimal == 0:

                        htparam = get_cache (Htparam, {"paramnr": [(eq, 145)]})

                        if htparam.finteger != 0:
                            n = 1
                            for i in range(1,htparam.finteger + 1) :
                                n = n * 10
                            amount = to_decimal(round(amount / n , 0) * n)
                    na_list = Na_list()
                    na_list_data.append(na_list)

                    na_list.zinr = res_line.zinr
                    na_list.name = res_line.name
                    na_list.zipreis =  to_decimal(price)
                    curr_posting = "room charge"
                    currzeit = currzeit + 3


                    update_bill(currzeit)

                    queasy = get_cache (Queasy, {"key": [(eq, 301)],"number1": [(eq, res_line.resnr)],"logi1": [(eq, True)]})

                    if queasy:

                        # bartikel = get_cache (Artikel, {"artnr": [(eq, divered_rental)],"departement": [(eq, 0)]})
                        bartikel = db_session.query(Artikel).filter((Artikel.artnr == divered_rental) & (Artikel.departement == 0)).first()

                        curr_posting = "Diverred Rental"
                        currzeit = currzeit + 3
                        roomrate =  - to_decimal(res_line.zipreis)
                        billart = divered_rental
                        qty = 1
                        description = bartikel.bezeich
                        price =  to_decimal(roomrate)
                        amount =  - to_decimal(res_line.zipreis)
                        amount =  to_decimal(round (amount , price_decimal) )


                        update_bill2(currzeit)

            if do_it:

                for argt_line in db_session.query(Argt_line).filter(
                         (Argt_line.argtnr == arrangement.argtnr) & (Argt_line.kind2)).order_by(Argt_line._recid).all():

                    if argt_line.fakt_modus == 6:

                        argt_list = query(argt_list_data, filters=(lambda argt_list: argt_list.argtnr == argt_line.argtnr and argt_list.departement == argt_line.departement and argt_list.argt_artnr == argt_line.argt_artnr and argt_list.vt_percnt == argt_line.vt_percnt and argt_list.is_charged == 1), first=True)

                        if not argt_list:
                            argt_list = Argt_list()
                            argt_list_data.append(argt_list)

                            argt_list.argtnr = argt_line.argtnr
                            argt_list.departement = argt_line.departement
                            argt_list.argt_artnr = argt_line.argt_artnr
                            argt_list.vt_percnt = argt_line.vt_percnt
                            argt_list.is_charged = 1

                        if argt_list.period < argt_line.intervall:

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, res_line.abreise)],"date2": [(ge, res_line.ankunft)]})

                            if reslin_queasy:

                                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

                                if reslin_queasy:
                                    post_it = check_fixargt_posted(argt_line.argt_artnr, argt_line.departement, argt_line.fakt_modus, argt_line.intervall, reslin_queasy.date1)

                                    if post_it :
                                        argt_list.period = argt_list.period + 1
                                else:
                                    post_it = False
                            else:
                                posted = check_fixargt_posted(argt_line.argt_artnr, argt_line.departement, argt_line.fakt_modus, argt_line.intervall, res_line.ankunft)

                                if post_it :
                                    argt_list.period = argt_list.period + 1
                        else:
                            post_it = False
                    else:
                        posted = check_fixargt_posted(argt_line.argt_artnr, argt_line.departement, argt_line.fakt_modus, argt_line.intervall, res_line.ankunft)

                    if not posted:

                        artikel = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})
                        billart = argt_line.argt_artnr
                        description = artikel.bezeich

                        if argt_line.vt_percnt == 0:

                            if argt_line.betriebsnr == 0:
                                qty = res_line.erwachs
                            else:
                                qty = argt_line.betriebsnr

                        elif argt_line.vt_percnt == 1:
                            qty = res_line.kind1

                        elif argt_line.vt_percnt == 2:
                            qty = res_line.kind2
                        price =  to_decimal("0")

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

                        if reslin_queasy:

                            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                                     (Reslin_queasy.key == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.number1 == argt_line.departement) & (Reslin_queasy.number2 == argt_line.argtnr) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (bill_date >= Reslin_queasy.date1) & (bill_date <= Reslin_queasy.date2)).order_by(Reslin_queasy._recid).all():

                                if reslin_queasy.char2.lower()  != "" and reslin_queasy.char2.lower()  != ("0").lower() :

                                    zwkum = db_session.query(Zwkum).filter(
                                             (Zwkum.zknr == artikel.zwkum) & (Zwkum.departement == artikel.departement) & (matches(Zwkum.bezeich,"*DISCOUNT*"))).first()

                                    if zwkum:
                                        price =  to_decimal(roomrate) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal("100") * to_decimal(-1)
                                    else:
                                        price =  to_decimal(roomrate) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal("100")
                                else:

                                    if reslin_queasy.deci1 != 0:
                                        price =  to_decimal(reslin_queasy.deci1)

                                    elif reslin_queasy.deci2 != 0:
                                        price =  to_decimal(reslin_queasy.deci2)

                                    elif reslin_queasy.deci3 != 0:
                                        price =  to_decimal(reslin_queasy.deci3)
                                amount =  to_decimal(price) * to_decimal(qty)

                                if foreign_rate or double_currency:

                                    if not res_line.adrflag:
                                        amount_foreign =  to_decimal(amount)
                                    else:
                                        amount_foreign =  to_decimal(amount) / to_decimal(frate)
                                amount =  to_decimal(round (price) * to_decimal(frate , price_decimal)) * to_decimal(qty)
                                curr_posting = "fix cost article"
                                currzeit = currzeit + 1

                                if price != 0:
                                    update_bill(currzeit)

                        if argt_line.betrag > 0:
                            amount =  to_decimal(argt_line.betrag) * to_decimal(frate) * to_decimal(qty)
                        else:

                            zwkum = db_session.query(Zwkum).filter(
                                     (Zwkum.zknr == artikel.zwkum) & (Zwkum.departement == artikel.departement) & (matches(Zwkum.bezeich,"*DISCOUNT*"))).first()

                            if zwkum:
                                amount =  to_decimal(roomrate) * to_decimal((argt_line.betrag) / to_decimal(100)) * to_decimal(frate) * to_decimal(qty)
                            else:
                                amount =  to_decimal(roomrate) * to_decimal(- to_decimal(argt_line.betrag) / to_decimal(100)) * to_decimal(frate) * to_decimal(qty)

                        if foreign_rate or double_currency:

                            if not res_line.adrflag:
                                amount_foreign =  to_decimal(amount)
                            else:
                                amount_foreign =  to_decimal(amount) / to_decimal(frate)
                        amount = to_decimal(round(amount , price_decimal))
                        curr_posting = "fix cost article"
                        currzeit = currzeit + 1

                        if price == 0 and amount != 0:
                            update_bill(currzeit)

                for fixleist in db_session.query(Fixleist).filter(
                         (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():
                    posted = check_fixleist_posted(fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)

                    if not posted:

                        artikel = get_cache (Artikel, {"artnr": [(eq, fixleist.artnr)],"departement": [(eq, fixleist.departement)]})
                        billart = fixleist.artnr
                        description = fixleist.bezeich
                        qty = fixleist.number
                        price =  to_decimal(fixleist.betrag)
                        amount_foreign =  to_decimal("0")
                        amount =  to_decimal(price) * to_decimal(qty)

                        if foreign_rate or double_currency:

                            if not res_line.adrflag:
                                amount_foreign =  to_decimal(amount)
                            else:
                                amount_foreign =  to_decimal(amount) / to_decimal(frate)
                        amount =  to_decimal(round (price) * to_decimal(frate , price_decimal)) * to_decimal(qty)
                        curr_posting = "fix cost article"
                        currzeit = currzeit + 1

                        if amount != 0:
                            update_bill(currzeit)


    def update_bill(currzeit:int):

        nonlocal user_init, new_contrate, billno, userinit, bill_date, exchg_rate, ex_rate, frate, price_decimal, billart, qty, double_currency, foreign_rate, master_str, master_exist, master_rechnr, curr_posting, divered_rental, description, amount_foreign, price, amount, curr_amount, bill_line, bill, artikel, htparam, waehrung, arrangement, zimmer, queasy, counters, guest, umsatz, billjournal, argt_line, res_line, res_history, exrate, reservation, segment, reslin_queasy, zwkum, fixleist, master, interface, mast_art, zimkateg, guest_pr
        nonlocal mbill, bartikel


        nonlocal art_list, jou_list, bline_list, argt_list, mbill, bartikel, na_list, s_list
        nonlocal art_list_data, jou_list_data, bline_list_data, argt_list_data, na_list_data, s_list_data

        master_flag:bool = False
        bil_recid:int = 0
        bill1 = None
        Bill1 =  create_buffer("Bill1",Bill)
        master_flag = update_masterbill(currzeit)

        if not master_flag:

            bill = get_cache (Bill, {"zinr": [(eq, res_line.zinr)],"resnr": [(eq, res_line.resnr)],"billtyp": [(eq, 0)],"parent_nr": [(eq, res_line.reslinnr)],"billnr": [(eq, billno)],"flag": [(eq, 0)]})

            if not bill:

                bill1 = get_cache (Bill, {"zinr": [(eq, res_line.zinr)],"gastnr": [(eq, res_line.gastnrpay)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"billtyp": [(eq, 0)],"billnr": [(eq, 1)],"flag": [(eq, 0)]})
                bil_recid = get_output(create_newbillbl(res_line.resnr, res_line.reslinnr, bill1.parent_nr, billno))

                bill = get_cache (Bill, {"_recid": [(eq, bil_recid)]})
            bill.argtumsatz =  to_decimal(bill.argtumsatz) + to_decimal(amount)
            bill.gesamtumsatz =  to_decimal(bill.gesamtumsatz) + to_decimal(amount)
            bill.rgdruck = 0
            bill.datum = bill_date
            bill.saldo =  to_decimal(bill.saldo) + to_decimal(amount)
            bill.mwst[98] = bill.mwst[98] + amount_foreign

            if bill.rechnr == 0:

                counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
                counters.counter = counters.counter + 1
                bill.rechnr = counters.counter
                pass
            bill_line = Bill_line()
            db_session.add(bill_line)

            bill_line.rechnr = bill.rechnr
            bill_line.artnr = billart
            bill_line.bezeich = description
            bill_line.anzahl = qty
            bill_line.betrag =  to_decimal(amount)
            bill_line.fremdwbetrag =  to_decimal(amount_foreign)
            bill_line.zinr = res_line.zinr
            bill_line.departement = artikel.departement
            bill_line.epreis =  to_decimal(price)
            bill_line.massnr = res_line.resnr
            bill_line.billin_nr = res_line.reslinnr
            bill_line.zeit = currzeit
            bill_line.userinit = userinit
            bill_line.massnr = res_line.resnr
            bill_line.billin_nr = res_line.reslinnr
            bill_line.arrangement = res_line.arrangement
            bill_line.bill_datum = bill_date


            pass

            umsatz = get_cache (Umsatz, {"artnr": [(eq, billart)],"departement": [(eq, artikel.departement)],"datum": [(eq, bill_date)]})

            if not umsatz:
                umsatz = Umsatz()
                db_session.add(umsatz)

                umsatz.artnr = billart
                umsatz.datum = bill_date
                umsatz.departement = artikel.departement
            umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(amount)
            umsatz.anzahl = umsatz.anzahl + qty
            pass
            billjournal = Billjournal()
            db_session.add(billjournal)

            billjournal.rechnr = bill.rechnr
            billjournal.artnr = billart
            billjournal.anzahl = qty
            billjournal.betrag =  to_decimal(amount)
            billjournal.fremdwaehrng =  to_decimal(amount_foreign)
            billjournal.bezeich = description
            billjournal.zinr = res_line.zinr
            billjournal.departement = artikel.departement
            billjournal.epreis =  to_decimal(price)
            billjournal.zeit = currzeit
            billjournal.userinit = userinit
            billjournal.bill_datum = bill_date
            billjournal.comment = to_string(res_line.resnr) + ";" +\
                    to_string(res_line.reslinnr)

            if curr_posting.lower()  == ("room charge").lower() and amount != 0:
                tax_service(currzeit)

    def update_bill2(currzeit:int):

        nonlocal user_init, new_contrate, billno, userinit, bill_date, exchg_rate, ex_rate, frate, price_decimal, billart, qty, double_currency, foreign_rate, master_str, master_exist, master_rechnr, curr_posting, divered_rental, description, amount_foreign, price, amount, curr_amount, bill_line, bill, artikel, htparam, waehrung, arrangement, zimmer, queasy, counters, guest, umsatz, billjournal, argt_line, res_line, res_history, exrate, reservation, segment, reslin_queasy, zwkum, fixleist, master, interface, mast_art, zimkateg, guest_pr
        nonlocal mbill, bartikel


        nonlocal art_list, jou_list, bline_list, argt_list, mbill, bartikel, na_list, s_list
        nonlocal art_list_data, jou_list_data, bline_list_data, argt_list_data, na_list_data, s_list_data

        master_flag:bool = False
        bil_recid:int = 0
        bill1 = None
        Bill1 =  create_buffer("Bill1",Bill)
        master_flag = update_masterbill(currzeit)

        if not master_flag:

            bill = get_cache (Bill, {"zinr": [(eq, res_line.zinr)],"resnr": [(eq, res_line.resnr)],"billtyp": [(eq, 0)],"parent_nr": [(eq, res_line.reslinnr)],"billnr": [(eq, billno)],"flag": [(eq, 0)]})

            if not bill:

                bill1 = get_cache (Bill, {"zinr": [(eq, res_line.zinr)],"gastnr": [(eq, res_line.gastnrpay)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"billtyp": [(eq, 0)],"billnr": [(eq, 1)],"flag": [(eq, 0)]})
                bil_recid = get_output(create_newbillbl(res_line.resnr, res_line.reslinnr, bill1.parent_nr, billno))

                bill = get_cache (Bill, {"_recid": [(eq, bil_recid)]})
            bill.argtumsatz =  to_decimal(bill.argtumsatz) + to_decimal(amount)
            bill.gesamtumsatz =  to_decimal(bill.gesamtumsatz) + to_decimal(amount)
            bill.rgdruck = 0
            bill.datum = bill_date
            bill.saldo =  to_decimal(bill.saldo) + to_decimal(amount)
            bill.mwst[98] = bill.mwst[98] + amount_foreign

            if bill.rechnr == 0:

                counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
                counters.counter = counters.counter + 1
                bill.rechnr = counters.counter
                pass
            bill_line = Bill_line()
            db_session.add(bill_line)

            bill_line.rechnr = bill.rechnr
            bill_line.artnr = billart
            bill_line.bezeich = description
            bill_line.anzahl = qty
            bill_line.betrag =  to_decimal(amount)
            bill_line.fremdwbetrag =  to_decimal(amount_foreign)
            bill_line.zinr = res_line.zinr
            bill_line.departement = bartikel.departement
            bill_line.epreis =  to_decimal(price)
            bill_line.massnr = res_line.resnr
            bill_line.billin_nr = res_line.reslinnr
            bill_line.zeit = currzeit
            bill_line.userinit = userinit
            bill_line.massnr = res_line.resnr
            bill_line.billin_nr = res_line.reslinnr
            bill_line.arrangement = res_line.arrangement
            bill_line.bill_datum = bill_date


            pass

            umsatz = get_cache (Umsatz, {"artnr": [(eq, billart)],"departement": [(eq, bartikel.departement)],"datum": [(eq, bill_date)]})

            if not umsatz:
                umsatz = Umsatz()
                db_session.add(umsatz)

                umsatz.artnr = billart
                umsatz.datum = bill_date
                umsatz.departement = bartikel.departement
            umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(amount)
            umsatz.anzahl = umsatz.anzahl + qty
            pass
            billjournal = Billjournal()
            db_session.add(billjournal)

            billjournal.rechnr = bill.rechnr
            billjournal.artnr = billart
            billjournal.anzahl = qty
            billjournal.betrag =  to_decimal(amount)
            billjournal.fremdwaehrng =  to_decimal(amount_foreign)
            billjournal.bezeich = description
            billjournal.zinr = res_line.zinr
            billjournal.departement = bartikel.departement
            billjournal.epreis =  to_decimal(price)
            billjournal.zeit = currzeit
            billjournal.userinit = userinit
            billjournal.bill_datum = bill_date
            billjournal.comment = to_string(res_line.resnr) + ";" +\
                    to_string(res_line.reslinnr)


            pass

            if curr_posting.lower()  == ("room charge").lower()  and amount != 0:
                tax_service(currzeit)


    def update_masterbill(currzeit:int):

        nonlocal user_init, new_contrate, billno, userinit, bill_date, exchg_rate, ex_rate, frate, price_decimal, bil_recid, billart, qty, double_currency, foreign_rate, master_str, master_exist, master_rechnr, curr_posting, divered_rental, description, amount_foreign, price, amount, curr_amount, bill_line, bill, artikel, htparam, waehrung, arrangement, zimmer, queasy, counters, guest, umsatz, billjournal, argt_line, res_line, res_history, exrate, reservation, segment, reslin_queasy, zwkum, fixleist, master, interface, mast_art, zimkateg, guest_pr
        nonlocal mbill, bartikel


        nonlocal art_list, jou_list, bline_list, argt_list, mbill, bartikel, na_list, s_list
        nonlocal art_list_data, jou_list_data, bline_list_data, argt_list_data, na_list_data, s_list_data

        master_flag = False
        mbill = None
        b_receiver = None
        resline = None
        resline1 = None
        room:string = ""
        transfer_case:int = 0

        def generate_inner_output():
            return (master_flag)

        Mbill =  create_buffer("Mbill",Bill)
        B_receiver =  create_buffer("B_receiver",Guest)
        Resline =  create_buffer("Resline",Res_line)
        Resline1 =  create_buffer("Resline1",Res_line)

        if res_line.l_zuordnung[4] != 0:

            master = get_cache (Master, {"resnr": [(eq, res_line.l_zuordnung[4])],"active": [(eq, True)],"flag": [(eq, 0)]})
        else:

            master = get_cache (Master, {"resnr": [(eq, res_line.resnr)],"active": [(eq, True)],"flag": [(eq, 0)]})

        if master:

            if master.rechnr != 0:

                mbill = get_cache (Bill, {"resnr": [(eq, master.resnr)],"reslinnr": [(eq, 0)],"flag": [(eq, 0)]})

                if not mbill:

                    mbill = get_cache (Bill, {"resnr": [(eq, master.resnr)],"reslinnr": [(eq, 0)],"flag": [(eq, 1)]})

                    if not mbill:

                        b_receiver = get_cache (Guest, {"gastnr": [(eq, master.gastnr)]})

                        counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
                        counters.counter = counters.counter + 1
                        pass
                        pass
                        mbill = Bill()
                        db_session.add(mbill)

                        mbill.resnr = master.resnr
                        mbill.reslinnr = 0
                        mbill.rgdruck = 1
                        mbill.billtyp = 2
                        mbill.rechnr = counters.counter
                        mbill.gastnr = master.gastnr
                        mbill.name = b_receiver.name
                        master.rechnr = mbill.rechnr


                        pass
                        pass
                    else:

                        if mbill.saldo != 0:

                            interface = get_cache (Interface, {"key": [(eq, 38)],"action": [(eq, True)],"parameters": [(eq, "close-bill")],"intfield": [(eq, mbill.rechnr)],"decfield": [(eq, mbill.billtyp)],"resnr": [(eq, mbill.resnr)],"reslinnr": [(eq, mbill.reslinnr)]})

                            if not interface:
                                pass
                                mbill.flag = 0
                                pass
                            else:

                                b_receiver = get_cache (Guest, {"gastnr": [(eq, master.gastnr)]})

                                counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
                                counters.counter = counters.counter + 1
                                pass
                                pass
                                mbill = Bill()
                                db_session.add(mbill)

                                mbill.resnr = master.resnr
                                mbill.reslinnr = 0
                                mbill.rgdruck = 1
                                mbill.billtyp = 2
                                mbill.rechnr = counters.counter
                                mbill.gastnr = master.gastnr
                                mbill.name = b_receiver.name
                                master.rechnr = mbill.rechnr


                                pass
                                pass
                        else:

                            bill_line = get_cache (Bill_line, {"rechnr": [(eq, mbill.rechnr)]})

                            if bill_line:
                                pass
                                mbill.flag = 0
                                pass
                                pass
                            else:

                                b_receiver = get_cache (Guest, {"gastnr": [(eq, master.gastnr)]})

                                counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
                                counters.counter = counters.counter + 1
                                pass
                                pass
                                mbill = Bill()
                                db_session.add(mbill)

                                mbill.resnr = master.resnr
                                mbill.reslinnr = 0
                                mbill.rgdruck = 1
                                mbill.billtyp = 2
                                mbill.rechnr = counters.counter
                                mbill.gastnr = master.gastnr
                                mbill.name = b_receiver.name
                                master.rechnr = mbill.rechnr


                                pass
                                pass

            elif master.rechnr == 0:
                mbill = Bill()
                db_session.add(mbill)

                mbill.resnr = master.resnr
                mbill.reslinnr = 0
                mbill.rgdruck = 1
                mbill.billtyp = 2

                counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
                counters.counter = counters.counter + 1
                mbill.rechnr = counters.counter
                pass
                pass
                master.rechnr = mbill.rechnr
                pass
                mbill.gastnr = master.gastnr

                b_receiver = get_cache (Guest, {"gastnr": [(eq, master.gastnr)]})
                mbill.name = b_receiver.name
                pass
            transfer_case = 1

            if curr_posting.lower()  == ("room charge").lower() :

                if master.umsatzart[1] :
                    master_flag = True

            elif curr_posting.lower()  == ("fix cost article").lower() :

                if (master.umsatzart[0]  and artikel.artart == 8) or (master.umsatzart[1]  and artikel.artart == 9) or (master.umsatzart[2]  and (artikel.umsatzart == 3 or artikel.umsatzart == 5 or artikel.umsatzart == 6)) or (master.umsatzart[3]  and artikel.umsatzart == 4):
                    master_flag = True

                if not master_flag:

                    mast_art = get_cache (Mast_art, {"resnr": [(eq, master.resnr)],"departement": [(eq, artikel.departement)],"artnr": [(eq, artikel.artnr)]})

                    if mast_art:
                        master_flag = True

        if res_line.l_zuordnung[1] != 0:
            master_flag = False

        if not master_flag:

            if res_line.memozinr != "" and res_line.memozinr != res_line.zinr:

                resline1 = get_cache (Res_line, {"zinr": [(eq, res_line.memozinr)],"resstatus": [(eq, 6)]})

                if resline1:
                    master_flag = True
                    transfer_case = 2

        if master_flag:

            if transfer_case == 1:

                mbill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, 0)],"flag": [(eq, 0)]})
            else:

                mbill = get_cache (Bill, {"resnr": [(eq, resline1.resnr)],"reslinnr": [(eq, resline1.reslinnr)],"flag": [(eq, 0)],"billnr": [(eq, 1)]})

            if curr_posting.lower()  == ("room charge").lower() :
                mbill.argtumsatz =  to_decimal(mbill.argtumsatz) + to_decimal(amount)
            else:

                if artikel.umsatzart == 1:
                    mbill.logisumsatz =  to_decimal(mbill.logisumsatz) + to_decimal(amount)

                elif artikel.umsatzart == 2:
                    mbill.argtumsatz =  to_decimal(mbill.argtumsatz) + to_decimal(amount)

                elif artikel.umsatzart == 3 or artikel.umsatzart == 5 or artikel.umsatzart == 6:
                    mbill.f_b_umsatz =  to_decimal(mbill.f_b_umsatz) + to_decimal(amount)

                elif artikel.umsatzart == 4:
                    mbill.sonst_umsatz =  to_decimal(mbill.sonst_umsatz) + to_decimal(amount)
            mbill.gesamtumsatz =  to_decimal(mbill.gesamtumsatz) + to_decimal(amount)
            mbill.rgdruck = 0
            mbill.datum = bill_date
            mbill.saldo =  to_decimal(mbill.saldo) + to_decimal(amount)
            mbill.mwst[98] = mbill.mwst[98] + amount_foreign

            if mbill.rechnr == 0:

                counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
                counters.counter = counters.counter + 1
                mbill.rechnr = counters.counter
                pass
                pass
                master.rechnr = mbill.rechnr
                pass
            bill_line = Bill_line()
            db_session.add(bill_line)

            bill_line.rechnr = mbill.rechnr
            bill_line.artnr = billart
            bill_line.bezeich = description
            bill_line.anzahl = qty
            bill_line.betrag =  to_decimal(amount)
            bill_line.fremdwbetrag =  to_decimal(amount_foreign)
            bill_line.zinr = res_line.zinr
            bill_line.departement = artikel.departement
            bill_line.epreis =  to_decimal(price)
            bill_line.zeit = currzeit
            bill_line.userinit = userinit
            bill_line.bill_datum = bill_date

            if curr_posting.lower()  == ("room charge").lower() :
                bill_line.massnr = res_line.resnr
                bill_line.billin_nr = res_line.reslinnr
                bill_line.arrangement = res_line.arrangement


            pass

            umsatz = get_cache (Umsatz, {"artnr": [(eq, billart)],"departement": [(eq, artikel.departement)],"datum": [(eq, bill_date)]})

            if not umsatz:
                umsatz = Umsatz()
                db_session.add(umsatz)

                umsatz.artnr = billart
                umsatz.datum = bill_date
                umsatz.departement = artikel.departement
            umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(amount)
            umsatz.anzahl = umsatz.anzahl + qty
            pass
            billjournal = Billjournal()
            db_session.add(billjournal)

            billjournal.rechnr = mbill.rechnr
            billjournal.artnr = billart
            billjournal.anzahl = qty
            billjournal.betrag =  to_decimal(amount)
            billjournal.fremdwaehrng =  to_decimal(amount_foreign)
            billjournal.bezeich = description
            billjournal.zinr = res_line.zinr
            billjournal.departement = artikel.departement
            billjournal.epreis =  to_decimal(price)
            billjournal.zeit = currzeit
            billjournal.userinit = userinit
            billjournal.bill_datum = bill_date

            if curr_posting.lower()  == ("room charge").lower() :
                billjournal.comment = to_string(res_line.resnr) + ";" + to_string(res_line.reslinnr)
            pass

            if curr_posting.lower()  == ("room charge").lower() :

                if amount != 0:
                    master_taxserv(currzeit, mbill._recid)
            pass

        return generate_inner_output()


    def tax_service(currzeit:int):

        nonlocal user_init, new_contrate, billno, userinit, bill_date, exchg_rate, ex_rate, frate, price_decimal, bil_recid, billart, qty, double_currency, foreign_rate, master_str, master_exist, master_rechnr, curr_posting, divered_rental, description, amount_foreign, price, amount, curr_amount, bill_line, bill, artikel, htparam, waehrung, arrangement, zimmer, queasy, counters, guest, umsatz, billjournal, argt_line, res_line, res_history, exrate, reservation, segment, reslin_queasy, zwkum, fixleist, master, interface, mast_art, zimkateg, guest_pr
        nonlocal mbill, bartikel


        nonlocal art_list, jou_list, bline_list, argt_list, mbill, bartikel, na_list, s_list
        nonlocal art_list_data, jou_list_data, bline_list_data, argt_list_data, na_list_data, s_list_data

        service:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        service_foreign:Decimal = to_decimal("0.0")
        vat_foreign:Decimal = to_decimal("0.0")
        artikel1 = None
        argt_betrag0:Decimal = to_decimal("0.0")
        argt_betrag:Decimal = to_decimal("0.0")
        rest_betrag:Decimal = to_decimal("0.0")
        rm_vat:bool = False
        rm_serv:bool = False
        post_it:bool = False
        qty1:int = 0
        Artikel1 =  create_buffer("Artikel1",Artikel)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 127)]})
        rm_vat = not htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 128)]})
        rm_serv = not htparam.flogical
        rest_betrag =  to_decimal(amount)

        for argt_line in db_session.query(Argt_line).filter(
                 (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():

            if argt_line.vt_percnt == 0:

                if argt_line.betriebsnr == 0:
                    qty1 = res_line.erwachs
                else:
                    qty1 = argt_line.betriebsnr

            elif argt_line.vt_percnt == 1:

                if argt_line.betriebsnr == 0:
                    qty1 = res_line.kind1
                else:
                    qty1 = argt_line.betriebsnr

            elif argt_line.vt_percnt == 2:

                if argt_line.betriebsnr == 0:
                    qty1 = res_line.kind2
                else:
                    qty1 = argt_line.betriebsnr
            post_it = False
            argt_betrag0, ex_rate = get_output(argt_betragbl(res_line._recid, argt_line._recid))
            argt_betrag = to_decimal(round(argt_betrag0 * ex_rate , price_decimal))

            artikel1 = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})

            if argt_betrag != 0:
                rest_betrag =  to_decimal(rest_betrag) - to_decimal(argt_betrag)

                artikel1 = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})

                umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel1.artnr)],"departement": [(eq, artikel1.departement)],"datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = artikel1.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = artikel1.departement
                umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(argt_betrag)
                umsatz.anzahl = umsatz.anzahl + qty1
                pass
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = qty1
                billjournal.fremdwaehrng =  to_decimal(argt_betrag)
                billjournal.betrag =  to_decimal(argt_betrag)
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = res_line.zinr
                billjournal.departement = artikel1.departement
                billjournal.epreis =  to_decimal("0")
                billjournal.zeit = currzeit
                billjournal.userinit = userinit
                billjournal.bill_datum = bill_date
                billjournal.comment = to_string(res_line.resnr) + ";" +\
                        to_string(res_line.reslinnr)

                pass

        artikel1 = get_cache (Artikel, {"artnr": [(eq, arrangement.artnr_logis)],"departement": [(eq, 0)]})

        umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel1.artnr)],"departement": [(eq, artikel1.departement)],"datum": [(eq, bill_date)]})

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artikel1.artnr
            umsatz.datum = bill_date
            umsatz.departement = artikel1.departement
        curr_amount =  to_decimal(curr_amount) + to_decimal(rest_betrag)


        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(rest_betrag)
        umsatz.anzahl = umsatz.anzahl + qty
        pass
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = bill.rechnr
        billjournal.artnr = artikel1.artnr
        billjournal.anzahl = qty
        billjournal.betrag =  to_decimal(rest_betrag)
        billjournal.bezeich = artikel1.bezeich
        billjournal.zinr = res_line.zinr
        billjournal.departement = artikel1.departement
        billjournal.epreis =  to_decimal("0")
        billjournal.zeit = currzeit
        billjournal.userinit = userinit
        billjournal.bill_datum = bill_date
        billjournal.comment = to_string(res_line.resnr) + ";" +\
                to_string(res_line.reslinnr)


        if double_currency or foreign_rate:
            billjournal.fremdwaehrng =  to_decimal(round (rest_betrag) / to_decimal(frate , 2))
        pass

        if rm_serv:

            htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.service_code)]})

            if htparam and htparam.fdecimal != 0:
                service =  to_decimal(htparam.fdecimal)

                htparam = get_cache (Htparam, {"paramnr": [(eq, 133)]})

                artikel1 = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})
                service =  to_decimal(service) * to_decimal(price) / to_decimal("100")
                service_foreign =  to_decimal(round (service , 2)) * to_decimal(qty)
                service =  to_decimal(round (service) * to_decimal(frate , price_decimal)) * to_decimal(qty)
                bill_line = Bill_line()
                db_session.add(bill_line)

                bill_line.rechnr = bill.rechnr
                bill_line.artnr = artikel1.artnr
                bill_line.bezeich = artikel1.bezeich
                bill_line.anzahl = qty
                bill_line.fremdwbetrag =  to_decimal(service_foreign)
                bill_line.betrag =  to_decimal(service)
                bill_line.zinr = res_line.zinr
                bill_line.departement = artikel1.departement
                bill_line.epreis =  to_decimal("0")
                bill_line.zeit = currzeit + 1
                bill_line.userinit = userinit
                bill_line.massnr = res_line.resnr
                bill_line.billin_nr = res_line.reslinnr
                bill_line.arrangement = res_line.arrangement
                bill_line.bill_datum = bill_date


                pass

                umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel1.artnr)],"departement": [(eq, artikel1.departement)],"datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = artikel1.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = artikel1.departement
                umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(service)
                umsatz.anzahl = umsatz.anzahl + qty
                pass
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = qty
                billjournal.fremdwaehrng =  to_decimal(service_foreign)
                billjournal.betrag =  to_decimal(service)
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = res_line.zinr
                billjournal.departement = artikel1.departement
                billjournal.epreis =  to_decimal("0")
                billjournal.zeit = currzeit + 1
                billjournal.userinit = userinit
                billjournal.bill_datum = bill_date
                billjournal.comment = to_string(res_line.resnr) + ";" +\
                        to_string(res_line.reslinnr)

                pass

        if rm_vat:

            htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.mwst_code)]})

            if htparam and htparam.fdecimal != 0:
                vat =  to_decimal(htparam.fdecimal)

                htparam = get_cache (Htparam, {"paramnr": [(eq, 132)]})

                artikel1 = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})

                htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})

                if htparam.flogical:
                    vat =  to_decimal(vat) * to_decimal((price) + to_decimal(service_foreign) / to_decimal(qty)) / to_decimal("100")
                else:
                    vat =  to_decimal(vat) * to_decimal(price) / to_decimal("100")
                vat_foreign =  to_decimal(round (vat , 2)) * to_decimal(qty)
                vat =  to_decimal(round (vat) * to_decimal(frate , price_decimal)) * to_decimal(qty)
                bill_line = Bill_line()
                db_session.add(bill_line)

                bill_line.rechnr = bill.rechnr
                bill_line.artnr = artikel1.artnr
                bill_line.bezeich = artikel1.bezeich
                bill_line.anzahl = qty
                bill_line.fremdwbetrag =  to_decimal(vat_foreign)
                bill_line.betrag =  to_decimal(vat)
                bill_line.zinr = res_line.zinr
                bill_line.departement = artikel1.departement
                bill_line.epreis =  to_decimal("0")
                bill_line.zeit = currzeit + 2
                bill_line.userinit = userinit
                bill_line.massnr = res_line.resnr
                bill_line.billin_nr = res_line.reslinnr
                bill_line.arrangement = res_line.arrangement
                bill_line.bill_datum = bill_date


                pass

                umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel1.artnr)],"departement": [(eq, artikel1.departement)],"datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = artikel1.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = artikel1.departement
                umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(vat)
                umsatz.anzahl = umsatz.anzahl + qty
                pass
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = qty
                billjournal.fremdwaehrng =  to_decimal(vat_foreign)
                billjournal.betrag =  to_decimal(vat)
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = res_line.zinr
                billjournal.departement = artikel1.departement
                billjournal.epreis =  to_decimal("0")
                billjournal.zeit = currzeit + 2
                billjournal.userinit = userinit
                billjournal.bill_datum = bill_date
                billjournal.comment = to_string(res_line.resnr) + ";" +\
                        to_string(res_line.reslinnr)

                pass
        bill.saldo =  to_decimal(bill.saldo) + to_decimal(vat) + to_decimal(service)
        bill.mwst[98] = bill.mwst[98] + vat_foreign + service_foreign


    def master_taxserv(currzeit:int, billrecid:int):

        nonlocal user_init, new_contrate, billno, userinit, bill_date, exchg_rate, ex_rate, frate, price_decimal, bil_recid, billart, qty, double_currency, foreign_rate, master_str, master_exist, master_rechnr, curr_posting, divered_rental, description, amount_foreign, price, amount, curr_amount, bill_line, bill, artikel, htparam, waehrung, arrangement, zimmer, queasy, counters, guest, umsatz, billjournal, argt_line, res_line, res_history, exrate, reservation, segment, reslin_queasy, zwkum, fixleist, master, interface, mast_art, zimkateg, guest_pr
        nonlocal mbill, bartikel


        nonlocal art_list, jou_list, bline_list, argt_list, mbill, bartikel, na_list, s_list
        nonlocal art_list_data, jou_list_data, bline_list_data, argt_list_data, na_list_data, s_list_data

        service:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        service_foreign:Decimal = to_decimal("0.0")
        vat_foreign:Decimal = to_decimal("0.0")
        artikel1 = None
        rest_betrag:Decimal = to_decimal("0.0")
        rm_vat:bool = False
        rm_serv:bool = False
        mbill = None
        post_it:bool = False
        argt_betrag:Decimal = to_decimal("0.0")
        argt_betrag0:Decimal = to_decimal("0.0")
        qty1:int = 0
        Artikel1 =  create_buffer("Artikel1",Artikel)
        Mbill =  create_buffer("Mbill",Bill)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 127)]})
        rm_vat = not htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 128)]})
        rm_serv = not htparam.flogical

        mbill = get_cache (Bill, {"_recid": [(eq, billrecid)]})
        rest_betrag =  to_decimal(amount)

        for argt_line in db_session.query(Argt_line).filter(
                 (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():

            if argt_line.vt_percnt == 0:

                if argt_line.betriebsnr == 0:
                    qty1 = res_line.erwachs
                else:
                    qty1 = argt_line.betriebsnr

            elif argt_line.vt_percnt == 1:

                if argt_line.betriebsnr == 0:
                    qty1 = res_line.kind1
                else:
                    qty1 = argt_line.betriebsnr

            elif argt_line.vt_percnt == 2:

                if argt_line.betriebsnr == 0:
                    qty1 = res_line.kind2
                else:
                    qty1 = argt_line.betriebsnr

            artikel1 = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})
            post_it = False
            argt_betrag0, ex_rate = get_output(argt_betragbl(res_line._recid, argt_line._recid))
            
            # Rulita 13-11-2025
            # argt_betrag =  to_decimal(round (argt_betrag0) * to_decimal(ex_rate , price_decimal))
            argt_betrag =  to_decimal(round (argt_betrag0 * ex_rate , price_decimal))

            if argt_betrag != 0:
                rest_betrag =  to_decimal(rest_betrag) - to_decimal(argt_betrag)

                artikel1 = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})

                umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel1.artnr)],"departement": [(eq, artikel1.departement)],"datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = artikel1.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = artikel1.departement
                umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(argt_betrag)
                umsatz.anzahl = umsatz.anzahl + qty1
                pass
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = mbill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = qty1
                billjournal.fremdwaehrng =  to_decimal(argt_betrag)
                billjournal.betrag =  to_decimal(argt_betrag)
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = res_line.zinr
                billjournal.departement = artikel1.departement
                billjournal.epreis =  to_decimal("0")
                billjournal.zeit = currzeit
                billjournal.userinit = userinit
                billjournal.bill_datum = bill_date
                billjournal.comment = to_string(res_line.resnr) + ";" +\
                        to_string(res_line.reslinnr)


                pass

        artikel1 = get_cache (Artikel, {"artnr": [(eq, arrangement.artnr_logis)],"departement": [(eq, 0)]})

        umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel1.artnr)],"departement": [(eq, artikel1.departement)],"datum": [(eq, bill_date)]})

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artikel1.artnr
            umsatz.datum = bill_date
            umsatz.departement = artikel1.departement
        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(rest_betrag)
        umsatz.anzahl = umsatz.anzahl + qty
        pass
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = mbill.rechnr
        billjournal.artnr = artikel1.artnr
        billjournal.anzahl = qty
        # Rulita, 13-11-2025
        # billjournal.fremdwaehrng =  to_decimal(round (rest_betrag) / to_decimal(frate , 2) )
        billjournal.fremdwaehrng =  to_decimal(round (rest_betrag / frate , 2) )
        billjournal.betrag =  to_decimal(rest_betrag)
        billjournal.bezeich = artikel1.bezeich
        billjournal.zinr = res_line.zinr
        billjournal.departement = artikel1.departement
        billjournal.epreis =  to_decimal("0")
        billjournal.zeit = currzeit
        billjournal.userinit = userinit
        billjournal.bill_datum = bill_date
        billjournal.comment = to_string(res_line.resnr) + ";" +\
                to_string(res_line.reslinnr)

        pass

        if rm_serv:

            htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.service_code)]})

            if htparam and htparam.fdecimal != 0:
                service =  to_decimal(htparam.fdecimal)

                htparam = get_cache (Htparam, {"paramnr": [(eq, 133)]})

                artikel1 = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})
                service =  to_decimal(service) * to_decimal(price) / to_decimal("100")
                service_foreign =  to_decimal(round (service , 2)) * to_decimal(qty)
                service =  to_decimal(round (service) * to_decimal(frate , price_decimal)) * to_decimal(qty)
                bill_line = Bill_line()
                db_session.add(bill_line)

                bill_line.rechnr = mbill.rechnr
                bill_line.artnr = artikel1.artnr
                bill_line.bezeich = artikel1.bezeich
                bill_line.anzahl = qty
                bill_line.fremdwbetrag =  to_decimal(service_foreign)
                bill_line.betrag =  to_decimal(service)
                bill_line.zinr = res_line.zinr
                bill_line.departement = artikel1.departement
                bill_line.epreis =  to_decimal("0")
                bill_line.zeit = currzeit + 1
                bill_line.userinit = userinit
                bill_line.massnr = res_line.resnr
                bill_line.billin_nr = res_line.reslinnr
                bill_line.arrangement = res_line.arrangement
                bill_line.bill_datum = bill_date


                pass

                umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel1.artnr)],"departement": [(eq, artikel1.departement)],"datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = artikel1.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = artikel1.departement
                umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(service)
                umsatz.anzahl = umsatz.anzahl + qty
                pass
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = mbill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = qty
                billjournal.fremdwaehrng =  to_decimal(service_foreign)
                billjournal.betrag =  to_decimal(service)
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = res_line.zinr
                billjournal.departement = artikel1.departement
                billjournal.epreis =  to_decimal("0")
                billjournal.zeit = currzeit + 1
                billjournal.userinit = userinit
                billjournal.bill_datum = bill_date
                billjournal.comment = to_string(res_line.resnr) + ";" +\
                        to_string(res_line.reslinnr)

                pass

        if rm_vat:

            htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.mwst_code)]})

            if htparam and htparam.fdecimal != 0:
                vat =  to_decimal(htparam.fdecimal)

                if (service * qty) < 0:
                    service =  - to_decimal(service)

                htparam = get_cache (Htparam, {"paramnr": [(eq, 132)]})

                artikel1 = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})

                htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})

                if htparam.flogical:
                    vat =  to_decimal(vat) * to_decimal((price) + to_decimal(service_foreign) / to_decimal(qty)) / to_decimal("100")
                else:
                    vat =  to_decimal(vat) * to_decimal(price) / to_decimal("100")
                vat_foreign =  to_decimal(round (vat , 2)) * to_decimal(qty)
                vat =  to_decimal(round (vat) * to_decimal(frate , price_decimal)) * to_decimal(qty)
                bill_line = Bill_line()
                db_session.add(bill_line)

                bill_line.rechnr = mbill.rechnr
                bill_line.artnr = artikel1.artnr
                bill_line.bezeich = artikel1.bezeich
                bill_line.anzahl = qty
                bill_line.fremdwbetrag =  to_decimal(vat_foreign)
                bill_line.betrag =  to_decimal(vat)
                bill_line.zinr = res_line.zinr
                bill_line.departement = artikel1.departement
                bill_line.epreis =  to_decimal("0")
                bill_line.zeit = currzeit + 2
                bill_line.userinit = userinit
                bill_line.massnr = res_line.resnr
                bill_line.billin_nr = res_line.reslinnr
                bill_line.arrangement = res_line.arrangement
                bill_line.bill_datum = bill_date


                pass

                umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel1.artnr)],"departement": [(eq, artikel1.departement)],"datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = artikel1.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = artikel1.departement
                umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(vat)
                umsatz.anzahl = umsatz.anzahl + qty
                pass
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = mbill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = qty
                billjournal.fremdwaehrng =  to_decimal(vat_foreign)
                billjournal.betrag =  to_decimal(vat)
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = res_line.zinr
                billjournal.departement = artikel1.departement
                billjournal.epreis =  to_decimal("0")
                billjournal.zeit = currzeit + 2
                billjournal.userinit = userinit
                billjournal.bill_datum = bill_date
                billjournal.comment = to_string(res_line.resnr) + ";" +\
                        to_string(res_line.reslinnr)

                pass
        mbill.saldo =  to_decimal(mbill.saldo) + to_decimal(vat) + to_decimal(service)
        mbill.mwst[98] = mbill.mwst[98] + vat_foreign + service_foreign
        pass


    def check_fixleist_posted(artnr:int, dept:int, fakt_modus:int, intervall:int, lfakt:date):

        nonlocal user_init, new_contrate, billno, userinit, bill_date, exchg_rate, ex_rate, frate, price_decimal, bil_recid, billart, qty, double_currency, foreign_rate, master_str, master_exist, master_rechnr, curr_posting, description, amount_foreign, price, amount, curr_amount, bill_line, bill, htparam, waehrung, arrangement, zimmer, queasy, counters, guest, artikel, umsatz, billjournal, argt_line, res_line, res_history, exrate, reservation, segment, reslin_queasy, zwkum, fixleist, master, interface, mast_art, zimkateg, guest_pr
        nonlocal mbill


        nonlocal art_list, jou_list, argt_list, bline_list, mbill, na_list, s_list
        nonlocal art_list_data, jou_list_data, argt_list_data, bline_list_data, na_list_data, s_list_data

        posted = False
        master_flag:bool = False
        delta:int = 0
        start_date:date = None
        invoice = None

        def generate_inner_output():
            return (posted)

        Invoice =  create_buffer("Invoice",Bill)

        master = get_cache (Master, {"resnr": [(eq, res_line.resnr)],"active": [(eq, True)],"flag": [(eq, 0)]})

        if master and master.umsatzart[1] :
            master_flag = True

        if master_flag:

            invoice = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, 0)]})
        else:

            invoice = get_cache (Bill, {"zinr": [(eq, res_line.zinr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"billtyp": [(eq, 0)],"billnr": [(eq, 1)],"flag": [(eq, 0)]})

        if not posted:

            if fakt_modus == 2:

                if res_line.ankunft != bill_date:
                    posted = True

            elif fakt_modus == 3:

                if (res_line.ankunft + 1) != bill_date:
                    posted = True

            elif fakt_modus == 4:

                if get_day(bill_date) != 1:
                    posted = True

            elif fakt_modus == 5:

                if get_day(bill_date + 1) != 1:
                    posted = True

            elif fakt_modus == 6:

                if lfakt == None:
                    delta = 0
                else:
                    delta = (lfakt - res_line.ankunft).days

                    if delta < 0:
                        delta = 0
                start_date = res_line.ankunft + timedelta(days=delta)

                if (res_line.abreise - start_date) < intervall:
                    start_date = res_line.ankunft

                if bill_date > (start_date + timedelta(days=(intervall - 1))):
                    posted = True

                if bill_date < start_date:
                    posted = True

        return generate_inner_output()


    def check_fixargt_posted(artnr:int, dept:int, fakt_modus:int, intervall:int, start_date:date):

        nonlocal user_init, new_contrate, billno, userinit, bill_date, exchg_rate, ex_rate, frate, price_decimal, bil_recid, billart, qty, double_currency, foreign_rate, master_str, master_exist, master_rechnr, curr_posting, divered_rental, description, amount_foreign, price, amount, curr_amount, bill_line, bill, artikel, htparam, waehrung, arrangement, zimmer, queasy, counters, guest, umsatz, billjournal, argt_line, res_line, res_history, exrate, reservation, segment, reslin_queasy, zwkum, fixleist, master, interface, mast_art, zimkateg, guest_pr
        nonlocal mbill, bartikel


        nonlocal art_list, jou_list, bline_list, argt_list, mbill, bartikel, na_list, s_list
        nonlocal art_list_data, jou_list_data, bline_list_data, argt_list_data, na_list_data, s_list_data

        posted = False
        master_flag:bool = False
        invoice = None

        def generate_inner_output():
            return (posted)

        Invoice =  create_buffer("Invoice",Bill)

        master = get_cache (Master, {"resnr": [(eq, res_line.resnr)],"active": [(eq, True)],"flag": [(eq, 0)]})

        if master and master.umsatzart[1] :
            master_flag = True

        if master_flag:

            invoice = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, 0)]})
        else:

            invoice = get_cache (Bill, {"zinr": [(eq, res_line.zinr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"billtyp": [(eq, 0)],"billnr": [(eq, 1)],"flag": [(eq, 0)]})

        if not posted:

            if fakt_modus == 2:

                if res_line.ankunft != bill_date:
                    posted = True

            elif fakt_modus == 3:

                if (res_line.ankunft + 1) != bill_date:
                    posted = True

            elif fakt_modus == 4:

                if get_day(bill_date) != 1:
                    posted = True

            elif fakt_modus == 5:

                if get_day(bill_date + 1) != 1:
                    posted = True

            elif fakt_modus == 6:

                if bill_date >= start_date and bill_date <= (start_date + timedelta(days=(intervall - 1))):
                    posted = True

        return generate_inner_output()


    def check_posted():

        nonlocal user_init, new_contrate, billno, userinit, bill_date, exchg_rate, ex_rate, frate, price_decimal, bil_recid, billart, qty, double_currency, foreign_rate, master_str, master_exist, master_rechnr, curr_posting, divered_rental, description, amount_foreign, price, amount, curr_amount, bill_line, bill, artikel, htparam, waehrung, arrangement, zimmer, queasy, counters, guest, umsatz, billjournal, argt_line, res_line, res_history, exrate, reservation, segment, reslin_queasy, zwkum, fixleist, master, interface, mast_art, zimkateg, guest_pr
        nonlocal mbill, bartikel


        nonlocal art_list, jou_list, bline_list, argt_list, mbill, bartikel, na_list, s_list
        nonlocal art_list_data, jou_list_data, bline_list_data, argt_list_data, na_list_data, s_list_data

        posted = False
        master_flag:bool = False
        post_it:bool = False
        skip_it:bool = True
        invoice = None

        def generate_inner_output():
            return (posted)

        Invoice =  create_buffer("Invoice",Bill)

        bline_list = query(bline_list_data, filters=(lambda bline_list: bline_list.artnr == artikel.artnr and bline_list.massnr == res_line.resnr and bline_list.billin_nr == res_line.reslinnr), first=True)

        if bline_list:
            posted = True
            bline_list_data.remove(bline_list)

            return generate_inner_output()

        if skip_it:

            return generate_inner_output()

        bill_line = get_cache (Bill_line, {"departement": [(eq, 0)],"artnr": [(eq, artikel.artnr)],"bill_datum": [(eq, bill_date)],"zinr": [(ne, "")],"massnr": [(eq, res_line.resnr)],"billin_nr": [(eq, res_line.reslinnr)]})
        posted = None != bill_line

        if skip_it:

            return generate_inner_output()

        jou_list = query(jou_list_data, filters=(lambda jou_list: jou_list.rechnr == bill.rechnr and jou_list.amount > 0), first=True)

        if jou_list:
            posted = True

            return generate_inner_output()

        invoice = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, 0)]})

        if invoice:

            bill_line = get_cache (Bill_line, {"artnr": [(eq, artikel.artnr)],"departement": [(eq, artikel.departement)],"massnr": [(eq, res_line.resnr)],"billin_nr": [(eq, res_line.reslinnr)],"bill_datum": [(eq, bill_date)]})

            if bill_line:
                posted = True

        if posted:

            return generate_inner_output()

        invoice = get_cache (Bill, {"zinr": [(eq, res_line.zinr),(eq, res_line.zinr)],"flag": [(eq, 0)],"resnr": [(eq, res_line.resnr)],"parent_nr": [(eq, res_line.reslinnr)]})
        while None != invoice and not posted:

            bill_line = get_cache (Bill_line, {"artnr": [(eq, artikel.artnr)],"departement": [(eq, artikel.departement)],"zinr": [(eq, res_line.zinr)],"rechnr": [(eq, invoice.rechnr)],"bill_datum": [(eq, bill_date)]})

            if bill_line:
                posted = True
            else:

                curr_recid = invoice._recid
                invoice = db_session.query(Invoice).filter(
                         (Invoice.zinr == res_line.zinr) & (Invoice.flag == 0) & (Invoice.resnr == res_line.resnr) & (Invoice.parent_nr == res_line.reslinnr) & (Invoice.zinr == res_line.zinr) & (Invoice._recid > curr_recid)).first()

        if posted:

            return generate_inner_output()

        if not posted:
            post_it = False

            if arrangement.fakt_modus == 1:
                post_it = True

            elif arrangement.fakt_modus == 2 or arrangement.fakt_modus == 3:

                bill_line = get_cache (Bill_line, {"artnr": [(eq, artikel.artnr)],"departement": [(eq, artikel.departement)],"zinr": [(eq, res_line.zinr)],"rechnr": [(eq, invoice.rechnr)]})

                if not bill_line:
                    post_it = True

            elif arrangement.fakt_modus == 4:

                if get_day(bill_date) == 1:
                    post_it = True

            elif arrangement.fakt_modus == 5:

                if get_day(bill_date + 1) == 1:
                    post_it = True
            posted = not post_it

        return generate_inner_output()


    def check_bonus():

        nonlocal user_init, new_contrate, billno, userinit, bill_date, exchg_rate, ex_rate, frate, price_decimal, bil_recid, billart, qty, double_currency, foreign_rate, master_str, master_exist, master_rechnr, curr_posting, divered_rental, description, amount_foreign, price, amount, curr_amount, bill_line, bill, artikel, htparam, waehrung, arrangement, zimmer, queasy, counters, guest, umsatz, billjournal, argt_line, res_line, res_history, exrate, reservation, segment, reslin_queasy, zwkum, fixleist, master, interface, mast_art, zimkateg, guest_pr
        nonlocal mbill, bartikel


        nonlocal art_list, jou_list, bline_list, argt_list, mbill, bartikel, na_list, s_list
        nonlocal art_list_data, jou_list_data, bline_list_data, argt_list_data, na_list_data, s_list_data

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

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

        if reslin_queasy:

            return generate_inner_output()

        guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

        if res_line.l_zuordnung[0] != 0:

            rmcat = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.l_zuordnung[0])]})
            curr_zikatnr = rmcat.zikatnr
        else:
            curr_zikatnr = res_line.zikatnr

        if new_contrate and guest_pr:
            bonus = get_output(ratecode_compli(res_line.resnr, res_line.reslinnr, guest_pr.code, curr_zikatnr, bill_date))

            return generate_inner_output()

        if length(arrangement.OPTIONS) != 16:

            return generate_inner_output()
        j = 1
        for i in range(1,4 + 1) :
            stay = 0
            pay = 0

            # Rulita,
            # - Missing table name arrangement
            stay = to_int(substring(arrangement.options, j - 1, 2))
            pay = to_int(substring(arrangement.options, j + 2 - 1, 2))

            if (stay - pay) > 0:
                n = num_bonus + pay + 1
                for k in range(n,stay + 1) :
                    bonus_array[k - 1] = True
                num_bonus = stay - pay
            j = j + 4
        n = (bill_date - res_line.ankunft + 1).days
        bonus = False

        if n <= 999:
            bonus = bonus_array[n - 1]

        return generate_inner_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 550)]})

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 84)]})
    billno = htparam.finteger

    if billno == 0:
        billno = 1

    if billno > 2:
        billno = 2

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    foreign_rate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    double_currency = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 104)]})
    userinit = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    if foreign_rate or double_currency:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 104)]})
    user_init = htparam.fchar
    create_list()
    rm_charge()
    rm_revenue()

    return generate_output()