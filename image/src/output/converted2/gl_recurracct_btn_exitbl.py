#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Gl_acct

def gl_recurracct_btn_exitbl(pvilanguage:int, case_type:int, titel:string, remark:string, fibu:string, rec_id:int):

    prepare_cache ([Gl_acct])

    msg_str = ""
    b1_list_list = []
    lvcarea:string = "gl-recurracct"
    queasy = gl_acct = None

    b1_list = gl_acc1 = None

    b1_list_list, B1_list = create_model_like(Queasy, {"fibukonto":string, "bezeich":string, "rec_id":int})

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


        pass

        if queasy:

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, queasy.char3)]})
            b1_list = B1_list()
            b1_list_list.append(b1_list)

            buffer_copy(queasy, b1_list)
            b1_list.rec_id = queasy._recid
            b1_list.fibukonto = gl_acct.fibukonto
            b1_list.bezeich = gl_acct.bezeich


    if case_type == 1:

        gl_acc1 = get_cache (Gl_acct, {"fibukonto": [(eq, fibu)]})

        if not gl_acc1:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("No such G/L Account number.", lvcarea, "")

            return generate_output()
        else:
            queasy = Queasy()
            db_session.add(queasy)

            fill_queasy()
            disp_it()

            return generate_output()

    elif case_type == 2:

        gl_acc1 = get_cache (Gl_acct, {"fibukonto": [(eq, fibu)]})

        if not gl_acc1:

            return generate_output()
        else:

            queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})

            if queasy:
                fill_queasy()
            pass
            disp_it()

            return generate_output()

    return generate_output()