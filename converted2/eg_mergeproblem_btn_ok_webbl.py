#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_request, Eg_subtask

def eg_mergeproblem_btn_ok_webbl(rec_id:int, maintask_nr:int, sub_code:string, maintask_nr2:int, sub_code2:string, bezeich:string):

    prepare_cache ([Eg_request])

    success_flag = False
    eg_request = eg_subtask = None

    buf_eg_request = None

    Buf_eg_request = create_buffer("Buf_eg_request",Eg_request)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, eg_request, eg_subtask
        nonlocal rec_id, maintask_nr, sub_code, maintask_nr2, sub_code2, bezeich
        nonlocal buf_eg_request


        nonlocal buf_eg_request

        return {"success_flag": success_flag}


    eg_subtask = get_cache (Eg_subtask, {"_recid": [(eq, rec_id)]})

    if not eg_subtask:
        success_flag = False
    else:

        for eg_request in db_session.query(Eg_request).order_by(Eg_request._recid).all():

            buf_eg_request = get_cache (Eg_request, {"reqnr": [(eq, eg_request.reqnr)],"maintask": [(eq, maintask_nr)],"sub_task": [(eq, sub_code)]})

            if buf_eg_request:
                pass
                buf_eg_request.maintask = maintask_nr2
                buf_eg_request.sub_task = sub_code2
                buf_eg_request.subtask_bezeich = bezeich


                pass
                pass
                success_flag = True
        pass
        db_session.delete(eg_subtask)
        pass
        success_flag = True

    return generate_output()