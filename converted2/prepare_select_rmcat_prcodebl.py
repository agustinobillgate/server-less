#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Zimkateg, Ratecode

def prepare_select_rmcat_prcodebl(rmcat:string):

    prepare_cache ([Zimkateg])

    t_queasy_data = []
    create_it:bool = False
    z_zikatnr:int = 0
    queasy = zimkateg = ratecode = None

    t_queasy = None

    t_queasy_data, T_queasy = create_model_like(Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_data, create_it, z_zikatnr, queasy, zimkateg, ratecode
        nonlocal rmcat


        nonlocal t_queasy
        nonlocal t_queasy_data

        return {"t-queasy": t_queasy_data}

    zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, rmcat)]})

    if zimkateg:
        z_zikatnr = zimkateg.zikatnr
    else:
        create_it = True

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 2) & not_ (Queasy.logi2)).order_by(Queasy.char1).all():

        ratecode = get_cache (Ratecode, {"code": [(eq, queasy.char1)],"zikatnr": [(eq, z_zikatnr)]})

        if ratecode or create_it:
            t_queasy = T_queasy()
            t_queasy_data.append(t_queasy)

            buffer_copy(queasy, t_queasy)

    return generate_output()