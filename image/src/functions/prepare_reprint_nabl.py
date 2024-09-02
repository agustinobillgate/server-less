from functions.additional_functions import *
import decimal
from datetime import date
from functions.reprint_nabl import reprint_nabl
from models import Htparam

def prepare_reprint_nabl():
    store_flag = False
    na_date = None
    na_time = 0
    na_name = ""
    b1_list_list = []
    htparam = None

    b1_list = None

    b1_list_list, B1_list = create_model("B1_list", {"reihenfolge":int, "hogarest":int, "bezeichnun":str, "rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal store_flag, na_date, na_time, na_name, b1_list_list, htparam


        nonlocal b1_list
        nonlocal b1_list_list
        return {"store_flag": store_flag, "na_date": na_date, "na_time": na_time, "na_name": na_name, "b1-list": b1_list_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 230)).first()

    if htparam.feldtyp == 4 and htparam.flogical:
        store_flag = True

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    na_date = htparam.fdate - 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 103)).first()
    na_time = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 253)).first()
    na_name = htparam.fchar
    b1_list_list = get_output(reprint_nabl())

    return generate_output()