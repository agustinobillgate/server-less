#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Kontline

def read_kontlinebl(case_type:int, kontignr:int, konstat:int, gastno:int, kontcode:string, datum:date):
    t_kontline_list = []
    curr_kontig:int = 0
    kontline = None

    t_kontline = None

    t_kontline_list, T_kontline = create_model_like(Kontline)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_kontline_list, curr_kontig, kontline
        nonlocal case_type, kontignr, konstat, gastno, kontcode, datum


        nonlocal t_kontline
        nonlocal t_kontline_list

        return {"t-kontline": t_kontline_list}

    if kontignr < 0:
        curr_kontig = - kontignr
    else:
        curr_kontig = kontignr

    if case_type == 1:

        kontline = get_cache (Kontline, {"kontignr": [(eq, curr_kontig)],"kontstatus": [(eq, konstat)]})
    elif case_type == 2:

        kontline = get_cache (Kontline, {"gastnr": [(eq, gastno)],"kontcode": [(eq, kontcode)],"kontstatus": [(eq, konstat)],"ankunft": [(le, datum)],"abreise": [(ge, datum)]})
    elif case_type == 3:

        kontline = get_cache (Kontline, {"kontignr": [(eq, curr_kontig)],"kontcode": [(eq, kontcode)],"kontstatus": [(eq, konstat)]})
    elif case_type == 4:

        kontline = get_cache (Kontline, {"gastnr": [(eq, gastno)],"kontignr": [(eq, curr_kontig)],"kontstatus": [(eq, konstat)]})
    elif case_type == 5:

        kontline = get_cache (Kontline, {"kontignr": [(eq, curr_kontig)],"kontcode": [(eq, kontcode)],"kontstatus": [(eq, konstat)]})
    elif case_type == 6:

        if curr_kontig != 0 and curr_kontig != None:

            kontline = get_cache (Kontline, {"gastnr": [(eq, gastno)],"kontignr": [(eq, curr_kontig)],"kontstatus": [(eq, konstat)],"betriebsnr": [(eq, 1)]})
        else:

            kontline = db_session.query(Kontline).filter(
                     (Kontline.gastnr == gastno) & (Kontline.kontignr > 0) & (Kontline.kontstatus == konstat) & (Kontline.betriebsnr == 1)).first()
    elif case_type == 7:

        if curr_kontig != 0 and curr_kontig != None:

            kontline = get_cache (Kontline, {"gastnr": [(eq, gastno)],"kontignr": [(eq, curr_kontig)],"kontstatus": [(eq, konstat)],"betriebsnr": [(eq, 0)]})
        else:

            kontline = db_session.query(Kontline).filter(
                     (Kontline.gastnr == gastno) & (Kontline.kontignr > 0) & (Kontline.kontstatus == konstat) & (Kontline.betriebsnr == 0)).first()
    elif case_type == 8:

        kontline = get_cache (Kontline, {"kontcode": [(eq, kontcode)],"betriebsnr": [(eq, 0)],"gastnr": [(ne, gastno),(gt, 0)],"kontstatus": [(eq, 1)]})
    elif case_type == 9:

        kontline = get_cache (Kontline, {"kontcode": [(eq, kontcode)],"gastnr": [(eq, gastno)]})
    elif case_type == 10:

        kontline = get_cache (Kontline, {"kontignr": [(eq, kontignr)],"gastnr": [(eq, gastno)]})
    elif case_type == 11:

        kontline = get_cache (Kontline, {"gastnr": [(eq, gastno)],"kontignr": [(eq, kontignr)],"betriebsnr": [(eq, 0)],"kontstatus": [(eq, 1)]})
    elif case_type == 12:

        kontline = get_cache (Kontline, {"gastnr": [(eq, gastno)],"kontignr": [(eq, kontignr)],"betriebsnr": [(eq, 1)],"kontstatus": [(eq, 1)]})
    elif case_type == 13:

        kontline = get_cache (Kontline, {"gastnr": [(eq, gastno)],"betriebsnr": [(eq, 1)],"kontcode": [(eq, kontcode)],"kontignr": [(ne, kontignr)],"zikatnr": [(ne, konstat)],"kontstatus": [(eq, 1)]})
    elif case_type == 14:

        kontline = get_cache (Kontline, {"kontcode": [(eq, kontcode)],"betriebsnr": [(eq, 1)],"gastnr": [(ne, gastno),(gt, 0)],"kontstatus": [(eq, 1)]})

    if kontline:
        t_kontline = T_kontline()
        t_kontline_list.append(t_kontline)

        buffer_copy(kontline, t_kontline)

    return generate_output()