#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Zimkateg

def mk_resline_reslin_list_zinr3bl(zikatstr:string):
    t_zimkateg_list = []
    zimkateg = None

    t_zimkateg = None

    t_zimkateg_list, T_zimkateg = create_model_like(Zimkateg)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_zimkateg_list, zimkateg
        nonlocal zikatstr


        nonlocal t_zimkateg
        nonlocal t_zimkateg_list

        return {"t-zimkateg": t_zimkateg_list}

    zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, zikatstr)]})
    t_zimkateg = T_zimkateg()
    t_zimkateg_list.append(t_zimkateg)

    buffer_copy(zimkateg, t_zimkateg)

    return generate_output()