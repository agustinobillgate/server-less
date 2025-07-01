#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.argt_betrag import argt_betrag
from models import Artikel, Bill, Arrangement, Htparam, Res_line, Argt_line, Umsatz, Billjournal, Bill_line

def fo_invoice_rev_bdownbl(bil_recid:int, currzeit:int, exchg_rate:Decimal, amount:Decimal, t_artnr:int, t_dept:int, arran_argtnr:int, price_decimal:int, bill_date:date, curr_room:string, cancel_str:string, user_init:string, curr_department:int, qty:int, double_currency:bool, foreign_rate:bool, price:Decimal, balance_foreign:Decimal):

    prepare_cache ([Artikel, Bill, Arrangement, Htparam, Res_line, Argt_line, Umsatz, Billjournal, Bill_line])

    balance = to_decimal("0.0")
    rm_vat:bool = False
    rm_serv:bool = False
    service:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    service_foreign:Decimal = to_decimal("0.0")
    vat_foreign:Decimal = to_decimal("0.0")
    rest_betrag:Decimal = to_decimal("0.0")
    argt_betrag:Decimal = to_decimal("0.0")
    frate:Decimal = to_decimal("0.0")
    p_sign:int = 1
    qty1:int = 0
    ex_rate:Decimal = to_decimal("0.0")
    artikel = bill = arrangement = htparam = res_line = argt_line = umsatz = billjournal = bill_line = None

    artikel1 = None

    Artikel1 = create_buffer("Artikel1",Artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal balance, rm_vat, rm_serv, service, vat, service_foreign, vat_foreign, rest_betrag, argt_betrag, frate, p_sign, qty1, ex_rate, artikel, bill, arrangement, htparam, res_line, argt_line, umsatz, billjournal, bill_line
        nonlocal bil_recid, currzeit, exchg_rate, amount, t_artnr, t_dept, arran_argtnr, price_decimal, bill_date, curr_room, cancel_str, user_init, curr_department, qty, double_currency, foreign_rate, price, balance_foreign
        nonlocal artikel1


        nonlocal artikel1

        return {"balance": balance}


    bill = get_cache (Bill, {"_recid": [(eq, bil_recid)]})

    artikel = get_cache (Artikel, {"artnr": [(eq, t_artnr)],"departement": [(eq, t_dept)]})

    arrangement = get_cache (Arrangement, {"argtnr": [(eq, arran_argtnr)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 127)]})
    rm_vat = not htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 128)]})
    rm_serv = not htparam.flogical

    res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})

    if res_line:

        if res_line.adrflag:
            frate =  to_decimal("1")

        elif res_line.reserve_dec != 0:
            frate =  to_decimal(res_line.reserve_dec)
    else:
        frate =  to_decimal(exchg_rate)
    rest_betrag =  to_decimal(amount)

    if amount < 0:
        p_sign = -1

    for argt_line in db_session.query(Argt_line).filter(
             (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():
        argt_betrag, ex_rate = get_output(argt_betrag(res_line._recid, argt_line._recid))
        argt_betrag =  to_decimal(round (argt_betrag) * to_decimal(ex_rate , price_decimal))
        rest_betrag =  to_decimal(rest_betrag) - to_decimal(argt_betrag) * to_decimal(p_sign)

        if argt_betrag != 0:

            if argt_line.vt_percnt == 0:

                if argt_line.betriebsnr == 0:
                    qty1 = res_line.erwachs * p_sign
                else:
                    qty1 = argt_line.betriebsnr * p_sign

            elif argt_line.vt_percnt == 1:

                if argt_line.betriebsnr == 0:
                    qty1 = res_line.kind1 * p_sign
                else:
                    qty1 = argt_line.betriebsnr * p_sign

            elif argt_line.vt_percnt == 2:

                if argt_line.betriebsnr == 0:
                    qty1 = res_line.kind2 * p_sign
                else:
                    qty1 = argt_line.betriebsnr * p_sign

            artikel1 = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})

            umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel1.artnr)],"departement": [(eq, artikel1.departement)],"datum": [(eq, bill_date)]})

            if not umsatz:
                umsatz = Umsatz()
                db_session.add(umsatz)

                umsatz.artnr = artikel1.artnr
                umsatz.datum = bill_date
                umsatz.departement = artikel1.departement


            umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(argt_betrag) * to_decimal(p_sign)
            umsatz.anzahl = umsatz.anzahl + qty1


            pass
            billjournal = Billjournal()
            db_session.add(billjournal)

            billjournal.rechnr = bill.rechnr
            billjournal.artnr = artikel1.artnr
            billjournal.anzahl = qty1
            billjournal.fremdwaehrng =  to_decimal(argt_line.betrag) * to_decimal(p_sign)
            billjournal.betrag =  to_decimal(argt_betrag) * to_decimal(p_sign)
            billjournal.bezeich = artikel1.bezeich
            billjournal.zinr = curr_room
            billjournal.departement = artikel1.departement
            billjournal.epreis =  to_decimal("0")
            billjournal.zeit = currzeit
            billjournal.stornogrund = cancel_str
            billjournal.userinit = user_init
            billjournal.bill_datum = bill_date


            pass

    artikel1 = get_cache (Artikel, {"artnr": [(eq, arrangement.artnr_logis)],"departement": [(eq, curr_department)]})

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

    billjournal.rechnr = bill.rechnr
    billjournal.artnr = artikel1.artnr
    billjournal.anzahl = qty
    billjournal.betrag =  to_decimal(rest_betrag)
    billjournal.bezeich = artikel1.bezeich
    billjournal.zinr = curr_room
    billjournal.departement = artikel1.departement
    billjournal.epreis =  to_decimal("0")
    billjournal.zeit = currzeit
    billjournal.stornogrund = cancel_str
    billjournal.userinit = user_init
    billjournal.bill_datum = bill_date

    if double_currency:
        billjournal.fremdwaehrng =  to_decimal(round (rest_betrag) / to_decimal(exchg_rate , 6))
    pass

    if rm_serv and artikel.service_code != 0:

        htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.service_code)]})

        if htparam and htparam.fdecimal != 0:
            service =  to_decimal(htparam.fdecimal)

            htparam = get_cache (Htparam, {"paramnr": [(eq, 133)]})

            artikel1 = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, curr_department)]})
            service =  to_decimal(service) * to_decimal(price) / to_decimal("100")
            service_foreign =  to_decimal(round (service , 2)) * to_decimal(qty)

            if double_currency:
                service =  to_decimal(round (service) * to_decimal(exchg_rate , price_decimal)) * to_decimal(qty)
            else:
                service =  to_decimal(round (service , price_decimal)) * to_decimal(qty)

            if artikel1.umsatzart == 1:
                bill.logisumsatz =  to_decimal(bill.logisumsatz) + to_decimal(service)
                bill.argtumsatz =  to_decimal(bill.argtumsatz) + to_decimal(service)

            elif artikel1.umsatzart == 2:
                bill.argtumsatz =  to_decimal(bill.argtumsatz) + to_decimal(service)

            elif (artikel1.umsatzart == 3 or artikel1.umsatzart == 5 or artikel1.umsatzart == 6):
                bill.f_b_umsatz =  to_decimal(bill.f_b_umsatz) + to_decimal(service)

            elif artikel1.umsatzart == 4:
                bill.sonst_umsatz =  to_decimal(bill.sonst_umsatz) + to_decimal(service)

            if artikel1.umsatzart >= 1 and artikel1.umsatzart <= 4:
                bill.gesamtumsatz =  to_decimal(bill.gesamtumsatz) + to_decimal(service)
            bill_line = Bill_line()
            db_session.add(bill_line)

            bill_line.rechnr = bill.rechnr
            bill_line.artnr = artikel1.artnr
            bill_line.bezeich = artikel1.bezeich
            bill_line.anzahl = qty
            bill_line.fremdwbetrag =  to_decimal(service_foreign)
            bill_line.betrag =  to_decimal(service)
            bill_line.zinr = curr_room
            bill_line.departement = artikel1.departement
            bill_line.epreis =  to_decimal("0")
            bill_line.zeit = currzeit + 1
            bill_line.userinit = user_init
            bill_line.bill_datum = bill_date

            if res_line:
                bill_line.arrangement = res_line.arrangement
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
            billjournal.zinr = curr_room
            billjournal.departement = artikel1.departement
            billjournal.epreis =  to_decimal("0")
            billjournal.zeit = currzeit + 1
            billjournal.stornogrund = cancel_str
            billjournal.userinit = user_init
            billjournal.bill_datum = bill_date


            pass

    if rm_vat and artikel.mwst_code != 0:

        htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.mwst_code)]})

        if htparam and htparam.fdecimal != 0:
            vat =  to_decimal(htparam.fdecimal)

            htparam = get_cache (Htparam, {"paramnr": [(eq, 132)]})

            artikel1 = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, curr_department)]})

            htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})

            if htparam.flogical:
                vat =  to_decimal(vat) * to_decimal((price) + to_decimal(service_foreign) / to_decimal(qty)) / to_decimal("100")
            else:
                vat =  to_decimal(vat) * to_decimal(price) / to_decimal("100")
            vat_foreign =  to_decimal(round (vat , 2)) * to_decimal(qty)

            if double_currency:
                vat =  to_decimal(round (vat) * to_decimal(exchg_rate , price_decimal)) * to_decimal(qty)
            else:
                vat =  to_decimal(round (vat , price_decimal)) * to_decimal(qty)

            if artikel1.umsatzart == 1:
                bill.logisumsatz =  to_decimal(bill.logisumsatz) + to_decimal(vat)
                bill.argtumsatz =  to_decimal(bill.argtumsatz) + to_decimal(vat)

            elif artikel1.umsatzart == 2:
                bill.argtumsatz =  to_decimal(bill.argtumsatz) + to_decimal(vat)

            elif (artikel1.umsatzart == 3 or artikel1.umsatzart == 5 or artikel1.umsatzart == 6):
                bill.f_b_umsatz =  to_decimal(bill.f_b_umsatz) + to_decimal(vat)

            elif artikel1.umsatzart == 4:
                bill.sonst_umsatz =  to_decimal(bill.sonst_umsatz) + to_decimal(vat)

            if artikel1.umsatzart >= 1 and artikel1.umsatzart <= 4:
                bill.gesamtumsatz =  to_decimal(bill.gesamtumsatz) + to_decimal(vat)
            bill_line = Bill_line()
            db_session.add(bill_line)

            bill_line.rechnr = bill.rechnr
            bill_line.artnr = artikel1.artnr
            bill_line.bezeich = artikel1.bezeich
            bill_line.anzahl = qty
            bill_line.fremdwbetrag =  to_decimal(vat_foreign)
            bill_line.betrag =  to_decimal(vat)
            bill_line.zinr = curr_room
            bill_line.departement = artikel1.departement
            bill_line.epreis =  to_decimal("0")
            bill_line.zeit = currzeit + 2
            bill_line.userinit = user_init
            bill_line.bill_datum = bill_date

            if res_line:
                bill_line.arrangement = res_line.arrangement
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
            billjournal.zinr = curr_room
            billjournal.departement = artikel1.departement
            billjournal.epreis =  to_decimal("0")
            billjournal.zeit = currzeit + 2
            billjournal.stornogrund = cancel_str
            billjournal.userinit = user_init
            billjournal.bill_datum = bill_date


            pass
    bill.saldo =  to_decimal(bill.saldo) + to_decimal(vat) + to_decimal(service)

    if price_decimal == 0 and bill.saldo <= 0.4 and bill.saldo >= -0.4:
        bill.saldo =  to_decimal("0")

    if double_currency or foreign_rate:
        bill.mwst[98] = bill.mwst[98] + vat_foreign + service_foreign
    balance =  to_decimal(bill.saldo)

    if double_currency or foreign_rate:
        balance_foreign =  to_decimal(bill.mwst[98])

    return generate_output()