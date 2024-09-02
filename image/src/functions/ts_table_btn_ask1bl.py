from functions.additional_functions import *
import decimal
from functions.ts_table_check_creditlimitbl import ts_table_check_creditlimitbl
from models import Res_line, Queasy

def ts_table_btn_ask1bl(pvilanguage:int, resrecid:int):
    klimit = 0
    ksaldo = 0
    remark = ""
    msg_str = ""
    t_resline_list = []
    lvcarea:str = "TS_table"
    res_line = queasy = None

    t_resline = None

    t_resline_list, T_resline = create_model("T_resline", {"resnr":int, "reslinnr":int, "zinr":str, "name":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal klimit, ksaldo, remark, msg_str, t_resline_list, lvcarea, res_line, queasy


        nonlocal t_resline
        nonlocal t_resline_list
        return {"klimit": klimit, "ksaldo": ksaldo, "remark": remark, "msg_str": msg_str, "t-resline": t_resline_list}

    res_line = db_session.query(Res_line).filter(
            (Res_line._recid == resrecid)).first()

    if res_line:
        klimit, ksaldo, remark = get_output(ts_table_check_creditlimitbl(resrecid))

        if res_line.code != "":

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 9) &  (Queasy.number1 == to_int(res_line.code))).first()

            if queasy and queasy.logi1:
                msg_str = msg_str + chr(2) + "&W" + translateExtended ("CASH BASIS Billing Instruction: ", lvcarea, "") + queasy.char1
        t_resline = T_resline()
        t_resline_list.append(t_resline)

        t_resline.resnr = res_line.resnr
        t_resline.reslinnr = res_line.reslinnr
        t_resline.zinr = res_line.zinr
        t_resline.name = res_line.name

        return generate_output()