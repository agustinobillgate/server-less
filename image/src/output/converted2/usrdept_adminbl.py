#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Guest

def usrdept_adminbl():

    prepare_cache ([Guest])

    t_queasy_list = []
    queasy = guest = None

    t_queasy = gbuff = None

    t_queasy_list, T_queasy = create_model_like(Queasy, {"comp_name":string})

    Gbuff = create_buffer("Gbuff",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_list, queasy, guest
        nonlocal gbuff


        nonlocal t_queasy, gbuff
        nonlocal t_queasy_list

        return {"t-queasy": t_queasy_list}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 19)).order_by(Queasy._recid).all():
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        buffer_copy(queasy, t_queasy)

        gbuff = get_cache (Guest, {"gastnr": [(eq, queasy.number2)]})

        if gbuff:
            t_queasy.comp_name = gbuff.name + " " + gbuff.anredefirma
        else:
            t_queasy.comp_name = ""

    return generate_output()