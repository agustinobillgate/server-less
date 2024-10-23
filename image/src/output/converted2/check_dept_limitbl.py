from functions.additional_functions import *
import decimal
from models import Htparam, Hoteldpt

def check_dept_limitbl():
    dept_limit = 0
    curr_anz = 0
    htparam = hoteldpt = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal dept_limit, curr_anz, htparam, hoteldpt


        return {"dept_limit": dept_limit, "curr_anz": curr_anz}

    def check_dept_limit():

        nonlocal dept_limit, curr_anz, htparam, hoteldpt

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 989)).first()

        if htparam.finteger > 0:
            dept_limit = htparam.finteger
        curr_anz = -1

        for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
            curr_anz = curr_anz + 1


    check_dept_limit()

    return generate_output()