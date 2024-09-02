from functions.additional_functions import *
import decimal
from datetime import date
from models import Outorder

def read_outorderbl(case_type:int, rmno:str, resno:int, ci_date:date, to_date:date):
    t_outorder_list = []
    outorder = None

    t_outorder = None

    t_outorder_list, T_outorder = create_model_like(Outorder)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_outorder_list, outorder


        nonlocal t_outorder
        nonlocal t_outorder_list
        return {"t-outorder": t_outorder_list}

    if case_type == 1:

        outorder = db_session.query(Outorder).filter(
                (Outorder.zinr == rmno) &  (Outorder.betriebsnr == resno)).first()
    elif case_type == 2:

        outorder = db_session.query(Outorder).filter(
                (Outorder.zinr == rmno)).first()
    elif case_type == 3:

        outorder = db_session.query(Outorder).filter(
                (Outorder.zinr == rmno) &  (Outorder.gespstart >= ci_date) &  (Outorder.gespende <= ci_date)).first()
    elif case_type == 4:

        outorder = db_session.query(Outorder).filter(
                (Outorder.zinr == rmno) &  (Outorder.gespende >= ci_date)).first()
    elif case_type == 5:

        outorder = db_session.query(Outorder).filter(
                (Outorder._recid == resno)).first()
    elif case_type == 6:

        outorder = db_session.query(Outorder).filter(
                (Outorder.zinr == rmno) &  (Outorder.gespstart <= ci_date) &  (Outorder.gespende >= ci_date) &  (Outorder.betriebsnr <= 1)).first()
    elif case_type == 7:

        outorder = db_session.query(Outorder).filter(
                (Outorder.zinr == rmno) &  (Outorder.betriebsnr == resno) &  (Outorder.gespstart > to_date) &  (Outorder.gespende < ci_date)).first()
    elif case_type == 99:

        outorder = db_session.query(Outorder).filter(
                (Outorder.zinr == rmno) &  (Outorder.betriebsnr == resno)).first()

    if outorder:
        t_outorder = T_outorder()
        t_outorder_list.append(t_outorder)

        buffer_copy(outorder, t_outorder)

    return generate_output()