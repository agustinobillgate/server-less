from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Gl_acct, Htparam, Artikel, L_ophdr, L_artikel, L_untergrup, L_op, L_lieferant, L_kredit, Fa_artikel, Fa_op, Fa_grup

def gl_linkstock1bl(pvilanguage:int, link_out:bool, link_in:bool, from_grp:int, from_date:date, to_date:date, user_init:str):
    curr_anz = 0
    credits = 0
    debits = 0
    remains = 0
    msg_str = ""
    msg_str2 = ""
    msg_str3 = ""
    msg_str4 = ""
    msg_str5 = ""
    t_g_list_list = []
    s_list_list = []
    curr_zeit:int = 0
    curr_lschein:str = ""
    curr_note:str = ""
    add_note:str = ""
    fibukonto:str = ""
    debit_betrag:decimal = 0
    credit_betrag:decimal = 0
    lvcarea:str = "gl_linkstock"
    gl_acct = htparam = artikel = l_ophdr = l_artikel = l_untergrup = l_op = l_lieferant = l_kredit = fa_artikel = fa_op = fa_grup = None

    g_list = t_g_list = s_list = gl_acct1 = art1 = gl_acc1 = None

    g_list_list, G_list = create_model("G_list", {"docu_nr":str, "lscheinnr":str, "jnr":int, "fibukonto":str, "debit":decimal, "credit":decimal, "bemerk":str, "userinit":str, "sysdate":date, "zeit":int, "chginit":str, "chgdate":date, "add_note":str, "duplicate":bool, "acct_fibukonto":str, "bezeich":str}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})
    t_g_list_list, T_g_list = create_model_like(G_list)
    s_list_list, S_list = create_model("S_list", {"nr":int, "name":str, "debit":decimal, "credit":decimal})

    Gl_acct1 = Gl_acct
    Art1 = Artikel
    Gl_acc1 = Gl_acct

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_anz, credits, debits, remains, msg_str, msg_str2, msg_str3, msg_str4, msg_str5, t_g_list_list, s_list_list, curr_zeit, curr_lschein, curr_note, add_note, fibukonto, debit_betrag, credit_betrag, lvcarea, gl_acct, htparam, artikel, l_ophdr, l_artikel, l_untergrup, l_op, l_lieferant, l_kredit, fa_artikel, fa_op, fa_grup
        nonlocal gl_acct1, art1, gl_acc1


        nonlocal g_list, t_g_list, s_list, gl_acct1, art1, gl_acc1
        nonlocal g_list_list, t_g_list_list, s_list_list
        return {"curr_anz": curr_anz, "credits": credits, "debits": debits, "remains": remains, "msg_str": msg_str, "msg_str2": msg_str2, "msg_str3": msg_str3, "msg_str4": msg_str4, "msg_str5": msg_str5, "t-g-list": t_g_list_list, "s-list": s_list_list}

    def step_two():

        nonlocal curr_anz, credits, debits, remains, msg_str, msg_str2, msg_str3, msg_str4, msg_str5, t_g_list_list, s_list_list, curr_zeit, curr_lschein, curr_note, add_note, fibukonto, debit_betrag, credit_betrag, lvcarea, gl_acct, htparam, artikel, l_ophdr, l_artikel, l_untergrup, l_op, l_lieferant, l_kredit, fa_artikel, fa_op, fa_grup
        nonlocal gl_acct1, art1, gl_acc1


        nonlocal g_list, t_g_list, s_list, gl_acct1, art1, gl_acc1
        nonlocal g_list_list, t_g_list_list, s_list_list

        cost_account:str = ""
        cost_value:decimal = 0
        do_it:bool = False
        Art1 = Artikel
        Gl_acc1 = Gl_acct
        curr_zeit = get_current_time_in_seconds()

        l_op_obj_list = []
        for l_op, l_ophdr, l_artikel, l_untergrup in db_session.query(L_op, L_ophdr, L_artikel, L_untergrup).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) &  (func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.fibukonto != "")).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                (L_op.pos > 0) &  (L_op.op_art == 3) &  (L_op.loeschflag < 2) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lager_nr > 0)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)

            if l_op.stornogrund != "":

                gl_acct1 = db_session.query(Gl_acct1).filter(
                        (Gl_acct1.fibukonto == l_op.stornogrund)).first()
            else:

                gl_acct1 = db_session.query(Gl_acct1).filter(
                        (Gl_acct1.fibukonto == l_ophdr.fibukonto)).first()
            do_it = None != gl_acct1
            cost_value = 0

            if do_it:
                curr_zeit = curr_zeit + 1
                curr_lschein = l_ophdr.lscheinnr
                curr_note = to_string(l_ophdr.lager_nr, "99") + "-" + curr_lschein + " " + l_artikel.bezeich
                add_note = ";&&5;" + to_string(l_ophdr.lager_nr, "99") + ";" + curr_lschein + ";"
                cost_account = gl_acct1.fibukonto

                gl_acct = db_session.query(Gl_acct).filter(
                        (Gl_acct.fibukonto == l_untergrup.fibukonto)).first()

                if not gl_acct:

                    gl_acct = db_session.query(Gl_acct).filter(
                            (Gl_acct.fibukonto == l_artikel.fibukonto)).first()

                if gl_acct:
                    fibukonto = gl_acct.fibukonto
                    cost_value = cost_value + round (l_op.warenwert, 2)

                    if l_op.warenwert > 0:
                        credit_betrag = round (l_op.warenwert, 2)
                        debit_betrag = 0

                        g_list = query(g_list_list, filters=(lambda g_list :g_list.fibukonto == gl_acct.fibukonto and g_list.lscheinnr == l_op.lscheinnr and g_list.credit != 0), first=True)

                        if not g_list:
                            add_list(True)
                        else:
                            add_list(True)

                    elif l_op.warenwert < 0:
                        debit_betrag = - round (l_op.warenwert, 2)
                        credit_betrag = 0

                        g_list = query(g_list_list, filters=(lambda g_list :g_list.fibukonto == gl_acct.fibukonto and g_list.lscheinnr == l_op.lscheinnr and g_list.debit != 0), first=True)

                        if not g_list:
                            add_list(True)
                        else:
                            add_list(True)
                else:
                    msg_str = msg_str + chr(2) + translateExtended ("Chart of Account not defined at stock article", lvcarea, "") + chr(10) + translateExtended ("ArticleNo", lvcarea, "") + " " + to_string(l_artikel.artnr) + " - " + l_artikel.bezeich

            if cost_value != 0:
                curr_zeit = curr_zeit + 1
                fibukonto = cost_account
                curr_lschein = l_ophdr.lscheinnr
                curr_note = to_string(l_ophdr.lager_nr, "99") + " - " + curr_lschein
                add_note = ";&&5;" + to_string(l_ophdr.lager_nr, "99") + ";" + curr_lschein + ";"

                if cost_value > 0:
                    debit_betrag = cost_value
                    credit_betrag = 0

                    g_list = query(g_list_list, filters=(lambda g_list :g_list.fibukonto.lower()  == (cost_account).lower()  and g_list.lscheinnr == l_op.lscheinnr and g_list.debit != 0), first=True)

                    if not g_list:
                        add_list(True)
                    else:
                        add_list(False)

                elif cost_value < 0:
                    credit_betrag = - cost_value
                    debit_betrag = 0

                    g_list = query(g_list_list, filters=(lambda g_list :g_list.fibukonto.lower()  == (cost_account).lower()  and g_list.lscheinnr == l_op.lscheinnr and g_list.credit != 0), first=True)

                    if not g_list:
                        add_list(True)
                    else:
                        add_list(False)

    def step_two1():

        nonlocal curr_anz, credits, debits, remains, msg_str, msg_str2, msg_str3, msg_str4, msg_str5, t_g_list_list, s_list_list, curr_zeit, curr_lschein, curr_note, add_note, fibukonto, debit_betrag, credit_betrag, lvcarea, gl_acct, htparam, artikel, l_ophdr, l_artikel, l_untergrup, l_op, l_lieferant, l_kredit, fa_artikel, fa_op, fa_grup
        nonlocal gl_acct1, art1, gl_acc1


        nonlocal g_list, t_g_list, s_list, gl_acct1, art1, gl_acc1
        nonlocal g_list_list, t_g_list_list, s_list_list

        cost_account:str = ""
        cost_value:decimal = 0
        do_it:bool = False
        s:decimal = 0
        Art1 = Artikel
        Gl_acc1 = Gl_acct
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.nr = 1
        s_list.name = "INVENTORY"
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.nr = 2
        s_list.name = "EXPENSES"
        curr_zeit = get_current_time_in_seconds()

        l_op_obj_list = []
        for l_op, l_ophdr, l_artikel, l_untergrup in db_session.query(L_op, L_ophdr, L_artikel, L_untergrup).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) &  (func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.fibukonto != "")).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                (L_op.pos > 0) &  (L_op.op_art == 3) &  (L_op.loeschflag < 2) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lager_nr > 0)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)

            if l_op.stornogrund != "":

                gl_acct1 = db_session.query(Gl_acct1).filter(
                        (Gl_acct1.fibukonto == l_op.stornogrund)).first()
            else:

                gl_acct1 = db_session.query(Gl_acct1).filter(
                        (Gl_acct1.fibukonto == l_ophdr.fibukonto)).first()
            do_it = None != gl_acct1
            cost_value = 0

            if do_it:
                curr_zeit = curr_zeit + 1
                curr_lschein = l_ophdr.lscheinnr
                curr_note = to_string(l_ophdr.lager_nr, "99") + "-" + curr_lschein + " " + l_artikel.bezeich
                add_note = ";&&5;" + to_string(l_ophdr.lager_nr, "99") + ";" + curr_lschein + ";"
                cost_account = gl_acct1.fibukonto

                gl_acct = db_session.query(Gl_acct).filter(
                        (Gl_acct.fibukonto == l_untergrup.fibukonto)).first()

                if not gl_acct:

                    gl_acct = db_session.query(Gl_acct).filter(
                            (Gl_acct.fibukonto == l_artikel.fibukonto)).first()

                if gl_acct:
                    fibukonto = gl_acct.fibukonto
                    cost_value = cost_value + round (l_op.warenwert, 2)
                    s = s + l_op.warenwert

                    if l_op.warenwert > 0:
                        credit_betrag = round (l_op.warenwert, 2)
                        debit_betrag = 0

                        g_list = query(g_list_list, filters=(lambda g_list :g_list.fibukonto == gl_acct.fibukonto and g_list.lscheinnr == l_op.lscheinnr and g_list.credit != 0), first=True)

                        if not g_list:
                            add_list1(True, 1)
                        else:
                            add_list1(True, 1)

                    elif l_op.warenwert < 0:
                        debit_betrag = - round (l_op.warenwert, 2)
                        credit_betrag = 0

                        g_list = query(g_list_list, filters=(lambda g_list :g_list.fibukonto == gl_acct.fibukonto and g_list.lscheinnr == l_op.lscheinnr and g_list.debit != 0), first=True)

                        if not g_list:
                            add_list1(True, 1)
                        else:
                            add_list1(True, 1)
                else:
                    msg_str2 = msg_str2 + chr(2) + translateExtended ("Chart of Account not defined at stock article", lvcarea, "") + chr(10) + translateExtended ("ArticleNo", lvcarea, "") + " " + to_string(l_artikel.artnr) + " - " + l_artikel.bezeich

            if cost_value != 0:
                curr_zeit = curr_zeit + 1
                fibukonto = cost_account
                curr_lschein = l_ophdr.lscheinnr
                curr_note = to_string(l_ophdr.lager_nr, "99") + " - " + curr_lschein
                add_note = ";&&5;" + to_string(l_ophdr.lager_nr, "99") + ";" + curr_lschein + ";"

                if cost_value > 0:
                    debit_betrag = cost_value
                    credit_betrag = 0

                    g_list = query(g_list_list, filters=(lambda g_list :g_list.fibukonto.lower()  == (cost_account).lower()  and g_list.lscheinnr == l_op.lscheinnr and g_list.debit != 0), first=True)

                    if not g_list:
                        add_list1(True, 2)
                    else:
                        add_list1(False, 2)

                elif cost_value < 0:
                    credit_betrag = - cost_value
                    debit_betrag = 0

                    g_list = query(g_list_list, filters=(lambda g_list :g_list.fibukonto.lower()  == (cost_account).lower()  and g_list.lscheinnr == l_op.lscheinnr and g_list.credit != 0), first=True)

                    if not g_list:
                        add_list1(True, 2)
                    else:
                        add_list1(False, 2)

    def step_two2():

        nonlocal curr_anz, credits, debits, remains, msg_str, msg_str2, msg_str3, msg_str4, msg_str5, t_g_list_list, s_list_list, curr_zeit, curr_lschein, curr_note, add_note, fibukonto, debit_betrag, credit_betrag, lvcarea, gl_acct, htparam, artikel, l_ophdr, l_artikel, l_untergrup, l_op, l_lieferant, l_kredit, fa_artikel, fa_op, fa_grup
        nonlocal gl_acct1, art1, gl_acc1


        nonlocal g_list, t_g_list, s_list, gl_acct1, art1, gl_acc1
        nonlocal g_list_list, t_g_list_list, s_list_list

        cost_value:decimal = 0
        do_it:bool = False
        s:decimal = 0
        wip_acct:str = ""
        Art1 = Artikel
        Gl_acc1 = Gl_acct

        l_op = db_session.query(L_op).filter(
                (L_op.op_art == 2) &  (L_op.loeschflag < 2) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lager_nr > 0) &  (L_op.herkunftflag == 3)).first()

        if not l_op:

            return
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.nr = 3
        s_list.name = "TRANSFORM OUT"
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.nr = 4
        s_list.name = "TRANSFORM IN"
        cost_value = 0
        curr_zeit = get_current_time_in_seconds()

        l_op_obj_list = []
        for l_op, l_ophdr, l_artikel, l_untergrup in db_session.query(L_op, L_ophdr, L_artikel, L_untergrup).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) &  (func.lower(L_ophdr.op_typ) == "STT")).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                (L_op.op_art >= 2) &  (L_op.op_art <= 4) &  (L_op.herkunftflag == 3) &  (L_op.loeschflag < 2) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lager_nr > 0)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)

            if wip_acct == "":

                gl_acct1 = db_session.query(Gl_acct1).filter(
                        (Gl_acct1.fibukonto == l_op.stornogrund)).first()
                do_it = None != gl_acct1

                if not do_it:
                    msg_str3 = msg_str3 + chr(2) + translateExtended ("No G/L WIP Account number found :", lvcarea, "") + " " + l_op.lscheinnr

                    return
            wip_acct = gl_acct1.fibukonto

            if do_it:
                curr_lschein = l_ophdr.lscheinnr
                curr_note = to_string(l_ophdr.lager_nr, "99") + " - " + curr_lschein
                add_note = ";&&6;" + to_string(l_ophdr.lager_nr, "99") + ";" + curr_lschein + ";"

                gl_acct = db_session.query(Gl_acct).filter(
                        (Gl_acct.fibukonto == l_untergrup.fibukonto)).first()

                if not gl_acct:

                    gl_acct = db_session.query(Gl_acct).filter(
                            (Gl_acct.fibukonto == l_artikel.fibukonto)).first()

                if gl_acct:
                    fibukonto = gl_acct.fibukonto
                    s = s + l_op.warenwert

                    if l_op.op_art == 4:
                        credit_betrag = round (l_op.warenwert, 2)
                        debit_betrag = 0

                        g_list = query(g_list_list, filters=(lambda g_list :g_list.fibukonto == gl_acct.fibukonto and g_list.lscheinnr == l_op.lscheinnr and g_list.credit != 0), first=True)

                        if not g_list:
                            curr_zeit = curr_zeit + 1
                            add_list1(True, 3)
                        else:
                            add_list1(False, 3)

                    elif l_op.op_art == 2:
                        curr_note = to_string(l_ophdr.lager_nr, "99") + " - " + l_artikel.bezeich
                        add_note = ";&&6;" + to_string(l_ophdr.lager_nr, "99") + ";" + curr_lschein + ";"
                        cost_value = cost_value + round (l_op.warenwert, 2)
                        debit_betrag = round (l_op.warenwert, 2)
                        credit_betrag = 0
                        add_list1(True, 4)
                else:
                    msg_str4 = msg_str4 + chr(2) + translateExtended ("Chart of Account not defined at stock article", lvcarea, "") + chr(10) + translateExtended ("ArticleNo", lvcarea, "") + " " + to_string(l_artikel.artnr) + " - " + l_artikel.bezeich

        if cost_value > 0:
            curr_zeit = curr_zeit + 1
            fibukonto = wip_acct
            curr_lschein = ""
            curr_note = "WIP Transform IN"
            debit_betrag = cost_value
            credit_betrag = 0
            add_list1(True, 0)
            curr_note = "WIP Transform OUT"
            credit_betrag = cost_value
            debit_betrag = 0
            add_list1(True, 0)

    def step_three():

        nonlocal curr_anz, credits, debits, remains, msg_str, msg_str2, msg_str3, msg_str4, msg_str5, t_g_list_list, s_list_list, curr_zeit, curr_lschein, curr_note, add_note, fibukonto, debit_betrag, credit_betrag, lvcarea, gl_acct, htparam, artikel, l_ophdr, l_artikel, l_untergrup, l_op, l_lieferant, l_kredit, fa_artikel, fa_op, fa_grup
        nonlocal gl_acct1, art1, gl_acc1


        nonlocal g_list, t_g_list, s_list, gl_acct1, art1, gl_acc1
        nonlocal g_list_list, t_g_list_list, s_list_list

        ap_account:str = ""
        ratio:decimal = 0
        note:str = ""
        curr_docu:str = ""
        curr_lschein:str = ""
        op_exist:bool = False
        tot_wert:decimal = 0
        do_it:bool = False
        Art1 = Artikel
        Gl_acc1 = Gl_acct

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 986)).first()
        ap_account = htparam.fchar
        op_exist = False
        curr_lschein = ""
        curr_zeit = get_current_time_in_seconds()

        l_op_obj_list = []
        for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                (L_op.pos > 0) &  (L_op.anzahl != 0) &  (L_op.op_art == 1) &  (L_op.loeschflag < 2) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)

            gl_acct = db_session.query(Gl_acct).filter(
                    (Gl_acct.fibukonto == l_untergrup.fibukonto)).first()

            if not gl_acct:

                gl_acct = db_session.query(Gl_acct).filter(
                        (Gl_acct.fibukonto == l_artikel.fibukonto)).first()

            if gl_acct:
                curr_zeit = curr_zeit + 1

                if curr_lschein == "":
                    curr_lschein = l_op.lscheinnr

                    l_lieferant = db_session.query(L_lieferant).filter(
                            (L_lieferant.lief_nr == l_op.lief_nr)).first()

                    if not l_lieferant:

                        l_kredit = db_session.query(L_kredit).filter(
                                (L_kredit.lscheinnr == l_op.lscheinnr)).first()

                if curr_lschein != l_op.lscheinnr:

                    if l_lieferant:
                        curr_note = curr_lschein + " " + l_lieferant.firma
                    else:
                        curr_note = curr_lschein
                    do_it = True

                    if l_lieferant and l_lieferant.z_code != "":

                        gl_acc1 = db_session.query(Gl_acc1).filter(
                                (Gl_acc1.fibukonto == l_lieferant.z_code)).first()

                        if gl_acc1:
                            do_it = (gl_acc1.fibukonto == ap_account)

                    if not do_it:
                        fibukonto = gl_acc1.fibukonto

                        if tot_wert > 0:
                            credit_betrag = tot_wert
                            debit_betrag = 0
                            add_list(True)

                        elif tot_wert < 0:
                            debit_betrag = - tot_wert
                            credit_betrag = 0
                            add_list(True)
                    else:
                        fibukonto = ap_account

                        for l_kredit in db_session.query(L_kredit).filter(
                                (L_kredit.rgdatum >= from_date) &  (L_kredit.rgdatum <= to_date) &  (func.lower(L_kredit.lscheinnr) == (curr_lschein).lower()) &  (L_kredit.opart >= 0) &  (L_kredit.zahlkonto == 0) &  (L_kredit.saldo != 0)).all():
                            ratio = l_kredit.netto / l_kredit.saldo

                            if l_kredit.netto >= 0:
                                credit_betrag = l_kredit.netto
                                debit_betrag = 0
                                add_list(True)

                            elif l_kredit.netto < 0:
                                debit_betrag = - l_kredit.netto
                                credit_betrag = 0
                                add_list(True)

                    l_lieferant = db_session.query(L_lieferant).filter(
                            (L_lieferant.lief_nr == l_op.lief_nr)).first()

                    if not l_lieferant:

                        l_kredit = db_session.query(L_kredit).filter(
                                (L_kredit.lscheinnr == l_op.lscheinnr)).first()
                    curr_lschein = l_op.lscheinnr
                    op_exist = False
                    tot_wert = 0

                if l_lieferant:
                    curr_note = l_op.lscheinnr + " " + l_artikel.bezeich + "; " + l_lieferant.firma
                else:
                    curr_note = l_op.lscheinnr + " " + l_artikel.bezeich
                add_note = ";&&3;" + to_string(l_op.lager_nr, "99") + ";" + to_string(l_op.lief_nr) + ";" + l_op.docu_nr + ";" + l_op.lscheinnr + ";"
                tot_wert = tot_wert + l_op.warenwert
                fibukonto = gl_acct.fibukonto
                curr_docu = l_op.docu_nr

                if l_op.warenwert >= 0:
                    debit_betrag = round (l_op.warenwert, 2)
                    credit_betrag = 0

                    g_list = query(g_list_list, filters=(lambda g_list :g_list.fibukonto == gl_acct.fibukonto and g_list.lscheinnr == l_op.lscheinnr and g_list.debit != 0), first=True)

                    if not g_list:
                        add_list(True)
                    else:
                        add_list(False)
                    op_exist = True

                elif l_op.warenwert < 0:
                    credit_betrag = - round (l_op.warenwert, 2)
                    debit_betrag = 0

                    g_list = query(g_list_list, filters=(lambda g_list :g_list.fibukonto == gl_acct.fibukonto and g_list.lscheinnr == l_op.lscheinnr and g_list.credit != 0), first=True)

                    if not g_list:
                        add_list(True)
                    else:
                        add_list(False)
                    op_exist = True
            else:
                msg_str5 = msg_str5 + chr(2) + translateExtended ("Chart_of_acct of following inventory item not defined :", lvcarea, "") + chr(10) + to_string(l_artikel.artnr) + " - " + l_artikel.bezeich

        if op_exist:
            curr_zeit = curr_zeit + 1

            if l_lieferant:
                curr_note = curr_lschein + " " + l_lieferant.firma
            else:
                curr_note = curr_lschein
            do_it = True

            if l_lieferant and l_lieferant.z_code != "":

                gl_acc1 = db_session.query(Gl_acc1).filter(
                        (Gl_acc1.fibukonto == l_lieferant.z_code)).first()

                if gl_acc1:
                    do_it = (gl_acc1.fibukonto == ap_account)

            if not do_it:
                fibukonto = gl_acc1.fibukonto

                if tot_wert > 0:
                    credit_betrag = tot_wert
                    debit_betrag = 0
                    add_list(True)

                elif tot_wert < 0:
                    debit_betrag = - tot_wert
                    credit_betrag = 0
                    add_list(True)
            else:
                fibukonto = ap_account

                for l_kredit in db_session.query(L_kredit).filter(
                        (L_kredit.rgdatum >= from_date) &  (L_kredit.rgdatum <= to_date) &  (func.lower(L_kredit.lscheinnr) == (curr_lschein).lower()) &  (L_kredit.opart >= 0) &  (L_kredit.zahlkonto == 0) &  (L_kredit.saldo != 0)).all():
                    ratio = l_kredit.netto / l_kredit.saldo

                    if l_kredit.netto >= 0:
                        credit_betrag = l_kredit.netto
                        debit_betrag = 0
                        add_list(True)

                    elif l_kredit.netto < 0:
                        debit_betrag = - l_kredit.netto
                        credit_betrag = 0
                        add_list(True)

    def step_three_fa():

        nonlocal curr_anz, credits, debits, remains, msg_str, msg_str2, msg_str3, msg_str4, msg_str5, t_g_list_list, s_list_list, curr_zeit, curr_lschein, curr_note, add_note, fibukonto, debit_betrag, credit_betrag, lvcarea, gl_acct, htparam, artikel, l_ophdr, l_artikel, l_untergrup, l_op, l_lieferant, l_kredit, fa_artikel, fa_op, fa_grup
        nonlocal gl_acct1, art1, gl_acc1


        nonlocal g_list, t_g_list, s_list, gl_acct1, art1, gl_acc1
        nonlocal g_list_list, t_g_list_list, s_list_list

        ap_account:str = ""
        note:str = ""
        curr_docu:str = ""
        curr_lschein:str = ""
        op_exist:bool = False
        Art1 = Artikel
        Gl_acc1 = Gl_acct

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 887)).first()

        if htparam.fchar != "":
            ap_account = htparam.fchar
        else:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 986)).first()
            ap_account = htparam.fchar
        op_exist = False
        curr_lschein = ""
        curr_zeit = get_current_time_in_seconds()

        fa_op_obj_list = []
        for fa_op, l_lieferant, fa_artikel in db_session.query(Fa_op, L_lieferant, Fa_artikel).join(L_lieferant,(L_lieferant.lief_nr == Fa_op.lief_nr)).join(Fa_artikel,(Fa_artikel.nr == Fa_op.nr)).filter(
                (Fa_op.anzahl != 0) &  (Fa_op.loeschflag < 2) &  (Fa_op.opart == 1) &  (Fa_op.datum >= from_date) &  (Fa_op.datum <= to_date)).all():
            if fa_op._recid in fa_op_obj_list:
                continue
            else:
                fa_op_obj_list.append(fa_op._recid)

            fa_grup = db_session.query(Fa_grup).filter(
                    (Fa_grup.gnr == fa_artikel.subgrp) &  (Fa_grup.flag == 1)).first()

            gl_acct = db_session.query(Gl_acct).filter(
                    (Gl_acct.fibukonto == fa_grup.fibukonto)).first()

            if not gl_acct:

                gl_acct = db_session.query(Gl_acct).filter(
                        (Gl_acct.fibukonto == fa_artikel.fibukonto)).first()
            curr_zeit = curr_zeit + 1
            add_note = ";&&9;" + trim(to_string(fa_op.nr, ">>>99")) + ";" + fa_op.docu_nr + ";" + fa_op.lscheinnr + ";"

            if curr_lschein == "":
                curr_lschein = fa_op.lscheinnr
                curr_note = curr_lschein + " - " + l_lieferant.firma

            if curr_lschein != fa_op.lscheinnr:
                fibukonto = ap_account

                for l_kredit in db_session.query(L_kredit).filter(
                        (L_kredit.rgdatum >= from_date) &  (L_kredit.rgdatum <= to_date) &  (func.lower(L_kredit.lscheinnr) == (curr_lschein).lower()) &  (L_kredit.opart >= 0) &  (L_kredit.zahlkonto == 0) &  (L_kredit.saldo != 0)).all():

                    if l_kredit.netto >= 0:
                        credit_betrag = l_kredit.netto
                        debit_betrag = 0
                        add_list(True)

                    elif l_kredit.netto < 0:
                        debit_betrag = - l_kredit.netto
                        credit_betrag = 0
                        add_list(True)
                curr_lschein = fa_op.lscheinnr
                curr_note = curr_lschein + " - " + l_lieferant.firma
                op_exist = False
            fibukonto = gl_acct.fibukonto
            curr_docu = fa_op.docu_nr

            if fa_op.warenwert >= 0:
                debit_betrag = round (fa_op.warenwert, 2)
                credit_betrag = 0

                g_list = query(g_list_list, filters=(lambda g_list :g_list.fibukonto == gl_acct.fibukonto and g_list.lscheinnr == fa_op.lscheinnr and g_list.debit != 0), first=True)

                if not g_list:
                    add_list(True)
                else:
                    add_list(False)
                op_exist = True

            elif fa_op.warenwert < 0:
                credit_betrag = - round (fa_op.warenwert, 2)
                debit_betrag = 0

                g_list = query(g_list_list, filters=(lambda g_list :g_list.fibukonto == gl_acct.fibukonto and g_list.lscheinnr == fa_op.lscheinnr and g_list.credit != 0), first=True)

                if not g_list:
                    add_list(True)
                else:
                    add_list(False)
                op_exist = True

        if op_exist:
            curr_zeit = curr_zeit + 1
            fibukonto = ap_account

            for l_kredit in db_session.query(L_kredit).filter(
                    (L_kredit.rgdatum >= from_date) &  (L_kredit.rgdatum <= to_date) &  (func.lower(L_kredit.lscheinnr) == (curr_lschein).lower()) &  (L_kredit.opart >= 0) &  (L_kredit.zahlkonto == 0) &  (L_kredit.saldo != 0)).all():

                if l_kredit.netto >= 0:
                    credit_betrag = l_kredit.netto
                    debit_betrag = 0
                    add_list(True)

                elif l_kredit.netto < 0:
                    debit_betrag = - l_kredit.netto
                    credit_betrag = 0
                    add_list(True)

    def add_list(create_it:bool):

        nonlocal curr_anz, credits, debits, remains, msg_str, msg_str2, msg_str3, msg_str4, msg_str5, t_g_list_list, s_list_list, curr_zeit, curr_lschein, curr_note, add_note, fibukonto, debit_betrag, credit_betrag, lvcarea, gl_acct, htparam, artikel, l_ophdr, l_artikel, l_untergrup, l_op, l_lieferant, l_kredit, fa_artikel, fa_op, fa_grup
        nonlocal gl_acct1, art1, gl_acc1


        nonlocal g_list, t_g_list, s_list, gl_acct1, art1, gl_acc1
        nonlocal g_list_list, t_g_list_list, s_list_list


        curr_anz = curr_anz + 1

        if create_it:
            g_list = G_list()
            g_list_list.append(g_list)

            g_list.fibukonto = fibukonto
            g_list.lscheinnr = curr_lschein
            g_list.bemerk = curr_note
            g_list.add_note = add_note
        g_list.debit = g_list.debit + debit_betrag
        g_list.credit = g_list.credit + credit_betrag
        g_list.userinit = user_init
        g_list.zeit = curr_zeit
        g_list.duplicate = False
        credits = credits + credit_betrag
        debits = debits + debit_betrag
        remains = debits - credits
        debit_betrag = 0
        credit_betrag = 0

    def add_list1(create_it:bool, nr:int):

        nonlocal curr_anz, credits, debits, remains, msg_str, msg_str2, msg_str3, msg_str4, msg_str5, t_g_list_list, s_list_list, curr_zeit, curr_lschein, curr_note, add_note, fibukonto, debit_betrag, credit_betrag, lvcarea, gl_acct, htparam, artikel, l_ophdr, l_artikel, l_untergrup, l_op, l_lieferant, l_kredit, fa_artikel, fa_op, fa_grup
        nonlocal gl_acct1, art1, gl_acc1


        nonlocal g_list, t_g_list, s_list, gl_acct1, art1, gl_acc1
        nonlocal g_list_list, t_g_list_list, s_list_list

        if nr > 0:

            s_list = query(s_list_list, filters=(lambda s_list :s_list.nr == nr), first=True)
            s_list.debit = s_list.debit + debit_betrag
            s_list.credit = s_list.credit + credit_betrag
        curr_anz = curr_anz + 1

        if create_it:
            g_list = G_list()
            g_list_list.append(g_list)

            g_list.fibukonto = fibukonto
            g_list.lscheinnr = curr_lschein
            g_list.bemerk = curr_note
            g_list.add_note = add_note
        g_list.debit = g_list.debit + debit_betrag
        g_list.credit = g_list.credit + credit_betrag
        g_list.userinit = user_init
        g_list.zeit = curr_zeit
        g_list.duplicate = False
        credits = credits + credit_betrag
        debits = debits + debit_betrag
        remains = debits - credits
        debit_betrag = 0
        credit_betrag = 0

    if link_out:

        if from_grp == 0:
            step_two()
        else:
            step_two1()

        if from_grp <= 1:
            step_two2()

    elif link_in:
        step_three()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 329)).first()

        if htparam.flogical :
            step_three_fa()

    for g_list in query(g_list_list):
        gl_acct1 = db_session.query(Gl_acct1).filter((Gl_acct1.fibukonto == g_list.fibukonto)).first()
        if not gl_acct1:
            continue

        t_g_list = T_g_list()
        t_g_list_list.append(t_g_list)

        buffer_copy(g_list, t_g_list)
        t_g_list.acct_fibukonto = gl_acct1.fibukonto
        t_g_list.bezeich = gl_acct1.bezeich

    return generate_output()