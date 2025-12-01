#using conversion tools version: 1.0.0.117
#-------------------------------------------
# Rd, 26/11/2025, with_for_update
#-------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def enter_passwd_delete_queasybl(case_type:int, q_recid:int):
    queasy = None

    qsy = None

    Qsy = create_buffer("Qsy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal case_type, q_recid
        nonlocal qsy


        nonlocal qsy

        return {}


    if case_type == 1:

        qsy = db_session.query(Qsy).filter(
                 (Qsy._recid == q_recid)).with_for_update().first()
        db_session.delete(qsy)
        pass

    return generate_output()