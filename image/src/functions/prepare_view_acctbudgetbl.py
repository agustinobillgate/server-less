from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Htparam, Gl_acct

def prepare_view_acctbudgetbl(fibukonto:str):
    curr_yr = 0
    price_decimal = 0
    tot_budget = 0
    b_list_list = []
    gl_acct1_list = []
    htparam = gl_acct = None

    b_list = gl_acct1 = None

    b_list_list, B_list = create_model("B_list", {"k":int, "monat":str, "wert":decimal})
    gl_acct1_list, Gl_acct1 = create_model("Gl_acct1", {"fibukonto":str, "bezeich":str, "budget":[decimal, 12]})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_yr, price_decimal, tot_budget, b_list_list, gl_acct1_list, htparam, gl_acct


        nonlocal b_list, gl_acct1
        nonlocal b_list_list, gl_acct1_list
        return {"curr_yr": curr_yr, "price_decimal": price_decimal, "tot_budget": tot_budget, "b-list": b_list_list, "gl-acct1": gl_acct1_list}

    def create_b_list():

        nonlocal curr_yr, price_decimal, tot_budget, b_list_list, gl_acct1_list, htparam, gl_acct

        nonlocal b_list, gl_acct1
        nonlocal b_list_list, gl_acct1_list

        i:int = 0
        mon:str = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
        gl_acct = db_session.query(Gl_acct).filter(
                (func.lower(Gl_acct.fibukonto) == fibukonto.lower())).first()
        tot_budget = 0

        
        for i in range(1,12 + 1) :
            tot_budget = tot_budget + gl_acct.budget[i - 1]
            b_list = B_list()
            
            b_list.k = i
            b_list.monat = mon[i - 1]
            b_list.wert = gl_acct.budget[i - 1]
            b_list_list.append(b_list)
        # print("i:", i, b_list_list)

    def create_gl_acct1():

        nonlocal curr_yr, price_decimal, tot_budget, b_list_list, gl_acct1_list, htparam, gl_acct


        nonlocal b_list, gl_acct1
        nonlocal b_list_list, gl_acct1_list

        i:int = 0

        for gl_acct in db_session.query(Gl_acct).filter(
                (Gl_acct.activeflag) &  ((Gl_acct.acc_type == 1) |  (Gl_acct.acc_type == 2) |  (Gl_acct.acc_type == 5))).all():
            gl_acct1 = Gl_acct1()
            

            gl_acct1.fibukonto = gl_acct.fibukonto
            gl_acct1.bezeich = gl_acct.bezeich
            gl_acct1_list.append(gl_acct1)
            
            for i in range(0, 12) :
                gl_acct1.budget[i ] = gl_acct.budget[i ]
            print("budget:", gl_acct1.bezeich , gl_acct1.budget)


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 597)).first()
    curr_yr = get_year(htparam.fdate)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger
    create_b_list()
    create_gl_acct1()

    return generate_output()