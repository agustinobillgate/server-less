from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Gl_jouhdr, Artikel, Gl_acct, L_kredit, Htparam

def gl_linkap1bl(pvilanguage:int, from_date:date, to_date:date, fibukonto:str, user_init:str, refno:str):
    acct_error = 0
    credits = 0
    debits = 0
    remains = 0
    curr_anz = 0
    msg_str = ""
    t_g_list_list = []
    s_list_list = []
    curr_docu:str = ""
    curr_lschein:str = ""
    note:str = ""
    note1:str = ""
    add_note:str = ""
    curr_nr:int = 0
    debit_betrag:decimal = 0
    credit_betrag:decimal = 0
    lvcarea:str = "gl_linkap"
    gl_jouhdr = artikel = gl_acct = l_kredit = htparam = None

    s_list = g_list = t_g_list = art1 = gl_acc1 = g_list1 = ap_buff = gl_acct1 = None

    s_list_list, S_list = create_model("S_list", {"fibukonto":str, "bezeich":str, "credit":decimal, "debet":decimal})
    g_list_list, G_list = create_model("G_list", {"nr":int, "remark":str, "docu_nr":str, "lscheinnr":str, "jnr":int, "fibukonto":str, "debit":decimal, "credit":decimal, "bemerk":str, "userinit":str, "sysdate":date, "zeit":int, "chginit":str, "chgdate":date, "duplicate":bool, "acct_fibukonto":str, "bezeich":str}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})
    t_g_list_list, T_g_list = create_model_like(G_list)

    Art1 = Artikel
    Gl_acc1 = Gl_acct
    G_list1 = G_list
    g_list1_list = g_list_list

    Ap_buff = L_kredit
    Gl_acct1 = Gl_acct

    db_session = local_storage.db_session

    def generate_output():
        nonlocal acct_error, credits, debits, remains, curr_anz, msg_str, t_g_list_list, s_list_list, curr_docu, curr_lschein, note, note1, add_note, curr_nr, debit_betrag, credit_betrag, lvcarea, gl_jouhdr, artikel, gl_acct, l_kredit, htparam
        nonlocal art1, gl_acc1, g_list1, ap_buff, gl_acct1


        nonlocal s_list, g_list, t_g_list, art1, gl_acc1, g_list1, ap_buff, gl_acct1
        nonlocal s_list_list, g_list_list, t_g_list_list
        return {"acct_error": acct_error, "credits": credits, "debits": debits, "remains": remains, "curr_anz": curr_anz, "msg_str": msg_str, "t-g-list": t_g_list_list, "s-list": s_list_list}

    def step_two():

        nonlocal acct_error, credits, debits, remains, curr_anz, msg_str, t_g_list_list, s_list_list, curr_docu, curr_lschein, note, note1, add_note, curr_nr, debit_betrag, credit_betrag, lvcarea, gl_jouhdr, artikel, gl_acct, l_kredit, htparam
        nonlocal art1, gl_acc1, g_list1, ap_buff, gl_acct1


        nonlocal s_list, g_list, t_g_list, art1, gl_acc1, g_list1, ap_buff, gl_acct1
        nonlocal s_list_list, g_list_list, t_g_list_list

        ap_account:str = ""
        ap_other:str = ""
        ap_fa:str = ""
        Art1 = Artikel
        Gl_acc1 = Gl_acct
        G_list1 = G_list
        Ap_buff = L_kredit

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 986)).first()
        ap_account = htparam.fchar

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 395)).first()

        gl_acct = db_session.query(Gl_acct).filter(
                (Gl_acct.fibukonto == htparam.fchar)).first()

        if gl_acct:
            ap_other = gl_acct.fibukonto
        else:
            ap_other = ap_account

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 887)).first()

        gl_acct = db_session.query(Gl_acct).filter(
                (Gl_acct.fibukonto == htparam.fchar)).first()

        if gl_acct:
            ap_fa = gl_acct.fibukonto
        else:
            ap_fa = ap_account

        for l_kredit in db_session.query(L_kredit).filter(
                (L_kredit.rgdatum >= from_date) &  (L_kredit.rgdatum <= to_date) &  (L_kredit.lief_nr > 0) &  (L_kredit.opart > 0) &  (L_kredit.zahlkonto > 0)).all():

            ap_buff = db_session.query(Ap_buff).filter(
                    (Ap_buff.counter == l_kredit.counter) &  (Ap_buff.zahlkonto == 0)).first()

            if ap_buff.betriebsnr == 0:
                fibukonto = ap_account

            elif ap_buff.betriebsnr == 1:
                fibukonto = ap_other

            elif ap_buff.betriebsnr == 2:
                fibukonto = ap_fa
            curr_docu = l_kredit.name
            curr_lschein = l_kredit.lscheinnr
            curr_nr = 1
            note = l_kredit.lscheinnr + " - " + l_kredit.bemerk
            note1 = l_kredit.bemerk + " - " + l_kredit.lscheinnr
            add_note = ";&&1;" + to_string(l_kredit.counter) + ";" + to_string(l_kredit.lief_nr)

            if l_kredit.saldo < 0:
                debit_betrag = - l_kredit.saldo
                credit_betrag = 0

                g_list = query(g_list_list, filters=(lambda g_list :g_list.(fibukonto).lower().lower()  == (fibukonto).lower()  and g_list.docu_nr == l_kredit.name and g_list.lscheinnr == l_kredit.lscheinnr and g_list.debit != 0), first=True)

                if not g_list:
                    add_list(True)
                else:
                    add_list(False)

            elif l_kredit.saldo > 0:
                credit_betrag = l_kredit.saldo
                debit_betrag = 0

                g_list = query(g_list_list, filters=(lambda g_list :g_list.(fibukonto).lower().lower()  == (fibukonto).lower()  and g_list.docu_nr == l_kredit.name and g_list.lscheinnr == l_kredit.lscheinnr and g_list.credit != 0), first=True)

                if not g_list:
                    add_list(True)
                else:
                    add_list(False)

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == l_kredit.zahlkonto) &  (Artikel.departement == 0)).first()

            gl_acct = db_session.query(Gl_acct).filter(
                    (Gl_acct.fibukonto == artikel.fibukonto)).first()

            if gl_acct:
                fibukonto = gl_acct.fibukonto
                curr_nr = 2
                note = l_kredit.bemerk
                note1 = l_kredit.bemerk + " - zz"
                add_note = ";&&2;" + to_string(l_kredit.counter) + ";" + to_string(l_kredit.lief_nr) + ";" + to_string(l_kredit.zahlkonto) + ";" + to_string(l_kredit.saldo * 100)

                if l_kredit.saldo <= 0:
                    credit_betrag = - l_kredit.saldo
                    debit_betrag = 0

                    g_list = query(g_list_list, filters=(lambda g_list :g_list.fibukonto == artikel.fibukonto and entry(0, g_list.bemerk, ";&&") == (note).lower()  and g_list.credit != 0), first=True)

                    if not g_list:
                        add_list(True)
                    else:
                        add_list(False)

                elif l_kredit.saldo > 0:
                    debit_betrag = l_kredit.saldo
                    credit_betrag = 0

                    g_list = query(g_list_list, filters=(lambda g_list :g_list.fibukonto == artikel.fibukonto and entry(0, g_list.bemerk, ";&&") == (note).lower()  and g_list.debit != 0), first=True)

                    if not g_list:
                        add_list(True)
                    else:
                        add_list(False)
            else:
                msg_str = msg_str + chr(2) + translateExtended ("Chart of Account not defined", lvcarea, "") + chr(10) + translateExtended ("ArticleNo", lvcarea, "") + " " + to_string(artikel.artnr) + " - " + artikel.bezeich
                acct_error = 2

                return

        for g_list in query(g_list_list, filters=(lambda g_list :g_list.nr == 1 and g_list.credit > 0)):

            g_list1 = query(g_list1_list, filters=(lambda g_list1 :g_list1.fibukonto == g_list.fibukonto and g_list.nr == 1 and g_list1.lscheinnr == g_list.lscheinnr and (g_list1.debit > g_list.credit)), first=True)

            if g_list1:
                g_list1.debit = g_list1.debit - g_list.credit
                credits = credits - g_list.credit
                debits = debits - g_list.credit
                g_list_list.remove(g_list)

    def add_list(create_it:bool):

        nonlocal acct_error, credits, debits, remains, curr_anz, msg_str, t_g_list_list, s_list_list, curr_docu, curr_lschein, note, note1, add_note, curr_nr, debit_betrag, credit_betrag, lvcarea, gl_jouhdr, artikel, gl_acct, l_kredit, htparam
        nonlocal art1, gl_acc1, g_list1, ap_buff, gl_acct1


        nonlocal s_list, g_list, t_g_list, art1, gl_acc1, g_list1, ap_buff, gl_acct1
        nonlocal s_list_list, g_list_list, t_g_list_list


        Gl_acct1 = Gl_acct

        gl_acct1 = db_session.query(Gl_acct1).filter(
                (func.lower(Gl_acct1.(fibukonto).lower()) == (fibukonto).lower())).first()
        curr_anz = curr_anz + 1

        if create_it:
            g_list = G_list()
            g_list_list.append(g_list)

            g_list.fibukonto = fibukonto
            g_list.nr = curr_nr
            g_list.remark = note1
            g_list.bemerk = note + add_note
            g_list.docu_nr = curr_docu
            g_list.lscheinnr = curr_lschein
        g_list.debit = g_list.debit + debit_betrag
        g_list.credit = g_list.credit + credit_betrag
        g_list.userinit = user_init
        g_list.zeit = get_current_time_in_seconds()
        g_list.duplicate = False

        s_list = query(s_list_list, filters=(lambda s_list :s_list.fibukonto == gl_acct1.fibukonto), first=True)

        if not s_list:
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.fibukonto = gl_acct1.fibukonto
            s_list.bezeich = gl_acct1.bezeich
        s_list.credit = s_list.credit + credit_betrag
        s_list.debet = s_list.debet + debit_betrag
        credits = credits + credit_betrag
        debits = debits + debit_betrag
        remains = debits - credits
        debit_betrag = 0
        credit_betrag = 0

    def step_three():

        nonlocal acct_error, credits, debits, remains, curr_anz, msg_str, t_g_list_list, s_list_list, curr_docu, curr_lschein, note, note1, add_note, curr_nr, debit_betrag, credit_betrag, lvcarea, gl_jouhdr, artikel, gl_acct, l_kredit, htparam
        nonlocal art1, gl_acc1, g_list1, ap_buff, gl_acct1


        nonlocal s_list, g_list, t_g_list, art1, gl_acc1, g_list1, ap_buff, gl_acct1
        nonlocal s_list_list, g_list_list, t_g_list_list


        Gl_acct1 = Gl_acct

        for g_list in query(g_list_list):
            gl_acct1 = db_session.query(Gl_acct1).filter((Gl_acct1.fibukonto == g_list.fibukonto)).first()
            if not gl_acct1:
                continue

            t_g_list = T_g_list()
            t_g_list_list.append(t_g_list)

            buffer_copy(g_list, t_g_list)
            t_g_list.acct_fibukonto = gl_acct1.fibukonto
            t_g_list.bezeich = gl_acct1.bezeich

    gl_jouhdr = db_session.query(Gl_jouhdr).filter(
            (func.lower(Gl_jouhdr.(refno).lower()) == (refno).lower()) &  (Gl_jouhdr.jtype == 4)).first()

    if gl_jouhdr:
        msg_str = translateExtended ("Reference number already exists.", lvcarea, "")
        acct_error = 1

        return generate_output()
    step_two()

    if acct_error > 0:
        g_list_list.clear()
        s_list_list.clear()

        return generate_output()
    step_three()

    return generate_output()