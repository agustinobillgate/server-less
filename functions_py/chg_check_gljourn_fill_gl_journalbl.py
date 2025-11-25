#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 25/11/2025, with_for_update added
# di program ini hanya menggunakan temp-table, (tdk ada operasi insert/update/delete pada tabel model)
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct, Gl_jouhdr

g_list_data, G_list = create_model("G_list", {"jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "duplicate":bool}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})

def chg_check_gljourn_fill_gl_journalbl(g_list_data:[G_list]):
    case_type:int = 0
    gl_acct = gl_jouhdr = None

    b1_list = g_list = t_gl_acct = t_gl_jouhdr = None

    b1_list_data, B1_list = create_model("B1_list", {"fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "bezeich":string, "chginit":string, "chgdate":date, "sysdate":date, "zeit":int, "activeflag":int, "rec_gl_journ":int, "tax_code":string, "tax_amount":string, "tot_amt":string})
    t_gl_acct_data, T_gl_acct = create_model_like(Gl_acct)
    t_gl_jouhdr_data, T_gl_jouhdr = create_model_like(Gl_jouhdr)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal case_type, gl_acct, gl_jouhdr
        nonlocal b1_list, g_list, t_gl_acct, t_gl_jouhdr
        nonlocal b1_list_data, t_gl_acct_data, t_gl_jouhdr_data

        return {"g-list": g_list_data}


    if case_type == 1:

        g_list = query(g_list_data, first=True)

        t_gl_jouhdr = query(t_gl_jouhdr_data, first=True)

        t_gl_jouhdr = query(t_gl_jouhdr_data, filters=(lambda t_gl_jouhdr: t_gl_jouhdr.jnr == g_list.jnr), first=True)
        t_gl_jouhdr.debit =  to_decimal(g_list.debit)
        t_gl_jouhdr.credit =  to_decimal(g_list.credit)
        pass

    return generate_output()