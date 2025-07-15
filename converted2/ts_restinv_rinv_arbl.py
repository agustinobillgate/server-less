#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Debitor, Htparam, Waehrung, Bediener, Artikel, Guest, Umsatz, Billjournal

def ts_restinv_rinv_arbl(curr_art:int, curr_dept:int, zinr:string, gastnr:int, gastnrmember:int, rechnr:int, saldo:Decimal, saldo_foreign:Decimal, bill_date:date, billname:string, userinit:string, voucher_nr:string, deptname:string):

    prepare_cache ([Htparam, Waehrung, Bediener, Artikel, Guest, Umsatz, Billjournal])

    debitor = htparam = waehrung = bediener = artikel = guest = umsatz = billjournal = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal debitor, htparam, waehrung, bediener, artikel, guest, umsatz, billjournal
        nonlocal curr_art, curr_dept, zinr, gastnr, gastnrmember, rechnr, saldo, saldo_foreign, bill_date, billname, userinit, voucher_nr, deptname

        return {}

    def inv_ar():

        nonlocal debitor, htparam, waehrung, bediener, artikel, guest, umsatz, billjournal
        nonlocal curr_art, curr_dept, zinr, gastnr, gastnrmember, rechnr, saldo, saldo_foreign, bill_date, billname, userinit, voucher_nr, deptname

        exchg_rate:Decimal = 1
        foreign_rate:bool = False
        double_currency:bool = False
        ar_license:bool = False
        debt = None
        Debt =  create_buffer("Debt",Debitor)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
        foreign_rate = htparam.fLOGICAL

        htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
        double_currency = htparam.fLOGICAL

        if foreign_rate:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

            if waehrung:
                exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

        if exchg_rate != 1:
            saldo_foreign = to_decimal(round(saldo / exchg_rate , 2))

        bediener = get_cache (Bediener, {"userinit": [(eq, userinit)]})

        htparam = get_cache (Htparam, {"paramnr": [(eq, 997)]})
        ar_license = htparam.flogical

        artikel = get_cache (Artikel, {"departement": [(eq, 0)],"artnr": [(eq, curr_art)]})

        guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})
        billname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

        debt = db_session.query(Debt).filter(
                 (Debt.artnr == curr_art) & (Debt.rechnr == rechnr) & (Debt.opart == 0) & (Debt.betriebsnr == curr_dept) & (Debt.rgdatum == bill_date) & (Debt.counter == 0) & (Debt.saldo == saldo)).first()

        if debt:
            pass
            db_session.delete(debt)

            umsatz = get_cache (Umsatz, {"departement": [(eq, 0)],"artnr": [(eq, curr_art)],"datum": [(eq, bill_date)]})
            umsatz.anzahl = umsatz.anzahl - 1
            umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(saldo)
            pass
            pass
            billjournal = Billjournal()
            db_session.add(billjournal)

            billjournal.rechnr = rechnr
            billjournal.bill_datum = bill_date
            billjournal.artnr = curr_art
            billjournal.betriebsnr = curr_dept
            billjournal.anzahl = 1
            billjournal.betrag =  to_decimal(saldo)

            if double_currency:
                billjournal.fremdwaehrng =  to_decimal(saldo_foreign)
            billjournal.bezeich = artikel.bezeich
            billjournal.zinr = zinr
            billjournal.zeit = get_current_time_in_seconds()
            billjournal.bediener_nr = bediener.nr
            billjournal.userinit = userinit
            pass

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
            debitor.saldo =  - to_decimal(saldo)
            debitor.transzeit = get_current_time_in_seconds()
            debitor.rgdatum = bill_date
            debitor.bediener_nr = bediener.nr
            debitor.name = billname
            debitor.vesrcod = deptname + voucher_nr

            if double_currency or foreign_rate:
                debitor.vesrdep =  - to_decimal(saldo_foreign)
            pass

        umsatz = get_cache (Umsatz, {"departement": [(eq, 0)],"artnr": [(eq, curr_art)],"datum": [(eq, bill_date)]})

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = curr_art
            umsatz.datum = bill_date
        umsatz.anzahl = umsatz.anzahl + 1
        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(saldo)
        pass
        pass
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = rechnr
        billjournal.bill_datum = bill_date
        billjournal.artnr = curr_art
        billjournal.betriebsnr = curr_dept
        billjournal.anzahl = 1
        billjournal.betrag =  to_decimal(saldo)

        if double_currency:
            billjournal.fremdwaehrng =  to_decimal(saldo_foreign)
        billjournal.bezeich = artikel.bezeich
        billjournal.zinr = zinr
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.bediener_nr = bediener.nr
        billjournal.userinit = userinit
        pass


    inv_ar()

    return generate_output()