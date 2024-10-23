from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy, Gl_acct

def gl_recurracct_btn_exitbl(pvilanguage:int, case_type:int, titel:str, remark:str, fibu:str, rec_id:int):
    msg_str = ""
    b1_list_list = []
    lvcarea:str = "gl-recurracct"
    queasy = gl_acct = None

    b1_list = gl_acc1 = None

    b1_list_list, B1_list = create_model_like(Queasy, {"fibukonto":str, "bezeich":str, "rec_id":int})

    Gl_acc1 = create_buffer("Gl_acc1",Gl_acct)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, b1_list_list, lvcarea, queasy, gl_acct
        nonlocal pvilanguage, case_type, titel, remark, fibu, rec_id
        nonlocal gl_acc1


        nonlocal b1_list, gl_acc1
        nonlocal b1_list_list
        return {"msg_str": msg_str, "b1-list": b1_list_list}

    def fill_queasy():

        nonlocal msg_str, b1_list_list, lvcarea, queasy, gl_acct
        nonlocal pvilanguage, case_type, titel, remark, fibu, rec_id
        nonlocal gl_acc1


        nonlocal b1_list, gl_acc1
        nonlocal b1_list_list


        queasy.key = 106
        queasy.char1 = titel
        queasy.char2 = remark
        queasy.char3 = fibu


    def disp_it():

        nonlocal msg_str, b1_list_list, lvcarea, queasy, gl_acct
        nonlocal pvilanguage, case_type, titel, remark, fibu, rec_id
        nonlocal gl_acc1


        nonlocal b1_list, gl_acc1
        nonlocal b1_list_list

        if queasy:

            gl_acct = db_session.query(Gl_acct).filter(
                     (Gl_acct.fibukonto == queasy.char3)).first()
            b1_list = B1_list()
            b1_list_list.append(b1_list)

            buffer_copy(queasy, b1_list)
            b1_list.rec_id = queasy._recid
            b1_list.fibukonto = gl_acct.fibukonto
            b1_list.bezeich = gl_acct.bezeich


    if case_type == 1:

        gl_acc1 = db_session.query(Gl_acc1).filter(
                 (func.lower(Gl_acc1.fibukonto) == (fibu).lower())).first()

        if not gl_acc1:
            msg_str = msg_str + chr(2) + translateExtended ("No such G/L Account number.", lvcarea, "")

            return generate_output()
        else:
            queasy = Queasy()
            db_session.add(queasy)

            fill_queasy()
            disp_it()

            return generate_output()

    elif case_type == 2:

        gl_acc1 = db_session.query(Gl_acc1).filter(
                 (func.lower(Gl_acc1.fibukonto) == (fibu).lower())).first()

        if not gl_acc1:

            return generate_output()
        else:

            queasy = db_session.query(Queasy).filter(
                     (Queasy._recid == rec_id)).first()

            if queasy:
                fill_queasy()
            disp_it()

            return generate_output()