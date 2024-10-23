from functions.additional_functions import *
import decimal
from models import Gl_acct

def coa_budget_create_list_webbl(disp_all:bool):
    max_row = 2
    coa_list_list = []
    gl_acct = None

    coa_list = None

    coa_list_list, Coa_list = create_model_like(Gl_acct)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal max_row, coa_list_list, gl_acct
        nonlocal disp_all


        nonlocal coa_list
        nonlocal coa_list_list
        return {"max_row": max_row, "coa-list": coa_list_list}

    def create_list():

        nonlocal max_row, coa_list_list, gl_acct
        nonlocal disp_all


        nonlocal coa_list
        nonlocal coa_list_list


        coa_list_list.clear()

        if not disp_all:

            for gl_acct in db_session.query(Gl_acct).filter(
                     (Gl_acct.acc_type != 3) & (Gl_acct.acc_type != 4)).order_by(Gl_acct.fibukonto).all():
                coa_list = Coa_list()
                coa_list_list.append(coa_list)

                buffer_copy(gl_acct, coa_list)
        else:

            for gl_acct in db_session.query(Gl_acct).order_by(Gl_acct.fibukonto).all():
                coa_list = Coa_list()
                coa_list_list.append(coa_list)

                buffer_copy(gl_acct, coa_list)

    create_list()

    for gl_acct in db_session.query(Gl_acct).order_by(Gl_acct._recid).all():
        max_row = max_row + 1

    return generate_output()