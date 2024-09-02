from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Gl_acct, Bediener, L_lager, L_ophdr, L_artikel, L_op, L_untergrup, Parameters

def cancel_stockout_btn_gobl(from_grp:int, mi_alloc_chk:bool, mi_article_chk:bool, mi_docu_chk:bool, mi_date_chk:bool, from_lager:int, to_lager:int, from_date:date, to_date:date, from_art:int, to_art:int, show_price:bool, cost_acct:str, mattype:int):
    it_exist = False
    str_list_list = []
    i:int = 0
    tot_anz:decimal = 0
    tot_amount:decimal = 0
    preis:decimal = 0
    wert:decimal = 0
    long_digit:bool = False
    htparam = gl_acct = bediener = l_lager = l_ophdr = l_artikel = l_op = l_untergrup = parameters = None

    s_list = str_list = gl_acct1 = usr = None

    s_list_list, S_list = create_model("S_list", {"fibu":str, "cost_center":str, "bezeich":str, "cost":decimal})
    str_list_list, Str_list = create_model("Str_list", {"fibu":str, "other_fibu":bool, "op_recid":int, "lscheinnr":str, "s":str})

    Gl_acct1 = Gl_acct
    Usr = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal it_exist, str_list_list, i, tot_anz, tot_amount, preis, wert, long_digit, htparam, gl_acct, bediener, l_lager, l_ophdr, l_artikel, l_op, l_untergrup, parameters
        nonlocal gl_acct1, usr


        nonlocal s_list, str_list, gl_acct1, usr
        nonlocal s_list_list, str_list_list
        return {"it_exist": it_exist, "str-list": str_list_list}

    def create_lista():

        nonlocal it_exist, str_list_list, i, tot_anz, tot_amount, preis, wert, long_digit, htparam, gl_acct, bediener, l_lager, l_ophdr, l_artikel, l_op, l_untergrup, parameters
        nonlocal gl_acct1, usr


        nonlocal s_list, str_list, gl_acct1, usr
        nonlocal s_list_list, str_list_list

        t_anz:decimal = 0
        t_val:decimal = 0
        curr_artnr:int = 0
        lschein:str = ""
        cost_bezeich:str = ""
        fibukonto:str = ""
        do_it:bool = False
        cc_code:int = 0
        other_fibu:bool = False
        create_it:bool = False
        usrid:str = ""
        i:int = 0
        reason:str = ""
        str_time:str = ""
        str1:str = ""
        acct_no:str = ""
        Gl_acct1 = Gl_acct
        Usr = Bediener
        it_exist = False
        str_list_list.clear()
        s_list_list.clear()
        tot_anz = 0
        tot_amount = 0
        do_it = True

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():
            do_it = True
            curr_artnr = 0
            usrid = ""
            reason = ""
            str_time = ""
            acct_no = ""

            l_op_obj_list = []
            for l_op, l_ophdr, gl_acct, l_artikel in db_session.query(L_op, L_ophdr, Gl_acct, L_artikel).join(L_ophdr,(func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.lscheinnr == L_op.lscheinnr) &  (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == l_ophdr.fibukonto)).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                    (L_op.lager_nr == l_lager.lager_nr) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  (L_op.anzahl != 0) &  (L_op.op_art == 3) &  (L_op.loeschflag == 2)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                usr = db_session.query(Usr).filter(
                        (Usr.nr == l_op.fuellflag)).first()

                if usr:
                    usrid = usr.userinit
                else:
                    usrid = "??"
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == "reason":
                        reason = entry(1, str1, ":")

                    elif entry(0, str1, ":") == "Time":
                        str_time = to_string(to_int(entry(1, str1, ":")) , "HH:MM:SS")
                    else:
                        acct_no = str1

                if show_price:
                    preis = l_op.einzelpreis
                    wert = l_op.warenwert
                it_exist = True
                other_fibu = False

                if acct_no != "":

                    gl_acct1 = db_session.query(Gl_acct1).filter(
                            (Gl_acct1.fibukonto == l_op.stornogrund)).first()

                    if gl_acct1:
                        other_fibu = True

                if other_fibu:
                    cc_code = get_costcenter_code(gl_acct1.fibukonto)
                else:
                    cc_code = get_costcenter_code(gl_acct.fibukonto)

                if lschein == "":
                    lschein = l_op.lscheinnr

                if other_fibu:
                    fibukonto = gl_acct1.fibukonto
                    cost_bezeich = gl_acct1.bezeich

                    if cost_acct == "":
                        create_it = True
                    else:
                        create_it = (cost_acct == fibukonto)
                else:
                    fibukonto = gl_acct.fibukonto
                    cost_bezeich = gl_acct.bezeich

                    if cost_acct == "":
                        create_it = True
                    else:
                        create_it = (cost_acct == fibukonto)

                if curr_artnr == 0:
                    curr_artnr = l_op.artnr

                if (curr_artnr != l_op.artnr) and t_anz != 0:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,45 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + "Subtotal "
                    for i in range(1,23 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
                    for i in range(1,14 + 1) :
                        str_list.s = str_list.s + " "

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9")
                    t_anz = 0
                    t_val = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    lschein = l_op.lscheinnr
                    curr_artnr = l_op.artnr

                if do_it:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.s = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(24)")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    do_it = False

                if create_it:

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.fibu = fibukonto
                        s_list.bezeich = cost_bezeich

                        if cc_code != 0:
                            s_list.bezeich = to_string(cc_code, "9999 ") + s_list.bezeich
                    s_list.cost = s_list.cost + wert
                    t_anz = t_anz + l_op.anzahl
                    t_val = t_val + wert
                    tot_anz = tot_anz + l_op.anzahl
                    tot_amount = tot_amount + wert
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.fibu = fibukonto
                    str_list.other_fibu = other_fibu
                    str_list.op_recid = l_op._recid

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_op.anzahl, "->,>>>,>>9.999") + to_string(preis, ">>>,>>>,>>9.99") + to_string(wert, "->>,>>>,>>9.99") + to_string(l_op.lscheinnr, "x(12)") + to_string(usrid, "x(2)") + to_string(str_time, "x(8)") + to_string(reason, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_op.anzahl, "->,>>>,>>9.999") + to_string(preis, ">,>>>>,>>>,>>9") + to_string(wert, "->,>>>,>>>,>>9") + to_string(l_op.lscheinnr, "x(12)") + to_string(usrid, "x(2)") + to_string(str_time, "x(8)") + to_string(reason, "x(24)")

        if t_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,45 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "Subtotal "
            for i in range(1,23 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
            for i in range(1,14 + 1) :
                str_list.s = str_list.s + " "

            if not long_digit:
                str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,23 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.999")
        for i in range(1,12 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("", "x(8)") + to_string("SUMMARY OF EXPENSES", "x(30)")
        tot_amount = 0

        for s_list in query(s_list_list):
            str_list = Str_list()
            str_list_list.append(str_list)


            if not long_digit:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(32)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->>,>>>,>>9.99")
            else:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(32)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->,>>>,>>>,>>9")
            tot_amount = tot_amount + s_list.cost
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,49 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9")

    def create_listb():

        nonlocal it_exist, str_list_list, i, tot_anz, tot_amount, preis, wert, long_digit, htparam, gl_acct, bediener, l_lager, l_ophdr, l_artikel, l_op, l_untergrup, parameters
        nonlocal gl_acct1, usr


        nonlocal s_list, str_list, gl_acct1, usr
        nonlocal s_list_list, str_list_list

        t_anz:decimal = 0
        t_val:decimal = 0
        curr_artnr:int = 0
        lschein:str = ""
        cost_bezeich:str = ""
        fibukonto:str = ""
        do_it:bool = False
        cc_code:int = 0
        other_fibu:bool = False
        create_it:bool = False
        usrid:str = ""
        i:int = 0
        reason:str = ""
        str_time:str = ""
        str1:str = ""
        acct_no:str = ""
        Gl_acct1 = Gl_acct
        Usr = Bediener
        it_exist = False
        str_list_list.clear()
        s_list_list.clear()
        tot_anz = 0
        tot_amount = 0
        do_it = True

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():
            do_it = True
            curr_artnr = 0
            usrid = ""
            reason = ""
            str_time = ""
            acct_no = ""

            l_op_obj_list = []
            for l_op, l_ophdr, gl_acct, l_artikel in db_session.query(L_op, L_ophdr, Gl_acct, L_artikel).join(L_ophdr,(func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.lscheinnr == L_op.lscheinnr) &  (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == l_ophdr.fibukonto)).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                    (L_op.lager_nr == l_lager.lager_nr) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  (L_op.anzahl != 0) &  (L_op.op_art == 3) &  (L_op.loeschflag == 2)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                usr = db_session.query(Usr).filter(
                        (Usr.nr == l_op.fuellflag)).first()

                if usr:
                    usrid = usr.userinit
                else:
                    usrid = "??"
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == "reason":
                        reason = entry(1, str1, ":")

                    elif entry(0, str1, ":") == "Time":
                        str_time = to_string(to_int(entry(1, str1, ":")) , "HH:MM:SS")
                    else:
                        acct_no = str1

                if show_price:
                    preis = l_op.einzelpreis
                    wert = l_op.warenwert
                it_exist = True
                other_fibu = False

                if acct_no != "":

                    gl_acct1 = db_session.query(Gl_acct1).filter(
                            (Gl_acct1.fibukonto == l_op.stornogrund)).first()

                    if gl_acct1:
                        other_fibu = True

                if other_fibu:
                    cc_code = get_costcenter_code(gl_acct1.fibukonto)
                else:
                    cc_code = get_costcenter_code(gl_acct.fibukonto)

                if other_fibu:
                    fibukonto = gl_acct1.fibukonto
                    cost_bezeich = gl_acct1.bezeich

                    if cost_acct == "":
                        create_it = True
                    else:
                        create_it = (cost_acct == fibukonto)
                else:
                    fibukonto = gl_acct.fibukonto
                    cost_bezeich = gl_acct.bezeich

                    if cost_acct == "":
                        create_it = True
                    else:
                        create_it = (cost_acct == fibukonto)

                if lschein == "":
                    lschein = l_op.lscheinnr

                if (lschein != l_op.lscheinnr) and t_anz != 0:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,45 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + "Subtotal "
                    for i in range(1,23 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
                    for i in range(1,14 + 1) :
                        str_list.s = str_list.s + " "

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9")
                    t_anz = 0
                    t_val = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    lschein = l_op.lscheinnr
                    curr_artnr = l_op.artnr

                if do_it:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.s = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(24)")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    do_it = False

                if create_it:

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.fibu = fibukonto
                        s_list.bezeich = cost_bezeich

                        if cc_code != 0:
                            s_list.bezeich = to_string(cc_code, "9999 ") + s_list.bezeich
                    s_list.cost = s_list.cost + wert
                    t_anz = t_anz + l_op.anzahl
                    t_val = t_val + wert
                    tot_anz = tot_anz + l_op.anzahl
                    tot_amount = tot_amount + wert
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.fibu = fibukonto
                    str_list.other_fibu = other_fibu
                    str_list.op_recid = l_op._recid

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_op.anzahl, "->,>>>,>>9.999") + to_string(preis, ">>>,>>>,>>9.99") + to_string(wert, "->>,>>>,>>9.99") + to_string(l_op.lscheinnr, "x(12)") + to_string(usrid, "x(2)") + to_string(str_time, "x(8)") + to_string(reason, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_op.anzahl, "->,>>>,>>9.999") + to_string(preis, ">>,>>>,>>>,>>9") + to_string(wert, "->,>>>,>>>,>>9") + to_string(l_op.lscheinnr, "x(12)") + to_string(usrid, "x(2)") + to_string(str_time, "x(8)") + to_string(reason, "x(24)")

        if t_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,45 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "Subtotal "
            for i in range(1,23 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
            for i in range(1,14 + 1) :
                str_list.s = str_list.s + " "

            if not long_digit:
                str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,23 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.999")
        for i in range(1,14 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("", "x(8)") + to_string("SUMMARY OF EXPENSES", "x(30)")
        tot_amount = 0

        for s_list in query(s_list_list):
            str_list = Str_list()
            str_list_list.append(str_list)


            if not long_digit:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(32)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->>,>>>,>>9.99")
            else:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(32)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->,>>>,>>>,>>9")
            tot_amount = tot_amount + s_list.cost
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,49 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9")

    def create_listc():

        nonlocal it_exist, str_list_list, i, tot_anz, tot_amount, preis, wert, long_digit, htparam, gl_acct, bediener, l_lager, l_ophdr, l_artikel, l_op, l_untergrup, parameters
        nonlocal gl_acct1, usr


        nonlocal s_list, str_list, gl_acct1, usr
        nonlocal s_list_list, str_list_list

        t_anz:decimal = 0
        t_val:decimal = 0
        curr_artnr:int = 0
        lschein:str = ""
        datum:date = None
        cost_bezeich:str = ""
        fibukonto:str = ""
        do_it:bool = False
        cc_code:int = 0
        other_fibu:bool = False
        create_it:bool = False
        usrid:str = ""
        i:int = 0
        reason:str = ""
        str_time:str = ""
        str1:str = ""
        acct_no:str = ""
        Gl_acct1 = Gl_acct
        Usr = Bediener
        it_exist = False
        str_list_list.clear()
        s_list_list.clear()
        tot_anz = 0
        tot_amount = 0
        do_it = True

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():
            do_it = True
            curr_artnr = 0
            usrid = ""
            reason = ""
            str_time = ""
            acct_no = ""

            l_op_obj_list = []
            for l_op, l_ophdr, gl_acct, l_artikel in db_session.query(L_op, L_ophdr, Gl_acct, L_artikel).join(L_ophdr,(func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.lscheinnr == L_op.lscheinnr) &  (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == l_ophdr.fibukonto)).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                    (L_op.lager_nr == l_lager.lager_nr) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  (L_op.anzahl != 0) &  (L_op.op_art == 3) &  (L_op.loeschflag == 2)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                usr = db_session.query(Usr).filter(
                        (Usr.nr == l_op.fuellflag)).first()

                if usr:
                    usrid = usr.userinit
                else:
                    usrid = "??"
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == "reason":
                        reason = entry(1, str1, ":")

                    elif entry(0, str1, ":") == "Time":
                        str_time = to_string(to_int(entry(1, str1, ":")) , "HH:MM:SS")
                    else:
                        acct_no = str1

                if show_price:
                    preis = l_op.einzelpreis
                    wert = l_op.warenwert
                it_exist = True
                other_fibu = False

                if acct_no != "":

                    gl_acct1 = db_session.query(Gl_acct1).filter(
                            (Gl_acct1.fibukonto == l_op.stornogrund)).first()

                    if gl_acct1:
                        other_fibu = True

                if other_fibu:
                    cc_code = get_costcenter_code(gl_acct1.fibukonto)
                else:
                    cc_code = get_costcenter_code(gl_acct.fibukonto)

                if other_fibu:
                    fibukonto = gl_acct1.fibukonto
                    cost_bezeich = gl_acct1.bezeich

                    if cost_acct == "":
                        create_it = True
                    else:
                        create_it = (cost_acct == fibukonto)
                else:
                    fibukonto = gl_acct.fibukonto
                    cost_bezeich = gl_acct.bezeich

                    if cost_acct == "":
                        create_it = True
                    else:
                        create_it = (cost_acct == fibukonto)

                if datum == None:
                    datum = l_op.datum

                if (datum != l_op.datum) and t_anz != 0:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,45 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + "Subtotal "
                    for i in range(1,23 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
                    for i in range(1,14 + 1) :
                        str_list.s = str_list.s + " "

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9")
                    t_anz = 0
                    t_val = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    lschein = l_op.lscheinnr
                    datum = l_op.datum
                    curr_artnr = l_op.artnr

                if do_it:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.s = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(24)")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    do_it = False

                if create_it:

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.fibu = fibukonto
                        s_list.bezeich = cost_bezeich

                        if cc_code != 0:
                            s_list.bezeich = to_string(cc_code, "9999 ") + s_list.bezeich
                    s_list.cost = s_list.cost + wert
                    t_anz = t_anz + l_op.anzahl
                    t_val = t_val + wert
                    tot_anz = tot_anz + l_op.anzahl
                    tot_amount = tot_amount + wert
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.fibu = fibukonto
                    str_list.other_fibu = other_fibu
                    str_list.op_recid = l_op._recid

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_op.anzahl, "->,>>>,>>9.999") + to_string(preis, ">>>,>>>,>>9.99") + to_string(wert, "->>,>>>,>>9.99") + to_string(l_op.lscheinnr, "x(12)") + to_string(usrid, "x(2)") + to_string(str_time, "x(8)") + to_string(reason, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_op.anzahl, "->,>>>,>>9.999") + to_string(preis, ">>,>>>,>>>,>>9") + to_string(wert, "->,>>>,>>>,>>9") + to_string(l_op.lscheinnr, "x(12)") + to_string(usrid, "x(2)") + to_string(str_time, "x(8)") + to_string(reason, "x(24)")

        if t_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,45 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "Subtotal "
            for i in range(1,23 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
            for i in range(1,14 + 1) :
                str_list.s = str_list.s + " "

            if not long_digit:
                str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,23 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.999")
        for i in range(1,12 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("", "x(8)") + to_string("SUMMARY OF EXPENSES", "x(30)")
        tot_amount = 0

        for s_list in query(s_list_list):
            str_list = Str_list()
            str_list_list.append(str_list)


            if not long_digit:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(32)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->>,>>>,>>9.99")
            else:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(32)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->,>>>,>>>,>>9")
            tot_amount = tot_amount + s_list.cost
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,49 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9")

    def create_list():

        nonlocal it_exist, str_list_list, i, tot_anz, tot_amount, preis, wert, long_digit, htparam, gl_acct, bediener, l_lager, l_ophdr, l_artikel, l_op, l_untergrup, parameters
        nonlocal gl_acct1, usr


        nonlocal s_list, str_list, gl_acct1, usr
        nonlocal s_list_list, str_list_list

        t_anz:decimal = 0
        t_val:decimal = 0
        lschein:str = ""
        cost_bezeich:str = ""
        fibukonto:str = ""
        do_it:bool = False
        cc_code:int = 0
        other_fibu:bool = False
        create_it:bool = False
        curr_fibu:str = ""
        usrid:str = ""
        i:int = 0
        reason:str = ""
        str_time:str = ""
        str1:str = ""
        acct_no:str = ""
        Gl_acct1 = Gl_acct
        Usr = Bediener
        it_exist = False
        str_list_list.clear()
        s_list_list.clear()
        tot_anz = 0
        tot_amount = 0

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():
            do_it = True
            usrid = ""
            reason = ""
            str_time = ""
            acct_no = ""

            l_op_obj_list = []
            for l_op, l_ophdr, gl_acct, l_artikel in db_session.query(L_op, L_ophdr, Gl_acct, L_artikel).join(L_ophdr,(func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.lscheinnr == L_op.lscheinnr) &  (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == l_ophdr.fibukonto)).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                    (L_op.lager_nr == l_lager.lager_nr) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  (L_op.anzahl != 0) &  (L_op.op_art == 3) &  (L_op.loeschflag == 2)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                usr = db_session.query(Usr).filter(
                        (Usr.nr == l_op.fuellflag)).first()

                if usr:
                    usrid = usr.userinit
                else:
                    usrid = "??"
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == "reason":
                        reason = entry(1, str1, ":")

                    elif entry(0, str1, ":") == "Time":
                        str_time = to_string(to_int(entry(1, str1, ":")) , "HH:MM:SS")
                    else:
                        acct_no = str1

                if show_price:
                    preis = l_op.einzelpreis
                    wert = l_op.warenwert
                it_exist = True
                other_fibu = False

                if acct_no != "":

                    gl_acct1 = db_session.query(Gl_acct1).filter(
                            (Gl_acct1.fibukonto == l_op.stornogrund)).first()

                    if gl_acct1:
                        other_fibu = True

                if other_fibu:
                    cc_code = get_costcenter_code(gl_acct1.fibukonto)
                else:
                    cc_code = get_costcenter_code(gl_acct.fibukonto)

                if lschein == "":
                    lschein = l_op.lscheinnr

                if other_fibu:
                    fibukonto = gl_acct1.fibukonto
                    cost_bezeich = gl_acct1.bezeich

                    if cost_acct == "":
                        create_it = True
                    else:
                        create_it = (cost_acct == fibukonto)
                else:
                    fibukonto = gl_acct.fibukonto
                    cost_bezeich = gl_acct.bezeich

                    if cost_acct == "":
                        create_it = True
                    else:
                        create_it = (cost_acct == fibukonto)

                if curr_fibu == "":
                    curr_fibu = fibukonto

                if curr_fibu.lower()  != (fibukonto).lower()  and t_anz != 0:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,45 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + "Subtotal "
                    for i in range(1,23 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
                    for i in range(1,14 + 1) :
                        str_list.s = str_list.s + " "

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9")
                    t_anz = 0
                    t_val = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    lschein = l_op.lscheinnr
                    curr_fibu = fibukonto

                if do_it:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.s = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(24)")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    do_it = False

                if create_it:

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.fibu = fibukonto
                        s_list.bezeich = cost_bezeich

                        if cc_code != 0:
                            s_list.bezeich = to_string(cc_code, "9999 ") + s_list.bezeich
                    s_list.cost = s_list.cost + wert
                    t_anz = t_anz + l_op.anzahl
                    t_val = t_val + wert
                    tot_anz = tot_anz + l_op.anzahl
                    tot_amount = tot_amount + wert
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.fibu = fibukonto
                    str_list.other_fibu = other_fibu
                    str_list.op_recid = l_op._recid

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_op.anzahl, "->,>>>,>>9.999") + to_string(preis, ">>>,>>>,>>9.99") + to_string(wert, "->>,>>>,>>9.99") + to_string(l_op.lscheinnr, "x(12)") + to_string(usrid, "x(2)") + to_string(str_time, "x(8)") + to_string(reason, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_op.anzahl, "->,>>>,>>9.999") + to_string(preis, ">>,>>>,>>>,>>9") + to_string(wert, "->,>>>,>>>,>>9") + to_string(l_op.lscheinnr, "x(12)") + to_string(usrid, "x(2)") + to_string(str_time, "x(8)") + to_string(reason, "x(24)")

        if t_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,45 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "Subtotal "
            for i in range(1,23 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
            for i in range(1,14 + 1) :
                str_list.s = str_list.s + " "

            if not long_digit:
                str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,23 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.999")
        for i in range(1,12 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("", "x(8)") + to_string("SUMMARY OF EXPENSES", "x(30)")
        tot_amount = 0

        for s_list in query(s_list_list):
            str_list = Str_list()
            str_list_list.append(str_list)


            if not long_digit:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(32)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->>,>>>,>>9.99")
            else:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(32)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->,>>>,>>>,>>9")
            tot_amount = tot_amount + s_list.cost
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,49 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9")

    def create_list1():

        nonlocal it_exist, str_list_list, i, tot_anz, tot_amount, preis, wert, long_digit, htparam, gl_acct, bediener, l_lager, l_ophdr, l_artikel, l_op, l_untergrup, parameters
        nonlocal gl_acct1, usr


        nonlocal s_list, str_list, gl_acct1, usr
        nonlocal s_list_list, str_list_list

        t_anz:decimal = 0
        t_val:decimal = 0
        lschein:str = ""
        cost_bezeich:str = ""
        fibukonto:str = ""
        do_it:bool = False
        create_it:bool = False
        cc_code:int = 0
        other_fibu:bool = False
        grp1:int = 0
        grp2:int = 1
        curr_fibu:str = ""
        usrid:str = ""
        i:int = 0
        reason:str = ""
        str_time:str = ""
        str1:str = ""
        acct_no:str = ""
        Usr = Bediener
        Gl_acct1 = Gl_acct
        it_exist = False
        str_list_list.clear()
        s_list_list.clear()

        if mattype == 1:
            grp2 = 0

        elif mattype == 2:
            grp1 = 1
        tot_anz = 0
        tot_amount = 0

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():
            do_it = True
            usrid = ""
            reason = ""
            str_time = ""
            acct_no = ""

            l_op_obj_list = []
            for l_op, l_ophdr, gl_acct, l_artikel, l_untergrup in db_session.query(L_op, L_ophdr, Gl_acct, L_artikel, L_untergrup).join(L_ophdr,(func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.lscheinnr == L_op.lscheinnr) &  (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == l_ophdr.fibukonto)).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum) &  ((L_untergrup.betriebsnr >= grp1) &  (L_untergrup.betriebsnr <= grp2))).filter(
                    (L_op.lager_nr == l_lager.lager_nr) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  (L_op.anzahl != 0) &  (L_op.op_art == 3) &  (L_op.loeschflag == 2)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                usr = db_session.query(Usr).filter(
                        (Usr.nr == l_op.fuellflag)).first()

                if usr:
                    usrid = usr.userinit
                else:
                    usrid = "??"
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == "reason":
                        reason = entry(1, str1, ":")

                    elif entry(0, str1, ":") == "Time":
                        str_time = to_string(to_int(entry(1, str1, ":")) , "HH:MM:SS")
                    else:
                        acct_no = str1

                if show_price:
                    preis = l_op.einzelpreis
                    wert = l_op.warenwert
                it_exist = True
                other_fibu = False

                if acct_no != "":

                    gl_acct1 = db_session.query(Gl_acct1).filter(
                            (Gl_acct1.fibukonto == l_op.stornogrund)).first()

                    if gl_acct1:
                        other_fibu = True

                if other_fibu:
                    cc_code = get_costcenter_code(gl_acct1.fibukonto)
                else:
                    cc_code = get_costcenter_code(gl_acct.fibukonto)

                if lschein == "":
                    lschein = l_op.lscheinnr

                if other_fibu:
                    fibukonto = gl_acct1.fibukonto
                    cost_bezeich = gl_acct1.bezeich

                    if cost_acct == "":
                        create_it = True
                    else:
                        create_it = (cost_acct == fibukonto)
                else:
                    fibukonto = gl_acct.fibukonto
                    cost_bezeich = gl_acct.bezeich

                    if cost_acct == "":
                        create_it = True
                    else:
                        create_it = (cost_acct == fibukonto)

                if curr_fibu == "":
                    curr_fibu = fibukonto

                if curr_fibu.lower()  != (fibukonto).lower()  and t_anz != 0:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,45 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + "Subtotal "
                    for i in range(1,23 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
                    for i in range(1,14 + 1) :
                        str_list.s = str_list.s + " "

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9")
                    t_anz = 0
                    t_val = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    lschein = l_op.lscheinnr
                    curr_fibu = fibukonto

                if do_it:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.s = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(30)")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    do_it = False

                if create_it:

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.fibu = fibukonto
                        s_list.bezeich = cost_bezeich

                        if cc_code != 0:
                            s_list.bezeich = to_string(cc_code, "9999 ") + s_list.bezeich
                    s_list.cost = s_list.cost + wert
                    t_anz = t_anz + l_op.anzahl
                    t_val = t_val + wert
                    tot_anz = tot_anz + l_op.anzahl
                    tot_amount = tot_amount + wert
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.other_fibu = other_fibu
                    str_list.fibu = fibukonto
                    str_list.op_recid = l_op._recid

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_op.anzahl, "->,>>>,>>9.999") + to_string(preis, ">>>,>>>,>>9.99") + to_string(wert, "->>,>>>,>>9.99") + to_string(l_op.lscheinnr, "x(12)") + to_string(usrid, "x(2)") + to_string(str_time, "x(8)") + to_string(reason, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_op.anzahl, "->,>>>,>>9.999") + to_string(preis, ">>,>>>,>>>,>>9") + to_string(wert, "->,>>>,>>>,>>9") + to_string(l_op.lscheinnr, "x(12)") + to_string(usrid, "x(2)") + to_string(str_time, "x(8)") + to_string(reason, "x(24)")

        if t_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,45 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "Subtotal "
            for i in range(1,23 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
            for i in range(1,14 + 1) :
                str_list.s = str_list.s + " "

            if not long_digit:
                str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,23 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.999")
        for i in range(1,12 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("", "x(8)") + to_string("SUMMARY OF EXPENSES", "x(30)")
        tot_amount = 0

        for s_list in query(s_list_list):
            str_list = Str_list()
            str_list_list.append(str_list)


            if not long_digit:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(32)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->>,>>>,>>9.99")
            else:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(32)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->,>>>,>>>,>>9")
            tot_amount = tot_amount + s_list.cost
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,49 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9")

    def create_list1a():

        nonlocal it_exist, str_list_list, i, tot_anz, tot_amount, preis, wert, long_digit, htparam, gl_acct, bediener, l_lager, l_ophdr, l_artikel, l_op, l_untergrup, parameters
        nonlocal gl_acct1, usr


        nonlocal s_list, str_list, gl_acct1, usr
        nonlocal s_list_list, str_list_list

        t_anz:decimal = 0
        t_val:decimal = 0
        curr_artnr:int = 0
        lschein:str = ""
        cost_bezeich:str = ""
        fibukonto:str = ""
        do_it:bool = False
        create_it:bool = False
        cc_code:int = 0
        other_fibu:bool = False
        grp1:int = 0
        grp2:int = 1
        usrid:str = ""
        i:int = 0
        reason:str = ""
        str_time:str = ""
        str1:str = ""
        acct_no:str = ""
        Usr = Bediener
        Gl_acct1 = Gl_acct
        it_exist = False
        str_list_list.clear()
        s_list_list.clear()

        if mattype == 1:
            grp2 = 0

        elif mattype == 2:
            grp1 = 1
        tot_anz = 0
        tot_amount = 0
        do_it = True

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():
            do_it = True
            curr_artnr = 0
            usrid = ""
            reason = ""
            str_time = ""
            acct_no = ""

            l_op_obj_list = []
            for l_op, l_artikel, l_ophdr, gl_acct, l_untergrup in db_session.query(L_op, L_artikel, L_ophdr, Gl_acct, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == from_grp)).join(L_ophdr,(func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.lscheinnr == L_op.lscheinnr) &  (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == l_ophdr.fibukonto)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum) &  ((L_untergrup.betriebsnr >= grp1) &  (L_untergrup.betriebsnr <= grp2))).filter(
                    (L_op.lager_nr == l_lager.lager_nr) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  (L_op.anzahl != 0) &  (L_op.op_art == 3) &  (L_op.loeschflag == 2)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                usr = db_session.query(Usr).filter(
                        (Usr.nr == l_op.fuellflag)).first()

                if usr:
                    usrid = usr.userinit
                else:
                    usrid = "??"
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == "reason":
                        reason = entry(1, str1, ":")

                    elif entry(0, str1, ":") == "Time":
                        str_time = to_string(to_int(entry(1, str1, ":")) , "HH:MM:SS")
                    else:
                        acct_no = str1

                if show_price:
                    preis = l_op.einzelpreis
                    wert = l_op.warenwert
                it_exist = True
                other_fibu = False

                if acct_no != "":

                    gl_acct1 = db_session.query(Gl_acct1).filter(
                            (Gl_acct1.fibukonto == l_op.stornogrund)).first()

                    if gl_acct1:
                        other_fibu = True

                if other_fibu:
                    cc_code = get_costcenter_code(gl_acct1.fibukonto)
                else:
                    cc_code = get_costcenter_code(gl_acct.fibukonto)

                if lschein == "":
                    lschein = l_op.lscheinnr

                if other_fibu:
                    fibukonto = gl_acct1.fibukonto
                    cost_bezeich = gl_acct1.bezeich

                    if cost_acct == "":
                        create_it = True
                    else:
                        create_it = (cost_acct == fibukonto)
                else:
                    fibukonto = gl_acct.fibukonto
                    cost_bezeich = gl_acct.bezeich

                    if cost_acct == "":
                        create_it = True
                    else:
                        create_it = (cost_acct == fibukonto)

                if curr_artnr == 0:
                    curr_artnr = l_op.artnr

                if curr_artnr != l_op.artnr and t_anz != 0:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,45 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + "Subtotal "
                    for i in range(1,23 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
                    for i in range(1,14 + 1) :
                        str_list.s = str_list.s + " "

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9")
                    t_anz = 0
                    t_val = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    lschein = l_op.lscheinnr
                    curr_artnr = l_op.artnr

                if do_it:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.s = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(30)")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    do_it = False

                if create_it:

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.fibu = fibukonto
                        s_list.bezeich = cost_bezeich

                        if cc_code != 0:
                            s_list.bezeich = to_string(cc_code, "9999 ") + s_list.bezeich
                    s_list.cost = s_list.cost + wert
                    t_anz = t_anz + l_op.anzahl
                    t_val = t_val + wert
                    tot_anz = tot_anz + l_op.anzahl
                    tot_amount = tot_amount + wert
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.other_fibu = other_fibu
                    str_list.fibu = fibukonto
                    str_list.op_recid = l_op._recid

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_op.anzahl, "->,>>>,>>9.999") + to_string(preis, ">>>,>>>,>>9.99") + to_string(wert, "->>,>>>,>>9.99") + to_string(l_op.lscheinnr, "x(12)") + to_string(usrid, "x(2)") + to_string(str_time, "x(8)") + to_string(reason, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_op.anzahl, "->,>>>,>>9.999") + to_string(preis, ">>,>>>,>>>,>>9") + to_string(wert, "->,>>>,>>>,>>9") + to_string(l_op.lscheinnr, "x(12)") + to_string(usrid, "x(2)") + to_string(str_time, "x(8)") + to_string(reason, "x(24)")

        if t_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,45 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "Subtotal "
            for i in range(1,23 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
            for i in range(1,14 + 1) :
                str_list.s = str_list.s + " "

            if not long_digit:
                str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,23 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.999")
        for i in range(1,12 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("", "x(8)") + to_string("SUMMARY OF EXPENSES", "x(30)")
        tot_amount = 0

        for s_list in query(s_list_list):
            str_list = Str_list()
            str_list_list.append(str_list)


            if not long_digit:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(32)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->>,>>>,>>9.99")
            else:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(32)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->,>>>,>>>,>>9")
            tot_amount = tot_amount + s_list.cost
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,49 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9")

    def create_list1b():

        nonlocal it_exist, str_list_list, i, tot_anz, tot_amount, preis, wert, long_digit, htparam, gl_acct, bediener, l_lager, l_ophdr, l_artikel, l_op, l_untergrup, parameters
        nonlocal gl_acct1, usr


        nonlocal s_list, str_list, gl_acct1, usr
        nonlocal s_list_list, str_list_list

        t_anz:decimal = 0
        t_val:decimal = 0
        curr_artnr:int = 0
        lschein:str = ""
        cost_bezeich:str = ""
        fibukonto:str = ""
        do_it:bool = False
        create_it:bool = False
        cc_code:int = 0
        other_fibu:bool = False
        grp1:int = 0
        grp2:int = 1
        usrid:str = ""
        i:int = 0
        reason:str = ""
        str_time:str = ""
        str1:str = ""
        acct_no:str = ""
        Usr = Bediener
        Gl_acct1 = Gl_acct
        it_exist = False
        str_list_list.clear()
        s_list_list.clear()

        if mattype == 1:
            grp2 = 0

        elif mattype == 2:
            grp1 = 1
        tot_anz = 0
        tot_amount = 0
        do_it = True

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():
            do_it = True
            curr_artnr = 0
            usrid = ""
            reason = ""
            str_time = ""
            acct_no = ""

            l_op_obj_list = []
            for l_op, l_artikel, l_ophdr, gl_acct, l_untergrup in db_session.query(L_op, L_artikel, L_ophdr, Gl_acct, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == from_grp)).join(L_ophdr,(func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.lscheinnr == L_op.lscheinnr) &  (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == l_ophdr.fibukonto)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum) &  ((L_untergrup.betriebsnr >= grp1) &  (L_untergrup.betriebsnr <= grp2))).filter(
                    (L_op.lager_nr == l_lager.lager_nr) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  (L_op.anzahl != 0) &  (L_op.op_art == 3) &  (L_op.loeschflag == 2)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                usr = db_session.query(Usr).filter(
                        (Usr.nr == l_op.fuellflag)).first()

                if usr:
                    usrid = usr.userinit
                else:
                    usrid = "??"
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == "reason":
                        reason = entry(1, str1, ":")

                    elif entry(0, str1, ":") == "Time":
                        str_time = to_string(to_int(entry(1, str1, ":")) , "HH:MM:SS")
                    else:
                        acct_no = str1

                if show_price:
                    preis = l_op.einzelpreis
                    wert = l_op.warenwert
                it_exist = True
                other_fibu = False

                if acct_no != "":

                    gl_acct1 = db_session.query(Gl_acct1).filter(
                            (Gl_acct1.fibukonto == l_op.stornogrund)).first()

                    if gl_acct1:
                        other_fibu = True

                if other_fibu:
                    cc_code = get_costcenter_code(gl_acct1.fibukonto)
                else:
                    cc_code = get_costcenter_code(gl_acct.fibukonto)

                if other_fibu:
                    fibukonto = gl_acct1.fibukonto
                    cost_bezeich = gl_acct1.bezeich

                    if cost_acct == "":
                        create_it = True
                    else:
                        create_it = (cost_acct == fibukonto)
                else:
                    fibukonto = gl_acct.fibukonto
                    cost_bezeich = gl_acct.bezeich

                    if cost_acct == "":
                        create_it = True
                    else:
                        create_it = (cost_acct == fibukonto)

                if lschein == "":
                    lschein = l_op.lscheinnr

                if lschein != l_op.lscheinnr and t_anz != 0:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,45 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + "Subtotal "
                    for i in range(1,23 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
                    for i in range(1,14 + 1) :
                        str_list.s = str_list.s + " "

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9")
                    t_anz = 0
                    t_val = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    lschein = l_op.lscheinnr
                    curr_artnr = l_op.artnr

                if do_it:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.s = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(30)")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    do_it = False

                if create_it:

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.fibu = fibukonto
                        s_list.bezeich = cost_bezeich

                        if cc_code != 0:
                            s_list.bezeich = to_string(cc_code, "9999 ") + s_list.bezeich
                    s_list.cost = s_list.cost + wert
                    t_anz = t_anz + l_op.anzahl
                    t_val = t_val + wert
                    tot_anz = tot_anz + l_op.anzahl
                    tot_amount = tot_amount + wert
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.other_fibu = other_fibu
                    str_list.fibu = fibukonto
                    str_list.op_recid = l_op._recid

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_op.anzahl, "->,>>>,>>9.999") + to_string(preis, ">>>,>>>,>>9.99") + to_string(wert, "->>,>>>,>>9.99") + to_string(l_op.lscheinnr, "x(12)") + to_string(usrid, "x(2)") + to_string(str_time, "x(8)") + to_string(reason, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_op.anzahl, "->,>>>,>>9.999") + to_string(preis, ">>,>>>,>>>,>>9") + to_string(wert, "->,>>>,>>>,>>9") + to_string(l_op.lscheinnr, "x(12)") + to_string(usrid, "x(2)") + to_string(str_time, "x(8)") + to_string(reason, "x(24)")

        if t_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,45 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "Subtotal "
            for i in range(1,23 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
            for i in range(1,14 + 1) :
                str_list.s = str_list.s + " "

            if not long_digit:
                str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,23 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.999")
        for i in range(1,12 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("", "x(8)") + to_string("SUMMARY OF EXPENSES", "x(30)")
        tot_amount = 0

        for s_list in query(s_list_list):
            str_list = Str_list()
            str_list_list.append(str_list)


            if not long_digit:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(32)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->>,>>>,>>9.99")
            else:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(32)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->,>>>,>>>,>>9")
            tot_amount = tot_amount + s_list.cost
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,49 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9")

    def create_list1c():

        nonlocal it_exist, str_list_list, i, tot_anz, tot_amount, preis, wert, long_digit, htparam, gl_acct, bediener, l_lager, l_ophdr, l_artikel, l_op, l_untergrup, parameters
        nonlocal gl_acct1, usr


        nonlocal s_list, str_list, gl_acct1, usr
        nonlocal s_list_list, str_list_list

        t_anz:decimal = 0
        t_val:decimal = 0
        curr_artnr:int = 0
        lschein:str = ""
        datum:date = None
        cost_bezeich:str = ""
        fibukonto:str = ""
        do_it:bool = False
        create_it:bool = False
        cc_code:int = 0
        other_fibu:bool = False
        grp1:int = 0
        grp2:int = 1
        usrid:str = ""
        i:int = 0
        reason:str = ""
        str_time:str = ""
        str1:str = ""
        acct_no:str = ""
        Usr = Bediener
        Gl_acct1 = Gl_acct
        it_exist = False
        str_list_list.clear()
        s_list_list.clear()

        if mattype == 1:
            grp2 = 0

        elif mattype == 2:
            grp1 = 1
        tot_anz = 0
        tot_amount = 0
        do_it = True

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():
            do_it = True
            curr_artnr = 0
            usrid = ""
            reason = ""
            str_time = ""
            acct_no = ""

            l_op_obj_list = []
            for l_op, l_artikel, l_ophdr, gl_acct, l_untergrup in db_session.query(L_op, L_artikel, L_ophdr, Gl_acct, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == from_grp)).join(L_ophdr,(func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.lscheinnr == L_op.lscheinnr) &  (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == l_ophdr.fibukonto)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum) &  ((L_untergrup.betriebsnr >= grp1) &  (L_untergrup.betriebsnr <= grp2))).filter(
                    (L_op.lager_nr == l_lager.lager_nr) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  (L_op.anzahl != 0) &  (L_op.op_art == 3) &  (L_op.loeschflag == 2)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                usr = db_session.query(Usr).filter(
                        (Usr.nr == l_op.fuellflag)).first()

                if usr:
                    usrid = usr.userinit
                else:
                    usrid = "??"
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == "reason":
                        reason = entry(1, str1, ":")

                    elif entry(0, str1, ":") == "Time":
                        str_time = to_string(to_int(entry(1, str1, ":")) , "HH:MM:SS")
                    else:
                        acct_no = str1

                if show_price:
                    preis = l_op.einzelpreis
                    wert = l_op.warenwert
                it_exist = True
                other_fibu = False

                if acct_no != "":

                    gl_acct1 = db_session.query(Gl_acct1).filter(
                            (Gl_acct1.fibukonto == l_op.stornogrund)).first()

                    if gl_acct1:
                        other_fibu = True

                if other_fibu:
                    cc_code = get_costcenter_code(gl_acct1.fibukonto)
                else:
                    cc_code = get_costcenter_code(gl_acct.fibukonto)

                if other_fibu:
                    fibukonto = gl_acct1.fibukonto
                    cost_bezeich = gl_acct1.bezeich

                    if cost_acct == "":
                        create_it = True
                    else:
                        create_it = (cost_acct == fibukonto)
                else:
                    fibukonto = gl_acct.fibukonto
                    cost_bezeich = gl_acct.bezeich

                    if cost_acct == "":
                        create_it = True
                    else:
                        create_it = (cost_acct == fibukonto)

                if datum == None:
                    datum = l_op.datum

                if datum != l_op.datum and t_anz != 0:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,45 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + "Subtotal "
                    for i in range(1,23 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
                    for i in range(1,14 + 1) :
                        str_list.s = str_list.s + " "

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9")
                    t_anz = 0
                    t_val = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    lschein = l_op.lscheinnr
                    datum = l_op.datum
                    curr_artnr = l_op.artnr

                if do_it:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.s = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(30)")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    do_it = False

                if create_it:

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.fibu = fibukonto
                        s_list.bezeich = cost_bezeich

                        if cc_code != 0:
                            s_list.bezeich = to_string(cc_code, "9999 ") + s_list.bezeich
                    s_list.cost = s_list.cost + wert
                    t_anz = t_anz + l_op.anzahl
                    t_val = t_val + wert
                    tot_anz = tot_anz + l_op.anzahl
                    tot_amount = tot_amount + wert
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.other_fibu = other_fibu
                    str_list.fibu = fibukonto
                    str_list.op_recid = l_op._recid

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_op.anzahl, "->,>>>,>>9.999") + to_string(preis, ">>>,>>>,>>9.99") + to_string(wert, "->>,>>>,>>9.99") + to_string(l_op.lscheinnr, "x(12)") + to_string(usrid, "x(2)") + to_string(str_time, "x(8)") + to_string(reason, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_op.anzahl, "->,>>>,>>9.999") + to_string(preis, ">>,>>>,>>>,>>9") + to_string(wert, "->,>>>,>>>,>>9") + to_string(l_op.lscheinnr, "x(12)") + to_string(usrid, "x(2)") + to_string(str_time, "x(8)") + to_string(reason, "x(24)")

        if t_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,45 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "Subtotal "
            for i in range(1,23 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
            for i in range(1,14 + 1) :
                str_list.s = str_list.s + " "

            if not long_digit:
                str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,23 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.999")
        for i in range(1,12 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("", "x(8)") + to_string("SUMMARY OF EXPENSES", "x(30)")
        tot_amount = 0

        for s_list in query(s_list_list):
            str_list = Str_list()
            str_list_list.append(str_list)


            if not long_digit:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(32)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->>,>>>,>>9.99")
            else:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(32)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->,>>>,>>>,>>9")
            tot_amount = tot_amount + s_list.cost
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,49 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9")

    def get_costcenter_code(fibukonto:str):

        nonlocal it_exist, str_list_list, i, tot_anz, tot_amount, preis, wert, long_digit, htparam, gl_acct, bediener, l_lager, l_ophdr, l_artikel, l_op, l_untergrup, parameters
        nonlocal gl_acct1, usr


        nonlocal s_list, str_list, gl_acct1, usr
        nonlocal s_list_list, str_list_list

        cc_code = 0

        def generate_inner_output():
            return cc_code

        parameters = db_session.query(Parameters).filter(
                (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Alloc") &  (Parameters.varname > "") &  (func.lower(Parameters.vstring) == (fibukonto).lower())).first()

        if PARAMETERs:
            cc_code = to_int(PARAMETERs.varname)


        return generate_inner_output()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    if from_grp == 0:

        if mi_alloc_chk :
            create_list()

        elif mi_article_chk :
            create_lista()

        elif mi_docu_chk :
            create_listb()

        elif mi_date_chk :
            create_listc()
    else:

        if mi_alloc_chk :
            create_list1()

        elif mi_article_chk :
            create_list1a()

        elif mi_docu_chk :
            create_list1b()

        elif mi_date_chk :
            create_list1c()

    return generate_output()