from functions.additional_functions import *
import decimal
from models import Gl_acct, Gl_jouhdr, Fa_artikel, Mathis, Fa_grup, Htparam

def fa_sale_step_twobl(nr:int, qty:int, amt:decimal, user_init:str):
    fa_wert = 0
    depn_wert = 0
    book_wert = 0
    curr_anz = 0
    debits = 0
    credits = 0
    remains = 0
    buff_g_list_list = []
    s_list_list = []
    profit:decimal = 0
    credit_betrag:decimal = 0
    debit_betrag:decimal = 0
    gl_acct = gl_jouhdr = fa_artikel = mathis = fa_grup = htparam = None

    gl_acc1 = gl_acct1 = gl_jouhdr1 = g_list = s_list = buff_g_list = None

    g_list_list, G_list = create_model("G_list", {"nr":int, "jnr":int, "fibukonto":str, "debit":decimal, "credit":decimal, "bemerk":str, "userinit":str, "sysdate":date, "zeit":int, "chginit":str, "chgdate":date, "duplicate":bool, "acct_fibukonto":str, "acct_bezeich":str}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})
    s_list_list, S_list = create_model("S_list", {"fibukonto":str, "bezeich":str, "credit":decimal, "debet":decimal})
    buff_g_list_list, Buff_g_list = create_model_like(G_list)

    Gl_acc1 = Gl_acct
    Gl_acct1 = Gl_acct
    Gl_jouhdr1 = Gl_jouhdr

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fa_wert, depn_wert, book_wert, curr_anz, debits, credits, remains, buff_g_list_list, s_list_list, profit, credit_betrag, debit_betrag, gl_acct, gl_jouhdr, fa_artikel, mathis, fa_grup, htparam
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list, s_list, buff_g_list
        nonlocal g_list_list, s_list_list, buff_g_list_list
        return {"fa_wert": fa_wert, "depn_wert": depn_wert, "book_wert": book_wert, "curr_anz": curr_anz, "debits": debits, "credits": credits, "remains": remains, "buff-g-list": buff_g_list_list, "s-list": s_list_list}

    def add_list(create_it:bool):

        nonlocal fa_wert, depn_wert, book_wert, curr_anz, debits, credits, remains, buff_g_list_list, s_list_list, profit, credit_betrag, debit_betrag, gl_acct, gl_jouhdr, fa_artikel, mathis, fa_grup, htparam
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list, s_list, buff_g_list
        nonlocal g_list_list, s_list_list, buff_g_list_list


        curr_anz = curr_anz + 1

        if create_it:
            g_list = G_list()
        g_list_list.append(g_list)

        g_list.nr = fa_artikel.nr
        g_list.fibukonto = gl_acc1.fibukonto
        g_list.debit = g_list.debit + debit_betrag
        g_list.credit = g_list.credit + credit_betrag
        g_list.bemerk = mathis.asset + " - " + mathis.name
        g_list.userinit = user_init
        g_list.zeit = get_current_time_in_seconds()
        g_list.duplicate = False

        s_list = query(s_list_list, filters=(lambda s_list :s_list.fibukonto == gl_acc1.fibukonto), first=True)

        if not s_list:
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.fibukonto = gl_acc1.fibukonto
            s_list.bezeich = gl_acc1.bezeich
        s_list.credit = s_list.credit + credit_betrag
        s_list.debet = s_list.debet + debit_betrag
        credits = credits + credit_betrag
        debits = debits + debit_betrag
        remains = debits - credits
        debit_betrag = 0
        credit_betrag = 0

    fa_artikel = db_session.query(Fa_artikel).filter(
            (Fa_artikel.nr == nr)).first()

    mathis = db_session.query(Mathis).filter(
            (Mathis.nr == nr)).first()

    if qty == fa_artikel.anzahl:
        fa_wert = fa_artikel.warenwert
        book_wert = fa_artikel.book_wert
        depn_wert = fa_artikel.depn_wert
    else:
        fa_wert = fa_artikel.warenwert * qty / fa_artikel.anzahl
        book_wert = fa_artikel.book_wert * qty / fa_artikel.anzahl
        depn_wert = fa_artikel.depn_wert * qty / fa_artikel.anzahl
    profit = amt - book_wert

    fa_grup = db_session.query(Fa_grup).filter(
            (Fa_grup.gnr == fa_artikel.subgrp) &  (Fa_grup.flag == 1)).first()

    gl_acc1 = db_session.query(Gl_acc1).filter(
            (Gl_acc1.fibukonto == fa_grup.fibukonto)).first()

    if not gl_acc1:

        gl_acc1 = db_session.query(Gl_acc1).filter(
                (Gl_acc1.fibukonto == fa_artikel.fibukonto)).first()

    if gl_acc1:
        credit_betrag = fa_wert
        debit_betrag = 0
        add_list(True)
    else:
        pass

    if depn_wert != 0:

        gl_acc1 = db_session.query(Gl_acc1).filter(
                (Gl_acc1.fibukonto == fa_artikel.credit_fibu)).first()

        if gl_acc1:
            debit_betrag = depn_wert
            credit_betrag = 0
            add_list(True)
        else:
            pass

    if amt != 0:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 882)).first()

        gl_acc1 = db_session.query(Gl_acc1).filter(
                (Gl_acc1.fibukonto == htparam.fchar)).first()

        if gl_acc1:
            debit_betrag = amt
            credit_betrag = 0
            add_list(True)
        else:
            pass

    if profit > 0:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 885)).first()

        gl_acc1 = db_session.query(Gl_acc1).filter(
                (Gl_acc1.fibukonto == htparam.fchar)).first()

        if gl_acc1:
            credit_betrag = profit
            debit_betrag = 0
            add_list(True)

        elif profit < 0:
            pass

    elif profit < 0:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 886)).first()

        gl_acc1 = db_session.query(Gl_acc1).filter(
                (Gl_acc1.fibukonto == htparam.fchar)).first()

        if gl_acc1:
            debit_betrag = - profit
            credit_betrag = 0
            add_list(True)
        else:
            pass

    for g_list in query(g_list_list):
        gl_acct1 = db_session.query(Gl_acct1).filter((Gl_acct1.fibukonto == g_list.fibukonto)).first()
        if not gl_acct1:
            continue

        buff_g_list = Buff_g_list()
        buff_g_list_list.append(buff_g_list)

        buffer_copy(g_list, buff_g_list)
        buff_g_list.acct_fibukonto = gl_acct1.fibukonto
        buff_g_list.acct_bezeich = gl_acct1.bezeich

    return generate_output()