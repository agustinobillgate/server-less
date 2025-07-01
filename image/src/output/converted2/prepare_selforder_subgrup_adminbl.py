#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Hoteldpt, Wgrpdep

def prepare_selforder_subgrup_adminbl():

    prepare_cache ([Queasy, Hoteldpt, Wgrpdep])

    t_subgrp_list = []
    t_maingrp_list = []
    t_dept_list = []
    queasy = hoteldpt = wgrpdep = None

    t_subgrp = t_maingrp = t_dept = buf_queasy = None

    t_subgrp_list, T_subgrp = create_model("T_subgrp", {"key":int, "subgrp_no":int, "subgrp":string, "maingrp_no":int, "maingrp":string, "dept":int, "dept_str":string, "prior":int})
    t_maingrp_list, T_maingrp = create_model_like(Queasy)
    t_dept_list, T_dept = create_model("T_dept", {"nr":int, "dept":string})

    Buf_queasy = create_buffer("Buf_queasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_subgrp_list, t_maingrp_list, t_dept_list, queasy, hoteldpt, wgrpdep
        nonlocal buf_queasy


        nonlocal t_subgrp, t_maingrp, t_dept, buf_queasy
        nonlocal t_subgrp_list, t_maingrp_list, t_dept_list

        return {"t-subgrp": t_subgrp_list, "t-maingrp": t_maingrp_list, "t-dept": t_dept_list}

    wgrpdep_obj_list = {}
    wgrpdep = Wgrpdep()
    hoteldpt = Hoteldpt()
    for wgrpdep.departement, wgrpdep.zknr, wgrpdep.bezeich, wgrpdep.betriebsnr, wgrpdep._recid, hoteldpt.depart, hoteldpt.num, hoteldpt._recid in db_session.query(Wgrpdep.departement, Wgrpdep.zknr, Wgrpdep.bezeich, Wgrpdep.betriebsnr, Wgrpdep._recid, Hoteldpt.depart, Hoteldpt.num, Hoteldpt._recid).join(Hoteldpt,(Hoteldpt.num == Wgrpdep.departement)).order_by(departement, Wgrpdep.zknr).all():
        if wgrpdep_obj_list.get(wgrpdep._recid):
            continue
        else:
            wgrpdep_obj_list[wgrpdep._recid] = True


        t_subgrp = T_subgrp()
        t_subgrp_list.append(t_subgrp)

        t_subgrp.dept = wgrpdep.departement
        t_subgrp.subgrp_no = wgrpdep.zknr
        t_subgrp.subgrp = wgrpdep.bezeich
        t_subgrp.prior = wgrpdep.betriebsnr
        t_subgrp.dept_str = hoteldpt.depart

        queasy = get_cache (Queasy, {"key": [(eq, 229)],"number1": [(eq, wgrpdep.zknr)],"number2": [(eq, wgrpdep.departement)]})

        if queasy:
            t_subgrp.key = queasy.key
            t_subgrp.maingrp_no = queasy.number3

            buf_queasy = get_cache (Queasy, {"key": [(eq, 228)],"number1": [(eq, queasy.number3)]})

            if buf_queasy:
                t_subgrp.maingrp = buf_queasy.char1

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 228)).order_by(Queasy._recid).all():
        t_maingrp = T_maingrp()
        t_maingrp_list.append(t_maingrp)

        buffer_copy(queasy, t_maingrp)

    for hoteldpt in db_session.query(Hoteldpt).filter(
             (Hoteldpt.num > 0)).order_by(Hoteldpt._recid).all():
        t_dept = T_dept()
        t_dept_list.append(t_dept)

        t_dept.nr = hoteldpt.num
        t_dept.dept = hoteldpt.depart.upper()

    return generate_output()