from functions.additional_functions import *
import decimal
from models import Gl_acct

coa_list_list, Coa_list = create_model_like(Gl_acct)

def coa_budget_update_budgetbl(coa_list_list:[Coa_list], sorttype:int):
    gl_acct = None

    coa_list = cbuff = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gl_acct
        nonlocal sorttype


        nonlocal coa_list, cbuff
        nonlocal coa_list_list
        return {}

    def update_budget():

        nonlocal gl_acct
        nonlocal sorttype


        nonlocal coa_list, cbuff
        nonlocal coa_list_list


        Cbuff = Coa_list
        cbuff_list = coa_list_list

        for cbuff in query(cbuff_list):

            gl_acct = db_session.query(Gl_acct).filter(
                     (Gl_acct.fibukonto == cbuff.fibukonto)).first()

            if gl_acct:

                if sorttype == 1:
                    gl_acct.budget[0] = cbuff.budget[0]
                    gl_acct.budget[1] = cbuff.budget[1]
                    gl_acct.budget[2] = cbuff.budget[2]
                    gl_acct.budget[3] = cbuff.budget[3]
                    gl_acct.budget[4] = cbuff.budget[4]
                    gl_acct.budget[5] = cbuff.budget[5]
                    gl_acct.budget[6] = cbuff.budget[6]
                    gl_acct.budget[7] = cbuff.budget[7]
                    gl_acct.budget[8] = cbuff.budget[8]
                    gl_acct.budget[9] = cbuff.budget[9]
                    gl_acct.budget[10] = cbuff.budget[10]
                    gl_acct.budget[11] = cbuff.budget[11]


                else:
                    gl_acct.debit[0] = cbuff.debit[0]
                    gl_acct.debit[1] = cbuff.debit[1]
                    gl_acct.debit[2] = cbuff.debit[2]
                    gl_acct.debit[3] = cbuff.debit[3]
                    gl_acct.debit[4] = cbuff.debit[4]
                    gl_acct.debit[5] = cbuff.debit[5]
                    gl_acct.debit[6] = cbuff.debit[6]
                    gl_acct.debit[7] = cbuff.debit[7]
                    gl_acct.debit[8] = cbuff.debit[8]
                    gl_acct.debit[9] = cbuff.debit[9]
                    gl_acct.debit[10] = cbuff.debit[10]
                    gl_acct.debit[11] = cbuff.debit[11]

    update_budget()

    return generate_output()