#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_jouhdr, Artikel, Gl_acct, L_kredit, Htparam

def gl_linkap1bl(pvilanguage:int, from_date:date, to_date:date, fibukonto:string, user_init:string, refno:string):

    prepare_cache ([Artikel, Gl_acct, L_kredit, Htparam])

    acct_error = 0
    credits = to_decimal("0.0")
    debits = to_decimal("0.0")
    remains = to_decimal("0.0")
    curr_anz = 0
    msg_str = ""
    t_g_list_list = []
    s_list_list = []
    curr_docu:string = ""
    curr_lschein:string = ""
    note:string = ""
    note1:string = ""
    add_note:string = ""
    curr_nr:int = 0
    debit_betrag:Decimal = to_decimal("0.0")
    credit_betrag:Decimal = to_decimal("0.0")
    lvcarea:string = "gl-linkap"
    gl_jouhdr = artikel = gl_acct = l_kredit = htparam = None

    s_list = g_list = t_g_list = g_list1 = None

    s_list_list, S_list = create_model("S_list", {"fibukonto":string, "bezeich":string, "credit":Decimal, "debet":Decimal})
    g_list_list, G_list = create_model("G_list", {"nr":int, "remark":string, "docu_nr":string, "lscheinnr":string, "jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "duplicate":bool, "acct_fibukonto":string, "bezeich":string}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})
    t_g_list_list, T_g_list = create_model_like(G_list)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal acct_error, credits, debits, remains, curr_anz, msg_str, t_g_list_list, s_list_list, curr_docu, curr_lschein, note, note1, add_note, curr_nr, debit_betrag, credit_betrag, lvcarea, gl_jouhdr, artikel, gl_acct, l_kredit, htparam
        nonlocal pvilanguage, from_date, to_date, fibukonto, user_init, refno


        nonlocal s_list, g_list, t_g_list, g_list1
        nonlocal s_list_list, g_list_list, t_g_list_list

        return {"acct_error": acct_error, "credits": credits, "debits": debits, "remains": remains, "curr_anz": curr_anz, "msg_str": msg_str, "t-g-list": t_g_list_list, "s-list": s_list_list}

    def step_two():

        nonlocal acct_error, credits, debits, remains, curr_anz, msg_str, t_g_list_list, s_list_list, curr_docu, curr_lschein, note, note1, add_note, curr_nr, debit_betrag, credit_betrag, lvcarea, gl_jouhdr, artikel, gl_acct, l_kredit, htparam
        nonlocal pvilanguage, from_date, to_date, fibukonto, user_init, refno


        nonlocal s_list, g_list, t_g_list, g_list1
        nonlocal s_list_list, g_list_list, t_g_list_list

        ap_account:string = ""
        ap_other:string = ""
        ap_fa:string = ""
        art1 = None
        gl_acc1 = None
        ap_buff = None
        Art1 =  create_buffer("Art1",Artikel)
        Gl_acc1 =  create_buffer("Gl_acc1",Gl_acct)
        G_list1 = G_list
        g_list1_list = g_list_list
        Ap_buff =  create_buffer("Ap_buff",L_kredit)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 986)]})
        ap_account = htparam.fchar

        htparam = get_cache (Htparam, {"paramnr": [(eq, 395)]})

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, htparam.fchar)]})

        if gl_acct:
            ap_other = gl_acct.fibukonto
        else:
            ap_other = ap_account

        htparam = get_cache (Htparam, {"paramnr": [(eq, 887)]})

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, htparam.fchar)]})

        if gl_acct:
            ap_fa = gl_acct.fibukonto
        else:
            ap_fa = ap_account

        for l_kredit in db_session.query(L_kredit).filter(
                 (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.lief_nr > 0) & (L_kredit.opart > 0) & (L_kredit.zahlkonto > 0)).order_by(L_kredit.bemerk, L_kredit.counter).all():

            ap_buff = get_cache (L_kredit, {"counter": [(eq, l_kredit.counter)],"zahlkonto": [(eq, 0)]})

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
                debit_betrag =  - to_decimal(l_kredit.saldo)
                credit_betrag =  to_decimal("0")

                g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto.lower()  == (fibukonto).lower()  and g_list.docu_nr == l_kredit.name and g_list.lscheinnr == l_kredit.lscheinnr and g_list.debit != 0), first=True)

                if not g_list:
                    add_list(True)
                else:
                    add_list(False)

            elif l_kredit.saldo > 0:
                credit_betrag =  to_decimal(l_kredit.saldo)
                debit_betrag =  to_decimal("0")

                g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto.lower()  == (fibukonto).lower()  and g_list.docu_nr == l_kredit.name and g_list.lscheinnr == l_kredit.lscheinnr and g_list.credit != 0), first=True)

                if not g_list:
                    add_list(True)
                else:
                    add_list(False)

            artikel = get_cache (Artikel, {"artnr": [(eq, l_kredit.zahlkonto)],"departement": [(eq, 0)]})

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, artikel.fibukonto)]})

            if gl_acct:
                fibukonto = gl_acct.fibukonto
                curr_nr = 2
                note = l_kredit.bemerk
                note1 = l_kredit.bemerk + " - zz"
                add_note = ";&&2;" + to_string(l_kredit.counter) + ";" + to_string(l_kredit.lief_nr) + ";" + to_string(l_kredit.zahlkonto) + ";" + to_string(l_kredit.saldo * 100)

                if l_kredit.saldo <= 0:
                    credit_betrag =  - to_decimal(l_kredit.saldo)
                    debit_betrag =  to_decimal("0")

                    g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto == artikel.fibukonto and entry(0, g_list.bemerk, ";&&") == (note).lower()  and g_list.credit != 0), first=True)

                    if not g_list:
                        add_list(True)
                    else:
                        add_list(False)

                elif l_kredit.saldo > 0:
                    debit_betrag =  to_decimal(l_kredit.saldo)
                    credit_betrag =  to_decimal("0")

                    g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto == artikel.fibukonto and entry(0, g_list.bemerk, ";&&") == (note).lower()  and g_list.debit != 0), first=True)

                    if not g_list:
                        add_list(True)
                    else:
                        add_list(False)
            else:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Chart of Account not defined", lvcarea, "") + chr_unicode(10) + translateExtended ("ArticleNo", lvcarea, "") + " " + to_string(artikel.artnr) + " - " + artikel.bezeich
                acct_error = 2

                return

        for g_list in query(g_list_list, filters=(lambda g_list: g_list.nr == 1 and g_list.credit > 0)):

            g_list1 = query(g_list1_list, filters=(lambda g_list1: g_list1.fibukonto == g_list.fibukonto and g_list.nr == 1 and g_list1.lscheinnr == g_list.lscheinnr and (g_list1.debit > g_list.credit)), first=True)

            if g_list1:
                g_list1.debit =  to_decimal(g_list1.debit) - to_decimal(g_list.credit)
                credits =  to_decimal(credits) - to_decimal(g_list.credit)
                debits =  to_decimal(debits) - to_decimal(g_list.credit)
                g_list_list.remove(g_list)


    def add_list(create_it:bool):

        nonlocal acct_error, credits, debits, remains, curr_anz, msg_str, t_g_list_list, s_list_list, curr_docu, curr_lschein, note, note1, add_note, curr_nr, debit_betrag, credit_betrag, lvcarea, gl_jouhdr, artikel, gl_acct, l_kredit, htparam
        nonlocal pvilanguage, from_date, to_date, fibukonto, user_init, refno


        nonlocal s_list, g_list, t_g_list, g_list1
        nonlocal s_list_list, g_list_list, t_g_list_list

        gl_acct1 = None
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)

        gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, fibukonto)]})
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
        g_list.debit =  to_decimal(g_list.debit) + to_decimal(debit_betrag)
        g_list.credit =  to_decimal(g_list.credit) + to_decimal(credit_betrag)
        g_list.userinit = user_init
        g_list.zeit = get_current_time_in_seconds()
        g_list.duplicate = False

        s_list = query(s_list_list, filters=(lambda s_list: s_list.fibukonto == gl_acct1.fibukonto), first=True)

        if not s_list:
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.fibukonto = gl_acct1.fibukonto
            s_list.bezeich = gl_acct1.bezeich
        s_list.credit =  to_decimal(s_list.credit) + to_decimal(credit_betrag)
        s_list.debet =  to_decimal(s_list.debet) + to_decimal(debit_betrag)
        credits =  to_decimal(credits) + to_decimal(credit_betrag)
        debits =  to_decimal(debits) + to_decimal(debit_betrag)
        remains =  to_decimal(debits) - to_decimal(credits)
        debit_betrag =  to_decimal("0")
        credit_betrag =  to_decimal("0")


    def step_three():

        nonlocal acct_error, credits, debits, remains, curr_anz, msg_str, t_g_list_list, s_list_list, curr_docu, curr_lschein, note, note1, add_note, curr_nr, debit_betrag, credit_betrag, lvcarea, gl_jouhdr, artikel, gl_acct, l_kredit, htparam
        nonlocal pvilanguage, from_date, to_date, fibukonto, user_init, refno


        nonlocal s_list, g_list, t_g_list, g_list1
        nonlocal s_list_list, g_list_list, t_g_list_list

        gl_acct1 = None
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)

        gl_acct1_obj_list = {}
        for gl_acct1 in db_session.query(Gl_acct1).filter(
                 ((Gl_acct1.fibukonto.in_(list(set([g_list.fibukonto for g_list in g_list_list])))))).order_by(g_list.remark, g_list.nr).all():
            if gl_acct1_obj_list.get(gl_acct1._recid):
                continue
            else:
                gl_acct1_obj_list[gl_acct1._recid] = True


            t_g_list = T_g_list()
            t_g_list_list.append(t_g_list)

            buffer_copy(g_list, t_g_list)
            t_g_list.acct_fibukonto = gl_acct1.fibukonto
            t_g_list.bezeich = gl_acct1.bezeich


    gl_jouhdr = get_cache (Gl_jouhdr, {"refno": [(eq, refno)],"jtype": [(eq, 4)]})

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