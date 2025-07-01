#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Hoteldpt

def check_dept_limitbl():

    prepare_cache ([Htparam])

    dept_limit = 0
    curr_anz = 0
    htparam = hoteldpt = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal dept_limit, curr_anz, htparam, hoteldpt

        return {"dept_limit": dept_limit, "curr_anz": curr_anz}

    def check_dept_limit():

        nonlocal dept_limit, curr_anz, htparam, hoteldpt

        htparam = get_cache (Htparam, {"paramnr": [(eq, 989)]})

        if htparam.finteger > 0:
            dept_limit = htparam.finteger
        curr_anz = -1

        for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
            curr_anz = curr_anz + 1


    check_dept_limit()

    return generate_output()