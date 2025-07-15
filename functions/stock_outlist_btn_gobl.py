#using conversion tools version: 1.0.0.27

from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Gl_acct, L_lager, L_ophdr, L_artikel, L_op, Parameters, L_untergrup, Bediener

def stock_outlist_btn_gobl(trans_code:str, from_grp:int, mi_alloc:bool, mi_article:bool, mi_docu:bool, mi_date:bool, mattype:int, from_lager:int, to_lager:int, from_date:date, to_date:date, from_art:int, to_art:int, show_price:bool, cost_acct:str, deptno:int):
    it_exist = False
    tot_anz = to_decimal("0.0")
    tot_amount = to_decimal("0.0")
    str_list_list = []
    preis:decimal = to_decimal("0.0")
    wert:decimal = to_decimal("0.0")
    i:int = 0
    do_it:bool = False
    mi_subgroup:bool = False
    gl_acct = l_lager = l_ophdr = l_artikel = l_op = parameters = l_untergrup = bediener = None

    str_list = s_list = None

    str_list_list, Str_list = create_model("Str_list", {"billdate":date, "fibu":str, "other_fibu":bool, "op_recid":int, "lscheinnr":str, "s":str, "id":str})
    s_list_list, S_list = create_model("S_list", {"fibu":str, "cost_center":str, "bezeich":str, "cost":decimal, "subgroup":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal it_exist, tot_anz, tot_amount, str_list_list, preis, wert, i, do_it, mi_subgroup, gl_acct, l_lager, l_ophdr, l_artikel, l_op, parameters, l_untergrup, bediener
        nonlocal trans_code, from_grp, mi_alloc, mi_article, mi_docu, mi_date, mattype, from_lager, to_lager, from_date, to_date, from_art, to_art, show_price, cost_acct, deptno


        nonlocal str_list, s_list
        nonlocal str_list_list, s_list_list

        return {"it_exist": it_exist, "tot_anz": tot_anz, "tot_amount": tot_amount, "str-list": str_list_list}

    def create_list_trans():

        nonlocal it_exist, tot_anz, tot_amount, str_list_list, preis, wert, i, mi_subgroup, gl_acct, l_lager, l_ophdr, l_artikel, l_op, parameters, l_untergrup, bediener
        nonlocal trans_code, from_grp, mi_alloc, mi_article, mi_docu, mi_date, mattype, from_lager, to_lager, from_date, to_date, from_art, to_art, show_price, cost_acct, deptno


        nonlocal str_list, s_list
        nonlocal str_list_list, s_list_list

        t_anz:decimal = to_decimal("0.0")
        t_val:decimal = to_decimal("0.0")
        lschein:str = ""
        cost_bezeich:str = ""
        fibukonto:str = ""
        do_it:bool = False
        cc_code:int = 0
        other_fibu:bool = False
        gl_acct1 = None
        create_it:bool = False
        curr_fibu:str = ""
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        it_exist = False
        str_list_list.clear()
        s_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")

        for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():
            do_it = True

            l_op_obj_list = []
            for l_op, l_ophdr, gl_acct, l_artikel in db_session.query(L_op, L_ophdr, Gl_acct, L_artikel).join(L_ophdr,(func.lower(L_ophdr.op_typ) == ("STT").lower()) & (L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_op.stornogrund)).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                     (L_op.lager_nr == l_lager.lager_nr) & (L_op.anzahl != 0) & (L_op.op_art == 3) & (func.lower(L_op.lscheinnr) == (trans_code).lower()) & (L_op.loeschflag <= 1)).order_by(L_op.stornogrund, L_ophdr.fibukonto, L_op.datum, L_op.artnr).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                if show_price:
                    preis =  to_decimal(l_op.einzelpreis)
                    wert =  to_decimal(l_op.warenwert)
                it_exist = True
                other_fibu = False

                if l_op.stornogrund != "":

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

                if create_it and deptno != 0:

                    parameters = db_session.query(Parameters).filter(
                             (func.lower(Parameters.progname) == ("CostCenter").lower()) & (func.lower(Parameters.section) == ("alloc").lower()) & (Parameters.varname == to_string(deptno)) & (func.lower(Parameters.vstring) == (fibukonto).lower())).first()
                    create_it = None != parameters

                if curr_fibu == "":
                    curr_fibu = fibukonto

                if curr_fibu.lower()  != (fibukonto).lower()  and t_anz != 0:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,45 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + "Subtotal "
                    for i in range(1,41 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
                    for i in range(1,14 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
                    t_anz =  to_decimal("0")
                    t_val =  to_decimal("0")
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

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.fibu = fibukonto
                        s_list.bezeich = cost_bezeich

                        if cc_code != 0:
                            s_list.bezeich = to_string(cc_code, "9999 ") + s_list.bezeich
                    s_list.cost = s_list.cost + wert
                    t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)
                    t_val =  to_decimal(t_val) + to_decimal(wert)
                    tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)
                    tot_amount =  to_decimal(tot_amount) + to_decimal(wert)
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    add_id()
                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.fibu = fibukonto
                    str_list.other_fibu = other_fibu
                    str_list.op_recid = l_op._recid
                    str_list.s = to_string(l_op.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_op.anzahl, "->,>>>,>>9.999") + to_string(preis, ">>>,>>>,>>9.99") + to_string(wert, "->,>>>,>>>,>>9.99") + to_string(l_op.lscheinnr, "x(12)")
                    str_list.billdate = l_op.datum

        if t_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,45 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "Subtotal "
            for i in range(1,41 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
            for i in range(1,14 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,41 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.999")
        for i in range(1,14 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("", "x(8)") + to_string("SUMMARY OF EXPENSES", "x(30)")
        tot_amount =  to_decimal("0")

        for s_list in query(s_list_list, sort_by=[("bezeich",False)]):
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(50)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>>>") + to_string(s_list.cost, "->,>>>,>>>,>>9.99")
            tot_amount =  to_decimal(tot_amount) + to_decimal(s_list.cost)
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,69 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")


    def create_list():

        nonlocal it_exist, tot_anz, tot_amount, str_list_list, preis, wert, i, mi_subgroup, gl_acct, l_lager, l_ophdr, l_artikel, l_op, parameters, l_untergrup, bediener
        nonlocal trans_code, from_grp, mi_alloc, mi_article, mi_docu, mi_date, mattype, from_lager, to_lager, from_date, to_date, from_art, to_art, show_price, cost_acct, deptno


        nonlocal str_list, s_list
        nonlocal str_list_list, s_list_list

        t_anz:decimal = to_decimal("0.0")
        t_val:decimal = to_decimal("0.0")
        lschein:str = ""
        cost_bezeich:str = ""
        fibukonto:str = ""
        do_it:bool = False
        cc_code:int = 0
        other_fibu:bool = False
        gl_acct1 = None
        create_it:bool = False
        curr_fibu:str = ""
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        it_exist = False
        str_list_list.clear()
        s_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():
            do_it = True

            l_op_obj_list = []
            for l_op, l_ophdr, gl_acct, l_artikel in db_session.query(L_op, L_ophdr, Gl_acct, L_artikel).join(L_ophdr,(func.lower(L_ophdr.op_typ) == ("STT").lower()) & (L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_op.stornogrund)).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                     (L_op.lager_nr == l_lager.lager_nr) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & (L_op.anzahl != 0) & (L_op.op_art == 3) & (L_op.loeschflag <= 1)).order_by(L_op.stornogrund, L_ophdr.fibukonto, L_op.datum, L_op.artnr).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                if show_price:
                    preis =  to_decimal(l_op.einzelpreis)
                    wert =  to_decimal(l_op.warenwert)
                it_exist = True
                other_fibu = False

                if l_op.stornogrund != "":

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

                if create_it and deptno != 0:

                    parameters = db_session.query(Parameters).filter(
                             (func.lower(Parameters.progname) == ("CostCenter").lower()) & (func.lower(Parameters.section) == ("alloc").lower()) & (Parameters.varname == to_string(deptno)) & (func.lower(Parameters.vstring) == (fibukonto).lower())).first()
                    create_it = None != parameters

                if curr_fibu == "":
                    curr_fibu = fibukonto

                if curr_fibu.lower()  != (fibukonto).lower()  and t_anz != 0:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,45 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + "Subtotal "
                    for i in range(1,41 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
                    for i in range(1,14 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
                    t_anz =  to_decimal("0")
                    t_val =  to_decimal("0")
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

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.fibu = fibukonto
                        s_list.bezeich = cost_bezeich

                        if cc_code != 0:
                            s_list.bezeich = to_string(cc_code, "9999 ") + s_list.bezeich
                    s_list.cost = s_list.cost + wert
                    t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)
                    t_val =  to_decimal(t_val) + to_decimal(wert)
                    tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)
                    tot_amount =  to_decimal(tot_amount) + to_decimal(wert)
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    add_id()
                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.fibu = fibukonto
                    str_list.other_fibu = other_fibu
                    str_list.op_recid = l_op._recid
                    str_list.s = to_string(l_op.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_op.anzahl, "->,>>>,>>9.999") + to_string(preis, ">>>,>>>,>>9.99") + to_string(wert, "->,>>>,>>>,>>9.99") + to_string(l_op.lscheinnr, "x(12)")
                    str_list.billdate = l_op.datum

        if t_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,45 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "Subtotal "
            for i in range(1,41 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
            for i in range(1,14 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,41 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.999")
        for i in range(1,14 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("", "x(8)") + to_string("SUMMARY OF EXPENSES", "x(30)")
        tot_amount =  to_decimal("0")

        for s_list in query(s_list_list, sort_by=[("bezeich",False)]):
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(50)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>>>") + to_string(s_list.cost, "->,>>>,>>>,>>9.99")
            tot_amount =  to_decimal(tot_amount) + to_decimal(s_list.cost)
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,69 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")


    def create_list1():

        nonlocal it_exist, tot_anz, tot_amount, str_list_list, preis, wert, i, mi_subgroup, gl_acct, l_lager, l_ophdr, l_artikel, l_op, parameters, l_untergrup, bediener
        nonlocal trans_code, from_grp, mi_alloc, mi_article, mi_docu, mi_date, mattype, from_lager, to_lager, from_date, to_date, from_art, to_art, show_price, cost_acct, deptno


        nonlocal str_list, s_list
        nonlocal str_list_list, s_list_list

        t_anz:decimal = to_decimal("0.0")
        t_val:decimal = to_decimal("0.0")
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
        gl_acct1 = None
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        it_exist = False
        str_list_list.clear()
        s_list_list.clear()

        if mattype == 1:
            grp2 = 0

        elif mattype == 2:
            grp1 = 1
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():
            do_it = True

            l_op_obj_list = []
            for l_op, l_ophdr, gl_acct, l_artikel, l_untergrup in db_session.query(L_op, L_ophdr, Gl_acct, L_artikel, L_untergrup).join(L_ophdr,(func.lower(L_ophdr.op_typ) == ("STT").lower()) & (L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_op.stornogrund)).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                     (L_op.lager_nr == l_lager.lager_nr) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & (L_op.anzahl != 0) & (L_op.op_art == 3) & (L_op.loeschflag <= 1)).order_by(L_op.stornogrund, L_ophdr.fibukonto, L_op.datum, L_op.artnr).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                if show_price:
                    preis =  to_decimal(l_op.einzelpreis)
                    wert =  to_decimal(l_op.warenwert)
                it_exist = True
                other_fibu = False

                if l_op.stornogrund != "":

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

                if create_it and deptno != 0:

                    parameters = db_session.query(Parameters).filter(
                             (func.lower(Parameters.progname) == ("CostCenter").lower()) & (func.lower(Parameters.section) == ("alloc").lower()) & (Parameters.varname == to_string(deptno)) & (func.lower(Parameters.vstring) == (fibukonto).lower())).first()
                    create_it = None != parameters

                if curr_fibu == "":
                    curr_fibu = fibukonto

                if curr_fibu.lower()  != (fibukonto).lower()  and t_anz != 0:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,45 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + "Subtotal "
                    for i in range(1,41 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
                    for i in range(1,14 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
                    t_anz =  to_decimal("0")
                    t_val =  to_decimal("0")
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

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.fibu = fibukonto
                        s_list.bezeich = cost_bezeich

                        if cc_code != 0:
                            s_list.bezeich = to_string(cc_code, "9999 ") + s_list.bezeich
                    s_list.cost = s_list.cost + wert
                    t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)
                    t_val =  to_decimal(t_val) + to_decimal(wert)
                    tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)
                    tot_amount =  to_decimal(tot_amount) + to_decimal(wert)
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    add_id()
                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.other_fibu = other_fibu
                    str_list.fibu = fibukonto
                    str_list.op_recid = l_op._recid
                    str_list.s = to_string(l_op.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_op.anzahl, "->,>>>,>>9.999") + to_string(preis, ">>>,>>>,>>9.99") + to_string(wert, "->,>>>,>>>,>>9.99") + to_string(l_op.lscheinnr, "x(12)")
                    str_list.billdate = l_op.datum

        if t_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,45 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "Subtotal "
            for i in range(1,41 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
            for i in range(1,14 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,41 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.999")
        for i in range(1,14 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("", "x(8)") + to_string("SUMMARY OF EXPENSES", "x(30)")
        tot_amount =  to_decimal("0")

        for s_list in query(s_list_list, sort_by=[("bezeich",False)]):
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(50)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>>>") + to_string(s_list.cost, "->,>>>,>>>,>>9.99")
            tot_amount =  to_decimal(tot_amount) + to_decimal(s_list.cost)
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,69 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")


    def create_list1a():

        nonlocal it_exist, tot_anz, tot_amount, str_list_list, preis, wert, i, mi_subgroup, gl_acct, l_lager, l_ophdr, l_artikel, l_op, parameters, l_untergrup, bediener
        nonlocal trans_code, from_grp, mi_alloc, mi_article, mi_docu, mi_date, mattype, from_lager, to_lager, from_date, to_date, from_art, to_art, show_price, cost_acct, deptno


        nonlocal str_list, s_list
        nonlocal str_list_list, s_list_list

        t_anz:decimal = to_decimal("0.0")
        t_val:decimal = to_decimal("0.0")
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
        gl_acct1 = None
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        it_exist = False
        str_list_list.clear()
        s_list_list.clear()

        if mattype == 1:
            grp2 = 0

        elif mattype == 2:
            grp1 = 1
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        do_it = True

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():
            do_it = True
            curr_artnr = 0

            l_op_obj_list = []
            for l_op, l_artikel, l_ophdr, gl_acct, l_untergrup in db_session.query(L_op, L_artikel, L_ophdr, Gl_acct, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).join(L_ophdr,(func.lower(L_ophdr.op_typ) == ("STT").lower()) & (L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_op.stornogrund)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                     (L_op.lager_nr == l_lager.lager_nr) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & (L_op.anzahl != 0) & (L_op.op_art == 3) & (L_op.loeschflag <= 1)).order_by(L_op.datum, L_op.lscheinnr, L_op.artnr).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                if show_price:
                    preis =  to_decimal(l_op.einzelpreis)
                    wert =  to_decimal(l_op.warenwert)
                it_exist = True
                other_fibu = False

                if l_op.stornogrund != "":

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

                if create_it and deptno != 0:

                    parameters = db_session.query(Parameters).filter(
                             (func.lower(Parameters.progname) == ("CostCenter").lower()) & (func.lower(Parameters.section) == ("alloc").lower()) & (Parameters.varname == to_string(deptno)) & (func.lower(Parameters.vstring) == (fibukonto).lower())).first()
                    create_it = None != parameters

                if curr_artnr == 0:
                    curr_artnr = l_op.artnr

                if curr_artnr != l_op.artnr and t_anz != 0:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,45 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + "Subtotal "
                    for i in range(1,41 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
                    for i in range(1,14 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
                    t_anz =  to_decimal("0")
                    t_val =  to_decimal("0")
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

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.fibu = fibukonto
                        s_list.bezeich = cost_bezeich

                        if cc_code != 0:
                            s_list.bezeich = to_string(cc_code, "9999 ") + s_list.bezeich
                    s_list.cost = s_list.cost + wert
                    t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)
                    t_val =  to_decimal(t_val) + to_decimal(wert)
                    tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)
                    tot_amount =  to_decimal(tot_amount) + to_decimal(wert)
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    add_id()
                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.other_fibu = other_fibu
                    str_list.fibu = fibukonto
                    str_list.op_recid = l_op._recid
                    str_list.s = to_string(l_op.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_op.anzahl, "->,>>>,>>9.999") + to_string(preis, ">>>,>>>,>>9.99") + to_string(wert, "->,>>>,>>>,>>9.99") + to_string(l_op.lscheinnr, "x(12)")
                    str_list.billdate = l_op.datum

        if t_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,45 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "Subtotal "
            for i in range(1,41 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
            for i in range(1,14 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,41 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.999")
        for i in range(1,14 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("", "x(8)") + to_string("SUMMARY OF EXPENSES", "x(30)")
        tot_amount =  to_decimal("0")

        for s_list in query(s_list_list, sort_by=[("bezeich",False)]):
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(50)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>>>") + to_string(s_list.cost, "->,>>>,>>>,>>9.99")
            tot_amount =  to_decimal(tot_amount) + to_decimal(s_list.cost)
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,69 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")


    def create_list1b():

        nonlocal it_exist, tot_anz, tot_amount, str_list_list, preis, wert, i, mi_subgroup, gl_acct, l_lager, l_ophdr, l_artikel, l_op, parameters, l_untergrup, bediener
        nonlocal trans_code, from_grp, mi_alloc, mi_article, mi_docu, mi_date, mattype, from_lager, to_lager, from_date, to_date, from_art, to_art, show_price, cost_acct, deptno


        nonlocal str_list, s_list
        nonlocal str_list_list, s_list_list

        t_anz:decimal = to_decimal("0.0")
        t_val:decimal = to_decimal("0.0")
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
        gl_acct1 = None
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        it_exist = False
        str_list_list.clear()
        s_list_list.clear()

        if mattype == 1:
            grp2 = 0

        elif mattype == 2:
            grp1 = 1
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        do_it = True

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():
            do_it = True
            curr_artnr = 0

            l_op_obj_list = []
            for l_op, l_artikel, l_ophdr, gl_acct, l_untergrup in db_session.query(L_op, L_artikel, L_ophdr, Gl_acct, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).join(L_ophdr,(func.lower(L_ophdr.op_typ) == ("STT").lower()) & (L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_op.stornogrund)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                     (L_op.lager_nr == l_lager.lager_nr) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & (L_op.anzahl != 0) & (L_op.op_art == 3) & (L_op.loeschflag <= 1)).order_by(L_op.lscheinnr, L_op.artnr).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                if show_price:
                    preis =  to_decimal(l_op.einzelpreis)
                    wert =  to_decimal(l_op.warenwert)
                it_exist = True
                other_fibu = False

                if l_op.stornogrund != "":

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

                if create_it and deptno != 0:

                    parameters = db_session.query(Parameters).filter(
                             (func.lower(Parameters.progname) == ("CostCenter").lower()) & (func.lower(Parameters.section) == ("alloc").lower()) & (Parameters.varname == to_string(deptno)) & (func.lower(Parameters.vstring) == (fibukonto).lower())).first()
                    create_it = None != parameters

                if lschein == "":
                    lschein = l_op.lscheinnr

                if lschein != l_op.lscheinnr and t_anz != 0:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,45 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + "Subtotal "
                    for i in range(1,41 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
                    for i in range(1,14 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
                    t_anz =  to_decimal("0")
                    t_val =  to_decimal("0")
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

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.fibu = fibukonto
                        s_list.bezeich = cost_bezeich

                        if cc_code != 0:
                            s_list.bezeich = to_string(cc_code, "9999 ") + s_list.bezeich
                    s_list.cost = s_list.cost + wert
                    t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)
                    t_val =  to_decimal(t_val) + to_decimal(wert)
                    tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)
                    tot_amount =  to_decimal(tot_amount) + to_decimal(wert)
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    add_id()
                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.other_fibu = other_fibu
                    str_list.fibu = fibukonto
                    str_list.op_recid = l_op._recid
                    str_list.s = to_string(l_op.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_op.anzahl, "->,>>>,>>9.999") + to_string(preis, ">>>,>>>,>>9.99") + to_string(wert, "->,>>>,>>>,>>9.99") + to_string(l_op.lscheinnr, "x(12)")
                    str_list.billdate = l_op.datum

        if t_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,45 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "Subtotal "
            for i in range(1,41 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
            for i in range(1,14 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,41 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.999")
        for i in range(1,14 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("", "x(8)") + to_string("SUMMARY OF EXPENSES", "x(30)")
        tot_amount =  to_decimal("0")

        for s_list in query(s_list_list, sort_by=[("bezeich",False)]):
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(50)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>>>") + to_string(s_list.cost, "->,>>>,>>>,>>9.99")
            tot_amount =  to_decimal(tot_amount) + to_decimal(s_list.cost)
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,69 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")


    def create_list1c():

        nonlocal it_exist, tot_anz, tot_amount, str_list_list, preis, wert, i, mi_subgroup, gl_acct, l_lager, l_ophdr, l_artikel, l_op, parameters, l_untergrup, bediener
        nonlocal trans_code, from_grp, mi_alloc, mi_article, mi_docu, mi_date, mattype, from_lager, to_lager, from_date, to_date, from_art, to_art, show_price, cost_acct, deptno


        nonlocal str_list, s_list
        nonlocal str_list_list, s_list_list

        t_anz:decimal = to_decimal("0.0")
        t_val:decimal = to_decimal("0.0")
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
        gl_acct1 = None
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        it_exist = False
        str_list_list.clear()
        s_list_list.clear()

        if mattype == 1:
            grp2 = 0

        elif mattype == 2:
            grp1 = 1
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        do_it = True

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():
            do_it = True
            curr_artnr = 0

            l_op_obj_list = []
            for l_op, l_artikel, l_ophdr, gl_acct, l_untergrup in db_session.query(L_op, L_artikel, L_ophdr, Gl_acct, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).join(L_ophdr,(func.lower(L_ophdr.op_typ) == ("STT").lower()) & (L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_op.stornogrund)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                     (L_op.lager_nr == l_lager.lager_nr) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & (L_op.anzahl != 0) & (L_op.op_art == 3) & (L_op.loeschflag <= 1)).order_by(L_op.datum, L_op.artnr).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                if show_price:
                    preis =  to_decimal(l_op.einzelpreis)
                    wert =  to_decimal(l_op.warenwert)
                it_exist = True
                other_fibu = False

                if l_op.stornogrund != "":

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

                if create_it and deptno != 0:

                    parameters = db_session.query(Parameters).filter(
                             (func.lower(Parameters.progname) == ("CostCenter").lower()) & (func.lower(Parameters.section) == ("alloc").lower()) & (Parameters.varname == to_string(deptno)) & (func.lower(Parameters.vstring) == (fibukonto).lower())).first()
                    create_it = None != parameters

                if datum == None:
                    datum = l_op.datum

                if datum != l_op.datum and t_anz != 0:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,45 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + "Subtotal "
                    for i in range(1,41 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
                    for i in range(1,14 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
                    t_anz =  to_decimal("0")
                    t_val =  to_decimal("0")
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

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.fibu = fibukonto
                        s_list.bezeich = cost_bezeich

                        if cc_code != 0:
                            s_list.bezeich = to_string(cc_code, "9999 ") + s_list.bezeich
                    s_list.cost = s_list.cost + wert
                    t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)
                    t_val =  to_decimal(t_val) + to_decimal(wert)
                    tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)
                    tot_amount =  to_decimal(tot_amount) + to_decimal(wert)
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    add_id()
                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.other_fibu = other_fibu
                    str_list.fibu = fibukonto
                    str_list.op_recid = l_op._recid
                    str_list.s = to_string(l_op.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_op.anzahl, "->,>>>,>>9.999") + to_string(preis, ">>>,>>>,>>9.99") + to_string(wert, "->,>>>,>>>,>>9.99") + to_string(l_op.lscheinnr, "x(12)")
                    str_list.billdate = l_op.datum

        if t_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,45 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "Subtotal "
            for i in range(1,41 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
            for i in range(1,14 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,41 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.999")
        for i in range(1,14 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("", "x(8)") + to_string("SUMMARY OF EXPENSES", "x(30)")
        tot_amount =  to_decimal("0")

        for s_list in query(s_list_list, sort_by=[("bezeich",False)]):
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(50)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>>>") + to_string(s_list.cost, "->,>>>,>>>,>>9.99")
            tot_amount =  to_decimal(tot_amount) + to_decimal(s_list.cost)
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,69 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")


    def create_listb():

        nonlocal it_exist, tot_anz, tot_amount, str_list_list, preis, wert, i, mi_subgroup, gl_acct, l_lager, l_ophdr, l_artikel, l_op, parameters, l_untergrup, bediener
        nonlocal trans_code, from_grp, mi_alloc, mi_article, mi_docu, mi_date, mattype, from_lager, to_lager, from_date, to_date, from_art, to_art, show_price, cost_acct, deptno


        nonlocal str_list, s_list
        nonlocal str_list_list, s_list_list

        t_anz:decimal = to_decimal("0.0")
        t_val:decimal = to_decimal("0.0")
        curr_artnr:int = 0
        lschein:str = ""
        cost_bezeich:str = ""
        fibukonto:str = ""
        do_it:bool = False
        cc_code:int = 0
        other_fibu:bool = False
        gl_acct1 = None
        create_it:bool = False
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        it_exist = False
        str_list_list.clear()
        s_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        do_it = True

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():
            do_it = True
            curr_artnr = 0

            l_op_obj_list = []
            for l_op, l_ophdr, gl_acct, l_artikel in db_session.query(L_op, L_ophdr, Gl_acct, L_artikel).join(L_ophdr,(func.lower(L_ophdr.op_typ) == ("STT").lower()) & (L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_op.stornogrund)).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                     (L_op.lager_nr == l_lager.lager_nr) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & (L_op.anzahl != 0) & (L_op.op_art == 3) & (L_op.loeschflag <= 1)).order_by(L_op.lscheinnr, L_op.artnr).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                if show_price:
                    preis =  to_decimal(l_op.einzelpreis)
                    wert =  to_decimal(l_op.warenwert)
                it_exist = True
                other_fibu = False

                if l_op.stornogrund != "":

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

                if create_it and deptno != 0:

                    parameters = db_session.query(Parameters).filter(
                             (func.lower(Parameters.progname) == ("CostCenter").lower()) & (func.lower(Parameters.section) == ("alloc").lower()) & (Parameters.varname == to_string(deptno)) & (func.lower(Parameters.vstring) == (fibukonto).lower())).first()
                    create_it = None != parameters

                if lschein == "":
                    lschein = l_op.lscheinnr

                if (lschein != l_op.lscheinnr) and t_anz != 0:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,45 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + "Subtotal "
                    for i in range(1,41 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
                    for i in range(1,14 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
                    t_anz =  to_decimal("0")
                    t_val =  to_decimal("0")
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

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.fibu = fibukonto
                        s_list.bezeich = cost_bezeich

                        if cc_code != 0:
                            s_list.bezeich = to_string(cc_code, "9999 ") + s_list.bezeich
                    s_list.cost = s_list.cost + wert
                    t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)
                    t_val =  to_decimal(t_val) + to_decimal(wert)
                    tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)
                    tot_amount =  to_decimal(tot_amount) + to_decimal(wert)
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    add_id()
                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.fibu = fibukonto
                    str_list.other_fibu = other_fibu
                    str_list.op_recid = l_op._recid
                    str_list.s = to_string(l_op.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_op.anzahl, "->,>>>,>>9.999") + to_string(preis, ">>>,>>>,>>9.99") + to_string(wert, "->,>>>,>>>,>>9.99") + to_string(l_op.lscheinnr, "x(12)")
                    str_list.billdate = l_op.datum

        if t_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,45 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "Subtotal "
            for i in range(1,41 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
            for i in range(1,14 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,41 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.999")
        for i in range(1,14 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("", "x(8)") + to_string("SUMMARY OF EXPENSES", "x(30)")
        tot_amount =  to_decimal("0")

        for s_list in query(s_list_list, sort_by=[("bezeich",False)]):
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(50)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>>>") + to_string(s_list.cost, "->,>>>,>>>,>>9.99")
            tot_amount =  to_decimal(tot_amount) + to_decimal(s_list.cost)
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,69 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")


    def create_listc():

        nonlocal it_exist, tot_anz, tot_amount, str_list_list, preis, wert, i, mi_subgroup, gl_acct, l_lager, l_ophdr, l_artikel, l_op, parameters, l_untergrup, bediener
        nonlocal trans_code, from_grp, mi_alloc, mi_article, mi_docu, mi_date, mattype, from_lager, to_lager, from_date, to_date, from_art, to_art, show_price, cost_acct, deptno


        nonlocal str_list, s_list
        nonlocal str_list_list, s_list_list

        t_anz:decimal = to_decimal("0.0")
        t_val:decimal = to_decimal("0.0")
        curr_artnr:int = 0
        lschein:str = ""
        datum:date = None
        cost_bezeich:str = ""
        fibukonto:str = ""
        do_it:bool = False
        cc_code:int = 0
        other_fibu:bool = False
        gl_acct1 = None
        create_it:bool = False
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        it_exist = False
        str_list_list.clear()
        s_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        do_it = True

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():
            do_it = True
            curr_artnr = 0

            l_op_obj_list = []
            for l_op, l_ophdr, gl_acct, l_artikel in db_session.query(L_op, L_ophdr, Gl_acct, L_artikel).join(L_ophdr,(func.lower(L_ophdr.op_typ) == ("STT").lower()) & (L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_op.stornogrund)).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                     (L_op.lager_nr == l_lager.lager_nr) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & (L_op.anzahl != 0) & (L_op.op_art == 3) & (L_op.loeschflag <= 1)).order_by(L_op.datum, L_op.artnr).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                if show_price:
                    preis =  to_decimal(l_op.einzelpreis)
                    wert =  to_decimal(l_op.warenwert)
                it_exist = True
                other_fibu = False

                if l_op.stornogrund != "":

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

                if create_it and deptno != 0:

                    parameters = db_session.query(Parameters).filter(
                             (func.lower(Parameters.progname) == ("CostCenter").lower()) & (func.lower(Parameters.section) == ("alloc").lower()) & (Parameters.varname == to_string(deptno)) & (func.lower(Parameters.vstring) == (fibukonto).lower())).first()
                    create_it = None != parameters

                if datum == None:
                    datum = l_op.datum

                if (datum != l_op.datum) and t_anz != 0:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,45 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + "Subtotal "
                    for i in range(1,41 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
                    for i in range(1,14 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
                    t_anz =  to_decimal("0")
                    t_val =  to_decimal("0")
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

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.fibu = fibukonto
                        s_list.bezeich = cost_bezeich

                        if cc_code != 0:
                            s_list.bezeich = to_string(cc_code, "9999 ") + s_list.bezeich
                    s_list.cost = s_list.cost + wert
                    t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)
                    t_val =  to_decimal(t_val) + to_decimal(wert)
                    tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)
                    tot_amount =  to_decimal(tot_amount) + to_decimal(wert)
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    add_id()
                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.fibu = fibukonto
                    str_list.other_fibu = other_fibu
                    str_list.op_recid = l_op._recid
                    str_list.s = to_string(l_op.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_op.anzahl, "->,>>>,>>9.999") + to_string(preis, ">>>,>>>,>>9.99") + to_string(wert, "->,>>>,>>>,>>9.99") + to_string(l_op.lscheinnr, "x(12)")
                    str_list.billdate = l_op.datum

        if t_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,45 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "Subtotal "
            for i in range(1,41 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
            for i in range(1,14 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,41 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.999")
        for i in range(1,14 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("", "x(8)") + to_string("SUMMARY OF EXPENSES", "x(30)")
        tot_amount =  to_decimal("0")

        for s_list in query(s_list_list, sort_by=[("bezeich",False)]):
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(50)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>>>") + to_string(s_list.cost, "->,>>>,>>>,>>9.99")
            tot_amount =  to_decimal(tot_amount) + to_decimal(s_list.cost)
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,69 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")


    def add_id():

        nonlocal it_exist, tot_anz, tot_amount, str_list_list, preis, wert, i, do_it, mi_subgroup, gl_acct, l_lager, l_ophdr, l_artikel, l_op, parameters, l_untergrup, bediener
        nonlocal trans_code, from_grp, mi_alloc, mi_article, mi_docu, mi_date, mattype, from_lager, to_lager, from_date, to_date, from_art, to_art, show_price, cost_acct, deptno


        nonlocal str_list, s_list
        nonlocal str_list_list, s_list_list

        usr = None
        Usr =  create_buffer("Usr",Bediener)

        usr = db_session.query(Usr).filter(
                 (Usr.nr == l_op.fuellflag)).first()

        if usr:
            str_list.id = usr.userinit

        elif l_op.fuellflag == 0:
            str_list.id = "**"


        else:
            str_list.id = "??"


    def get_costcenter_code(fibukonto:str):

        nonlocal it_exist, tot_anz, tot_amount, str_list_list, preis, wert, i, do_it, mi_subgroup, gl_acct, l_lager, l_ophdr, l_artikel, l_op, parameters, l_untergrup, bediener
        nonlocal trans_code, from_grp, mi_alloc, mi_article, mi_docu, mi_date, mattype, from_lager, to_lager, from_date, to_date, from_art, to_art, show_price, cost_acct, deptno


        nonlocal str_list, s_list
        nonlocal str_list_list, s_list_list

        cc_code = 0

        def generate_inner_output():
            return (cc_code)


        parameters = db_session.query(Parameters).filter(
                 (func.lower(Parameters.progname) == ("CostCenter").lower()) & (func.lower(Parameters.section) == ("Alloc").lower()) & (Parameters.varname > "") & (func.lower(Parameters.vstring) == (fibukonto).lower())).first()

        if parameters:
            cc_code = to_int(parameters.varname)

        return generate_inner_output()


    def create_lista():

        nonlocal it_exist, tot_anz, tot_amount, str_list_list, preis, wert, i, mi_subgroup, gl_acct, l_lager, l_ophdr, l_artikel, l_op, parameters, l_untergrup, bediener
        nonlocal trans_code, from_grp, mi_alloc, mi_article, mi_docu, mi_date, mattype, from_lager, to_lager, from_date, to_date, from_art, to_art, show_price, cost_acct, deptno


        nonlocal str_list, s_list
        nonlocal str_list_list, s_list_list

        t_anz:decimal = to_decimal("0.0")
        t_val:decimal = to_decimal("0.0")
        curr_artnr:int = 0
        lschein:str = ""
        cost_bezeich:str = ""
        fibukonto:str = ""
        do_it:bool = False
        cc_code:int = 0
        other_fibu:bool = False
        gl_acct1 = None
        create_it:bool = False
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        it_exist = False
        str_list_list.clear()
        s_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():
            do_it = True
            curr_artnr = 0

            l_op_obj_list = []
            for l_op, l_ophdr, gl_acct, l_artikel in db_session.query(L_op, L_ophdr, Gl_acct, L_artikel).join(L_ophdr,(func.lower(L_ophdr.op_typ) == ("STT").lower()) & (L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_op.stornogrund)).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                     (L_op.lager_nr == l_lager.lager_nr) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & (L_op.anzahl != 0) & (L_op.op_art == 3) & (L_op.loeschflag <= 1)).order_by(L_op.datum, L_op.lscheinnr, L_op.artnr).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                if show_price:
                    preis =  to_decimal(l_op.einzelpreis)
                    wert =  to_decimal(l_op.warenwert)
                it_exist = True
                other_fibu = False

                if l_op.stornogrund != "":

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

                if create_it and deptno != 0:

                    parameters = db_session.query(Parameters).filter(
                             (func.lower(Parameters.progname) == ("CostCenter").lower()) & (func.lower(Parameters.section) == ("alloc").lower()) & (Parameters.varname == to_string(deptno)) & (func.lower(Parameters.vstring) == (fibukonto).lower())).first()
                    create_it = None != parameters

                if curr_artnr == 0:
                    curr_artnr = l_op.artnr

                if (curr_artnr != l_op.artnr) and t_anz != 0:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,45 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + "Subtotal "
                    for i in range(1,41 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
                    for i in range(1,14 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
                    t_anz =  to_decimal("0")
                    t_val =  to_decimal("0")
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

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.fibu = fibukonto
                        s_list.bezeich = cost_bezeich

                        if cc_code != 0:
                            s_list.bezeich = to_string(cc_code, "9999 ") + s_list.bezeich
                    s_list.cost = s_list.cost + wert
                    t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)
                    t_val =  to_decimal(t_val) + to_decimal(wert)
                    tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)
                    tot_amount =  to_decimal(tot_amount) + to_decimal(wert)
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    add_id()
                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.fibu = fibukonto
                    str_list.other_fibu = other_fibu
                    str_list.op_recid = l_op._recid
                    str_list.s = to_string(l_op.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_op.anzahl, "->,>>>,>>9.999") + to_string(preis, ">>>,>>>,>>9.99") + to_string(wert, "->,>>>,>>>,>>9.99") + to_string(l_op.lscheinnr, "x(12)")
                    str_list.billdate = l_op.datum

        if t_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,45 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "Subtotal "
            for i in range(1,41 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
            for i in range(1,14 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,41 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.999")
        for i in range(1,14 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("", "x(8)") + to_string("SUMMARY OF EXPENSES", "x(30)")
        tot_amount =  to_decimal("0")

        for s_list in query(s_list_list, sort_by=[("bezeich",False)]):
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(50)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>>>") + to_string(s_list.cost, "->,>>>,>>>,>>9.99")
            tot_amount =  to_decimal(tot_amount) + to_decimal(s_list.cost)
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,69 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")


    def create_listd():

        nonlocal it_exist, tot_anz, tot_amount, str_list_list, preis, wert, i, mi_subgroup, gl_acct, l_lager, l_ophdr, l_artikel, l_op, parameters, l_untergrup, bediener
        nonlocal trans_code, from_grp, mi_alloc, mi_article, mi_docu, mi_date, mattype, from_lager, to_lager, from_date, to_date, from_art, to_art, show_price, cost_acct, deptno


        nonlocal str_list, s_list
        nonlocal str_list_list, s_list_list

        t_anz:decimal = to_decimal("0.0")
        t_val:decimal = to_decimal("0.0")
        curr_artnr:int = 0
        lschein:str = ""
        datum:date = None
        cost_bezeich:str = ""
        fibukonto:str = ""
        do_it:bool = False
        cc_code:int = 0
        other_fibu:bool = False
        gl_acct1 = None
        create_it:bool = False
        curr_zwkum:int = 0
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        it_exist = False
        str_list_list.clear()
        s_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        do_it = True

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():
            do_it = True
            curr_artnr = 0

            l_op_obj_list = []
            for l_op, l_ophdr, gl_acct, l_artikel, l_untergrup in db_session.query(L_op, L_ophdr, Gl_acct, L_artikel, L_untergrup).join(L_ophdr,(func.lower(L_ophdr.op_typ) == ("STT").lower()) & (L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophdr.fibukonto)).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_op.lager_nr == l_lager.lager_nr) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & (L_op.anzahl != 0) & (L_op.op_art == 3) & (L_op.loeschflag <= 1)).order_by(L_untergrup.bezeich, L_op.datum, L_op.artnr).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                if show_price:
                    preis =  to_decimal(l_op.einzelpreis)
                    wert =  to_decimal(l_op.warenwert)
                it_exist = True
                other_fibu = False

                if l_op.stornogrund != "":

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

                if create_it and deptno != 0:

                    parameters = db_session.query(Parameters).filter(
                             (func.lower(Parameters.progname) == ("CostCenter").lower()) & (func.lower(Parameters.section) == ("alloc").lower()) & (Parameters.varname == to_string(deptno)) & (func.lower(Parameters.vstring) == (fibukonto).lower())).first()
                    create_it = None != parameters

                if datum == None:
                    datum = l_op.datum

                if (datum != l_op.datum) and t_anz != 0:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,45 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + "Subtotal "
                    for i in range(1,41 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
                    for i in range(1,14 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
                    t_anz =  to_decimal("0")
                    t_val =  to_decimal("0")
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

                if curr_zwkum != l_untergrup.zwkum:
                    curr_zwkum = l_untergrup.zwkum
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.s = to_string("", "x(8)") + to_string(l_untergrup.bezeich, "x(24)")

                if create_it:

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.subgroup == l_untergrup.bezeich), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.fibu = fibukonto
                        s_list.bezeich = cost_bezeich
                        s_list.subgroup = to_string(l_untergrup.bezeich, "x(24)")

                        if cc_code != 0:
                            s_list.bezeich = to_string(cc_code, "9999 ") + s_list.bezeich
                    s_list.cost = s_list.cost + wert
                    t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)
                    t_val =  to_decimal(t_val) + to_decimal(wert)
                    tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)
                    tot_amount =  to_decimal(tot_amount) + to_decimal(wert)
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    add_id()
                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.fibu = fibukonto
                    str_list.other_fibu = other_fibu
                    str_list.op_recid = l_op._recid
                    str_list.s = to_string(l_op.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_op.anzahl, "->,>>>,>>9.999") + to_string(preis, ">>>,>>>,>>9.99") + to_string(wert, "->,>>>,>>>,>>9.99") + to_string(l_op.lscheinnr, "x(12)")
                    str_list.billdate = l_op.datum

        if t_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,45 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "Subtotal "
            for i in range(1,41 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
            for i in range(1,14 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,41 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.999")
        for i in range(1,14 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("", "x(8)") + to_string("SUMMARY OF EXPENSES", "x(30)")
        tot_amount =  to_decimal("0")

        for s_list in query(s_list_list, sort_by=[("bezeich",False)]):
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.subgroup, "x(50)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>>>") + to_string(s_list.cost, "->,>>>,>>>,>>9.99")
            tot_amount =  to_decimal(tot_amount) + to_decimal(s_list.cost)
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,69 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")


    def create_list1d():

        nonlocal it_exist, tot_anz, tot_amount, str_list_list, preis, wert, i, mi_subgroup, gl_acct, l_lager, l_ophdr, l_artikel, l_op, parameters, l_untergrup, bediener
        nonlocal trans_code, from_grp, mi_alloc, mi_article, mi_docu, mi_date, mattype, from_lager, to_lager, from_date, to_date, from_art, to_art, show_price, cost_acct, deptno


        nonlocal str_list, s_list
        nonlocal str_list_list, s_list_list

        t_anz:decimal = to_decimal("0.0")
        t_val:decimal = to_decimal("0.0")
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
        gl_acct1 = None
        curr_zwkum:int = 0
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        it_exist = False
        str_list_list.clear()
        s_list_list.clear()

        if mattype == 1:
            grp2 = 0

        elif mattype == 2:
            grp1 = 1
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        do_it = True

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():
            do_it = True
            curr_artnr = 0

            l_op_obj_list = []
            for l_op, l_artikel, l_ophdr, gl_acct, l_untergrup in db_session.query(L_op, L_artikel, L_ophdr, Gl_acct, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).join(L_ophdr,(func.lower(L_ophdr.op_typ) == ("STT").lower()) & (L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophdr.fibukonto)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter(
                     (L_op.lager_nr == l_lager.lager_nr) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & (L_op.anzahl != 0) & (L_op.op_art == 3) & (L_op.loeschflag <= 1)).order_by(L_untergrup.bezeich, L_op.datum, L_op.artnr).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                if show_price:
                    preis =  to_decimal(l_op.einzelpreis)
                    wert =  to_decimal(l_op.warenwert)
                it_exist = True
                other_fibu = False

                if l_op.stornogrund != "":

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

                if create_it and deptno != 0:

                    parameters = db_session.query(Parameters).filter(
                             (func.lower(Parameters.progname) == ("CostCenter").lower()) & (func.lower(Parameters.section) == ("alloc").lower()) & (Parameters.varname == to_string(deptno)) & (func.lower(Parameters.vstring) == (fibukonto).lower())).first()
                    create_it = None != parameters

                if datum == None:
                    datum = l_op.datum

                if datum != l_op.datum and t_anz != 0:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,45 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + "Subtotal "
                    for i in range(1,41 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
                    for i in range(1,14 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
                    t_anz =  to_decimal("0")
                    t_val =  to_decimal("0")
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

                if curr_zwkum != l_untergrup.zwkum:
                    curr_zwkum = l_untergrup.zwkum
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.s = to_string("", "x(8)") + to_string(l_untergrup.bezeich, "x(24)")

                if create_it:

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.subgroup == l_untergrup.bezeich), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.fibu = fibukonto
                        s_list.bezeich = cost_bezeich
                        s_list.subgroup = to_string(l_untergrup.bezeich, "x(24)")

                        if cc_code != 0:
                            s_list.bezeich = to_string(cc_code, "9999 ") + s_list.bezeich
                    s_list.cost = s_list.cost + wert
                    t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)
                    t_val =  to_decimal(t_val) + to_decimal(wert)
                    tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)
                    tot_amount =  to_decimal(tot_amount) + to_decimal(wert)
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    add_id()
                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.other_fibu = other_fibu
                    str_list.fibu = fibukonto
                    str_list.op_recid = l_op._recid
                    str_list.s = to_string(l_op.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(50)") + to_string(l_op.anzahl, "->,>>>,>>9.999") + to_string(preis, ">>>,>>>,>>9.99") + to_string(wert, "->,>>>,>>>,>>9.99") + to_string(l_op.lscheinnr, "x(12)")
                    str_list.billdate = l_op.datum

        if t_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,45 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "Subtotal "
            for i in range(1,41 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
            for i in range(1,14 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,41 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.999")
        for i in range(1,14 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("", "x(8)") + to_string("SUMMARY OF EXPENSES", "x(30)")
        tot_amount =  to_decimal("0")

        for s_list in query(s_list_list, sort_by=[("bezeich",False)]):
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(50)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>>>") + to_string(s_list.cost, "->,>>>,>>>,>>9.99")
            tot_amount =  to_decimal(tot_amount) + to_decimal(s_list.cost)
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,69 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")

    if num_entries(trans_code, ";") > 1:
        mi_subgroup = logical(entry(1, trans_code, ";"))
        trans_code = entry(0, trans_code, ";")
    trans_code = replace_str(trans_code, ";", "")

    if trans_code != "":
        create_list_trans()
    else:

        if from_grp == 0:

            if mi_alloc :
                create_list()

            elif mi_article :
                create_lista()

            elif mi_docu :
                create_listb()

            elif mi_date :
                create_listc()

            elif mi_subgroup :
                create_listd()
        else:

            if mi_alloc :
                create_list1()

            elif mi_article :
                create_list1a()

            elif mi_docu :
                create_list1b()

            elif mi_date :
                create_list1c()

            elif mi_date :
                create_list1d()

    return generate_output()