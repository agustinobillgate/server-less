from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Bk_rart, Nightaudit, Bk_veran, Guest, Counters, Bill, Bk_reser, Artikel, Bill_line, Umsatz, Billjournal

def select_artikel_check_unpostedbl(veran_nr:int, veran_seite:int, sub_group:int, ba_dept:int, exchg_rate:decimal, curr_date:date, bill_date:date, double_currency:bool, user_init:str):
    done = False
    price = 0
    amount = 0
    amount_foreign = 0
    void_flag:bool = False
    answer:bool = True
    bk_rart = nightaudit = bk_veran = guest = counters = bill = bk_reser = artikel = bill_line = umsatz = billjournal = None

    a_list = rbuff = None

    a_list_list, A_list = create_model("A_list", {"artnr":int, "anzahl":int, "preis":decimal})

    Rbuff = Bk_rart

    db_session = local_storage.db_session

    def generate_output():
        nonlocal done, price, amount, amount_foreign, void_flag, answer, bk_rart, nightaudit, bk_veran, guest, counters, bill, bk_reser, artikel, bill_line, umsatz, billjournal
        nonlocal rbuff


        nonlocal a_list, rbuff
        nonlocal a_list_list
        return {"done": done, "price": price, "amount": amount, "amount_foreign": amount_foreign}

    def create_bill_line(artikel_no:int, qty:int, deposit_flag:bool):

        nonlocal done, price, amount, amount_foreign, void_flag, answer, bk_rart, nightaudit, bk_veran, guest, counters, bill, bk_reser, artikel, bill_line, umsatz, billjournal
        nonlocal rbuff


        nonlocal a_list, rbuff
        nonlocal a_list_list

        bezeich:str = ""

        artikel = db_session.query(Artikel).filter(
                (Artikel.departement == ba_dept) &  (Artikel.artnr == artikel_no)).first()
        bezeich = bk_reser.raum + "> " + artikel.bezeich

        if artikel.umsatzart == 1:
            bill.logisumsatz = bill.logisumsatz + amount

        elif artikel.umsatzart == 2:
            bill.argtumsatz = bill.argtumsatz + amount

        elif artikel.umsatzart == 3:
            bill.f_b_umsatz = bill.f_b_umsatz + amount

        elif artikel.umsatzart == 4:
            bill.sonst_umsatz = bill.sonst_umsatz + amount

        if artikel.umsatzart >= 1 and artikel.umsatzart <= 4:
            bill.gesamtumsatz = bill.gesamtumsatz + amount
        bill.rgdruck = 0
        bill.datum = bill_date
        bill.saldo = bill.saldo + amount

        if double_currency:
            bill.mwst[98] = bill.mwst[98] + amount_foreign
        bill_line = Bill_line()
        db_session.add(bill_line)

        bill_line.rechnr = bill.rechnr
        bill_line.artnr = artikel.artnr
        bill_line.anzahl = qty
        bill_line.epreis = price
        bill_line.betrag = amount
        bill_line.fremdwbetrag = amount_foreign
        bill_line.bezeich = bezeich
        bill_line.departement = artikel.departement
        bill_line.zeit = get_current_time_in_seconds()
        bill_line.userinit = user_init
        bill_line.bill_datum = bill_date

        bill_line = db_session.query(Bill_line).first()

        umsatz = db_session.query(Umsatz).filter(
                (Umsatz.artnr == artikel.artnr) &  (Umsatz.departement == artikel.departement) &  (Umsatz.datum == bill_date)).first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artikel.artnr
            umsatz.datum = bill_date
            umsatz.departement = artikel.departement


        umsatz.betrag = umsatz.betrag + amount
        umsatz.anzahl = umsatz.anzahl + qty

        umsatz = db_session.query(Umsatz).first()
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = bill.rechnr
        billjournal.artnr = artikel.artnr
        billjournal.anzahl = qty
        billjournal.fremdwaehrng = amount_foreign
        billjournal.betrag = amount
        billjournal.bezeich = bezeich
        billjournal.departement = artikel.departement
        billjournal.epreis = price
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date

        billjournal = db_session.query(Billjournal).first()

    a_list = query(a_list_list, first=True)
    void_flag = None != a_list

    bk_rart = db_session.query(Bk_rart).filter(
            (Bk_rart.veran_nr == veran_nr) &  (Bk_rart.veran_seite == veran_seite) &  (Bk_rart.zwkum == sub_group) &  (Bk_rart.preis != 0) &  (Bk_rart.fakturiert == 0)).first()

    if not bk_rart and not void_flag:

        return generate_output()

    nightaudit = db_session.query(Nightaudit).filter(
            (func.lower(Nightaudit.programm) == "nt_bapostbill.p")).first()

    if not nightaudit:

        return generate_output()

    if bk_rart:

        if not answer:
            done = False

            return generate_output()

    bk_veran = db_session.query(Bk_veran).filter(
            (Bk_veran.veran_nr == veran_nr)).first()

    if bk_veran.rechnr == 0:

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == bk_veran.gastnrver)).first()

        counters = db_session.query(Counters).filter(
                (Counters.counter_no == 3)).first()
        counters = counters + 1

        counters = db_session.query(Counters).first()
        bill = Bill()
        db_session.add(bill)

        bill.gastnr = guest.gastnr
        billtyp = ba_dept
        bill.name = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                " " + guest.vorname1
        bill.reslinnr = 1
        bill.rgdruck = 1
        bill.rechnr = counters

        bk_veran = db_session.query(Bk_veran).first()
        bk_veran.rechnr = bill.rechnr

        bk_veran = db_session.query(Bk_veran).first()
    else:

        bill = db_session.query(Bill).filter(
                (Bill.rechnr == bk_veran.rechnr)).first()

    bk_rart_obj_list = []
    for bk_rart, bk_reser in db_session.query(Bk_rart, Bk_reser).join(Bk_reser,(Bk_reser.veran_nr == veran_nr) &  (Bk_reser.veran_resnr == Bk_rart.veran_resnr) &  (Bk_reser.resstatus <= 3) &  (Bk_reser.datum == curr_date)).filter(
            (Bk_rart.veran_nr == veran_nr) &  (Bk_rart.veran_seite == veran_seite) &  (Bk_rart.zwkum == sub_group) &  (Bk_rart.preis != 0) &  (Bk_rart.fakturiert == 0)).all():
        if bk_rart._recid in bk_rart_obj_list:
            continue
        else:
            bk_rart_obj_list.append(bk_rart._recid)


        price = bk_rart.preis
        amount = bk_rart.preis * bk_rart.anzahl
        amount_foreign = amount / exchg_rate
        create_bill_line(bk_rart.veran_artnr, bk_rart.anzahl, False)

        rbuff = db_session.query(Rbuff).filter(
                (Rbuff._recid == bk_rart._recid)).first()
        rbuff.fakturiert = 1

        rbuff = db_session.query(Rbuff).first()

    for a_list in query(a_list_list, filters=(lambda a_list :a_list.anzahl != 0)):
        price = a_list.preis
        amount = a_list.preis * a_list.anzahl
        amount_foreign = amount / exchg_rate
        create_bill_line(a_list.artnr, a_list.anzahl, False)

    bill = db_session.query(Bill).first()

    return generate_output()