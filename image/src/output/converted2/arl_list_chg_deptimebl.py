from functions.additional_functions import *
import decimal
from functions.intevent_1 import intevent_1
from models import Res_line, Htparam

def arl_list_chg_deptimebl(recid_resline:int, zeit:int):
    res_line = htparam = None

    resline = None

    Resline = create_buffer("Resline",Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_line, htparam
        nonlocal recid_resline, zeit
        nonlocal resline


        nonlocal resline
        return {}


    resline = db_session.query(Resline).filter(
                 (Resline._recid == recid_resline)).first()
    resline.abreisezeit = zeit

    htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 341)).first()

    if htparam.fchar != "" and resline.resstatus == 6:
        get_output(intevent_1(9, resline.zinr, "Chg DepTime!", resline.resnr, resline.reslinnr))


    return generate_output()