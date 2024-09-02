from functions.additional_functions import *
import decimal
from models import Res_history

def res_log_res_commentbl(his_recid:int):
    res_com = ""
    res_history = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_com, res_history


        return {"res_com": res_com}


    res_history = db_session.query(Res_history).filter(
            (Res_history._recid == his_recid)).first()
    res_com = res_history.aenderung

    return generate_output()