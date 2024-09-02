from functions.additional_functions import *
import decimal
from models import H_bill

def ts_restinv_run_help_check_billbl(case_type:int, tischnr:int, curr_dept:int):
    pvilanguage:int = 0
    lvcarea:str = "ts_restinv"
    t_h_bill_list = []
    h_bill = None

    t_h_bill = None

    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal pvilanguage, lvcarea, t_h_bill_list, h_bill


        nonlocal t_h_bill
        nonlocal t_h_bill_list
        return {"t-h-bill": t_h_bill_list}

    if case_type == 1:

        h_bill = db_session.query(H_bill).filter(
                (H_bill.tischnr == tischnr) &  (H_bill.departement == curr_dept) &  (H_bill.flag == 0)).first()

    elif case_type == 2:

        h_bill = db_session.query(H_bill).filter(
                (H_bill.tischnr == tischnr) &  (H_bill.departement == curr_dept)).first()

    elif case_type == 3:

        h_bill = db_session.query(H_bill).filter(
                (H_bill.tischnr == tischnr) &  (H_bill.departement == curr_dept) &  (H_bill.flag == 0)).first()

        if h_bill:
            t_h_bill._list.clear()
            t_h_bill = T_h_bill()
            t_h_bill_list.append(t_h_bill)

            t_h_bill.bilname = translateExtended ("Table already has an active bill", lvcarea, "")

            return generate_output()
        else:

            return generate_output()

    elif case_type == 4:

        h_bill = db_session.query(H_bill).filter(
                (H_bill.tischnr == tischnr) &  (H_bill.departement == curr_dept) &  (H_bill.flag == 0)).first()

        if not h_bill:
            t_h_bill._list.clear()
            t_h_bill = T_h_bill()
            t_h_bill_list.append(t_h_bill)

            t_h_bill.bilname = translateExtended ("There is no bill active on this table" + chr(10) +\
                    "Or bill on this table has been closed" + chr(10) +\
                    "Payment not possible", lvcarea, "")

            return generate_output()
        else:

            return generate_output()

    if h_bill:
        t_h_bill = T_h_bill()
        t_h_bill_list.append(t_h_bill)

        buffer_copy(h_bill, t_h_bill)
        t_h_bill.rec_id = h_bill._recid

    return generate_output()