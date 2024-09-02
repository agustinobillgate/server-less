from functions.additional_functions import *
import decimal
from models import H_compli

def ktrans_report_btn_del_1bl(c_list_s_recid:int):
    successflag = False
    h_compli = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, h_compli


        return {"successflag": successflag}


    h_compli = db_session.query(H_compli).filter(
            (H_compli._recid == c_list_s_recid)).first()

    if h_compli:
        db_session.delete(h_compli)
        successflag = True


    else:
        successflag = False

    return generate_output()