from functions.additional_functions import *
import decimal
from datetime import date
from models import Kellner, Htparam, H_bill, Umsatz, H_bill_line, H_journal

def ts_restinv_waiter_transferbl(pvilanguage:int, table_list:[Table_list], transdate:date, curr_waiter:int, curr_dept:int, usr_nr:int):
    bill_date = None
    t_kellner1_list = []
    lvcarea:str = "TS_restinv"
    kellner = htparam = h_bill = umsatz = h_bill_line = h_journal = None

    t_kellner1 = table_list = hbill = hbill1 = kellner1 = kellner2 = umsatz2 = None

    t_kellner1_list, T_kellner1 = create_model_like(Kellner)
    table_list_list, Table_list = create_model("Table_list", {"rechnr":int, "tischnr":int, "saldo":decimal, "belong":str}, {"belong": "L"})

    Hbill = H_bill
    Hbill1 = H_bill
    Kellner1 = Kellner
    Kellner2 = Kellner
    Umsatz2 = Umsatz

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, t_kellner1_list, lvcarea, kellner, htparam, h_bill, umsatz, h_bill_line, h_journal
        nonlocal hbill, hbill1, kellner1, kellner2, umsatz2


        nonlocal t_kellner1, table_list, hbill, hbill1, kellner1, kellner2, umsatz2
        nonlocal t_kellner1_list, table_list_list
        return {"bill_date": bill_date, "t-kellner1": t_kellner1_list}

    def transfer_now(k1:int, k2:int, bill_date:date):

        nonlocal t_kellner1_list, lvcarea, kellner, htparam, h_bill, umsatz, h_bill_line, h_journal
        nonlocal hbill, hbill1, kellner1, kellner2, umsatz2


        nonlocal t_kellner1, table_list, hbill, hbill1, kellner1, kellner2, umsatz2
        nonlocal t_kellner1_list, table_list_list


        Hbill = H_bill
        Hbill1 = H_bill
        Kellner1 = Kellner
        Kellner2 = Kellner
        Umsatz2 = Umsatz

        kellner1 = db_session.query(Kellner1).filter(
                    (Kellner1.kellner_nr == k1) &  (Kellner1.departement == curr_dept)).first()

        kellner2 = db_session.query(Kellner2).filter(
                    (Kellner2.kellner_nr == k2) &  (Kellner2.departement == curr_dept)).first()

        for table_list in query(table_list_list, filters=(lambda table_list :table_list.belong.lower()  == "R")):

            hbill = db_session.query(Hbill).filter(
                        (Hbill.rechnr == table_list.rechnr) &  (Hbill.departement == curr_dept)).first()

            hbill1 = db_session.query(Hbill1).filter(
                        (Hbill1._recid == hbill._recid)).first()
            hbill1.kellner_nr = k2

            hbill1 = db_session.query(Hbill1).first()

            h_bill_line = db_session.query(H_bill_line).filter(
                        (H_bill_line.rechnr == hbill.rechnr) &  (H_bill_line.departement == curr_dept)).first()

            if h_bill_line:
                h_journal = H_journal()
                db_session.add(h_journal)

                h_journal.rechnr = hbill.rechnr
                h_journal.departement = hbill.departement
                h_journal.bill_datum = h_bill_line.bill_datum
                h_journal.tischnr = hbill.tischnr
                h_journal.zeit = get_current_time_in_seconds()
                h_journal.kellner_nr = k1


                h_journal.bezeich = translateExtended ("Waiter Transfer To", lvcarea, "") + " " + to_string(k2)
            table_list_list.remove(table_list)


        if kellner1:
            t_kellner1 = T_kellner1()
            t_kellner1_list.append(t_kellner1)

            buffer_copy(kellner1, t_kellner1)


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

    if transdate != None:
        bill_date = transdate
    else:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 253)).first()

        if htparam.flogical and bill_date < get_current_date():
            bill_date = bill_date + 1
    transfer_now(curr_waiter, usr_nr, bill_date)

    return generate_output()