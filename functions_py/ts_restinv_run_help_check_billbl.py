#using conversion tools version: 1.0.0.117

#------------------------------------------
# Rulita, 15/08/2025
# Added bill_saldo recalculate saldo 
# ticket: 4B5043
# Rd, 01/12/2025, with_for_update added
#--------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill, H_bill_line

def ts_restinv_run_help_check_billbl(case_type:int, tischnr:int, curr_dept:int):

    prepare_cache ([H_bill_line])

    pvilanguage:int = 0
    lvcarea:string = "ts-restinv"
    t_h_bill_data = []
    bill_saldo:Decimal = to_decimal("0.0")              # Rulita 4B5043, 15/08/2025
    h_bill = h_bill_line = None

    t_h_bill = None

    t_h_bill_data, T_h_bill = create_model_like(H_bill, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal pvilanguage, lvcarea, t_h_bill_data, bill_saldo, h_bill, h_bill_line
        nonlocal case_type, tischnr, curr_dept


        nonlocal t_h_bill
        nonlocal t_h_bill_data

        return {"t-h-bill": t_h_bill_data}

    if case_type == 1:

        # h_bill = get_cache (H_bill, {"tischnr": [(eq, tischnr)],"departement": [(eq, curr_dept)],"flag": [(eq, 0)]})
        h_bill = db_session.query(H_bill).filter(
                 (H_bill.tischnr == tischnr) & (H_bill.departement == curr_dept) & (H_bill.flag == 0)).with_for_update().first()

        # Rulita 4B5043, 15/08/2025
        if h_bill:

            if h_bill.saldo != 0:
                bill_saldo =  to_decimal("0")

                for h_bill_line in db_session.query(H_bill_line).filter(
                         (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == h_bill.departement)).order_by(H_bill_line._recid).all():
                    bill_saldo =  to_decimal(bill_saldo) + to_decimal(h_bill_line.betrag)

                if bill_saldo != h_bill.saldo:
                    pass
                    h_bill.saldo =  to_decimal(bill_saldo)
                    pass

    elif case_type == 2:

        h_bill = get_cache (H_bill, {"tischnr": [(eq, tischnr)],"departement": [(eq, curr_dept)]})

    elif case_type == 3:

        h_bill = get_cache (H_bill, {"tischnr": [(eq, tischnr)],"departement": [(eq, curr_dept)],"flag": [(eq, 0)]})

        if h_bill:
            t_h_bill_data.clear()
            t_h_bill = T_h_bill()
            t_h_bill_data.append(t_h_bill)

            t_h_bill.bilname = translateExtended ("Table already has an active bill", lvcarea, "")

            return generate_output()
        else:

            return generate_output()

    elif case_type == 4:

        h_bill = get_cache (H_bill, {"tischnr": [(eq, tischnr)],"departement": [(eq, curr_dept)],"flag": [(eq, 0)]})

        if not h_bill:
            t_h_bill_data.clear()
            t_h_bill = T_h_bill()
            t_h_bill_data.append(t_h_bill)

            t_h_bill.bilname = translateExtended ("There is no bill active on this table" + chr_unicode(10) +\
                    "Or bill on this table has been closed" + chr_unicode(10) +\
                    "Payment not possible", lvcarea, "")

            return generate_output()
        else:

            return generate_output()

    if h_bill:
        t_h_bill = T_h_bill()
        t_h_bill_data.append(t_h_bill)

        buffer_copy(h_bill, t_h_bill)
        t_h_bill.rec_id = h_bill._recid

    return generate_output()