from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import H_bill, H_artikel, Htparam, Kellne1, H_bill_line, H_umsatz, H_journal, Umsatz, Guest, Artikel, Debitor, Waehrung, Bediener, Billjournal

def ts_closeinv_update_billbl(amount:decimal, amount_foreign:decimal, balance:decimal, rec_bill_guest:int, foreign_rate:bool, curr_dept:int, rec_h_artikel:int, rec_h_bill:int, h_artart:int, h_artnrfront:int, unit_price:decimal, double_currency:bool, exchg_rate:decimal, price_decimal:int, qty:int, kreditlimit:decimal, billart:int, description:str, change_str:str, nett_amount:decimal, tischnr:int, price:decimal, bill_date:date, b_list_departement:int, avail_b_list:bool, cc_comment:str, b_list_waehrungsnr:int, hoga_card:str, cancel_str:str, req_str:str, curr_waiter:int, pay_type:int, transfer_zinr:str, curr_room:str, user_init:str, deptname:str):
    service_foreign = 0
    mwst_foreign = 0
    service = 0
    mwst = 0
    bcol = 0
    balance_foreign = 0
    closed = False
    t_h_bill_list = []
    h_service:decimal = 0
    h_service_foreign:decimal = 0
    h_mwst:decimal = 0
    h_mwst_foreign:decimal = 0
    sysdate:date = None
    zeit:int = 0
    h_bill = h_artikel = htparam = kellne1 = h_bill_line = h_umsatz = h_journal = umsatz = guest = artikel = debitor = waehrung = bediener = billjournal = None

    t_h_bill = bill_guest = debt = None

    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})

    Bill_guest = Guest
    Debt = Debitor

    db_session = local_storage.db_session

    def generate_output():
        nonlocal service_foreign, mwst_foreign, service, mwst, bcol, balance_foreign, closed, t_h_bill_list, h_service, h_service_foreign, h_mwst, h_mwst_foreign, sysdate, zeit, h_bill, h_artikel, htparam, kellne1, h_bill_line, h_umsatz, h_journal, umsatz, guest, artikel, debitor, waehrung, bediener, billjournal
        nonlocal bill_guest, debt


        nonlocal t_h_bill, bill_guest, debt
        nonlocal t_h_bill_list
        return {"service_foreign": service_foreign, "mwst_foreign": mwst_foreign, "service": service, "mwst": mwst, "bcol": bcol, "balance_foreign": balance_foreign, "closed": closed, "t-h-bill": t_h_bill_list}

    def inv_ar(curr_art:int, curr_dept:int, zinr:str, gastnr:int, gastnrmember:int, rechnr:int, saldo:decimal, saldo_foreign:decimal, bill_date:date, billname:str, userinit:str, voucher_nr:str):

        nonlocal service_foreign, mwst_foreign, service, mwst, bcol, balance_foreign, closed, t_h_bill_list, h_service, h_service_foreign, h_mwst, h_mwst_foreign, sysdate, zeit, h_bill, h_artikel, htparam, kellne1, h_bill_line, h_umsatz, h_journal, umsatz, guest, artikel, debitor, waehrung, bediener, billjournal
        nonlocal bill_guest, debt


        nonlocal t_h_bill, bill_guest, debt
        nonlocal t_h_bill_list

        exchg_rate:decimal = 1
        foreign_rate:bool = False
        double_currency:bool = False
        ar_license:bool = False
        Debt = Debitor

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 143)).first()
        foreign_rate = htparam.fLOGICAL

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 240)).first()
        double_currency = htparam.fLOGICAL

        if foreign_rate:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 144)).first()

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrung.wabkurz == htparam.fchar)).first()

            if waehrung:
                exchg_rate = waehrung.ankauf / waehrung.einheit

        if exchg_rate != 1:
            saldo_foreign = round(saldo / exchg_rate, 2)

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.(userinit).lower()) == (userinit).lower())).first()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 997)).first()
        ar_license = htparam.flogical

        artikel = db_session.query(Artikel).filter(
                (Artikel.departement == 0) &  (Artikel.artnr == curr_art)).first()

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == gastnr)).first()
        billname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

        debt = db_session.query(Debt).filter(
                (Debt.artnr == curr_art) &  (Debt.rechnr == rechnr) &  (Debt.opart == 0) &  (Debt.betriebsnr == curr_dept) &  (Debt.rgdatum == bill_date) &  (Debt.counter == 0) &  (Debt.saldo == saldo)).first()

        if debt:

            debt = db_session.query(Debt).first()
            db_session.delete(debt)

            umsatz = db_session.query(Umsatz).filter(
                    (Umsatz.departement == 0) &  (Umsatz.artnr == curr_art) &  (Umsatz.datum == bill_date)).first()
            umsatz.anzahl = umsatz.anzahl - 1
            umsatz.betrag = umsatz.betrag + saldo

            umsatz = db_session.query(Umsatz).first()

            billjournal = Billjournal()
            db_session.add(billjournal)

            billjournal.rechnr = rechnr
            billjournal.bill_datum = bill_date
            billjournal.artnr = curr_art
            billjournal.betriebsnr = curr_dept
            billjournal.anzahl = 1
            billjournal.betrag = saldo

            if double_currency:
                billjournal.fremdwaehrng = saldo_foreign
            billjournal.bezeich = artikel.bezeich
            billjournal.zinr = zinr
            billjournal.zeit = get_current_time_in_seconds()
            billjournal.bediener_nr = bediener.nr
            billjournal.userinit = userinit


            return

        if ar_license:

            if voucher_nr != "":
                voucher_nr = "/" + voucher_nr
            debitor = Debitor()
            db_session.add(debitor)

            debitor.artnr = curr_art
            debitor.betrieb_gastmem = artikel.betriebsnr
            debitor.betriebsnr = curr_dept
            debitor.zinr = zinr
            debitor.gastnr = gastnr
            debitor.gastnrmember = gastnrmember
            debitor.rechnr = rechnr
            debitor.saldo = - saldo
            debitor.transzeit = get_current_time_in_seconds()
            debitor.rgdatum = bill_date
            debitor.bediener_nr = bediener.nr
            debitor.name = billname
            debitor.vesrcod = deptname + voucher_nr

            if double_currency or foreign_rate:
                debitor.vesrdep = - saldo_foreign


        umsatz = db_session.query(Umsatz).filter(
                (Umsatz.departement == 0) &  (Umsatz.artnr == curr_art) &  (Umsatz.datum == bill_date)).first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = curr_art
            umsatz.datum = bill_date
        umsatz.anzahl = umsatz.anzahl + 1
        umsatz.betrag = umsatz.betrag + saldo

        umsatz = db_session.query(Umsatz).first()

        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = rechnr
        billjournal.bill_datum = bill_date
        billjournal.artnr = curr_art
        billjournal.betriebsnr = curr_dept
        billjournal.anzahl = 1
        billjournal.betrag = saldo

        if double_currency:
            billjournal.fremdwaehrng = saldo_foreign
        billjournal.bezeich = artikel.bezeich
        billjournal.zinr = zinr
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.bediener_nr = bediener.nr
        billjournal.userinit = userinit


    h_artikel = db_session.query(H_artikel).filter(
            (H_artikel._recid == rec_h_artikel)).first()

    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_h_bill)).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 135)).first()

    if not htparam.flogical and h_artart == 0 and h_artikel.service_code != 0:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == h_artikel.service_code)).first()

        if htparam.fdecimal != 0:
            h_service = unit_price * htparam.fdecimal / 100
            h_service_foreign = round(h_service, 2)

            if double_currency:
                h_service = round(h_service * exchg_rate, price_decimal)
            else:
                h_service = round(h_service, price_decimal)
            service = service + h_service * qty
            service_foreign = service_foreign + h_service_foreign * qty

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 134)).first()

    if not htparam.flogical and h_artart == 0 and h_artikel.mwst_code != 0:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == h_artikel.mwst_code)).first()

        if htparam.fdecimal != 0:
            h_mwst = htparam.fdecimal

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 479)).first()

            if htparam.flogical:
                h_mwst = h_mwst * (unit_price + h_service_foreign) / 100
            else:
                h_mwst = h_mwst * unit_price / 100
            h_mwst_foreign = round(h_mwst, 2)

            if double_currency:
                h_mwst = round(h_mwst * exchg_rate, price_decimal)
            else:
                h_mwst = round(h_mwst, price_decimal)
            mwst = mwst + h_mwst * qty
            mwst_foreign = mwst_foreign + h_mwst_foreign * qty
    amount = amount + (h_service + h_mwst) * qty
    amount_foreign = amount_foreign + (h_service_foreign + h_mwst_foreign) * qty

    h_bill = db_session.query(H_bill).first()

    kellne1 = db_session.query(Kellne1).filter(
                (Kellne1.kellner_nr == h_bill.kellner_nr) &  (Kellne1.departement == curr_dept)).first()

    if h_artart == 0:
        h_bill.gesamtumsatz = h_bill.gesamtumsatz + amount
    balance = balance + amount

    if balance <= kreditlimit:
        bcol = 2
    h_bill.saldo = h_bill.saldo + amount
    h_bill.mwst[98] = h_bill.mwst[98] + amount_foreign
    balance = h_bill.saldo
    balance_foreign = h_bill.mwst[98]

    if balance != 0:
        h_bill.rgdruck = 0

    if balance <= kreditlimit:
        bcol = 2
    sysdate = get_current_date()
    zeit = get_current_time_in_seconds()
    h_bill_line = H_bill_line()
    db_session.add(h_bill_line)

    h_bill_line.rechnr = h_bill.rechnr
    h_bill_line.artnr = billart
    h_bill_line.bezeich = description + change_str
    h_bill_line.anzahl = qty
    h_bill_line.nettobetrag = nett_amount
    h_bill_line.fremdwbetrag = amount_foreign
    h_bill_line.betrag = amount
    h_bill_line.tischnr = tischnr
    h_bill_line.departement = curr_dept
    h_bill_line.epreis = price
    h_bill_line.zeit = zeit
    h_bill_line.bill_datum = bill_date
    h_bill_line.sysdate = sysdate

    if avail_b_list and b_list_departement < 999:
        h_bill_line.bezeich = h_bill_line.bezeich + cc_comment

    if avail_b_list:
        h_bill_line.waehrungsnr = b_list_waehrungsnr

    if substring(description, 0, 5) == "RmNo " or substring(description, 0, 5) == "Card ":
        h_bill_line.segmentcode = to_int(substring(hoga_card, 0, 9))

    h_bill_line = db_session.query(H_bill_line).first()

    if billart != 0:

        h_umsatz = db_session.query(H_umsatz).filter(
                    (H_umsatz.artnr == billart) &  (H_umsatz.departement == curr_dept) &  (H_umsatz.datum == bill_date)).first()

        if not h_umsatz:
            h_umsatz = H_umsatz()
            db_session.add(h_umsatz)

            h_umsatz.artnr = billart
            h_umsatz.datum = bill_date
            h_umsatz.departement = curr_dept


        h_umsatz.betrag = h_umsatz.betrag + amount
        h_umsatz.anzahl = h_umsatz.anzahl + qty

        h_umsatz = db_session.query(H_umsatz).first()
    h_journal = H_journal()
    db_session.add(h_journal)

    h_journal.rechnr = h_bill.rechnr
    h_journal.artnr = billart
    h_journal.anzahl = qty
    h_journal.fremdwaehrng = amount_foreign

    if h_artikel:
        h_journal.artart = h_artikel.artart

    if h_artart == 6:
        h_journal.betrag = amount

        umsatz = db_session.query(Umsatz).filter(
                    (Umsatz.artnr == h_artikel.artnrfront) &  (Umsatz.departement == 0) &  (Umsatz.datum == bill_date)).first()

        if umsatz:

            umsatz = db_session.query(Umsatz).first()
        else:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = h_artikel.artnrfront
            umsatz.datum = bill_date
            umsatz.departement = 0


        umsatz.betrag = umsatz.betrag + amount
        umsatz.anzahl = umsatz.anzahl + qty

        umsatz = db_session.query(Umsatz).first()
    else:
        h_journal.betrag = amount
    h_journal.bezeich = description + change_str
    h_journal.tischnr = tischnr
    h_journal.departement = curr_dept
    h_journal.epreis = price
    h_journal.zeit = zeit
    h_journal.stornogrund = cancel_str
    h_journal.aendertext = req_str
    h_journal.kellner_nr = to_int(user_init)
    h_journal.bill_datum = bill_date
    h_journal.sysdate = sysdate
    h_journal.artnrfront = h_artnrfront

    if avail_b_list and b_list_departement < 999:
        h_journal.bezeich = h_journal.bezeich + cc_comment

    if billart == 0:
        h_journal.artart = 0
    else:
        h_journal.artart = h_artart

    if pay_type == 2:
        h_journal.zinr = transfer_zinr

    if h_artart == 11:
        h_journal.aendertext = h_bill.bilname
        h_journal.segmentcode = billart

    h_journal = db_session.query(H_journal).first()
    change_str = ""
    closed = False

    if h_artart == 2 or h_artart == 7:

        bill_guest = db_session.query(Bill_guest).filter(
                    (Bill_guest._recid == rec_bill_guest)).first()

        artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == 0)).first()

        if foreign_rate and not double_currency:
            amount_foreign = amount / exchg_rate

        if b_list_departement == 999:
            inv_ar(artikel.artnr, curr_dept, curr_room, bill_guest.gastnr, bill_guest.gastnr, h_bill.rechnr, amount, amount_foreign, bill_date, bill_guest.name, user_init, "")
        else:
            inv_ar(artikel.artnr, curr_dept, curr_room, bill_guest.gastnr, bill_guest.gastnr, h_bill.rechnr, amount, amount_foreign, bill_date, bill_guest.name, user_init, cc_comment)

    if h_artart == 2 or h_artart == 7 or h_artart == 11 or h_artart == 12:

        if balance == 0:
            closed = True

            h_bill = db_session.query(H_bill).first()
            h_bill.flag = 1

            h_bill = db_session.query(H_bill).first()


    h_bill = db_session.query(H_bill).first()
    t_h_bill = T_h_bill()
    t_h_bill_list.append(t_h_bill)

    buffer_copy(h_bill, t_h_bill)
    t_h_bill.rec_id = h_bill._recid

    return generate_output()