#using conversion tools version: 1.0.0.117
#-------------------------------------------
# Rd, 26/11/2025, with_for_update
#-------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Zimmer

t_zimmer_data, T_zimmer = create_model_like(Zimmer)

def write_zimmerbl(t_zimmer_data:[T_zimmer]):
    success_flag = False
    zimmer = None

    t_zimmer = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, zimmer


        nonlocal t_zimmer

        return {"success_flag": success_flag}

    t_zimmer = query(t_zimmer_data, first=True)

    if t_zimmer:

        zimmer = get_cache (Zimmer, {"zinr": [(eq, t_zimmer.zinr)]})

        if zimmer:
            buffer_copy(t_zimmer, zimmer)
            pass
            success_flag = True

    return generate_output()