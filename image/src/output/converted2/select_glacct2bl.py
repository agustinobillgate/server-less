#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct, Queasy

def select_glacct2bl():

    prepare_cache ([Gl_acct])

    q1_list_list = []
    gl_acct = queasy = None

    q1_list = gl_acct2 = None

    q1_list_list, Q1_list = create_model("Q1_list", {"fibukonto":string, "bezeich":string, "fibukonto2":string})

    Gl_acct2 = create_buffer("Gl_acct2",Gl_acct)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_list, gl_acct, queasy
        nonlocal gl_acct2


        nonlocal q1_list, gl_acct2
        nonlocal q1_list_list

        return {"q1-list": q1_list_list}

    def assign_it():

        nonlocal q1_list_list, gl_acct, queasy
        nonlocal gl_acct2


        nonlocal q1_list, gl_acct2
        nonlocal q1_list_list


        q1_list = Q1_list()
        q1_list_list.append(q1_list)

        q1_list.fibukonto = gl_acct.fibukonto
        q1_list.bezeich = gl_acct.bezeich
        q1_list.fibukonto2 = gl_acct.fibukonto


    queasy_obj_list = {}
    for queasy, gl_acct, gl_acct2 in db_session.query(Queasy, Gl_acct, Gl_acct2).join(Gl_acct,(Gl_acct.fibukonto == Queasy.char1) & (Gl_acct.activeflag)).join(Gl_acct2,(Gl_acct2.fibukonto == Queasy.char2) & (Gl_acct2.activeflag)).filter(
             (Queasy.key == 108)).order_by(Gl_acct.fibukonto).all():
        if queasy_obj_list.get(queasy._recid):
            continue
        else:
            queasy_obj_list[queasy._recid] = True


        assign_it()

    return generate_output()