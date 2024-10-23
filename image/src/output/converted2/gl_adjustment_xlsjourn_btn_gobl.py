from functions.additional_functions import *
import decimal
from models import Gl_acct

g_list_list, G_list = create_model("G_list", {"jnr":int, "fibukonto":str, "fibukonto2":str, "debit":decimal, "credit":decimal, "userinit":str, "sysdate":date, "zeit":int, "chginit":str, "chgdate":date, "bemerk":str, "descr":str, "duplicate":bool, "correct":int}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})

def gl_adjustment_xlsjourn_btn_gobl(g_list_list:[G_list]):
    debits = None
    credits = None
    remains = None
    gl_acct = None

    g_list = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal debits, credits, remains, gl_acct


        nonlocal g_list
        nonlocal g_list_list
        return {"g-list": g_list_list, "debits": debits, "credits": credits, "remains": remains}

    def check_acc():

        nonlocal debits, credits, remains, gl_acct


        nonlocal g_list
        nonlocal g_list_list

        for g_list in query(g_list_list):

            gl_acct = db_session.query(Gl_acct).filter(
                     (Gl_acct.fibukonto == g_list.fibukonto2)).first()

            if not gl_acct:
                correct = 2


    def debt_credit():

        nonlocal debits, credits, remains, gl_acct


        nonlocal g_list
        nonlocal g_list_list


        debits = 0
        credits = 0
        remains = 0

        for g_list in query(g_list_list):

            if g_list:
                debits = debits + g_list.debit
                credits = credits + g_list.credit
        remains = debits - credits

    check_acc()
    debt_credit()

    return generate_output()