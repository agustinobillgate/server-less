#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Zimmer, Paramtext

def mk_resline_check_bedsetup1bl(r_zinr:string):

    prepare_cache ([Paramtext])

    curr_setup = ""
    t_zimmer_data = []
    zimmer = paramtext = None

    t_zimmer = None

    t_zimmer_data, T_zimmer = create_model_like(Zimmer)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_setup, t_zimmer_data, zimmer, paramtext
        nonlocal r_zinr


        nonlocal t_zimmer
        nonlocal t_zimmer_data

        return {"curr_setup": curr_setup, "t-zimmer": t_zimmer_data}

    zimmer = get_cache (Zimmer, {"zinr": [(eq, r_zinr)]})

    if zimmer.setup != 0:

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, (9200 + zimmer.setup))]})
        curr_setup = substring(paramtext.notes, 0, 1)
    else:
        curr_setup = ""
    t_zimmer = T_zimmer()
    t_zimmer_data.append(t_zimmer)

    buffer_copy(zimmer, t_zimmer)

    return generate_output()