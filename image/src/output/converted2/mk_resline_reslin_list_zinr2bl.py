#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Zimmer

def mk_resline_reslin_list_zinr2bl(r_zinr:string):
    t_zimmer_list = []
    zimmer = None

    t_zimmer = None

    t_zimmer_list, T_zimmer = create_model_like(Zimmer)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_zimmer_list, zimmer
        nonlocal r_zinr


        nonlocal t_zimmer
        nonlocal t_zimmer_list

        return {"t-zimmer": t_zimmer_list}

    zimmer = get_cache (Zimmer, {"zinr": [(eq, r_zinr)]})
    t_zimmer = T_zimmer()
    t_zimmer_list.append(t_zimmer)

    buffer_copy(zimmer, t_zimmer)

    return generate_output()