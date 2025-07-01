#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_acct, Gl_jouhdr, Htparam, Mathis, Fa_artikel, Fa_grup, Fa_kateg

def fa_depn_step_twobl(datum:date, user_init:string, curr_anz:int, debits:Decimal, credits:Decimal, remains:Decimal):

    prepare_cache ([Gl_acct, Htparam, Mathis, Fa_artikel, Fa_grup, Fa_kateg])

    buff_g_list_list = []
    debit_betrag:Decimal = to_decimal("0.0")
    credit_betrag:Decimal = to_decimal("0.0")
    depn_value:Decimal = to_decimal("0.0")
    dept_methode:bool = False
    gl_acct = gl_jouhdr = htparam = mathis = fa_artikel = fa_grup = fa_kateg = None

    gl_acc1 = gl_acct1 = gl_jouhdr1 = s_list = g_list = buff_g_list = None

    s_list_list, S_list = create_model("S_list", {"fibukonto":string, "bezeich":string, "credit":Decimal, "debet":Decimal})
    g_list_list, G_list = create_model("G_list", {"nr":int, "jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "duplicate":bool, "gl_acct1_fibukonto":string, "gl_acct1_bezeich":string}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})
    buff_g_list_list, Buff_g_list = create_model_like(G_list)

    Gl_acc1 = create_buffer("Gl_acc1",Gl_acct)
    Gl_acct1 = create_buffer("Gl_acct1",Gl_acct)
    Gl_jouhdr1 = create_buffer("Gl_jouhdr1",Gl_jouhdr)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal buff_g_list_list, debit_betrag, credit_betrag, depn_value, dept_methode, gl_acct, gl_jouhdr, htparam, mathis, fa_artikel, fa_grup, fa_kateg
        nonlocal datum, user_init, curr_anz, debits, credits, remains
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, s_list, g_list, buff_g_list
        nonlocal s_list_list, g_list_list, buff_g_list_list

        return {"curr_anz": curr_anz, "debits": debits, "credits": credits, "remains": remains, "buff-g-list": buff_g_list_list}

    def add_list(create_it:bool):

        nonlocal buff_g_list_list, debit_betrag, credit_betrag, depn_value, dept_methode, gl_acct, gl_jouhdr, htparam, mathis, fa_artikel, fa_grup, fa_kateg
        nonlocal datum, user_init, curr_anz, debits, credits, remains
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, s_list, g_list, buff_g_list
        nonlocal s_list_list, g_list_list, buff_g_list_list


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


    def get_depn_value():

        nonlocal buff_g_list_list, debit_betrag, credit_betrag, depn_value, dept_methode, gl_acct, gl_jouhdr, htparam, mathis, fa_artikel, fa_grup, fa_kateg
        nonlocal datum, user_init, curr_anz, debits, credits, remains
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, s_list, g_list, buff_g_list
        nonlocal s_list_list, g_list_list, buff_g_list_list

        tot_anz:int = 0

        fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_artikel.katnr)]})

        if fa_kateg.methode == 0:

            if dept_methode:
                tot_anz = fa_kateg.nutzjahr - fa_artikel.anz_depn
            else:
                tot_anz = fa_kateg.nutzjahr * 12 - fa_artikel.anz_depn

            if tot_anz > 0:
                depn_value =  to_decimal(fa_artikel.book_wert) / to_decimal(tot_anz)
            else:
                depn_value =  to_decimal("0")


    htparam = get_cache (Htparam, {"paramnr": [(eq, 1366)],"bezeichnung": [(ne, "not used")]})

    if htparam:
        dept_methode = htparam.flogical

    fa_artikel_obj_list = {}
    fa_artikel = Fa_artikel()
    mathis = Mathis()
    for fa_artikel.nr, fa_artikel.katnr, fa_artikel.anz_depn, fa_artikel.book_wert, fa_artikel.subgrp, fa_artikel.credit_fibu, fa_artikel.debit_fibu, fa_artikel._recid, mathis.asset, mathis.name, mathis._recid in db_session.query(Fa_artikel.nr, Fa_artikel.katnr, Fa_artikel.anz_depn, Fa_artikel.book_wert, Fa_artikel.subgrp, Fa_artikel.credit_fibu, Fa_artikel.debit_fibu, Fa_artikel._recid, Mathis.asset, Mathis.name, Mathis._recid).join(Mathis,(Mathis.nr == Fa_artikel.nr)).filter(
             (Fa_artikel.next_depn == datum) & (Fa_artikel.loeschflag == 0)).order_by(Mathis.name).all():
        if fa_artikel_obj_list.get(fa_artikel._recid):
            continue
        else:
            fa_artikel_obj_list[fa_artikel._recid] = True

        fa_grup = get_cache (Fa_grup, {"gnr": [(eq, fa_artikel.subgrp)],"flag": [(eq, 1)]})
        get_depn_value()

        if depn_value > 0:

            gl_acc1 = get_cache (Gl_acct, {"fibukonto": [(eq, fa_grup.credit_fibu)]})

            if not gl_acc1:

                gl_acc1 = get_cache (Gl_acct, {"fibukonto": [(eq, fa_artikel.credit_fibu)]})

            if gl_acc1:
                credit_betrag =  to_decimal(depn_value)
                debit_betrag =  to_decimal("0")
                add_list(True)
            else:
                pass

            gl_acc1 = get_cache (Gl_acct, {"fibukonto": [(eq, fa_grup.debit_fibu)]})

            if not gl_acc1:

                gl_acc1 = get_cache (Gl_acct, {"fibukonto": [(eq, fa_artikel.debit_fibu)]})

            if gl_acc1:
                debit_betrag =  to_decimal(depn_value)
                credit_betrag =  to_decimal("0")
                add_list(True)
            else:
                pass

    gl_acct1_obj_list = {}
    for gl_acct1 in db_session.query(Gl_acct1).filter(
             ((Gl_acct1.fibukonto.in_(list(set([g_list.fibukonto for g_list in g_list_list])))))).order_by(g_list.sysdate.desc(), g_list.zeit.desc()).all():
        if gl_acct1_obj_list.get(gl_acct1._recid):
            continue
        else:
            gl_acct1_obj_list[gl_acct1._recid] = True


        buff_g_list = Buff_g_list()
        buff_g_list_list.append(buff_g_list)

        buffer_copy(g_list, buff_g_list)
        buff_g_list.gl_acct1_fibukonto = gl_acct1.fibukonto
        buff_g_list.gl_acct1_bezeich = gl_acct1.bezeich

    return generate_output()