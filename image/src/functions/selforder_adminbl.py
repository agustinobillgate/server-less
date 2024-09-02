from functions.additional_functions import *
import decimal
from datetime import date
from models import Queasy

def selforder_adminbl(deptno:int, grup:int, paramnr:int, intval:int, decval:decimal, dateval:date, logval:bool, charval:str):
    htp_val = ""
    htp_logv = False
    queasy = None

    t_param = None

    t_param_list, T_param = create_model("T_param", {"grup":int, "number":int, "bezeich":str, "typ":int, "logv":bool, "val":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal htp_val, htp_logv, queasy


        nonlocal t_param
        nonlocal t_param_list
        return {"htp_val": htp_val, "htp_logv": htp_logv}

    def update_queasy():

        nonlocal htp_val, htp_logv, queasy


        nonlocal t_param
        nonlocal t_param_list

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 222) &  (Queasy.betriebsnr == deptno) &  (Queasy.number1 == grup) &  (Queasy.number2 == paramnr)).first()

        if queasy.number3 == 1:
            queasy.char2 = to_string(intval)
            htp_val = to_string(queasy.char2)

        elif queasy.number3 == 2:
            queasy.deci1 = decval
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