#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def prepare_select_prcodebl():
    tqueasy_data = []
    queasy = None

    tqueasy = None

    tqueasy_data, Tqueasy = create_model_like(Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tqueasy_data, queasy


        nonlocal tqueasy
        nonlocal tqueasy_data

        return {"tqueasy1": tqueasy_data}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 2)).order_by(Queasy.char1).all():
        tqueasy = Tqueasy()
        tqueasy_data.append(tqueasy)

        buffer_copy(queasy, tqueasy)

    return generate_output()