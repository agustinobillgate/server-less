#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line

t_res_line_data, T_res_line = create_model_like(Res_line)

def write_res_linebl(case_type:int, t_res_line_data:[T_res_line]):
    success_flag = False
    res_line = None

    t_res_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, res_line
        nonlocal case_type


        nonlocal t_res_line

        return {"success_flag": success_flag}

    def delete_procedure():

        nonlocal success_flag, res_line
        nonlocal case_type


        nonlocal t_res_line

    t_res_line = query(t_res_line_data, first=True)

    if case_type == 1:

        res_line = get_cache (Res_line, {"resnr": [(eq, t_res_line.resnr)],"reslinnr": [(eq, t_res_line.reslinnr)]})

        if res_line:
            buffer_copy(t_res_line, res_line)
            pass
            success_flag = True
    elif case_type == 2:
        res_line = Res_line()
        db_session.add(res_line)

        buffer_copy(t_res_line, res_line)
        pass
        success_flag = True
    elif case_type == 3:

        res_line = get_cache (Res_line, {"resnr": [(eq, t_res_line.resnr)],"reslinnr": [(eq, t_res_line.reslinnr)]})

        if res_line:
            success_flag = True

    return generate_output()