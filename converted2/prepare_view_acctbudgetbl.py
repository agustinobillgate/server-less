#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Gl_acct

def prepare_view_acctbudgetbl(fibukonto:string):

    prepare_cache ([Htparam, Gl_acct])

    curr_yr = 0
    price_decimal = 0
    tot_budget = to_decimal("0.0")
    b_list_data = []
    gl_acct1_data = []
    htparam = gl_acct = None

    b_list = gl_acct1 = None

    b_list_data, B_list = create_model("B_list", {"k":int, "monat":string, "wert":Decimal})
    gl_acct1_data, Gl_acct1 = create_model("Gl_acct1", {"fibukonto":string, "bezeich":string, "budget":[Decimal,12]})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_yr, price_decimal, tot_budget, b_list_data, gl_acct1_data, htparam, gl_acct
        nonlocal fibukonto


        nonlocal b_list, gl_acct1
        nonlocal b_list_data, gl_acct1_data

        return {"curr_yr": curr_yr, "price_decimal": price_decimal, "tot_budget": tot_budget, "b-list": b_list_data, "gl-acct1": gl_acct1_data}

    def create_b_list():

        nonlocal curr_yr, price_decimal, tot_budget, b_list_data, gl_acct1_data, htparam, gl_acct
        nonlocal fibukonto


        nonlocal b_list, gl_acct1
        nonlocal b_list_data, gl_acct1_data

        i:int = 0
        mon:List[string] = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "FalseV", "DEC"]

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fibukonto)]})
        tot_budget =  to_decimal("0")
        for i in range(1,12 + 1) :
            tot_budget =  to_decimal(tot_budget) + to_decimal(gl_acct.budget[i - 1])
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.k = i
            b_list.monat = mon[i - 1]
            b_list.wert =  to_decimal(gl_acct.budget[i - 1])


    def create_gl_acct1():

        nonlocal curr_yr, price_decimal, tot_budget, b_list_data, gl_acct1_data, htparam, gl_acct
        nonlocal fibukonto


        nonlocal b_list, gl_acct1
        nonlocal b_list_data, gl_acct1_data

        i:int = 0

        for gl_acct in db_session.query(Gl_acct).filter(
                 (Gl_acct.activeflag) & ((Gl_acct.acc_type == 1) | (Gl_acct.acc_type == 2) | (Gl_acct.acc_type == 5))).order_by(Gl_acct.fibukonto).all():
            gl_acct1 = Gl_acct1()
            gl_acct1_data.append(gl_acct1)

            gl_acct1.fibukonto = gl_acct.fibukonto
            gl_acct1.bezeich = gl_acct.bezeich


            for i in range(1,12 + 1) :
                gl_acct1.budget[i - 1] = gl_acct.budget[i - 1]

    htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
    curr_yr = get_year(htparam.fdate)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger
    create_b_list()
    create_gl_acct1()

    return generate_output()