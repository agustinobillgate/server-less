from functions.additional_functions import *
import decimal
from sqlalchemy import func
from functions.del_reslinebl import del_reslinebl
from models import Res_line, Bediener, Htparam

def del_reservebl(pvilanguage:int, res_mode:str, resnr:int, user_init:str, cancel_str:str):
    msg_str = ""
    del_mainres:bool = False
    lvcarea:str = "del-reserve"
    res_line = bediener = htparam = None

    rline = None

    Rline = create_buffer("Rline",Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, del_mainres, lvcarea, res_line, bediener, htparam
        nonlocal pvilanguage, res_mode, resnr, user_init, cancel_str
        nonlocal rline


        nonlocal rline
        return {"msg_str": msg_str}


    bediener = db_session.query(Bediener).filter(
             (func.lower(Bediener.userinit) == (user_init).lower())).first()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 87)).first()

    if res_mode.lower()  == ("cancel").lower()  or res_mode.lower()  == ("delete").lower() :

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == resnr) & (Res_line.active_flag == 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).first()
        while None != res_line:
            del_mainres, msg_str = get_output(del_reslinebl(pvilanguage, res_mode, res_line.resnr, res_line.reslinnr, user_init, cancel_str))

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.resnr == resnr) & (Res_line.active_flag == 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).filter(Res_line._recid > curr_recid).first()

    return generate_output()