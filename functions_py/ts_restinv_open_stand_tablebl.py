#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 01/12/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Tisch, H_bill

def ts_restinv_open_stand_tablebl(curr_dept:int, curr_waiter:int):

    prepare_cache ([Tisch, H_bill])

    tischno = 0
    openbill_found = False
    fl_code = 0
    tisch = h_bill = None

    tbuff = tbuff1 = hbuff = None

    Tbuff = create_buffer("Tbuff",Tisch)
    Tbuff1 = create_buffer("Tbuff1",Tisch)
    Hbuff = create_buffer("Hbuff",H_bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tischno, openbill_found, fl_code, tisch, h_bill
        nonlocal curr_dept, curr_waiter
        nonlocal tbuff, tbuff1, hbuff


        nonlocal tbuff, tbuff1, hbuff

        return {"tischno": tischno, "openbill_found": openbill_found, "fl_code": fl_code}


    tbuff = db_session.query(Tbuff).filter(
             (Tbuff.departement == curr_dept) & (Tbuff.roomcharge)).first()

    if not tbuff:
        fl_code = 1

        return generate_output()

    tbuff = db_session.query(Tbuff).filter(
             (Tbuff.departement == curr_dept) & (Tbuff.roomcharge) & (Tbuff.kellner_nr == curr_waiter)).first()

    if tbuff:
        tischno = tbuff.tischnr

        hbuff = get_cache (H_bill, {"departement": [(eq, curr_dept)],"tischnr": [(eq, tbuff.tischnr)],"flag": [(eq, 0)]})

        if hbuff and hbuff.saldo != 0:
            openbill_found = True
    else:

        for tbuff in db_session.query(Tbuff).filter(
                 (Tbuff.departement == curr_dept) & (Tbuff.roomcharge) & (Tbuff.kellner_nr == 0)).order_by(Tbuff.tischnr).yield_per(100):

            hbuff = get_cache (H_bill, {"departement": [(eq, curr_dept)],"tischnr": [(eq, tbuff.tischnr)],"flag": [(eq, 0)]})

            if not hbuff:
                tischno = tbuff.tischnr

                # tbuff1 = get_cache (Tisch, {"_recid": [(eq, tbuff._recid)]})
                tbuff1 = db_session.query(Tbuff1).filter(
                         (Tbuff1._recid == tbuff._recid)).with_for_update().first()
                tbuff1.kellner_nr = curr_waiter


                pass
                break

    if tischno == 0:
        fl_code = 2

        return generate_output()

    return generate_output()