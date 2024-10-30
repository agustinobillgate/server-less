from functions.additional_functions import *
import decimal
from models import Queasy, Gl_acct

def gl_recurracctbl():
    b1_list_list = []
    queasy = gl_acct = None

    b1_list = None

    b1_list_list, B1_list = create_model_like(Queasy, {"fibukonto":str, "bezeich":str, "rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal b1_list_list, queasy, gl_acct


        nonlocal b1_list
        nonlocal b1_list_list

        return {"b1-list": b1_list_list}

    queasy_obj_list = []
    for queasy, gl_acct in db_session.query(Queasy, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Queasy.char3)).filter(
             (Queasy.key == 106)).order_by(Queasy.char1, Gl_acct.fibukonto).all():
        if queasy._recid in queasy_obj_list:
            continue
        else:
            queasy_obj_list.append(queasy._recid)


        b1_list = B1_list()
        b1_list_list.append(b1_list)

        buffer_copy(queasy, b1_list)
        b1_list.rec_id = queasy._recid
        b1_list.fibukonto = gl_acct.fibukonto
        b1_list.bezeich = gl_acct.bezeich

    return generate_output()