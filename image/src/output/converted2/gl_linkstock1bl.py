#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_acct, Htparam, Artikel, Queasy, L_ophdr, L_artikel, L_untergrup, L_op, L_lieferant, L_kredit, Fa_artikel, Fa_op, Fa_grup

def gl_linkstock1bl(pvilanguage:int, link_out:bool, link_in:bool, from_grp:int, from_date:date, to_date:date, user_init:string):

    prepare_cache ([Htparam, Queasy, L_ophdr, L_artikel, L_untergrup, L_op, L_lieferant, L_kredit, Fa_artikel, Fa_op, Fa_grup])

    curr_anz = 0
    credits = to_decimal("0.0")
    debits = to_decimal("0.0")
    remains = to_decimal("0.0")
    msg_str = ""
    msg_str2 = ""
    msg_str3 = ""
    msg_str4 = ""
    msg_str5 = ""
    t_g_list_list = []
    s_list_list = []
    curr_zeit:int = 0
    curr_lschein:string = ""
    curr_note:string = ""
    add_note:string = ""
    fibukonto:string = ""
    debit_betrag:Decimal = to_decimal("0.0")
    credit_betrag:Decimal = to_decimal("0.0")
    tot_credit:Decimal = to_decimal("0.0")
    tot_debit:Decimal = to_decimal("0.0")
    counter:Decimal = to_decimal("0.0")
    lvcarea:string = "gl-linkstock"
    gl_acct = htparam = artikel = queasy = l_ophdr = l_artikel = l_untergrup = l_op = l_lieferant = l_kredit = fa_artikel = fa_op = fa_grup = None

    g_list = t_g_list = s_list = gl_acct1 = None

    g_list_list, G_list = create_model("G_list", {"docu_nr":string, "lscheinnr":string, "jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "add_note":string, "duplicate":bool, "acct_fibukonto":string, "bezeich":string}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})
    t_g_list_list, T_g_list = create_model_like(G_list)
    s_list_list, S_list = create_model("S_list", {"nr":int, "name":string, "debit":Decimal, "credit":Decimal})

    Gl_acct1 = create_buffer("Gl_acct1",Gl_acct)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_anz, credits, debits, remains, msg_str, msg_str2, msg_str3, msg_str4, msg_str5, t_g_list_list, s_list_list, curr_zeit, curr_lschein, curr_note, add_note, fibukonto, debit_betrag, credit_betrag, tot_credit, tot_debit, counter, lvcarea, gl_acct, htparam, artikel, queasy, l_ophdr, l_artikel, l_untergrup, l_op, l_lieferant, l_kredit, fa_artikel, fa_op, fa_grup
        nonlocal pvilanguage, link_out, link_in, from_grp, from_date, to_date, user_init
        nonlocal gl_acct1


        nonlocal g_list, t_g_list, s_list, gl_acct1
        nonlocal g_list_list, t_g_list_list, s_list_list

        return {"curr_anz": curr_anz, "credits": credits, "debits": debits, "remains": remains, "msg_str": msg_str, "msg_str2": msg_str2, "msg_str3": msg_str3, "msg_str4": msg_str4, "msg_str5": msg_str5, "t-g-list": t_g_list_list, "s-list": s_list_list}

    def step_two():

        nonlocal curr_anz, credits, debits, remains, msg_str, msg_str2, msg_str3, msg_str4, msg_str5, t_g_list_list, s_list_list, curr_zeit, curr_lschein, curr_note, add_note, fibukonto, debit_betrag, credit_betrag, tot_credit, tot_debit, counter, lvcarea, gl_acct, htparam, artikel, queasy, l_ophdr, l_artikel, l_untergrup, l_op, l_lieferant, l_kredit, fa_artikel, fa_op, fa_grup
        nonlocal pvilanguage, link_out, link_in, from_grp, from_date, to_date, user_init
        nonlocal gl_acct1


        nonlocal g_list, t_g_list, s_list, gl_acct1
        nonlocal g_list_list, t_g_list_list, s_list_list

        art1 = None
        gl_acc1 = None
        gl_acc2 = None
        bqueasy = None
        cost_account:string = ""
        cost_value:Decimal = to_decimal("0.0")
        do_it:bool = False
        Art1 =  create_buffer("Art1",Artikel)
        Gl_acc1 =  create_buffer("Gl_acc1",Gl_acct)
        Gl_acc2 =  create_buffer("Gl_acc2",Gl_acct)
        Bqueasy =  create_buffer("Bqueasy",Queasy)
        curr_zeit = get_current_time_in_seconds()

        l_op_obj_list = {}
        l_op = L_op()
        l_ophdr = L_ophdr()
        l_artikel = L_artikel()
        l_untergrup = L_untergrup()
        for l_op.stornogrund, l_op.warenwert, l_op.lscheinnr, l_op.lief_nr, l_op.lager_nr, l_op.docu_nr, l_op.artnr, l_op.op_art, l_op._recid, l_ophdr.fibukonto, l_ophdr.lscheinnr, l_ophdr.lager_nr, l_ophdr._recid, l_artikel.bezeich, l_artikel.fibukonto, l_artikel.artnr, l_artikel._recid, l_untergrup.fibukonto, l_untergrup._recid in db_session.query(L_op.stornogrund, L_op.warenwert, L_op.lscheinnr, L_op.lief_nr, L_op.lager_nr, L_op.docu_nr, L_op.artnr, L_op.op_art, L_op._recid, L_ophdr.fibukonto, L_ophdr.lscheinnr, L_ophdr.lager_nr, L_ophdr._recid, L_artikel.bezeich, L_artikel.fibukonto, L_artikel.artnr, L_artikel._recid, L_untergrup.fibukonto, L_untergrup._recid).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.op_typ == ("STT").lower()) & (L_ophdr.fibukonto != "")).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                 (L_op.pos > 0) & (L_op.op_art == 3) & (L_op.loeschflag < 2) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lager_nr > 0)).order_by(L_op.datum, L_op.lscheinnr).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True

            if l_op.stornogrund != "":

                gl_acct1 = db_session.query(Gl_acct1).filter(
                         (Gl_acct1.fibukonto == l_op.stornogrund)).first()
            else:

                gl_acct1 = db_session.query(Gl_acct1).filter(
                         (Gl_acct1.fibukonto == l_ophdr.fibukonto)).first()
            do_it = None != gl_acct1
            cost_value =  to_decimal("0")

            if do_it:
                curr_zeit = curr_zeit + 1
                curr_lschein = l_ophdr.lscheinnr
                curr_note = to_string(l_ophdr.lager_nr, "99") + "-" + curr_lschein + " " + l_artikel.bezeich
                add_note = ";&&5;" + to_string(l_ophdr.lager_nr, "99") + ";" + curr_lschein + ";"
                cost_account = gl_acct1.fibukonto

                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_untergrup.fibukonto)]})

                if not gl_acct:

                    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_artikel.fibukonto)]})

                if gl_acct:
                    fibukonto = gl_acct.fibukonto
                    cost_value =  to_decimal(cost_value) + to_decimal(round (l_op.warenwert , 2))

                    if l_op.warenwert > 0:
                        credit_betrag =  to_decimal(round (l_op.warenwert , 2))
                        debit_betrag =  to_decimal("0")

                        g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto == gl_acct.fibukonto and g_list.lscheinnr == l_op.lscheinnr and g_list.credit != 0), first=True)

                        if not g_list:
                            add_list(True)
                        else:
                            add_list(True)

                    elif l_op.warenwert < 0:
                        debit_betrag =  - to_decimal(round (l_op.warenwert , 2))
                        credit_betrag =  to_decimal("0")

                        g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto == gl_acct.fibukonto and g_list.lscheinnr == l_op.lscheinnr and g_list.debit != 0), first=True)

                        if not g_list:
                            add_list(True)
                        else:
                            add_list(True)
                else:
                    msg_str = msg_str + chr_unicode(2) + translateExtended ("Chart of Account not defined at stock article", lvcarea, "") + chr_unicode(10) + translateExtended ("ArticleNo", lvcarea, "") + " " + to_string(l_artikel.artnr) + " - " + l_artikel.bezeich

            if cost_value != 0:
                curr_zeit = curr_zeit + 1
                fibukonto = cost_account
                curr_lschein = l_ophdr.lscheinnr
                curr_note = to_string(l_ophdr.lager_nr, "99") + " - " + curr_lschein
                add_note = ";&&5;" + to_string(l_ophdr.lager_nr, "99") + ";" + curr_lschein + ";"

                if cost_value > 0:
                    debit_betrag =  to_decimal(cost_value)
                    credit_betrag =  to_decimal("0")

                    g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto.lower()  == (cost_account).lower()  and g_list.lscheinnr == l_op.lscheinnr and g_list.debit != 0), first=True)

                    if not g_list:
                        add_list(True)
                    else:
                        add_list(False)

                elif cost_value < 0:
                    credit_betrag =  - to_decimal(cost_value)
                    debit_betrag =  to_decimal("0")

                    g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto.lower()  == (cost_account).lower()  and g_list.lscheinnr == l_op.lscheinnr and g_list.credit != 0), first=True)

                    if not g_list:
                        add_list(True)
                    else:
                        add_list(False)


    def step_two1():

        nonlocal curr_anz, credits, debits, remains, msg_str, msg_str2, msg_str3, msg_str4, msg_str5, t_g_list_list, s_list_list, curr_zeit, curr_lschein, curr_note, add_note, fibukonto, debit_betrag, credit_betrag, tot_credit, tot_debit, counter, lvcarea, gl_acct, htparam, artikel, queasy, l_ophdr, l_artikel, l_untergrup, l_op, l_lieferant, l_kredit, fa_artikel, fa_op, fa_grup
        nonlocal pvilanguage, link_out, link_in, from_grp, from_date, to_date, user_init
        nonlocal gl_acct1


        nonlocal g_list, t_g_list, s_list, gl_acct1
        nonlocal g_list_list, t_g_list_list, s_list_list

        art1 = None
        gl_acc1 = None
        cost_account:string = ""
        cost_value:Decimal = to_decimal("0.0")
        do_it:bool = False
        s:Decimal = to_decimal("0.0")
        Art1 =  create_buffer("Art1",Artikel)
        Gl_acc1 =  create_buffer("Gl_acc1",Gl_acct)
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.nr = 1
        s_list.name = "INVENTORY"
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.nr = 2
        s_list.name = "EXPENSES"
        curr_zeit = get_current_time_in_seconds()

        l_op_obj_list = {}
        l_op = L_op()
        l_ophdr = L_ophdr()
        l_artikel = L_artikel()
        l_untergrup = L_untergrup()
        for l_op.stornogrund, l_op.warenwert, l_op.lscheinnr, l_op.lief_nr, l_op.lager_nr, l_op.docu_nr, l_op.artnr, l_op.op_art, l_op._recid, l_ophdr.fibukonto, l_ophdr.lscheinnr, l_ophdr.lager_nr, l_ophdr._recid, l_artikel.bezeich, l_artikel.fibukonto, l_artikel.artnr, l_artikel._recid, l_untergrup.fibukonto, l_untergrup._recid in db_session.query(L_op.stornogrund, L_op.warenwert, L_op.lscheinnr, L_op.lief_nr, L_op.lager_nr, L_op.docu_nr, L_op.artnr, L_op.op_art, L_op._recid, L_ophdr.fibukonto, L_ophdr.lscheinnr, L_ophdr.lager_nr, L_ophdr._recid, L_artikel.bezeich, L_artikel.fibukonto, L_artikel.artnr, L_artikel._recid, L_untergrup.fibukonto, L_untergrup._recid).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.op_typ == ("STT").lower()) & (L_ophdr.fibukonto != "")).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                 (L_op.pos > 0) & (L_op.op_art == 3) & (L_op.loeschflag < 2) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lager_nr > 0)).order_by(L_op.datum, L_op.lscheinnr).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True

            if l_op.stornogrund != "":

                gl_acct1 = db_session.query(Gl_acct1).filter(
                         (Gl_acct1.fibukonto == l_op.stornogrund)).first()
            else:

                gl_acct1 = db_session.query(Gl_acct1).filter(
                         (Gl_acct1.fibukonto == l_ophdr.fibukonto)).first()
            do_it = None != gl_acct1
            cost_value =  to_decimal("0")

            if do_it:
                curr_zeit = curr_zeit + 1
                curr_lschein = l_ophdr.lscheinnr
                curr_note = to_string(l_ophdr.lager_nr, "99") + "-" + curr_lschein + " " + l_artikel.bezeich
                add_note = ";&&5;" + to_string(l_ophdr.lager_nr, "99") + ";" + curr_lschein + ";"
                cost_account = gl_acct1.fibukonto

                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_untergrup.fibukonto)]})

                if not gl_acct:

                    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_artikel.fibukonto)]})

                if gl_acct:
                    fibukonto = gl_acct.fibukonto
                    cost_value =  to_decimal(cost_value) + to_decimal(round (l_op.warenwert , 2))
                    s =  to_decimal(s) + to_decimal(l_op.warenwert)

                    if l_op.warenwert > 0:
                        credit_betrag =  to_decimal(round (l_op.warenwert , 2))
                        debit_betrag =  to_decimal("0")

                        g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto == gl_acct.fibukonto and g_list.lscheinnr == l_op.lscheinnr and g_list.credit != 0), first=True)

                        if not g_list:
                            add_list1(True, 1)
                        else:
                            add_list1(True, 1)

                    elif l_op.warenwert < 0:
                        debit_betrag =  - to_decimal(round (l_op.warenwert , 2))
                        credit_betrag =  to_decimal("0")

                        g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto == gl_acct.fibukonto and g_list.lscheinnr == l_op.lscheinnr and g_list.debit != 0), first=True)

                        if not g_list:
                            add_list1(True, 1)
                        else:
                            add_list1(True, 1)
                else:
                    msg_str2 = msg_str2 + chr_unicode(2) + translateExtended ("Chart of Account not defined at stock article", lvcarea, "") + chr_unicode(10) + translateExtended ("ArticleNo", lvcarea, "") + " " + to_string(l_artikel.artnr) + " - " + l_artikel.bezeich

            if cost_value != 0:
                curr_zeit = curr_zeit + 1
                fibukonto = cost_account
                curr_lschein = l_ophdr.lscheinnr
                curr_note = to_string(l_ophdr.lager_nr, "99") + " - " + curr_lschein
                add_note = ";&&5;" + to_string(l_ophdr.lager_nr, "99") + ";" + curr_lschein + ";"

                if cost_value > 0:
                    debit_betrag =  to_decimal(cost_value)
                    credit_betrag =  to_decimal("0")

                    g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto.lower()  == (cost_account).lower()  and g_list.lscheinnr == l_op.lscheinnr and g_list.debit != 0), first=True)

                    if not g_list:
                        add_list1(True, 2)
                    else:
                        add_list1(False, 2)

                elif cost_value < 0:
                    credit_betrag =  - to_decimal(cost_value)
                    debit_betrag =  to_decimal("0")

                    g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto.lower()  == (cost_account).lower()  and g_list.lscheinnr == l_op.lscheinnr and g_list.credit != 0), first=True)

                    if not g_list:
                        add_list1(True, 2)
                    else:
                        add_list1(False, 2)


    def step_two2():

        nonlocal curr_anz, credits, debits, remains, msg_str, msg_str2, msg_str3, msg_str4, msg_str5, t_g_list_list, s_list_list, curr_zeit, curr_lschein, curr_note, add_note, fibukonto, debit_betrag, credit_betrag, tot_credit, tot_debit, counter, lvcarea, gl_acct, htparam, artikel, queasy, l_ophdr, l_artikel, l_untergrup, l_op, l_lieferant, l_kredit, fa_artikel, fa_op, fa_grup
        nonlocal pvilanguage, link_out, link_in, from_grp, from_date, to_date, user_init
        nonlocal gl_acct1


        nonlocal g_list, t_g_list, s_list, gl_acct1
        nonlocal g_list_list, t_g_list_list, s_list_list

        art1 = None
        gl_acc1 = None
        cost_value:Decimal = to_decimal("0.0")
        do_it:bool = False
        s:Decimal = to_decimal("0.0")
        wip_acct:string = ""
        Art1 =  create_buffer("Art1",Artikel)
        Gl_acc1 =  create_buffer("Gl_acc1",Gl_acct)

        l_op = get_cache (L_op, {"op_art": [(eq, 2)],"loeschflag": [(lt, 2)],"datum": [(ge, from_date),(le, to_date)],"lager_nr": [(gt, 0)],"herkunftflag": [(eq, 3)]})

        if not l_op:

            return
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.nr = 3
        s_list.name = "transFORM OUT"
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.nr = 4
        s_list.name = "transFORM IN"
        cost_value =  to_decimal("0")
        curr_zeit = get_current_time_in_seconds()

        l_op_obj_list = {}
        l_op = L_op()
        l_ophdr = L_ophdr()
        l_artikel = L_artikel()
        l_untergrup = L_untergrup()
        for l_op.stornogrund, l_op.warenwert, l_op.lscheinnr, l_op.lief_nr, l_op.lager_nr, l_op.docu_nr, l_op.artnr, l_op.op_art, l_op._recid, l_ophdr.fibukonto, l_ophdr.lscheinnr, l_ophdr.lager_nr, l_ophdr._recid, l_artikel.bezeich, l_artikel.fibukonto, l_artikel.artnr, l_artikel._recid, l_untergrup.fibukonto, l_untergrup._recid in db_session.query(L_op.stornogrund, L_op.warenwert, L_op.lscheinnr, L_op.lief_nr, L_op.lager_nr, L_op.docu_nr, L_op.artnr, L_op.op_art, L_op._recid, L_ophdr.fibukonto, L_ophdr.lscheinnr, L_ophdr.lager_nr, L_ophdr._recid, L_artikel.bezeich, L_artikel.fibukonto, L_artikel.artnr, L_artikel._recid, L_untergrup.fibukonto, L_untergrup._recid).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.op_typ == ("STT").lower())).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                 (L_op.op_art >= 2) & (L_op.op_art <= 4) & (L_op.herkunftflag == 3) & (L_op.loeschflag < 2) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lager_nr > 0)).order_by(L_op.datum, L_op.lscheinnr, L_op.op_art.desc()).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True

            if wip_acct == "":

                gl_acct1 = db_session.query(Gl_acct1).filter(
                         (Gl_acct1.fibukonto == l_op.stornogrund)).first()
                do_it = None != gl_acct1

                if not do_it:
                    msg_str3 = msg_str3 + chr_unicode(2) + translateExtended ("No G/L WIP Account number found :", lvcarea, "") + " " + l_op.lscheinnr

                    return
            wip_acct = gl_acct1.fibukonto

            if do_it:
                curr_lschein = l_ophdr.lscheinnr
                curr_note = to_string(l_ophdr.lager_nr, "99") + " - " + curr_lschein
                add_note = ";&&6;" + to_string(l_ophdr.lager_nr, "99") + ";" + curr_lschein + ";"

                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_untergrup.fibukonto)]})

                if not gl_acct:

                    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_artikel.fibukonto)]})

                if gl_acct:
                    fibukonto = gl_acct.fibukonto
                    s =  to_decimal(s) + to_decimal(l_op.warenwert)

                    if l_op.op_art == 4:
                        credit_betrag =  to_decimal(round (l_op.warenwert , 2))
                        debit_betrag =  to_decimal("0")

                        g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto == gl_acct.fibukonto and g_list.lscheinnr == l_op.lscheinnr and g_list.credit != 0), first=True)

                        if not g_list:
                            curr_zeit = curr_zeit + 1
                            add_list1(True, 3)
                        else:
                            add_list1(False, 3)

                    elif l_op.op_art == 2:
                        curr_note = to_string(l_ophdr.lager_nr, "99") + " - " + l_artikel.bezeich
                        add_note = ";&&6;" + to_string(l_ophdr.lager_nr, "99") + ";" + curr_lschein + ";"
                        cost_value =  to_decimal(cost_value) + to_decimal(round (l_op.warenwert , 2))
                        debit_betrag =  to_decimal(round (l_op.warenwert , 2))
                        credit_betrag =  to_decimal("0")
                        add_list1(True, 4)
                else:
                    msg_str4 = msg_str4 + chr_unicode(2) + translateExtended ("Chart of Account not defined at stock article", lvcarea, "") + chr_unicode(10) + translateExtended ("ArticleNo", lvcarea, "") + " " + to_string(l_artikel.artnr) + " - " + l_artikel.bezeich

        if cost_value > 0:
            curr_zeit = curr_zeit + 1
            fibukonto = wip_acct
            curr_lschein = ""
            curr_note = "WIP Transform IN"
            debit_betrag =  to_decimal(cost_value)
            credit_betrag =  to_decimal("0")
            add_list1(True, 0)
            curr_note = "WIP Transform OUT"
            credit_betrag =  to_decimal(cost_value)
            debit_betrag =  to_decimal("0")
            add_list1(True, 0)


    def step_three():

        nonlocal curr_anz, credits, debits, remains, msg_str, msg_str2, msg_str3, msg_str4, msg_str5, t_g_list_list, s_list_list, curr_zeit, curr_note, add_note, fibukonto, debit_betrag, credit_betrag, tot_credit, tot_debit, lvcarea, gl_acct, htparam, artikel, queasy, l_ophdr, l_artikel, l_untergrup, l_op, l_lieferant, l_kredit, fa_artikel, fa_op, fa_grup
        nonlocal pvilanguage, link_out, link_in, from_grp, from_date, to_date, user_init
        nonlocal gl_acct1


        nonlocal g_list, t_g_list, s_list, gl_acct1
        nonlocal g_list_list, t_g_list_list, s_list_list

        art1 = None
        gl_acc1 = None
        ap_account:string = ""
        ratio:Decimal = to_decimal("0.0")
        note:string = ""
        curr_docu:string = ""
        curr_lschein:string = ""
        op_exist:bool = False
        tot_wert:Decimal = to_decimal("0.0")
        do_it:bool = False
        tot_vat:Decimal = to_decimal("0.0")
        curr_bezeich:string = ""
        curr_firma:string = ""
        counter:int = 0
        bqueasy = None
        gl_acc2 = None
        Art1 =  create_buffer("Art1",Artikel)
        Gl_acc1 =  create_buffer("Gl_acc1",Gl_acct)
        Bqueasy =  create_buffer("Bqueasy",Queasy)
        Gl_acc2 =  create_buffer("Gl_acc2",Gl_acct)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 986)]})
        ap_account = htparam.fchar
        op_exist = False
        curr_lschein = ""
        curr_zeit = get_current_time_in_seconds()

        l_op_obj_list = {}
        l_op = L_op()
        l_artikel = L_artikel()
        l_untergrup = L_untergrup()
        for l_op.stornogrund, l_op.warenwert, l_op.lscheinnr, l_op.lief_nr, l_op.lager_nr, l_op.docu_nr, l_op.artnr, l_op.op_art, l_op._recid, l_artikel.bezeich, l_artikel.fibukonto, l_artikel.artnr, l_artikel._recid, l_untergrup.fibukonto, l_untergrup._recid in db_session.query(L_op.stornogrund, L_op.warenwert, L_op.lscheinnr, L_op.lief_nr, L_op.lager_nr, L_op.docu_nr, L_op.artnr, L_op.op_art, L_op._recid, L_artikel.bezeich, L_artikel.fibukonto, L_artikel.artnr, L_artikel._recid, L_untergrup.fibukonto, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                 (L_op.pos > 0) & (L_op.anzahl != 0) & (L_op.op_art == 1) & (L_op.loeschflag < 2) & (L_op.datum >= from_date) & (L_op.datum <= to_date)).order_by(L_op.lscheinnr, L_op.lief_nr).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_untergrup.fibukonto)]})

            if not gl_acct:

                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_artikel.fibukonto)]})

            if gl_acct:
                curr_zeit = curr_zeit + 1

                if curr_lschein == "":
                    curr_lschein = l_op.lscheinnr

                    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_op.lief_nr)]})

                    if not l_lieferant:

                        l_kredit = get_cache (L_kredit, {"lscheinnr": [(eq, l_op.lscheinnr)]})

                if curr_lschein != l_op.lscheinnr:

                    if l_lieferant:

                        if counter <= 1:
                            curr_note = curr_lschein + " - " + curr_bezeich + "; " + l_lieferant.firma
                        else:
                            curr_note = curr_lschein + " - " + l_lieferant.firma
                        counter = 0
                    else:

                        if counter <= 1:
                            curr_note = curr_lschein + " - " + curr_bezeich + "; " + curr_firma
                        else:
                            curr_note = curr_lschein + " - " + curr_firma
                        counter = 0
                    do_it = True

                    if l_lieferant and l_lieferant.z_code != "":

                        gl_acc1 = db_session.query(Gl_acc1).filter(
                                 (Gl_acc1.fibukonto == l_lieferant.z_code)).first()

                        if gl_acc1:
                            do_it = (gl_acc1.fibukonto == ap_account)

                    if not do_it:
                        fibukonto = gl_acc1.fibukonto

                        if tot_wert > 0:
                            credit_betrag =  to_decimal(tot_wert)
                            debit_betrag =  to_decimal("0")
                            add_list(True)

                        elif tot_wert < 0:
                            debit_betrag =  - to_decimal(tot_wert)
                            credit_betrag =  to_decimal("0")
                            add_list(True)
                    else:
                        fibukonto = ap_account

                        for l_kredit in db_session.query(L_kredit).filter(
                                 (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.lscheinnr == (curr_lschein).lower()) & (L_kredit.opart >= 0) & (L_kredit.zahlkonto == 0) & (L_kredit.saldo != 0)).order_by(L_kredit._recid).all():
                            ratio =  to_decimal(l_kredit.netto) / to_decimal(l_kredit.saldo)

                            if l_kredit.netto >= 0:
                                credit_betrag =  to_decimal(l_kredit.netto)
                                debit_betrag =  to_decimal("0")
                                add_list(True)

                            elif l_kredit.netto < 0:
                                debit_betrag =  - to_decimal(l_kredit.netto)
                                credit_betrag =  to_decimal("0")
                                add_list(True)

                    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_op.lief_nr)]})

                    if not l_lieferant:

                        l_kredit = get_cache (L_kredit, {"lscheinnr": [(eq, l_op.lscheinnr)]})
                    curr_lschein = l_op.lscheinnr
                    op_exist = False
                    tot_wert =  to_decimal("0")
                    tot_vat =  to_decimal("0")

                if l_lieferant:
                    curr_note = l_op.lscheinnr + " - " + l_artikel.bezeich + "; " + l_lieferant.firma
                    curr_bezeich = l_artikel.bezeich
                    curr_firma = l_lieferant.firma
                    counter = counter + 1
                else:
                    curr_note = l_op.lscheinnr + " - " + l_artikel.bezeich
                add_note = ";&&3;" + to_string(l_op.lager_nr, "99") + ";" + to_string(l_op.lief_nr) + ";" + l_op.docu_nr + ";" + l_op.lscheinnr + ";"
                tot_wert =  to_decimal(tot_wert) + to_decimal(l_op.warenwert)
                fibukonto = gl_acct.fibukonto
                curr_docu = l_op.docu_nr

                if l_op.warenwert >= 0:
                    debit_betrag =  to_decimal(l_op.warenwert)
                    credit_betrag =  to_decimal("0")

                    g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto == gl_acct.fibukonto and g_list.lscheinnr == l_op.lscheinnr and g_list.debit != 0), first=True)

                    if not g_list and debit_betrag != 0:
                        add_list(True)
                    else:
                        add_list(False)
                    op_exist = True

                elif l_op.warenwert < 0:
                    credit_betrag =  - to_decimal(l_op.warenwert)
                    debit_betrag =  to_decimal("0")

                    g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto == gl_acct.fibukonto and g_list.lscheinnr == l_op.lscheinnr and g_list.credit != 0), first=True)

                    if not g_list and credit_betrag != 0:
                        add_list(True)
                    else:
                        add_list(False)
                    op_exist = True

                queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

                if queasy:

                    bqueasy = get_cache (Queasy, {"key": [(eq, 303)],"number1": [(eq, queasy.number2)]})

                    gl_acc2 = db_session.query(Gl_acc2).filter(
                             (Gl_acc2.fibukonto == bqueasy.char2)).first()

                    if l_lieferant:
                        curr_note = "VAT " + l_op.lscheinnr + " " + l_artikel.bezeich + "; " + l_lieferant.firma
                    else:
                        curr_note = "VAT " + l_op.lscheinnr + " " + l_artikel.bezeich
                    add_note = ";&&3;" + to_string(l_op.lager_nr, "99") + ";" + to_string(l_op.lief_nr) + ";" + l_op.docu_nr + ";" + l_op.lscheinnr + ";"
                    tot_wert =  to_decimal(tot_wert) + to_decimal((l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100)))
                    tot_vat =  to_decimal(tot_vat) + to_decimal((l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100)))

                    if gl_acc2:
                        fibukonto = gl_acc2.fibukonto
                    curr_docu = l_op.docu_nr

                    if (l_op.warenwert * (queasy.deci1 / 100)) >= 0:
                        debit_betrag = ( to_decimal(l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100)))
                        credit_betrag =  to_decimal("0")

                        g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto == gl_acc2.fibukonto and g_list.lscheinnr == l_op.lscheinnr and g_list.debit != 0), first=True)

                        if not g_list and debit_betrag != 0:
                            add_list(True)
                        else:
                            add_list(False)
                        op_exist = True

                    elif (l_op.warenwert * (queasy.deci1 / 100)) < 0:
                        credit_betrag =  - to_decimal((l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100)))
                        debit_betrag =  to_decimal("0")

                        g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto == gl_acc2.fibukonto and g_list.lscheinnr == l_op.lscheinnr and g_list.credit != 0), first=True)

                        if not g_list and debit_betrag != 0:
                            add_list(True)
                        else:
                            add_list(False)
                        op_exist = True
            else:
                msg_str5 = msg_str5 + chr_unicode(2) + translateExtended ("Chart-of-acct of following inventory item not defined :", lvcarea, "") + chr_unicode(10) + to_string(l_artikel.artnr) + " - " + l_artikel.bezeich

        if op_exist:
            curr_zeit = curr_zeit + 1

            if l_lieferant:

                if counter <= 1:
                    curr_note = curr_lschein + " - " + curr_bezeich + "; " + l_lieferant.firma
                else:
                    curr_note = curr_lschein + " - " + l_lieferant.firma
                counter = 0
            else:

                if counter <= 1:
                    curr_note = curr_lschein + " - " + curr_bezeich + "; " + curr_firma
                else:
                    curr_note = curr_lschein + " - " + curr_firma
                counter = 0
            do_it = True

            if l_lieferant and l_lieferant.z_code != "":

                gl_acc1 = db_session.query(Gl_acc1).filter(
                         (Gl_acc1.fibukonto == l_lieferant.z_code)).first()

                if gl_acc1:
                    do_it = (gl_acc1.fibukonto == ap_account)

            if not do_it:
                fibukonto = gl_acc1.fibukonto

                if tot_wert > 0:
                    credit_betrag =  to_decimal(tot_wert)
                    debit_betrag =  to_decimal("0")
                    add_list(True)

                elif tot_wert < 0:
                    debit_betrag =  - to_decimal(tot_wert)
                    credit_betrag =  to_decimal("0")
                    add_list(True)
            else:
                fibukonto = ap_account

                for l_kredit in db_session.query(L_kredit).filter(
                         (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.lscheinnr == (curr_lschein).lower()) & (L_kredit.opart >= 0) & (L_kredit.zahlkonto == 0) & (L_kredit.saldo != 0)).order_by(L_kredit._recid).all():
                    ratio =  to_decimal(l_kredit.netto) / to_decimal(l_kredit.saldo)

                    if l_kredit.netto >= 0:
                        credit_betrag =  to_decimal(l_kredit.netto)
                        debit_betrag =  to_decimal("0")
                        add_list(True)

                    elif l_kredit.netto < 0:
                        debit_betrag =  - to_decimal(l_kredit.netto)
                        credit_betrag =  to_decimal("0")
                        add_list(True)


    def step_three_fa():

        nonlocal curr_anz, credits, debits, remains, msg_str, msg_str2, msg_str3, msg_str4, msg_str5, t_g_list_list, s_list_list, curr_zeit, curr_note, add_note, fibukonto, debit_betrag, credit_betrag, tot_credit, tot_debit, counter, lvcarea, gl_acct, htparam, artikel, queasy, l_ophdr, l_artikel, l_untergrup, l_op, l_lieferant, l_kredit, fa_artikel, fa_op, fa_grup
        nonlocal pvilanguage, link_out, link_in, from_grp, from_date, to_date, user_init
        nonlocal gl_acct1


        nonlocal g_list, t_g_list, s_list, gl_acct1
        nonlocal g_list_list, t_g_list_list, s_list_list

        art1 = None
        gl_acc1 = None
        ap_account:string = ""
        note:string = ""
        curr_docu:string = ""
        curr_lschein:string = ""
        op_exist:bool = False
        tot_vat:Decimal = to_decimal("0.0")
        bqueasy = None
        gl_acc2 = None
        Art1 =  create_buffer("Art1",Artikel)
        Gl_acc1 =  create_buffer("Gl_acc1",Gl_acct)
        Bqueasy =  create_buffer("Bqueasy",Queasy)
        Gl_acc2 =  create_buffer("Gl_acc2",Gl_acct)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 887)]})

        if htparam.fchar != "":
            ap_account = htparam.fchar
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 986)]})
            ap_account = htparam.fchar
        op_exist = False
        curr_lschein = ""
        curr_zeit = get_current_time_in_seconds()

        fa_op_obj_list = {}
        fa_op = Fa_op()
        l_lieferant = L_lieferant()
        fa_artikel = Fa_artikel()
        for fa_op.nr, fa_op.docu_nr, fa_op.lscheinnr, fa_op.warenwert, fa_op._recid, l_lieferant.firma, l_lieferant.z_code, l_lieferant._recid, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel._recid in db_session.query(Fa_op.nr, Fa_op.docu_nr, Fa_op.lscheinnr, Fa_op.warenwert, Fa_op._recid, L_lieferant.firma, L_lieferant.z_code, L_lieferant._recid, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel._recid).join(L_lieferant,(L_lieferant.lief_nr == Fa_op.lief_nr)).join(Fa_artikel,(Fa_artikel.nr == Fa_op.nr)).filter(
                 (Fa_op.anzahl != 0) & (Fa_op.loeschflag < 2) & (Fa_op.opart == 1) & (Fa_op.datum >= from_date) & (Fa_op.datum <= to_date)).order_by(Fa_op.lscheinnr).all():
            if fa_op_obj_list.get(fa_op._recid):
                continue
            else:
                fa_op_obj_list[fa_op._recid] = True

            fa_grup = get_cache (Fa_grup, {"gnr": [(eq, fa_artikel.subgrp)],"flag": [(eq, 1)]})

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fa_grup.fibukonto)]})

            if not gl_acct:

                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fa_artikel.fibukonto)]})
            curr_zeit = curr_zeit + 1
            add_note = ";&&9;" + trim(to_string(fa_op.nr, ">>>99")) + ";" + fa_op.docu_nr + ";" + fa_op.lscheinnr + ";"

            if curr_lschein == "":
                curr_lschein = fa_op.lscheinnr
                curr_note = curr_lschein + " - " + l_lieferant.firma

            if curr_lschein != fa_op.lscheinnr:
                fibukonto = ap_account

                for l_kredit in db_session.query(L_kredit).filter(
                         (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.lscheinnr == (curr_lschein).lower()) & (L_kredit.opart >= 0) & (L_kredit.zahlkonto == 0) & (L_kredit.saldo != 0)).order_by(L_kredit._recid).all():

                    if l_kredit.netto >= 0:
                        credit_betrag =  to_decimal(l_kredit.netto)
                        debit_betrag =  to_decimal("0")
                        add_list(True)

                    elif l_kredit.netto < 0:
                        debit_betrag =  - to_decimal(l_kredit.netto)
                        credit_betrag =  to_decimal("0")
                        add_list(True)
                curr_lschein = fa_op.lscheinnr
                curr_note = curr_lschein + " - " + l_lieferant.firma
                op_exist = False
                tot_vat =  to_decimal("0")
            fibukonto = gl_acct.fibukonto
            curr_docu = fa_op.docu_nr

            if fa_op.warenwert >= 0:
                debit_betrag =  to_decimal(round (fa_op.warenwert , 2))
                credit_betrag =  to_decimal("0")

                g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto == gl_acct.fibukonto and g_list.lscheinnr == fa_op.lscheinnr and g_list.debit != 0), first=True)

                if not g_list:
                    add_list(True)
                else:
                    add_list(False)
                op_exist = True

            elif fa_op.warenwert < 0:
                credit_betrag =  - to_decimal(round (fa_op.warenwert , 2))
                debit_betrag =  to_decimal("0")

                g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto == gl_acct.fibukonto and g_list.lscheinnr == fa_op.lscheinnr and g_list.credit != 0), first=True)

                if not g_list:
                    add_list(True)
                else:
                    add_list(False)
                op_exist = True

            queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

            if queasy:

                bqueasy = get_cache (Queasy, {"key": [(eq, 303)],"number1": [(eq, queasy.number2)]})

                gl_acc2 = db_session.query(Gl_acc2).filter(
                         (Gl_acc2.fibukonto == bqueasy.char2)).first()
                fibukonto = gl_acc2.fibukonto
                curr_docu = fa_op.docu_nr
                tot_vat = ( to_decimal(fa_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100)))

                if (fa_op.warenwert * (queasy.deci1 / 100)) >= 0:
                    debit_betrag =  to_decimal(round ((fa_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100)) , 2))
                    credit_betrag =  to_decimal("0")

                    g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto == gl_acc2.fibukonto and g_list.lscheinnr == fa_op.lscheinnr and g_list.debit != 0), first=True)

                    if not g_list:
                        add_list(True)
                    else:
                        add_list(False)
                    op_exist = True

                elif (fa_op.warenwert * (queasy.deci1 / 100)) < 0:
                    credit_betrag =  - to_decimal(round ((fa_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100)) , 2))
                    debit_betrag =  to_decimal("0")

                    g_list = query(g_list_list, filters=(lambda g_list: g_list.fibukonto == gl_acc2.fibukonto and g_list.lscheinnr == fa_op.lscheinnr and g_list.credit != 0), first=True)

                    if not g_list:
                        add_list(True)
                    else:
                        add_list(False)
                    op_exist = True

        if op_exist:
            curr_zeit = curr_zeit + 1
            fibukonto = ap_account

            for l_kredit in db_session.query(L_kredit).filter(
                     (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.lscheinnr == (curr_lschein).lower()) & (L_kredit.opart >= 0) & (L_kredit.zahlkonto == 0) & (L_kredit.saldo != 0)).order_by(L_kredit._recid).all():

                if l_kredit.netto >= 0:
                    credit_betrag =  to_decimal(l_kredit.netto)
                    debit_betrag =  to_decimal("0")
                    add_list(True)

                elif l_kredit.netto < 0:
                    debit_betrag =  - to_decimal(l_kredit.netto)
                    credit_betrag =  to_decimal("0")
                    add_list(True)


    def add_list(create_it:bool):

        nonlocal curr_anz, credits, debits, remains, msg_str, msg_str2, msg_str3, msg_str4, msg_str5, t_g_list_list, s_list_list, curr_zeit, curr_lschein, curr_note, add_note, fibukonto, debit_betrag, credit_betrag, tot_credit, tot_debit, counter, lvcarea, gl_acct, htparam, artikel, queasy, l_ophdr, l_artikel, l_untergrup, l_op, l_lieferant, l_kredit, fa_artikel, fa_op, fa_grup
        nonlocal pvilanguage, link_out, link_in, from_grp, from_date, to_date, user_init
        nonlocal gl_acct1


        nonlocal g_list, t_g_list, s_list, gl_acct1
        nonlocal g_list_list, t_g_list_list, s_list_list


        curr_anz = curr_anz + 1

        if create_it:
            g_list = G_list()
            g_list_list.append(g_list)

            g_list.fibukonto = fibukonto
            g_list.lscheinnr = curr_lschein
            g_list.bemerk = curr_note
            g_list.add_note = add_note
        g_list.debit =  to_decimal(g_list.debit) + to_decimal(debit_betrag)
        g_list.credit =  to_decimal(g_list.credit) + to_decimal(credit_betrag)
        g_list.userinit = user_init
        g_list.zeit = curr_zeit
        g_list.duplicate = False
        credits =  to_decimal(credits) + to_decimal(credit_betrag)
        debits =  to_decimal(debits) + to_decimal(debit_betrag)
        remains =  to_decimal(debits) - to_decimal(credits)
        debit_betrag =  to_decimal("0")
        credit_betrag =  to_decimal("0")


    def add_list1(create_it:bool, nr:int):

        nonlocal curr_anz, credits, debits, remains, msg_str, msg_str2, msg_str3, msg_str4, msg_str5, t_g_list_list, s_list_list, curr_zeit, curr_lschein, curr_note, add_note, fibukonto, debit_betrag, credit_betrag, tot_credit, tot_debit, counter, lvcarea, gl_acct, htparam, artikel, queasy, l_ophdr, l_artikel, l_untergrup, l_op, l_lieferant, l_kredit, fa_artikel, fa_op, fa_grup
        nonlocal pvilanguage, link_out, link_in, from_grp, from_date, to_date, user_init
        nonlocal gl_acct1


        nonlocal g_list, t_g_list, s_list, gl_acct1
        nonlocal g_list_list, t_g_list_list, s_list_list

        if nr > 0:

            s_list = query(s_list_list, filters=(lambda s_list: s_list.nr == nr), first=True)
            s_list.debit =  to_decimal(s_list.debit) + to_decimal(debit_betrag)
            s_list.credit =  to_decimal(s_list.credit) + to_decimal(credit_betrag)
        tot_credit =  to_decimal(tot_credit) + to_decimal(credit_betrag)
        tot_debit =  to_decimal(tot_debit) + to_decimal(debit_betrag)

        if create_it:
            counter = counter + 1

            if tot_debit - tot_credit == 0.01:
                g_list.credit =  to_decimal(g_list.credit) + to_decimal(0.01)
                credits =  to_decimal(credits) + to_decimal(0.01)

            elif tot_debit - tot_credit == -0.01:
                g_list.credit =  to_decimal(g_list.credit) - to_decimal(0.01)
                credits =  to_decimal(credits) - to_decimal(0.01)

            if counter > 1:
                tot_credit =  to_decimal("0")
                tot_debit =  to_decimal("0")
                counter = 0
        curr_anz = curr_anz + 1

        if create_it:
            g_list = G_list()
            g_list_list.append(g_list)

            g_list.fibukonto = fibukonto
            g_list.lscheinnr = curr_lschein
            g_list.bemerk = curr_note
            g_list.add_note = add_note
        g_list.debit =  to_decimal(g_list.debit) + to_decimal(debit_betrag)
        g_list.credit =  to_decimal(g_list.credit) + to_decimal(credit_betrag)
        g_list.userinit = user_init
        g_list.zeit = curr_zeit
        g_list.duplicate = False
        credits =  to_decimal(credits) + to_decimal(credit_betrag)
        debits =  to_decimal(debits) + to_decimal(debit_betrag)
        remains =  to_decimal(debits) - to_decimal(credits)
        debit_betrag =  to_decimal("0")
        credit_betrag =  to_decimal("0")


    if link_out:

        if from_grp == 0:
            step_two()
        else:
            step_two1()

        if from_grp <= 1:
            step_two2()

    elif link_in:
        step_three()
        credits =  to_decimal("0")
        debits =  to_decimal("0")

        for g_list in query(g_list_list):
            g_list.debit = to_decimal(round(g_list.debit , 2))
            g_list.credit = to_decimal(round(g_list.credit , 2))
            credits =  to_decimal(credits) + to_decimal(g_list.credit)
            debits =  to_decimal(debits) + to_decimal(g_list.debit)
        remains =  to_decimal(debits) - to_decimal(credits)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 329)]})

        if htparam.flogical :
            step_three_fa()

    gl_acct1_obj_list = {}
    for gl_acct1 in db_session.query(Gl_acct1).filter(
             ((Gl_acct1.fibukonto.in_(list(set([g_list.fibukonto for g_list in g_list_list])))))).order_by(g_list.zeit, func.substring(g_list.bemerk, 0, 24), Gl_acct1.fibukonto).all():
        if gl_acct1_obj_list.get(gl_acct1._recid):
            continue
        else:
            gl_acct1_obj_list[gl_acct1._recid] = True


        t_g_list = T_g_list()
        t_g_list_list.append(t_g_list)

        buffer_copy(g_list, t_g_list)
        t_g_list.acct_fibukonto = gl_acct1.fibukonto
        t_g_list.bezeich = gl_acct1.bezeich

    return generate_output()