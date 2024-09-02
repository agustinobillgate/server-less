from functions.additional_functions import *
import decimal
from models import Queasy

def usrdept_admin_disp_deptlist_webbl(t_queasy:[T_queasy]):
    dept_list_list = []
    queasy = None

    t_queasy = dept_list = None

    t_queasy_list, T_queasy = create_model_like(Queasy, {"comp_name":str})
    dept_list_list, Dept_list = create_model("Dept_list", {"nr":int, "dept":str, "selected":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal dept_list_list, queasy


        nonlocal t_queasy, dept_list
        nonlocal t_queasy_list, dept_list_list
        return {"dept-list": dept_list_list}

    def create_dptlist():

        nonlocal dept_list_list, queasy


        nonlocal t_queasy, dept_list
        nonlocal t_queasy_list, dept_list_list

        i:int = 0

        for t_queasy in query(t_queasy_list):
            dept_list = Dept_list()
            dept_list_list.append(dept_list)

            dept_list.nr = t_queasy.number1
            dept_list.dept = t_queasy.char3
            dept_list.SELECTED = False

        for t_queasy in query(t_queasy_list, filters=(lambda t_queasy :t_queasy.char2 != "")):
            for i in range(1,num_entries(t_queasy.char2, ";")  + 1) :

                dept_list = query(dept_list_list, filters=(lambda dept_list :dept_list.nr == to_int(entry(i - 1, t_queasy.char2, ";"))), first=True)

                if dept_list:
                    dept_list.SELECTED = True

    create_dptlist()

    return generate_output()