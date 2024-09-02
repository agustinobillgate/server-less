from functions.additional_functions import *
import decimal
from models import H_bill, H_bill_line

def ts_restinv_check_move_table_1bl(case_mode:int, rec_id:int, bill_no:int, curr_tableno:int, dept_no:int):
    error_code = 0
    table_no = 0
    h_bill = h_bill_line = None

    buff_hbill = sp_bline = None

    Buff_hbill = H_bill
    Sp_bline = H_bill_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_code, table_no, h_bill, h_bill_line
        nonlocal buff_hbill, sp_bline


        nonlocal buff_hbill, sp_bline
        return {"error_code": error_code, "table_no": table_no}


    if case_mode == 1:

        h_bill = db_session.query(H_bill).filter(
                (H_bill.rechnr == bill_no) &  (H_bill.departement == dept_no) &  (H_bill.tischnr == curr_tableno)).first()

        if not h_bill:

            buff_hbill = db_session.query(Buff_hbill).filter(
                    (Buff_hbill._recid == rec_id)).first()

            if buff_hbill:
                table_no = buff_hbill.tischnr
            error_code = 1

            return generate_output()

    elif case_mode == 2:

        sp_bline = db_session.query(Sp_bline).filter(
                (Sp_bline.rechnr == bill_no) &  (Sp_bline.departement == dept_no) &  (Sp_bline.waehrungsnr > 0)).first()

        if sp_bline:
            error_code = 2

            return generate_output()

    elif case_mode == 3:

        h_bill = db_session.query(H_bill).filter(
                (H_bill._recid == rec_id)).first()

        if h_bill:

            if h_bill.flag == 0 and h_bill.saldo == 0:

                h_bill_line = db_session.query(H_bill_line).filter(
                        (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.departement == h_bill.departement) &  (H_bill_line.betrag == 0)).first()

                if not h_bill_line:
                    error_code = 3

                    return generate_output()