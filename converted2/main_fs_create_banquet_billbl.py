#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_veran, Guest, Htparam, Counters, Bill

def main_fs_create_banquet_billbl(resnr:int):

    prepare_cache ([Bk_veran, Guest, Htparam, Counters, Bill])

    bq_rechnr = 0
    bk_veran = guest = htparam = counters = bill = None

    bk_main = gast = b_dept = None

    Bk_main = create_buffer("Bk_main",Bk_veran)
    Gast = create_buffer("Gast",Guest)
    B_dept = create_buffer("B_dept",Htparam)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bq_rechnr, bk_veran, guest, htparam, counters, bill
        nonlocal resnr
        nonlocal bk_main, gast, b_dept


        nonlocal bk_main, gast, b_dept

        return {"bq_rechnr": bq_rechnr}


    bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, resnr)]})

    b_dept = get_cache (Htparam, {"paramnr": [(eq, 900)]})

    bk_main = get_cache (Bk_veran, {"veran_nr": [(eq, bk_veran.veran_nr)]})

    gast = get_cache (Guest, {"gastnr": [(eq, bk_main.gastnrver)]})

    counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
    counters.counter = counters.counter + 1
    pass
    bill = Bill()
    db_session.add(bill)

    bill.gastnr = gast.gastnr
    bill.billtyp = b_dept.finteger
    bill.name = gast.name + ", " + gast.vorname1 + gast.anredefirma +\
            " " + gast.vorname1
    bill.reslinnr = 1
    bill.rgdruck = 1
    bill.rechnr = counters.counter


    bk_main.rechnr = bill.rechnr
    pass
    pass
    bq_rechnr = bill.rechnr

    return generate_output()