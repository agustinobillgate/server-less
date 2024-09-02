from functions.additional_functions import *
import decimal
from models import Queasy

def enter_passwd_delete_queasybl(case_type:int, q_recid:int):
    queasy = None

    qsy = None

    Qsy = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal qsy


        nonlocal qsy
        return {}


    if case_type == 1:

        qsy = db_session.query(Qsy).filter(
                (Qsy._recid == q_recid)).first()
        db_session.delete(qsy)


    return generate_output()