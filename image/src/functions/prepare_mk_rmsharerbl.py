from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from models import Res_line, Guest

def prepare_mk_rmsharerbl(inp_resnr:int, inp_resline:int):
    anz_sharer = 0
    gnation = ""
    ci_date = None
    t_res_line_list = []
    res_line = guest = None

    t_res_line = rline = None

    t_res_line_list, T_res_line = create_model_like(Res_line)

    Rline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal anz_sharer, gnation, ci_date, t_res_line_list, res_line, guest
        nonlocal rline


        nonlocal t_res_line, rline
        nonlocal t_res_line_list
        return {"anz_sharer": anz_sharer, "gnation": gnation, "ci_date": ci_date, "t-res-line": t_res_line_list}

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == inp_resnr) &  (Res_line.reslinnr == inp_resline)).first()

    if not res_line:

        return generate_output()
    t_res_line = T_res_line()
    t_res_line_list.append(t_res_line)

    buffer_copy(res_line, t_res_line)
    ci_date = get_output(htpdate(87))

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == res_line.gastnrmember)).first()

    if guest.karteityp == 0:
        gnation = guest.nation1
    else:
        gnation = guest.land

    if res_line.erwachs == 1:

        return generate_output()
    anz_sharer = res_line.erwachs - 1

    for rline in db_session.query(Rline).filter(
            (Rline.resnr == inp_resnr) &  ((Rline.resstatus == 11) |  (Rline.resstatus == 13)) &  (Rline.active_flag <= 1)).all():
        anz_sharer = anz_sharer - 1

    if res_line.zimmeranz > 1:
        gnation = gnation + chr(2) + to_string(res_line.zimmeranz)

        if anz_sharer > 1:
            anz_sharer = 1

    return generate_output()