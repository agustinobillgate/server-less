from functions.additional_functions import *
import decimal
from models import Queasy, Hoteldpt, Wgrpdep

def prepare_selforder_subgrup_adminbl():
    t_subgrp_list = []
    t_maingrp_list = []
    t_dept_list = []
    queasy = hoteldpt = wgrpdep = None

    t_subgrp = t_maingrp = t_dept = buf_queasy = None

    t_subgrp_list, T_subgrp = create_model("T_subgrp", {"key":int, "subgrp_no":int, "subgrp":str, "maingrp_no":int, "maingrp":str, "dept":int, "dept_str":str, "prior":int})
    t_maingrp_list, T_maingrp = create_model_like(Queasy)
    t_dept_list, T_dept = create_model("T_dept", {"nr":int, "dept":str})

    Buf_queasy = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_subgrp_list, t_maingrp_list, t_dept_list, queasy, hoteldpt, wgrpdep
        nonlocal buf_queasy


        nonlocal t_subgrp, t_maingrp, t_dept, buf_queasy
        nonlocal t_subgrp_list, t_maingrp_list, t_dept_list
        return {"t-subgrp": t_subgrp_list, "t-maingrp": t_maingrp_list, "t-dept": t_dept_list}

    wgrpdep_obj_list = []
    for wgrpdep, hoteldpt in db_session.query(Wgrpdep, Hoteldpt).join(Hoteldpt,(Hoteldpt.num == Wgrpdep.departement)).all():
        if wgrpdep._recid in wgrpdep_obj_list:
            continue
        else:
            wgrpdep_obj_list.append(wgrpdep._recid)


        t_subgrp = T_subgrp()
        t_subgrp_list.append(t_subgrp)

        t_subgrp.dept = wgrpdep.departement
        t_subgrp.subgrp_no = wgrpdep.zknr
        t_subgrp.subgrp = wgrpdep.bezeich
        t_subgrp.prior = wgrpdep.betriebsnr
        t_subgrp.dept_str = hoteldpt.depart

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 229) &  (Queasy.number1 == wgrpdep.zknr) &  (Queasy.number2 == wgrpdep.departement)).first()

        if queasy:
            t_subgrp.key = queasy.KEY
            t_subgrp.maingrp_no = queasy.number3

            buf_queasy = db_session.query(Buf_queasy).filter(
                    (Buf_queasy.key == 228) &  (Buf_queasy.number1 == queasy.number3)).first()

            if buf_queasy:
                t_subgrp.maingrp = buf_queasy.char1

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 228)).all():
        t_maingrp = T_maingrp()
        t_maingrp_list.append(t_maingrp)

        buffer_copy(queasy, t_maingrp)

    for hoteldpt in db_session.query(Hoteldpt).filter(
            (Hoteldpt.num > 0)).all():
        t_dept = T_dept()
        t_dept_list.append(t_dept)

        t_dept.nr = hoteldpt.num
        t_dept.dept = hoteldpt.depart.upper()

    return generate_output()