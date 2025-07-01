#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import Queasy

def prepare_grphtl_adminbl():
    t_queasy_list = []
    queasy = None

    t_queasy = queasy1 = None

    t_queasy_list, T_queasy = create_model_like(Queasy, {"rec_id":int})

    Queasy1 = create_buffer("Queasy1",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_list, queasy
        nonlocal queasy1


        nonlocal t_queasy, queasy1
        nonlocal t_queasy_list

        return {"t-queasy": t_queasy_list}

    def check_queasy136():

        nonlocal t_queasy_list, queasy
        nonlocal queasy1


        nonlocal t_queasy, queasy1
        nonlocal t_queasy_list

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 136) & (not_(matches(Queasy.char1,("*:*"))))).first()
        while None != queasy:

            queasy1 = db_session.query(Queasy1).filter(
                         (Queasy1._recid == queasy._recid)).first()
            queasy.char1 = queasy.char2 + ":" + queasy.char1
            queasy.char2 = ""


            pass
            pass

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 136) & (not_(matches(Queasy.char1,("*:*")))) & (Queasy._recid > curr_recid)).first()

    check_queasy136()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 136)).order_by(Queasy.number1).all():
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        buffer_copy(queasy, t_queasy)
        t_queasy.rec_id = queasy._recid

    return generate_output()