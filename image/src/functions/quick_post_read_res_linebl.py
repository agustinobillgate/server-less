from functions.additional_functions import *
import decimal
from models import Res_line

def quick_post_read_res_linebl(resnr:int, reslinnr:int):
    t_res_line_list = []
    res_line = None

    t_res_line = None

    t_res_line_list, T_res_line = create_model("T_res_line", {"resnr":int, "reslinnr":int, "name":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_res_line_list, res_line


        nonlocal t_res_line
        nonlocal t_res_line_list
        return {"t-res-line": t_res_line_list}

    if reslinnr != None:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            t_res_line.resnr = res_line.resnr
            t_res_line.reslinnr = res_line.reslinnr
            t_res_line.name = res_line.name


    else:

        res_line = db_session.query(Res_line).filter(
                (Res_line._recid == resnr)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            t_res_line.resnr = res_line.resnr
            t_res_line.reslinnr = res_line.reslinnr
            t_res_line.name = res_line.name

    return generate_output()