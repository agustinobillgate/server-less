from functions.additional_functions import *
import decimal
from models import Fa_artikel, Gl_acct, Mathis

def fa_upgrade_step_twobl(p_nr:int, amt:decimal, user_init:str):
    debits = 0
    credits = 0
    avail_gl_acct = False
    avail_gl_acct1 = False
    name_mathis = ""
    curr_anz = 0
    remains = 0
    g_list_list = []
    s_list_list = []
    debit_betrag:decimal = 0
    credit_betrag:decimal = 0
    fa_artikel = gl_acct = mathis = None

    g_list = s_list = None

    g_list_list, G_list = create_model("G_list", {"nr":int, "jnr":int, "fibukonto":str, "debit":decimal, "credit":decimal, "bemerk":str, "userinit":str, "sysdate":date, "zeit":int, "chginit":str, "chgdate":date, "duplicate":bool}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})
    s_list_list, S_list = create_model("S_list", {"fibukonto":str, "bezeich":str, "credit":decimal, "debet":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal debits, credits, avail_gl_acct, avail_gl_acct1, name_mathis, curr_anz, remains, g_list_list, s_list_list, debit_betrag, credit_betrag, fa_artikel, gl_acct, mathis


        nonlocal g_list, s_list
        nonlocal g_list_list, s_list_list
        return {"debits": debits, "credits": credits, "avail_gl_acct": avail_gl_acct, "avail_gl_acct1": avail_gl_acct1, "name_mathis": name_mathis, "curr_anz": curr_anz, "remains": remains, "g-list": g_list_list, "s-list": s_list_list}

    def add_list(create_it:bool):

        nonlocal debits, credits, avail_gl_acct, avail_gl_acct1, name_mathis, curr_anz, remains, g_list_list, s_list_list, debit_betrag, credit_betrag, fa_artikel, gl_acct, mathis


        nonlocal g_list, s_list
        nonlocal g_list_list, s_list_list


        curr_anz = curr_anz + 1

        if create_it:
            g_list = G_list()
        g_list_list.append(g_list)

        g_list.nr = fa_artikel.nr
        g_list.fibukonto = gl_acct.fibukonto
        g_list.debit = g_list.debit + debit_betrag
        g_list.credit = g_list.credit + credit_betrag
        g_list.bemerk = mathis.asset + " - " + mathis.name
        g_list.userinit = user_init
        g_list.zeit = get_current_time_in_seconds()
        g_list.duplicate = False

        s_list = query(s_list_list, filters=(lambda s_list :s_list.fibukonto == gl_acct.fibukonto), first=True)

        if not s_list:
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.fibukonto = gl_acct.fibukonto
            s_list.bezeich = gl_acct.bezeich


        s_list.credit = s_list.credit + credit_betrag
        s_list.debet = s_list.debet + debit_betrag
        credits = credits + credit_betrag
        debits = debits + debit_betrag
        remains = debits - credits
        debit_betrag = 0
        credit_betrag = 0


    fa_artikel = db_session.query(Fa_artikel).filter(
            (Fa_artikel.nr == p_nr)).first()

    gl_acct = db_session.query(Gl_acct).filter(
            (Gl_acct.fibukonto == fa_artikel.fibukonto)).first()

    if gl_acct:
        avail_gl_acct1 = True
        debit_betrag = amt
        credit_betrag = 0


        add_list(True)

    mathis = db_session.query(Mathis).filter(
            (Mathis.nr == p_nr)).first()

    fa_artikel = db_session.query(Fa_artikel).filter(
            (Fa_artikel.nr == p_nr)).first()

    gl_acct = db_session.query(Gl_acct).filter(
            (Gl_acct.fibukonto == fa_artikel.fibukonto)).first()

    if gl_acct:
        avail_gl_acct = True
        credit_betrag = amt
        debit_betrag = 0


        add_list(True)
    else:
        name_mathis = mathis.name

    return generate_output()