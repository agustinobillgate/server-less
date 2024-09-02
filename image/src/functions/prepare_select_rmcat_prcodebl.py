from functions.additional_functions import *
import decimal
from models import Queasy, Zimkateg, Ratecode

def prepare_select_rmcat_prcodebl(rmcat:str):
    t_queasy_list = []
    create_it:bool = False
    queasy = zimkateg = ratecode = None

    t_queasy = None

    t_queasy_list, T_queasy = create_model_like(Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_list, create_it, queasy, zimkateg, ratecode


        nonlocal t_queasy
        nonlocal t_queasy_list
        return {"t-queasy": t_queasy_list}

    zimkateg = db_session.query(Zimkateg).filter(
            (Zimkateg.kurzbez == rmcat)).first()
    create_it = not None != zimkateg

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 2) &  (not Queasy.logi2)).all():

        ratecode = db_session.query(Ratecode).filter(
                (Ratecode.CODE == queasy.char1) &  (Ratecode.zikatnr == zimkateg.zikatnr)).first()

        if ratecode or create_it:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)

    return generate_output()