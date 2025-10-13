#using conversion tools version: 1.0.0.117

"""_yusufwijasena_ 10/10/2025

    TICKET ID: 822CBF
    ISSUE:  - fix define variabel & variabel = None
            - bk_reser."raum" is not a known attribute
            - operator not supported for types "Cast[Unknown] | Decimal | Literal[0] | None" and "Cast[Unknown] | Decimal | Literal[0] | None"
            - cannot assign to attribute for class "Bill"
            - add type:ignore to model, avoid warning cannot assign attribute
"""

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_rart, Htparam, Waehrung, Bk_reser, Bk_veran, Guest, Counters, Bill, Bk_func, Artikel, Bill_line, Umsatz, Billjournal

def nt_bapostbill():

    prepare_cache ([Bk_rart, Htparam, Waehrung, Bk_reser, Bk_veran, Guest, Counters, Bill, Bk_func, Artikel, Bill_line, Umsatz, Billjournal])

    zugriff:bool = False
    veran_nr:int = 0
    invnr:int = 0
    curr_resnr:int = 0
    banquet_dep:int = 0
    bill_date:date
    price = to_decimal("0.0")
    amount = to_decimal("0.0")
    amount_foreign = to_decimal("0.0")
    room_amount = to_decimal("0.0")
    fb_amount = to_decimal("0.0")
    deposit_amount = (to_decimal("0.0") or 0)
    exchg_rate = to_decimal(1)
    double_currency:bool = False
    foreign_rate:bool = False
    charge_flag:bool = False
    i:int = 0
    
    # issue:
    #     "raum" is not a known attribute
    # before:
    #     bk_rart = htparam = waehrung = bk_reser = bk_veran = guest = counters = bill = bk_func = artikel = bill_line = umsatz = billjournal = None
    
    bk_reser = Bk_reser()
    bk_rart = htparam = waehrung = bk_veran = guest = counters = bill = bk_func = artikel = bill_line = umsatz = billjournal = None

    rbuff = None

    Rbuff = create_buffer("Rbuff",Bk_rart)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal zugriff, veran_nr, invnr, curr_resnr, banquet_dep, bill_date, price, amount, amount_foreign, room_amount, fb_amount, deposit_amount, exchg_rate, double_currency, foreign_rate, charge_flag, i, bk_rart, htparam, waehrung, bk_reser, bk_veran, guest, counters, bill, bk_func, artikel, bill_line, umsatz, billjournal
        nonlocal rbuff


        nonlocal rbuff

        return {}

    def create_bill_line(artikel_no:int, qty:int, deposit_flag:bool):

        # issue:
        #     not a known attribute
        # before: 
        #     nonlocal zugriff, veran_nr, invnr, curr_resnr, banquet_dep, bill_date, price, amount, amount_foreign, room_amount, fb_amount, deposit_amount, exchg_rate, double_currency, foreign_rate, charge_flag, i, bk_rart, htparam, waehrung, bk_reser, bk_veran,  guest, counters, bill, bk_func, artikel, bill_line, umsatz, billjournal
        
        
        bk_veran = Bk_veran()
        bill = Bill()
        nonlocal zugriff, veran_nr, invnr, curr_resnr, banquet_dep, bill_date, price, amount, amount_foreign, room_amount, fb_amount, deposit_amount, exchg_rate, double_currency, foreign_rate, charge_flag, i, bk_rart, htparam, waehrung, bk_reser,  guest, counters, bk_func, artikel, bill_line, umsatz, billjournal
        nonlocal rbuff


        nonlocal rbuff

        bezeich:string = ""

        if deposit_flag:

            artikel = get_cache (Artikel, {"departement": [(eq, banquet_dep)],"artnr": [(eq, artikel_no)],"artart": [(eq, 5)]})

            if not artikel:

                artikel = get_cache (Artikel, {"departement": [(eq, 0)],"artnr": [(eq, artikel_no)],"artart": [(eq, 5)]})
        else:

            artikel = get_cache (Artikel, {"departement": [(eq, banquet_dep)],"artnr": [(eq, artikel_no)]})

        if artikel:
            bezeich = bk_reser.raum + "> " + artikel.bezeich

            if deposit_flag:
                bezeich = bezeich + " #" + str(to_string(bk_veran.veran_nr))

            if artikel.umsatzart == 1:
                bill.logisumsatz [(to_decimal(bill.logisumsatz) or 0) + (to_decimal(amount) or 0) ]

            elif artikel.umsatzart == 2:
                bill.argtumsatz [(to_decimal(bill.argtumsatz) or 0) + (to_decimal(amount) or 0)] 

            elif artikel.umsatzart == 3:
                bill.f_b_umsatz [(to_decimal(bill.f_b_umsatz) or 0) + (to_decimal(amount) or 0)]

            elif artikel.umsatzart == 4:
                bill.sonst_umsatz [(to_decimal(bill.sonst_umsatz) or 0) + (to_decimal(amount) or 0)]

            if artikel.umsatzart >= 1 and artikel.umsatzart <= 4:
                bill.gesamtumsatz [(to_decimal(bill.gesamtumsatz) or 0) + (to_decimal(amount) or 0)] 
            bill.rgdruck [0]
            bill.datum [bill_date]
            bill.saldo [(to_decimal(bill.saldo) or 0) + (to_decimal(amount) or 0)]

            if double_currency:
                bill.mwst[98] [bill.mwst[98] + amount_foreign] 
            bill_line = Bill_line()
            

            bill_line.rechnr = bill.rechnr
            bill_line.artnr = artikel.artnr
            bill_line.anzahl [qty]
            bill_line.epreis [to_decimal(price)]
            bill_line.betrag [to_decimal(amount)]
            bill_line.fremdwbetrag [to_decimal(amount_foreign)]
            bill_line.bezeich [str(bezeich)]
            bill_line.departement = artikel.departement
            bill_line.zeit [get_current_time_in_seconds()]
            bill_line.userinit ["$$"]
            bill_line.bill_datum [bill_date]
            
            db_session.add(bill_line)


            pass

            umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel.artnr)],"departement": [(eq, artikel.departement)],"datum": [(eq, bill_date)]})

            if not umsatz:
                umsatz = Umsatz()

                umsatz.artnr = artikel.artnr
                umsatz.datum [bill_date] 
                umsatz.departement = artikel.departement

                db_session.add(umsatz)


            umsatz.betrag [(to_decimal(umsatz.betrag) or 0) + (to_decimal(amount) or 0)] 
            umsatz.anzahl [umsatz.anzahl + qty] 


            pass
            billjournal = Billjournal()

            billjournal.rechnr = bill.rechnr
            billjournal.artnr = artikel.artnr
            billjournal.anzahl [qty] 
            billjournal.fremdwaehrng [to_decimal(amount_foreign)] 
            billjournal.betrag [to_decimal(amount)] 
            billjournal.bezeich [bezeich] 
            billjournal.departement = artikel.departement
            billjournal.epreis [to_decimal(price)] 
            billjournal.zeit [get_current_time_in_seconds()] 
            billjournal.userinit ["$$"] 
            billjournal.bill_datum [bill_date] 

            db_session.add(billjournal)

            pass

    htparam = get_cache (Htparam, {"paramnr": [(eq, 985)]})

    if not htparam.flogical:

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 900)]})
    banquet_dep = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate + timedelta(days=1)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    double_currency = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    foreign_rate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 950)]})
    charge_flag = htparam.flogical

    if foreign_rate or double_currency:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            exchg_rate =  (to_decimal(waehrung.ankauf) or 0) / (to_decimal(waehrung.einheit) or 0)

    for bk_reser in db_session.query(Bk_reser).filter(
                 (Bk_reser.datum == bill_date) & (Bk_reser.von_zeit >= ("00:00").lower()) & (Bk_reser.resstatus == 1) & (Bk_reser.fakturiert == 0)).order_by(Bk_reser.veran_nr).all():

        if curr_resnr != bk_reser.veran_nr:
            curr_resnr = bk_reser.veran_nr

            bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, curr_resnr)]})

            guest = get_cache (Guest, {"gastnr": [(eq, bk_veran.gastnrver)]})
            deposit_amount =  to_decimal("0")
            for i in range(1,9 + 1) :
                deposit_amount =  (to_decimal(deposit_amount) or 0) + (to_decimal(bk_veran.deposit_payment[i - 1]) or 0)

            if bk_veran.rechnr == 0:

                counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
                counters.counter = counters.counter + 1
                pass
                bill = Bill()

                bill.gastnr = guest.gastnr
                bill.billtyp [banquet_dep]
                bill.name = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.vorname1
                bill.reslinnr[1]
                bill.rgdruck [1]
                bill.rechnr = counters.counter
                bill.flag [0]
                
                db_session.add(bill)


                bk_veran.rechnr = bill.rechnr
            else:

                bill = get_cache (Bill, {"rechnr": [(eq, bk_veran.rechnr)]})

            # if deposit_amount != 0 and bk_veran.last_paid_date:
            if [deposit_amount] and bk_veran.last_paid_date:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 117)]})
                price =  to_decimal("0")
                amount = -to_decimal(deposit_amount) # type:ignore
                amount_foreign =  to_decimal(amount) / to_decimal(exchg_rate) # type: ignore
                create_bill_line(htparam.finteger, 1, True)
                bk_veran.last_paid_date = bill_date
            pass

        bk_func = get_cache (Bk_func, {"veran_nr": [(eq, bk_reser.veran_nr)],"veran_seite": [(eq, bk_reser.veran_seite)]})

        if bk_func:
            room_amount =  to_decimal(bk_func.rpreis[0])

            if [room_amount] and charge_flag == "YES" :

                htparam = get_cache (Htparam, {"paramnr": [(eq, 901)]})
                price =  to_decimal(room_amount)
                amount =  to_decimal(room_amount)
                amount_foreign =  to_decimal(amount) / to_decimal(exchg_rate)  # type: ignore
                create_bill_line(htparam.finteger, 1, False)

        for bk_rart in db_session.query(Bk_rart).filter(
                     (Bk_rart.veran_nr == bk_reser.veran_nr) & (Bk_rart.veran_seite == bk_reser.veran_seite)).order_by(Bk_rart.veran_nr).all():

            if bk_rart.preis != 0 and bk_rart.fakturiert == 0:
                price =  to_decimal(bk_rart.preis)
                amount =  to_decimal(bk_rart.preis) * to_decimal(bk_rart.anzahl)  # type: ignore
                amount_foreign =  to_decimal(amount) / to_decimal(exchg_rate)  # type: ignore
                create_bill_line(bk_rart.veran_artnr, bk_rart.anzahl, False)

                rbuff = get_cache (Bk_rart, {"_recid": [(eq, bk_rart._recid)]})
                rbuff.fakturiert = 1
                pass
        pass
        bk_reser.fakturiert = 1

    return generate_output()