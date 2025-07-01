#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Gl_acct

def gl_recurracctbl():

    prepare_cache ([Gl_acct])

    b1_list_list = []
    queasy = gl_acct = None

    b1_list = None

    b1_list_list, B1_list = create_model_like(Queasy, {"fibukonto":string, "bezeich":string, "rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal b1_list_list, queasy, gl_acct


        nonlocal b1_list
        nonlocal b1_list_list

        return {"b1-list": b1_list_list}

    queasy_obj_list = {}
    for queasy, gl_acct in db_session.query(Queasy, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Queasy.char3)).filter(
             (Queasy.key == 106)).order_by(Queasy.char1, Gl_acct.fibukonto).all():
        if queasy_obj_list.get(queasy._recid):
            continue
        else:
            queasy_obj_list[queasy._recid] = True


        b1_list = B1_list()
        b1_list_list.append(b1_list)

        buffer_copy(queasy, b1_list)
        b1_list.rec_id = queasy._recid
        b1_list.fibukonto = gl_acct.fibukonto
        b1_list.bezeich = gl_acct.bezeich

    return generate_output()