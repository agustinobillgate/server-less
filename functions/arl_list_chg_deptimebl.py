#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.intevent_1 import intevent_1
from models import Res_line, Htparam

def arl_list_chg_deptimebl(recid_resline:int, zeit:int):

    prepare_cache ([Res_line, Htparam])

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


    resline = get_cache (Res_line, {"_recid": [(eq, recid_resline)]})

    if resline:
        pass
        resline.abreisezeit = zeit

        htparam = get_cache (Htparam, {"paramnr": [(eq, 341)]})

        if htparam.fchar != "" and resline.resstatus == 6:
            get_output(intevent_1(9, resline.zinr, "Chg DepTime!", resline.resnr, resline.reslinnr))
        pass
        pass

    return generate_output()