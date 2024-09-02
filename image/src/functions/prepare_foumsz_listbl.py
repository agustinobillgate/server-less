from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Hoteldpt

def prepare_foumsz_listbl():
    to_date = None
    vat_artnr = 0
    vat_str = ""
    deptname1 = ""
    serv_artnr = 0
    to_dept = 0
    deptname2 = ""
    price_decimal = 0
    htparam = hoteldpt = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal to_date, vat_artnr, vat_str, deptname1, serv_artnr, to_dept, deptname2, price_decimal, htparam, hoteldpt


        return {"to_date": to_date, "vat_artnr": vat_artnr, "vat_str": vat_str, "deptname1": deptname1, "serv_artnr": serv_artnr, "to_dept": to_dept, "deptname2": deptname2, "price_decimal": price_decimal}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    to_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 132)).first()
    vat_artnr = htparam.finteger
    vat_str = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 133)).first()
    serv_artnr = htparam.finteger

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == 0)).first()
    deptname1 = hoteldpt.depart

    for hoteldpt in db_session.query(Hoteldpt).all():

        if to_dept < hoteldpt.num:
            to_dept = hoteldpt.num
            deptname2 = hoteldpt.depart

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    return generate_output()