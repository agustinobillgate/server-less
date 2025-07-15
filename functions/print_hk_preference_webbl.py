#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.read_res_linebl import read_res_linebl
from models import Res_line

t_buff_data, T_buff = create_model("T_buff", {"key":int, "number1":int, "number2":int, "number3":int, "date1":date, "date2":date, "date3":date, "char1":string, "char2":string, "char3":string, "deci1":Decimal, "deci2":Decimal, "deci3":Decimal, "logi1":bool, "logi2":bool, "logi3":bool, "betriebsnr":int, "gname":string})

def print_hk_preference_webbl(t_buff_data:[T_buff]):
    res_line = None

    t_buff = t_res_line = None

    t_res_line_data, T_res_line = create_model_like(Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_line


        nonlocal t_buff, t_res_line
        nonlocal t_res_line_data

        return {"t-buff": t_buff_data}


    for t_buff in query(t_buff_data, sort_by=[("char1",False),("date1",False)]):
        t_res_line_data = get_output(read_res_linebl(20, None, None, 6, 1, t_buff.char1, None, None, None, None, ""))

        t_res_line = query(t_res_line_data, first=True)

        if not t_res_line:
            t_res_line_data = get_output(read_res_linebl(20, None, None, 13, 1, t_buff.char1, None, None, None, None, ""))

        t_res_line = query(t_res_line_data, filters=(lambda t_res_line: t_res_line.zinr == t_buff.char1), first=True)

        if t_res_line:
            t_buff.gname = t_res_line.name

    return generate_output()