#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct, Gl_jouhdr, Fa_artikel, Mathis, Fa_grup, Htparam

def fa_sale_step_twobl(nr:int, qty:int, amt:Decimal, user_init:string):

    prepare_cache ([Gl_acct, Fa_artikel, Mathis, Fa_grup, Htparam])

    fa_wert = to_decimal("0.0")
    depn_wert = to_decimal("0.0")
    book_wert = to_decimal("0.0")
    curr_anz = 0
    debits = to_decimal("0.0")
    credits = to_decimal("0.0")
    remains = to_decimal("0.0")
    buff_g_list_list = []
    s_list_list = []
    profit:Decimal = to_decimal("0.0")
    credit_betrag:Decimal = to_decimal("0.0")
    debit_betrag:Decimal = to_decimal("0.0")
    gl_acct = gl_jouhdr = fa_artikel = mathis = fa_grup = htparam = None

    gl_acc1 = gl_acct1 = gl_jouhdr1 = g_list = s_list = buff_g_list = None

    g_list_list, G_list = create_model("G_list", {"nr":int, "jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "duplicate":bool, "acct_fibukonto":string, "acct_bezeich":string}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})
    s_list_list, S_list = create_model("S_list", {"fibukonto":string, "bezeich":string, "credit":Decimal, "debet":Decimal})
    buff_g_list_list, Buff_g_list = create_model_like(G_list)

    Gl_acc1 = create_buffer("Gl_acc1",Gl_acct)
    Gl_acct1 = create_buffer("Gl_acct1",Gl_acct)
    Gl_jouhdr1 = create_buffer("Gl_jouhdr1",Gl_jouhdr)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fa_wert, depn_wert, book_wert, curr_anz, debits, credits, remains, buff_g_list_list, s_list_list, profit, credit_betrag, debit_betrag, gl_acct, gl_jouhdr, fa_artikel, mathis, fa_grup, htparam
        nonlocal nr, qty, amt, user_init
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list, s_list, buff_g_list
        nonlocal g_list_list, s_list_list, buff_g_list_list

        return {"fa_wert": fa_wert, "depn_wert": depn_wert, "book_wert": book_wert, "curr_anz": curr_anz, "debits": debits, "credits": credits, "remains": remains, "buff-g-list": buff_g_list_list, "s-list": s_list_list}

    def add_list(create_it:bool):

        nonlocal fa_wert, depn_wert, book_wert, curr_anz, debits, credits, remains, buff_g_list_list, s_list_list, profit, credit_betrag, debit_betrag, gl_acct, gl_jouhdr, fa_artikel, mathis, fa_grup, htparam
        nonlocal nr, qty, amt, user_init
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list, s_list, buff_g_list
        nonlocal g_list_list, s_list_list, buff_g_list_list


        curr_anz = curr_anz + 1

        if create_it:
            g_list = G_list()
            g_list_list.append(g_list)

        g_list.nr = fa_artikel.nr
        g_list.fibukonto = gl_acc1.fibukonto
        g_list.debit =  to_decimal(g_list.debit) + to_decimal(debit_betrag)
        g_list.credit =  to_decimal(g_list.credit) + to_decimal(credit_betrag)
        g_list.bemerk = mathis.asset + " - " + mathis.name
        g_list.userinit = user_init
        g_list.zeit = get_current_time_in_seconds()
        g_list.duplicate = False

        s_list = query(s_list_list, filters=(lambda s_list: s_list.fibukonto == gl_acc1.fibukonto), first=True)

        if not s_list:
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.fibukonto = gl_acc1.fibukonto
            s_list.bezeich = gl_acc1.bezeich
        s_list.credit =  to_decimal(s_list.credit) + to_decimal(credit_betrag)
        s_list.debet =  to_decimal(s_list.debet) + to_decimal(debit_betrag)
        credits =  to_decimal(credits) + to_decimal(credit_betrag)
        debits =  to_decimal(debits) + to_decimal(debit_betrag)
        remains =  to_decimal(debits) - to_decimal(credits)
        debit_betrag =  to_decimal("0")
        credit_betrag =  to_decimal("0")


    fa_artikel = get_cache (Fa_artikel, {"nr": [(eq, nr)]})

    mathis = get_cache (Mathis, {"nr": [(eq, nr)]})

    if qty == fa_artikel.anzahl:
        fa_wert =  to_decimal(fa_artikel.warenwert)
        book_wert =  to_decimal(fa_artikel.book_wert)
        depn_wert =  to_decimal(fa_artikel.depn_wert)
    else:
        fa_wert =  to_decimal(fa_artikel.warenwert) * to_decimal(qty) / to_decimal(fa_artikel.anzahl)
        book_wert =  to_decimal(fa_artikel.book_wert) * to_decimal(qty) / to_decimal(fa_artikel.anzahl)
        depn_wert =  to_decimal(fa_artikel.depn_wert) * to_decimal(qty) / to_decimal(fa_artikel.anzahl)
    profit =  to_decimal(amt) - to_decimal(book_wert)

    fa_grup = get_cache (Fa_grup, {"gnr": [(eq, fa_artikel.subgrp)],"flag": [(eq, 1)]})

    gl_acc1 = get_cache (Gl_acct, {"fibukonto": [(eq, fa_grup.fibukonto)]})

    if not gl_acc1:

        gl_acc1 = get_cache (Gl_acct, {"fibukonto": [(eq, fa_artikel.fibukonto)]})

    if gl_acc1:
        credit_betrag =  to_decimal(fa_wert)
        debit_betrag =  to_decimal("0")
        add_list(True)
    else:
        pass

    if depn_wert != 0:

        gl_acc1 = get_cache (Gl_acct, {"fibukonto": [(eq, fa_artikel.credit_fibu)]})

        if gl_acc1:
            debit_betrag =  to_decimal(depn_wert)
            credit_betrag =  to_decimal("0")
            add_list(True)
        else:
            pass

    if amt != 0:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 882)]})

        gl_acc1 = get_cache (Gl_acct, {"fibukonto": [(eq, htparam.fchar)]})

        if gl_acc1:
            debit_betrag =  to_decimal(amt)
            credit_betrag =  to_decimal("0")
            add_list(True)
        else:
            pass

    if profit > 0:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 885)]})

        gl_acc1 = get_cache (Gl_acct, {"fibukonto": [(eq, htparam.fchar)]})

        if gl_acc1:
            credit_betrag =  to_decimal(profit)
            debit_betrag =  to_decimal("0")
            add_list(True)

        elif profit < 0:
            pass

    elif profit < 0:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 886)]})

        gl_acc1 = get_cache (Gl_acct, {"fibukonto": [(eq, htparam.fchar)]})

        if gl_acc1:
            debit_betrag =  - to_decimal(profit)
            credit_betrag =  to_decimal("0")
            add_list(True)
        else:
            pass

    gl_acct1_obj_list = {}
    for gl_acct1 in db_session.query(Gl_acct1).filter(
             ((Gl_acct1.fibukonto.in_(list(set([g_list.fibukonto for g_list in g_list_list])))))).order_by(Gl_acct1._recid).all():
        if gl_acct1_obj_list.get(gl_acct1._recid):
            continue
        else:
            gl_acct1_obj_list[gl_acct1._recid] = True


        buff_g_list = Buff_g_list()
        buff_g_list_list.append(buff_g_list)

        buffer_copy(g_list, buff_g_list)
        buff_g_list.acct_fibukonto = gl_acct1.fibukonto
        buff_g_list.acct_bezeich = gl_acct1.bezeich

    return generate_output()