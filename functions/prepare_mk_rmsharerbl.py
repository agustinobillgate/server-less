#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Res_line, Guest

def prepare_mk_rmsharerbl(inp_resnr:int, inp_resline:int):

    prepare_cache ([Guest])

    anz_sharer = 0
    gnation = ""
    ci_date = None
    t_res_line_data = []
    res_line = guest = None

    t_res_line = rline = None

    t_res_line_data, T_res_line = create_model_like(Res_line)

    Rline = create_buffer("Rline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal anz_sharer, gnation, ci_date, t_res_line_data, res_line, guest
        nonlocal inp_resnr, inp_resline
        nonlocal rline


        nonlocal t_res_line, rline
        nonlocal t_res_line_data

        return {"anz_sharer": anz_sharer, "gnation": gnation, "ci_date": ci_date, "t-res-line": t_res_line_data}

    res_line = get_cache (Res_line, {"resnr": [(eq, inp_resnr)],"reslinnr": [(eq, inp_resline)]})

    if not res_line:

        return generate_output()
    t_res_line = T_res_line()
    t_res_line_data.append(t_res_line)

    buffer_copy(res_line, t_res_line)
    ci_date = get_output(htpdate(87))

    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

    if guest.karteityp == 0:
        gnation = guest.nation1
    else:
        gnation = guest.land

    if res_line.erwachs == 1:

        return generate_output()
    anz_sharer = res_line.erwachs - 1

    for rline in db_session.query(Rline).filter(
             (Rline.resnr == inp_resnr) & ((Rline.resstatus == 11) | (Rline.resstatus == 13)) & (Rline.active_flag <= 1)).order_by(Rline._recid).all():
        anz_sharer = anz_sharer - 1

    if res_line.zimmeranz > 1:
        gnation = gnation + chr_unicode(2) + to_string(res_line.zimmeranz)

        if anz_sharer > 1:
            anz_sharer = 1

    return generate_output()