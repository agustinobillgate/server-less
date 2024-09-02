from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Zimmer, Paramtext

def mk_resline_check_bedsetup1bl(r_zinr:str):
    curr_setup = ""
    t_zimmer_list = []
    zimmer = paramtext = None

    t_zimmer = None

    t_zimmer_list, T_zimmer = create_model_like(Zimmer)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_setup, t_zimmer_list, zimmer, paramtext


        nonlocal t_zimmer
        nonlocal t_zimmer_list
        return {"curr_setup": curr_setup, "t-zimmer": t_zimmer_list}

    zimmer = db_session.query(Zimmer).filter(
            (func.lower(Zimmer.zinr) == (r_zinr).lower())).first()

    if zimmer.setup != 0:

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == (9200 + zimmer.setup))).first()
        curr_setup = substring(paramtext.notes, 0, 1)
    else:
        curr_setup = ""
    t_zimmer = T_zimmer()
    t_zimmer_list.append(t_zimmer)

    buffer_copy(zimmer, t_zimmer)

    return generate_output()