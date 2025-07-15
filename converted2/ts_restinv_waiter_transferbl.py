#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Kellner, Htparam, H_bill, Umsatz, H_bill_line, H_journal

table_list_data, Table_list = create_model("Table_list", {"rechnr":int, "tischnr":int, "saldo":Decimal, "belong":string}, {"belong": "L"})

def ts_restinv_waiter_transferbl(pvilanguage:int, table_list_data:[Table_list], transdate:date, curr_waiter:int, curr_dept:int, usr_nr:int):

    prepare_cache ([Htparam, H_bill, H_bill_line, H_journal])

    bill_date = None
    t_kellner1_data = []
    lvcarea:string = "TS-restinv"
    kellner = htparam = h_bill = umsatz = h_bill_line = h_journal = None

    t_kellner1 = table_list = None

    t_kellner1_data, T_kellner1 = create_model_like(Kellner)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, t_kellner1_data, lvcarea, kellner, htparam, h_bill, umsatz, h_bill_line, h_journal
        nonlocal pvilanguage, transdate, curr_waiter, curr_dept, usr_nr


        nonlocal t_kellner1, table_list
        nonlocal t_kellner1_data

        return {"bill_date": bill_date, "t-kellner1": t_kellner1_data}

    def transfer_now(k1:int, k2:int, bill_date:date):

        nonlocal t_kellner1_data, lvcarea, kellner, htparam, h_bill, umsatz, h_bill_line, h_journal
        nonlocal pvilanguage, transdate, curr_waiter, curr_dept, usr_nr


        nonlocal t_kellner1, table_list
        nonlocal t_kellner1_data

        hbill = None
        hbill1 = None
        kellner1 = None
        kellner2 = None
        umsatz2 = None
        Hbill =  create_buffer("Hbill",H_bill)
        Hbill1 =  create_buffer("Hbill1",H_bill)
        Kellner1 =  create_buffer("Kellner1",Kellner)
        Kellner2 =  create_buffer("Kellner2",Kellner)
        Umsatz2 =  create_buffer("Umsatz2",Umsatz)

        kellner1 = db_session.query(Kellner1).filter(
                     (Kellner1.kellner_nr == k1) & (Kellner1.departement == curr_dept)).first()

        kellner2 = db_session.query(Kellner2).filter(
                     (Kellner2.kellner_nr == k2) & (Kellner2.departement == curr_dept)).first()

        for table_list in query(table_list_data, filters=(lambda table_list: table_list.belong.lower()  == ("R").lower())):

            hbill = get_cache (H_bill, {"rechnr": [(eq, table_list.rechnr)],"departement": [(eq, curr_dept)]})

            if hbill:

                hbill1 = get_cache (H_bill, {"_recid": [(eq, hbill._recid)]})
                hbill1.kellner_nr = k2


                pass

                h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, hbill.rechnr)],"departement": [(eq, curr_dept)]})

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
                table_list_data.remove(table_list)

        if kellner1:
            t_kellner1 = T_kellner1()
            t_kellner1_data.append(t_kellner1)

            buffer_copy(kellner1, t_kellner1)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    if transdate != None:
        bill_date = transdate
    else:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})

        if htparam.flogical and bill_date < get_current_date():
            bill_date = bill_date + timedelta(days=1)
    transfer_now(curr_waiter, usr_nr, bill_date)

    return generate_output()