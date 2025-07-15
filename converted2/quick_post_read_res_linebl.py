#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line

def quick_post_read_res_linebl(resnr:int, reslinnr:int):

    prepare_cache ([Res_line])

    t_res_line_data = []
    res_line = None

    t_res_line = None

    t_res_line_data, T_res_line = create_model("T_res_line", {"resnr":int, "reslinnr":int, "name":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_res_line_data, res_line
        nonlocal resnr, reslinnr


        nonlocal t_res_line
        nonlocal t_res_line_data

        return {"t-res-line": t_res_line_data}

    if reslinnr != None:

        res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_data.append(t_res_line)

            t_res_line.resnr = res_line.resnr
            t_res_line.reslinnr = res_line.reslinnr
            t_res_line.name = res_line.name


    else:

        res_line = get_cache (Res_line, {"_recid": [(eq, resnr)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_data.append(t_res_line)

            t_res_line.resnr = res_line.resnr
            t_res_line.reslinnr = res_line.reslinnr
            t_res_line.name = res_line.name

    return generate_output()