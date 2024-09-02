from functions.additional_functions import *
import decimal
from datetime import date
from models import H_bill, Htparam, Counters, Hoteldpt, H_bill_line, H_journal, Queasy

def ts_splitbill_move_tablebl(temp:[Temp], rhbline:[Rhbline], tableno:int, bilrecid:int, new_waiter:int, rec_id:int, curr_waiter:int, dept:int, tischnr:int):
    h_bill = htparam = counters = hoteldpt = h_bill_line = h_journal = queasy = None

    temp = rhbline = hbill = None

    temp_list, Temp = create_model("Temp", {"pos":int, "bezeich":str, "artnr":int})
    rhbline_list, Rhbline = create_model("Rhbline", {"nr":int, "rid":int})

    Hbill = H_bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bill, htparam, counters, hoteldpt, h_bill_line, h_journal, queasy
        nonlocal hbill


        nonlocal temp, rhbline, hbill
        nonlocal temp_list, rhbline_list
        return {}

    def move_table():

        nonlocal h_bill, htparam, counters, hoteldpt, h_bill_line, h_journal, queasy
        nonlocal hbill


        nonlocal temp, rhbline, hbill
        nonlocal temp_list, rhbline_list

        i:int = 0
        billdate:date = None
        f_discart:int = -1
        b_discart:int = -1
        b2_discart:int = -1
        o_discart:int = -1
        move_amt:decimal = 0
        Hbill = H_bill

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 557)).first()

        if htparam.finteger != 0:
            f_discart = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 596)).first()

        if htparam.finteger != 0:
            b_discart = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1009)).first()

        if htparam.finteger != 0:
            b2_discart = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 556)).first()

        if htparam.finteger != 0:
            o_discart = htparam.finteger

        if new_waiter == 0:
            new_waiter = curr_waiter

        if bilrecid != 0:

            hbill = db_session.query(Hbill).filter(
                    (Hbill._recid == bilrecid)).first()
        else:

            counters = db_session.query(Counters).filter(
                    (Counters.counter_no == (100 + dept))).first()

            if counters:

                counters = db_session.query(Counters).first()
            else:

                hoteldpt = db_session.query(Hoteldpt).filter(
                        (Hoteldpt.num == dept)).first()
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 100 + dept
                counters.counter_bez = "Outlet Invoice: " + hoteldpt.depart
            counters = counters + 1

            counters = db_session.query(Counters).first()
            hbill = Hbill()
            db_session.add(hbill)

            hbill.tischnr = tableno
            hbill.departement = dept
            hbill.kellner_nr = curr_waiter
            hbill.rechnr = counters
            hbill.belegung = 1

        h_bill = db_session.query(H_bill).first()
        h_bill.rgdruck = 0

        for temp in query(temp_list):

            rhbline = query(rhbline_list, filters=(lambda rhbline :Rhbline.nr == temp.pos), first=True)

            h_bill_line = db_session.query(H_bill_line).filter(
                    (H_bill_line._recid == Rhbline.rid)).first()
            move_amt = move_amt + h_bill_line.betrag
            billdate = h_bill_line.bill_datum

            if h_bill_line.artnr == f_discart:

                for h_journal in db_session.query(H_journal).filter(
                        (H_journal.bill_datum == h_bill_line.bill_datum) &  (H_journal.departement == h_bill_line.departement) &  (H_journal.rechnr == h_bill_line.rechnr) &  ((H_journal.artnr == f_discart) |  (H_journal.artnr == b_discart) |  (H_journal.artnr == b2_discart) |  (H_journal.artnr == o_discart)) &  (H_journal.zeit == h_bill_line.zeit)).all():
                    h_journal.tischnr = tableno
                    h_journal.rechnr = hbill.rechnr

            else:

                h_journal = db_session.query(H_journal).filter(
                        (H_journal.bill_datum == h_bill_line.bill_datum) &  (H_journal.departement == h_bill_line.departement) &  (H_journal.rechnr == h_bill_line.rechnr) &  (H_journal.artnr == h_bill_line.artnr) &  (H_journal.zeit == h_bill_line.zeit)).first()

                if h_journal:
                    h_journal.tischnr = tableno
                    h_journal.rechnr = hbill.rechnr

                    h_journal = db_session.query(H_journal).first()
            h_bill_line.waehrungsnr = 0
            h_bill_line.tischnr = tableno
            h_bill_line.rechnr = hbill.rechnr

            h_bill_line = db_session.query(H_bill_line).first()
            h_bill.saldo = h_bill.saldo - h_bill_line.betrag
            hbill.saldo = hbill.saldo + h_bill_line.betrag
        h_journal = H_journal()
        db_session.add(h_journal)

        h_journal.rechnr = h_bill.rechnr
        h_journal.artnr = 0
        h_journal.anzahl = 0
        h_journal.epreis = 0
        h_journal.bezeich = "To Table " + to_string(tableno) +\
                " *" + to_string(hbill.rechnr)
        vhp.h_journal.tischnr = tischnr
        h_journal.departement = h_bill.departement
        h_journal.zeit = get_current_time_in_seconds()
        h_journal.kellner_nr = curr_waiter
        h_journal.bill_datum = billdate
        h_journal.artnrfront = 0
        h_journal.aendertext = ""
        h_journal.betrag = - move_amt

        h_journal = db_session.query(H_journal).first()
        h_journal = H_journal()
        db_session.add(h_journal)

        h_journal.rechnr = hbill.rechnr
        h_journal.artnr = 0
        h_journal.anzahl = 0
        h_journal.epreis = 0
        h_journal.bezeich = "From Table " + to_string(tischnr) +\
                " *" + to_string(h_bill.rechnr)
        h_journal.tischnr = tableno
        h_journal.departement = h_bill.departement
        h_journal.zeit = get_current_time_in_seconds()
        h_journal.kellner_nr = new_waiter
        h_journal.bill_datum = billdate
        h_journal.artnrfront = 0
        h_journal.aendertext = ""
        h_journal.betrag = move_amt

        h_journal = db_session.query(H_journal).first()

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 31) &  (Queasy.number1 == dept) &  (Queasy.number2 == tableno)).first()

        if queasy and queasy.date1 == None:

            if queasy.date1 == None:
                queasy.number3 = get_current_time_in_seconds()
                queasy.date1 = get_current_date()

            queasy = db_session.query(Queasy).first()

        hbill = db_session.query(Hbill).first()

        h_bill = db_session.query(H_bill).first()
        temp_list.clear()
        Rhbline_list.clear()


    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_id)).first()
    move_table()

    return generate_output()