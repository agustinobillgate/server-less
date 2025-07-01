#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Hoteldpt, Htparam

def prepare_setup_departbl():

    prepare_cache ([Htparam])

    max_dept = 0
    dept_list_list = []
    hoteldpt = htparam = None

    dept_list = None

    dept_list_list, Dept_list = create_model_like(Hoteldpt, {"dpttype":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal max_dept, dept_list_list, hoteldpt, htparam


        nonlocal dept_list
        nonlocal dept_list_list

        return {"max_dept": max_dept, "dept-list": dept_list_list}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 989)]})

    if htparam:
        max_dept = htparam.finteger + 1

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
        dept_list = Dept_list()
        dept_list_list.append(dept_list)

        buffer_copy(hoteldpt, dept_list)

    return generate_output()