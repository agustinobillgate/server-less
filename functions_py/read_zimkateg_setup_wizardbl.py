#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 09-10-2025
# Tiket ID : 8CF423 | Recompile Program
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Zimkateg

input_param_data, Input_param = create_model("Input_param", {"case_type":int, "zikatno":int, "shortbez":string})

def read_zimkateg_setup_wizardbl(input_param_data:[Input_param]):

    prepare_cache ([Zimkateg])

    t_zimkateg_data = []
    zimkateg = None

    t_zimkateg = input_param = None

    t_zimkateg_data, T_zimkateg = create_model("T_zimkateg", {"zikatnr":int, "kurzbez":string, "bezeichnung":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_zimkateg_data, zimkateg


        nonlocal t_zimkateg, input_param
        nonlocal t_zimkateg_data

        return {"t-zimkateg": t_zimkateg_data}


    input_param = query(input_param_data, first=True)

    if input_param.case_type == 1:

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
            t_zimkateg = T_zimkateg()
            t_zimkateg_data.append(t_zimkateg)

            zimkateg.zikatnr = t_zimkateg.zikatnr
            zimkateg.kurzbez = t_zimkateg.kurzbez
            zimkateg.bezeichnung = t_zimkateg.bezeichnung

    return generate_output()