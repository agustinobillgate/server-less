from functions.additional_functions import *
import decimal
from models import Queasy

def prepare_select_flagdeptbl(inp_dept:str):
    dept_list_list = []
    queasy = None

    dept_list = None

    dept_list_list, Dept_list = create_model("Dept_list", {"deptnr":int, "bezeich":str, "select_flag":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal dept_list_list, queasy
        nonlocal inp_dept


        nonlocal dept_list
        nonlocal dept_list_list
        return {"dept-list": dept_list_list}

    def create_list():

        nonlocal dept_list_list, queasy
        nonlocal inp_dept


        nonlocal dept_list
        nonlocal dept_list_list

        curr_i:int = 0
        mesvalue:str = ""

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 19)).order_by(Queasy.number1).all():
            dept_list = Dept_list()
            dept_list_list.append(dept_list)

            dept_list.deptnr = queasy.number1
            dept_list.bezeich = queasy.char3


        for curr_i in range(1,num_entries(inp_dept, ",")  + 1) :
            mesvalue = entry(curr_i - 1, inp_dept, ",")

            if mesvalue != "":

                dept_list = query(dept_list_list, filters=(lambda dept_list: dept_list.deptnr == to_int(mesvalue)), first=True)

                if dept_list:
                    dept_list.select_flag = True

    create_list()

    return generate_output()