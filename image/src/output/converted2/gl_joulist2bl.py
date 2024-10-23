from functions.additional_functions import *
import decimal
from datetime import date
from models import Gl_journal

out_list_list, Out_list = create_model("Out_list", {"s_recid":int, "marked":str, "fibukonto":str, "jnr":int, "jtype":int, "bemerk":str, "trans_date":date, "bezeich":str, "number1":str, "debit":decimal, "credit":decimal, "balance":decimal, "debit_str":str, "credit_str":str, "balance_str":str, "refno":str, "uid":str, "created":date, "chgid":str, "chgdate":date, "tax_code":str, "tax_amount":str, "tot_amt":str, "approved":bool, "prev_bal":str, "counter":int})

def gl_joulist2bl(out_list_list:[Out_list]):
    gl_journal = None

    out_list = g_jour = None

    G_jour = create_buffer("G_jour",Gl_journal)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gl_journal
        nonlocal g_jour


        nonlocal out_list, g_jour
        nonlocal out_list_list
        return {}

    for out_list in query(out_list_list):

        gl_journal = db_session.query(Gl_journal).filter(
                 (Gl_journal._recid == out_list.s_recid)).first()

        if gl_journal:

            g_jour = db_session.query(G_jour).filter(
                     (G_jour._recid == gl_journal._recid)).first()

            if num_entries(g_jour.bemerk, chr(2)) > 1:
                g_jour.bemerk = entry(1, g_jour.bemerk, chr(2), out_list.number1)


            else:
                g_jour.bemerk = g_jour.bemerk + chr(2) + out_list.number1


            pass

    return generate_output()