#using conversion tools version: 1.0.0.117
# ============================
# Rd, 24/11/2025, update last_count for counter update
# ============================
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.argt_betragbl import argt_betragbl
from functions.i_master_taxserv import i_master_taxserv
from models import Htparam, Res_line, Waehrung, Arrangement, Artikel, Bill, Counters, Bill_line, Umsatz, Billjournal, Argt_line, Guest, Master, Interface, Mast_art
from functions.next_counter_for_update import next_counter_for_update


def post_dayuse(resnr:int, reslinnr:int):

    prepare_cache ([Htparam, Res_line, Waehrung, Arrangement, Artikel, Bill, Counters, Bill_line, Umsatz, Billjournal, Argt_line, Guest, Master, Interface, Mast_art])

    user_init:string = ""
    master_flag:bool = False
    gastnrmember:int = 0
    amount:Decimal = to_decimal("0.0")
    amount_foreign:Decimal = to_decimal("0.0")
    description:string = ""
    bill_date:date = None
    price_decimal:int = 0
    exchg_rate:Decimal = 1
    ex_rate:Decimal = to_decimal("0.0")
    double_currency:bool = False
    foreign_rate:bool = False
    billart:int = 0
    qty:int = 1
    curr_room:string = ""
    cancel_str:string = ""
    master_str:string = ""
    master_rechnr:string = ""
    curr_department:int = 0
    price:Decimal = to_decimal("0.0")
    currzeit:int = 0
    i:int = 0
    n:int = 1
    curr_posting:string = ""

    htparam = res_line = waehrung = arrangement = artikel = bill = counters = bill_line = umsatz = billjournal = argt_line = None

    db_session = local_storage.db_session
    last_count = 0
    error_lock = ""

    def generate_output():
        nonlocal user_init, master_flag, gastnrmember, amount, amount_foreign, description, bill_date, price_decimal, exchg_rate, ex_rate, double_currency, foreign_rate, billart, qty, curr_room, cancel_str, master_str, master_rechnr, curr_department, price, currzeit, i, n, htparam, res_line, waehrung, arrangement, artikel, bill, counters, bill_line, umsatz, billjournal, argt_line
        nonlocal resnr, reslinnr

        return {}

    def update_masterbill(currzeit:int):
        
        nonlocal curr_posting, user_init, master_flag, gastnrmember, amount, amount_foreign, description, bill_date, price_decimal, exchg_rate, ex_rate, double_currency, foreign_rate, billart, qty, curr_room, cancel_str, master_str, master_rechnr, curr_department, price, i, n, htparam, res_line, waehrung, arrangement, artikel, bill, counters, bill_line, umsatz, billjournal, argt_line
        nonlocal resnr, reslinnr


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

                        counters = db_session.query(Counters).filter(
                                 (Counters.counter_no == 3)).with_for_update().first()

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

                                # counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
                                counters = db_session.query(Counters).filter(
                                         (Counters.counter_no == 3)).with_for_update().first()
                                counters.counter = counters.counter + 1
                                # pass
                                # pass
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

                                # counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
                                counters = db_session.query(Counters).filter(
                                         (Counters.counter_no == 3)).with_for_update().first()
                                counters.counter = counters.counter + 1
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

                # counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
                counters = db_session.query(Counters).filter(
                         (Counters.counter_no == 3)).with_for_update().first()
                counters.counter = counters.counter + 1
                mbill.rechnr = counters.counter

                master.rechnr = mbill.rechnr
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

                # counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
                counters = db_session.query(Counters).filter(
                         (Counters.counter_no == 3)).with_for_update().first()
                counters.counter = counters.counter + 1
                mbill.rechnr = counters.counter
                master.rechnr = mbill.rechnr
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
            bill_line.userinit = user_init
            bill_line.bill_datum = bill_date

            if curr_posting.lower()  == ("room charge").lower() :
                bill_line.massnr = res_line.resnr
                bill_line.billin_nr = res_line.reslinnr
                bill_line.arrangement = res_line.arrangement


            pass

            # umsatz = get_cache (Umsatz, {"artnr": [(eq, billart)],"departement": [(eq, artikel.departement)],"datum": [(eq, bill_date)]})
            umsatz = db_session.query(Umsatz).filter(
                     (Umsatz.artnr == billart) & (Umsatz.departement == artikel.departement) & (Umsatz.datum == bill_date)).with_for_update().first()

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
            billjournal.userinit = user_init
            billjournal.bill_datum = bill_date

            if curr_posting.lower()  == ("room charge").lower() :
                billjournal.comment = to_string(res_line.resnr) + ";" + to_string(res_line.reslinnr)
            pass

            if curr_posting.lower()  == ("room charge").lower() :

                if amount != 0:
                    i_master_taxserv(currzeit, mbill._recid)
            pass

        return generate_inner_output()

    def tax_service(currzeit:int):

        nonlocal user_init, master_flag, gastnrmember, amount, amount_foreign, description, bill_date, price_decimal, exchg_rate, ex_rate, double_currency, foreign_rate, billart, qty, curr_room, cancel_str, master_str, master_rechnr, curr_department, price, i, n, htparam, res_line, waehrung, arrangement, artikel, bill, counters, bill_line, umsatz, billjournal, argt_line
        nonlocal resnr, reslinnr

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
        Artikel1 =  create_buffer("Artikel1",Artikel)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 127)]})
        rm_vat = not htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 128)]})
        rm_serv = not htparam.flogical
        rest_betrag =  to_decimal(amount)

        for argt_line in db_session.query(Argt_line).filter(
                 (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():
            post_it = False
            argt_betrag0, ex_rate = get_output(argt_betragbl(res_line._recid, argt_line._recid))
            argt_betrag =  to_decimal(round(argt_betrag0 * ex_rate, price_decimal))

            artikel1 = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})

            if argt_line.fakt_modus == 1:
                post_it = True

            elif argt_line.fakt_modus == 2 or argt_line.fakt_modus == 3:

                billjournal = get_cache (Billjournal, {"rechnr": [(eq, bill.rechnr)],"artnr": [(eq, artikel1.artnr)],"betrag": [(eq, argt_betrag)],"departement": [(eq, artikel1.departement)]})

                if not billjournal:
                    post_it = True

            elif argt_line.fakt_modus == 4:

                if get_day(bill_date) == 1:
                    post_it = True

            elif argt_line.fakt_modus == 5:

                if get_day(bill_date + 1) == 1:
                    post_it = True

            if post_it and argt_betrag != 0:
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
                umsatz.anzahl = umsatz.anzahl + qty
                
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = qty
                billjournal.fremdwaehrng =  to_decimal(argt_betrag0)
                billjournal.betrag =  to_decimal(argt_betrag)
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = res_line.zinr
                billjournal.departement = artikel1.departement
                billjournal.epreis =  to_decimal("0")
                billjournal.zeit = currzeit
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date
                pass

        artikel1 = get_cache (Artikel, {"artnr": [(eq, arrangement.artnr_logis)],"departement": [(eq, artikel.departement)]})

        umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel1.artnr)],"departement": [(eq, artikel1.departement)],"datum": [(eq, bill_date)]})

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artikel1.artnr
            umsatz.datum = bill_date
            umsatz.departement = artikel1.departement
        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(rest_betrag)
        umsatz.anzahl = umsatz.anzahl + 1
        pass
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = bill.rechnr
        billjournal.artnr = artikel1.artnr
        billjournal.anzahl = 1
        billjournal.fremdwaehrng =  to_decimal(round(rest_betrag / exchg_rate, 2))
        billjournal.betrag =  to_decimal(rest_betrag)
        billjournal.bezeich = artikel1.bezeich
        billjournal.zinr = res_line.zinr
        billjournal.departement = artikel1.departement
        billjournal.epreis =  to_decimal("0")
        billjournal.zeit = currzeit
        billjournal.stornogrund = ""
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date
        pass

        if rm_serv and artikel.service_code != 0:

            htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.service_code)]})

            if htparam and htparam.fdecimal != 0:
                service =  to_decimal(htparam.fdecimal)

                htparam = get_cache (Htparam, {"paramnr": [(eq, 133)]})

                artikel1 = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, artikel.departement)]})
                service =  to_decimal(service) * to_decimal(amount_foreign) / to_decimal("100")
                service_foreign =  to_decimal(round(service, 2))

                if double_currency:
                    service =  to_decimal(round(service * exchg_rate, price_decimal))
                else:
                    service =  to_decimal(round(service, price_decimal))

                bill_line = Bill_line()
                db_session.add(bill_line)

                bill_line.rechnr = bill.rechnr
                bill_line.artnr = artikel1.artnr
                bill_line.bezeich = artikel1.bezeich
                bill_line.anzahl = 1
                bill_line.fremdwbetrag =  to_decimal(service_foreign)
                bill_line.betrag =  to_decimal(service)
                bill_line.zinr = res_line.zinr
                bill_line.departement = artikel1.departement
                bill_line.epreis =  to_decimal("0")
                bill_line.zeit = currzeit + 1
                bill_line.userinit = user_init
                bill_line.arrangement = res_line.arrangement
                bill_line.bill_datum = bill_date
                bill_line.massnr = res_line.resnr
                bill_line.billin_nr = res_line.reslinnr


                pass

                umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel1.artnr)],"departement": [(eq, artikel1.departement)],"datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = artikel1.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = artikel1.departement
                umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(service)
                umsatz.anzahl = umsatz.anzahl + 1
                pass
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = 1
                billjournal.fremdwaehrng =  to_decimal(service_foreign)
                billjournal.betrag =  to_decimal(service)
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = res_line.zinr
                billjournal.departement = artikel1.departement
                billjournal.epreis =  to_decimal("0")
                billjournal.zeit = currzeit + 1
                billjournal.stornogrund = ""
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date
                pass

        if rm_vat and artikel.mwst_code != 0:

            htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.mwst_code)]})

            if htparam and htparam.fdecimal != 0:
                vat =  to_decimal(htparam.fdecimal)

                htparam = get_cache (Htparam, {"paramnr": [(eq, 132)]})

                artikel1 = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, artikel.departement)]})

                htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})

                if htparam.flogical:
                    vat =  to_decimal(vat) * to_decimal((amount_foreign) + to_decimal(service_foreign)) / to_decimal("100")
                else:
                    vat =  to_decimal(vat) * to_decimal(amount_foreign) / to_decimal("100")
                vat_foreign =  to_decimal(round(vat , 2))

                if double_currency:
                    vat =  to_decimal(round(vat * exchg_rate, price_decimal))
                else:
                    vat =  to_decimal(round(vat, price_decimal))
                bill_line = Bill_line()
                db_session.add(bill_line)

                bill_line.rechnr = bill.rechnr
                bill_line.artnr = artikel1.artnr
                bill_line.bezeich = artikel1.bezeich
                bill_line.anzahl = 1
                bill_line.fremdwbetrag =  to_decimal(vat_foreign)
                bill_line.betrag =  to_decimal(vat)
                bill_line.zinr = res_line.zinr
                bill_line.departement = artikel1.departement
                bill_line.epreis =  to_decimal("0")
                bill_line.zeit = currzeit + 2
                bill_line.userinit = user_init
                bill_line.arrangement = res_line.arrangement
                bill_line.bill_datum = bill_date
                bill_line.massnr = res_line.resnr
                bill_line.billin_nr = res_line.reslinnr


                pass

                umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel1.artnr)],"departement": [(eq, artikel.departement)],"datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = artikel1.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = artikel1.departement
                umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(vat)
                umsatz.anzahl = umsatz.anzahl + 1
                pass
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = 1
                billjournal.fremdwaehrng =  to_decimal(vat_foreign)
                billjournal.betrag =  to_decimal(vat)
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = res_line.zinr
                billjournal.departement = artikel1.departement
                billjournal.epreis =  to_decimal("0")
                billjournal.zeit = currzeit + 2
                billjournal.stornogrund = ""
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date
                pass
        bill.saldo =  to_decimal(bill.saldo) + to_decimal(vat) + to_decimal(service)
        bill.mwst[98] = bill.mwst[98] + vat_foreign + service_foreign

    htparam = get_cache (Htparam, {"paramnr": [(eq, 104)]})
    user_init = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})
    gastnrmember = res_line.gastnrmember
    price =  to_decimal(res_line.zipreis)
    amount =  to_decimal(res_line.zipreis)
    curr_room = res_line.zinr

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    foreign_rate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    double_currency = htparam.flogical

    if double_currency or foreign_rate or res_line.betriebsnr != 0:

        if res_line.betriebsnr != 0:

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

            if res_line.adrflag and res_line.betriebsnr == 0:
                exchg_rate =  to_decimal("1")
            amount_foreign =  to_decimal(res_line.zipreis)
            amount =  to_decimal(round(res_line.zipreis) * (exchg_rate))

            if foreign_rate and price_decimal == 0:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 145)]})

                if htparam.finteger != 0:
                    n = 1
                    for i in range(1,htparam.finteger + 1) :
                        n = n * 10
                    amount = to_decimal(round(amount / n , 0) * n)

    arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

    artikel = get_cache (Artikel, {"departement": [(eq, 0)],"artnr": [(eq, arrangement.argt_artikelnr)]})
    billart = artikel.artnr
    description = arrangement.argt_rgbez

    bill = get_cache (Bill, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)],"zinr": [(eq, res_line.zinr)],"billnr": [(eq, 1)],"flag": [(eq, 0)]})
    currzeit = get_current_time_in_seconds()
    master_flag = update_masterbill(currzeit)

    if not master_flag:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        bill_date = htparam.fdate

        bill = get_cache (Bill, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)],"zinr": [(eq, res_line.zinr)],"billnr": [(eq, 1)],"flag": [(eq, 0)]})

        if artikel.umsatzart == 1:
            bill.logisumsatz =  to_decimal(bill.logisumsatz) + to_decimal(amount)

        elif artikel.umsatzart == 2:
            bill.argtumsatz =  to_decimal(bill.argtumsatz) + to_decimal(amount)

        elif artikel.umsatzart == 3:
            bill.f_b_umsatz =  to_decimal(bill.f_b_umsatz) + to_decimal(amount)

        elif artikel.umsatzart == 4:
            bill.sonst_umsatz =  to_decimal(bill.sonst_umsatz) + to_decimal(amount)

        if artikel.umsatzart >= 1 and artikel.umsatzart <= 4:
            bill.gesamtumsatz =  to_decimal(bill.gesamtumsatz) + to_decimal(amount)
        bill.rgdruck = 0
        bill.saldo =  to_decimal(bill.saldo) + to_decimal(amount)
        bill.mwst[98] = bill.mwst[98] + amount_foreign

        if bill.datum < bill_date:
            bill.datum = bill_date

        if bill.rechnr == 0:

            # counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
            counters = db_session.query(Counters).filter(
                     (Counters.counter_no == 3)).with_for_update().first()
            counters.counter = counters.counter + 1
            bill.rechnr = counters.counter
            
            pass
        bill_line = Bill_line()
        db_session.add(bill_line)

        bill_line.rechnr = bill.rechnr
        bill_line.artnr = artikel.artnr
        bill_line.bezeich = description
        bill_line.anzahl = 1
        bill_line.betrag =  to_decimal(amount)
        bill_line.fremdwbetrag =  to_decimal(amount_foreign)
        bill_line.zinr = res_line.zinr
        bill_line.departement = artikel.departement
        bill_line.zeit = currzeit
        bill_line.userinit = user_init
        bill_line.arrangement = res_line.arrangement
        bill_line.bill_datum = bill_date
        bill_line.massnr = res_line.resnr
        bill_line.billin_nr = res_line.reslinnr

        if double_currency:
            bill_line.epreis =  to_decimal(amount_foreign)
        else:
            bill_line.epreis =  to_decimal(amount)
        pass

        # umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel.artnr)],"departement": [(eq, artikel.departement)],"datum": [(eq, bill_date)]})
        umsatz = db_session.query(Umsatz).filter(
                     (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == artikel.departement) & (Umsatz.datum == bill_date)).with_for_update().first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artikel.artnr
            umsatz.datum = bill_date
            umsatz.departement = artikel.departement
        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(amount)
        umsatz.anzahl = umsatz.anzahl + 1
        pass
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = bill.rechnr
        billjournal.artnr = artikel.artnr
        billjournal.anzahl = 1
        billjournal.betrag =  to_decimal(amount)
        billjournal.fremdwaehrng =  to_decimal(amount_foreign)
        billjournal.bezeich = description
        billjournal.zinr = res_line.zinr
        billjournal.departement = artikel.departement

        if double_currency:
            billjournal.epreis =  to_decimal(amount_foreign)
        else:
            billjournal.epreis =  to_decimal(amount)
        billjournal.zeit = currzeit
        billjournal.stornogrund = ""
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date
        pass
        tax_service(currzeit)
        pass


    return generate_output()