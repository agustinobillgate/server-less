from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Zimkateg

def mk_resline_reslin_list_zinr3bl(zikatstr:str):
    t_zimkateg_list = []
    zimkateg = None

    t_zimkateg = None

    t_zimkateg_list, T_zimkateg = create_model_like(Zimkateg)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_zimkateg_list, zimkateg


        nonlocal t_zimkateg
        nonlocal t_zimkateg_list
        return {"t-zimkateg": t_zimkateg_list}

    zimkateg = db_session.query(Zimkateg).filter(
            (func.lower(Zimkateg.kurzbez) == (zikatstr).lower())).first()
    t_zimkateg = T_zimkateg()
    t_zimkateg_list.append(t_zimkateg)

    buffer_copy(zimkateg, t_zimkateg)

    return generate_output()