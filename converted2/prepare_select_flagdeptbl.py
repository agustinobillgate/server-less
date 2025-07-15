#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def prepare_select_flagdeptbl(inp_dept:string):

    prepare_cache ([Queasy])

    dept_list_data = []
    queasy = None

    dept_list = None

    dept_list_data, Dept_list = create_model("Dept_list", {"deptnr":int, "bezeich":string, "select_flag":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal dept_list_data, queasy
        nonlocal inp_dept


        nonlocal dept_list
        nonlocal dept_list_data

        return {"dept-list": dept_list_data}

    def create_list():

        nonlocal dept_list_data, queasy
        nonlocal inp_dept


        nonlocal dept_list
        nonlocal dept_list_data

        curr_i:int = 0
        mesvalue:string = ""

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 19)).order_by(Queasy.number1).all():
            dept_list = Dept_list()
            dept_list_data.append(dept_list)

            dept_list.deptnr = queasy.number1
            dept_list.bezeich = queasy.char3


        for curr_i in range(1,num_entries(inp_dept, ",")  + 1) :
            mesvalue = entry(curr_i - 1, inp_dept, ",")

            if mesvalue != "":

                dept_list = query(dept_list_data, filters=(lambda dept_list: dept_list.deptnr == to_int(mesvalue)), first=True)

                if dept_list:
                    dept_list.select_flag = True

    create_list()

    return generate_output()