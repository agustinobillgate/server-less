from functions.additional_functions import *
import decimal
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
            (Queasy.key == 2)).all():
        tqueasy = Tqueasy()
        tqueasy_list.append(tqueasy)

        buffer_copy(queasy, tqueasy)

    return generate_output()