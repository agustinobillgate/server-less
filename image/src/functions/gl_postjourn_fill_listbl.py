from functions.additional_functions import *
import decimal
from models import Gl_acct, Gl_journal

def gl_postjourn_fill_listbl(jnr:int):
    credits = 0
    debits = 0
    remains = 0
    buf_g_list_list = []
    gl_acct = gl_journal = None

    g_list = buf_g_list = gl_acct1 = None

    g_list_list, G_list = create_model("G_list", {"jnr":int, "fibukonto":str, "acct_fibukonto":str, "debit":decimal, "credit":decimal, "userinit":str, "sysdate":date, "zeit":int, "chginit":str, "chgdate":date, "bemerk":str, "bezeich":str, "duplicate":bool, "tax_code":str, "tax_amount":str, "tot_amt":str}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})
    buf_g_list_list, Buf_g_list = create_model_like(G_list)

    Gl_acct1 = Gl_acct

    db_session = local_storage.db_session

    def generate_output():
        nonlocal credits, debits, remains, buf_g_list_list, gl_acct, gl_journal
        nonlocal gl_acct1


        nonlocal g_list, buf_g_list, gl_acct1
        nonlocal g_list_list, buf_g_list_list
        return {"credits": credits, "debits": debits, "remains": remains, "buf-g-list": buf_g_list_list}


    for gl_journal in db_session.query(Gl_journal).filter(
            (Gl_journal.jnr == jnr)).all():
        g_list = G_list()
        g_list_list.append(g_list)

        g_list.fibukonto = gl_journal.fibukonto
        g_list.debit = gl_journal.debit
        g_list.credit = gl_journal.credit
        g_list.userinit = gl_journal.userinit
        g_list.sysdate = gl_journal.sysdate
        g_list.zeit = gl_journal.zeit
        g_list.chginit = gl_journal.chginit
        g_list.chgdate = gl_journal.chgdate
        g_list.bemerk = gl_journal.bemerk
        credits = credits + gl_journal.credit
        debits = debits + gl_journal.debit
        remains = debits - credits

    for g_list in query(g_list_list):
        gl_acct1 = db_session.query(Gl_acct1).filter((Gl_acct1.fibukonto == g_list.fibukonto)).first()
        if not gl_acct1:
            continue

        buf_g_list = Buf_g_list()
        buf_g_list_list.append(buf_g_list)

        buffer_copy(g_list, buf_g_list)
        buf_g_list.acct_fibukonto = gl_acct1.fibukonto
        buf_g_list.bezeich = gl_acct1.bezeich

        if num_entries(gl_acct1.bemerk, ";") > 1:
            buf_g_list.tax_code = entry(1, gl_acct1.bemerk, ";")

    return generate_output()