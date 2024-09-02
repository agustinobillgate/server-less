from functions.additional_functions import *
import decimal
from datetime import date
from models import Gl_acct, Gl_jouhdr, Mathis, Fa_artikel, Fa_grup, Fa_kateg

def fa_depn_step_twobl(datum:date, user_init:str, curr_anz:int, debits:decimal, credits:decimal, remains:decimal):
    buff_g_list_list = []
    debit_betrag:decimal = 0
    credit_betrag:decimal = 0
    depn_value:decimal = 0
    gl_acct = gl_jouhdr = mathis = fa_artikel = fa_grup = fa_kateg = None

    gl_acc1 = gl_acct1 = gl_jouhdr1 = s_list = g_list = buff_g_list = None

    s_list_list, S_list = create_model("S_list", {"fibukonto":str, "bezeich":str, "credit":decimal, "debet":decimal})
    g_list_list, G_list = create_model("G_list", {"nr":int, "jnr":int, "fibukonto":str, "debit":decimal, "credit":decimal, "bemerk":str, "userinit":str, "sysdate":date, "zeit":int, "chginit":str, "chgdate":date, "duplicate":bool, "gl_acct1_fibukonto":str, "gl_acct1_bezeich":str}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})
    buff_g_list_list, Buff_g_list = create_model_like(G_list)

    Gl_acc1 = Gl_acct
    Gl_acct1 = Gl_acct
    Gl_jouhdr1 = Gl_jouhdr

    db_session = local_storage.db_session

    def generate_output():
        nonlocal buff_g_list_list, debit_betrag, credit_betrag, depn_value, gl_acct, gl_jouhdr, mathis, fa_artikel, fa_grup, fa_kateg
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, s_list, g_list, buff_g_list
        nonlocal s_list_list, g_list_list, buff_g_list_list
        return {"buff-g-list": buff_g_list_list}

    def add_list(create_it:bool):

        nonlocal buff_g_list_list, debit_betrag, credit_betrag, depn_value, gl_acct, gl_jouhdr, mathis, fa_artikel, fa_grup, fa_kateg
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, s_list, g_list, buff_g_list
        nonlocal s_list_list, g_list_list, buff_g_list_list


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

    def get_depn_value():

        nonlocal buff_g_list_list, debit_betrag, credit_betrag, depn_value, gl_acct, gl_jouhdr, mathis, fa_artikel, fa_grup, fa_kateg
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, s_list, g_list, buff_g_list
        nonlocal s_list_list, g_list_list, buff_g_list_list

        tot_anz:int = 0

        fa_kateg = db_session.query(Fa_kateg).filter(
                (Fa_kateg.katnr == fa_artikel.katnr)).first()

        if fa_kateg.methode == 0:
            tot_anz = fa_kateg.nutzjahr * 12 - fa_artikel.anz_depn

            if tot_anz > 0:
                depn_value = fa_artikel.book_wert / tot_anz
            else:
                depn_value = 0

    fa_artikel_obj_list = []
    for fa_artikel, mathis in db_session.query(Fa_artikel, Mathis).join(Mathis,(Mathis.nr == Fa_artikel.nr)).filter(
            (Fa_artikel.next_depn == datum) &  (Fa_artikel.loeschflag == 0)).all():
        if fa_artikel._recid in fa_artikel_obj_list:
            continue
        else:
            fa_artikel_obj_list.append(fa_artikel._recid)

        fa_grup = db_session.query(Fa_grup).filter(
                (Fa_grup.gnr == fa_artikel.subgrp) &  (Fa_grup.flag == 1)).first()
        get_depn_value()

        if depn_value > 0:

            gl_acc1 = db_session.query(Gl_acc1).filter(
                    (Gl_acc1.fibukonto == fa_grup.credit_fibu)).first()

            if not gl_acc1:

                gl_acc1 = db_session.query(Gl_acc1).filter(
                        (Gl_acc1.fibukonto == fa_artikel.credit_fibu)).first()

            if gl_acc1:
                credit_betrag = depn_value
                debit_betrag = 0
                add_list(True)
            else:
                pass

            gl_acc1 = db_session.query(Gl_acc1).filter(
                    (Gl_acc1.fibukonto == fa_grup.debit_fibu)).first()

            if not gl_acc1:

                gl_acc1 = db_session.query(Gl_acc1).filter(
                        (Gl_acc1.fibukonto == fa_artikel.debit_fibu)).first()

            if gl_acc1:
                debit_betrag = depn_value
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
        buff_g_list.gl_acct1_fibukonto = gl_acct1.fibukonto
        buff_g_list.gl_acct1_bezeich = gl_acct1.bezeich

    return generate_output()