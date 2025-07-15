#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy

def vhp_rms_parambl(deptno:int, grup:int, paramnr:int, intval:int, decval:Decimal, dateval:date, logval:bool, charval:string):

    prepare_cache ([Queasy])

    htp_val = ""
    htp_logv = False
    queasy = None

    t_param = None

    t_param_data, T_param = create_model("T_param", {"grup":int, "number":int, "bezeich":string, "typ":int, "logv":bool, "val":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal htp_val, htp_logv, queasy
        nonlocal deptno, grup, paramnr, intval, decval, dateval, logval, charval


        nonlocal t_param
        nonlocal t_param_data

        return {"htp_val": htp_val, "htp_logv": htp_logv}

    def update_queasy():

        nonlocal htp_val, htp_logv, queasy
        nonlocal deptno, grup, paramnr, intval, decval, dateval, logval, charval


        nonlocal t_param
        nonlocal t_param_data

        queasy = get_cache (Queasy, {"key": [(eq, 347)],"betriebsnr": [(eq, 3)],"number1": [(eq, paramnr)]})

        if queasy:
            pass

            if queasy.number3 == 1:
                queasy.char2 = to_string(intval)
                htp_val = to_string(queasy.char2)

            elif queasy.number3 == 2:
                queasy.deci1 =  to_decimal(decval)
                htp_val = to_string(queasy.deci1)

            elif queasy.number3 == 3:
                queasy.date1 = dateval
                htp_val = to_string(queasy.date1)

            elif queasy.number3 == 4:
                queasy.logi1 = logval
                htp_logv = queasy.logi1

            elif queasy.number3 == 5:
                queasy.char2 = to_string(charval)
                htp_val = to_string(queasy.char2)
            pass
            pass

    update_queasy()

    return generate_output()