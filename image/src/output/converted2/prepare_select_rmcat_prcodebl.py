#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Zimkateg, Ratecode

def prepare_select_rmcat_prcodebl(rmcat:string):
    t_queasy_list = []
    create_it:bool = False
    queasy = zimkateg = ratecode = None

    t_queasy = None

    t_queasy_list, T_queasy = create_model_like(Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_list, create_it, queasy, zimkateg, ratecode
        nonlocal rmcat


        nonlocal t_queasy
        nonlocal t_queasy_list

        return {"t-queasy": t_queasy_list}

    zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, rmcat)]})
    create_it = not None != zimkateg

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 2) & not_ (Queasy.logi2)).order_by(Queasy.char1).all():

        ratecode = get_cache (Ratecode, {"code": [(eq, queasy.char1)],"zikatnr": [(eq, zimkateg.zikatnr)]})

        if ratecode or create_it:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)

    return generate_output()