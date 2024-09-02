from functions.additional_functions import *
import decimal
from models import Hoteldpt, Htparam

def prepare_setup_departbl():
    max_dept = 0
    dept_list_list = []
    hoteldpt = htparam = None

    dept_list = None

    dept_list_list, Dept_list = create_model_like(Hoteldpt, {"dpttype":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal max_dept, dept_list_list, hoteldpt, htparam


        nonlocal dept_list
        nonlocal dept_list_list
        return {"max_dept": max_dept, "dept-list": dept_list_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 989)).first()

    if htparam:
        max_dept = htparam.finteger + 1

    for hoteldpt in db_session.query(Hoteldpt).all():
        dept_list = Dept_list()
        dept_list_list.append(dept_list)

        buffer_copy(hoteldpt, dept_list)

    return generate_output()