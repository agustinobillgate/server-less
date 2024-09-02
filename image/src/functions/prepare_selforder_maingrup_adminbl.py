from functions.additional_functions import *
import decimal
from models import Queasy, Paramtext, Hoteldpt

def prepare_selforder_maingrup_adminbl():
    t_maingrp_list = []
    t_dept_list = []
    licensenr = 0
    queasy = paramtext = hoteldpt = None

    t_maingrp = t_dept = None

    t_maingrp_list, T_maingrp = create_model_like(Queasy)
    t_dept_list, T_dept = create_model("T_dept", {"nr":int, "dept":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_maingrp_list, t_dept_list, licensenr, queasy, paramtext, hoteldpt


        nonlocal t_maingrp, t_dept
        nonlocal t_maingrp_list, t_dept_list
        return {"t-maingrp": t_maingrp_list, "t-dept": t_dept_list, "licensenr": licensenr}

    def decode_string(in_str:str):

        nonlocal t_maingrp_list, t_dept_list, licensenr, queasy, paramtext, hoteldpt


        nonlocal t_maingrp, t_dept
        nonlocal t_maingrp_list, t_dept_list

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return out_str
        s = in_str
        j = ord(substring(s, 0, 1)) - 70
        len_ = len(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,len(s)  + 1) :
            out_str = out_str + chr (ord(substring(s, len_ - 1, 1)) - j)


        return generate_inner_output()


    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 228)).all():
        t_maingrp = T_maingrp()
        t_maingrp_list.append(t_maingrp)

        buffer_copy(queasy, t_maingrp)

    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == 243)).first()

    if paramtext and paramtext.ptexte != "":
        licensenr = decode_string(ptexte)

    for hoteldpt in db_session.query(Hoteldpt).filter(
            (Hoteldpt.num > 0)).all():
        t_dept = T_dept()
        t_dept_list.append(t_dept)

        t_dept.nr = hoteldpt.num
        t_dept.dept = hoteldpt.depart.upper()

    return generate_output()