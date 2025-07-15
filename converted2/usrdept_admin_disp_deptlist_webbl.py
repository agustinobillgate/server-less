#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

t_queasy_data, T_queasy = create_model_like(Queasy, {"comp_name":string})

def usrdept_admin_disp_deptlist_webbl(t_queasy_data:[T_queasy]):
    dept_list_data = []
    queasy = None

    t_queasy = dept_list = None

    dept_list_data, Dept_list = create_model("Dept_list", {"nr":int, "dept":string, "selected":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal dept_list_data, queasy


        nonlocal t_queasy, dept_list
        nonlocal dept_list_data

        return {"dept-list": dept_list_data}

    def create_dptlist():

        nonlocal dept_list_data, queasy


        nonlocal t_queasy, dept_list
        nonlocal dept_list_data

        i:int = 0

        for t_queasy in query(t_queasy_data):
            dept_list = Dept_list()
            dept_list_data.append(dept_list)

            dept_list.nr = t_queasy.number1
            dept_list.dept = t_queasy.char3
            dept_list.selected = False

        for t_queasy in query(t_queasy_data, filters=(lambda t_queasy: t_queasy.char2 != "")):
            for i in range(1,num_entries(t_queasy.char2, ";")  + 1) :

                dept_list = query(dept_list_data, filters=(lambda dept_list: dept_list.nr == to_int(entry(i - 1, t_queasy.char2, ";"))), first=True)

                if dept_list:
                    dept_list.selected = True


    create_dptlist()

    return generate_output()