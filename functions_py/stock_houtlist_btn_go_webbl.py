#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
# TODO: Oscar skip for a while
# from functions.stockhoutli_arch import stockhoutli_arch
from models import Gl_acct, L_lager, L_ophhis, Gl_department, L_artikel, L_ophis, Parameters, Queasy, L_untergrup

def stock_houtlist_btn_go_webbl(pvilanguage:int, trans_code:string, from_grp:int, mi_alloc_chk:bool, mi_article_chk:bool, mi_docu_chk:bool, mi_date_chk:bool, from_lager:int, to_lager:int, from_date:date, to_date:date, from_art:int, to_art:int, deptno:int, long_digit:bool, cost_acct:string, mattype:int, mi_sub_group:bool):

    prepare_cache ([Gl_acct, L_lager, Gl_department, L_artikel, L_ophis, Queasy, L_untergrup])

    it_exist = False
    str_list_data = []
    tot_anz:Decimal = to_decimal("0.0")
    tot_amount:Decimal = to_decimal("0.0")
    i:int = 0
    lvcarea:string = "stock-houtlist"
    cost_acct = cost_acct.strip()
    trans_code = trans_code.strip()

    gl_acct = l_lager = l_ophhis = gl_department = l_artikel = l_ophis = parameters = queasy = l_untergrup = None

    s_list = str_list = None

    s_list_data, S_list = create_model("S_list", {"fibu":string, "cost_center":string, "bezeich":string, "cost":Decimal})
    str_list_data, Str_list = create_model("Str_list", {"fibu":string, "other_fibu":bool, "op_recid":int, "lscheinnr":string, "s":string, "mark":string, "gldept":string, "masseinheit":string, "datum":string, "bezeich":string, "artnr":string, "description":string, "anzahl":string, "einzelpreis":string, "warenwert":string, "remark_artikel":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal it_exist, str_list_data, tot_anz, tot_amount, i, lvcarea, gl_acct, l_lager, l_ophhis, gl_department, l_artikel, l_ophis, parameters, queasy, l_untergrup
        nonlocal pvilanguage, trans_code, from_grp, mi_alloc_chk, mi_article_chk, mi_docu_chk, mi_date_chk, from_lager, to_lager, from_date, to_date, from_art, to_art, deptno, long_digit, cost_acct, mattype, mi_sub_group


        nonlocal s_list, str_list
        nonlocal s_list_data, str_list_data

        return {"it_exist": it_exist, "str-list": str_list_data}

    def format_fixed_length(text: str, length: int) -> str:
        if len(text) > length:
            return text[:length]   # trim
        else:
            return text.ljust(length)

    def check_connection_arch():
        # TODO: Oscar - need to handle how to connect to vhparch database
        return False

    def create_list_trans():

        nonlocal it_exist, str_list_data, tot_anz, tot_amount, i, lvcarea, gl_acct, l_lager, l_ophhis, gl_department, l_artikel, l_ophis, parameters, queasy, l_untergrup
        nonlocal pvilanguage, trans_code, from_grp, mi_alloc_chk, mi_article_chk, mi_docu_chk, mi_date_chk, from_lager, to_lager, from_date, to_date, from_art, to_art, deptno, long_digit, cost_acct, mattype, mi_sub_group


        nonlocal s_list, str_list
        nonlocal s_list_data, str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        curr_artnr:int = 0
        lschein:string = ""
        cost_bezeich:string = ""
        fibukonto:string = ""
        do_it:bool = False
        cc_code:int = 0
        other_fibu:bool = False
        gl_acct1 = None
        create_it:bool = False
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        it_exist = False
        str_list_data.clear()
        s_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        trans_code = trim(trans_code)

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():

            do_it = True
            curr_artnr = 0

            l_ophis_obj_list = {}
            for l_ophis, l_ophhis, gl_acct, gl_department, l_artikel in db_session.query(L_ophis, L_ophhis, Gl_acct, Gl_department, L_artikel).join(L_ophhis,(L_ophhis.op_typ == ("STT").lower()) & (L_ophhis.lscheinnr == L_ophis.lscheinnr) & (L_ophhis.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophis.fibukonto)).join(Gl_department,(Gl_department.nr == Gl_acct.deptnr)).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).filter((L_ophis.lager_nr == l_lager.lager_nr) & (L_ophis.anzahl != 0) & (L_ophis.op_art == 3) & (L_ophis.lscheinnr == (trans_code).lower())).order_by(L_ophis.datum, L_ophis.lscheinnr).all():

                # if l_ophis_obj_list.get(l_ophis._recid):
                #     continue
                # else:
                #     l_ophis_obj_list[l_ophis._recid] = True

                it_exist = True
                other_fibu = False

                if l_ophis.fibukonto != "":

                    if deptno != 0:
                        gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)],"deptnr": [(eq, deptno)]})
                    else:
                        gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)]})

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

                    parameters = get_cache (Parameters, {"progname": [(eq, "costcenter")],"section": [(eq, "alloc")],"varname": [(eq, to_string(deptno))],"vstring": [(eq, gl_acct.fibukonto)]})
                    create_it = None != parameters

                if curr_artnr == 0:
                    curr_artnr = l_ophis.artnr

                if (curr_artnr != l_ophis.artnr) and t_anz != 0:
                    str_list = Str_list()
                    str_list_data.append(str_list)

                    str_list.description = "Subtotal"
                    str_list.anzahl = to_string(t_anz, "->,>>>,>>9.999")

                    if not long_digit:
                        str_list.warenwert = to_string(t_val, "->,>>>,>>>,>>9.99")
                    else:
                        str_list.warenwert = to_string(t_val, "->>>,>>>,>>>,>>9")

                    t_anz =  to_decimal("0")
                    t_val =  to_decimal("0")

                    str_list = Str_list()
                    str_list_data.append(str_list)

                    lschein = l_ophis.lscheinnr
                    curr_artnr = l_ophis.artnr

                if do_it:
                    str_list = Str_list()
                    str_list_data.append(str_list)

                    str_list = Str_list()
                    str_list_data.append(str_list)

                    # str_list.s = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(24)")
                    # str_list.bezeich = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(36)")
                    str_list.s = to_string("", "x(8)") + format_fixed_length(l_lager.bezeich, 24)
                    str_list.bezeich = to_string("", "x(8)") + format_fixed_length(l_lager.bezeich, 36)
                    str_list = Str_list()
                    str_list_data.append(str_list)

                    do_it = False

                if create_it:

                    s_list = query(s_list_data, filters=(lambda s_list: s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_data.append(s_list)

                        s_list.fibu = fibukonto
                        s_list.bezeich = cost_bezeich

                        if cc_code != 0:
                            s_list.bezeich = to_string(cc_code, "9999") + " " + s_list.bezeich

                    s_list.cost = s_list.cost + l_ophis.warenwert
                    t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                    t_val =  to_decimal(t_val) + to_decimal(l_ophis.warenwert)
                    tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                    str_list = Str_list()
                    str_list_data.append(str_list)

                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.fibu = fibukonto
                    str_list.other_fibu = other_fibu
                    str_list.op_recid = l_ophis._recid
                    str_list.gldept = to_string(gl_department.nr) + " - " + gl_department.bezeich
                    str_list.masseinheit = l_artikel.masseinheit

                    queasy = get_cache (Queasy, {"key": [(eq, 340)],"char1": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)],"deci1": [(eq, l_ophis.einzelpreis)]})

                    if queasy:
                        str_list.remark_artikel = queasy.char2
                    else:
                        str_list.remark_artikel = ""

                    if not long_digit:

                        if l_ophis.einzelpreis > 9999999:
                            str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                            str_list.bezeich = to_string(s_list.bezeich)
                            str_list.artnr = to_string(l_artikel.artnr)
                            str_list.description = to_string(l_artikel.bezeich, "x(55)")
                            str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                            str_list.einzelpreis = to_string(l_ophis.einzelpreis, " >>>,>>>,>>9")
                            str_list.warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                            # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")

                            if l_ophis.warenwert >= 0:
                                tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">,>>>,>>>,>>9.99"), 17)
                            else:
                                tmp_warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                            if l_ophis.anzahl >= 0:
                                tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                            else:
                                tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                            str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + format_fixed_length(to_string(l_ophis.einzelpreis, ">>>,>>>,>>9"), 12) + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)
                        else:
                            str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                            str_list.bezeich = to_string(s_list.bezeich)
                            str_list.artnr = to_string(l_artikel.artnr)
                            str_list.description = to_string(l_artikel.bezeich)
                            str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                            str_list.einzelpreis = to_string(l_ophis.einzelpreis, ">,>>>,>>9.99")
                            str_list.warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                            # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")

                            if l_ophis.warenwert >= 0:
                                tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">,>>>,>>>,>>9.99"), 17)
                            else:
                                tmp_warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                            if l_ophis.anzahl >= 0:
                                tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                            else:
                                tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                            str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)
                    else:
                        str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                        str_list.bezeich = to_string(s_list.bezeich)
                        str_list.artnr = to_string(l_artikel.artnr)
                        str_list.description = to_string(l_artikel.bezeich, "x(55)")
                        str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                        str_list.einzelpreis = to_string(l_ophis.einzelpreis, " >>>,>>>,>>9")
                        str_list.warenwert = to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9")

                        # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9") + to_string(l_ophis.lscheinnr, "x(12)")

                        if l_ophis.warenwert >= 0:
                            tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">>>,>>>,>>>,>>9"), 16)
                        else:
                            tmp_warenwert = to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9")

                        if l_ophis.anzahl >= 0:
                            tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                        else:
                            tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                        str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + format_fixed_length(to_string(l_ophis.einzelpreis, ">>>,>>>,>>9"), 12) + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)

        if t_anz != 0:
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.description = "Subtotal "
            str_list.anzahl = to_string(t_anz, "->,>>>,>>9.999")

            if not long_digit:
                str_list.warenwert = trim(to_string(t_val, "->,>>>,>>>,>>9.99"))
            else:
                str_list.warenwert = trim(to_string(t_val, "->>>,>>>,>>>,>>9"))

            str_list = Str_list()
            str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.description = "T O T A L"
        str_list.anzahl = to_string(tot_anz, "->,>>>,>>9.999")

        if not long_digit:
            str_list.warenwert = trim(to_string(tot_amount, "->,>>>,>>>,>>9.99"))
        else:
            str_list.warenwert = trim(to_string(tot_amount, "->>>>,>>>,>>>,>>9"))

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        # str_list.s = to_string("", "x(8)") + to_string(translateExtended ("SUMMARY OF EXPENSES", lvcarea, "") , "x(30)")
        str_list.s = to_string("", "x(8)") + format_fixed_length(translateExtended ("SUMMARY OF EXPENSES", lvcarea, ""), 30)
        str_list.mark = "Summary"

        tot_amount =  to_decimal("0")

        for s_list in query(s_list_data, sort_by=[("bezeich",False)]):
            str_list = Str_list()
            str_list_data.append(str_list)

            if not long_digit:
                # str_list.description = to_string(s_list.bezeich, "x(32)")
                str_list.description = format_fixed_length(s_list.bezeich, 32)
                str_list.warenwert = trim(to_string(s_list.cost, "->,>>>,>>>,>>9.99"))
            else:
                # str_list.description = to_string(s_list.bezeich, "x(32)")
                str_list.description = format_fixed_length(s_list.bezeich, 32)
                str_list.warenwert = trim(to_string(s_list.cost, "->>>>,>>>,>>>,>>9"))

            tot_amount =  to_decimal(tot_amount) + to_decimal(s_list.cost)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.description = "T O T A L"

        if not long_digit:
            str_list.warenwert = trim(to_string(tot_amount, "->,>>>,>>>,>>9.99"))
        else:
            str_list.warenwert = trim(to_string(tot_amount, "->>>>,>>>,>>>,>>9"))


    def create_lista():

        nonlocal it_exist, str_list_data, tot_anz, tot_amount, i, lvcarea, gl_acct, l_lager, l_ophhis, gl_department, l_artikel, l_ophis, parameters, queasy, l_untergrup
        nonlocal pvilanguage, trans_code, from_grp, mi_alloc_chk, mi_article_chk, mi_docu_chk, mi_date_chk, from_lager, to_lager, from_date, to_date, from_art, to_art, deptno, long_digit, cost_acct, mattype, mi_sub_group


        nonlocal s_list, str_list
        nonlocal s_list_data, str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        curr_artnr:int = 0
        lschein:string = ""
        cost_bezeich:string = ""
        fibukonto:string = ""
        do_it:bool = False
        cc_code:int = 0
        other_fibu:bool = False
        gl_acct1 = None
        create_it:bool = False
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        it_exist = False
        str_list_data.clear()
        s_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():
            do_it = True
            curr_artnr = 0

            is_connected_to_vhparch = check_connection_arch()

            if is_connected_to_vhparch:
                it_exist, t_anz, t_val, tot_anz, tot_amount = get_output(stockhoutli_arch('listA', l_lager.lager_nr, from_date, to_date, from_art, to_art, deptno, long_digit, do_it, l_lager.bezeich, from_grp, "", ""))
            else:
                l_ophis_obj_list = {}
                for l_ophis, l_ophhis, gl_acct, gl_department, l_artikel in db_session.query(L_ophis, L_ophhis, Gl_acct, Gl_department, L_artikel).join(L_ophhis,(L_ophhis.op_typ == ("STT").lower()) & (L_ophhis.lscheinnr == L_ophis.lscheinnr) & (L_ophhis.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophis.fibukonto)).join(Gl_department,(Gl_department.nr == Gl_acct.deptnr)).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).filter((L_ophis.lager_nr == l_lager.lager_nr) & (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.artnr >= from_art) & (L_ophis.artnr <= to_art) & (L_ophis.anzahl != 0) & (L_ophis.op_art == 3)).order_by(L_ophis.datum, L_ophis.lscheinnr, L_ophis.artnr).all():

                    # if l_ophis_obj_list.get(l_ophis._recid):
                    #     continue
                    # else:
                    #     l_ophis_obj_list[l_ophis._recid] = True

                    it_exist = True
                    other_fibu = False

                    if l_ophis.fibukonto != "":

                        if deptno != 0:
                            gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)],"deptnr": [(eq, deptno)]})
                        else:
                            gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)]})

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

                        parameters = get_cache (Parameters, {"progname": [(eq, "costcenter")],"section": [(eq, "alloc")],"varname": [(eq, to_string(deptno))],"vstring": [(eq, gl_acct.fibukonto)]})
                        create_it = None != parameters

                    if curr_artnr == 0:
                        curr_artnr = l_ophis.artnr

                    if (curr_artnr != l_ophis.artnr) and t_anz != 0:
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list.description = "Subtotal"
                        str_list.anzahl = to_string(t_anz, "->,>>>,>>9.999")

                        if not long_digit:
                            str_list.warenwert = to_string(t_val, "->,>>>,>>>,>>9.99")
                        else:
                            str_list.warenwert = to_string(t_val, "->>>,>>>,>>>,>>9")

                        t_anz =  to_decimal("0")
                        t_val =  to_decimal("0")

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        lschein = l_ophis.lscheinnr
                        curr_artnr = l_ophis.artnr

                    if do_it:
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        # str_list.s = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(24)")
                        # str_list.bezeich = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(36)")
                        str_list.s = to_string("", "x(8)") + format_fixed_length(l_lager.bezeich, 24)
                        str_list.bezeich = to_string("", "x(8)") + format_fixed_length(l_lager.bezeich, 36)
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        do_it = False

                    if create_it:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.fibu = fibukonto
                            s_list.bezeich = cost_bezeich

                            if cc_code != 0:
                                s_list.bezeich = to_string(cc_code, "9999") + " " + s_list.bezeich

                        s_list.cost = s_list.cost + l_ophis.warenwert
                        t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                        t_val =  to_decimal(t_val) + to_decimal(l_ophis.warenwert)
                        tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list.lscheinnr = l_ophis.lscheinnr
                        str_list.fibu = fibukonto
                        str_list.other_fibu = other_fibu
                        str_list.op_recid = l_ophis._recid
                        str_list.gldept = to_string(gl_department.nr) + " - " + gl_department.bezeich
                        str_list.masseinheit = l_artikel.masseinheit

                        queasy = get_cache (Queasy, {"key": [(eq, 340)],"char1": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)],"deci1": [(eq, l_ophis.einzelpreis)]})

                        if queasy:
                            str_list.remark_artikel = queasy.char2
                        else:
                            str_list.remark_artikel = ""

                        if not long_digit:

                            if l_ophis.einzelpreis > 9999999:
                                str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                                str_list.bezeich = to_string(s_list.bezeich)
                                str_list.artnr = to_string(l_artikel.artnr)
                                str_list.description = to_string(l_artikel.bezeich, "x(55)")
                                str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                                str_list.einzelpreis = to_string(l_ophis.einzelpreis, " >>>,>>>,>>9")
                                str_list.warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")

                                if l_ophis.warenwert >= 0:
                                    tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">,>>>,>>>,>>9.99"), 17)
                                else:
                                    tmp_warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                if l_ophis.anzahl >= 0:
                                    tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                                else:
                                    tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                                str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + format_fixed_length(to_string(l_ophis.einzelpreis, ">>>,>>>,>>9"), 12) + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)
                            else:
                                str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                                str_list.bezeich = to_string(s_list.bezeich)
                                str_list.artnr = to_string(l_artikel.artnr)
                                str_list.description = to_string(l_artikel.bezeich)
                                str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                                str_list.einzelpreis = to_string(l_ophis.einzelpreis, ">,>>>,>>9.99")
                                str_list.warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")

                                if l_ophis.warenwert >= 0:
                                    tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">,>>>,>>>,>>9.99"), 17)
                                else:
                                    tmp_warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                if l_ophis.anzahl >= 0:
                                    tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                                else:
                                    tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                                str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)
                        else:
                            str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                            str_list.bezeich = to_string(s_list.bezeich)
                            str_list.artnr = to_string(l_artikel.artnr)
                            str_list.description = to_string(l_artikel.bezeich, "x(55)")
                            str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                            str_list.einzelpreis = to_string(l_ophis.einzelpreis, " >>>,>>>,>>9")
                            str_list.warenwert = to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9")

                            # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9") + to_string(l_ophis.lscheinnr, "x(12)")

                            if l_ophis.warenwert >= 0:
                                tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">>>,>>>,>>>,>>9"), 16)
                            else:
                                tmp_warenwert = to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9")

                            if l_ophis.anzahl >= 0:
                                tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                            else:
                                tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                            str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + format_fixed_length(to_string(l_ophis.einzelpreis, ">>>,>>>,>>9"), 12) + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)

        if t_anz != 0:
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.description = "Subtotal "
            str_list.anzahl = to_string(t_anz, "->,>>>,>>9.999")

            if not long_digit:
                str_list.warenwert = trim(to_string(t_val, "->,>>>,>>>,>>9.99"))
            else:
                str_list.warenwert = trim(to_string(t_val, "->>>,>>>,>>>,>>9"))

            str_list = Str_list()
            str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.description = "T O T A L"
        str_list.anzahl = to_string(tot_anz, "->,>>>,>>9.999")

        if not long_digit:
            str_list.warenwert = trim(to_string(tot_amount, "->,>>>,>>>,>>9.99"))
        else:
            str_list.warenwert = trim(to_string(tot_amount, "->>>>,>>>,>>>,>>9"))

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        # str_list.s = to_string("", "x(8)") + to_string(translateExtended ("SUMMARY OF EXPENSES", lvcarea, "") , "x(30)")
        str_list.s = to_string("", "x(8)") + format_fixed_length(translateExtended ("SUMMARY OF EXPENSES", lvcarea, ""), 30)
        str_list.mark = "Summary"

        tot_amount =  to_decimal("0")

        for s_list in query(s_list_data, sort_by=[("bezeich",False)]):
            str_list = Str_list()
            str_list_data.append(str_list)

            if not long_digit:
                # str_list.description = to_string(s_list.bezeich, "x(32)")
                str_list.description = format_fixed_length(s_list.bezeich, 32)
                str_list.warenwert = trim(to_string(s_list.cost, "->,>>>,>>>,>>9.99"))
            else:
                # str_list.description = to_string(s_list.bezeich, "x(32)")
                str_list.description = format_fixed_length(s_list.bezeich, 32)
                str_list.warenwert = trim(to_string(s_list.cost, "->>>>,>>>,>>>,>>9"))

            tot_amount =  to_decimal(tot_amount) + to_decimal(s_list.cost)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.description = "T O T A L"

        if not long_digit:
            str_list.warenwert = trim(to_string(tot_amount, "->,>>>,>>>,>>9.99"))
        else:
            str_list.warenwert = trim(to_string(tot_amount, "->>>>,>>>,>>>,>>9"))


    def create_listb():

        nonlocal it_exist, str_list_data, tot_anz, tot_amount, i, lvcarea, gl_acct, l_lager, l_ophhis, gl_department, l_artikel, l_ophis, parameters, queasy, l_untergrup
        nonlocal pvilanguage, trans_code, from_grp, mi_alloc_chk, mi_article_chk, mi_docu_chk, mi_date_chk, from_lager, to_lager, from_date, to_date, from_art, to_art, deptno, long_digit, cost_acct, mattype, mi_sub_group


        nonlocal s_list, str_list
        nonlocal s_list_data, str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        curr_artnr:int = 0
        lschein:string = ""
        cost_bezeich:string = ""
        fibukonto:string = ""
        do_it:bool = False
        cc_code:int = 0
        other_fibu:bool = False
        gl_acct1 = None
        create_it:bool = False
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        it_exist = False
        str_list_data.clear()
        s_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():

            do_it = True
            curr_artnr = 0

            is_connected_to_vhparch = check_connection_arch()

            if is_connected_to_vhparch:
                it_exist, t_anz, t_val, tot_anz, tot_amount = get_output(stockhoutli_arch('listB', l_lager.lager_nr, from_date, to_date, from_art, to_art, deptno, long_digit, do_it, l_lager.bezeich, from_grp, "", ""))
            else:
                l_ophis_obj_list = {}
                for l_ophis, l_ophhis, gl_acct, gl_department, l_artikel in db_session.query(L_ophis, L_ophhis, Gl_acct, Gl_department, L_artikel).join(L_ophhis,(L_ophhis.op_typ == ("STT").lower()) & (L_ophhis.lscheinnr == L_ophis.lscheinnr) & (L_ophhis.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophis.fibukonto)).join(Gl_department,(Gl_department.nr == Gl_acct.deptnr)).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).filter((L_ophis.lager_nr == l_lager.lager_nr) & (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.artnr >= from_art) & (L_ophis.artnr <= to_art) & (L_ophis.anzahl != 0) & (L_ophis.op_art == 3)).order_by(L_ophis.lscheinnr, L_ophis.artnr).all():

                    # if l_ophis_obj_list.get(l_ophis._recid):
                    #     continue
                    # else:
                    #     l_ophis_obj_list[l_ophis._recid] = True

                    it_exist = True
                    other_fibu = False

                    if l_ophis.fibukonto != "":

                        if deptno != 0:
                            gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)],"deptnr": [(eq, deptno)]})
                        else:
                            gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)]})

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

                        parameters = get_cache (Parameters, {"progname": [(eq, "costcenter")],"section": [(eq, "alloc")],"varname": [(eq, to_string(deptno))],"vstring": [(eq, gl_acct.fibukonto)]})
                        create_it = None != parameters

                    if lschein == "":
                        lschein = l_ophis.lscheinnr

                    if (lschein != l_ophis.lscheinnr) and t_anz != 0:
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list.description = "Subtotal"
                        str_list.anzahl = to_string(t_anz, "->,>>>,>>9.999")

                        if not long_digit:
                            str_list.warenwert = to_string(t_val, "->,>>>,>>>,>>9.99")
                        else:
                            str_list.warenwert = to_string(t_val, "->>>,>>>,>>>,>>9")

                        t_anz =  to_decimal("0")
                        t_val =  to_decimal("0")

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        lschein = l_ophis.lscheinnr
                        curr_artnr = l_ophis.artnr

                    if do_it:
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        # str_list.s = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(24)")
                        # str_list.bezeich = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(36)")
                        str_list.s = to_string("", "x(8)") + format_fixed_length(l_lager.bezeich, 24)
                        str_list.bezeich = to_string("", "x(8)") + format_fixed_length(l_lager.bezeich, 36)
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        do_it = False

                    if create_it:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.fibu = fibukonto
                            s_list.bezeich = cost_bezeich

                            if cc_code != 0:
                                s_list.bezeich = to_string(cc_code, "9999") + " " + s_list.bezeich

                        s_list.cost = s_list.cost + l_ophis.warenwert
                        t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                        t_val =  to_decimal(t_val) + to_decimal(l_ophis.warenwert)
                        tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list.lscheinnr = l_ophis.lscheinnr
                        str_list.fibu = fibukonto
                        str_list.other_fibu = other_fibu
                        str_list.op_recid = l_ophis._recid
                        str_list.gldept = to_string(gl_department.nr) + " - " + gl_department.bezeich
                        str_list.masseinheit = l_artikel.masseinheit

                        queasy = get_cache (Queasy, {"key": [(eq, 340)],"char1": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)],"deci1": [(eq, l_ophis.einzelpreis)]})

                        if queasy:
                            str_list.remark_artikel = queasy.char2
                        else:
                            str_list.remark_artikel = ""

                        if not long_digit:

                            if l_ophis.einzelpreis > 9999999:
                                str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                                str_list.bezeich = to_string(s_list.bezeich)
                                str_list.artnr = to_string(l_artikel.artnr)
                                str_list.description = to_string(l_artikel.bezeich, "x(55)")
                                str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                                str_list.einzelpreis = to_string(l_ophis.einzelpreis, " >>>,>>>,>>9")
                                str_list.warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")
                                
                                # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")

                                if l_ophis.warenwert >= 0:
                                    tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">,>>>,>>>,>>9.99"), 17)
                                else:
                                    tmp_warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                if l_ophis.anzahl >= 0:
                                    tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                                else:
                                    tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                                str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + format_fixed_length(to_string(l_ophis.einzelpreis, ">>>,>>>,>>9"), 12) + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)
                            else:
                                str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                                str_list.bezeich = to_string(s_list.bezeich)
                                str_list.artnr = to_string(l_artikel.artnr)
                                str_list.description = to_string(l_artikel.bezeich, "x(55)")
                                str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                                str_list.einzelpreis = to_string(l_ophis.einzelpreis, ">,>>>,>>9.99")
                                str_list.warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")

                                if l_ophis.warenwert >= 0:
                                    tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">,>>>,>>>,>>9.99"), 17)
                                else:
                                    tmp_warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                if l_ophis.anzahl >= 0:
                                    tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                                else:
                                    tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                                str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)
                        else:
                            str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                            str_list.bezeich = to_string(s_list.bezeich)
                            str_list.artnr = to_string(l_artikel.artnr)
                            str_list.description = to_string(l_artikel.bezeich, "x(55)")
                            str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                            str_list.einzelpreis = to_string(l_ophis.einzelpreis, " >>>,>>>,>>9")
                            str_list.warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                            # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9") + to_string(l_ophis.lscheinnr, "x(12)")

                            if l_ophis.warenwert >= 0:
                                tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">>>,>>>,>>>,>>9"), 16)
                            else:
                                tmp_warenwert = to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9")

                            if l_ophis.anzahl >= 0:
                                tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                            else:
                                tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                            str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + format_fixed_length(to_string(l_ophis.einzelpreis, ">>>,>>>,>>9"), 12) + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)

        if t_anz != 0:
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.description = "Subtotal "
            str_list.anzahl = to_string(t_anz, "->,>>>,>>9.999")

            if not long_digit:
                str_list.warenwert = trim(to_string(t_val, "->,>>>,>>>,>>9.99"))
            else:
                str_list.warenwert = trim(to_string(t_val, "->>>,>>>,>>>,>>9"))

            str_list = Str_list()
            str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.description = "T O T A L"
        str_list.anzahl = to_string(tot_anz, "->,>>>,>>9.999")

        if not long_digit:
            str_list.warenwert = trim(to_string(tot_amount, "->,>>>,>>>,>>9.99"))
        else:
            str_list.warenwert = trim(to_string(tot_amount, "->>>>,>>>,>>>,>>9"))

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        # str_list.bezeich = to_string("", "x(8)") + to_string(translateExtended ("SUMMARY OF EXPENSES", lvcarea, "") , "x(30)")
        str_list.bezeich = to_string("", "x(8)") + format_fixed_length(translateExtended ("SUMMARY OF EXPENSES", lvcarea, ""), 30)
        str_list.mark = "Summary"

        tot_amount =  to_decimal("0")

        for s_list in query(s_list_data, sort_by=[("bezeich",False)]):
            str_list = Str_list()
            str_list_data.append(str_list)

            if not long_digit:
                # str_list.description = to_string(s_list.bezeich, "x(32)")
                str_list.description = format_fixed_length(s_list.bezeich, 32)
                str_list.warenwert = trim(to_string(s_list.cost, "->,>>>,>>>,>>9.99"))
            else:
                # str_list.description = to_string(s_list.bezeich, "x(32)")
                str_list.description = format_fixed_length(s_list.bezeich, 32)
                str_list.warenwert = trim(to_string(s_list.cost, "->>>>,>>>,>>>,>>9"))

            tot_amount =  to_decimal(tot_amount) + to_decimal(s_list.cost)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.description = "T O T A L"

        if not long_digit:
            str_list.warenwert = trim(to_string(tot_amount, "->,>>>,>>>,>>9.99"))
        else:
            str_list.warenwert = trim(to_string(tot_amount, "->>>>,>>>,>>>,>>9"))


    def create_listc():

        nonlocal it_exist, str_list_data, tot_anz, tot_amount, i, lvcarea, gl_acct, l_lager, l_ophhis, gl_department, l_artikel, l_ophis, parameters, queasy, l_untergrup
        nonlocal pvilanguage, trans_code, from_grp, mi_alloc_chk, mi_article_chk, mi_docu_chk, mi_date_chk, from_lager, to_lager, from_date, to_date, from_art, to_art, deptno, long_digit, cost_acct, mattype, mi_sub_group


        nonlocal s_list, str_list
        nonlocal s_list_data, str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        curr_artnr:int = 0
        lschein:string = ""
        datum:date = None
        cost_bezeich:string = ""
        fibukonto:string = ""
        do_it:bool = False
        cc_code:int = 0
        other_fibu:bool = False
        gl_acct1 = None
        create_it:bool = False
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        it_exist = False
        str_list_data.clear()
        s_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        do_it = True

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():

            do_it = True
            curr_artnr = 0

            is_connected_to_vhparch = check_connection_arch()

            if is_connected_to_vhparch:
                it_exist, t_anz, t_val, tot_anz, tot_amount = get_output(stockhoutli_arch('listC', l_lager.lager_nr, from_date, to_date, from_art, to_art, deptno, long_digit, do_it, l_lager.bezeich, from_grp, "", ""))
            else:
                l_ophis_obj_list = {}
                for l_ophis, l_ophhis, gl_acct, gl_department, l_artikel in db_session.query(L_ophis, L_ophhis, Gl_acct, Gl_department, L_artikel).join(L_ophhis,(L_ophhis.op_typ == ("STT").lower()) & (L_ophhis.lscheinnr == L_ophis.lscheinnr) & (L_ophhis.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophis.fibukonto)).join(Gl_department,(Gl_department.nr == Gl_acct.deptnr)).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).filter((L_ophis.lager_nr == l_lager.lager_nr) & (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.artnr >= from_art) & (L_ophis.artnr <= to_art) & (L_ophis.anzahl != 0) & (L_ophis.op_art == 3)).order_by(L_ophis.datum, L_ophis.artnr).all():

                    # if l_ophis_obj_list.get(l_ophis._recid):
                    #     continue
                    # else:
                    #     l_ophis_obj_list[l_ophis._recid] = True

                    it_exist = True
                    other_fibu = False

                    if l_ophis.fibukonto != "":

                        if deptno != 0:
                            gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)],"deptnr": [(eq, deptno)]})
                        else:
                            gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)]})

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

                        parameters = get_cache (Parameters, {"progname": [(eq, "costcenter")],"section": [(eq, "alloc")],"varname": [(eq, to_string(deptno))],"vstring": [(eq, gl_acct.fibukonto)]})
                        create_it = None != parameters

                    if datum == None:
                        datum = l_ophis.datum

                    if (datum != l_ophis.datum) and t_anz != 0:
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list.description = "Subtotal"
                        str_list.anzahl = to_string(t_anz, "->,>>>,>>9.999")

                        if not long_digit:
                            str_list.warenwert = to_string(t_val, "->,>>>,>>>,>>9.99")
                        else:
                            str_list.warenwert = to_string(t_val, "->>>,>>>,>>>,>>9")

                        t_anz =  to_decimal("0")
                        t_val =  to_decimal("0")

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        lschein = l_ophis.lscheinnr
                        datum = l_ophis.datum
                        curr_artnr = l_ophis.artnr

                    if do_it:
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        # str_list.s = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(24)")
                        # str_list.bezeich = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(36)")
                        str_list.s = to_string("", "x(8)") + format_fixed_length(l_lager.bezeich, 24)
                        str_list.bezeich = to_string("", "x(8)") + format_fixed_length(l_lager.bezeich, 36)
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        do_it = False

                    if create_it:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.fibu = fibukonto
                            s_list.bezeich = cost_bezeich

                            if cc_code != 0:
                                s_list.bezeich = to_string(cc_code, "9999") + " " + s_list.bezeich

                        s_list.cost = s_list.cost + l_ophis.warenwert
                        t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                        t_val =  to_decimal(t_val) + to_decimal(l_ophis.warenwert)
                        tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list.lscheinnr = l_ophis.lscheinnr
                        str_list.fibu = fibukonto
                        str_list.other_fibu = other_fibu
                        str_list.op_recid = l_ophis._recid
                        str_list.gldept = to_string(gl_department.nr) + " - " + gl_department.bezeich
                        str_list.masseinheit = l_artikel.masseinheit

                        queasy = get_cache (Queasy, {"key": [(eq, 340)],"char1": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)],"deci1": [(eq, l_ophis.einzelpreis)]})

                        if queasy:
                            str_list.remark_artikel = queasy.char2
                        else:
                            str_list.remark_artikel = ""

                        if not long_digit:

                            if l_ophis.einzelpreis > 9999999:
                                str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                                str_list.bezeich = to_string(s_list.bezeich)
                                str_list.artnr = to_string(l_artikel.artnr)
                                str_list.description = to_string(l_artikel.bezeich, "x(55)")
                                str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                                str_list.einzelpreis = to_string(l_ophis.einzelpreis, " >>>,>>>,>>9")
                                str_list.warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")

                                if l_ophis.warenwert >= 0:
                                    tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">,>>>,>>>,>>9.99"), 17)
                                else:
                                    tmp_warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                if l_ophis.anzahl >= 0:
                                    tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                                else:
                                    tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                                str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + format_fixed_length(to_string(l_ophis.einzelpreis, ">>>,>>>,>>9"), 12) + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)
                            else:
                                str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                                str_list.bezeich = to_string(s_list.bezeich)
                                str_list.artnr = to_string(l_artikel.artnr)
                                str_list.description = to_string(l_artikel.bezeich, "x(55)")
                                str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                                str_list.einzelpreis = to_string(l_ophis.einzelpreis, "->,>>>,>>9.999")
                                str_list.warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")

                                if l_ophis.warenwert >= 0:
                                    tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">,>>>,>>>,>>9.99"), 17)
                                else:
                                    tmp_warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                if l_ophis.anzahl >= 0:
                                    tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                                else:
                                    tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                                str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)
                        else:
                            str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                            str_list.bezeich = to_string(s_list.bezeich)
                            str_list.artnr = to_string(l_artikel.artnr)
                            str_list.description = to_string(l_artikel.bezeich, "x(55)")
                            str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                            str_list.einzelpreis = to_string(l_ophis.einzelpreis, " >>>,>>>,>>9")
                            str_list.warenwert = to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9")

                            # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9") + to_string(l_ophis.lscheinnr, "x(12)")

                            if l_ophis.warenwert >= 0:
                                tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">>>,>>>,>>>,>>9"), 16)
                            else:
                                tmp_warenwert = to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9")

                            if l_ophis.anzahl >= 0:
                                tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                            else:
                                tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                            str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + format_fixed_length(to_string(l_ophis.einzelpreis, ">>>,>>>,>>9"), 12) + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)

        if t_anz != 0:
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.description = "Subtotal "
            str_list.anzahl = to_string(t_anz, "->,>>>,>>9.999")

            if not long_digit:
                str_list.warenwert = trim(to_string(t_val, "->,>>>,>>>,>>9.99"))
            else:
                str_list.warenwert = trim(to_string(t_val, "->>>,>>>,>>>,>>9"))

            str_list = Str_list()
            str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.description = "T O T A L"
        str_list.anzahl = to_string(tot_anz, "->,>>>,>>9.999")

        if not long_digit:
            str_list.warenwert = trim(to_string(tot_amount, "->,>>>,>>>,>>9.99"))
        else:
            str_list.warenwert = trim(to_string(tot_amount, "->>>>,>>>,>>>,>>9"))

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        # str_list.s = to_string("", "x(8)") + to_string(translateExtended ("SUMMARY OF EXPENSES", lvcarea, "") , "x(30)")
        str_list.s = to_string("", "x(8)") + format_fixed_length(translateExtended ("SUMMARY OF EXPENSES", lvcarea, ""), 30)
        str_list.mark = "Summary"

        tot_amount =  to_decimal("0")

        for s_list in query(s_list_data, sort_by=[("bezeich",False)]):
            str_list = Str_list()
            str_list_data.append(str_list)

            if not long_digit:
                # str_list.description = to_string(s_list.bezeich, "x(32)")
                str_list.description = format_fixed_length(s_list.bezeich, 32)
                str_list.warenwert = trim(to_string(s_list.cost, "->,>>>,>>>,>>9.99"))
            else:
                # str_list.description = to_string(s_list.bezeich, "x(32)")
                str_list.description = format_fixed_length(s_list.bezeich, 32)
                str_list.warenwert = trim(to_string(s_list.cost, "->>>>,>>>,>>>,>>9"))

            tot_amount =  to_decimal(tot_amount) + to_decimal(s_list.cost)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.description = "T O T A L"

        if not long_digit:
            str_list.warenwert = trim(to_string(tot_amount, "->,>>>,>>>,>>9.99"))
        else:
            str_list.warenwert = trim(to_string(tot_amount, "->>>>,>>>,>>>,>>9"))


    def create_list():

        nonlocal it_exist, str_list_data, tot_anz, tot_amount, i, lvcarea, gl_acct, l_lager, l_ophhis, gl_department, l_artikel, l_ophis, parameters, queasy, l_untergrup
        nonlocal pvilanguage, trans_code, from_grp, mi_alloc_chk, mi_article_chk, mi_docu_chk, mi_date_chk, from_lager, to_lager, from_date, to_date, from_art, to_art, deptno, long_digit, cost_acct, mattype, mi_sub_group


        nonlocal s_list, str_list
        nonlocal s_list_data, str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        lschein:string = ""
        cost_bezeich:string = ""
        fibukonto:string = ""
        do_it:bool = False
        cc_code:int = 0
        other_fibu:bool = False
        gl_acct1 = None
        create_it:bool = False
        curr_fibu:string = ""
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        it_exist = False
        str_list_data.clear()
        s_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():

            do_it = True

            is_connected_to_vhparch = check_connection_arch()

            if is_connected_to_vhparch:
                it_exist, t_anz, t_val, tot_anz, tot_amount = get_output(stockhoutli_arch('list', l_lager.lager_nr, from_date, to_date, from_art, to_art, deptno, long_digit, do_it, l_lager.bezeich, from_grp, "", ""))
            else:
                l_ophis_obj_list = {}
                for l_ophis, l_ophhis, gl_acct, gl_department, l_artikel in db_session.query(L_ophis, L_ophhis, Gl_acct, Gl_department, L_artikel).join(L_ophhis,(L_ophhis.op_typ == ("STT").lower()) & (L_ophhis.lscheinnr == L_ophis.lscheinnr) & (L_ophhis.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophis.fibukonto)).join(Gl_department,(Gl_department.nr == Gl_acct.deptnr)).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).filter((L_ophis.lager_nr == l_lager.lager_nr) & (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.artnr >= from_art) & (L_ophis.artnr <= to_art) & (L_ophis.anzahl != 0) & (L_ophis.op_art == 3)).order_by(L_ophis.fibukonto, L_ophis.datum, L_ophis.artnr).all():

                    # if l_ophis_obj_list.get(l_ophis._recid):
                    #     continue
                    # else:
                    #     l_ophis_obj_list[l_ophis._recid] = True

                    it_exist = True
                    other_fibu = False

                    if l_ophis.fibukonto != "":

                        if deptno != 0:
                            gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)],"deptnr": [(eq, deptno)]})
                        else:
                            gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)]})

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

                        parameters = get_cache (Parameters, {"progname": [(eq, "costcenter")],"section": [(eq, "alloc")],"varname": [(eq, to_string(deptno))],"vstring": [(eq, fibukonto)]})
                        create_it = None != parameters

                    if curr_fibu == "":
                        curr_fibu = fibukonto

                    if curr_fibu.lower()  != (fibukonto).lower()  and t_anz != 0:
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list.description = "Subtotal"
                        str_list.anzahl = to_string(t_anz, "->,>>>,>>9.999")

                        if not long_digit:
                            str_list.warenwert = to_string(t_val, "->,>>>,>>>,>>9.99")
                        else:
                            str_list.warenwert = to_string(t_val, "->>>,>>>,>>>,>>9")

                        t_anz =  to_decimal("0")
                        t_val =  to_decimal("0")
                        
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        lschein = l_ophis.lscheinnr
                        curr_fibu = fibukonto

                    if do_it:
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        # str_list.s = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(24)")
                        # str_list.bezeich = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(36)")
                        str_list.s = to_string("", "x(8)") + format_fixed_length(l_lager.bezeich, 24)
                        str_list.bezeich = to_string("", "x(8)") + format_fixed_length(l_lager.bezeich, 36)
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        do_it = False

                    if create_it:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.fibu = fibukonto
                            s_list.bezeich = cost_bezeich

                            if cc_code != 0:
                                s_list.bezeich = to_string(cc_code, "9999") + " " + s_list.bezeich

                        s_list.cost = s_list.cost + l_ophis.warenwert
                        t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                        t_val =  to_decimal(t_val) + to_decimal(l_ophis.warenwert)
                        tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list.lscheinnr = l_ophis.lscheinnr
                        str_list.fibu = fibukonto
                        str_list.other_fibu = other_fibu
                        str_list.op_recid = l_ophis._recid
                        str_list.gldept = to_string(gl_department.nr) + " - " + gl_department.bezeich
                        str_list.masseinheit = l_artikel.masseinheit

                        queasy = get_cache (Queasy, {"key": [(eq, 340)],"char1": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)],"deci1": [(eq, l_ophis.einzelpreis)]})

                        if queasy:
                            str_list.remark_artikel = queasy.char2
                        else:
                            str_list.remark_artikel = ""

                        if not long_digit:

                            if l_ophis.einzelpreis > 9999999:
                                str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                                str_list.bezeich = to_string(s_list.bezeich)
                                str_list.artnr = to_string(l_artikel.artnr)
                                str_list.description = to_string(l_artikel.bezeich, "x(55)")
                                str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                                str_list.einzelpreis = to_string(l_ophis.einzelpreis, " >>>,>>>,>>9")
                                str_list.warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")

                                if l_ophis.warenwert >= 0:
                                    tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">,>>>,>>>,>>9.99"), 17)
                                else:
                                    tmp_warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                if l_ophis.anzahl >= 0:
                                    tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                                else:
                                    tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                                str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + format_fixed_length(to_string(l_ophis.einzelpreis, ">>>,>>>,>>9"), 12) + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)
                            else:
                                str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                                str_list.bezeich = to_string(s_list.bezeich)
                                str_list.artnr = to_string(l_artikel.artnr)
                                str_list.description = to_string(l_artikel.bezeich, "x(55)")
                                str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                                str_list.einzelpreis = to_string(l_ophis.einzelpreis, ">,>>>,>>9.99")
                                str_list.warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")

                                if l_ophis.warenwert >= 0:
                                    tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">,>>>,>>>,>>9.99"), 17)
                                else:
                                    tmp_warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                if l_ophis.anzahl >= 0:
                                    tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                                else:
                                    tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                                str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)
                        else:
                            str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                            str_list.bezeich = to_string(s_list.bezeich)
                            str_list.artnr = to_string(l_artikel.artnr)
                            str_list.description = to_string(l_artikel.bezeich, "x(55)")
                            str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                            str_list.einzelpreis = to_string(l_ophis.einzelpreis, " >>>,>>>,>>9")
                            str_list.warenwert = to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9")

                            # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9") + to_string(l_ophis.lscheinnr, "x(12)")

                            if l_ophis.warenwert >= 0:
                                tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">>>,>>>,>>>,>>9"), 16)
                            else:
                                tmp_warenwert = to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9")

                            if l_ophis.anzahl >= 0:
                                tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                            else:
                                tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                            str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + format_fixed_length(to_string(l_ophis.einzelpreis, ">>>,>>>,>>9"), 12) + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)

        if t_anz != 0:
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.description = "Subtotal "
            str_list.anzahl = to_string(t_anz, "->,>>>,>>9.999")

            if not long_digit:
                str_list.warenwert = trim(to_string(t_val, "->,>>>,>>>,>>9.99"))
            else:
                str_list.warenwert = trim(to_string(t_val, "->>>,>>>,>>>,>>9"))

            str_list = Str_list()
            str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.description = "T O T A L"
        str_list.anzahl = to_string(tot_anz, "->,>>>,>>9.999")

        if not long_digit:
            str_list.warenwert = trim(to_string(tot_amount, "->,>>>,>>>,>>9.99"))
        else:
            str_list.warenwert = trim(to_string(tot_amount, "->>>>,>>>,>>>,>>9"))

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        tot_amount =  to_decimal("0")

        for s_list in query(s_list_data, sort_by=[("bezeich",False)]):
            str_list = Str_list()
            str_list_data.append(str_list)


            if not long_digit:
                # str_list.description = to_string(s_list.bezeich, "x(32)")
                str_list.description = format_fixed_length(s_list.bezeich, 32)
                str_list.warenwert = trim(to_string(s_list.cost, "->,>>>,>>>,>>9.99"))
            else:
                # str_list.description = to_string(s_list.bezeich, "x(32)")
                str_list.description = format_fixed_length(s_list.bezeich, 32)
                str_list.warenwert = trim(to_string(s_list.cost, "->>>>,>>>,>>>,>>9"))

            tot_amount =  to_decimal(tot_amount) + to_decimal(s_list.cost)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.description = "T O T A L"

        if not long_digit:
            str_list.warenwert = trim(to_string(tot_amount, "->,>>>,>>>,>>9.99"))
        else:
            str_list.warenwert = trim(to_string(tot_amount, "->>>>,>>>,>>>,>>9"))


    def create_list1():

        nonlocal it_exist, str_list_data, tot_anz, tot_amount, i, lvcarea, gl_acct, l_lager, l_ophhis, gl_department, l_artikel, l_ophis, parameters, queasy, l_untergrup
        nonlocal pvilanguage, trans_code, from_grp, mi_alloc_chk, mi_article_chk, mi_docu_chk, mi_date_chk, from_lager, to_lager, from_date, to_date, from_art, to_art, deptno, long_digit, cost_acct, mattype, mi_sub_group


        nonlocal s_list, str_list
        nonlocal s_list_data, str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        lschein:string = ""
        cost_bezeich:string = ""
        fibukonto:string = ""
        do_it:bool = False
        create_it:bool = False
        cc_code:int = 0
        other_fibu:bool = False
        grp1:int = 0
        grp2:int = 1
        curr_fibu:string = ""
        gl_acct1 = None
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        it_exist = False
        str_list_data.clear()
        s_list_data.clear()

        if mattype == 1:
            grp2 = 0

        elif mattype == 2:
            grp1 = 1
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():
            do_it = True

            is_connected_to_vhparch = check_connection_arch()

            if is_connected_to_vhparch:
                it_exist, t_anz, t_val, tot_anz, tot_amount = get_output(stockhoutli_arch('list1', l_lager.lager_nr, from_date, to_date, from_art, to_art, deptno, long_digit, do_it, l_lager.bezeich, from_grp, grp1, grp2))
            else:
                l_ophis_obj_list = {}
                for l_ophis, l_ophhis, gl_acct, gl_department, l_artikel, l_untergrup in db_session.query(L_ophis, L_ophhis, Gl_acct, Gl_department, L_artikel, L_untergrup).join(L_ophhis,(L_ophhis.op_typ == ("STT").lower()) & (L_ophhis.lscheinnr == L_ophis.lscheinnr) & (L_ophhis.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophis.fibukonto)).join(Gl_department,(Gl_department.nr == Gl_acct.deptnr)).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter((L_ophis.lager_nr == l_lager.lager_nr) & (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.artnr >= from_art) & (L_ophis.artnr <= to_art) & (L_ophis.anzahl != 0) & (L_ophis.op_art == 3)).order_by(L_ophis.fibukonto, L_ophhis.fibukonto, L_ophis.datum, L_ophis.artnr).all():

                    # if l_ophis_obj_list.get(l_ophis._recid):
                    #     continue
                    # else:
                    #     l_ophis_obj_list[l_ophis._recid] = True

                    it_exist = True
                    other_fibu = False

                    if l_ophis.fibukonto != "":

                        if deptno != 0:
                            gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)],"deptnr": [(eq, deptno)]})
                        else:
                            gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)]})

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

                        parameters = get_cache (Parameters, {"progname": [(eq, "costcenter")],"section": [(eq, "alloc")],"varname": [(eq, to_string(deptno))],"vstring": [(eq, gl_acct.fibukonto)]})
                        create_it = None != parameters

                    if curr_fibu == "":
                        curr_fibu = fibukonto

                    if curr_fibu.lower()  != (fibukonto).lower()  and t_anz != 0 and create_it:
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list.description = "Subtotal"
                        str_list.anzahl = to_string(t_anz, "->,>>>,>>9.999")

                        if not long_digit:
                            str_list.warenwert = to_string(t_val, "->,>>>,>>>,>>9.99")
                        else:
                            str_list.warenwert = to_string(t_val, "->>>,>>>,>>>,>>9")

                        t_anz =  to_decimal("0")
                        t_val =  to_decimal("0")

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        lschein = l_ophis.lscheinnr
                        curr_fibu = fibukonto

                    if do_it:
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        # str_list.s = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(30)")
                        # str_list.bezeich = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(36)")
                        str_list.s = to_string("", "x(8)") + format_fixed_length(l_lager.bezeich, 24)
                        str_list.bezeich = to_string("", "x(8)") + format_fixed_length(l_lager.bezeich, 36)
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        do_it = False

                    if create_it:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.fibu = fibukonto
                            s_list.bezeich = cost_bezeich

                            if cc_code != 0:
                                s_list.bezeich = to_string(cc_code, "9999") + " " + s_list.bezeich

                        s_list.cost = s_list.cost + l_ophis.warenwert
                        t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                        t_val =  to_decimal(t_val) + to_decimal(l_ophis.warenwert)
                        tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list.lscheinnr = l_ophis.lscheinnr
                        str_list.other_fibu = other_fibu
                        str_list.fibu = fibukonto
                        str_list.op_recid = l_ophis._recid
                        str_list.gldept = to_string(gl_department.nr) + " - " + gl_department.bezeich
                        str_list.masseinheit = l_artikel.masseinheit

                        queasy = get_cache (Queasy, {"key": [(eq, 340)],"char1": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)],"deci1": [(eq, l_ophis.einzelpreis)]})

                        if queasy:
                            str_list.remark_artikel = queasy.char2
                        else:
                            str_list.remark_artikel = ""

                        if not long_digit:

                            if l_ophis.einzelpreis > 9999999:
                                str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                                str_list.bezeich = to_string(s_list.bezeich)
                                str_list.artnr = to_string(l_artikel.artnr)
                                str_list.description = to_string(l_artikel.bezeich, "x(55)")
                                str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                                str_list.einzelpreis = to_string(l_ophis.einzelpreis, " >>>,>>>,>>9")
                                str_list.warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")

                                if l_ophis.warenwert >= 0:
                                    tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">,>>>,>>>,>>9.99"), 17)
                                else:
                                    tmp_warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                if l_ophis.anzahl >= 0:
                                    tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                                else:
                                    tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                                str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + format_fixed_length(to_string(l_ophis.einzelpreis, ">>>,>>>,>>9"), 12) + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)
                                
                            else:
                                str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                                str_list.bezeich = to_string(s_list.bezeich)
                                str_list.artnr = to_string(l_artikel.artnr)
                                str_list.description = to_string(l_artikel.bezeich, "x(55)")
                                str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                                str_list.einzelpreis = to_string(l_ophis.einzelpreis, ">,>>>,>>9.99")
                                str_list.warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")
                                
                                # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")

                                if l_ophis.warenwert >= 0:
                                    tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">,>>>,>>>,>>9.99"), 17)
                                else:
                                    tmp_warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                if l_ophis.anzahl >= 0:
                                    tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                                else:
                                    tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                                str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)
                        else:
                            str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                            str_list.bezeich = to_string(s_list.bezeich)
                            str_list.artnr = to_string(l_artikel.artnr)
                            str_list.description = to_string(l_artikel.bezeich, "x(55)")
                            str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                            str_list.einzelpreis = to_string(l_ophis.einzelpreis, " >>>,>>>,>>9")
                            str_list.warenwert = to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9")

                            # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9") + to_string(l_ophis.lscheinnr, "x(12)")

                            if l_ophis.warenwert >= 0:
                                tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">>>,>>>,>>>,>>9"), 16)
                            else:
                                tmp_warenwert = to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9")

                            if l_ophis.anzahl >= 0:
                                tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                            else:
                                tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                            str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + format_fixed_length(to_string(l_ophis.einzelpreis, ">>>,>>>,>>9"), 12) + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)

        if t_anz != 0:
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.description = "Subtotal "
            str_list.anzahl = to_string(t_anz, "->,>>>,>>9.999")

            if not long_digit:
                str_list.warenwert = trim(to_string(t_val, "->,>>>,>>>,>>9.99"))
            else:
                str_list.warenwert = trim(to_string(t_val, "->>>,>>>,>>>,>>9"))

            str_list = Str_list()
            str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.description = "T O T A L"
        str_list.anzahl = to_string(tot_anz, "->,>>>,>>9.999")

        if not long_digit:
            str_list.warenwert = trim(to_string(tot_amount, "->,>>>,>>>,>>9.99"))
        else:
            str_list.warenwert = trim(to_string(tot_amount, "->>>>,>>>,>>>,>>9"))

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        # str_list.s = to_string("", "x(8)") + to_string(translateExtended ("SUMMARY OF EXPENSES", lvcarea, "") , "x(30)")
        str_list.s = to_string("", "x(8)") + format_fixed_length(translateExtended ("SUMMARY OF EXPENSES", lvcarea, ""), 30)
        str_list.mark = "Summary"

        tot_amount =  to_decimal("0")

        for s_list in query(s_list_data, sort_by=[("bezeich",False)]):
            str_list = Str_list()
            str_list_data.append(str_list)

            if not long_digit:
                # str_list.description = to_string(s_list.bezeich, "x(32)")
                str_list.description = format_fixed_length(s_list.bezeich, 32)
                str_list.warenwert = trim(to_string(s_list.cost, "->,>>>,>>>,>>9.99"))
            else:
                # str_list.description = to_string(s_list.bezeich, "x(32)")
                str_list.description = format_fixed_length(s_list.bezeich, 32)
                str_list.warenwert = trim(to_string(s_list.cost, "->>>>,>>>,>>>,>>9"))

            tot_amount =  to_decimal(tot_amount) + to_decimal(s_list.cost)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.description = "T O T A L"

        if not long_digit:
            str_list.warenwert = trim(to_string(tot_amount, "->,>>>,>>>,>>9.99"))
        else:
            str_list.warenwert = trim(to_string(tot_amount, "->>>>,>>>,>>>,>>9"))

    def create_list1a():

        nonlocal it_exist, str_list_data, tot_anz, tot_amount, i, lvcarea, gl_acct, l_lager, l_ophhis, gl_department, l_artikel, l_ophis, parameters, queasy, l_untergrup
        nonlocal pvilanguage, trans_code, from_grp, mi_alloc_chk, mi_article_chk, mi_docu_chk, mi_date_chk, from_lager, to_lager, from_date, to_date, from_art, to_art, deptno, long_digit, cost_acct, mattype, mi_sub_group


        nonlocal s_list, str_list
        nonlocal s_list_data, str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        curr_artnr:int = 0
        lschein:string = ""
        cost_bezeich:string = ""
        fibukonto:string = ""
        do_it:bool = False
        create_it:bool = False
        cc_code:int = 0
        other_fibu:bool = False
        grp1:int = 0
        grp2:int = 1
        gl_acct1 = None
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        it_exist = False
        str_list_data.clear()
        s_list_data.clear()

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

            is_connected_to_vhparch = check_connection_arch()

            if is_connected_to_vhparch:
                it_exist, t_anz, t_val, tot_anz, tot_amount = get_output(stockhoutli_arch('list1A', l_lager.lager_nr, from_date, to_date, from_art, to_art, deptno, long_digit, do_it, l_lager.bezeich, from_grp, grp1, grp2))
            else:
                l_ophis_obj_list = {}
                for l_ophis, l_artikel, l_ophhis, gl_acct, gl_department, l_untergrup in db_session.query(L_ophis, L_artikel, L_ophhis, Gl_acct, Gl_department, L_untergrup).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum == from_grp)).join(L_ophhis,(L_ophhis.op_typ == ("STT").lower()) & (L_ophhis.lscheinnr == L_ophis.lscheinnr) & (L_ophhis.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophis.fibukonto)).join(Gl_department,(Gl_department.nr == Gl_acct.deptnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter((L_ophis.lager_nr == l_lager.lager_nr) & (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.artnr >= from_art) & (L_ophis.artnr <= to_art) & (L_ophis.anzahl != 0) & (L_ophis.op_art == 3)).order_by(L_ophis.datum, L_ophis.lscheinnr, L_ophis.artnr).all():

                    # if l_ophis_obj_list.get(l_ophis._recid):
                    #     continue
                    # else:
                    #     l_ophis_obj_list[l_ophis._recid] = True

                    it_exist = True
                    other_fibu = False

                    if l_ophis.fibukonto != "":

                        if deptno != 0:
                            gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)],"deptnr": [(eq, deptno)]})
                        else:
                            gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)]})

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

                        parameters = get_cache (Parameters, {"progname": [(eq, "costcenter")],"section": [(eq, "alloc")],"varname": [(eq, to_string(deptno))],"vstring": [(eq, gl_acct.fibukonto)]})
                        create_it = None != parameters

                    if curr_artnr == 0:
                        curr_artnr = l_ophis.artnr

                    if curr_artnr != l_ophis.artnr and t_anz != 0:
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list.description = "Subtotal"
                        str_list.anzahl = to_string(t_anz, "->,>>>,>>9.999")

                        if not long_digit:
                            str_list.warenwert = to_string(t_val, "->,>>>,>>>,>>9.99")
                        else:
                            str_list.warenwert = to_string(t_val, "->>>,>>>,>>>,>>9")

                        t_anz =  to_decimal("0")
                        t_val =  to_decimal("0")

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        lschein = l_ophis.lscheinnr
                        curr_artnr = l_ophis.artnr

                    if do_it:
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        # str_list.s = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(30)")
                        # str_list.bezeich = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(36)")
                        str_list.s = to_string("", "x(8)") + format_fixed_length(l_lager.bezeich, 24)
                        str_list.bezeich = to_string("", "x(8)") + format_fixed_length(l_lager.bezeich, 36)
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        do_it = False

                    if create_it:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.fibu = fibukonto
                            s_list.bezeich = cost_bezeich

                            if cc_code != 0:
                                s_list.bezeich = to_string(cc_code, "9999") + " " + s_list.bezeich

                        s_list.cost = s_list.cost + l_ophis.warenwert
                        t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                        t_val =  to_decimal(t_val) + to_decimal(l_ophis.warenwert)
                        tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list.lscheinnr = l_ophis.lscheinnr
                        str_list.other_fibu = other_fibu
                        str_list.fibu = fibukonto
                        str_list.op_recid = l_ophis._recid
                        str_list.gldept = to_string(gl_department.nr) + " - " + gl_department.bezeich
                        str_list.masseinheit = l_artikel.masseinheit

                        queasy = get_cache (Queasy, {"key": [(eq, 340)],"char1": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)],"deci1": [(eq, l_ophis.einzelpreis)]})

                        if queasy:
                            str_list.remark_artikel = queasy.char2
                        else:
                            str_list.remark_artikel = ""

                        if not long_digit:

                            if l_ophis.einzelpreis > 9999999:
                                str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                                str_list.bezeich = to_string(s_list.bezeich)
                                str_list.artnr = to_string(l_artikel.artnr)
                                str_list.description = to_string(l_artikel.bezeich, "x(55)")
                                str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                                str_list.einzelpreis = to_string(l_ophis.einzelpreis, " >>>,>>>,>>9")
                                str_list.warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")
                                
                                # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")

                                if l_ophis.warenwert >= 0:
                                    tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">,>>>,>>>,>>9.99"), 17)
                                else:
                                    tmp_warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                if l_ophis.anzahl >= 0:
                                    tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                                else:
                                    tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                                str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + format_fixed_length(to_string(l_ophis.einzelpreis, ">>>,>>>,>>9"), 12) + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)
                            else:
                                str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                                str_list.bezeich = to_string(s_list.bezeich)
                                str_list.artnr = to_string(l_artikel.artnr)
                                str_list.description = to_string(l_artikel.bezeich, "x(55)")
                                str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                                str_list.einzelpreis = to_string(l_ophis.einzelpreis, ">,>>>,>>9.99")
                                str_list.warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")
                                
                                # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")

                                if l_ophis.warenwert >= 0:
                                    tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">,>>>,>>>,>>9.99"), 17)
                                else:
                                    tmp_warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                if l_ophis.anzahl >= 0:
                                    tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                                else:
                                    tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                                str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)
                        else:
                            str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                            str_list.bezeich = to_string(s_list.bezeich)
                            str_list.artnr = to_string(l_artikel.artnr)
                            str_list.description = to_string(l_artikel.bezeich, "x(55)")
                            str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                            str_list.einzelpreis = to_string(l_ophis.einzelpreis, " >>>,>>>,>>9")
                            str_list.warenwert = to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9")

                            # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9") + to_string(l_ophis.lscheinnr, "x(12)")

                            if l_ophis.warenwert >= 0:
                                tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">>>,>>>,>>>,>>9"), 16)
                            else:
                                tmp_warenwert = to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9")

                            if l_ophis.anzahl >= 0:
                                tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                            else:
                                tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                            str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + format_fixed_length(to_string(l_ophis.einzelpreis, ">>>,>>>,>>9"), 12) + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)

        if t_anz != 0:
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.description = "Subtotal "
            str_list.anzahl = to_string(t_anz, "->,>>>,>>9.999")

            if not long_digit:
                str_list.warenwert = trim(to_string(t_val, "->,>>>,>>>,>>9.99"))
            else:
                str_list.warenwert = trim(to_string(t_val, "->>>,>>>,>>>,>>9"))

            str_list = Str_list()
            str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.description = "T O T A L"
        str_list.anzahl = to_string(tot_anz, "->,>>>,>>9.999")

        if not long_digit:
            str_list.warenwert = trim(to_string(tot_amount, "->,>>>,>>>,>>9.99"))
        else:
            str_list.warenwert = trim(to_string(tot_amount, "->>>>,>>>,>>>,>>9"))

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        # str_list.s = to_string("", "x(8)") + to_string(translateExtended ("SUMMARY OF EXPENSES", lvcarea, "") , "x(30)")
        str_list.s = to_string("", "x(8)") + format_fixed_length(translateExtended ("SUMMARY OF EXPENSES", lvcarea, ""), 30)
        str_list.mark = "Summary"

        tot_amount =  to_decimal("0")

        for s_list in query(s_list_data, sort_by=[("bezeich",False)]):
            str_list = Str_list()
            str_list_data.append(str_list)

            if not long_digit:
                # str_list.description = to_string(s_list.bezeich, "x(32)")
                str_list.description = format_fixed_length(s_list.bezeich, 32)
                str_list.warenwert = trim(to_string(s_list.cost, "->,>>>,>>>,>>9.99"))
            else:
                # str_list.description = to_string(s_list.bezeich, "x(32)")
                str_list.description = format_fixed_length(s_list.bezeich, 32)
                str_list.warenwert = trim(to_string(s_list.cost, "->>>>,>>>,>>>,>>9"))

            tot_amount =  to_decimal(tot_amount) + to_decimal(s_list.cost)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.description = "T O T A L"

        if not long_digit:
            str_list.warenwert = trim(to_string(tot_amount, "->,>>>,>>>,>>9.99"))
        else:
            str_list.warenwert = trim(to_string(tot_amount, "->>>>,>>>,>>>,>>9"))


    def create_list1b():

        nonlocal it_exist, str_list_data, tot_anz, tot_amount, i, lvcarea, gl_acct, l_lager, l_ophhis, gl_department, l_artikel, l_ophis, parameters, queasy, l_untergrup
        nonlocal pvilanguage, trans_code, from_grp, mi_alloc_chk, mi_article_chk, mi_docu_chk, mi_date_chk, from_lager, to_lager, from_date, to_date, from_art, to_art, deptno, long_digit, cost_acct, mattype, mi_sub_group


        nonlocal s_list, str_list
        nonlocal s_list_data, str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        curr_artnr:int = 0
        lschein:string = ""
        cost_bezeich:string = ""
        fibukonto:string = ""
        do_it:bool = False
        create_it:bool = False
        cc_code:int = 0
        other_fibu:bool = False
        grp1:int = 0
        grp2:int = 1
        gl_acct1 = None
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        it_exist = False
        str_list_data.clear()
        s_list_data.clear()

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

            is_connected_to_vhparch = check_connection_arch()

            if is_connected_to_vhparch:
                it_exist, t_anz, t_val, tot_anz, tot_amount = get_output(stockhoutli_arch('list1B', l_lager.lager_nr, from_date, to_date, from_art, to_art, deptno, long_digit, do_it, l_lager.bezeich, from_grp, grp1, grp2))
            else:
                l_ophis_obj_list = {}
                for l_ophis, l_artikel, l_ophhis, gl_acct, gl_department, l_untergrup in db_session.query(L_ophis, L_artikel, L_ophhis, Gl_acct, Gl_department, L_untergrup).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum == from_grp)).join(L_ophhis,(L_ophhis.op_typ == ("STT").lower()) & (L_ophhis.lscheinnr == L_ophis.lscheinnr) & (L_ophhis.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophis.fibukonto)).join(Gl_department,(Gl_department.nr == Gl_acct.deptnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter((L_ophis.lager_nr == l_lager.lager_nr) & (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.artnr >= from_art) & (L_ophis.artnr <= to_art) & (L_ophis.anzahl != 0) & (L_ophis.op_art == 3)).order_by(L_ophis.lscheinnr, L_ophis.artnr).all():

                    # if l_ophis_obj_list.get(l_ophis._recid):
                    #     continue
                    # else:
                    #     l_ophis_obj_list[l_ophis._recid] = True

                    it_exist = True
                    other_fibu = False

                    if l_ophis.fibukonto != "":

                        if deptno != 0:
                            gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)],"deptnr": [(eq, deptno)]})
                        else:
                            gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)]})

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

                        parameters = get_cache (Parameters, {"progname": [(eq, "costcenter")],"section": [(eq, "alloc")],"varname": [(eq, to_string(deptno))],"vstring": [(eq, gl_acct.fibukonto)]})
                        create_it = None != parameters

                    if lschein == "":
                        lschein = l_ophis.lscheinnr

                    if lschein != l_ophis.lscheinnr and t_anz != 0:
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list.description = "Subtotal"
                        str_list.anzahl = to_string(t_anz, "->,>>>,>>9.999")

                        if not long_digit:
                            str_list.warenwert = to_string(t_val, "->,>>>,>>>,>>9.99")
                        else:
                            str_list.warenwert = to_string(t_val, "->>>,>>>,>>>,>>9")

                        t_anz =  to_decimal("0")
                        t_val =  to_decimal("0")

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        lschein = l_ophis.lscheinnr
                        curr_artnr = l_ophis.artnr

                    if do_it:
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        # str_list.s = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(30)")
                        # str_list.bezeich = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(36)")
                        str_list.s = to_string("", "x(8)") + format_fixed_length(l_lager.bezeich, 24)
                        str_list.bezeich = to_string("", "x(8)") + format_fixed_length(l_lager.bezeich, 36)
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        do_it = False

                    if create_it:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.fibu = fibukonto
                            s_list.bezeich = cost_bezeich

                            if cc_code != 0:
                                s_list.bezeich = to_string(cc_code, "9999") + " " + s_list.bezeich

                        s_list.cost = s_list.cost + l_ophis.warenwert
                        t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                        t_val =  to_decimal(t_val) + to_decimal(l_ophis.warenwert)
                        tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list.lscheinnr = l_ophis.lscheinnr
                        str_list.other_fibu = other_fibu
                        str_list.fibu = fibukonto
                        str_list.op_recid = l_ophis._recid
                        str_list.gldept = to_string(gl_department.nr) + " - " + gl_department.bezeich
                        str_list.masseinheit = l_artikel.masseinheit

                        queasy = get_cache (Queasy, {"key": [(eq, 340)],"char1": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)],"deci1": [(eq, l_ophis.einzelpreis)]})

                        if queasy:
                            str_list.remark_artikel = queasy.char2
                        else:
                            str_list.remark_artikel = ""

                        if not long_digit:

                            if l_ophis.einzelpreis > 9999999:
                                str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                                str_list.bezeich = to_string(s_list.bezeich)
                                str_list.artnr = to_string(l_artikel.artnr)
                                str_list.description = to_string(l_artikel.bezeich, "x(55)")
                                str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                                str_list.einzelpreis = to_string(l_ophis.einzelpreis, " >>>,>>>,>>9")
                                str_list.warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")

                                if l_ophis.warenwert >= 0:
                                    tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">,>>>,>>>,>>9.99"), 17)
                                else:
                                    tmp_warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                if l_ophis.anzahl >= 0:
                                    tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                                else:
                                    tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                                str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + format_fixed_length(to_string(l_ophis.einzelpreis, ">>>,>>>,>>9"), 12) + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)

                            else:
                                str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                                str_list.bezeich = to_string(s_list.bezeich)
                                str_list.artnr = to_string(l_artikel.artnr)
                                str_list.description = to_string(l_artikel.bezeich, "x(55)")
                                str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                                str_list.einzelpreis = to_string(l_ophis.einzelpreis, " >,>>>,>>9.99")
                                str_list.warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")

                                if l_ophis.warenwert >= 0:
                                    tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">,>>>,>>>,>>9.99"), 17)
                                else:
                                    tmp_warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                if l_ophis.anzahl >= 0:
                                    tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                                else:
                                    tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                                str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)
                        else:
                            str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                            str_list.bezeich = to_string(s_list.bezeich)
                            str_list.artnr = to_string(l_artikel.artnr)
                            str_list.description = to_string(l_artikel.bezeich, "x(55)")
                            str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                            str_list.einzelpreis = to_string(l_ophis.einzelpreis, " >>>,>>>,>>9")
                            str_list.warenwert = to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9")

                            # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9") + to_string(l_ophis.lscheinnr, "x(12)")

                            if l_ophis.warenwert >= 0:
                                tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">>>,>>>,>>>,>>9"), 16)
                            else:
                                tmp_warenwert = to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9")

                            if l_ophis.anzahl >= 0:
                                tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                            else:
                                tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                            str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + format_fixed_length(to_string(l_ophis.einzelpreis, ">>>,>>>,>>9"), 12) + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)

        if t_anz != 0:
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.description = "Subtotal "
            str_list.anzahl = to_string(t_anz, "->,>>>,>>9.999")

            if not long_digit:
                str_list.warenwert = trim(to_string(t_val, "->,>>>,>>>,>>9.99"))
            else:
                str_list.warenwert = trim(to_string(t_val, "->>>,>>>,>>>,>>9"))

            str_list = Str_list()
            str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.description = "T O T A L"
        str_list.anzahl = to_string(tot_anz, "->,>>>,>>9.999")

        if not long_digit:
            str_list.warenwert = trim(to_string(tot_amount, "->,>>>,>>>,>>9.99"))
        else:
            str_list.warenwert = trim(to_string(tot_amount, "->>>>,>>>,>>>,>>9"))

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        # str_list.s = to_string("", "x(8)") + to_string(translateExtended ("SUMMARY OF EXPENSES", lvcarea, "") , "x(30)")
        str_list.s = to_string("", "x(8)") + format_fixed_length(translateExtended ("SUMMARY OF EXPENSES", lvcarea, ""), 30)
        str_list.mark = "Summary"

        tot_amount =  to_decimal("0")

        for s_list in query(s_list_data, sort_by=[("bezeich",False)]):
            str_list = Str_list()
            str_list_data.append(str_list)

            if not long_digit:
                # str_list.description = to_string(s_list.bezeich, "x(32)")
                str_list.description = format_fixed_length(s_list.bezeich, 32)
                str_list.warenwert = trim(to_string(s_list.cost, "->,>>>,>>>,>>9.99"))
            else:
                # str_list.description = to_string(s_list.bezeich, "x(32)")
                str_list.description = format_fixed_length(s_list.bezeich, 32)
                str_list.warenwert = trim(to_string(s_list.cost, "->>>>,>>>,>>>,>>9"))

            tot_amount =  to_decimal(tot_amount) + to_decimal(s_list.cost)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.description = "T O T A L"

        if not long_digit:
            str_list.warenwert = trim(to_string(tot_amount, "->,>>>,>>>,>>9.99"))
        else:
            str_list.warenwert = trim(to_string(tot_amount, "->>>>,>>>,>>>,>>9"))


    def create_list1c():

        nonlocal it_exist, str_list_data, tot_anz, tot_amount, i, lvcarea, gl_acct, l_lager, l_ophhis, gl_department, l_artikel, l_ophis, parameters, queasy, l_untergrup
        nonlocal pvilanguage, trans_code, from_grp, mi_alloc_chk, mi_article_chk, mi_docu_chk, mi_date_chk, from_lager, to_lager, from_date, to_date, from_art, to_art, deptno, long_digit, cost_acct, mattype, mi_sub_group


        nonlocal s_list, str_list
        nonlocal s_list_data, str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        curr_artnr:int = 0
        lschein:string = ""
        datum:date = None
        cost_bezeich:string = ""
        fibukonto:string = ""
        do_it:bool = False
        create_it:bool = False
        cc_code:int = 0
        other_fibu:bool = False
        grp1:int = 0
        grp2:int = 1
        gl_acct1 = None
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        it_exist = False
        str_list_data.clear()
        s_list_data.clear()

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

            is_connected_to_vhparch = check_connection_arch()

            if is_connected_to_vhparch:
                it_exist, t_anz, t_val, tot_anz, tot_amount = get_output(stockhoutli_arch('list1C', l_lager.lager_nr, from_date, to_date, from_art, to_art, deptno, long_digit, do_it, l_lager.bezeich, from_grp, grp1, grp2))
            else:
                l_ophis_obj_list = {}
                for l_ophis, l_artikel, l_ophhis, gl_acct, gl_department, l_untergrup in db_session.query(L_ophis, L_artikel, L_ophhis, Gl_acct, Gl_department, L_untergrup).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum == from_grp)).join(L_ophhis,(L_ophhis.op_typ == ("STT").lower()) & (L_ophhis.lscheinnr == L_ophis.lscheinnr) & (L_ophhis.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophis.fibukonto)).join(Gl_department,(Gl_department.nr == Gl_acct.deptnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter((L_ophis.lager_nr == l_lager.lager_nr) & (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.artnr >= from_art) & (L_ophis.artnr <= to_art) & (L_ophis.anzahl != 0) & (L_ophis.op_art == 3)).order_by(L_ophis.datum, L_ophis.artnr).all():

                    # if l_ophis_obj_list.get(l_ophis._recid):
                    #     continue
                    # else:
                    #     l_ophis_obj_list[l_ophis._recid] = True

                    it_exist = True
                    other_fibu = False

                    if l_ophis.fibukonto != "":

                        if deptno != 0:
                            gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)],"deptnr": [(eq, deptno)]})
                        else:
                            gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)]})

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

                        parameters = get_cache (Parameters, {"progname": [(eq, "costcenter")],"section": [(eq, "alloc")],"varname": [(eq, to_string(deptno))],"vstring": [(eq, gl_acct.fibukonto)]})
                        create_it = None != parameters

                    if datum == None:
                        datum = l_ophis.datum

                    if datum != l_ophis.datum and t_anz != 0:
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list.description = "Subtotal"
                        str_list.anzahl = to_string(t_anz, "->,>>>,>>9.999")

                        if not long_digit:
                            str_list.warenwert = to_string(t_val, "->,>>>,>>>,>>9.99")
                        else:
                            str_list.warenwert = to_string(t_val, "->>>,>>>,>>>,>>9")

                        t_anz =  to_decimal("0")
                        t_val =  to_decimal("0")

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        lschein = l_ophis.lscheinnr
                        datum = l_ophis.datum
                        curr_artnr = l_ophis.artnr

                    if do_it:
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        # str_list.s = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(30)")
                        # str_list.bezeich = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(36)")
                        str_list.s = to_string("", "x(8)") + format_fixed_length(l_lager.bezeich, 24)
                        str_list.bezeich = to_string("", "x(8)") + format_fixed_length(l_lager.bezeich, 36)
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        do_it = False

                    if create_it:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.fibu = fibukonto
                            s_list.bezeich = cost_bezeich

                            if cc_code != 0:
                                s_list.bezeich = to_string(cc_code, "9999") + " " + s_list.bezeich

                        s_list.cost = s_list.cost + l_ophis.warenwert
                        t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                        t_val =  to_decimal(t_val) + to_decimal(l_ophis.warenwert)
                        tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list.lscheinnr = l_ophis.lscheinnr
                        str_list.other_fibu = other_fibu
                        str_list.fibu = fibukonto
                        str_list.op_recid = l_ophis._recid
                        str_list.gldept = to_string(gl_department.nr) + " - " + gl_department.bezeich
                        str_list.masseinheit = l_artikel.masseinheit

                        queasy = get_cache (Queasy, {"key": [(eq, 340)],"char1": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)],"deci1": [(eq, l_ophis.einzelpreis)]})

                        if queasy:
                            str_list.remark_artikel = queasy.char2
                        else:
                            str_list.remark_artikel = ""

                        if not long_digit:

                            if l_ophis.einzelpreis > 9999999:
                                str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                                str_list.bezeich = to_string(s_list.bezeich)
                                str_list.artnr = to_string(l_artikel.artnr)
                                str_list.description = to_string(l_artikel.bezeich, "x(55)")
                                str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                                str_list.einzelpreis = to_string(l_ophis.einzelpreis, " >>>,>>>,>>9")
                                str_list.warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")
                                
                                # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")

                                if l_ophis.warenwert >= 0:
                                    tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">,>>>,>>>,>>9.99"), 17)
                                else:
                                    tmp_warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                if l_ophis.anzahl >= 0:
                                    tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                                else:
                                    tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                                str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + format_fixed_length(to_string(l_ophis.einzelpreis, ">>>,>>>,>>9"), 12) + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)
                            else:
                                str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                                str_list.bezeich = to_string(s_list.bezeich)
                                str_list.artnr = to_string(l_artikel.artnr)
                                str_list.description = to_string(l_artikel.bezeich, "x(55)")
                                str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                                str_list.einzelpreis = to_string(l_ophis.einzelpreis, ">,>>>,>>9.99")
                                str_list.warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")

                                if l_ophis.warenwert >= 0:
                                    tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">,>>>,>>>,>>9.99"), 17)
                                else:
                                    tmp_warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                if l_ophis.anzahl >= 0:
                                    tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                                else:
                                    tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                                str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)
                        else:
                            str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                            str_list.bezeich = to_string(s_list.bezeich)
                            str_list.artnr = to_string(l_artikel.artnr)
                            str_list.description = to_string(l_artikel.bezeich, "x(55)")
                            str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                            str_list.einzelpreis = to_string(l_ophis.einzelpreis, " >>>,>>>,>>9")
                            str_list.warenwert = to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9")

                            # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9") + to_string(l_ophis.lscheinnr, "x(12)")

                            if l_ophis.warenwert >= 0:
                                tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">>>,>>>,>>>,>>9"), 16)
                            else:
                                tmp_warenwert = to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9")

                            if l_ophis.anzahl >= 0:
                                tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                            else:
                                tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                            str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + format_fixed_length(to_string(l_ophis.einzelpreis, ">>>,>>>,>>9"), 12) + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)

        if t_anz != 0:
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.description = "Subtotal "
            str_list.anzahl = to_string(t_anz, "->,>>>,>>9.999")

            if not long_digit:
                str_list.warenwert = trim(to_string(t_val, "->,>>>,>>>,>>9.99"))
            else:
                str_list.warenwert = trim(to_string(t_val, "->>>,>>>,>>>,>>9"))

            str_list = Str_list()
            str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.description = "T O T A L"
        str_list.anzahl = to_string(tot_anz, "->,>>>,>>9.999")

        if not long_digit:
            str_list.warenwert = trim(to_string(tot_amount, "->,>>>,>>>,>>9.99"))
        else:
            str_list.warenwert = trim(to_string(tot_amount, "->>>>,>>>,>>>,>>9"))

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        # str_list.s = to_string("", "x(8)") + to_string(translateExtended ("SUMMARY OF EXPENSES", lvcarea, "") , "x(30)")
        str_list.s = to_string("", "x(8)") + format_fixed_length(translateExtended ("SUMMARY OF EXPENSES", lvcarea, ""), 30)
        str_list.mark = "Summary"

        tot_amount =  to_decimal("0")

        for s_list in query(s_list_data, sort_by=[("bezeich",False)]):
            str_list = Str_list()
            str_list_data.append(str_list)

            if not long_digit:
                # str_list.description = to_string(s_list.bezeich, "x(32)")
                str_list.description = format_fixed_length(s_list.bezeich, 32)
                str_list.warenwert = trim(to_string(s_list.cost, "->,>>>,>>>,>>9.99"))
            else:
                # str_list.description = to_string(s_list.bezeich, "x(32)")
                str_list.description = format_fixed_length(s_list.bezeich, 32)
                str_list.warenwert = trim(to_string(s_list.cost, "->>>>,>>>,>>>,>>9"))

            tot_amount =  to_decimal(tot_amount) + to_decimal(s_list.cost)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.description = "T O T A L"

        if not long_digit:
            str_list.warenwert = trim(to_string(tot_amount, "->,>>>,>>>,>>9.99"))
        else:
            str_list.warenwert = trim(to_string(tot_amount, "->>>>,>>>,>>>,>>9"))


    def get_costcenter_code(fibukonto:string):

        nonlocal it_exist, str_list_data, tot_anz, tot_amount, i, lvcarea, gl_acct, l_lager, l_ophhis, gl_department, l_artikel, l_ophis, parameters, queasy, l_untergrup
        nonlocal pvilanguage, trans_code, from_grp, mi_alloc_chk, mi_article_chk, mi_docu_chk, mi_date_chk, from_lager, to_lager, from_date, to_date, from_art, to_art, deptno, long_digit, cost_acct, mattype, mi_sub_group


        nonlocal s_list, str_list
        nonlocal s_list_data, str_list_data

        cc_code = 0

        def generate_inner_output():
            return (cc_code)


        parameters = get_cache (Parameters, {"progname": [(eq, "costcenter")],"section": [(eq, "alloc")],"varname": [(gt, "")],"vstring": [(eq, fibukonto)]})

        if parameters:
            cc_code = to_int(parameters.varname)

        return generate_inner_output()


    def create_listd():

        nonlocal it_exist, str_list_data, tot_anz, tot_amount, i, lvcarea, gl_acct, l_lager, l_ophhis, gl_department, l_artikel, l_ophis, parameters, queasy, l_untergrup
        nonlocal pvilanguage, trans_code, from_grp, mi_alloc_chk, mi_article_chk, mi_docu_chk, mi_date_chk, from_lager, to_lager, from_date, to_date, from_art, to_art, deptno, long_digit, cost_acct, mattype, mi_sub_group


        nonlocal s_list, str_list
        nonlocal s_list_data, str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        lschein:string = ""
        cost_bezeich:string = ""
        fibukonto:string = ""
        do_it:bool = False
        cc_code:int = 0
        other_fibu:bool = False
        gl_acct1 = None
        create_it:bool = False
        curr_fibu:string = ""
        grp1:int = 0
        grp2:int = 1
        curr_zwkum:int = 0
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        it_exist = False
        str_list_data.clear()
        s_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():

            do_it = True

            is_connected_to_vhparch = check_connection_arch()

            if is_connected_to_vhparch:
                it_exist, t_anz, t_val, tot_anz, tot_amount = get_output(stockhoutli_arch('list', l_lager.lager_nr, from_date, to_date, from_art, to_art, deptno, long_digit, do_it, l_lager.bezeich, from_grp, "", ""))
            else:
                l_ophis_obj_list = {}
                for l_ophis, l_ophhis, gl_acct, gl_department, l_artikel, l_untergrup in db_session.query(L_ophis, L_ophhis, Gl_acct, Gl_department, L_artikel, L_untergrup).join(L_ophhis,(L_ophhis.op_typ == ("STT").lower()) & (L_ophhis.lscheinnr == L_ophis.lscheinnr) & (L_ophhis.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophis.fibukonto)).join(Gl_department,(Gl_department.nr == Gl_acct.deptnr)).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter((L_ophis.lager_nr == l_lager.lager_nr) & (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.artnr >= from_art) & (L_ophis.artnr <= to_art) & (L_ophis.anzahl != 0) & (L_ophis.op_art == 3)).order_by(L_untergrup.bezeich, L_ophis.datum, L_ophis.artnr).all():

                    # if l_ophis_obj_list.get(l_ophis._recid):
                    #     continue
                    # else:
                    #     l_ophis_obj_list[l_ophis._recid] = True

                    it_exist = True
                    other_fibu = False

                    if l_ophis.fibukonto != "":

                        if deptno != 0:
                            gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)],"deptnr": [(eq, deptno)]})
                        else:
                            gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)]})

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

                        parameters = get_cache (Parameters, {"progname": [(eq, "costcenter")],"section": [(eq, "alloc")],"varname": [(eq, to_string(deptno))],"vstring": [(eq, fibukonto)]})
                        create_it = None != parameters

                    if curr_fibu == "":
                        curr_fibu = fibukonto

                    if curr_fibu.lower()  != (fibukonto).lower()  and t_anz != 0:
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list.description = "Subtotal"
                        str_list.anzahl = to_string(t_anz, "->,>>>,>>9.999")

                        if not long_digit:
                            str_list.warenwert = to_string(t_val, "->,>>>,>>>,>>9.99")
                        else:
                            str_list.warenwert = to_string(t_val, "->>>,>>>,>>>,>>9")

                        t_anz =  to_decimal("0")
                        t_val =  to_decimal("0")

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        lschein = l_ophis.lscheinnr
                        curr_fibu = fibukonto

                    if do_it:
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        # str_list.s = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(24)")
                        # str_list.bezeich = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(36)")
                        str_list.s = to_string("", "x(8)") + format_fixed_length(l_lager.bezeich, 24)
                        str_list.bezeich = to_string("", "x(8)") + format_fixed_length(l_lager.bezeich, 36)
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        do_it = False

                    if curr_zwkum != l_untergrup.zwkum:
                        curr_zwkum = l_untergrup.zwkum
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        # str_list.s = to_string("", "x(8)") + to_string(l_untergrup.bezeich, "x(24)")
                        # str_list.bezeich = to_string("", "x(8)") + to_string(l_untergrup.bezeich, "x(24)")
                        str_list.s = to_string("", "x(8)") + format_fixed_length(l_untergrup.bezeich, 24)
                        str_list.bezeich = to_string("", "x(8)") + format_fixed_length(l_untergrup.bezeich, 36)

                    if create_it:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.fibu = fibukonto
                            s_list.bezeich = cost_bezeich

                            if cc_code != 0:
                                s_list.bezeich = to_string(cc_code, "9999") + " " + s_list.bezeich

                        s_list.cost = s_list.cost + l_ophis.warenwert
                        t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                        t_val =  to_decimal(t_val) + to_decimal(l_ophis.warenwert)
                        tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list.lscheinnr = l_ophis.lscheinnr
                        str_list.fibu = fibukonto
                        str_list.other_fibu = other_fibu
                        str_list.op_recid = l_ophis._recid
                        str_list.gldept = to_string(gl_department.nr) + " - " + gl_department.bezeich
                        str_list.masseinheit = l_artikel.masseinheit

                        queasy = get_cache (Queasy, {"key": [(eq, 340)],"char1": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)],"deci1": [(eq, l_ophis.einzelpreis)]})

                        if queasy:
                            str_list.remark_artikel = queasy.char2
                        else:
                            str_list.remark_artikel = ""

                        if not long_digit:

                            if l_ophis.einzelpreis > 9999999:
                                str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                                str_list.bezeich = to_string(s_list.bezeich)
                                str_list.artnr = to_string(l_artikel.artnr)
                                str_list.description = to_string(l_artikel.bezeich, "x(55)")
                                str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                                str_list.einzelpreis = to_string(l_ophis.einzelpreis, " >>>,>>>,>>9")
                                str_list.warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")

                                if l_ophis.warenwert >= 0:
                                    tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">,>>>,>>>,>>9.99"), 17)
                                else:
                                    tmp_warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                if l_ophis.anzahl >= 0:
                                    tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                                else:
                                    tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                                str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + format_fixed_length(to_string(l_ophis.einzelpreis, ">>>,>>>,>>9"), 12) + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)
                            else:
                                str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                                str_list.bezeich = to_string(s_list.bezeich)
                                str_list.artnr = to_string(l_artikel.artnr)
                                str_list.description = to_string(l_artikel.bezeich, "x(55)")
                                str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                                str_list.einzelpreis = to_string(l_ophis.einzelpreis, ">,>>>,>>9.99")
                                str_list.warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")

                                if l_ophis.warenwert >= 0:
                                    tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">,>>>,>>>,>>9.99"), 17)
                                else:
                                    tmp_warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                if l_ophis.anzahl >= 0:
                                    tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                                else:
                                    tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                                str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)
                        else:
                            str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                            str_list.bezeich = to_string(s_list.bezeich)
                            str_list.artnr = to_string(l_artikel.artnr)
                            str_list.description = to_string(l_artikel.bezeich, "x(55)")
                            str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                            str_list.einzelpreis = to_string(l_ophis.einzelpreis, " >>>,>>>,>>9")
                            str_list.warenwert = to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9")

                            # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9") + to_string(l_ophis.lscheinnr, "x(12)")

                            if l_ophis.warenwert >= 0:
                                tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">>>,>>>,>>>,>>9"), 16)
                            else:
                                tmp_warenwert = to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9")

                            if l_ophis.anzahl >= 0:
                                tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                            else:
                                tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                            str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + format_fixed_length(to_string(l_ophis.einzelpreis, ">>>,>>>,>>9"), 12) + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)

        if t_anz != 0:
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.description = "Subtotal "
            str_list.anzahl = to_string(t_anz, "->,>>>,>>9.999")

            if not long_digit:
                str_list.warenwert = trim(to_string(t_val, "->,>>>,>>>,>>9.99"))
            else:
                str_list.warenwert = trim(to_string(t_val, "->>>,>>>,>>>,>>9"))

            str_list = Str_list()
            str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.description = "T O T A L"
        str_list.anzahl = to_string(tot_anz, "->,>>>,>>9.999")

        if not long_digit:
            str_list.warenwert = trim(to_string(tot_amount, "->,>>>,>>>,>>9.99"))
        else:
            str_list.warenwert = trim(to_string(tot_amount, "->>>>,>>>,>>>,>>9"))

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        tot_amount =  to_decimal("0")

        for s_list in query(s_list_data, sort_by=[("bezeich",False)]):
            str_list = Str_list()
            str_list_data.append(str_list)

            if not long_digit:
                # str_list.description = to_string(s_list.bezeich, "x(32)")
                str_list.description = format_fixed_length(s_list.bezeich, 32)
                str_list.warenwert = trim(to_string(s_list.cost, "->,>>>,>>>,>>9.99"))
            else:
                # str_list.description = to_string(s_list.bezeich, "x(32)")
                str_list.description = format_fixed_length(s_list.bezeich, 32)
                str_list.warenwert = trim(to_string(s_list.cost, "->>>>,>>>,>>>,>>9"))

            tot_amount =  to_decimal(tot_amount) + to_decimal(s_list.cost)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.description = "T O T A L"

        if not long_digit:
            str_list.warenwert = trim(to_string(tot_amount, "->,>>>,>>>,>>9.99"))
        else:
            str_list.warenwert = trim(to_string(tot_amount, "->>>>,>>>,>>>,>>9"))


    def create_list1d():

        nonlocal it_exist, str_list_data, tot_anz, tot_amount, i, lvcarea, gl_acct, l_lager, l_ophhis, gl_department, l_artikel, l_ophis, parameters, queasy, l_untergrup
        nonlocal pvilanguage, trans_code, from_grp, mi_alloc_chk, mi_article_chk, mi_docu_chk, mi_date_chk, from_lager, to_lager, from_date, to_date, from_art, to_art, deptno, long_digit, cost_acct, mattype, mi_sub_group


        nonlocal s_list, str_list
        nonlocal s_list_data, str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        curr_artnr:int = 0
        lschein:string = ""
        datum:date = None
        cost_bezeich:string = ""
        fibukonto:string = ""
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
        str_list_data.clear()
        s_list_data.clear()

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

            is_connected_to_vhparch = check_connection_arch()

            if is_connected_to_vhparch:
                it_exist, t_anz, t_val, tot_anz, tot_amount = get_output(stockhoutli_arch('list1C', l_lager.lager_nr, from_date, to_date, from_art, to_art, deptno, long_digit, do_it, l_lager.bezeich, from_grp, grp1, grp2))
            else:
                l_ophis_obj_list = {}
                for l_ophis, l_artikel, l_ophhis, gl_acct, gl_department, l_untergrup in db_session.query(L_ophis, L_artikel, L_ophhis, Gl_acct, Gl_department, L_untergrup).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum == from_grp)).join(L_ophhis,(L_ophhis.op_typ == ("STT").lower()) & (L_ophhis.lscheinnr == L_ophis.lscheinnr) & (L_ophhis.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophis.fibukonto)).join(Gl_department,(Gl_department.nr == Gl_acct.deptnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum) & ((L_untergrup.betriebsnr >= grp1) & (L_untergrup.betriebsnr <= grp2))).filter((L_ophis.lager_nr == l_lager.lager_nr) & (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.artnr >= from_art) & (L_ophis.artnr <= to_art) & (L_ophis.anzahl != 0) & (L_ophis.op_art == 3)).order_by(L_untergrup.bezeich, L_ophis.datum, L_ophis.artnr).all():

                    # if l_ophis_obj_list.get(l_ophis._recid):
                    #     continue
                    # else:
                    #     l_ophis_obj_list[l_ophis._recid] = True

                    it_exist = True
                    other_fibu = False

                    if l_ophis.fibukonto != "":

                        if deptno != 0:
                            gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)],"deptnr": [(eq, deptno)]})
                        else:
                            gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)]})

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

                        parameters = get_cache (Parameters, {"progname": [(eq, "costcenter")],"section": [(eq, "alloc")],"varname": [(eq, to_string(deptno))],"vstring": [(eq, gl_acct.fibukonto)]})
                        create_it = None != parameters

                    if datum == None:
                        datum = l_ophis.datum

                    if datum != l_ophis.datum and t_anz != 0:
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list.description = "Subtotal"
                        str_list.anzahl = to_string(t_anz, "->,>>>,>>9.999")

                        if not long_digit:
                            str_list.warenwert = to_string(t_val, "->,>>>,>>>,>>9.99")
                        else:
                            str_list.warenwert = to_string(t_val, "->>>,>>>,>>>,>>9")

                        t_anz =  to_decimal("0")
                        t_val =  to_decimal("0")

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        lschein = l_ophis.lscheinnr
                        datum = l_ophis.datum
                        curr_artnr = l_ophis.artnr

                    if do_it:
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        # str_list.s = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(30)")
                        # str_list.bezeich = to_string("", "x(8)") + to_string(l_lager.bezeich, "x(36)")
                        str_list.s = to_string("", "x(8)") + format_fixed_length(l_lager.bezeich, 24)
                        str_list.bezeich = to_string("", "x(8)") + format_fixed_length(l_lager.bezeich, 36)
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        do_it = False

                    if curr_zwkum != l_untergrup.zwkum:
                        curr_zwkum = l_untergrup.zwkum
                        str_list = Str_list()
                        str_list_data.append(str_list)

                        # str_list.s = to_string("", "x(8)") + to_string(l_untergrup.bezeich, "x(24)")
                        # str_list.bezeich = to_string("", "x(8)") + to_string(l_untergrup.bezeich, "x(24)")
                        str_list.s = to_string("", "x(8)") + format_fixed_length(l_untergrup.bezeich, 24)
                        str_list.bezeich = to_string("", "x(8)") + format_fixed_length(l_untergrup.bezeich, 24)

                    if create_it:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.fibu.lower()  == (fibukonto).lower()), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.fibu = fibukonto
                            s_list.bezeich = cost_bezeich

                            if cc_code != 0:
                                s_list.bezeich = to_string(cc_code, "9999") + " " + s_list.bezeich

                        s_list.cost = s_list.cost + l_ophis.warenwert
                        t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                        t_val =  to_decimal(t_val) + to_decimal(l_ophis.warenwert)
                        tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                        str_list = Str_list()
                        str_list_data.append(str_list)

                        str_list.lscheinnr = l_ophis.lscheinnr
                        str_list.other_fibu = other_fibu
                        str_list.fibu = fibukonto
                        str_list.op_recid = l_ophis._recid
                        str_list.gldept = to_string(gl_department.nr) + " - " + gl_department.bezeich
                        str_list.masseinheit = l_artikel.masseinheit

                        queasy = get_cache (Queasy, {"key": [(eq, 340)],"char1": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)],"deci1": [(eq, l_ophis.einzelpreis)]})

                        if queasy:
                            str_list.remark_artikel = queasy.char2
                        else:
                            str_list.remark_artikel = ""

                        if not long_digit:

                            if l_ophis.einzelpreis > 9999999:
                                str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                                str_list.bezeich = to_string(s_list.bezeich)
                                str_list.artnr = to_string(l_artikel.artnr)
                                str_list.description = to_string(l_artikel.bezeich, "x(55)")
                                str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                                str_list.einzelpreis = to_string(l_ophis.einzelpreis, " >>>,>>>,>>9")
                                str_list.warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")

                                if l_ophis.warenwert >= 0:
                                    tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">,>>>,>>>,>>9.99"), 17)
                                else:
                                    tmp_warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                if l_ophis.anzahl >= 0:
                                    tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                                else:
                                    tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                                str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + format_fixed_length(to_string(l_ophis.einzelpreis, ">>>,>>>,>>9"), 12) + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)
                            else:
                                str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                                str_list.bezeich = to_string(s_list.bezeich)
                                str_list.artnr = to_string(l_artikel.artnr)
                                str_list.description = to_string(l_artikel.bezeich, "x(55)")
                                str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                                str_list.einzelpreis = to_string(l_ophis.einzelpreis, ">,>>>,>>9.99")
                                str_list.warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(12)")

                                if l_ophis.warenwert >= 0:
                                    tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">,>>>,>>>,>>9.99"), 17)
                                else:
                                    tmp_warenwert = to_string(l_ophis.warenwert, "->,>>>,>>>,>>9.99")

                                if l_ophis.anzahl >= 0:
                                    tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                                else:
                                    tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                                str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + to_string(l_ophis.einzelpreis, ">,>>>,>>9.99") + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)
                        else:
                            str_list.datum = l_ophis.datum.strftime("%d/%m/%y")
                            str_list.bezeich = to_string(s_list.bezeich)
                            str_list.artnr = to_string(l_artikel.artnr)
                            str_list.description = to_string(l_artikel.bezeich, "x(55)")
                            str_list.anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")
                            str_list.einzelpreis = to_string(l_ophis.einzelpreis, " >>>,>>>,>>9")
                            str_list.warenwert = to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9")

                            # str_list.s = to_string(l_ophis.datum) + to_string(s_list.bezeich, "x(30)") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(55)") + to_string(l_ophis.anzahl, "->,>>>,>>9.999") + to_string(l_ophis.einzelpreis, " >>>,>>>,>>9") + to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9") + to_string(l_ophis.lscheinnr, "x(12)")

                            if l_ophis.warenwert >= 0:
                                tmp_warenwert = format_fixed_length(to_string(l_ophis.warenwert, ">>>,>>>,>>>,>>9"), 16)
                            else:
                                tmp_warenwert = to_string(l_ophis.warenwert, "->>>,>>>,>>>,>>9")

                            if l_ophis.anzahl >= 0:
                                tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.999"), 14)
                            else:
                                tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.999")

                            str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(s_list.bezeich, 30) + to_string(l_artikel.artnr, "9999999") + format_fixed_length(l_artikel.bezeich, 55) + tmp_anzahl + format_fixed_length(to_string(l_ophis.einzelpreis, ">>>,>>>,>>9"), 12) + tmp_warenwert + format_fixed_length(l_ophis.lscheinnr, 12)

        if t_anz != 0:
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.description = "Subtotal "
            str_list.anzahl = to_string(t_anz, "->,>>>,>>9.999")

            if not long_digit:
                str_list.warenwert = trim(to_string(t_val, "->,>>>,>>>,>>9.99"))
            else:
                str_list.warenwert = trim(to_string(t_val, "->>>,>>>,>>>,>>9"))

            str_list = Str_list()
            str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.description = "T O T A L"
        str_list.anzahl = to_string(tot_anz, "->,>>>,>>9.999")

        if not long_digit:
            str_list.warenwert = trim(to_string(tot_amount, "->,>>>,>>>,>>9.99"))
        else:
            str_list.warenwert = trim(to_string(tot_amount, "->>>>,>>>,>>>,>>9"))

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        # str_list.s = to_string("", "x(8)") + to_string(translateExtended ("SUMMARY OF EXPENSES", lvcarea, "") , "x(30)")
        str_list.s = to_string("", "x(8)") + format_fixed_length(translateExtended ("SUMMARY OF EXPENSES", lvcarea, ""), 30)
        str_list.mark = "Summary"

        tot_amount =  to_decimal("0")

        for s_list in query(s_list_data, sort_by=[("bezeich",False)]):
            str_list = Str_list()
            str_list_data.append(str_list)

            if not long_digit:
                # str_list.description = to_string(s_list.bezeich, "x(32)")
                str_list.description = format_fixed_length(s_list.bezeich, 32)
                str_list.warenwert = trim(to_string(s_list.cost, "->,>>>,>>>,>>9.99"))
            else:
                # str_list.description = to_string(s_list.bezeich, "x(32)")
                str_list.description = format_fixed_length(s_list.bezeich, 32)
                str_list.warenwert = trim(to_string(s_list.cost, "->>>>,>>>,>>>,>>9"))

            tot_amount =  to_decimal(tot_amount) + to_decimal(s_list.cost)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.description = "T O T A L"

        if not long_digit:
            str_list.warenwert = trim(to_string(tot_amount, "->,>>>,>>>,>>9.99"))
        else:
            str_list.warenwert = trim(to_string(tot_amount, "->>>>,>>>,>>>,>>9"))

    if trans_code != "":
        create_list_trans()
    else:

        if from_grp == 0:

            if mi_alloc_chk :
                create_list()

            elif mi_article_chk :
                create_lista()

            elif mi_docu_chk :
                create_listb()

            elif mi_date_chk :
                create_listc()

            elif mi_sub_group :
                create_listd()
        else:

            if mi_alloc_chk :
                create_list1()

            elif mi_article_chk :
                create_list1a()

            elif mi_docu_chk :
                create_list1b()

            elif mi_date_chk :
                create_list1c()

            elif mi_sub_group :
                create_list1d()

    return generate_output()