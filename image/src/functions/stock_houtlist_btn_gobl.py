from functions.additional_functions import *
import decimal
from datetime import date
from functions.stockhoutli_arch import stockhoutli_arch
from sqlalchemy import func
from models import Gl_acct, L_lager, L_ophhis, L_artikel, L_ophis, Parameters, L_untergrup

def stock_houtlist_btn_gobl(pvilanguage:int, trans_code:str, from_grp:int, mi_alloc_chk:bool, mi_article_chk:bool, mi_docu_chk:bool, mi_date_chk:bool, from_lager:int, to_lager:int, from_date:date, to_date:date, from_art:int, to_art:int, deptno:int, long_digit:bool, cost_acct:str, mattype:int):
    it_exist = False
    str_list_list = []
    tot_anz:decimal = 0
    tot_amount:decimal = 0
    i:int = 0
    lvcarea:str = "stock_houtlist"
    gl_acct = l_lager = l_ophhis = l_artikel = l_ophis = parameters = l_untergrup = None

    s_list = str_list = gl_acct1 = None

    s_list_list, S_list = create_model("S_list", {"fibu":str, "cost_center":str, "bezeich":str, "cost":decimal})
    str_list_list, Str_list = create_model("Str_list", {"fibu":str, "other_fibu":bool, "op_recid":int, "lscheinnr":str, "s":str, "mark":str})

    Gl_acct1 = Gl_acct

    db_session = local_storage.db_session

    def generate_output():
        nonlocal it_exist, str_list_list, tot_anz, tot_amount, i, lvcarea, gl_acct, l_lager, l_ophhis, l_artikel, l_ophis, parameters, l_untergrup
        nonlocal gl_acct1


        nonlocal s_list, str_list, gl_acct1
        nonlocal s_list_list, str_list_list
        return {"it_exist": it_exist, "str-list": str_list_list}

    def create_lista():

        nonlocal it_exist, str_list_list, tot_anz, tot_amount, i, lvcarea, gl_acct, l_lager, l_ophhis, l_artikel, l_ophis, parameters, l_untergrup
        nonlocal gl_acct1


        nonlocal s_list, str_list, gl_acct1
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
        Gl_acct1 = Gl_acct
        it_exist = False
        str_list_list.clear()
        s_list_list.clear()
        tot_anz = 0
        tot_amount = 0

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():
            do_it = True
            curr_artnr = 0

            if CONNECTED ("vhparch"):
                it_exist, t_anz, t_val, tot_anz, tot_amount = get_output(stockhoutli_arch('listA', l_lager.lager_nr, from_date, to_date, from_art, to_art, deptno, long_digit, do_it, l_lager.bezeich, from_grp, "", ""))
            else:

                l_ophis_obj_list = []
                for l_ophis, l_ophhis, gl_acct, l_artikel in db_session.query(L_ophis, L_ophhis, Gl_acct, L_artikel).join(L_ophhis,(func.lower(L_ophhis.op_typ) == "STT") &  (L_ophhis.lscheinnr == L_ophis.lscheinnr) &  (L_ophhis.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophis.fibukonto)).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).filter(
                        (L_ophis.lager_nr == l_lager.lager_nr) &  (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.artnr >= from_art) &  (L_ophis.artnr <= to_art) &  (L_ophis.anzahl != 0) &  (L_ophis.op_art == 3)).all():
                    if l_ophis._recid in l_ophis_obj_list:
                        continue
                    else:
                        l_ophis_obj_list.append(l_ophis._recid)


                    it_exist = True
                    other_fibu = False

                    if l_ophis.fibukonto != "":

                        if deptno != 0:

                            gl_acct1 = db_session.query(Gl_acct1).filter(
                                    (Gl_acct1.fibukonto == l_ophis.fibukonto) &  (Gl_acct1.deptnr == deptno)).first()
                        else:

                            gl_acct1 = db_session.query(Gl_acct1).filter(
                                    (Gl_acct1.fibukonto == l_ophis.fibukonto)).first()

                        if gl_acct1:
                            other_fibu = True

                    if other_fibu:
                        cc_code = get_costcenter_code(gl_acct1.fibukonto)
                    else:
                        cc_code = get_costcenter_code(gl_acct.fibukonto)

                    if lschein == "":
                        lschein = l_ophis.lscheinnr

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
                                (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "alloc") &  (Parameters.varname == to_string(deptno)) &  (Parameters.vstring == gl_acct.fibukonto)).first()
                        create_it = None != parameters

                    if curr_artnr == 0:
                        curr_artnr = l_ophis.artnr

                    if (curr_artnr != l_ophis.artnr) and t_anz != 0:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        for i in range(1,45 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.s = str_list.s + "Subtotal "
                        for i in range(1,46 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
                        for i in range(1,12 + 1) :
                            str_list.s = str_list.s + " "

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_val, "->>>>,>>>,>>>,>>9")
                        t_anz = 0
                        t_val = 0
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        lschein = l_ophis.lscheinnr
                        curr_artnr = l_ophis.artnr

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
                        s_list.cost = s_list.cost + l_ophis.warenwert
                        t_anz = t_anz + l_ophis.anzahl
                        t_val = t_val + l_ophis.warenwert
                        tot_anz = tot_anz + l_ophis.anzahl
                        tot_amount = tot_amount + l_ophis.warenwert
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.lscheinnr = l_ophis.lscheinnr
                        str_list.fibu = fibukonto
                        str_list.other_fibu = other_fibu
                        str_list.op_recid = l_op._recid

                        if not long_digit:

                            if l_ophis.einzelpreis > 9999999:
                                str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(45)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")
                            else:
                                str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(45)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")
                        else:
                            str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(45)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->>>>,>>>,>>>,>>9") + to_string(l_ophis.lscheinnr, "x(12)")

        if t_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,45 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "Subtotal "
            for i in range(1,46 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
            for i in range(1,12 + 1) :
                str_list.s = str_list.s + " "

            if not long_digit:
                str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(t_val, "->>>>,>>>,>>>,>>9")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,46 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.999")
        for i in range(1,12 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->>>>,>>>,>>>,>>9")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("", "x(8)") +\
                to_string(translateExtended ("SUMMARY OF EXPENSES", lvcarea, "") , "x(30)")
        str_list.mark = "Summary"


        tot_amount = 0

        for s_list in query(s_list_list):
            str_list = Str_list()
            str_list_list.append(str_list)


            if not long_digit:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(45)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->,>>>,>>>,>>9.99")
            else:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(45)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->>>>,>>>,>>>,>>9")
            tot_amount = tot_amount + s_list.cost
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,72 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->>>>,>>>,>>>,>>9")

    def create_listb():

        nonlocal it_exist, str_list_list, tot_anz, tot_amount, i, lvcarea, gl_acct, l_lager, l_ophhis, l_artikel, l_ophis, parameters, l_untergrup
        nonlocal gl_acct1


        nonlocal s_list, str_list, gl_acct1
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
        Gl_acct1 = Gl_acct
        it_exist = False
        str_list_list.clear()
        s_list_list.clear()
        tot_anz = 0
        tot_amount = 0

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():
            do_it = True
            curr_artnr = 0

            if CONNECTED ("vhparch"):
                it_exist, t_anz, t_val, tot_anz, tot_amount = get_output(stockhoutli_arch('listB', l_lager.lager_nr, from_date, to_date, from_art, to_art, deptno, long_digit, do_it, l_lager.bezeich, from_grp, "", ""))
            else:

                l_ophis_obj_list = []
                for l_ophis, l_ophhis, gl_acct, l_artikel in db_session.query(L_ophis, L_ophhis, Gl_acct, L_artikel).join(L_ophhis,(func.lower(L_ophhis.op_typ) == "STT") &  (L_ophhis.lscheinnr == L_ophis.lscheinnr) &  (L_ophhis.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophis.fibukonto)).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).filter(
                        (L_ophis.lager_nr == l_lager.lager_nr) &  (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.artnr >= from_art) &  (L_ophis.artnr <= to_art) &  (L_ophis.anzahl != 0) &  (L_ophis.op_art == 3)).all():
                    if l_ophis._recid in l_ophis_obj_list:
                        continue
                    else:
                        l_ophis_obj_list.append(l_ophis._recid)


                    it_exist = True
                    other_fibu = False

                    if l_ophis.fibukonto != "":

                        if deptno != 0:

                            gl_acct1 = db_session.query(Gl_acct1).filter(
                                    (Gl_acct1.fibukonto == l_ophis.fibukonto) &  (Gl_acct1.deptnr == deptno)).first()
                        else:

                            gl_acct1 = db_session.query(Gl_acct1).filter(
                                    (Gl_acct1.fibukonto == l_ophis.fibukonto)).first()

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
                                (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "alloc") &  (Parameters.varname == to_string(deptno)) &  (Parameters.vstring == gl_acct.fibukonto)).first()
                        create_it = None != parameters

                    if lschein == "":
                        lschein = l_ophis.lscheinnr

                    if (lschein != l_ophis.lscheinnr) and t_anz != 0:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        for i in range(1,45 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.s = str_list.s + "Subtotal "
                        for i in range(1,46 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
                        for i in range(1,12 + 1) :
                            str_list.s = str_list.s + " "

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_val, "->>>>,>>>,>>>,>>9")
                        t_anz = 0
                        t_val = 0
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        lschein = l_ophis.lscheinnr
                        curr_artnr = l_ophis.artnr

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
                        s_list.cost = s_list.cost + l_ophis.warenwert
                        t_anz = t_anz + l_ophis.anzahl
                        t_val = t_val + l_ophis.warenwert
                        tot_anz = tot_anz + l_ophis.anzahl
                        tot_amount = tot_amount + l_ophis.warenwert
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.lscheinnr = l_ophis.lscheinnr
                        str_list.fibu = fibukonto
                        str_list.other_fibu = other_fibu
                        str_list.op_recid = l_op._recid

                        if not long_digit:

                            if l_ophis.einzelpreis > 9999999:
                                str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")
                            else:
                                str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")
                        else:
                            str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->>>>,>>>,>>>,>>9") + to_string(l_ophis.lscheinnr, "x(12)")

        if t_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,45 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "Subtotal "
            for i in range(1,46 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
            for i in range(1,12 + 1) :
                str_list.s = str_list.s + " "

            if not long_digit:
                str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(t_val, "->>>>,>>>,>>>,>>9")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,46 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.999")
        for i in range(1,12 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->>>>,>>>,>>>,>>9")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("", "x(8)") +\
                to_string(translateExtended ("SUMMARY OF EXPENSES", lvcarea, "") , "x(30)")
        str_list.mark = "Summary"


        tot_amount = 0

        for s_list in query(s_list_list):
            str_list = Str_list()
            str_list_list.append(str_list)


            if not long_digit:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(55)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->,>>>,>>>,>>9.99")
            else:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(55)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->>>>,>>>,>>>,>>9")
            tot_amount = tot_amount + s_list.cost
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,72 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->>>>,>>>,>>>,>>9")

    def create_listc():

        nonlocal it_exist, str_list_list, tot_anz, tot_amount, i, lvcarea, gl_acct, l_lager, l_ophhis, l_artikel, l_ophis, parameters, l_untergrup
        nonlocal gl_acct1


        nonlocal s_list, str_list, gl_acct1
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
        Gl_acct1 = Gl_acct
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

            if CONNECTED ("vhparch"):
                it_exist, t_anz, t_val, tot_anz, tot_amount = get_output(stockhoutli_arch('listC', l_lager.lager_nr, from_date, to_date, from_art, to_art, deptno, long_digit, do_it, l_lager.bezeich, from_grp, "", ""))
            else:

                l_ophis_obj_list = []
                for l_ophis, l_ophhis, gl_acct, l_artikel in db_session.query(L_ophis, L_ophhis, Gl_acct, L_artikel).join(L_ophhis,(func.lower(L_ophhis.op_typ) == "STT") &  (L_ophhis.lscheinnr == L_ophis.lscheinnr) &  (L_ophhis.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophis.fibukonto)).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).filter(
                        (L_ophis.lager_nr == l_lager.lager_nr) &  (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.artnr >= from_art) &  (L_ophis.artnr <= to_art) &  (L_ophis.anzahl != 0) &  (L_ophis.op_art == 3)).all():
                    if l_ophis._recid in l_ophis_obj_list:
                        continue
                    else:
                        l_ophis_obj_list.append(l_ophis._recid)


                    it_exist = True
                    other_fibu = False

                    if l_ophis.fibukonto != "":

                        if deptno != 0:

                            gl_acct1 = db_session.query(Gl_acct1).filter(
                                    (Gl_acct1.fibukonto == l_ophis.fibukonto) &  (Gl_acct1.deptnr == deptno)).first()
                        else:

                            gl_acct1 = db_session.query(Gl_acct1).filter(
                                    (Gl_acct1.fibukonto == l_ophis.fibukonto)).first()

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
                                (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "alloc") &  (Parameters.varname == to_string(deptno)) &  (Parameters.vstring == gl_acct.fibukonto)).first()
                        create_it = None != parameters

                    if datum == None:
                        datum = l_ophis.datum

                    if (datum != l_ophis.datum) and t_anz != 0:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        for i in range(1,45 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.s = str_list.s + "Subtotal "
                        for i in range(1,46 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
                        for i in range(1,12 + 1) :
                            str_list.s = str_list.s + " "

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_val, "->>>>,>>>,>>>,>>9")
                        t_anz = 0
                        t_val = 0
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        lschein = l_ophis.lscheinnr
                        datum = l_ophis.datum
                        curr_artnr = l_ophis.artnr

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
                        s_list.cost = s_list.cost + l_ophis.warenwert
                        t_anz = t_anz + l_ophis.anzahl
                        t_val = t_val + l_ophis.warenwert
                        tot_anz = tot_anz + l_ophis.anzahl
                        tot_amount = tot_amount + l_ophis.warenwert
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.lscheinnr = l_ophis.lscheinnr
                        str_list.fibu = fibukonto
                        str_list.other_fibu = other_fibu
                        str_list.op_recid = l_op._recid

                        if not long_digit:

                            if l_ophis.einzelpreis > 9999999:
                                str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")
                            else:
                                str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")
                        else:
                            str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->>>>,>>>,>>>,>>9") + to_string(l_ophis.lscheinnr, "x(12)")

        if t_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,45 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "Subtotal "
            for i in range(1,46 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
            for i in range(1,12 + 1) :
                str_list.s = str_list.s + " "

            if not long_digit:
                str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(t_val, "->>>>,>>>,>>>,>>9")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,46 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.999")
        for i in range(1,12 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->>>>,>>>,>>>,>>9")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("", "x(8)") +\
                to_string(translateExtended ("SUMMARY OF EXPENSES", lvcarea, "") , "x(30)")
        str_list.mark = "Summary"


        tot_amount = 0

        for s_list in query(s_list_list):
            str_list = Str_list()
            str_list_list.append(str_list)


            if not long_digit:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(55)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->,>>>,>>>,>>9.99")
            else:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(55)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->>>>,>>>,>>>,>>9")
            tot_amount = tot_amount + s_list.cost
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,72 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->>>>,>>>,>>>,>>9")

    def create_list():

        nonlocal it_exist, str_list_list, tot_anz, tot_amount, i, lvcarea, gl_acct, l_lager, l_ophhis, l_artikel, l_ophis, parameters, l_untergrup
        nonlocal gl_acct1


        nonlocal s_list, str_list, gl_acct1
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
        Gl_acct1 = Gl_acct
        it_exist = False
        str_list_list.clear()
        s_list_list.clear()
        tot_anz = 0
        tot_amount = 0

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():
            do_it = True

            if CONNECTED ("vhparch"):
                it_exist, t_anz, t_val, tot_anz, tot_amount = get_output(stockhoutli_arch('list', l_lager.lager_nr, from_date, to_date, from_art, to_art, deptno, long_digit, do_it, l_lager.bezeich, from_grp, "", ""))
            else:

                l_ophis_obj_list = []
                for l_ophis, l_ophhis, gl_acct, l_artikel in db_session.query(L_ophis, L_ophhis, Gl_acct, L_artikel).join(L_ophhis,(func.lower(L_ophhis.op_typ) == "STT") &  (L_ophhis.lscheinnr == L_ophis.lscheinnr) &  (L_ophhis.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophis.fibukonto)).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).filter(
                        (L_ophis.lager_nr == l_lager.lager_nr) &  (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.artnr >= from_art) &  (L_ophis.artnr <= to_art) &  (L_ophis.anzahl != 0) &  (L_ophis.op_art == 3)).all():
                    if l_ophis._recid in l_ophis_obj_list:
                        continue
                    else:
                        l_ophis_obj_list.append(l_ophis._recid)


                    it_exist = True
                    other_fibu = False

                    if l_ophis.fibukonto != "":

                        if deptno != 0:

                            gl_acct1 = db_session.query(Gl_acct1).filter(
                                    (Gl_acct1.fibukonto == l_ophis.fibukonto) &  (Gl_acct1.deptnr == deptno)).first()
                        else:

                            gl_acct1 = db_session.query(Gl_acct1).filter(
                                    (Gl_acct1.fibukonto == l_ophis.fibukonto)).first()

                        if gl_acct1:
                            other_fibu = True

                    if other_fibu:
                        cc_code = get_costcenter_code(gl_acct1.fibukonto)
                    else:
                        cc_code = get_costcenter_code(gl_acct.fibukonto)

                    if lschein == "":
                        lschein = l_ophis.lscheinnr

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
                                (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "alloc") &  (Parameters.varname == to_string(deptno)) &  (func.lower(Parameters.vstring) == (fibukonto).lower())).first()
                        create_it = None != parameters

                    if curr_fibu == "":
                        curr_fibu = fibukonto

                    if curr_fibu.lower()  != (fibukonto).lower()  and t_anz != 0:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        for i in range(1,45 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.s = str_list.s + "Subtotal "
                        for i in range(1,46 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
                        for i in range(1,12 + 1) :
                            str_list.s = str_list.s + " "

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_val, "->>>>,>>>,>>>,>>9")
                        t_anz = 0
                        t_val = 0
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        lschein = l_ophis.lscheinnr
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
                        s_list.cost = s_list.cost + l_ophis.warenwert
                        t_anz = t_anz + l_ophis.anzahl
                        t_val = t_val + l_ophis.warenwert
                        tot_anz = tot_anz + l_ophis.anzahl
                        tot_amount = tot_amount + l_ophis.warenwert
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.lscheinnr = l_ophis.lscheinnr
                        str_list.fibu = fibukonto
                        str_list.other_fibu = other_fibu
                        str_list.op_recid = l_op._recid

                        if not long_digit:

                            if l_ophis.einzelpreis > 9999999:
                                str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")
                            else:
                                str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")
                        else:
                            str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->>>>,>>>,>>>,>>9") + to_string(l_ophis.lscheinnr, "x(12)")

        if t_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,45 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "Subtotal "
            for i in range(1,46 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
            for i in range(1,12 + 1) :
                str_list.s = str_list.s + " "

            if not long_digit:
                str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(t_val, "->>>>,>>>,>>>,>>9")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,46 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.999")
        for i in range(1,12 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->>>>,>>>,>>>,>>9")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        tot_amount = 0

        for s_list in query(s_list_list):
            str_list = Str_list()
            str_list_list.append(str_list)


            if not long_digit:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(55)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->,>>>,>>>,>>9.99")
            else:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(55)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->>>>,>>>,>>>,>>9")
            tot_amount = tot_amount + s_list.cost
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,72 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->>>>,>>>,>>>,>>9")

    def create_list1():

        nonlocal it_exist, str_list_list, tot_anz, tot_amount, i, lvcarea, gl_acct, l_lager, l_ophhis, l_artikel, l_ophis, parameters, l_untergrup
        nonlocal gl_acct1


        nonlocal s_list, str_list, gl_acct1
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

            if CONNECTED ("vhparch"):
                it_exist, t_anz, t_val, tot_anz, tot_amount = get_output(stockhoutli_arch('list1', l_lager.lager_nr, from_date, to_date, from_art, to_art, deptno, long_digit, do_it, l_lager.bezeich, from_grp, grp1, grp2))
            else:

                l_ophis_obj_list = []
                for l_ophis, l_ophhis, gl_acct, l_artikel, l_untergrup in db_session.query(L_ophis, L_ophhis, Gl_acct, L_artikel, L_untergrup).join(L_ophhis,(func.lower(L_ophhis.op_typ) == "STT") &  (L_ophhis.lscheinnr == L_ophis.lscheinnr) &  (L_ophhis.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophis.fibukonto)).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) &  (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum) &  ((L_untergrup.betriebsnr >= grp1) &  (L_untergrup.betriebsnr <= grp2))).filter(
                        (L_ophis.lager_nr == l_lager.lager_nr) &  (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.artnr >= from_art) &  (L_ophis.artnr <= to_art) &  (L_ophis.anzahl != 0) &  (L_ophis.op_art == 3)).all():
                    if l_ophis._recid in l_ophis_obj_list:
                        continue
                    else:
                        l_ophis_obj_list.append(l_ophis._recid)


                    it_exist = True
                    other_fibu = False

                    if l_ophis.fibukonto != "":

                        if deptno != 0:

                            gl_acct1 = db_session.query(Gl_acct1).filter(
                                    (Gl_acct1.fibukonto == l_ophis.fibukonto) &  (Gl_acct1.deptnr == deptno)).first()
                        else:

                            gl_acct1 = db_session.query(Gl_acct1).filter(
                                    (Gl_acct1.fibukonto == l_ophis.fibukonto)).first()

                        if gl_acct1:
                            other_fibu = True

                    if other_fibu:
                        cc_code = get_costcenter_code(gl_acct1.fibukonto)
                    else:
                        cc_code = get_costcenter_code(gl_acct.fibukonto)

                    if lschein == "":
                        lschein = l_ophis.lscheinnr

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
                                (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "alloc") &  (Parameters.varname == to_string(deptno)) &  (Parameters.vstring == gl_acct.fibukonto)).first()
                        create_it = None != parameters

                    if curr_fibu == "":
                        curr_fibu = fibukonto

                    if curr_fibu.lower()  != (fibukonto).lower()  and t_anz != 0 and create_it:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        for i in range(1,45 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.s = str_list.s + "Subtotal "
                        for i in range(1,46 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
                        for i in range(1,12 + 1) :
                            str_list.s = str_list.s + " "

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_val, "->>>>,>>>,>>>,>>9")
                        t_anz = 0
                        t_val = 0
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        lschein = l_ophis.lscheinnr
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
                        s_list.cost = s_list.cost + l_ophis.warenwert
                        t_anz = t_anz + l_ophis.anzahl
                        t_val = t_val + l_ophis.warenwert
                        tot_anz = tot_anz + l_ophis.anzahl
                        tot_amount = tot_amount + l_ophis.warenwert
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.lscheinnr = l_ophis.lscheinnr
                        str_list.other_fibu = other_fibu
                        str_list.fibu = fibukonto
                        str_list.op_recid = l_op._recid

                        if not long_digit:

                            if l_ophis.einzelpreis > 9999999:
                                str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")
                            else:
                                str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")
                        else:
                            str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->>>>,>>>,>>>,>>9") + to_string(l_ophis.lscheinnr, "x(12)")

        if t_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,45 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "Subtotal "
            for i in range(1,46 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
            for i in range(1,12 + 1) :
                str_list.s = str_list.s + " "

            if not long_digit:
                str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(t_val, "->>>>,>>>,>>>,>>9")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,46 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.999")
        for i in range(1,12 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->>>>,>>>,>>>,>>9")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("", "x(8)") +\
                to_string(translateExtended ("SUMMARY OF EXPENSES", lvcarea, "") , "x(30)")
        str_list.mark = "Summary"


        tot_amount = 0

        for s_list in query(s_list_list):
            str_list = Str_list()
            str_list_list.append(str_list)


            if not long_digit:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(55)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->,>>>,>>>,>>9.99")
            else:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(55)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->>>>,>>>,>>>,>>9")
            tot_amount = tot_amount + s_list.cost
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,72 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->>>>,>>>,>>>,>>9")

    def create_list1a():

        nonlocal it_exist, str_list_list, tot_anz, tot_amount, i, lvcarea, gl_acct, l_lager, l_ophhis, l_artikel, l_ophis, parameters, l_untergrup
        nonlocal gl_acct1


        nonlocal s_list, str_list, gl_acct1
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

            if CONNECTED ("vhparch"):
                it_exist, t_anz, t_val, tot_anz, tot_amount = get_output(stockhoutli_arch('list1A', l_lager.lager_nr, from_date, to_date, from_art, to_art, deptno, long_digit, do_it, l_lager.bezeich, from_grp, grp1, grp2))
            else:

                l_ophis_obj_list = []
                for l_ophis, l_artikel, l_ophhis, gl_acct, l_untergrup in db_session.query(L_ophis, L_artikel, L_ophhis, Gl_acct, L_untergrup).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) &  (L_artikel.endkum == from_grp)).join(L_ophhis,(func.lower(L_ophhis.op_typ) == "STT") &  (L_ophhis.lscheinnr == L_ophis.lscheinnr) &  (L_ophhis.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophis.fibukonto)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum) &  ((L_untergrup.betriebsnr >= grp1) &  (L_untergrup.betriebsnr <= grp2))).filter(
                        (L_ophis.lager_nr == l_lager.lager_nr) &  (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.artnr >= from_art) &  (L_ophis.artnr <= to_art) &  (L_ophis.anzahl != 0) &  (L_ophis.op_art == 3)).all():
                    if l_ophis._recid in l_ophis_obj_list:
                        continue
                    else:
                        l_ophis_obj_list.append(l_ophis._recid)


                    it_exist = True
                    other_fibu = False

                    if l_ophis.fibukonto != "":

                        if deptno != 0:

                            gl_acct1 = db_session.query(Gl_acct1).filter(
                                    (Gl_acct1.fibukonto == l_ophis.fibukonto) &  (Gl_acct1.deptnr == deptno)).first()
                        else:

                            gl_acct1 = db_session.query(Gl_acct1).filter(
                                    (Gl_acct1.fibukonto == l_ophis.fibukonto)).first()

                        if gl_acct1:
                            other_fibu = True

                    if other_fibu:
                        cc_code = get_costcenter_code(gl_acct1.fibukonto)
                    else:
                        cc_code = get_costcenter_code(gl_acct.fibukonto)

                    if lschein == "":
                        lschein = l_ophis.lscheinnr

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
                                (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "alloc") &  (Parameters.varname == to_string(deptno)) &  (Parameters.vstring == gl_acct.fibukonto)).first()
                        create_it = None != parameters

                    if curr_artnr == 0:
                        curr_artnr = l_ophis.artnr

                    if curr_artnr != l_ophis.artnr and t_anz != 0:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        for i in range(1,45 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.s = str_list.s + "Subtotal "
                        for i in range(1,46 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
                        for i in range(1,12 + 1) :
                            str_list.s = str_list.s + " "

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9")
                        t_anz = 0
                        t_val = 0
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        lschein = l_ophis.lscheinnr
                        curr_artnr = l_ophis.artnr

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
                        s_list.cost = s_list.cost + l_ophis.warenwert
                        t_anz = t_anz + l_ophis.anzahl
                        t_val = t_val + l_ophis.warenwert
                        tot_anz = tot_anz + l_ophis.anzahl
                        tot_amount = tot_amount + l_ophis.warenwert
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.lscheinnr = l_ophis.lscheinnr
                        str_list.other_fibu = other_fibu
                        str_list.fibu = fibukonto
                        str_list.op_recid = l_op._recid

                        if not long_digit:

                            if l_ophis.einzelpreis > 9999999:
                                str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")
                            else:
                                str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")
                        else:
                            str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->>>>,>>>,>>>,>>9") + to_string(l_ophis.lscheinnr, "x(12)")

        if t_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,45 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "Subtotal "
            for i in range(1,46 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
            for i in range(1,12 + 1) :
                str_list.s = str_list.s + " "

            if not long_digit:
                str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(t_val, "->>>>,>>>,>>>,>>9")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,46 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.999")
        for i in range(1,12 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->>>>,>>>,>>>,>>9")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("", "x(8)") +\
                to_string(translateExtended ("SUMMARY OF EXPENSES", lvcarea, "") , "x(30)")
        str_list.mark = "Summary"


        tot_amount = 0

        for s_list in query(s_list_list):
            str_list = Str_list()
            str_list_list.append(str_list)


            if not long_digit:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(55)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->,>>>,>>>,>>9.99")
            else:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(55)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->>>>,>>>,>>>,>>9")
            tot_amount = tot_amount + s_list.cost
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,72 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->>>>,>>>,>>>,>>9")

    def create_list1b():

        nonlocal it_exist, str_list_list, tot_anz, tot_amount, i, lvcarea, gl_acct, l_lager, l_ophhis, l_artikel, l_ophis, parameters, l_untergrup
        nonlocal gl_acct1


        nonlocal s_list, str_list, gl_acct1
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

            if CONNECTED ("vhparch"):
                it_exist, t_anz, t_val, tot_anz, tot_amount = get_output(stockhoutli_arch('list1B', l_lager.lager_nr, from_date, to_date, from_art, to_art, deptno, long_digit, do_it, l_lager.bezeich, from_grp, grp1, grp2))
            else:

                l_ophis_obj_list = []
                for l_ophis, l_artikel, l_ophhis, gl_acct, l_untergrup in db_session.query(L_ophis, L_artikel, L_ophhis, Gl_acct, L_untergrup).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) &  (L_artikel.endkum == from_grp)).join(L_ophhis,(func.lower(L_ophhis.op_typ) == "STT") &  (L_ophhis.lscheinnr == L_ophis.lscheinnr) &  (L_ophhis.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophis.fibukonto)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum) &  ((L_untergrup.betriebsnr >= grp1) &  (L_untergrup.betriebsnr <= grp2))).filter(
                        (L_ophis.lager_nr == l_lager.lager_nr) &  (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.artnr >= from_art) &  (L_ophis.artnr <= to_art) &  (L_ophis.anzahl != 0) &  (L_ophis.op_art == 3)).all():
                    if l_ophis._recid in l_ophis_obj_list:
                        continue
                    else:
                        l_ophis_obj_list.append(l_ophis._recid)


                    it_exist = True
                    other_fibu = False

                    if l_ophis.fibukonto != "":

                        if deptno != 0:

                            gl_acct1 = db_session.query(Gl_acct1).filter(
                                    (Gl_acct1.fibukonto == l_ophis.fibukonto) &  (Gl_acct1.deptnr == deptno)).first()
                        else:

                            gl_acct1 = db_session.query(Gl_acct1).filter(
                                    (Gl_acct1.fibukonto == l_ophis.fibukonto)).first()

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
                                (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "alloc") &  (Parameters.varname == to_string(deptno)) &  (Parameters.vstring == gl_acct.fibukonto)).first()
                        create_it = None != parameters

                    if lschein == "":
                        lschein = l_ophis.lscheinnr

                    if lschein != l_ophis.lscheinnr and t_anz != 0:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        for i in range(1,45 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.s = str_list.s + "Subtotal "
                        for i in range(1,46 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
                        for i in range(1,12 + 1) :
                            str_list.s = str_list.s + " "

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_val, "->>>>,>>>,>>>,>>9")
                        t_anz = 0
                        t_val = 0
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        lschein = l_ophis.lscheinnr
                        curr_artnr = l_ophis.artnr

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
                        s_list.cost = s_list.cost + l_ophis.warenwert
                        t_anz = t_anz + l_ophis.anzahl
                        t_val = t_val + l_ophis.warenwert
                        tot_anz = tot_anz + l_ophis.anzahl
                        tot_amount = tot_amount + l_ophis.warenwert
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.lscheinnr = l_ophis.lscheinnr
                        str_list.other_fibu = other_fibu
                        str_list.fibu = fibukonto
                        str_list.op_recid = l_op._recid

                        if not long_digit:

                            if l_ophis.einzelpreis > 9999999:
                                str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")
                            else:
                                str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")
                        else:
                            str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->>>>,>>>,>>>,>>9") + to_string(l_ophis.lscheinnr, "x(12)")

        if t_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,45 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "Subtotal "
            for i in range(1,46 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
            for i in range(1,12 + 1) :
                str_list.s = str_list.s + " "

            if not long_digit:
                str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(t_val, "->>>>,>>>,>>>,>>9")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,46 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.999")
        for i in range(1,12 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->>>>,>>>,>>>,>>9")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("", "x(8)") +\
                to_string(translateExtended ("SUMMARY OF EXPENSES", lvcarea, "") , "x(30)")
        str_list.mark = "Summary"


        tot_amount = 0

        for s_list in query(s_list_list):
            str_list = Str_list()
            str_list_list.append(str_list)


            if not long_digit:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(55)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->,>>>,>>>,>>9.99")
            else:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(55)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->>>>,>>>,>>>,>>9")
            tot_amount = tot_amount + s_list.cost
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,72 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->>>>,>>>,>>>,>>9")

    def create_list1c():

        nonlocal it_exist, str_list_list, tot_anz, tot_amount, i, lvcarea, gl_acct, l_lager, l_ophhis, l_artikel, l_ophis, parameters, l_untergrup
        nonlocal gl_acct1


        nonlocal s_list, str_list, gl_acct1
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

            if CONNECTED ("vhparch"):
                it_exist, t_anz, t_val, tot_anz, tot_amount = get_output(stockhoutli_arch('list1C', l_lager.lager_nr, from_date, to_date, from_art, to_art, deptno, long_digit, do_it, l_lager.bezeich, from_grp, grp1, grp2))
            else:

                l_ophis_obj_list = []
                for l_ophis, l_artikel, l_ophhis, gl_acct, l_untergrup in db_session.query(L_ophis, L_artikel, L_ophhis, Gl_acct, L_untergrup).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) &  (L_artikel.endkum == from_grp)).join(L_ophhis,(func.lower(L_ophhis.op_typ) == "STT") &  (L_ophhis.lscheinnr == L_ophis.lscheinnr) &  (L_ophhis.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophis.fibukonto)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum) &  ((L_untergrup.betriebsnr >= grp1) &  (L_untergrup.betriebsnr <= grp2))).filter(
                        (L_ophis.lager_nr == l_lager.lager_nr) &  (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.artnr >= from_art) &  (L_ophis.artnr <= to_art) &  (L_ophis.anzahl != 0) &  (L_ophis.op_art == 3)).all():
                    if l_ophis._recid in l_ophis_obj_list:
                        continue
                    else:
                        l_ophis_obj_list.append(l_ophis._recid)


                    it_exist = True
                    other_fibu = False

                    if l_ophis.fibukonto != "":

                        if deptno != 0:

                            gl_acct1 = db_session.query(Gl_acct1).filter(
                                    (Gl_acct1.fibukonto == l_ophis.fibukonto) &  (Gl_acct1.deptnr == deptno)).first()
                        else:

                            gl_acct1 = db_session.query(Gl_acct1).filter(
                                    (Gl_acct1.fibukonto == l_ophis.fibukonto)).first()

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
                                (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "alloc") &  (Parameters.varname == to_string(deptno)) &  (Parameters.vstring == gl_acct.fibukonto)).first()
                        create_it = None != parameters

                    if datum == None:
                        datum = l_ophis.datum

                    if datum != l_ophis.datum and t_anz != 0:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        for i in range(1,45 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.s = str_list.s + "Subtotal "
                        for i in range(1,46 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
                        for i in range(1,12 + 1) :
                            str_list.s = str_list.s + " "

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_val, "->>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9")
                        t_anz = 0
                        t_val = 0
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        lschein = l_ophis.lscheinnr
                        datum = l_ophis.datum
                        curr_artnr = l_ophis.artnr

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
                        s_list.cost = s_list.cost + l_ophis.warenwert
                        t_anz = t_anz + l_ophis.anzahl
                        t_val = t_val + l_ophis.warenwert
                        tot_anz = tot_anz + l_ophis.anzahl
                        tot_amount = tot_amount + l_ophis.warenwert
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.lscheinnr = l_ophis.lscheinnr
                        str_list.other_fibu = other_fibu
                        str_list.fibu = fibukonto
                        str_list.op_recid = l_op._recid

                        if not long_digit:

                            if l_ophis.einzelpreis > 9999999:
                                str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")
                            else:
                                str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")
                        else:
                            str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->>>>,>>>,>>>,>>9") + to_string(l_ophis.lscheinnr, "x(12)")

        if t_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,45 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "Subtotal "
            for i in range(1,46 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.999")
            for i in range(1,12 + 1) :
                str_list.s = str_list.s + " "

            if not long_digit:
                str_list.s = str_list.s + to_string(t_val, "->,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(t_val, "->>>>,>>>,>>>,>>9")
            str_list = Str_list()
            str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,46 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.999")
        for i in range(1,12 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->>>>,>>>,>>>,>>9")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("", "x(8)") +\
                to_string(translateExtended ("SUMMARY OF EXPENSES", lvcarea, "") , "x(30)")
        str_list.mark = "Summary"


        tot_amount = 0

        for s_list in query(s_list_list):
            str_list = Str_list()
            str_list_list.append(str_list)


            if not long_digit:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(55)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->,>>>,>>>,>>9.99")
            else:
                str_list.s = to_string("", "x(8)") + to_string("", "x(30)") + to_string("", "x(7)") + to_string(s_list.bezeich, "x(55)") + to_string(0, "->>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>") + to_string(s_list.cost, "->>>>,>>>,>>>,>>9")
            tot_amount = tot_amount + s_list.cost
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,45 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,72 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_amount, "->,>>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_amount, "->>>>,>>>,>>>,>>9")

    def get_costcenter_code(fibukonto:str):

        nonlocal it_exist, str_list_list, tot_anz, tot_amount, i, lvcarea, gl_acct, l_lager, l_ophhis, l_artikel, l_ophis, parameters, l_untergrup
        nonlocal gl_acct1


        nonlocal s_list, str_list, gl_acct1
        nonlocal s_list_list, str_list_list

        cc_code = 0

        def generate_inner_output():
            return cc_code

        parameters = db_session.query(Parameters).filter(
                (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Alloc") &  (Parameters.varname > "") &  (func.lower(Parameters.vstring) == (fibukonto).lower())).first()

        if parameters:
            cc_code = to_int(parameters.varname)


        return generate_inner_output()


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