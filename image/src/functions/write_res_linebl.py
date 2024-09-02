from functions.additional_functions import *
import decimal
from models import Res_line

def write_res_linebl(case_type:int, t_res_line:[T_res_line]):
    success_flag = False
    res_line = None

    t_res_line = None

    t_res_line_list, T_res_line = create_model_like(Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, res_line


        nonlocal t_res_line
        nonlocal t_res_line_list
        return {"success_flag": success_flag}

    def delete_procedure():

        nonlocal success_flag, res_line


        nonlocal t_res_line
        nonlocal t_res_line_list

    hHandle = THIS_PROCEDURE

    t_res_line = query(t_res_line_list, first=True)

    if case_type == 1:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == t_Res_line.resnr) &  (Res_line.reslinnr == t_Res_line.reslinnr)).first()

        if res_line:
            buffer_copy(t_res_line, res_line)

            success_flag = True
    elif case_type == 2:
        res_line = Res_line()
        db_session.add(res_line)

        buffer_copy(t_res_line, res_line)

        success_flag = True
    elif case_type == 3:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == t_Res_line.resnr) &  (Res_line.reslinnr == t_Res_line.reslinnr)).first()

        if res_line:
            success_flag = True

    return generate_output()