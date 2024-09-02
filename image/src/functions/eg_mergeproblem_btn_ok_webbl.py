from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Eg_request, Eg_subtask

def eg_mergeproblem_btn_ok_webbl(rec_id:int, maintask_nr:int, sub_code:str, maintask_nr2:int, sub_code2:str, bezeich:str):
    success_flag = False
    eg_request = eg_subtask = None

    buf_eg_request = None

    Buf_eg_request = Eg_request

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, eg_request, eg_subtask
        nonlocal buf_eg_request


        nonlocal buf_eg_request
        return {"success_flag": success_flag}


    eg_subtask = db_session.query(Eg_subtask).filter(
            (Eg_subtask._recid == rec_id)).first()

    if not eg_subtask:
        success_flag = False
    else:

        for eg_request in db_session.query(Eg_request).all():

            buf_eg_request = db_session.query(Buf_eg_request).filter(
                    (Buf_eg_request.reqnr == eg_request.reqnr) &  (Buf_eg_request.maintask == maintask_nr) &  (func.lower(Buf_eg_request.sub_task) == (sub_code).lower())).first()

            if buf_eg_request:

                buf_eg_request = db_session.query(Buf_eg_request).first()
                buf_eg_request.maintask = maintask_nr2
                buf_eg_request.sub_task = sub_code2
                buf_eg_request.subtask_bezeich = bezeich

                buf_eg_request = db_session.query(Buf_eg_request).first()

                success_flag = True

        eg_subtask = db_session.query(Eg_subtask).first()
        db_session.delete(eg_subtask)

        success_flag = True

    return generate_output()