from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Waehrung

def prepare_ldry_complibl():
    billdate = None
    from_dept = 0
    double_currency = False
    foreign_nr = 0
    exchg_rate = 0
    htparam = waehrung = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, from_dept, double_currency, foreign_nr, exchg_rate, htparam, waehrung


        return {"billdate": billdate, "from_dept": from_dept, "double_currency": double_currency, "foreign_nr": foreign_nr, "exchg_rate": exchg_rate}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    billdate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1081)).first()
    from_dept = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()

    if htparam.flogical:
        double_currency = True

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            foreign_nr = waehrungsnr
            exchg_rate = waehrung.ankauf / waehrung.einheit
        else:
            exchg_rate = 1

    return generate_output()