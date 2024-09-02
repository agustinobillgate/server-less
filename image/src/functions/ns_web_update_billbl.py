from functions.additional_functions import *
import decimal
from datetime import date
from functions.ns_invoice_check_saldobl import ns_invoice_check_saldobl
from functions.inv_update_billbl import inv_update_billbl
from functions.read_bill2bl import read_bill2bl
from models import Bill_line, Bill

def ns_web_update_billbl(pvilanguage:int, bil_flag:int, b_recid:int, t_bill_rechnr:int, bill_line_departement:int, transdate:date, billart:int, qty:int, price:decimal, amount:decimal, amount_foreign:decimal, description:str, voucher_nr:str, cancel_str:str, user_init:str, rechnr:int, balance:decimal, balance_foreign:decimal):
    msg_str = ""
    success_flag = False
    t_bill_list = []
    t_bill_line_list = []
    lvcarea:str = "ns_web_update_billbl"
    master_str:str = ""
    master_rechnr:str = ""
    master_flag:bool = False
    msg_answer:bool = False
    str1:str = "NS"
    bline_dept:int = 0
    gname:str = ""
    bil_recid:int = 0
    telbill_flag:bool = False
    babill_flag:bool = False
    bill_line = bill = None

    t_bill_line = t_blinebuff = t_bill = None

    t_bill_line_list, T_bill_line = create_model_like(Bill_line, {"bl_recid":int, "artart":int, "tool_tip":str})
    t_blinebuff_list, T_blinebuff = create_model_like(Bill_line, {"bl_recid":int, "artart":int, "tool_tip":str})
    t_bill_list, T_bill = create_model_like(Bill, {"bl_recid":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, success_flag, t_bill_list, t_bill_line_list, lvcarea, master_str, master_rechnr, master_flag, msg_answer, str1, bline_dept, gname, bil_recid, telbill_flag, babill_flag, bill_line, bill


        nonlocal t_bill_line, t_blinebuff, t_bill
        nonlocal t_bill_line_list, t_blinebuff_list, t_bill_list
        return {"msg_str": msg_str, "success_flag": success_flag, "t-bill": t_bill_list, "t-bill-line": t_bill_line_list}


    bline_dept = bill_line_departement

    if t_bill_rechnr != 0:
        t_bill_list, t_bill_line_list = get_output(ns_invoice_check_saldobl(0, t_bill_rechnr))

        t_bill = query(t_bill_list, first=True)

        if t_bill and t_bill.resnr == 0 and t_bill.flag == 0:
            bil_recid = t_bill.bl_recid
            gname = t_bill.name
    rechnr, master_str, master_rechnr, balance, balance_foreign, master_flag, msg_str, success_flag, t_blinebuff_list = get_output(inv_update_billbl(pvilanguage, bil_flag, str1, transdate, b_recid, bline_dept, billart, qty, price, amount, amount_foreign, description, voucher_nr, cancel_str, user_init, rechnr, master_str, master_rechnr, balance, balance_foreign))
    telbill_flag, babill_flag, t_bill_list = get_output(read_bill2bl(5, b_recid, None, None, None, None, None, None, None, None))

    t_blinebuff = query(t_blinebuff_list, first=True)

    if t_blinebuff:
        t_bill_line = T_bill_line()
        t_bill_line_list.append(t_bill_line)

        buffer_copy(t_blinebuff, t_bill_line)

    return generate_output()