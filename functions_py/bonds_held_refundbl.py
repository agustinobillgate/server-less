# using conversion tools version: 1.0.0.119
"""_yusufwijasena_03/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix var decklaration
                    - fix python indentation
                    - changed string to str
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bill_line, Htparam, Bill, Artikel, Umsatz, Billjournal, Bediener, Debitor, Res_line, Guest

def bonds_held_refundbl(rechnr:int, user_init:string):

    prepare_cache ([Bill_line, Htparam, Bill, Artikel, Umsatz, Billjournal, Bediener, Debitor, Res_line, Guest])

    art_security:int = 0
    art_lost:int = 0
    bill_date:date = None
    qty:int = 0
    lostnbreak:Decimal = to_decimal("0.0")
    curr_amount:Decimal = to_decimal("0.0")
    bill_line = htparam = bill = artikel = umsatz = billjournal = bediener = debitor = res_line = guest = None

    tlist = bline = None

    tlist_data, Tlist = create_model(
        "Tlist",
        {
            "artnr": int,
            "dept": int,
            "amount": Decimal,
            "room": string
        })

    Bline = create_buffer("Bline", Bill_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal art_security, art_lost, bill_date, qty, lostnbreak, curr_amount, bill_line, htparam, bill, artikel, umsatz, billjournal, bediener, debitor, res_line, guest
        nonlocal rechnr, user_init
        nonlocal bline


        nonlocal tlist, bline
        nonlocal tlist_data

        return {}

    htparam = db_session.query(Htparam).filter(Htparam.paramnr == 1053).first()
    if htparam:
        art_security = htparam.finteger

    htparam = db_session.query(Htparam).filter(Htparam.paramnr == 110).first()
    if htparam:
        bill_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(Htparam.paramnr == 1043).first()
    if htparam:
        art_lost = htparam.finteger


    tlist_data.clear()

    bill = db_session.query(Bill).filter((Bill.rechnr == rechnr) & (Bill.flag == 0) & (Bill.billnr == 4)).first()

    if bill:

        bill_line_obj_list = {}
        bill_line = Bill_line()
        artikel = Artikel()
        for bill_line.artnr, bill_line.departement, bill_line.zinr, bill_line.betrag, bill_line.rechnr, bill_line.bezeich, bill_line.anzahl, bill_line.fremdwbetrag, bill_line.bill_datum, bill_line.zeit, bill_line.userinit, bill_line._recid, artikel.artnr, artikel.bezeich, artikel.departement, artikel.artart, artikel.umsatzart, artikel._recid in db_session.query(Bill_line.artnr, Bill_line.departement, Bill_line.zinr, Bill_line.betrag, Bill_line.rechnr, Bill_line.bezeich, Bill_line.anzahl, Bill_line.fremdwbetrag, Bill_line.bill_datum, Bill_line.zeit, Bill_line.userinit, Bill_line._recid, Artikel.artnr, Artikel.bezeich, Artikel.departement, Artikel.artart, Artikel.umsatzart, Artikel._recid).join(Artikel, (Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement) & (Artikel.artart != 0)).filter(
                (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line.sysdate, Bill_line.zeit).all():
            if bill_line_obj_list.get(bill_line._recid):
                continue
            else:
                bill_line_obj_list[bill_line._recid] = True

            tlist = query(tlist_data, filters=(lambda tlist: tlist.artnr == bill_line.artnr and tlist.dept == bill_line.departement), first=True)

            if not tlist:
                tlist = Tlist()
                tlist_data.append(tlist)

                tlist.artnr = bill_line.artnr
                tlist.dept = bill_line.departement
                tlist.room = bill_line.zinr

            tlist.amount = to_decimal(tlist.amount + bill_line.betrag)

        bill_line_obj_list = {}
        bill_line = Bill_line()
        artikel = Artikel()
        for bill_line.artnr, bill_line.departement, bill_line.zinr, bill_line.betrag, bill_line.rechnr, bill_line.bezeich, bill_line.anzahl, bill_line.fremdwbetrag, bill_line.bill_datum, bill_line.zeit, bill_line.userinit, bill_line._recid, artikel.artnr, artikel.bezeich, artikel.departement, artikel.artart, artikel.umsatzart, artikel._recid in db_session.query(Bill_line.artnr, Bill_line.departement, Bill_line.zinr, Bill_line.betrag, Bill_line.rechnr, Bill_line.bezeich, Bill_line.anzahl, Bill_line.fremdwbetrag, Bill_line.bill_datum, Bill_line.zeit, Bill_line.userinit, Bill_line._recid, Artikel.artnr, Artikel.bezeich, Artikel.departement, Artikel.artart, Artikel.umsatzart, Artikel._recid).join(Artikel, (Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement) & (Artikel.artart == 0)).filter(
                (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line._recid).all():
            if bill_line_obj_list.get(bill_line._recid):
                continue
            else:
                bill_line_obj_list[bill_line._recid] = True

            lostnbreak = to_decimal(lostnbreak + bill_line.betrag)

        artikel_obj_list = {}
        for artikel in db_session.query(Artikel).filter(
                ((Artikel.artnr.in_(list(set([tlist.artnr for tlist in tlist_data])))) & (Artikel.departement == tlist.dept))).order_by(tlist.artnr).all():
            if artikel_obj_list.get(artikel._recid):
                continue
            else:
                artikel_obj_list[artikel._recid] = True

            tlist = query(tlist_data, (lambda tlist: (
                artikel.artnr == tlist.artnr)), first=True)

            if tlist.amount == 0:
                tlist_data.remove(tlist)
            else:
                curr_amount = to_decimal(tlist.amount)
                qty = -1

                if lostnbreak != 0:

                    if curr_amount < 0:
                        curr_amount = to_decimal(curr_amount + lostnbreak)

                    elif curr_amount > 0:
                        curr_amount = to_decimal(curr_amount - lostnbreak)

                bill_line = Bill_line()
                db_session.add(bill_line)

                bill_line.rechnr = bill.rechnr
                bill_line.artnr = artikel.artnr
                bill_line.bezeich = artikel.bezeich
                bill_line.anzahl = qty
                bill_line.betrag = to_decimal(curr_amount)
                bill_line.fremdwbetrag = to_decimal(curr_amount)
                bill_line.zinr = tlist.room
                bill_line.departement = artikel.departement
                bill_line.bill_datum = bill_date
                bill_line.zeit = get_current_time_in_seconds()
                bill_line.userinit = user_init

                umsatz = db_session.query(Umsatz).filter(Umsatz.artnr == artikel.artnr, Umsatz.departement == artikel.departement, Umsatz.datum == bill_date).with_for_update().first()
                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)
                    umsatz.artnr = artikel.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = artikel.departement

                umsatz.betrag = to_decimal(umsatz.betrag + curr_amount)
                umsatz.anzahl = umsatz.anzahl + qty
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel.artnr
                billjournal.anzahl = qty
                billjournal.fremdwaehrng = to_decimal(curr_amount)
                billjournal.betrag = to_decimal(curr_amount)
                billjournal.bezeich = artikel.bezeich
                billjournal.zinr = tlist.room
                billjournal.departement = artikel.departement
                billjournal.zeit = get_current_time_in_seconds()
                billjournal.stornogrund = " "
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date

                if artikel.artart == 2 or artikel.artart == 7:

                    bediener = db_session.query(Bediener).filter((Bediener.userinit == user_init)).first()
                    debitor = Debitor()
                    db_session.add(debitor)

                    debitor.artnr = artikel.artnr
                    debitor.rechnr = bill.rechnr
                    debitor.rgdatum = bill_date
                    debitor.saldo = to_decimal(curr_amount)
                    debitor.vesrdep = to_decimal(curr_amount)
                    debitor.bediener_nr = bediener.nr
                    debitor.vesrdat = get_current_date()
                    debitor.transzeit = get_current_time_in_seconds()

                    res_line = db_session.query(Res_line).filter((Res_line.resnr == bill.resnr) & (Res_line.reslinnr == bill.parent_nr)).first()

                    if res_line:
                        guest = db_session.query(Guest).filter((Guest.gastnr == res_line.gastnr)).first()

                        if guest:
                            debitor.name = guest.name
                            debitor.gastnr = res_line.gastnr
                            debitor.gastnrmember = res_line.gastnrmember

                db_session.refresh(bill, with_for_update=True)
                if artikel.umsatzart == 1:
                    bill.logisumsatz = to_decimal(bill.logisumsatz + curr_amount)
                    bill.argtumsatz = to_decimal(bill.argtumsatz + curr_amount)

                elif artikel.umsatzart == 2:
                    bill.argtumsatz = to_decimal(bill.argtumsatz + curr_amount)

                elif (artikel.umsatzart == 3 or artikel.umsatzart == 5 or artikel.umsatzart == 6):
                    bill.f_b_umsatz = to_decimal(bill.f_b_umsatz + curr_amount)

                elif artikel.umsatzart == 4:
                    bill.sonst_umsatz = to_decimal(bill.sonst_umsatz + curr_amount)

                if artikel.umsatzart >= 1 and artikel.umsatzart <= 4:
                    bill.gesamtumsatz = to_decimal(bill.gesamtumsatz + curr_amount)

                if not artikel.autosaldo:
                    bill.rgdruck = 0

                elif artikel.artart == 6:
                    bill.rgdruck = 0

                bill.saldo =  to_decimal(bill.saldo) + to_decimal(curr_amount)
        pass

    return generate_output()