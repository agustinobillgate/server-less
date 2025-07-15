#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.ts_table_check_creditlimitbl import ts_table_check_creditlimitbl
from models import Res_line, Queasy

def ts_table_btn_ask1bl(pvilanguage:int, resrecid:int):

    prepare_cache ([Res_line, Queasy])

    klimit = to_decimal("0.0")
    ksaldo = to_decimal("0.0")
    remark = ""
    msg_str = ""
    t_resline_data = []
    lvcarea:string = "TS-table"
    res_line = queasy = None

    t_resline = None

    t_resline_data, T_resline = create_model("T_resline", {"resnr":int, "reslinnr":int, "zinr":string, "name":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal klimit, ksaldo, remark, msg_str, t_resline_data, lvcarea, res_line, queasy
        nonlocal pvilanguage, resrecid


        nonlocal t_resline
        nonlocal t_resline_data

        return {"klimit": klimit, "ksaldo": ksaldo, "remark": remark, "msg_str": msg_str, "t-resline": t_resline_data}

    res_line = get_cache (Res_line, {"_recid": [(eq, resrecid)]})

    if res_line:
        klimit, ksaldo, remark = get_output(ts_table_check_creditlimitbl(resrecid))

        if res_line.code != "":

            queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code))]})

            if queasy and queasy.logi1:
                msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("CASH BASIS Billing Instruction: ", lvcarea, "") + queasy.char1
        t_resline = T_resline()
        t_resline_data.append(t_resline)

        t_resline.resnr = res_line.resnr
        t_resline.reslinnr = res_line.reslinnr
        t_resline.zinr = res_line.zinr
        t_resline.name = res_line.name

        return generate_output()

    return generate_output()