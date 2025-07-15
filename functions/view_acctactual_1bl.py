#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct

def view_acctactual_1bl(fibukonto:string):

    prepare_cache ([Gl_acct])

    b_list_data = []
    gl_acct = None

    b_list = None

    b_list_data, B_list = create_model("B_list", {"k":int, "monat":string, "wert":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal b_list_data, gl_acct
        nonlocal fibukonto


        nonlocal b_list
        nonlocal b_list_data

        return {"b-list": b_list_data}

    def create_b_list():

        nonlocal b_list_data, gl_acct
        nonlocal fibukonto


        nonlocal b_list
        nonlocal b_list_data

        i:int = 0
        mon:List[string] = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "FalseV", "DEC"]

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fibukonto)]})
        for i in range(1,12 + 1) :
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.k = i
            b_list.monat = mon[i - 1]
            b_list.wert =  to_decimal(gl_acct.actual[i - 1])

    create_b_list()

    return generate_output()