from functions.additional_functions import *
import decimal
from models import Gl_acct

def inv_adjustment_chk_fibubl(c_list:[C_list]):
    err_code = 0
    gl_acct = None

    c_list = c_list1 = None

    c_list_list, C_list = create_model("C_list", {"artnr":int, "bezeich":str, "munit":str, "inhalt":str, "zwkum":str, "endkum":int, "qty":decimal, "qty1":decimal, "fibukonto":str, "avrg_price":decimal, "cost_center":str}, {"fibukonto": "0000000000"})

    C_list1 = C_list
    c_list1_list = c_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, gl_acct
        nonlocal c_list1


        nonlocal c_list, c_list1
        nonlocal c_list_list
        return {"err_code": err_code}

    for c_list1 in query(c_list1_list, filters=(lambda c_list1 :c_list1.qty != c_list1.qty1 and c_list1.fibukonto.lower()  != "0000000000")):

        gl_acct = db_session.query(Gl_acct).filter(
                (Gl_acct.fibukonto == c_list1.fibukonto)).first()

        if not gl_acct:
            err_code = 1

            return generate_output()