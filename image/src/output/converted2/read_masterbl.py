#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Master, Bill, Res_line

def read_masterbl(case_type:int, resno:int, gastno:int):

    prepare_cache ([Bill, Res_line])

    t_master_list = []
    billno:int = 0
    master = bill = res_line = None

    t_master = mbill = None

    t_master_list, T_master = create_model_like(Master)

    Mbill = create_buffer("Mbill",Bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_master_list, billno, master, bill, res_line
        nonlocal case_type, resno, gastno
        nonlocal mbill


        nonlocal t_master, mbill
        nonlocal t_master_list

        return {"t-master": t_master_list}

    if case_type == 1:

        master = get_cache (Master, {"resnr": [(eq, resno)]})

        if master:
            t_master = T_master()
            t_master_list.append(t_master)

            buffer_copy(master, t_master)
    elif case_type == 2:

        master = get_cache (Master, {"resnr": [(eq, resno)],"flag": [(eq, 0)]})

        if master:
            t_master = T_master()
            t_master_list.append(t_master)

            buffer_copy(master, t_master)
    elif case_type == 3:

        master = get_cache (Master, {"resnr": [(eq, resno)],"active": [(eq, True)],"flag": [(eq, 0)]})

        if master:
            t_master = T_master()
            t_master_list.append(t_master)

            buffer_copy(master, t_master)
    elif case_type == 4:

        master = get_cache (Master, {"gastnr": [(eq, gastno)],"resnr": [(eq, resno)]})

        if master:
            t_master = T_master()
            t_master_list.append(t_master)

            buffer_copy(master, t_master)
    elif case_type == 5:
        billno = gastno

        bill = get_cache (Bill, {"rechnr": [(eq, billno)]})

        res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})

        if res_line.l_zuordnung[4] != 0:

            mbill = get_cache (Bill, {"resnr": [(eq, res_line.l_zuordnung[4])],"reslinnr": [(eq, 0)]})
        else:

            mbill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, 0)]})

        if not mbill:

            return generate_output()

        master = get_cache (Master, {"resnr": [(eq, mbill.resnr)]})

        if master:
            t_master = T_master()
            t_master_list.append(t_master)

            buffer_copy(master, t_master)

    return generate_output()