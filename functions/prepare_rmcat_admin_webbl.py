#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Zimkateg, Queasy

def prepare_rmcat_admin_webbl():

    prepare_cache ([Queasy])

    t_zimkateg_data = []
    t_queasy_data = []
    zimkateg = queasy = None

    t_zimkateg = t_queasy = pqueasy = None

    t_zimkateg_data, T_zimkateg = create_model_like(Zimkateg, {"priority":int, "max_avail":int})
    t_queasy_data, T_queasy = create_model_like(Queasy)

    Pqueasy = create_buffer("Pqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_zimkateg_data, t_queasy_data, zimkateg, queasy
        nonlocal pqueasy


        nonlocal t_zimkateg, t_queasy, pqueasy
        nonlocal t_zimkateg_data, t_queasy_data

        return {"t-zimkateg": t_zimkateg_data, "t-queasy": t_queasy_data}


    for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
        t_zimkateg = T_zimkateg()
        t_zimkateg_data.append(t_zimkateg)

        buffer_copy(zimkateg, t_zimkateg)

        pqueasy = get_cache (Queasy, {"key": [(eq, 325)],"number1": [(eq, zimkateg.zikatnr)]})

        if pqueasy:
            t_zimkateg.priority = pqueasy.number2
            t_zimkateg.max_avail = pqueasy.number3

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 152)).order_by(Queasy.number1).all():
        t_queasy = T_queasy()
        t_queasy_data.append(t_queasy)

        buffer_copy(queasy, t_queasy)

    return generate_output()