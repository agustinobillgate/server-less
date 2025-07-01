#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill, H_bill_line

def ts_restinv_check_move_table_1bl(case_mode:int, rec_id:int, bill_no:int, curr_tableno:int, dept_no:int):

    prepare_cache ([H_bill])

    error_code = 0
    table_no = 0
    h_bill = h_bill_line = None

    buff_hbill = sp_bline = None

    Buff_hbill = create_buffer("Buff_hbill",H_bill)
    Sp_bline = create_buffer("Sp_bline",H_bill_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_code, table_no, h_bill, h_bill_line
        nonlocal case_mode, rec_id, bill_no, curr_tableno, dept_no
        nonlocal buff_hbill, sp_bline


        nonlocal buff_hbill, sp_bline

        return {"error_code": error_code, "table_no": table_no}


    if case_mode == 1:

        h_bill = get_cache (H_bill, {"rechnr": [(eq, bill_no)],"departement": [(eq, dept_no)],"tischnr": [(eq, curr_tableno)]})

        if not h_bill:

            buff_hbill = get_cache (H_bill, {"_recid": [(eq, rec_id)]})

            if buff_hbill:
                table_no = buff_hbill.tischnr
            error_code = 1

            return generate_output()

    elif case_mode == 2:

        sp_bline = db_session.query(Sp_bline).filter(
                 (Sp_bline.rechnr == bill_no) & (Sp_bline.departement == dept_no) & (Sp_bline.waehrungsnr > 0)).first()

        if sp_bline:
            error_code = 2

            return generate_output()

    elif case_mode == 3:

        h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id)]})

        if h_bill:

            if h_bill.flag == 0 and h_bill.saldo == 0:

                h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, h_bill.rechnr)],"departement": [(eq, h_bill.departement)],"betrag": [(eq, 0)]})

                if not h_bill_line:
                    error_code = 3

                    return generate_output()

    return generate_output()