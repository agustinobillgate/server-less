#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Hoteldpt

def prepare_foumsz_listbl():

    prepare_cache ([Htparam, Hoteldpt])

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


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    to_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 132)]})
    vat_artnr = htparam.finteger
    vat_str = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 133)]})
    serv_artnr = htparam.finteger

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, 0)]})
    deptname1 = hoteldpt.depart

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():

        if to_dept < hoteldpt.num:
            to_dept = hoteldpt.num
            deptname2 = hoteldpt.depart

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    return generate_output()