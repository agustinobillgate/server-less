#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def ts_biltransfer2_webbl(mc_str:string, curr_dept:int):
    do_it = False
    msg_str = ""
    t_queasy_list = []
    excl_str:string = ""
    count_i:int = 0
    dept:int = 0
    queasy = None

    t_queasy = dept_list = None

    t_queasy_list, T_queasy = create_model("T_queasy", {"char3":string, "char1":string, "number3":int, "deci3":Decimal})
    dept_list_list, Dept_list = create_model("Dept_list", {"deptno":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal do_it, msg_str, t_queasy_list, excl_str, count_i, dept, queasy
        nonlocal mc_str, curr_dept


        nonlocal t_queasy, dept_list
        nonlocal t_queasy_list, dept_list_list

        return {"do_it": do_it, "msg_str": msg_str, "t-queasy": t_queasy_list}

    dept_list_list.clear()

    queasy = get_cache (Queasy, {"key": [(eq, 105)],"number2": [(eq, 0)],"deci2": [(eq, 0)],"char2": [(eq, mc_str)],"logi2": [(eq, False)]})
    do_it = None != queasy

    if queasy:
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        t_queasy.char3 = queasy.char3
        t_queasy.char1 = queasy.char1
        t_queasy.number3 = queasy.number3
        t_queasy.deci3 =  to_decimal(queasy.deci3)

    t_queasy = query(t_queasy_list, first=True)

    if t_queasy:
        excl_str = ""
        excl_str = entry(1, t_queasy.char3, "&")

        if excl_str != "":
            for count_i in range(1,num_entries(excl_str, ",")  + 1) :
                dept = -1
                dept = to_int(entry(count_i - 1, excl_str, ","))

                if dept > 0:
                    dept_list = Dept_list()
                    dept_list_list.append(dept_list)

                    dept_list.deptno = dept

            dept_list = query(dept_list_list, filters=(lambda dept_list: dept_list.deptno == curr_dept), first=True)

            if dept_list:
                msg_str = "Card not applicable for this outlet."

                return generate_output()
    else:
        msg_str = "No such Card Number found."

        return generate_output()

    return generate_output()