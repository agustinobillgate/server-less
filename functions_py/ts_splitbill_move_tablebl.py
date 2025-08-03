#using conversion tools version: 1.0.0.117
#----------------------------------------
# Rd 3/8/2025
# if not availble -> return
#----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_bill, Htparam, Counters, Hoteldpt, H_bill_line, H_journal, Queasy

temp_data, Temp = create_model("Temp", {"pos":int, "bezeich":string, "artnr":int})
rhbline_data, Rhbline = create_model("Rhbline", {"nr":int, "rid":int})

def ts_splitbill_move_tablebl(temp_data:[Temp], rhbline_data:[Rhbline], tableno:int, bilrecid:int, new_waiter:int, rec_id:int, curr_waiter:int, dept:int, tischnr:int):

    prepare_cache ([H_bill, Htparam, Counters, Hoteldpt, H_bill_line, H_journal, Queasy])

    h_bill = htparam = counters = hoteldpt = h_bill_line = h_journal = queasy = None

    temp = rhbline = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bill, htparam, counters, hoteldpt, h_bill_line, h_journal, queasy
        nonlocal tableno, bilrecid, new_waiter, rec_id, curr_waiter, dept, tischnr


        nonlocal temp, rhbline

        return {}

    def move_table():

        nonlocal h_bill, htparam, counters, hoteldpt, h_bill_line, h_journal, queasy
        nonlocal tableno, bilrecid, new_waiter, rec_id, curr_waiter, dept, tischnr


        nonlocal temp, rhbline

        i:int = 0
        billdate:date = None
        f_discart:int = -1
        b_discart:int = -1
        b2_discart:int = -1
        o_discart:int = -1
        move_amt:Decimal = to_decimal("0.0")
        hbill = None
        Hbill =  create_buffer("Hbill",H_bill)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})

        if htparam.finteger != 0:
            f_discart = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 596)]})

        if htparam.finteger != 0:
            b_discart = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1009)]})

        if htparam.finteger != 0:
            b2_discart = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 556)]})

        if htparam.finteger != 0:
            o_discart = htparam.finteger

        if new_waiter == 0:
            new_waiter = curr_waiter

        if bilrecid != 0:

            hbill = get_cache (H_bill, {"_recid": [(eq, bilrecid)]})
            # Rd 3/8/2025
            # if not avail return
            if h_bill is None:
                return
        else:

            counters = get_cache (Counters, {"counter_no": [(eq, (100 + dept))]})

            if counters:
                pass
            else:

                hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept)]})
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 100 + dept
                counters.counter_bez = "Outlet Invoice: " + hoteldpt.depart
            counters.counter = counters.counter + 1
            pass
            hbill = H_bill()
            db_session.add(hbill)

            hbill.tischnr = tableno
            hbill.departement = dept
            hbill.kellner_nr = curr_waiter
            hbill.rechnr = counters.counter
            hbill.belegung = 1


            pass
        pass
        h_bill.rgdruck = 0

        for temp in query(temp_data):

            rhbline = query(rhbline_data, filters=(lambda rhbline: rhbline.Rhbline.nr == temp.pos), first=True)

            h_bill_line = get_cache (H_bill_line, {"_recid": [(eq, rhbline.rid)]})
            move_amt =  to_decimal(move_amt) + to_decimal(h_bill_line.betrag)
            billdate = h_bill_line.bill_datum

            if h_bill_line.artnr == f_discart:

                for h_journal in db_session.query(H_journal).filter(
                         (H_journal.bill_datum == h_bill_line.bill_datum) & (H_journal.departement == h_bill_line.departement) & (H_journal.rechnr == h_bill_line.rechnr) & ((H_journal.artnr == f_discart) | (H_journal.artnr == b_discart) | (H_journal.artnr == b2_discart) | (H_journal.artnr == o_discart)) & (H_journal.zeit == h_bill_line.zeit)).order_by(H_journal._recid).all():
                    h_journal.tischnr = tableno
                    h_journal.rechnr = hbill.rechnr

            else:

                h_journal = get_cache (H_journal, {"bill_datum": [(eq, h_bill_line.bill_datum)],"departement": [(eq, h_bill_line.departement)],"rechnr": [(eq, h_bill_line.rechnr)],"artnr": [(eq, h_bill_line.artnr)],"zeit": [(eq, h_bill_line.zeit)]})

                if h_journal:
                    h_journal.tischnr = tableno
                    h_journal.rechnr = hbill.rechnr


                    pass
            h_bill_line.waehrungsnr = 0
            h_bill_line.tischnr = tableno
            h_bill_line.rechnr = hbill.rechnr


            pass
            h_bill.saldo =  to_decimal(h_bill.saldo) - to_decimal(h_bill_line.betrag)
            hbill.saldo =  to_decimal(hbill.saldo) + to_decimal(h_bill_line.betrag)
        h_journal = H_journal()
        db_session.add(h_journal)

        h_journal.rechnr = h_bill.rechnr
        h_journal.artnr = 0
        h_journal.anzahl = 0
        h_journal.epreis =  to_decimal("0")
        h_journal.bezeich = "To Table " + to_string(tableno) +\
                " *" + to_string(hbill.rechnr)
        h_journal.tischnr = tischnr
        h_journal.departement = h_bill.departement
        h_journal.zeit = get_current_time_in_seconds()
        h_journal.kellner_nr = curr_waiter
        h_journal.bill_datum = billdate
        h_journal.artnrfront = 0
        h_journal.aendertext = ""
        h_journal.betrag =  - to_decimal(move_amt)


        pass
        h_journal = H_journal()
        db_session.add(h_journal)

        h_journal.rechnr = hbill.rechnr
        h_journal.artnr = 0
        h_journal.anzahl = 0
        h_journal.epreis =  to_decimal("0")
        h_journal.bezeich = "From Table " + to_string(tischnr) +\
                " *" + to_string(h_bill.rechnr)
        h_journal.tischnr = tableno
        h_journal.departement = h_bill.departement
        h_journal.zeit = get_current_time_in_seconds()
        h_journal.kellner_nr = new_waiter
        h_journal.bill_datum = billdate
        h_journal.artnrfront = 0
        h_journal.aendertext = ""
        h_journal.betrag =  to_decimal(move_amt)


        pass

        queasy = get_cache (Queasy, {"key": [(eq, 31)],"number1": [(eq, dept)],"number2": [(eq, tableno)]})

        if queasy and queasy.date1 == None:
            pass

            if queasy.date1 == None:
                queasy.number3 = get_current_time_in_seconds()
                queasy.date1 = get_current_date()


            pass
            pass
        pass
        pass
        pass
        pass
        temp_data.clear()
        rhbline_data.clear()

    h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id)]})
    # Rd 3/8/2025
    # if  availble 
    if h_bill:
        move_table()

    return generate_output()