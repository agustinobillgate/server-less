#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added, remark area
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy

def selforder_adminbl(deptno:int, grup:int, paramnr:int, intval:int, decval:Decimal, dateval:date, logval:bool, charval:string):

    prepare_cache ([Queasy])

    htp_val = ""
    htp_logv = False
    queasy = None

    t_param = None

    t_param_data, T_param = create_model("T_param", {"grup":int, "number":int, "bezeich":string, "typ":int, "logv":bool, "val":string})

    db_session = local_storage.db_session
    charval = charval.strip()

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

        # queasy = get_cache (Queasy, {"key": [(eq, 222)],"betriebsnr": [(eq, deptno)],"number1": [(eq, grup)],"number2": [(eq, paramnr)]})
        queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 222) &
                    (Queasy.betriebsnr == deptno) &
                    (Queasy.number1 == grup) &
                    (Queasy.number2 == paramnr)).with_for_update().first()

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

    update_queasy()

    return generate_output()