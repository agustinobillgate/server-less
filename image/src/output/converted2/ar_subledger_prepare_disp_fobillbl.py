#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bill_line, Blinehis, Artikel

def ar_subledger_prepare_disp_fobillbl(a_rechnr:int):

    prepare_cache ([Artikel])

    t_bill_line_list = []
    t_blinehis_list = []
    bill_line = blinehis = artikel = None

    t_bill_line = t_blinehis = foart = None

    t_bill_line_list, T_bill_line = create_model_like(Bill_line, {"rec_id":int, "run_disp_restbill":bool})
    t_blinehis_list, T_blinehis = create_model_like(Blinehis, {"rec_id":int, "run_disp_restbill":bool})

    Foart = create_buffer("Foart",Artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bill_line_list, t_blinehis_list, bill_line, blinehis, artikel
        nonlocal a_rechnr
        nonlocal foart


        nonlocal t_bill_line, t_blinehis, foart
        nonlocal t_bill_line_list, t_blinehis_list

        return {"t-bill-line": t_bill_line_list, "t-blinehis": t_blinehis_list}


    bill_line = get_cache (Bill_line, {"rechnr": [(eq, a_rechnr)]})

    if bill_line:

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.rechnr == a_rechnr)).order_by(Bill_line._recid).all():

            foart = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)],"departement": [(eq, 0)]})
            t_bill_line = T_bill_line()
            t_bill_line_list.append(t_bill_line)

            buffer_copy(bill_line, t_bill_line)
            t_bill_line.rec_id = (bill_line._recid)

            if foart and foart.artart == 1:
                t_bill_line.run_disp_restbill = True

    else:

        for blinehis in db_session.query(Blinehis).filter(
                 (Blinehis.rechnr == a_rechnr)).order_by(Blinehis._recid).all():

            foart = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)],"departement": [(eq, 0)]})
            t_blinehis = T_blinehis()
            t_blinehis_list.append(t_blinehis)

            buffer_copy(blinehis, t_blinehis)
            t_blinehis.rec_id = (blinehis._recid)

            if foart and foart.artart == 1:
                t_blinehis.run_disp_restbill = True


    return generate_output()