from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct

def view_acctactual_1bl(fibukonto:str):
    b_list_list = []
    gl_acct = None

    b_list = None

    b_list_list, B_list = create_model("B_list", {"k":int, "monat":str, "wert":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal b_list_list, gl_acct


        nonlocal b_list
        nonlocal b_list_list
        return {"b-list": b_list_list}

    def create_b_list():

        nonlocal b_list_list, gl_acct


        nonlocal b_list
        nonlocal b_list_list

        i:int = 0
        mon:str = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

        gl_acct = db_session.query(Gl_acct).filter(
                (func.lower(Gl_acct.fibukonto) == (fibukonto).lower())).first()
        for i in range(1,12 + 1) :
            b_list = B_list()
            b_list_list.append(b_list)

            b_list.k = i
            b_list.monat = mon[i - 1]
            b_list.wert = gl_acct.actual[i - 1]


    create_b_list()

    return generate_output()