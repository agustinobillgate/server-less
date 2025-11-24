#using conversion tools version: 1.0.0.117
#---------------------------------------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#---------------------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_rart, Nightaudit, Bk_veran, Guest, Counters, Bill, Bk_reser, Artikel, Bill_line, Umsatz, Billjournal

def select_artikel_check_unpostedbl(veran_nr:int, veran_seite:int, sub_group:int, ba_dept:int, exchg_rate:Decimal, curr_date:date, bill_date:date, double_currency:bool, user_init:string):

    prepare_cache ([Bk_rart, Bk_veran, Guest, Counters, Bill, Bk_reser, Artikel, Bill_line, Umsatz, Billjournal])

    done = True
    price = to_decimal("0.0")
    amount = to_decimal("0.0")
    amount_foreign = to_decimal("0.0")
    void_flag:bool = False
    answer:bool = True
    bk_rart = nightaudit = bk_veran = guest = counters = bill = bk_reser = artikel = bill_line = umsatz = billjournal = None

    a_list = rbuff = None

    a_list_data, A_list = create_model("A_list", {"artnr":int, "anzahl":int, "preis":Decimal})

    Rbuff = create_buffer("Rbuff",Bk_rart)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal done, price, amount, amount_foreign, void_flag, answer, bk_rart, nightaudit, bk_veran, guest, counters, bill, bk_reser, artikel, bill_line, umsatz, billjournal
        nonlocal veran_nr, veran_seite, sub_group, ba_dept, exchg_rate, curr_date, bill_date, double_currency, user_init
        nonlocal rbuff


        nonlocal a_list, rbuff
        nonlocal a_list_data

        return {"done": done, "price": price, "amount": amount, "amount_foreign": amount_foreign}

    def create_bill_line(artikel_no:int, qty:int, deposit_flag:bool):

        nonlocal done, price, amount, amount_foreign, void_flag, answer, bk_rart, nightaudit, bk_veran, guest, counters, bill, bk_reser, artikel, bill_line, umsatz, billjournal
        nonlocal veran_nr, veran_seite, sub_group, ba_dept, exchg_rate, curr_date, bill_date, double_currency, user_init
        nonlocal rbuff


        nonlocal a_list, rbuff
        nonlocal a_list_data

        bezeich:string = ""

        artikel = get_cache (Artikel, {"departement": [(eq, ba_dept)],"artnr": [(eq, artikel_no)]})
        bezeich = bk_reser.raum + "> " + artikel.bezeich

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
        bill.datum = bill_date
        bill.saldo =  to_decimal(bill.saldo) + to_decimal(amount)

        if double_currency:
            bill.mwst[98] = bill.mwst[98] + amount_foreign
        bill_line = Bill_line()
        db_session.add(bill_line)

        bill_line.rechnr = bill.rechnr
        bill_line.artnr = artikel.artnr
        bill_line.anzahl = qty
        bill_line.epreis =  to_decimal(price)
        bill_line.betrag =  to_decimal(amount)
        bill_line.fremdwbetrag =  to_decimal(amount_foreign)
        bill_line.bezeich = bezeich
        bill_line.departement = artikel.departement
        bill_line.zeit = get_current_time_in_seconds()
        bill_line.userinit = user_init
        bill_line.bill_datum = bill_date


        pass

        umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel.artnr)],"departement": [(eq, artikel.departement)],"datum": [(eq, bill_date)]})

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artikel.artnr
            umsatz.datum = bill_date
            umsatz.departement = artikel.departement


        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(amount)
        umsatz.anzahl = umsatz.anzahl + qty
        pass
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = bill.rechnr
        billjournal.artnr = artikel.artnr
        billjournal.anzahl = qty
        billjournal.fremdwaehrng =  to_decimal(amount_foreign)
        billjournal.betrag =  to_decimal(amount)
        billjournal.bezeich = bezeich
        billjournal.departement = artikel.departement
        billjournal.epreis =  to_decimal(price)
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date


        pass


    a_list = query(a_list_data, first=True)
    void_flag = None != a_list

    bk_rart = get_cache (Bk_rart, {"veran_nr": [(eq, veran_nr)],"veran_seite": [(eq, veran_seite)],"zwkum": [(eq, sub_group)],"preis": [(ne, 0)],"fakturiert": [(eq, 0)]})

    if not bk_rart and not void_flag:

        return generate_output()

    nightaudit = get_cache (Nightaudit, {"programm": [(eq, "nt-bapostbill.p")]})

    if not nightaudit:

        return generate_output()

    if bk_rart:

        if not answer:
            done = False

            return generate_output()

    bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, veran_nr)]})

    if bk_veran.rechnr == 0:

        guest = get_cache (Guest, {"gastnr": [(eq, bk_veran.gastnrver)]})

        # Rd, 24/11/2025, Update last counter dengan next_counter_for_update
        # counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
        counters = db_session.query(Counters).with_for_update().filter(
                 (Counters.counter_no == 3)).first()
        counters.counter = counters.counter + 1
        pass
        bill = Bill()
        db_session.add(bill)

        bill.gastnr = guest.gastnr
        bill.billtyp = ba_dept
        bill.name = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                " " + guest.vorname1
        bill.reslinnr = 1
        bill.rgdruck = 1
        bill.rechnr = counters.counter


        pass
        bk_veran.rechnr = bill.rechnr
        pass
    else:

        bill = get_cache (Bill, {"rechnr": [(eq, bk_veran.rechnr)]})

    bk_rart_obj_list = {}
    bk_rart = Bk_rart()
    bk_reser = Bk_reser()
    for bk_rart.preis, bk_rart.anzahl, bk_rart._recid, bk_rart.fakturiert, bk_reser.raum, bk_reser._recid in db_session.query(Bk_rart.preis, Bk_rart.anzahl, Bk_rart._recid, Bk_rart.fakturiert, Bk_reser.raum, Bk_reser._recid).join(Bk_reser,(Bk_reser.veran_nr == veran_nr) & (Bk_reser.veran_resnr == Bk_rart.veran_resnr) & (Bk_reser.resstatus <= 3) & (Bk_reser.datum == curr_date)).filter(
             (Bk_rart.veran_nr == veran_nr) & (Bk_rart.veran_seite == veran_seite) & (Bk_rart.zwkum == sub_group) & (Bk_rart.preis != 0) & (Bk_rart.fakturiert == 0)).order_by(Bk_rart.veran_artnr).all():
        if bk_rart_obj_list.get(bk_rart._recid):
            continue
        else:
            bk_rart_obj_list[bk_rart._recid] = True


        price =  to_decimal(bk_rart.preis)
        amount =  to_decimal(bk_rart.preis) * to_decimal(bk_rart.anzahl)
        amount_foreign =  to_decimal(amount) / to_decimal(exchg_rate)
        create_bill_line(bk_rart.veran_artnr, bk_rart.anzahl, False)

        rbuff = get_cache (Bk_rart, {"_recid": [(eq, bk_rart._recid)]})
        rbuff.fakturiert = 1
        pass

    for a_list in query(a_list_data, filters=(lambda a_list: a_list.anzahl != 0)):
        price =  to_decimal(a_list.preis)
        amount =  to_decimal(a_list.preis) * to_decimal(a_list.anzahl)
        amount_foreign =  to_decimal(amount) / to_decimal(exchg_rate)
        create_bill_line(a_list.artnr, a_list.anzahl, False)
    pass

    return generate_output()