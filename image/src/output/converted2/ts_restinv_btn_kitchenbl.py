#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Printer

def ts_restinv_btn_kitchenbl(avail_t_h_bill:bool, from_acct:bool, prorder:int, prorder2:int):
    close_it = True
    err_code1 = 0
    err_code2 = 0
    t_printer1_list = []
    t_printer2_list = []
    printer = None

    t_printer1 = t_printer2 = None

    t_printer1_list, T_printer1 = create_model_like(Printer)
    t_printer2_list, T_printer2 = create_model_like(Printer)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal close_it, err_code1, err_code2, t_printer1_list, t_printer2_list, printer
        nonlocal avail_t_h_bill, from_acct, prorder, prorder2


        nonlocal t_printer1, t_printer2
        nonlocal t_printer1_list, t_printer2_list

        return {"close_it": close_it, "err_code1": err_code1, "err_code2": err_code2, "t-printer1": t_printer1_list, "t-printer2": t_printer2_list}


    if avail_t_h_bill and not from_acct:

        if prorder2 > 0:

            printer = get_cache (Printer, {"nr": [(eq, prorder2)]})

            if printer:
                close_it = False

        printer = get_cache (Printer, {"nr": [(eq, prorder)]})

        if not printer or (prorder == 0):
            err_code1 = 1

            return generate_output()
        err_code1 = 2
        t_printer1 = T_printer1()
        t_printer1_list.append(t_printer1)

        buffer_copy(printer, t_printer1)

    if prorder2 != 0:

        printer = get_cache (Printer, {"nr": [(eq, prorder2)]})

        if not printer:
            err_code2 = 1

            return generate_output()
        err_code2 = 2
        t_printer2 = T_printer2()
        t_printer2_list.append(t_printer2)

        buffer_copy(printer, t_printer2)

    return generate_output()