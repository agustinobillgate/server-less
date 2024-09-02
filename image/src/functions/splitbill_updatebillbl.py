from functions.additional_functions import *
import decimal
from datetime import date
from models import Bill, Bill_line, Artikel, Guest, Counters, Res_line, Htparam, Billjournal, Debitor

def splitbill_updatebillbl(pvilanguage:int, j:int, recid_curr:int, recid_j:int, user_init:str, spbill_list:[Spbill_list]):
    msg_str = ""
    lvcarea:str = "split_bill"
    bill = bill_line = artikel = guest = counters = res_line = htparam = billjournal = debitor = None

    spbill_list = billi = billj = art1 = bline = gbuff = None

    spbill_list_list, Spbill_list = create_model("Spbill_list", {"selected":bool, "bl_recid":int}, {"selected": True})

    Billi = Bill
    Billj = Bill
    Art1 = Artikel
    Bline = Bill_line
    Gbuff = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, bill, bill_line, artikel, guest, counters, res_line, htparam, billjournal, debitor
        nonlocal billi, billj, art1, bline, gbuff


        nonlocal spbill_list, billi, billj, art1, bline, gbuff
        nonlocal spbill_list_list
        return {"msg_str": msg_str}

    def check_bill_line():

        nonlocal msg_str, lvcarea, bill, bill_line, artikel, guest, counters, res_line, htparam, billjournal, debitor
        nonlocal billi, billj, art1, bline, gbuff


        nonlocal spbill_list, billi, billj, art1, bline, gbuff
        nonlocal spbill_list_list

        bill = db_session.query(Bill).filter(
                (Bill._recid == recid_curr)).first()

        for spbill_list in query(spbill_list_list, filters=(lambda spbill_list :spbill_list.selected)):

            bill_line = db_session.query(Bill_line).filter(
                    (Bill_line._recid == spbill_list.bl_recid) &  (Bill_line.rechnr == bill.rechnr)).first()

            if not bill_line:
                msg_str = translateExtended ("Bill transfer not possible:", lvcarea, "") + chr(10) + translateExtended ("One of the bill has been changed, please refresh the screen!", lvcarea, "")
                break

    def update_billine():

        nonlocal msg_str, lvcarea, bill, bill_line, artikel, guest, counters, res_line, htparam, billjournal, debitor
        nonlocal billi, billj, art1, bline, gbuff


        nonlocal spbill_list, billi, billj, art1, bline, gbuff
        nonlocal spbill_list_list

        rechnr:int = 0
        datum:date = None
        replace_it:bool = False
        do_it:bool = False
        billine_datum:date = None
        Billi = Bill
        Billj = Bill
        Art1 = Artikel
        Bline = Bill_line
        Gbuff = Guest

        billi = db_session.query(Billi).filter(
                (Billi._recid == recid_curr)).first()
        rechnr = billi.rechnr

        billj = db_session.query(Billj).filter(
                (Billj._recid == recid_j)).first()

        if billj.rechnr == 0:

            counters = db_session.query(Counters).filter(
                    (Counters.counter_no == 3)).first()
            counters.counter = counters.counter + 1
            billj.rechnr = counters.counter

            counters = db_session.query(Counters).first()
            replace_it = True
        else:

            bline = db_session.query(Bline).filter(
                    (Bline.rechnr == billj.rechnr)).first()

            if not bline:
                replace_it = True

        gbuff = db_session.query(Gbuff).filter(
                (Gbuff.gastnr == billj.gastnr)).first()

        for spbill_list in query(spbill_list_list, filters=(lambda spbill_list :spbill_list.selected)):

            bill_line = db_session.query(Bill_line).filter(
                    (Bill_line._recid == spbill_list.bl_recid) &  (Bill_line.rechnr == rechnr)).first()

            if bill_line:

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == bill_line.artnr) &  (Artikel.departement == bill_line.departement)).first()

                if artikel and artikel.artart == 2 and gbuff.zahlungsart == 0:
                    msg_str = translateExtended ("Bill transfer not possible:", lvcarea, "") + chr(10) + translateExtended ("Destination bill does not have C/L account", lvcarea, "")

                    return

        for spbill_list in query(spbill_list_list, filters=(lambda spbill_list :spbill_list.selected)):

            bill_line = db_session.query(Bill_line).filter(
                    (Bill_line._recid == spbill_list.bl_recid) &  (Bill_line.rechnr == rechnr)).first()
            do_it = (None != bill_line)

            if do_it and billj.resnr > 0 and billj.reslinnr > 0 and bill_line.typ > 0 and bill_line.typ != billi.resnr and bill_line.typ != billj.resnr and (billi.gastnr != billj.gastnr):

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == billj.resnr) &  (Res_line.reslinnr == billj.parent_nr)).first()

                if res_line and res_line.ankunft > bill_line.bill_datum:
                    do_it = False
                    billine_datum = bill_line.bill_datum

            if not do_it:
                msg_str = msg_str + chr(2) + translateExtended ("Bill transfer not possible:", lvcarea, "") + chr(10) + translateExtended ("Posting date:", lvcarea, "") + " " + to_string(billine_datum) + " " + translateExtended ("BUT Arrival Date of the transferred guest bill is", lvcarea, "") + " " + to_string(res_line.ankunft) + chr(10)
            else:
                billi.rgdruck = 0
                billj.rgdruck = 0
                bill_line.rechnr = billj.rechnr
                billi.saldo = billi.saldo - bill_line.betrag
                billj.saldo = billj.saldo + bill_line.betrag
                billi.mwst[98] = billi.mwst[98] - bill_line.fremdwbetrag
                billj.mwst[98] = billj.mwst[98] + bill_line.fremdwbetrag

                if bill_line.typ == 0:
                    bill_line.typ = billi.resnr

                if datum == None:
                    datum = bill_line.bill_datum

                elif datum < bill_line.bill_datum:
                    datum = bill_line.bill_datum

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 110)).first()
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = billj.rechnr
                billjournal.artnr = bill_line.artnr
                billjournal.anzahl = 0
                billjournal.betrag = bill_line.betrag
                billjournal.fremdwaehrng = bill_line.fremdwbetrag
                billjournal.zinr = billj.zinr
                billjournal.departement = bill_line.departement
                billjournal.epreis = bill_line.epreis
                billjournal.zeit = get_current_time_in_seconds()
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_line.bill_datum


                billjournal.bezeich = "*" + to_string(billi.rechnr) + "; " + to_string(htparam.fdate) + " " + translateExtended ("RmNo", lvcarea, "") + " " + billi.zinr

                bill_line = db_session.query(Bill_line).first()

                billjournal = db_session.query(Billjournal).first()

                art1 = db_session.query(Art1).filter(
                        (Art1.artnr == bill_line.artnr) &  (Art1.departement == bill_line.departement)).first()

                if art1 and (art1.artart == 2 or art1.artart == 7):

                    debitor = db_session.query(Debitor).filter(
                            (Debitor.artnr == art1.artnr) &  (Debitor.rechnr == billi.rechnr) &  (Debitor.rgdatum == bill_line.bill_datum) &  (Debitor.saldo == - bill_line.betrag) &  (Debitor.counter == 0)).first()

                    if debitor:

                        gbuff = db_session.query(Gbuff).filter(
                                (Gbuff.gastnr == billj.gastnr)).first()

                        debitor = db_session.query(Debitor).first()
                        debitor.rechnr = billj.rechnr
                        debitor.gastnr = billj.gastnr
                        debitor.name = gbuff.name

                        debitor = db_session.query(Debitor).first()
            spbill_list_list.remove(spbill_list)

        if datum != None and replace_it:
            billj.datum = datum

        elif billj.datum < datum and datum != None:
            billj.datum = datum
        datum = None

        for bline in db_session.query(Bline).filter(
                (Bline.rechnr == billi.rechnr)).all():

            if datum == None:
                datum = bline.bill_datum

            elif datum < bline.bill_datum:
                datum = bline.bill_datum

        if datum != billi.datum and datum != None:
            billi.datum = datum

        billi = db_session.query(Billi).first()

        billj = db_session.query(Billj).first()


    check_bill_line()

    if msg_str == "":
        update_billine()

    return generate_output()