from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Debitor, Htparam, Waehrung, Bediener, Artikel, Guest, Umsatz, Billjournal

def ts_restinv_rinv_arbl(curr_art:int, curr_dept:int, zinr:str, gastnr:int, gastnrmember:int, rechnr:int, saldo:decimal, saldo_foreign:decimal, bill_date:date, billname:str, userinit:str, voucher_nr:str, deptname:str):
    debitor = htparam = waehrung = bediener = artikel = guest = umsatz = billjournal = None

    debt = None

    Debt = Debitor

    db_session = local_storage.db_session

    def generate_output():
        nonlocal debitor, htparam, waehrung, bediener, artikel, guest, umsatz, billjournal
        nonlocal debt


        nonlocal debt
        return {}

    def inv_ar():

        nonlocal debitor, htparam, waehrung, bediener, artikel, guest, umsatz, billjournal
        nonlocal debt


        nonlocal debt

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


    inv_ar()

    return generate_output()