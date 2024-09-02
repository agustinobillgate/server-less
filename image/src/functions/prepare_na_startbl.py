from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Nation

def prepare_na_startbl():
    def_natcode = ""
    na_date = None
    na_time = 0
    na_name = ""
    htparam = nation = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal def_natcode, na_date, na_time, na_name, htparam, nation


        return {"def_natcode": def_natcode, "na_date": na_date, "na_time": na_time, "na_name": na_name}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 276)).first()

    nation = db_session.query(Nation).filter(
            (Nation.kurzbez == htparam.fchar)).first()

    if nation:
        def_natcode = nation.kurzbez

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 102)).first()
    na_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 103)).first()
    na_time = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 253)).first()
    na_name = htparam.fchar

    return generate_output()