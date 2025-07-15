#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct, Gl_journal

def gl_postjourn_fill_listbl(jnr:int):

    prepare_cache ([Gl_acct, Gl_journal])

    credits = None
    debits = None
    remains = None
    buf_g_list_data = []
    gl_acct = gl_journal = None

    g_list = buf_g_list = gl_acct1 = None

    g_list_data, G_list = create_model("G_list", {"jnr":int, "fibukonto":string, "acct_fibukonto":string, "debit":Decimal, "credit":Decimal, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "bemerk":string, "bezeich":string, "duplicate":bool, "tax_code":string, "tax_amount":string, "tot_amt":string}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})
    buf_g_list_data, Buf_g_list = create_model_like(G_list)

    Gl_acct1 = create_buffer("Gl_acct1",Gl_acct)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal credits, debits, remains, buf_g_list_data, gl_acct, gl_journal
        nonlocal jnr
        nonlocal gl_acct1


        nonlocal g_list, buf_g_list, gl_acct1
        nonlocal g_list_data, buf_g_list_data

        return {"credits": credits, "debits": debits, "remains": remains, "buf-g-list": buf_g_list_data}


    for gl_journal in db_session.query(Gl_journal).filter(
             (Gl_journal.jnr == jnr)).order_by(Gl_journal._recid).all():
        g_list = G_list()
        g_list_data.append(g_list)

        g_list.fibukonto = gl_journal.fibukonto
        g_list.debit =  to_decimal(gl_journal.debit)
        g_list.credit =  to_decimal(gl_journal.credit)
        g_list.userinit = gl_journal.userinit
        g_list.sysdate = gl_journal.sysdate
        g_list.zeit = gl_journal.zeit
        g_list.chginit = gl_journal.chginit
        g_list.chgdate = gl_journal.chgdate
        g_list.bemerk = gl_journal.bemerk
        credits = credits + gl_journal.credit
        debits = debits + gl_journal.debit
        remains = debits - credits

    gl_acct1_obj_list = {}
    for gl_acct1 in db_session.query(Gl_acct1).filter(
             ((Gl_acct1.fibukonto.in_(list(set([g_list.fibukonto for g_list in g_list_data])))))).order_by(g_list.sysdate.desc(), g_list.zeit.desc()).all():
        if gl_acct1_obj_list.get(gl_acct1._recid):
            continue
        else:
            gl_acct1_obj_list[gl_acct1._recid] = True


        buf_g_list = Buf_g_list()
        buf_g_list_data.append(buf_g_list)

        buffer_copy(g_list, buf_g_list)
        buf_g_list.acct_fibukonto = gl_acct1.fibukonto
        buf_g_list.bezeich = gl_acct1.bezeich

        if num_entries(gl_acct1.bemerk, ";") > 1:
            buf_g_list.tax_code = entry(1, gl_acct1.bemerk, ";")

    return generate_output()