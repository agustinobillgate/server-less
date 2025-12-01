#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Kellner, Guest, Hoteldpt, Htparam, Waehrung, H_artikel, H_bill, H_bill_line, H_umsatz, H_journal, Umsatz, Artikel, Debitor, Bediener, Billjournal

def ts_splitbill_update_billbl(rec_id_h_bill:int, rec_id_h_artikel:int, h_artart:int, h_artnrfront:int, dept:int, amount:Decimal, transdate:date, billart:int, description:string, change_str:string, qty:int, tischnr:int, price:Decimal, add_zeit:int, curr_select:int, hoga_card:string, cancel_str:string, curr_waiter:int, amount_foreign:Decimal, curr_room:string, user_init:string, cc_comment:string, guestnr:int):

    prepare_cache ([Guest, Hoteldpt, Htparam, Waehrung, H_artikel, H_bill, H_bill_line, H_umsatz, H_journal, Umsatz, Artikel, Bediener, Billjournal])

    bill_date = None
    deptname:string = ""
    foreign_rate:bool = False
    exchg_rate:Decimal = 1
    kellner = guest = hoteldpt = htparam = waehrung = h_artikel = h_bill = h_bill_line = h_umsatz = h_journal = umsatz = artikel = debitor = bediener = billjournal = None

    kellner1 = bill_guest = None

    Kellner1 = create_buffer("Kellner1",Kellner)
    Bill_guest = create_buffer("Bill_guest",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, deptname, foreign_rate, exchg_rate, kellner, guest, hoteldpt, htparam, waehrung, h_artikel, h_bill, h_bill_line, h_umsatz, h_journal, umsatz, artikel, debitor, bediener, billjournal
        nonlocal rec_id_h_bill, rec_id_h_artikel, h_artart, h_artnrfront, dept, amount, transdate, billart, description, change_str, qty, tischnr, price, add_zeit, curr_select, hoga_card, cancel_str, curr_waiter, amount_foreign, curr_room, user_init, cc_comment, guestnr
        nonlocal kellner1, bill_guest


        nonlocal kellner1, bill_guest

        return {"bill_date": bill_date}

    def update_bill():

        nonlocal bill_date, deptname, foreign_rate, exchg_rate, kellner, guest, hoteldpt, htparam, waehrung, h_artikel, h_bill, h_bill_line, h_umsatz, h_journal, umsatz, artikel, debitor, bediener, billjournal
        nonlocal rec_id_h_bill, rec_id_h_artikel, h_artart, h_artnrfront, dept, amount, transdate, billart, description, change_str, qty, tischnr, price, add_zeit, curr_select, hoga_card, cancel_str, curr_waiter, amount_foreign, curr_room, user_init, cc_comment, guestnr
        nonlocal kellner1, bill_guest


        nonlocal kellner1, bill_guest

        closed:bool = False

        # h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id_h_bill)]})
        h_bill = db_session.query(H_bill).filter(H_bill._recid == rec_id_h_bill).with_for_update().first()

        if h_bill:
            pass
            h_bill.kellner_nr = curr_waiter

            kellner1 = db_session.query(Kellner1).filter(
                     (Kellner1.kellner_nr == h_bill.kellner_nr) & (Kellner1.departement == h_bill.departement)).first()
            h_bill.saldo =  to_decimal(h_bill.saldo) + to_decimal(amount)

            if h_bill.saldo != 0:
                h_bill.rgdruck = 0

            htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
            bill_date = htparam.fdate

            if transdate != None:
                bill_date = transdate
            else:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})

                if htparam.flogical and bill_date < get_current_date():
                    bill_date = bill_date + timedelta(days=1)
            h_bill_line = H_bill_line()
            db_session.add(h_bill_line)

            h_bill_line.rechnr = h_bill.rechnr
            h_bill_line.artnr = billart
            h_bill_line.bezeich = description + change_str + cc_comment
            h_bill_line.anzahl = qty
            h_bill_line.nettobetrag =  to_decimal(amount)
            h_bill_line.betrag =  to_decimal(amount)
            h_bill_line.tischnr = tischnr
            h_bill_line.departement = h_bill.departement
            h_bill_line.epreis =  to_decimal(price)
            h_bill_line.zeit = get_current_time_in_seconds() + add_zeit
            h_bill_line.bill_datum = bill_date
            h_bill_line.waehrungsnr = curr_select
            h_bill_line.fremdwbetrag =  to_decimal(amount_foreign)

            if substring(description, 0, 5) == ("RmNo ").lower()  or substring(description, 0, 5) == ("Card ").lower() :
                h_bill_line.segmentcode = to_int(substring(hoga_card, 0, 9))
            pass

            if billart != 0:

                # h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, billart)],"departement": [(eq, h_bill.departement)],"datum": [(eq, bill_date)]})
                h_umsatz = db_session.query(H_umsatz).filter(
                                (H_umsatz.artnr == billart) &
                                (H_umsatz.departement == h_bill.departement) &
                                (H_umsatz.datum == bill_date)
                            ).with_for_update().first()

                if not h_umsatz:
                    h_umsatz = H_umsatz()
                    db_session.add(h_umsatz)

                    h_umsatz.artnr = billart
                    h_umsatz.datum = bill_date
                    h_umsatz.departement = h_bill.departement
                h_umsatz.betrag =  to_decimal(h_umsatz.betrag) + to_decimal(amount)
                h_umsatz.anzahl = h_umsatz.anzahl + qty
                pass
            h_journal = H_journal()
            db_session.add(h_journal)

            h_journal.rechnr = h_bill.rechnr
            h_journal.artnr = billart
            h_journal.anzahl = qty
            h_journal.betrag =  to_decimal(amount)
            h_journal.bezeich = description + change_str + cc_comment
            h_journal.tischnr = tischnr
            h_journal.departement = h_bill.departement
            h_journal.epreis =  to_decimal(price)
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
            pass

            if h_artart == 6:

                # umsatz = get_cache (Umsatz, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, 0)],"datum": [(eq, bill_date)]})
                umsatz = db_session.query(Umsatz).filter(
                                (Umsatz.artnr == h_artikel.artnrfront) &
                                (Umsatz.departement == 0) &
                                (Umsatz.datum == bill_date)
                            ).with_for_update().first()

                if umsatz:
                    pass
                else:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = h_artikel.artnrfront
                    umsatz.datum = bill_date
                    umsatz.departement = 0
                umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(amount)
                umsatz.anzahl = umsatz.anzahl + 1
                pass
            closed = False

            if h_artart == 2 or h_artart == 7:

                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, 0)]})
                amount_foreign =  to_decimal("0")

                if foreign_rate and amount_foreign == 0:
                    amount_foreign =  to_decimal(amount) / to_decimal(exchg_rate)

                htparam = get_cache (Htparam, {"paramnr": [(eq, 867)]})

                bill_guest = get_cache (Guest, {"gastnr": [(eq, htparam.finteger)]})
                inv_ar(artikel.artnr, h_bill.departement, curr_room, bill_guest.gastnr, bill_guest.gastnr, h_bill.rechnr, amount, amount_foreign, bill_date, bill_guest.name, user_init, cc_comment)
            pass

            if curr_select > 0:

                for h_bill_line in db_session.query(H_bill_line).filter(
                         (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.waehrungsnr == curr_select) & 
                         (H_bill_line.departement == dept)).order_by(H_bill_line._recid).with_for_update().all():
                    h_bill_line.paid_flag = 1
                pass
            else:

                for h_bill_line in db_session.query(H_bill_line).filter(
                         (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == dept)).order_by(H_bill_line._recid).with_for_update().all():
                    h_bill_line.paid_flag = 1
                pass


    def inv_ar(curr_art:int, curr_dept:int, zinr:string, gastnr:int, gastnrmember:int, rechnr:int, saldo:Decimal, saldo_foreign:Decimal, bill_date:date, billname:string, userinit:string, voucher_nr:string):

        nonlocal deptname, kellner, guest, hoteldpt, htparam, waehrung, h_artikel, h_bill, h_bill_line, h_umsatz, h_journal, umsatz, artikel, debitor, bediener, billjournal
        nonlocal rec_id_h_bill, rec_id_h_artikel, h_artart, h_artnrfront, dept, amount, transdate, billart, description, change_str, qty, tischnr, price, add_zeit, curr_select, hoga_card, cancel_str, curr_waiter, amount_foreign, curr_room, user_init, cc_comment, guestnr
        nonlocal kellner1, bill_guest


        nonlocal kellner1, bill_guest

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

        # umsatz = get_cache (Umsatz, {"departement": [(eq, 0)],"artnr": [(eq, curr_art)],"datum": [(eq, bill_date)]})
        umsatz = db_session.query(Umsatz).filter(
                 (Umsatz.departement == 0) &
                 (Umsatz.artnr == curr_art) &
                 (Umsatz.datum == bill_date)
            ).with_for_update().first()

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

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept)]})
    deptname = hoteldpt.depart

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    foreign_rate = htparam.flogical

    if foreign_rate:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    h_artikel = get_cache (H_artikel, {"_recid": [(eq, rec_id_h_artikel)]})
    update_bill()

    return generate_output()