#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def prepare_select_prcodebl():
    tqueasy_list = []
    queasy = None

    tqueasy = None

    tqueasy_list, Tqueasy = create_model_like(Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tqueasy_list, queasy


        nonlocal tqueasy
        nonlocal tqueasy_list

        return {"tqueasy": tqueasy_list}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 2)).order_by(Queasy.char1).all():
        tqueasy = Tqueasy()
        tqueasy_list.append(tqueasy)

        buffer_copy(queasy, tqueasy)

    return generate_output()