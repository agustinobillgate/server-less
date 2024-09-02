from functions.additional_functions import *
import decimal
from models import Htparam, Gl_acct

def inv_check_fibukontobl(c_list:[C_list]):
    found_it = False
    p_272:str = ""
    p_275:str = ""
    htparam = gl_acct = None

    c_list = None

    c_list_list, C_list = create_model("C_list", {"artnr":int, "bezeich":str, "munit":str, "inhalt":str, "zwkum":str, "endkum":int, "qty":decimal, "qty1":decimal, "fibukonto":str, "avrg_price":decimal, "cost_center":str}, {"fibukonto": "0000000000"})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal found_it, p_272, p_275, htparam, gl_acct


        nonlocal c_list
        nonlocal c_list_list
        return {"found_it": found_it}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 272)).first()

    if htparam:
        p_272 = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 275)).first()

    if htparam:
        p_275 = htparam.fchar

    for c_list in query(c_list_list, filters=(lambda c_list :c_list.fibukonto.lower()  != "0000000000")):

        gl_acct = db_session.query(Gl_acct).filter(
                (Gl_acct.fibukonto == c_list.fibukonto) &  (Gl_acct.acc_type == 2)).first()

        if gl_acct:

            if gl_acct.fibukonto.lower()  != (p_272).lower()  and gl_acct.fibukonto.lower()  != (p_275).lower() :
                found_it = True


                break

    return generate_output()