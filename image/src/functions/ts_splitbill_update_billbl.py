from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Kellner, Guest, Hoteldpt, Htparam, Waehrung, H_bill, H_artikel, H_bill_line, H_umsatz, H_journal, Umsatz, Artikel, Debitor, Bediener, Billjournal

def ts_splitbill_update_billbl(rec_id_h_bill:int, rec_id_h_artikel:int, h_artart:int, h_artnrfront:int, dept:int, amount:decimal, transdate:date, billart:int, description:str, change_str:str, qty:int, tischnr:int, price:decimal, add_zeit:int, curr_select:int, hoga_card:str, cancel_str:str, curr_waiter:int, amount_foreign:decimal, curr_room:str, user_init:str, cc_comment:str, guestnr:int):
    bill_date = None
    deptname:str = ""
    foreign_rate:bool = False
    exchg_rate:decimal = 1
    kellner = guest = hoteldpt = htparam = waehrung = h_bill = h_artikel = h_bill_line = h_umsatz = h_journal = umsatz = artikel = debitor = bediener = billjournal = None

    kellner1 = bill_guest = debt = None

    Kellner1 = Kellner
    Bill_guest = Guest
    Debt = Debitor

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, deptname, foreign_rate, exchg_rate, kellner, guest, hoteldpt, htparam, waehrung, h_bill, h_artikel, h_bill_line, h_umsatz, h_journal, umsatz, artikel, debitor, bediener, billjournal
        nonlocal kellner1, bill_guest, debt


        nonlocal kellner1, bill_guest, debt
        return {"bill_date": bill_date}

    def update_bill():

        nonlocal bill_date, deptname, foreign_rate, exchg_rate, kellner, guest, hoteldpt, htparam, waehrung, h_bill, h_artikel, h_bill_line, h_umsatz, h_journal, umsatz, artikel, debitor, bediener, billjournal
        nonlocal kellner1, bill_guest, debt


        nonlocal kellner1, bill_guest, debt

        closed:bool = False

        h_bill = db_session.query(H_bill).first()
        h_bill.kellner_nr = curr_waiter

        kellner1 = db_session.query(Kellner1).filter(
                    (Kellner1.kellner_nr == h_bill.kellner_nr) &  (Kellner1.departement == h_bill.departement)).first()
        h_bill.saldo = h_bill.saldo + amount

        if h_bill.saldo != 0:
            h_bill.rgdruck = 0

        htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 110)).first()
        bill_date = htparam.fdate

        if transdate != None:
            bill_date = transdate
        else:

            htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 253)).first()

            if htparam.flogical and bill_date < get_current_date():
                bill_date = bill_date + 1
        h_bill_line = H_bill_line()
        db_session.add(h_bill_line)

        h_bill_line.rechnr = h_bill.rechnr
        h_bill_line.artnr = billart
        h_bill_line.bezeich = description + change_str + cc_comment
        h_bill_line.anzahl = qty
        h_bill_line.nettobetrag = amount
        h_bill_line.betrag = amount
        h_bill_line.tischnr = tischnr
        h_bill_line.departement = h_bill.departement
        h_bill_line.epreis = price
        h_bill_line.zeit = get_current_time_in_seconds() + add_zeit
        h_bill_line.bill_datum = bill_date
        h_bill_line.waehrungsnr = curr_select
        h_bill_line.fremdwbetrag = amount_foreign

        if substring(description, 0, 5) == "RmNo " or substring(description, 0, 5) == "Card ":
            h_bill_line.segmentcode = to_int(substring(hoga_card, 0, 9))

        h_bill_line = db_session.query(H_bill_line).first()

        if billart != 0:

            h_umsatz = db_session.query(H_umsatz).filter(
                        (H_umsatz.artnr == billart) &  (H_umsatz.departement == h_bill.departement) &  (H_umsatz.datum == bill_date)).first()

            if not h_umsatz:
                h_umsatz = H_umsatz()
                db_session.add(h_umsatz)

                h_umsatz.artnr = billart
                h_umsatz.datum = bill_date
                h_umsatz.departement = h_bill.departement
            h_umsatz.betrag = h_umsatz.betrag + amount
            h_umsatz.anzahl = h_umsatz.anzahl + qty

            h_umsatz = db_session.query(H_umsatz).first()
        h_journal = H_journal()
        db_session.add(h_journal)

        h_journal.rechnr = h_bill.rechnr
        h_journal.artnr = billart
        h_journal.anzahl = qty
        h_journal.betrag = amount
        h_journal.bezeich = description + change_str + cc_comment
        h_journal.tischnr = tischnr
        h_journal.departement = h_bill.departement
        h_journal.epreis = price
        h_journal.zeit = get_current_time_in_seconds() + add_zeit
        h_journal.stornogrund = cancel_str
        h_journal.kellner_nr = curr_waiter
        h_journal.bill_datum = bill_date
        h_journal.artnrfront = h_artnrfront
        h_journal.aendertext = ""
        h_journal.artart = h_artart
        h_journal.waehrungcode = curr_select

        if h_artikel:
            h_journal.artart = h_artikel.artart

        h_journal = db_session.query(H_journal).first()

        if h_artart == 6:

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
            umsatz.anzahl = umsatz.anzahl + 1

            umsatz = db_session.query(Umsatz).first()
        closed = False

        if h_artart == 2 or h_artart == 7:

            artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == 0)).first()
            amount_foreign = 0

            if foreign_rate and amount_foreign == 0:
                amount_foreign = amount / exchg_rate

            htparam = db_session.query(Htparam).filter(
                        (htpara.paramnr == 867)).first()

            bill_guest = db_session.query(Bill_guest).filter(
                        (Bill_guest.gastnr == htparam.finteger)).first()
            inv_ar(artikel.artnr, h_bill.departement, curr_room, bill_guest.gastnr, bill_guest.gastnr, h_bill.rechnr, amount, amount_foreign, bill_date, bill_guest.name, user_init, cc_comment)

        h_bill = db_session.query(H_bill).first()
        put_paidflag()

    def inv_ar(curr_art:int, curr_dept:int, zinr:str, gastnr:int, gastnrmember:int, rechnr:int, saldo:decimal, saldo_foreign:decimal, bill_date:date, billname:str, userinit:str, voucher_nr:str):

        nonlocal deptname, foreign_rate, exchg_rate, kellner, guest, hoteldpt, htparam, waehrung, h_bill, h_artikel, h_bill_line, h_umsatz, h_journal, umsatz, artikel, debitor, bediener, billjournal
        nonlocal kellner1, bill_guest, debt


        nonlocal kellner1, bill_guest, debt

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


    def put_paidflag():

        nonlocal bill_date, deptname, foreign_rate, exchg_rate, kellner, guest, hoteldpt, htparam, waehrung, h_bill, h_artikel, h_bill_line, h_umsatz, h_journal, umsatz, artikel, debitor, bediener, billjournal
        nonlocal kellner1, bill_guest, debt


        nonlocal kellner1, bill_guest, debt

        if curr_select > 0:

            for h_bill_line in db_session.query(H_bill_line).filter(
                    (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.waehrungsnr == curr_select) &  (H_bill_line.departement == dept)).all():
                h_bill_line.paid_flag = 1
        else:

            for h_bill_line in db_session.query(H_bill_line).filter(
                    (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.departement == dept)).all():
                h_bill_line.paid_flag = 1


    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == dept)).first()
    deptname = hoteldpt.depart

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 143)).first()
    foreign_rate = htparam.flogical

    if foreign_rate:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            exchg_rate = waehrung.ankauf / waehrung.einheit

    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_id_h_bill)).first()

    h_artikel = db_session.query(H_artikel).filter(
            (H_artikel._recid == rec_id_h_artikel)).first()
    update_bill()

    return generate_output()