#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Fa_lager, Mathis, Fa_artikel, Fa_grup, Gl_acct, Fa_kateg, Htparam

lagerbuff_list, Lagerbuff = create_model_like(Fa_lager)

def fa_valuate_btn_gobl(pvilanguage:int, lagerbuff_list:[Lagerbuff], mi_lager_chk:bool, mi_subgrp_chk:bool, mi_acct_chk:bool, mi_bookvalue_chk:bool, from_grp:int, from_date:date, to_lager:int, from_lager:int, maxnr:int, to_date:date, zero_value_only:bool, last_acctdate:date, yy:int, mm:int, from_subgr:int, to_subgr:int):

    prepare_cache ([Mathis, Fa_artikel, Fa_grup, Fa_kateg, Htparam])

    str_list_list = []
    do_it:bool = False
    sub_depn:int = 0
    val_dep:Decimal = to_decimal("0.0")
    datum:date = None
    flag:bool = False
    p_depn_wert:Decimal = to_decimal("0.0")
    p_book_wert:Decimal = to_decimal("0.0")
    lvcarea:string = "fa-valuate"
    fa_lager = mathis = fa_artikel = fa_grup = gl_acct = fa_kateg = htparam = None

    lagerbuff = str_list = None

    str_list_list, Str_list = create_model("Str_list", {"flag":int, "refno":string, "location":string, "s":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_list_list, do_it, sub_depn, val_dep, datum, flag, p_depn_wert, p_book_wert, lvcarea, fa_lager, mathis, fa_artikel, fa_grup, gl_acct, fa_kateg, htparam
        nonlocal pvilanguage, mi_lager_chk, mi_subgrp_chk, mi_acct_chk, mi_bookvalue_chk, from_grp, from_date, to_lager, from_lager, maxnr, to_date, zero_value_only, last_acctdate, yy, mm, from_subgr, to_subgr


        nonlocal lagerbuff, str_list
        nonlocal str_list_list

        return {"str-list": str_list_list}

    def create_list():

        nonlocal str_list_list, do_it, sub_depn, val_dep, datum, flag, p_depn_wert, p_book_wert, lvcarea, fa_lager, mathis, fa_artikel, fa_grup, gl_acct, fa_kateg, htparam
        nonlocal pvilanguage, mi_lager_chk, mi_subgrp_chk, mi_acct_chk, mi_bookvalue_chk, from_grp, from_date, to_lager, from_lager, maxnr, to_date, zero_value_only, last_acctdate, yy, mm, from_subgr, to_subgr


        nonlocal lagerbuff, str_list
        nonlocal str_list_list

        i:int = 0
        j:int = 0
        t_anz:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        t_val1:Decimal = to_decimal("0.0")
        t_val2:Decimal = to_decimal("0.0")
        tt_anz:Decimal = to_decimal("0.0")
        tt_val:Decimal = to_decimal("0.0")
        tt_val1:Decimal = to_decimal("0.0")
        tt_val2:Decimal = to_decimal("0.0")
        tot_anz:Decimal = to_decimal("0.0")
        tot_val:Decimal = to_decimal("0.0")
        tot_val1:Decimal = to_decimal("0.0")
        tot_val2:Decimal = to_decimal("0.0")
        zwkum:int = 0
        bezeich:string = ""
        l_oh = None
        qty:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        max_lager:int = 0
        L_oh =  create_buffer("L_oh",Mathis)
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_val =  to_decimal("0")
        tot_val1 =  to_decimal("0")
        tot_val2 =  to_decimal("0")


        max_lager = to_lager

        if from_lager != to_lager and (maxnr - 1) == to_lager:
            max_lager = maxnr

        for lagerbuff in query(lagerbuff_list, filters=(lambda lagerbuff: lagerbuff.lagerBuff.lager_nr >= from_lager and lagerBuff.lager_nr <= maxnr)):
            i = 0
            zwkum = 0
            t_anz =  to_decimal("0")
            t_val =  to_decimal("0")
            t_val1 =  to_decimal("0")
            t_val2 =  to_decimal("0")
            tt_anz =  to_decimal("0")
            tt_val =  to_decimal("0")
            tt_val1 =  to_decimal("0")
            tt_val2 =  to_decimal("0")
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.s = to_string(lagerBuff.lager_nr, ">>99") + "-" + to_string(lagerBuff.bezeich, "x(56)")

            if mi_bookvalue_chk :

                mathis_obj_list = {}
                mathis = Mathis()
                fa_artikel = Fa_artikel()
                fa_grup = Fa_grup()
                for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel.katnr, fa_artikel._recid, fa_grup.bezeich, fa_grup._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel.katnr, Fa_artikel._recid, Fa_grup.bezeich, Fa_grup._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.gnr) & (Fa_grup.flag == 0)).filter(
                         (Mathis.location == lagerBuff.bezeich) & (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Fa_grup.gnr, Mathis.name).all():
                    if mathis_obj_list.get(mathis._recid):
                        continue
                    else:
                        mathis_obj_list[mathis._recid] = True


                    do_it = False

                    if not zero_value_only:
                        do_it = True
                    else:
                        do_it = fa_artikel.book_wert == 0

                    if do_it:

                        if zwkum != fa_artikel.gnr:

                            if zwkum != 0:
                                str_list = Str_list()
                                str_list_list.append(str_list)

                                for j in range(1,60 + 1) :
                                    str_list.s = str_list.s + " "
                                str_list.refno = "SUB TOTAL"
                                str_list.s = str_list.s + to_string("SUB TOTAL", "x(22)")

                                if t_anz > 99999:
                                    str_list.s = str_list.s + to_string(t_anz, ">>>>>9")
                                else:
                                    str_list.s = str_list.s + to_string(t_anz, ">>,>>9")

                                if t_val > 99999999999 or t_val1 > 99999999999 or t_val2 > 99999999999:
                                    str_list.s = str_list.s + to_string(t_val, ">,>>>,>>>,>>>,>>9") + to_string(t_val1, ">,>>>,>>>,>>>,>>9") + to_string(t_val2, ">,>>>,>>>,>>>,>>9")
                                else:
                                    str_list.s = str_list.s + to_string(t_val, ">>>,>>>,>>>,>>9.99") + to_string(t_val1, ">>>,>>>,>>>,>>9.99") + to_string(t_val2, ">>>,>>>,>>>,>>9.99")
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.s = to_string(fa_grup.bezeich, "x(28)")
                            t_anz =  to_decimal("0")
                            t_val =  to_decimal("0")
                            t_val1 =  to_decimal("0")
                            t_val2 =  to_decimal("0")
                            zwkum = fa_artikel.gnr


                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.refno = mathis.asset
                        str_list.s = to_string(mathis.name, "x(60)") + to_string(mathis.asset, "x(14)") + to_string(mathis.datum) + to_string(fa_artikel.anzahl, ">>,>>9")
                        val_dep =  to_decimal(fa_artikel.depn_wert) / to_decimal(fa_artikel.anz_depn)
                        sub_depn = 0
                        flag = False

                        if val_dep == None:
                            val_dep =  to_decimal("0")
                        for datum in date_range(from_date,to_date) :

                            if flag and datum == date_mdy(get_month(datum) + 1, 1, get_year(datum)) - 1:
                                sub_depn = sub_depn + 1

                            if datum == fa_artikel.first_depn:
                                sub_depn = sub_depn + 1
                                flag = True

                            if datum == fa_artikel.last_depn:
                                break
                        p_depn_wert =  to_decimal(val_dep) * to_decimal(sub_depn)
                        p_book_wert =  to_decimal(fa_artikel.warenwert) - to_decimal(p_depn_wert)


                        i = i + 1
                        t_anz =  to_decimal(t_anz) + to_decimal(fa_artikel.anzahl)
                        t_val =  to_decimal(t_val) + to_decimal(fa_artikel.warenwert)
                        t_val1 =  to_decimal(t_val1) + to_decimal(p_depn_wert)
                        t_val2 =  to_decimal(t_val2) + to_decimal(p_book_wert)
                        tt_anz =  to_decimal(tt_anz) + to_decimal(fa_artikel.anzahl)
                        tt_val =  to_decimal(tt_val) + to_decimal(fa_artikel.warenwert)
                        tt_val1 =  to_decimal(tt_val1) + to_decimal(p_depn_wert)
                        tt_val2 =  to_decimal(tt_val2) + to_decimal(p_book_wert)
                        tot_anz =  to_decimal(tot_anz) + to_decimal(fa_artikel.anzahl)
                        tot_val =  to_decimal(tot_val) + to_decimal(fa_artikel.warenwert)
                        tot_val1 =  to_decimal(tot_val1) + to_decimal(p_depn_wert)
                        tot_val2 =  to_decimal(tot_val2) + to_decimal(p_book_wert)
                        str_list.s = str_list.s + to_string(fa_artikel.warenwert, ">,>>>,>>>,>>>,>>9.99") + to_string(p_depn_wert, ">>>,>>>,>>>,>>9.99") + to_string(p_book_wert, ">>>,>>>,>>>,>>9.99")

                        if fa_artikel.first_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.first_depn)
                        else:
                            str_list.s = str_list.s + " "

                        if fa_artikel.next_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.next_depn)
                        else:
                            str_list.s = str_list.s + " "

                        if fa_artikel.last_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.last_depn)
                        else:
                            str_list.s = str_list.s + " "

                        if fa_artikel.anz_depn != None:
                            str_list.s = str_list.s + to_string(sub_depn)
                        else:
                            str_list.s = str_list.s + " "
            else:

                mathis_obj_list = {}
                mathis = Mathis()
                fa_artikel = Fa_artikel()
                fa_grup = Fa_grup()
                for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel.katnr, fa_artikel._recid, fa_grup.bezeich, fa_grup._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel.katnr, Fa_artikel._recid, Fa_grup.bezeich, Fa_grup._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.gnr) & (Fa_grup.flag == 0)).filter(
                         (Mathis.location == lagerBuff.bezeich) & (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Fa_grup.gnr, Mathis.name).all():
                    if mathis_obj_list.get(mathis._recid):
                        continue
                    else:
                        mathis_obj_list[mathis._recid] = True


                    do_it = False

                    if not zero_value_only:
                        do_it = True
                    else:
                        do_it = fa_artikel.book_wert == 0

                    if do_it:

                        if zwkum != fa_artikel.gnr:

                            if zwkum != 0:
                                str_list = Str_list()
                                str_list_list.append(str_list)

                                for j in range(1,60 + 1) :
                                    str_list.s = str_list.s + " "
                                str_list.refno = "SUB TOTAL"
                                str_list.s = str_list.s + to_string("SUB TOTAL", "x(22)")

                                if t_anz > 99999:
                                    str_list.s = str_list.s + to_string(t_anz, ">>>>>9")
                                else:
                                    str_list.s = str_list.s + to_string(t_anz, ">>,>>9")

                                if t_val > 99999999999 or t_val1 > 99999999999 or t_val2 > 99999999999:
                                    str_list.s = str_list.s + to_string(t_val, ">,>>>,>>>,>>>,>>9") + to_string(t_val1, ">,>>>,>>>,>>>,>>9") + to_string(t_val2, ">,>>>,>>>,>>>,>>9")
                                else:
                                    str_list.s = str_list.s + to_string(t_val, ">>>,>>>,>>>,>>9.99") + to_string(t_val1, ">>>,>>>,>>>,>>9.99") + to_string(t_val2, ">>>,>>>,>>>,>>9.99")
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.s = to_string(fa_grup.bezeich, "x(28)")
                            t_anz =  to_decimal("0")
                            t_val =  to_decimal("0")
                            t_val1 =  to_decimal("0")
                            t_val2 =  to_decimal("0")
                            zwkum = fa_artikel.gnr


                        i = i + 1
                        t_anz =  to_decimal(t_anz) + to_decimal(fa_artikel.anzahl)
                        t_val =  to_decimal(t_val) + to_decimal(fa_artikel.warenwert)
                        t_val1 =  to_decimal(t_val1) + to_decimal(fa_artikel.depn_wert)
                        t_val2 =  to_decimal(t_val2) + to_decimal(fa_artikel.book_wert)
                        tt_anz =  to_decimal(tt_anz) + to_decimal(fa_artikel.anzahl)
                        tt_val =  to_decimal(tt_val) + to_decimal(fa_artikel.warenwert)
                        tt_val1 =  to_decimal(tt_val1) + to_decimal(fa_artikel.depn_wert)
                        tt_val2 =  to_decimal(tt_val2) + to_decimal(fa_artikel.book_wert)
                        tot_anz =  to_decimal(tot_anz) + to_decimal(fa_artikel.anzahl)
                        tot_val =  to_decimal(tot_val) + to_decimal(fa_artikel.warenwert)
                        tot_val1 =  to_decimal(tot_val1) + to_decimal(fa_artikel.depn_wert)
                        tot_val2 =  to_decimal(tot_val2) + to_decimal(fa_artikel.book_wert)
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.refno = mathis.asset
                        str_list.s = to_string(mathis.name, "x(60)") + to_string(mathis.asset, "x(14)") + to_string(mathis.datum) + to_string(fa_artikel.anzahl, ">>,>>9")
                        str_list.s = str_list.s + to_string(fa_artikel.warenwert, ">,>>>,>>>,>>>,>>9.99") + to_string(fa_artikel.depn_wert, ">>>,>>>,>>>,>>9.99") + to_string(fa_artikel.book_wert, ">>>,>>>,>>>,>>9.99")

                        if fa_artikel.first_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.first_depn)
                        else:
                            str_list.s = str_list.s + " "

                        if fa_artikel.next_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.next_depn)
                        else:
                            str_list.s = str_list.s + " "

                        if fa_artikel.last_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.last_depn)
                        else:
                            str_list.s = str_list.s + " "

                        if fa_artikel.anz_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.anz_depn)
                        else:
                            str_list.s = str_list.s + " "

            if t_anz != 0:
                str_list = Str_list()
                str_list_list.append(str_list)

                for j in range(1,60 + 1) :
                    str_list.s = str_list.s + " "
                str_list.refno = "SUB TOTAL"
                str_list.s = str_list.s + to_string("SUB TOTAL", "x(22)")

                if t_anz > 99999:
                    str_list.s = str_list.s + to_string(t_anz, ">>>>>9")
                else:
                    str_list.s = str_list.s + to_string(t_anz, ">>,>>9")

                if t_val > 99999999999 or t_val1 > 99999999999 or t_val2 > 99999999999:
                    str_list.s = str_list.s + to_string(t_val, ">,>>>,>>>,>>>,>>9") + to_string(t_val1, ">,>>>,>>>,>>>,>>9") + to_string(t_val2, ">,>>>,>>>,>>>,>>9")
                else:
                    str_list.s = str_list.s + to_string(t_val, ">>>,>>>,>>>,>>9.99") + to_string(t_val1, ">>>,>>>,>>>,>>9.99") + to_string(t_val2, ">>>,>>>,>>>,>>9.99")

            if i > 0:
                str_list = Str_list()
                str_list_list.append(str_list)

                for j in range(1,60 + 1) :
                    str_list.s = str_list.s + " "
            str_list.refno = "T O T A L"
            str_list.flag = 1

            if length(trim(to_string(str_list.s))) != 0:
                str_list.s = str_list.s + to_string("T O T A L", "x(21)")
            else:
                str_list.s = str_list.s + to_string("T O T A L", "x(22)")

            if length(trim(to_string(tt_anz))) > 5:
                str_list.s = str_list.s + to_string(tt_anz, ">>>>>9")
            else:
                str_list.s = str_list.s + to_string(tt_anz, ">>,>>9")

            if length(trim(to_string(tt_val, ">>>,>>>,>>>,>>9.99"))) > 17:
                str_list.s = str_list.s + to_string(tt_val, ">,>>>,>>>,>>>,>>9")
            else:
                str_list.s = str_list.s + to_string(tt_val, ">>>,>>>,>>>,>>9.99")
            str_list.s = str_list.s + to_string(tt_val1, ">>>,>>>,>>>,>>9.99") + to_string(tt_val2, ">>>,>>>,>>>,>>9.99")

        if from_lager != to_lager and tot_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list = Str_list()
            str_list_list.append(str_list)

            for j in range(1,60 + 1) :
                str_list.s = str_list.s + " "
            str_list.flag = 2
            str_list.refno = "GRAND TOTAL"

            if length(trim(to_string(str_list.s))) != 0:
                str_list.s = str_list.s + to_string(" ", "x(21)")
            else:
                str_list.s = str_list.s + to_string(" ", "x(22)")

            if length(trim(to_string(tot_anz))) > 6:
                str_list.s = str_list.s + to_string(tot_anz, ">>>>>9")
            else:
                str_list.s = str_list.s + to_string(tot_anz, ">>,>>9")

            if tot_val > 99999999999 or tot_val1 > 99999999999 or tot_val2 > 99999999999:
                str_list.s = str_list.s + to_string(tot_val, ">,>>>,>>>,>>>,>>9") + to_string(tot_val1, ">,>>>,>>>,>>>,>>9") + to_string(tot_val2, ">,>>>,>>>,>>>,>>9")
            else:
                str_list.s = str_list.s + to_string(tot_val, ">>>,>>>,>>>,>>9.99") + to_string(tot_val1, ">>>,>>>,>>>,>>9.99") + to_string(tot_val2, ">>>,>>>,>>>,>>9.99")


    def create_list0():

        nonlocal str_list_list, do_it, sub_depn, val_dep, datum, flag, p_depn_wert, p_book_wert, lvcarea, fa_lager, mathis, fa_artikel, fa_grup, gl_acct, fa_kateg, htparam
        nonlocal pvilanguage, mi_lager_chk, mi_subgrp_chk, mi_acct_chk, mi_bookvalue_chk, from_grp, from_date, to_lager, from_lager, maxnr, to_date, zero_value_only, last_acctdate, yy, mm, from_subgr, to_subgr


        nonlocal lagerbuff, str_list
        nonlocal str_list_list

        i:int = 0
        j:int = 0
        t_anz:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        t_val1:Decimal = to_decimal("0.0")
        t_val2:Decimal = to_decimal("0.0")
        tt_anz:Decimal = to_decimal("0.0")
        tt_val:Decimal = to_decimal("0.0")
        tt_val1:Decimal = to_decimal("0.0")
        tt_val2:Decimal = to_decimal("0.0")
        tot_anz:Decimal = to_decimal("0.0")
        tot_val:Decimal = to_decimal("0.0")
        tot_val1:Decimal = to_decimal("0.0")
        tot_val2:Decimal = to_decimal("0.0")
        zwkum:int = 0
        bezeich:string = ""
        l_oh = None
        qty:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        max_lager:int = 0
        L_oh =  create_buffer("L_oh",Mathis)
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_val =  to_decimal("0")
        tot_val1 =  to_decimal("0")
        tot_val2 =  to_decimal("0")
        max_lager = to_lager

        if from_lager != to_lager and (maxnr - 1) == to_lager:
            max_lager = maxnr

        for lagerbuff in query(lagerbuff_list, filters=(lambda lagerbuff: lagerbuff.lagerBuff.lager_nr >= from_lager and lagerBuff.lager_nr <= maxnr)):
            i = 0
            zwkum = 0
            t_anz =  to_decimal("0")
            t_val =  to_decimal("0")
            t_val1 =  to_decimal("0")
            t_val2 =  to_decimal("0")
            tt_anz =  to_decimal("0")
            tt_val =  to_decimal("0")
            tt_val1 =  to_decimal("0")
            tt_val2 =  to_decimal("0")
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.s = to_string(lagerBuff.lager_nr, ">>99") + "-" + to_string(lagerBuff.bezeich, "x(56)")

            if mi_bookvalue_chk :

                mathis_obj_list = {}
                mathis = Mathis()
                fa_artikel = Fa_artikel()
                fa_grup = Fa_grup()
                for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel.katnr, fa_artikel._recid, fa_grup.bezeich, fa_grup._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel.katnr, Fa_artikel._recid, Fa_grup.bezeich, Fa_grup._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.gnr) & (Fa_grup.flag == 0)).filter(
                         (Mathis.location == lagerBuff.bezeich) & (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Fa_grup.gnr, Mathis.name).all():
                    if mathis_obj_list.get(mathis._recid):
                        continue
                    else:
                        mathis_obj_list[mathis._recid] = True


                    do_it = False

                    if not zero_value_only:
                        do_it = True
                    else:
                        do_it = fa_artikel.book_wert == 0

                    if do_it:

                        if zwkum != fa_artikel.gnr:

                            if zwkum != 0:
                                str_list = Str_list()
                                str_list_list.append(str_list)

                                for j in range(1,60 + 1) :
                                    str_list.s = str_list.s + " "
                                str_list.refno = "SUB TOTAL"
                                str_list.s = str_list.s + to_string("SUB TOTAL", "x(60)")

                                if t_anz > 99999:
                                    str_list.s = str_list.s + to_string(t_anz, ">>>>>9")
                                else:
                                    str_list.s = str_list.s + to_string(t_anz, ">>,>>9")

                                if t_val > 99999999999 or t_val1 > 99999999999 or t_val2 > 99999999999:
                                    str_list.s = str_list.s + to_string(t_val, ">,>>>,>>>,>>>,>>9") + to_string(t_val1, ">,>>>,>>>,>>>,>>9") + to_string(t_val2, ">,>>>,>>>,>>>,>>9")
                                else:
                                    str_list.s = str_list.s + to_string(t_val, ">>>,>>>,>>>,>>9.99") + to_string(t_val1, ">>>,>>>,>>>,>>9.99") + to_string(t_val2, ">>>,>>>,>>>,>>9.99")
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.s = to_string(fa_grup.bezeich, "x(28)")
                            t_anz =  to_decimal("0")
                            t_val =  to_decimal("0")
                            t_val1 =  to_decimal("0")
                            t_val2 =  to_decimal("0")
                            zwkum = fa_artikel.gnr


                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.refno = mathis.asset
                        str_list.s = to_string(mathis.name, "x(60)") + to_string(mathis.asset, "x(14)") + to_string(mathis.datum) + to_string(fa_artikel.anzahl, ">>,>>9")
                        val_dep =  to_decimal(fa_artikel.depn_wert) / to_decimal(fa_artikel.anz_depn)
                        sub_depn = 0
                        flag = False

                        if val_dep == None:
                            val_dep =  to_decimal("0")
                        for datum in date_range(from_date,to_date) :

                            if flag and datum == date_mdy(get_month(datum) + 1, 1, get_year(datum)) - 1:
                                sub_depn = sub_depn + 1

                            if datum == fa_artikel.first_depn:
                                sub_depn = sub_depn + 1
                                flag = True

                            if datum == fa_artikel.last_depn:
                                break
                        p_depn_wert =  to_decimal(val_dep) * to_decimal(sub_depn)
                        p_book_wert =  to_decimal(fa_artikel.warenwert) - to_decimal(p_depn_wert)


                        i = i + 1
                        t_anz =  to_decimal(t_anz) + to_decimal(fa_artikel.anzahl)
                        t_val =  to_decimal(t_val) + to_decimal(fa_artikel.warenwert)
                        t_val1 =  to_decimal(t_val1) + to_decimal(p_depn_wert)
                        t_val2 =  to_decimal(t_val2) + to_decimal(p_book_wert)
                        tt_anz =  to_decimal(tt_anz) + to_decimal(fa_artikel.anzahl)
                        tt_val =  to_decimal(tt_val) + to_decimal(fa_artikel.warenwert)
                        tt_val1 =  to_decimal(tt_val1) + to_decimal(p_depn_wert)
                        tt_val2 =  to_decimal(tt_val2) + to_decimal(p_book_wert)
                        tot_anz =  to_decimal(tot_anz) + to_decimal(fa_artikel.anzahl)
                        tot_val =  to_decimal(tot_val) + to_decimal(fa_artikel.warenwert)
                        tot_val1 =  to_decimal(tot_val1) + to_decimal(p_depn_wert)
                        tot_val2 =  to_decimal(tot_val2) + to_decimal(p_book_wert)
                        str_list.s = str_list.s + to_string(fa_artikel.warenwert, ">,>>>,>>>,>>>,>>9.99") + to_string(p_depn_wert, ">>>,>>>,>>>,>>9.99") + to_string(p_book_wert, ">>>,>>>,>>>,>>9.99")

                        if fa_artikel.first_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.first_depn)
                        else:
                            str_list.s = str_list.s + " "

                        if fa_artikel.next_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.next_depn)
                        else:
                            str_list.s = str_list.s + " "

                        if fa_artikel.last_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.last_depn)
                        else:
                            str_list.s = str_list.s + " "

                        if fa_artikel.anz_depn != None:
                            str_list.s = str_list.s + to_string(sub_depn)
                        else:
                            str_list.s = str_list.s + " "
            else:

                mathis_obj_list = {}
                mathis = Mathis()
                fa_artikel = Fa_artikel()
                fa_grup = Fa_grup()
                for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel.katnr, fa_artikel._recid, fa_grup.bezeich, fa_grup._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel.katnr, Fa_artikel._recid, Fa_grup.bezeich, Fa_grup._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.gnr) & (Fa_grup.flag == 0)).filter(
                         (Mathis.location == lagerBuff.bezeich) & (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Fa_grup.gnr, Mathis.name).all():
                    if mathis_obj_list.get(mathis._recid):
                        continue
                    else:
                        mathis_obj_list[mathis._recid] = True


                    do_it = False

                    if not zero_value_only:
                        do_it = True
                    else:
                        do_it = fa_artikel.book_wert == 0

                    if do_it:

                        if zwkum != fa_artikel.gnr:

                            if zwkum != 0:
                                str_list = Str_list()
                                str_list_list.append(str_list)

                                for j in range(1,60 + 1) :
                                    str_list.s = str_list.s + " "
                                str_list.refno = "SUB TOTAL"
                                str_list.s = str_list.s + to_string("SUB TOTAL", "x(22)")

                                if t_anz > 99999:
                                    str_list.s = str_list.s + to_string(t_anz, ">>>>>9")
                                else:
                                    str_list.s = str_list.s + to_string(t_anz, ">>,>>9")

                                if t_val > 99999999999 or t_val1 > 99999999999 or t_val2 > 99999999999:
                                    str_list.s = str_list.s + to_string(t_val, ">,>>>,>>>,>>>,>>9") + to_string(t_val1, ">,>>>,>>>,>>>,>>9") + to_string(t_val2, ">,>>>,>>>,>>>,>>9")
                                else:
                                    str_list.s = str_list.s + to_string(t_val, ">>>,>>>,>>>,>>9.99") + to_string(t_val1, ">>>,>>>,>>>,>>9.99") + to_string(t_val2, ">>>,>>>,>>>,>>9.99")
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.s = to_string(fa_grup.bezeich, "x(28)")
                            t_anz =  to_decimal("0")
                            t_val =  to_decimal("0")
                            t_val1 =  to_decimal("0")
                            t_val2 =  to_decimal("0")
                            zwkum = fa_artikel.gnr


                        i = i + 1
                        t_anz =  to_decimal(t_anz) + to_decimal(fa_artikel.anzahl)
                        t_val =  to_decimal(t_val) + to_decimal(fa_artikel.warenwert)
                        t_val1 =  to_decimal(t_val1) + to_decimal(fa_artikel.depn_wert)
                        t_val2 =  to_decimal(t_val2) + to_decimal(fa_artikel.book_wert)
                        tt_anz =  to_decimal(tt_anz) + to_decimal(fa_artikel.anzahl)
                        tt_val =  to_decimal(tt_val) + to_decimal(fa_artikel.warenwert)
                        tt_val1 =  to_decimal(tt_val1) + to_decimal(fa_artikel.depn_wert)
                        tt_val2 =  to_decimal(tt_val2) + to_decimal(fa_artikel.book_wert)
                        tot_anz =  to_decimal(tot_anz) + to_decimal(fa_artikel.anzahl)
                        tot_val =  to_decimal(tot_val) + to_decimal(fa_artikel.warenwert)
                        tot_val1 =  to_decimal(tot_val1) + to_decimal(fa_artikel.depn_wert)
                        tot_val2 =  to_decimal(tot_val2) + to_decimal(fa_artikel.book_wert)
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.refno = mathis.asset
                        str_list.s = to_string(mathis.name, "x(60)") + to_string(mathis.asset, "x(14)") + to_string(mathis.datum) + to_string(fa_artikel.anzahl, ">>,>>9")
                        str_list.s = str_list.s + to_string(fa_artikel.warenwert, ">>>,>>>,>>>,>>9.99") + to_string(fa_artikel.depn_wert, ">>>,>>>,>>>,>>9.99") + to_string(fa_artikel.book_wert, ">>>,>>>,>>>,>>9.99")

                        if fa_artikel.first_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.first_depn)
                        else:
                            str_list.s = str_list.s + " "

                        if fa_artikel.next_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.next_depn)
                        else:
                            str_list.s = str_list.s + " "

                        if fa_artikel.last_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.last_depn)
                        else:
                            str_list.s = str_list.s + " "

                        if fa_artikel.anz_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.anz_depn)
                        else:
                            str_list.s = str_list.s + " "

            if t_anz != 0:
                str_list = Str_list()
                str_list_list.append(str_list)

                for j in range(1,60 + 1) :
                    str_list.s = str_list.s + " "
                str_list.refno = "SUB TOTAL"
                str_list.s = str_list.s + to_string("SUB TOTAL", "x(22)")

                if t_anz > 99999:
                    str_list.s = str_list.s + to_string(t_anz, ">>>>>9")
                else:
                    str_list.s = str_list.s + to_string(t_anz, ">>,>>9")

                if t_val > 99999999999 or t_val1 > 99999999999 or t_val2 > 99999999999:
                    str_list.s = str_list.s + to_string(t_val, ">,>>>,>>>,>>>,>>9") + to_string(t_val1, ">,>>>,>>>,>>>,>>9") + to_string(t_val2, ">,>>>,>>>,>>>,>>9")
                else:
                    str_list.s = str_list.s + to_string(t_val, ">>>,>>>,>>>,>>9.99") + to_string(t_val1, ">>>,>>>,>>>,>>9.99") + to_string(t_val2, ">>>,>>>,>>>,>>9.99")

            if i > 0:
                str_list = Str_list()
                str_list_list.append(str_list)

                for j in range(1,60 + 1) :
                    str_list.s = str_list.s + " "
            str_list.refno = "T O T A L"
            str_list.flag = 1

            if length(trim(to_string(str_list.s))) != 0:
                str_list.s = str_list.s + to_string("T O T A L", "x(21)")
            else:
                str_list.s = str_list.s + to_string("T O T A L", "x(22)")

            if length(trim(to_string(tt_anz))) > 6:
                str_list.s = str_list.s + to_string(tt_anz, ">>>>>9")
            else:
                str_list.s = str_list.s + to_string(tt_anz, ">>,>>9")

            if length(trim(to_string(tt_val, ">>>,>>>,>>>,>>9.99"))) > 18:
                str_list.s = str_list.s + to_string(tt_val, ">,>>>,>>>,>>>,>>9")
            else:
                str_list.s = str_list.s + to_string(tt_val, ">>>,>>>,>>>,>>9.99")
            str_list.s = str_list.s + to_string(tt_val1, ">>>,>>>,>>>,>>9.99") + to_string(tt_val2, ">>>,>>>,>>>,>>9.99")

        if from_lager != to_lager and tot_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list = Str_list()
            str_list_list.append(str_list)

            for j in range(1,60 + 1) :
                str_list.s = str_list.s + " "
            str_list.flag = 2
            str_list.refno = "GRAND TOTAL"

            if length(trim(to_string(str_list.s))) != 0:
                str_list.s = str_list.s + to_string(" ", "x(21)")
            else:
                str_list.s = str_list.s + to_string(" ", "x(22)")

            if length(trim(to_string(tot_anz))) > 6:
                str_list.s = str_list.s + to_string(tot_anz, ">>>>>9")
            else:
                str_list.s = str_list.s + to_string(tot_anz, ">>,>>9")

            if tot_val > 99999999999 or tot_val1 > 99999999999 or tot_val2 > 99999999999:
                str_list.s = str_list.s + to_string(tot_val, ">,>>>,>>>,>>>,>>9") + to_string(tot_val1, ">,>>>,>>>,>>>,>>9") + to_string(tot_val2, ">,>>>,>>>,>>>,>>9")
            else:
                str_list.s = str_list.s + to_string(tot_val, ">>>,>>>,>>>,>>9.99") + to_string(tot_val1, ">>>,>>>,>>>,>>9.99") + to_string(tot_val2, ">>>,>>>,>>>,>>9.99")


    def create_list1():

        nonlocal str_list_list, do_it, sub_depn, val_dep, datum, flag, p_depn_wert, p_book_wert, lvcarea, fa_lager, mathis, fa_artikel, fa_grup, gl_acct, fa_kateg, htparam
        nonlocal pvilanguage, mi_lager_chk, mi_subgrp_chk, mi_acct_chk, mi_bookvalue_chk, from_grp, from_date, to_lager, from_lager, maxnr, to_date, zero_value_only, last_acctdate, yy, mm, from_subgr, to_subgr


        nonlocal lagerbuff, str_list
        nonlocal str_list_list

        i:int = 0
        j:int = 0
        t_anz:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        t_val1:Decimal = to_decimal("0.0")
        t_val2:Decimal = to_decimal("0.0")
        tt_anz:Decimal = to_decimal("0.0")
        tt_val:Decimal = to_decimal("0.0")
        tt_val1:Decimal = to_decimal("0.0")
        tt_val2:Decimal = to_decimal("0.0")
        tot_anz:Decimal = to_decimal("0.0")
        tot_val:Decimal = to_decimal("0.0")
        tot_val1:Decimal = to_decimal("0.0")
        tot_val2:Decimal = to_decimal("0.0")
        zwkum:int = 0
        bezeich:string = ""
        l_oh = None
        qty:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        L_oh =  create_buffer("L_oh",Mathis)
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_val =  to_decimal("0")
        tot_val1 =  to_decimal("0")
        tot_val2 =  to_decimal("0")

        fa_grup = get_cache (Fa_grup, {"gnr": [(eq, from_grp)],"flag": [(eq, 0)]})

        for lagerbuff in query(lagerbuff_list, filters=(lambda lagerbuff: lagerbuff.lagerBuff.lager_nr >= from_lager and lagerBuff.lager_nr <= to_lager)):
            i = 0
            zwkum = 0
            t_anz =  to_decimal("0")
            t_val =  to_decimal("0")
            t_val1 =  to_decimal("0")
            t_val2 =  to_decimal("0")
            tt_anz =  to_decimal("0")
            tt_val =  to_decimal("0")
            tt_val1 =  to_decimal("0")
            tt_val2 =  to_decimal("0")
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.s = to_string(lagerBuff.lager_nr, ">>99") + "-" + to_string(lagerBuff.bezeich, "x(24)")

            if mi_bookvalue_chk :

                mathis_obj_list = {}
                mathis = Mathis()
                fa_artikel = Fa_artikel()
                for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel.katnr, fa_artikel._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel.katnr, Fa_artikel._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0) & (Fa_artikel.gnr == from_grp)).filter(
                         (Mathis.location == lagerBuff.bezeich) & (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Mathis.name).all():
                    if mathis_obj_list.get(mathis._recid):
                        continue
                    else:
                        mathis_obj_list[mathis._recid] = True


                    do_it = False

                    if not zero_value_only:
                        do_it = True
                    else:
                        do_it = fa_artikel.book_wert == 0

                    if do_it:

                        if zwkum != fa_artikel.gnr:

                            if zwkum != 0:
                                str_list = Str_list()
                                str_list_list.append(str_list)

                                for j in range(1,28 + 1) :
                                    str_list.s = str_list.s + " "
                                str_list.refno = "SUB TOTAL"
                                str_list.s = str_list.s + to_string("SUB TOTAL", "x(22)")

                                if t_anz > 99999:
                                    str_list.s = str_list.s + to_string(t_anz, ">>>>>9")
                                else:
                                    str_list.s = str_list.s + to_string(t_anz, ">>,>>9")

                                if t_val > 99999999999 or t_val1 > 99999999999 or t_val2 > 99999999999:
                                    str_list.s = str_list.s + to_string(t_val, ">,>>>,>>>,>>>,>>9") + to_string(t_val1, ">,>>>,>>>,>>>,>>9") + to_string(t_val2, ">,>>>,>>>,>>>,>>9")
                                else:
                                    str_list.s = str_list.s + to_string(t_val, ">>,>>>,>>>,>>9.99") + to_string(t_val1, ">>,>>>,>>>,>>9.99") + to_string(t_val2, ">>,>>>,>>>,>>9.99")
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.s = to_string(fa_grup.bezeich, "x(28)")
                            t_anz =  to_decimal("0")
                            t_val =  to_decimal("0")
                            t_val1 =  to_decimal("0")
                            t_val2 =  to_decimal("0")
                            zwkum = fa_artikel.gnr


                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.refno = mathis.asset
                        str_list.s = to_string(mathis.name, "x(28)") + to_string(mathis.asset, "x(14)") + to_string(mathis.datum) + to_string(fa_artikel.anzahl, ">>,>>9")
                        val_dep =  to_decimal(fa_artikel.depn_wert) / to_decimal(fa_artikel.anz_depn)
                        sub_depn = 0
                        flag = False

                        if val_dep == None:
                            val_dep =  to_decimal("0")
                        for datum in date_range(from_date,to_date) :

                            if flag and datum == date_mdy(get_month(datum) + 1, 1, get_year(datum)) - 1:
                                sub_depn = sub_depn + 1

                            if datum == fa_artikel.first_depn:
                                sub_depn = sub_depn + 1
                                flag = True

                            if datum == fa_artikel.last_depn:
                                break
                        p_depn_wert =  to_decimal(val_dep) * to_decimal(sub_depn)
                        p_book_wert =  to_decimal(fa_artikel.warenwert) - to_decimal(p_depn_wert)


                        i = i + 1
                        t_anz =  to_decimal(t_anz) + to_decimal(fa_artikel.anzahl)
                        t_val =  to_decimal(t_val) + to_decimal(fa_artikel.warenwert)
                        t_val1 =  to_decimal(t_val1) + to_decimal(p_depn_wert)
                        t_val2 =  to_decimal(t_val2) + to_decimal(p_book_wert)
                        tt_anz =  to_decimal(tt_anz) + to_decimal(fa_artikel.anzahl)
                        tt_val =  to_decimal(tt_val) + to_decimal(fa_artikel.warenwert)
                        tt_val1 =  to_decimal(tt_val1) + to_decimal(p_depn_wert)
                        tt_val2 =  to_decimal(tt_val2) + to_decimal(p_book_wert)
                        tot_anz =  to_decimal(tot_anz) + to_decimal(fa_artikel.anzahl)
                        tot_val =  to_decimal(tot_val) + to_decimal(fa_artikel.warenwert)
                        tot_val1 =  to_decimal(tot_val1) + to_decimal(p_depn_wert)
                        tot_val2 =  to_decimal(tot_val2) + to_decimal(p_book_wert)
                        str_list.s = str_list.s + to_string(fa_artikel.warenwert, ">,>>>,>>>,>>>,>>9.99") + to_string(p_depn_wert, ">>>,>>>,>>>,>>9.99") + to_string(p_book_wert, ">>>,>>>,>>>,>>9.99")

                        if fa_artikel.first_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.first_depn)
                        else:
                            str_list.s = str_list.s + " "

                        if fa_artikel.next_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.next_depn)
                        else:
                            str_list.s = str_list.s + " "

                        if fa_artikel.last_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.last_depn)
                        else:
                            str_list.s = str_list.s + " "

                        if fa_artikel.anz_depn != None:
                            str_list.s = str_list.s + to_string(sub_depn)
                        else:
                            str_list.s = str_list.s + " "

                    if t_anz != 0:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        for j in range(1,28 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.refno = "SUB TOTAL"
                        str_list.s = str_list.s + to_string("SUB TOTAL", "x(22)")

                        if t_anz > 99999:
                            str_list.s = str_list.s + to_string(t_anz, ">>>>>9")
                        else:
                            str_list.s = str_list.s + to_string(t_anz, ">>,>>9")

                        if t_val > 99999999999 or t_val1 > 99999999999 or t_val2 > 99999999999:
                            str_list.s = str_list.s + to_string(t_val, ">,>>>,>>>,>>>,>>9") + to_string(t_val1, ">,>>>,>>>,>>>,>>9") + to_string(t_val2, ">,>>>,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(t_val, ">>,>>>,>>>,>>9.99") + to_string(t_val1, ">>,>>>,>>>,>>9.99") + to_string(t_val2, ">>,>>>,>>>,>>9.99")

                    if i > 0:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        for j in range(1,28 + 1) :
                            str_list.s = str_list.s + " "
                    str_list.refno = "T O T A L"
                    str_list.flag = 1
                    str_list.s = str_list.s + to_string("T O T A L", "x(22)")
                    str_list.s = str_list.s + to_string(tt_anz, ">>,>>9")
                    str_list.s = str_list.s + to_string(tt_val, ">>,>>>,>>>,>>9.99") + to_string(tt_val1, ">>,>>>,>>>,>>9.99") + to_string(tt_val2, ">>,>>>,>>>,>>9.99")
            else:

                mathis_obj_list = {}
                mathis = Mathis()
                fa_artikel = Fa_artikel()
                for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel.katnr, fa_artikel._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel.katnr, Fa_artikel._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0) & (Fa_artikel.gnr == from_grp)).filter(
                         (Mathis.location == lagerBuff.bezeich) & (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Mathis.name).all():
                    if mathis_obj_list.get(mathis._recid):
                        continue
                    else:
                        mathis_obj_list[mathis._recid] = True


                    do_it = False

                    if not zero_value_only:
                        do_it = True
                    else:
                        do_it = fa_artikel.book_wert == 0

                    if do_it:

                        if zwkum != fa_artikel.gnr:

                            if zwkum != 0:
                                str_list = Str_list()
                                str_list_list.append(str_list)

                                for j in range(1,28 + 1) :
                                    str_list.s = str_list.s + " "
                                str_list.refno = "SUB TOTAL"
                                str_list.s = str_list.s + to_string("SUB TOTAL", "x(22)")

                                if t_anz > 99999:
                                    str_list.s = str_list.s + to_string(t_anz, ">>>>>9")
                                else:
                                    str_list.s = str_list.s + to_string(t_anz, ">>,>>9")

                                if t_val > 99999999999 or t_val1 > 99999999999 or t_val2 > 99999999999:
                                    str_list.s = str_list.s + to_string(t_val, ">,>>>,>>>,>>>,>>9") + to_string(t_val1, ">,>>>,>>>,>>>,>>9") + to_string(t_val2, ">,>>>,>>>,>>>,>>9")
                                else:
                                    str_list.s = str_list.s + to_string(t_val, ">>,>>>,>>>,>>9.99") + to_string(t_val1, ">>,>>>,>>>,>>9.99") + to_string(t_val2, ">>,>>>,>>>,>>9.99")
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.s = to_string(fa_grup.bezeich, "x(28)")
                            t_anz =  to_decimal("0")
                            t_val =  to_decimal("0")
                            t_val1 =  to_decimal("0")
                            t_val2 =  to_decimal("0")
                            zwkum = fa_artikel.gnr


                        i = i + 1
                        t_anz =  to_decimal(t_anz) + to_decimal(fa_artikel.anzahl)
                        t_val =  to_decimal(t_val) + to_decimal(fa_artikel.warenwert)
                        t_val1 =  to_decimal(t_val1) + to_decimal(fa_artikel.depn_wert)
                        t_val2 =  to_decimal(t_val2) + to_decimal(fa_artikel.book_wert)
                        tt_anz =  to_decimal(tt_anz) + to_decimal(fa_artikel.anzahl)
                        tt_val =  to_decimal(tt_val) + to_decimal(fa_artikel.warenwert)
                        tt_val1 =  to_decimal(tt_val1) + to_decimal(fa_artikel.depn_wert)
                        tt_val2 =  to_decimal(tt_val2) + to_decimal(fa_artikel.book_wert)
                        tot_anz =  to_decimal(tot_anz) + to_decimal(fa_artikel.anzahl)
                        tot_val =  to_decimal(tot_val) + to_decimal(fa_artikel.warenwert)
                        tot_val1 =  to_decimal(tot_val1) + to_decimal(fa_artikel.depn_wert)
                        tot_val2 =  to_decimal(tot_val2) + to_decimal(fa_artikel.book_wert)
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.refno = mathis.asset
                        str_list.s = to_string(mathis.name, "x(28)") + to_string(mathis.asset, "x(14)") + to_string(mathis.datum) + to_string(fa_artikel.anzahl, ">>,>>9")
                        str_list.s = str_list.s + to_string(fa_artikel.warenwert, ">,>>>,>>>,>>>,>>9.99") + to_string(fa_artikel.depn_wert, ">>,>>>,>>>,>>9.99") + to_string(fa_artikel.book_wert, ">>,>>>,>>>,>>9.99")

                        if fa_artikel.first_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.first_depn)
                        else:
                            str_list.s = str_list.s + " "

                        if fa_artikel.next_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.next_depn)
                        else:
                            str_list.s = str_list.s + " "

                        if fa_artikel.last_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.last_depn)
                        else:
                            str_list.s = str_list.s + " "

                        if fa_artikel.anz_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.anz_depn)
                        else:
                            str_list.s = str_list.s + " "

                    if t_anz != 0:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        for j in range(1,28 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.refno = "SUB TOTAL"
                        str_list.s = str_list.s + to_string("SUB TOTAL", "x(22)")

                        if t_anz > 99999:
                            str_list.s = str_list.s + to_string(t_anz, ">>>>>9")
                        else:
                            str_list.s = str_list.s + to_string(t_anz, ">>,>>9")

                        if t_val > 99999999999 or t_val1 > 99999999999 or t_val2 > 99999999999:
                            str_list.s = str_list.s + to_string(t_val, ">,>>>,>>>,>>>,>>9") + to_string(t_val1, ">,>>>,>>>,>>>,>>9") + to_string(t_val2, ">,>>>,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(t_val, ">>,>>>,>>>,>>9.99") + to_string(t_val1, ">>,>>>,>>>,>>9.99") + to_string(t_val2, ">>,>>>,>>>,>>9.99")

                    if i > 0:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        for j in range(1,28 + 1) :
                            str_list.s = str_list.s + " "
                    str_list.refno = "T O T A L"
                    str_list.flag = 1
                    str_list.s = str_list.s + to_string("T O T A L", "x(22)")
                    str_list.s = str_list.s + to_string(tt_anz, ">>,>>9")
                    str_list.s = str_list.s + to_string(tt_val, ">>,>>>,>>>,>>9.99") + to_string(tt_val1, ">>,>>>,>>>,>>9.99") + to_string(tt_val2, ">>,>>>,>>>,>>9.99")

        if from_lager != to_lager and tot_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list = Str_list()
            str_list_list.append(str_list)

            for j in range(1,28 + 1) :
                str_list.s = str_list.s + " "
            str_list.flag = 2
            str_list.refno = "GRAND TOTAL"

            if length(trim(to_string(str_list.s))) != 0:
                str_list.s = str_list.s + to_string(" ", "x(21)")
            else:
                str_list.s = str_list.s + to_string(" ", "x(22)")

            if length(trim(to_string(tot_anz))) > 6:
                str_list.s = str_list.s + to_string(tot_anz, ">>>>>9")
            else:
                str_list.s = str_list.s + to_string(tot_anz, ">>,>>9")

            if tot_val > 99999999999 or tot_val1 > 99999999999 or tot_val2 > 99999999999:
                str_list.s = str_list.s + to_string(tot_val, ">,>>>,>>>,>>>,>>9") + to_string(tot_val1, ">,>>>,>>>,>>>,>>9") + to_string(tot_val2, ">,>>>,>>>,>>>,>>9")
            else:
                str_list.s = str_list.s + to_string(tot_val, ">>,>>>,>>>,>>9.99") + to_string(tot_val1, ">>,>>>,>>>,>>9.99") + to_string(tot_val2, ">>,>>>,>>>,>>9.99")


    def create_list11():

        nonlocal str_list_list, do_it, sub_depn, val_dep, datum, flag, p_depn_wert, p_book_wert, lvcarea, fa_lager, mathis, fa_artikel, fa_grup, gl_acct, fa_kateg, htparam
        nonlocal pvilanguage, mi_lager_chk, mi_subgrp_chk, mi_acct_chk, mi_bookvalue_chk, from_grp, from_date, to_lager, from_lager, maxnr, to_date, zero_value_only, last_acctdate, yy, mm, from_subgr, to_subgr


        nonlocal lagerbuff, str_list
        nonlocal str_list_list

        i:int = 0
        j:int = 0
        t_anz:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        t_val1:Decimal = to_decimal("0.0")
        t_val2:Decimal = to_decimal("0.0")
        tt_anz:Decimal = to_decimal("0.0")
        tt_val:Decimal = to_decimal("0.0")
        tt_val1:Decimal = to_decimal("0.0")
        tt_val2:Decimal = to_decimal("0.0")
        tot_anz:Decimal = to_decimal("0.0")
        tot_val:Decimal = to_decimal("0.0")
        tot_val1:Decimal = to_decimal("0.0")
        tot_val2:Decimal = to_decimal("0.0")
        zwkum:int = 0
        bezeich:string = ""
        l_oh = None
        qty:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        L_oh =  create_buffer("L_oh",Mathis)
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_val =  to_decimal("0")
        tot_val1 =  to_decimal("0")
        tot_val2 =  to_decimal("0")

        fa_grup = get_cache (Fa_grup, {"gnr": [(eq, from_grp)],"flag": [(eq, 0)]})

        for lagerbuff in query(lagerbuff_list, filters=(lambda lagerbuff: lagerbuff.lagerBuff.lager_nr >= from_lager and lagerBuff.lager_nr <= to_lager)):
            i = 0
            zwkum = 0
            t_anz =  to_decimal("0")
            t_val =  to_decimal("0")
            t_val1 =  to_decimal("0")
            t_val2 =  to_decimal("0")
            tt_anz =  to_decimal("0")
            tt_val =  to_decimal("0")
            tt_val1 =  to_decimal("0")
            tt_val2 =  to_decimal("0")
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.s = to_string(lagerBuff.lager_nr, ">>99") + "-" + to_string(lagerBuff.bezeich, "x(24)")

            if mi_bookvalue_chk :

                mathis_obj_list = {}
                mathis = Mathis()
                fa_artikel = Fa_artikel()
                for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel.katnr, fa_artikel._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel.katnr, Fa_artikel._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0) & (Fa_artikel.gnr == from_grp)).filter(
                         (Mathis.location == lagerBuff.bezeich) & (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Mathis.name).all():
                    if mathis_obj_list.get(mathis._recid):
                        continue
                    else:
                        mathis_obj_list[mathis._recid] = True


                    do_it = False

                    if not zero_value_only:
                        do_it = True
                    else:
                        do_it = fa_artikel.book_wert == 0

                    if do_it:

                        if zwkum != fa_artikel.gnr:

                            if zwkum != 0:
                                str_list = Str_list()
                                str_list_list.append(str_list)

                                for j in range(1,28 + 1) :
                                    str_list.s = str_list.s + " "
                                str_list.refno = "SUB TOTAL"
                                str_list.s = str_list.s + to_string("SUB TOTAL", "x(22)")

                                if t_anz > 99999:
                                    str_list.s = str_list.s + to_string(t_anz, ">>>>>9")
                                else:
                                    str_list.s = str_list.s + to_string(t_anz, ">>,>>9")

                                if t_val > 99999999999 or t_val1 > 99999999999 or t_val2 > 99999999999:
                                    str_list.s = str_list.s + to_string(t_val, ">,>>>,>>>,>>>,>>9") + to_string(t_val1, ">,>>>,>>>,>>>,>>9") + to_string(t_val2, ">,>>>,>>>,>>>,>>9")
                                else:
                                    str_list.s = str_list.s + to_string(t_val, ">>>,>>>,>>>,>>9.99") + to_string(t_val1, ">>>,>>>,>>>,>>9.99") + to_string(t_val2, ">>>,>>>,>>>,>>9.99")
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.s = to_string(fa_grup.bezeich, "x(28)")
                            t_anz =  to_decimal("0")
                            t_val =  to_decimal("0")
                            t_val1 =  to_decimal("0")
                            t_val2 =  to_decimal("0")
                            zwkum = fa_artikel.gnr


                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.refno = mathis.asset
                        str_list.s = to_string(mathis.name, "x(28)") + to_string(mathis.asset, "x(14)") + to_string(mathis.datum) + to_string(fa_artikel.anzahl, ">>,>>9")
                        val_dep =  to_decimal(fa_artikel.depn_wert) / to_decimal(fa_artikel.anz_depn)
                        sub_depn = 0
                        flag = False

                        if val_dep == None:
                            val_dep =  to_decimal("0")
                        for datum in date_range(from_date,to_date) :

                            if flag and datum == date_mdy(get_month(datum) + 1, 1, get_year(datum)) - 1:
                                sub_depn = sub_depn + 1

                            if datum == fa_artikel.first_depn:
                                sub_depn = sub_depn + 1
                                flag = True

                            if datum == fa_artikel.last_depn:
                                break
                        p_depn_wert =  to_decimal(val_dep) * to_decimal(sub_depn)
                        p_book_wert =  to_decimal(fa_artikel.warenwert) - to_decimal(p_depn_wert)


                        i = i + 1
                        t_anz =  to_decimal(t_anz) + to_decimal(fa_artikel.anzahl)
                        t_val =  to_decimal(t_val) + to_decimal(fa_artikel.warenwert)
                        t_val1 =  to_decimal(t_val1) + to_decimal(p_depn_wert)
                        t_val2 =  to_decimal(t_val2) + to_decimal(p_book_wert)
                        tt_anz =  to_decimal(tt_anz) + to_decimal(fa_artikel.anzahl)
                        tt_val =  to_decimal(tt_val) + to_decimal(fa_artikel.warenwert)
                        tt_val1 =  to_decimal(tt_val1) + to_decimal(p_depn_wert)
                        tt_val2 =  to_decimal(tt_val2) + to_decimal(p_book_wert)
                        tot_anz =  to_decimal(tot_anz) + to_decimal(fa_artikel.anzahl)
                        tot_val =  to_decimal(tot_val) + to_decimal(fa_artikel.warenwert)
                        tot_val1 =  to_decimal(tot_val1) + to_decimal(p_depn_wert)
                        tot_val2 =  to_decimal(tot_val2) + to_decimal(p_book_wert)
                        str_list.s = str_list.s + to_string(fa_artikel.warenwert, ">,>>>,>>>,>>>,>>9.99") + to_string(p_depn_wert, ">>>,>>>,>>>,>>9.99") + to_string(p_book_wert, ">>>,>>>,>>>,>>9.99")

                        if fa_artikel.first_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.first_depn)
                        else:
                            str_list.s = str_list.s + " "

                        if fa_artikel.next_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.next_depn)
                        else:
                            str_list.s = str_list.s + " "

                        if fa_artikel.last_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.last_depn)
                        else:
                            str_list.s = str_list.s + " "

                        if fa_artikel.anz_depn != None:
                            str_list.s = str_list.s + to_string(sub_depn)
                        else:
                            str_list.s = str_list.s + " "

                    if t_anz != 0:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        for j in range(1,28 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.refno = "SUB TOTAL"
                        str_list.s = str_list.s + to_string("SUB TOTAL", "x(22)")

                        if t_anz > 99999:
                            str_list.s = str_list.s + to_string(t_anz, ">>>>>9")
                        else:
                            str_list.s = str_list.s + to_string(t_anz, ">>,>>9")

                        if t_val > 99999999999 or t_val1 > 99999999999 or t_val2 > 99999999999:
                            str_list.s = str_list.s + to_string(t_val, ">,>>>,>>>,>>>,>>9") + to_string(t_val1, ">,>>>,>>>,>>>,>>9") + to_string(t_val2, ">,>>>,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(t_val, ">>>,>>>,>>>,>>9.99") + to_string(t_val1, ">>>,>>>,>>>,>>9.99") + to_string(t_val2, ">>>,>>>,>>>,>>9.99")

                    if i > 0:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        for j in range(1,28 + 1) :
                            str_list.s = str_list.s + " "
                    str_list.refno = "T O T A L"
                    str_list.flag = 1
                    str_list.s = str_list.s + to_string("T O T A L", "x(22)")
                    str_list.s = str_list.s + to_string(tt_anz, ">>,>>9")
                    str_list.s = str_list.s + to_string(tt_val, ">>>,>>>,>>>,>>9.99") + to_string(tt_val1, ">>>,>>>,>>>,>>9.99") + to_string(tt_val2, ">>>,>>>,>>>,>>9.99")
            else:

                mathis_obj_list = {}
                mathis = Mathis()
                fa_artikel = Fa_artikel()
                for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel.katnr, fa_artikel._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel.katnr, Fa_artikel._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0) & (Fa_artikel.gnr == from_grp)).filter(
                         (Mathis.location == lagerBuff.bezeich) & (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Mathis.name).all():
                    if mathis_obj_list.get(mathis._recid):
                        continue
                    else:
                        mathis_obj_list[mathis._recid] = True


                    do_it = False

                    if not zero_value_only:
                        do_it = True
                    else:
                        do_it = fa_artikel.book_wert == 0

                    if do_it:

                        if zwkum != fa_artikel.gnr:

                            if zwkum != 0:
                                str_list = Str_list()
                                str_list_list.append(str_list)

                                for j in range(1,28 + 1) :
                                    str_list.s = str_list.s + " "
                                str_list.refno = "SUB TOTAL"
                                str_list.s = str_list.s + to_string("SUB TOTAL", "x(22)")

                                if t_anz > 99999:
                                    str_list.s = str_list.s + to_string(t_anz, ">>>>>9")
                                else:
                                    str_list.s = str_list.s + to_string(t_anz, ">>,>>9")

                                if t_val > 99999999999 or t_val1 > 99999999999 or t_val2 > 99999999999:
                                    str_list.s = str_list.s + to_string(t_val, ">,>>>,>>>,>>>,>>9") + to_string(t_val1, ">,>>>,>>>,>>>,>>9") + to_string(t_val2, ">,>>>,>>>,>>>,>>9")
                                else:
                                    str_list.s = str_list.s + to_string(t_val, ">>>,>>>,>>>,>>9.99") + to_string(t_val1, ">>>,>>>,>>>,>>9.99") + to_string(t_val2, ">>>,>>>,>>>,>>9.99")
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.s = to_string(fa_grup.bezeich, "x(28)")
                            t_anz =  to_decimal("0")
                            t_val =  to_decimal("0")
                            t_val1 =  to_decimal("0")
                            t_val2 =  to_decimal("0")
                            zwkum = fa_artikel.gnr


                        i = i + 1
                        t_anz =  to_decimal(t_anz) + to_decimal(fa_artikel.anzahl)
                        t_val =  to_decimal(t_val) + to_decimal(fa_artikel.warenwert)
                        t_val1 =  to_decimal(t_val1) + to_decimal(fa_artikel.depn_wert)
                        t_val2 =  to_decimal(t_val2) + to_decimal(fa_artikel.book_wert)
                        tt_anz =  to_decimal(tt_anz) + to_decimal(fa_artikel.anzahl)
                        tt_val =  to_decimal(tt_val) + to_decimal(fa_artikel.warenwert)
                        tt_val1 =  to_decimal(tt_val1) + to_decimal(fa_artikel.depn_wert)
                        tt_val2 =  to_decimal(tt_val2) + to_decimal(fa_artikel.book_wert)
                        tot_anz =  to_decimal(tot_anz) + to_decimal(fa_artikel.anzahl)
                        tot_val =  to_decimal(tot_val) + to_decimal(fa_artikel.warenwert)
                        tot_val1 =  to_decimal(tot_val1) + to_decimal(fa_artikel.depn_wert)
                        tot_val2 =  to_decimal(tot_val2) + to_decimal(fa_artikel.book_wert)
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.refno = mathis.asset
                        str_list.s = to_string(mathis.name, "x(28)") + to_string(mathis.asset, "x(14)") + to_string(mathis.datum) + to_string(fa_artikel.anzahl, ">>,>>9")
                        str_list.s = str_list.s + to_string(fa_artikel.warenwert, ">,>>>,>>>,>>>,>>9.99") + to_string(fa_artikel.depn_wert, ">>>,>>>,>>>,>>9.99") + to_string(fa_artikel.book_wert, ">>>,>>>,>>>,>>9.99")

                        if fa_artikel.first_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.first_depn)
                        else:
                            str_list.s = str_list.s + " "

                        if fa_artikel.next_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.next_depn)
                        else:
                            str_list.s = str_list.s + " "

                        if fa_artikel.last_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.last_depn)
                        else:
                            str_list.s = str_list.s + " "

                        if fa_artikel.anz_depn != None:
                            str_list.s = str_list.s + to_string(fa_artikel.anz_depn)
                        else:
                            str_list.s = str_list.s + " "

                    if t_anz != 0:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        for j in range(1,28 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.refno = "SUB TOTAL"
                        str_list.s = str_list.s + to_string("SUB TOTAL", "x(22)")

                        if t_anz > 99999:
                            str_list.s = str_list.s + to_string(t_anz, ">>>>>9")
                        else:
                            str_list.s = str_list.s + to_string(t_anz, ">>,>>9")

                        if t_val > 99999999999 or t_val1 > 99999999999 or t_val2 > 99999999999:
                            str_list.s = str_list.s + to_string(t_val, ">,>>>,>>>,>>>,>>9") + to_string(t_val1, ">,>>>,>>>,>>>,>>9") + to_string(t_val2, ">,>>>,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(t_val, ">>>,>>>,>>>,>>9.99") + to_string(t_val1, ">>>,>>>,>>>,>>9.99") + to_string(t_val2, ">>>,>>>,>>>,>>9.99")

                    if i > 0:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        for j in range(1,28 + 1) :
                            str_list.s = str_list.s + " "
                    str_list.refno = "T O T A L"
                    str_list.flag = 1
                    str_list.s = str_list.s + to_string("T O T A L", "x(22)")
                    str_list.s = str_list.s + to_string(tt_anz, ">>,>>9")
                    str_list.s = str_list.s + to_string(tt_val, ">>>,>>>,>>>,>>9.99") + to_string(tt_val1, ">>>,>>>,>>>,>>9.99") + to_string(tt_val2, ">>>,>>>,>>>,>>9.99")

        if from_lager != to_lager and tot_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list = Str_list()
            str_list_list.append(str_list)

            for j in range(1,28 + 1) :
                str_list.s = str_list.s + " "
            str_list.flag = 2
            str_list.refno = "GRAND TOTAL"

            if length(trim(to_string(str_list.s))) != 0:
                str_list.s = str_list.s + to_string(" ", "x(21)")
            else:
                str_list.s = str_list.s + to_string(" ", "x(22)")

            if length(trim(to_string(tot_anz))) > 6:
                str_list.s = str_list.s + to_string(tot_anz, ">>>>>9")
            else:
                str_list.s = str_list.s + to_string(tot_anz, ">>,>>9")

            if tot_val > 99999999999 or tot_val1 > 99999999999 or tot_val2 > 99999999999:
                str_list.s = str_list.s + to_string(tot_val, ">,>>>,>>>,>>>,>>9") + to_string(tot_val1, ">,>>>,>>>,>>>,>>9") + to_string(tot_val2, ">,>>>,>>>,>>>,>>9")
            else:
                str_list.s = str_list.s + to_string(tot_val, ">>>,>>>,>>>,>>9.99") + to_string(tot_val1, ">>>,>>>,>>>,>>9.99") + to_string(tot_val2, ">>>,>>>,>>>,>>9.99")


    def create_listsgrp():

        nonlocal str_list_list, do_it, sub_depn, val_dep, datum, flag, p_depn_wert, p_book_wert, lvcarea, fa_lager, mathis, fa_artikel, fa_grup, gl_acct, fa_kateg, htparam
        nonlocal pvilanguage, mi_lager_chk, mi_subgrp_chk, mi_acct_chk, mi_bookvalue_chk, from_grp, from_date, to_lager, from_lager, maxnr, to_date, zero_value_only, last_acctdate, yy, mm, from_subgr, to_subgr


        nonlocal lagerbuff, str_list
        nonlocal str_list_list

        i:int = 0
        j:int = 0
        t_anz:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        t_val1:Decimal = to_decimal("0.0")
        t_val2:Decimal = to_decimal("0.0")
        tot_anz:Decimal = to_decimal("0.0")
        tot_val:Decimal = to_decimal("0.0")
        tot_val1:Decimal = to_decimal("0.0")
        tot_val2:Decimal = to_decimal("0.0")
        zwkum:int = 0
        bezeich:string = ""
        l_oh = None
        qty:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        diff_n:int = 0
        diff_wert:Decimal = to_decimal("0.0")
        L_oh =  create_buffer("L_oh",Mathis)
        str_list_list.clear()
        diff_n = (get_year(last_acctdate) - yy) * 12 + get_month(last_acctdate) - mm
        tot_anz =  to_decimal("0")
        tot_val =  to_decimal("0")
        tot_val1 =  to_decimal("0")
        tot_val2 =  to_decimal("0")
        i = 0
        zwkum = 0
        t_anz =  to_decimal("0")
        t_val =  to_decimal("0")
        t_val1 =  to_decimal("0")
        t_val2 =  to_decimal("0")

        if mi_bookvalue_chk :

            mathis_obj_list = {}
            mathis = Mathis()
            fa_artikel = Fa_artikel()
            fa_grup = Fa_grup()
            for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel.katnr, fa_artikel._recid, fa_grup.bezeich, fa_grup._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel.katnr, Fa_artikel._recid, Fa_grup.bezeich, Fa_grup._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1) & (Fa_grup.gnr >= from_subgr) & (Fa_grup.gnr <= to_subgr)).filter(
                         (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Fa_artikel.subgrp, Mathis.name).all():
                if mathis_obj_list.get(mathis._recid):
                    continue
                else:
                    mathis_obj_list[mathis._recid] = True

                if zwkum != fa_artikel.subgrp:

                    if zwkum != 0:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        for j in range(1,38 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.refno = "SUB TOTAL"
                        str_list.flag = 1
                        str_list.s = str_list.s + to_string("SUB TOTAL", "x(55)") + " "

                        if t_anz > 99999:
                            str_list.s = str_list.s + to_string(t_anz, ">>>>>9")
                        else:
                            str_list.s = str_list.s + to_string(t_anz, ">>,>>9")

                        if t_val > 99999999999 or t_val1 > 99999999999 or t_val2 > 99999999999:
                            str_list.s = str_list.s + to_string(t_val, ">,>>>,>>>,>>>,>>9") + to_string(t_val1, ">,>>>,>>>,>>>,>>9") + to_string(t_val2, ">,>>>,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(t_val, ">>,>>>,>>>,>>9.99") + to_string(t_val1, ">>,>>>,>>>,>>9.99") + to_string(t_val2, ">>,>>>,>>>,>>9.99")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.s = to_string(fa_grup.bezeich, "x(28)")
                    t_anz =  to_decimal("0")
                    t_val =  to_decimal("0")
                    t_val1 =  to_decimal("0")
                    t_val2 =  to_decimal("0")
                    zwkum = fa_artikel.subgrp


                str_list = Str_list()
                str_list_list.append(str_list)

                str_list.refno = mathis.asset
                str_list.location = trim (mathis.location)
                str_list.s = to_string(mathis.name, "x(38)") +\
                        to_string(mathis.asset, "x(14)") +\
                        to_string(mathis.datum) +\
                        to_string(fa_artikel.anzahl, ">>,>>9")


                val_dep =  to_decimal(fa_artikel.depn_wert) / to_decimal(fa_artikel.anz_depn)
                sub_depn = 0
                flag = False

                if val_dep == None:
                    val_dep =  to_decimal("0")
                for datum in date_range(from_date,to_date) :

                    if flag and datum == date_mdy(get_month(datum) + 1, 1, get_year(datum)) - 1:
                        sub_depn = sub_depn + 1

                    if datum == fa_artikel.first_depn:
                        sub_depn = sub_depn + 1
                        flag = True

                    if datum == fa_artikel.last_depn:
                        break
                p_depn_wert =  to_decimal(val_dep) * to_decimal(sub_depn)
                p_book_wert =  to_decimal(fa_artikel.warenwert) - to_decimal(p_depn_wert)


                i = i + 1
                t_anz =  to_decimal(t_anz) + to_decimal(fa_artikel.anzahl)
                t_val =  to_decimal(t_val) + to_decimal(fa_artikel.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(fa_artikel.anzahl)
                tot_val =  to_decimal(tot_val) + to_decimal(fa_artikel.warenwert)

                if (fa_artikel.anz_depn - diff_n) == 0:
                    t_val2 =  to_decimal(t_val2) + to_decimal(fa_artikel.warenwert)
                    tot_val2 =  to_decimal(tot_val2) + to_decimal(fa_artikel.warenwert)
                else:
                    diff_wert = ( to_decimal(p_depn_wert) / to_decimal(sub_depn)) * to_decimal(diff_n)

                    if diff_wert == None:
                        diff_wert =  to_decimal("0")
                    t_val1 =  to_decimal(t_val1) + to_decimal(p_depn_wert) - to_decimal(diff_wert)
                    t_val2 =  to_decimal(t_val2) + to_decimal(p_book_wert) + to_decimal(diff_wert)
                    tot_val1 =  to_decimal(tot_val1) + to_decimal(p_depn_wert) - to_decimal(diff_wert)
                    tot_val2 =  to_decimal(tot_val2) + to_decimal(p_book_wert) + to_decimal(diff_wert)

                if (fa_artikel.anz_depn - diff_n) == 0:
                    str_list.s = str_list.s + to_string(fa_artikel.warenwert, ">,>>>,>>>,>>>,>>9.99") + to_string(0, ">>,>>>,>>>,>>9.99") + to_string(fa_artikel.warenwert, ">,>>>,>>>,>>>,>>9.99")
                else:
                    str_list.s = str_list.s + to_string(fa_artikel.warenwert, ">,>>>,>>>,>>>,>>9.99") + to_string(p_depn_wert - diff_wert, ">>>,>>>,>>>,>>9.99") + to_string(p_book_wert + diff_wert, ">>>,>>>,>>>,>>9.99")

                if fa_artikel.first_depn != None:
                    str_list.s = str_list.s + to_string(fa_artikel.first_depn)
                else:
                    str_list.s = str_list.s + " "

                if fa_artikel.next_depn != None:
                    str_list.s = str_list.s + to_string(fa_artikel.next_depn)
                else:
                    str_list.s = str_list.s + " "

                if fa_artikel.last_depn != None:
                    str_list.s = str_list.s + to_string(fa_artikel.last_depn)
                else:
                    str_list.s = str_list.s + " "

                if fa_artikel.anz_depn != None:
                    str_list.s = str_list.s + to_string(sub_depn)
                else:
                    str_list.s = str_list.s + " "

            if t_anz != 0:
                str_list = Str_list()
                str_list_list.append(str_list)

                for j in range(1,38 + 1) :
                    str_list.s = str_list.s + " "
                str_list.refno = "SUB TOTAL"
                str_list.flag = 1
                str_list.s = str_list.s + to_string("SUB TOTAL", "x(24)")

                if t_anz > 99999:
                    str_list.s = str_list.s + to_string(t_anz, ">>>>>9")
                else:
                    str_list.s = str_list.s + to_string(t_anz, ">>,>>9")

                if t_val > 99999999999 or t_val1 > 99999999999 or t_val2 > 99999999999:
                    str_list.s = str_list.s + to_string(t_val, ">,>>>,>>>,>>>,>>9") + to_string(t_val1, ">,>>>,>>>,>>>,>>9") + to_string(t_val2, ">,>>>,>>>,>>>,>>9")
                else:
                    str_list.s = str_list.s + to_string(t_val, ">>,>>>,>>>,>>9.99") + to_string(t_val1, ">>,>>>,>>>,>>9.99") + to_string(t_val2, ">>,>>>,>>>,>>9.99")
        else:

            mathis_obj_list = {}
            mathis = Mathis()
            fa_artikel = Fa_artikel()
            fa_grup = Fa_grup()
            for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel.katnr, fa_artikel._recid, fa_grup.bezeich, fa_grup._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel.katnr, Fa_artikel._recid, Fa_grup.bezeich, Fa_grup._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1) & (Fa_grup.gnr >= from_subgr) & (Fa_grup.gnr <= to_subgr)).filter(
                         (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Fa_artikel.subgrp, Mathis.name).all():
                if mathis_obj_list.get(mathis._recid):
                    continue
                else:
                    mathis_obj_list[mathis._recid] = True

                if zwkum != fa_artikel.subgrp:

                    if zwkum != 0:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        for j in range(1,38 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.refno = "SUB TOTAL"
                        str_list.flag = 1
                        str_list.s = str_list.s + to_string("SUB TOTAL", "x(23)")

                        if t_anz > 99999:
                            str_list.s = str_list.s + to_string(t_anz, ">>>9") + " "
                        else:
                            str_list.s = str_list.s + to_string(t_anz, ">,>>9") + " "

                        if t_val > 99999999999 or t_val1 > 99999999999 or t_val2 > 99999999999:
                            str_list.s = str_list.s + to_string(t_val, ">,>>>,>>>,>>>,>>9") + " " + to_string(t_val1, ">,>>>,>>>,>>>,>>9") + " " + to_string(t_val2, ">,>>>,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(t_val, ">>,>>>,>>>,>>9.99") + " " + to_string(t_val1, ">>,>>>,>>>,>>9.99") + " " + to_string(t_val2, ">>,>>>,>>>,>>9.99")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.s = to_string(fa_grup.bezeich, "x(28)")
                    t_anz =  to_decimal("0")
                    t_val =  to_decimal("0")
                    t_val1 =  to_decimal("0")
                    t_val2 =  to_decimal("0")
                    zwkum = fa_artikel.subgrp


                i = i + 1
                t_anz =  to_decimal(t_anz) + to_decimal(fa_artikel.anzahl)
                t_val =  to_decimal(t_val) + to_decimal(fa_artikel.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(fa_artikel.anzahl)
                tot_val =  to_decimal(tot_val) + to_decimal(fa_artikel.warenwert)

                if (fa_artikel.anz_depn - diff_n) == 0:
                    t_val2 =  to_decimal(t_val2) + to_decimal(fa_artikel.warenwert)
                    tot_val2 =  to_decimal(tot_val2) + to_decimal(fa_artikel.warenwert)
                else:
                    diff_wert = ( to_decimal(fa_artikel.depn_wert) / to_decimal(fa_artikel.anz_depn)) * to_decimal(diff_n)

                    if diff_wert == None:
                        diff_wert =  to_decimal("0")
                    t_val1 =  to_decimal(t_val1) + to_decimal(fa_artikel.depn_wert) - to_decimal(diff_wert)
                    t_val2 =  to_decimal(t_val2) + to_decimal(fa_artikel.book_wert) + to_decimal(diff_wert)
                    tot_val1 =  to_decimal(tot_val1) + to_decimal(fa_artikel.depn_wert) - to_decimal(diff_wert)
                    tot_val2 =  to_decimal(tot_val2) + to_decimal(fa_artikel.book_wert) + to_decimal(diff_wert)
                str_list = Str_list()
                str_list_list.append(str_list)

                str_list.refno = mathis.asset
                str_list.location = trim (mathis.location)
                str_list.s = to_string(mathis.name, "x(38)") +\
                        to_string(mathis.asset, "x(14)") +\
                        to_string(mathis.datum) +\
                        to_string(fa_artikel.anzahl, ">>,>>9")

                if (fa_artikel.anz_depn - diff_n) == 0:
                    str_list.s = str_list.s + to_string(fa_artikel.warenwert, ">,>>>,>>>,>>>,>>9.99") + to_string(0, ">>,>>>,>>>,>>9.99") + to_string(fa_artikel.warenwert, ">,>>>,>>>,>>>,>>9.99")
                else:
                    str_list.s = str_list.s + to_string(fa_artikel.warenwert, ">,>>>,>>>,>>>,>>9.99") + to_string(fa_artikel.depn_wert - diff_wert, ">>>,>>>,>>>,>>9.99") + to_string(fa_artikel.book_wert + diff_wert, ">>>,>>>,>>>,>>9.99")

                if fa_artikel.first_depn != None:
                    str_list.s = str_list.s + to_string(fa_artikel.first_depn)
                else:
                    str_list.s = str_list.s + " "

                if fa_artikel.next_depn != None:
                    str_list.s = str_list.s + to_string(fa_artikel.next_depn)
                else:
                    str_list.s = str_list.s + " "

                if fa_artikel.last_depn != None:
                    str_list.s = str_list.s + to_string(fa_artikel.last_depn)
                else:
                    str_list.s = str_list.s + " "

                if fa_artikel.anz_depn != None:
                    str_list.s = str_list.s + to_string(fa_artikel.anz_depn)
                else:
                    str_list.s = str_list.s + " "

            if t_anz != 0:
                str_list = Str_list()
                str_list_list.append(str_list)

                for j in range(1,38 + 1) :
                    str_list.s = str_list.s + " "
                str_list.refno = "SUB TOTAL"
                str_list.flag = 1
                str_list.s = str_list.s + to_string("SUB TOTAL", "x(23)")

                if t_anz > 99999:
                    str_list.s = str_list.s + to_string(t_anz, ">>>9") + " "
                else:
                    str_list.s = str_list.s + to_string(t_anz, ">,>>9") + " "

                if t_val > 99999999999 or t_val1 > 99999999999 or t_val2 > 99999999999:
                    str_list.s = str_list.s + to_string(t_val, ">,>>>,>>>,>>>,>>9") + " " + to_string(t_val1, ">,>>>,>>>,>>>,>>9") + " " + to_string(t_val2, ">,>>>,>>>,>>>,>>9")
                else:
                    str_list.s = str_list.s + to_string(t_val, ">>,>>>,>>>,>>9.99") + " " + to_string(t_val1, ">>,>>>,>>>,>>9.99") + " " + to_string(t_val2, ">>,>>>,>>>,>>9.99")

        if tot_anz != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list = Str_list()
            str_list_list.append(str_list)

            for j in range(1,38 + 1) :
                str_list.s = str_list.s + " "
            str_list.flag = 2
            str_list.refno = "GRAND TOTAL"

            if length(trim(to_string(str_list.s))) != 0:
                str_list.s = str_list.s + to_string(" ", "x(21)")
            else:
                str_list.s = str_list.s + to_string(" ", "x(22)")

            if length(trim(to_string(tot_anz))) > 6:
                str_list.s = str_list.s + to_string(tot_anz, ">>>>>9")
            else:
                str_list.s = str_list.s + to_string(tot_anz, ">>,>>9") + " "

            if tot_val > 99999999999 or tot_val1 > 99999999999 or tot_val2 > 99999999999:
                str_list.s = str_list.s + to_string(tot_val, ">,>>>,>>>,>>>,>>9") + " " + to_string(tot_val1, ">,>>>,>>>,>>>,>>9") + " " + to_string(tot_val2, ">,>>>,>>>,>>>,>>9")
            else:
                str_list.s = str_list.s + to_string(tot_val, ">>,>>>,>>>,>>9.99") + to_string(tot_val1, ">>,>>>,>>>,>>9.99") + to_string(tot_val2, ">>,>>>,>>>,>>9.99")


    def create_listacct():

        nonlocal str_list_list, do_it, sub_depn, val_dep, datum, flag, p_depn_wert, p_book_wert, lvcarea, fa_lager, mathis, fa_artikel, fa_grup, gl_acct, fa_kateg, htparam
        nonlocal pvilanguage, mi_lager_chk, mi_subgrp_chk, mi_acct_chk, mi_bookvalue_chk, from_grp, from_date, to_lager, from_lager, maxnr, to_date, zero_value_only, last_acctdate, yy, mm, from_subgr, to_subgr


        nonlocal lagerbuff, str_list
        nonlocal str_list_list

        curr_acct:string = ""
        fibu:string = ""
        diff_n:int = 0
        diff_wert:Decimal = to_decimal("0.0")
        t_oh:Decimal = to_decimal("0.0")
        t_depn:Decimal = to_decimal("0.0")
        tot_oh:Decimal = to_decimal("0.0")
        tot_depn:Decimal = to_decimal("0.0")
        t_book:Decimal = to_decimal("0.0")
        tot_book:Decimal = to_decimal("0.0")
        t_anz:Decimal = to_decimal("0.0")
        tot_anz:Decimal = to_decimal("0.0")
        str_list_list.clear()
        diff_n = (get_year(last_acctdate) - yy) * 12 + get_month(last_acctdate) - mm

        if mi_bookvalue_chk :

            mathis_obj_list = {}
            mathis = Mathis()
            fa_artikel = Fa_artikel()
            for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel.katnr, fa_artikel._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel.katnr, Fa_artikel._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).filter(
                     (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Fa_artikel.fibukonto).all():
                if mathis_obj_list.get(mathis._recid):
                    continue
                else:
                    mathis_obj_list[mathis._recid] = True

                if curr_acct != fa_artikel.fibukonto:
                    tot_anz =  to_decimal(tot_anz) + to_decimal(t_anz)
                    tot_oh =  to_decimal(tot_oh) + to_decimal(t_oh)
                    tot_depn =  to_decimal(tot_depn) + to_decimal(t_depn)
                    tot_book =  to_decimal(tot_book) + to_decimal(t_book)

                    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, curr_acct)]})

                    if gl_acct:
                        fibu = convert_fibu(curr_acct)

                    if curr_acct != "":
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.location = ""
                        str_list.s = to_string("SUBTOTAL ", "x(13)") +\
                                to_string(" ", "x(48)") +\
                                " " +\
                                to_string(t_anz, ">>,>>9") +\
                                to_string(t_oh, ">>>,>>>,>>>,>>9.99") +\
                                to_string(t_depn, ">>>,>>>,>>>,>>9.99") +\
                                to_string(t_book, " >>>,>>>,>>>,>>9.99")


                        str_list = Str_list()
                        str_list_list.append(str_list)

                    curr_acct = fa_artikel.fibukonto
                    t_anz =  to_decimal("0")
                    t_oh =  to_decimal("0")
                    t_depn =  to_decimal("0")
                    t_book =  to_decimal("0")

                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fa_artikel.fibukonto)]})
                fibu = convert_fibu(fa_artikel.fibukonto)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.substring(str_list.s, 0, 13) == (fibu).lower()), first=True)

                if str_list:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.refno = mathis.asset
                    str_list.location = trim (mathis.location)
                    str_list.s = to_string(" ", "x(13)") +\
                            to_string(mathis.name, "x(48)") +\
                            to_string(mathis.datum) +\
                            to_string(fa_artikel.anzahl, ">>,>>9")


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.refno = mathis.asset
                    str_list.location = trim (mathis.location)
                    str_list.s = to_string(fibu, "x(13)") +\
                            to_string(mathis.name, "x(48)") +\
                            to_string(mathis.datum) +\
                            to_string(fa_artikel.anzahl, ">>,>>9")


                val_dep =  to_decimal(fa_artikel.depn_wert) / to_decimal(fa_artikel.anz_depn)
                sub_depn = 0
                flag = False

                if val_dep == None:
                    val_dep =  to_decimal("0")
                for datum in date_range(from_date,to_date) :

                    if flag and datum == date_mdy(get_month(datum) + 1, 1, get_year(datum)) - 1:
                        sub_depn = sub_depn + 1

                    if datum == fa_artikel.first_depn:
                        sub_depn = sub_depn + 1
                        flag = True

                    if datum == fa_artikel.last_depn:
                        break
                p_depn_wert =  to_decimal(val_dep) * to_decimal(sub_depn)
                p_book_wert =  to_decimal(fa_artikel.warenwert) - to_decimal(p_depn_wert)

                if (fa_artikel.anz_depn - diff_n) == 0:
                    str_list.s = str_list.s + to_string(fa_artikel.warenwert, ">>>,>>>,>>>,>>9.99") + to_string(0, ">>>,>>>,>>>,>>9.99") + to_string(fa_artikel.warenwert, ">,>>>,>>>,>>>,>>9.99")
                else:
                    str_list.s = str_list.s + to_string(fa_artikel.warenwert, ">>>,>>>,>>>,>>9.99") + to_string(p_depn_wert - diff_wert, ">>>,>>>,>>>,>>9.99") + to_string(p_book_wert + diff_wert, " >>>,>>>,>>>,>>9.99")

                if fa_artikel.first_depn != None:
                    str_list.s = str_list.s + to_string(fa_artikel.first_depn)
                else:
                    str_list.s = str_list.s + " "

                if fa_artikel.next_depn != None:
                    str_list.s = str_list.s + to_string(fa_artikel.next_depn)
                else:
                    str_list.s = str_list.s + " "

                if fa_artikel.last_depn != None:
                    str_list.s = str_list.s + to_string(fa_artikel.last_depn)
                else:
                    str_list.s = str_list.s + " "

                if fa_artikel.anz_depn != None:
                    str_list.s = str_list.s + to_string(sub_depn)
                else:
                    str_list.s = str_list.s + " "

                if (fa_artikel.anz_depn - diff_n) == 0:
                    t_anz =  to_decimal(t_anz) + to_decimal(fa_artikel.anzahl)
                    t_oh =  to_decimal(t_oh) + to_decimal(fa_artikel.warenwert)
                    t_book =  to_decimal(t_book) + to_decimal(fa_artikel.book_wert)

                elif fa_artikel.anz_depn - diff_n > 0:

                    fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_artikel.katnr)]})

                    if (fa_kateg.methode == 0):
                        diff_wert = ( to_decimal(p_book_wert) / to_decimal(sub_depn)) * to_decimal(diff_n)

                        if diff_wert == None:
                            diff_wert =  to_decimal("0")
                        t_anz =  to_decimal(t_anz) + to_decimal(fa_artikel.anzahl)
                        t_oh =  to_decimal(t_oh) + to_decimal(fa_artikel.warenwert)
                        t_depn =  to_decimal(t_depn) + to_decimal(p_depn_wert) - to_decimal(diff_wert)
                        t_book =  to_decimal(t_book) + to_decimal(p_book_wert) + to_decimal(diff_wert)
        else:

            mathis_obj_list = {}
            mathis = Mathis()
            fa_artikel = Fa_artikel()
            for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel.katnr, fa_artikel._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel.katnr, Fa_artikel._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).filter(
                     (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Fa_artikel.fibukonto).all():
                if mathis_obj_list.get(mathis._recid):
                    continue
                else:
                    mathis_obj_list[mathis._recid] = True

                if curr_acct != fa_artikel.fibukonto:
                    tot_anz =  to_decimal(tot_anz) + to_decimal(t_anz)
                    tot_oh =  to_decimal(tot_oh) + to_decimal(t_oh)
                    tot_depn =  to_decimal(tot_depn) + to_decimal(t_depn)
                    tot_book =  to_decimal(tot_book) + to_decimal(t_book)

                    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, curr_acct)]})

                    if gl_acct:
                        fibu = convert_fibu(curr_acct)

                    if curr_acct != "":
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.location = ""
                        str_list.s = to_string("SUBTOTAL ", "x(13)") +\
                                to_string(" ", "x(48)") +\
                                " " +\
                                to_string(t_anz, ">>,>>9") +\
                                to_string(t_oh, ">>>,>>>,>>>,>>9.99") +\
                                to_string(t_depn, ">>>,>>>,>>>,>>9.99") +\
                                to_string(t_book, " >>>,>>>,>>>,>>9.99")


                        str_list = Str_list()
                        str_list_list.append(str_list)

                    curr_acct = fa_artikel.fibukonto
                    t_anz =  to_decimal("0")
                    t_oh =  to_decimal("0")
                    t_depn =  to_decimal("0")
                    t_book =  to_decimal("0")

                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fa_artikel.fibukonto)]})
                fibu = convert_fibu(fa_artikel.fibukonto)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.substring(str_list.s, 0, 13) == (fibu).lower()), first=True)

                if str_list:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.refno = mathis.asset
                    str_list.location = trim (mathis.location)
                    str_list.s = to_string(" ", "x(13)") +\
                            to_string(mathis.name, "x(48)") +\
                            to_string(mathis.datum) +\
                            to_string(fa_artikel.anzahl, ">>,>>9")


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.refno = mathis.asset
                    str_list.location = trim (mathis.location)
                    str_list.s = to_string(fibu, "x(13)") +\
                            to_string(mathis.name, "x(48)") +\
                            to_string(mathis.datum) +\
                            to_string(fa_artikel.anzahl, ">>,>>9")

                if (fa_artikel.anz_depn - diff_n) == 0:
                    str_list.s = str_list.s + to_string(fa_artikel.warenwert, ">>>,>>>,>>>,>>9.99") + to_string(0, ">>>,>>>,>>>,>>9.99") + to_string(fa_artikel.warenwert, ">,>>>,>>>,>>>,>>9.99")
                else:
                    str_list.s = str_list.s + to_string(fa_artikel.warenwert, ">>>,>>>,>>>,>>9.99") + to_string(fa_artikel.depn_wert - diff_wert, ">>>,>>>,>>>,>>9.99") + to_string(fa_artikel.book_wert + diff_wert, " >>>,>>>,>>>,>>9.99")

                if fa_artikel.first_depn != None:
                    str_list.s = str_list.s + to_string(fa_artikel.first_depn)
                else:
                    str_list.s = str_list.s + " "

                if fa_artikel.next_depn != None:
                    str_list.s = str_list.s + to_string(fa_artikel.next_depn)
                else:
                    str_list.s = str_list.s + " "

                if fa_artikel.last_depn != None:
                    str_list.s = str_list.s + to_string(fa_artikel.last_depn)
                else:
                    str_list.s = str_list.s + " "

                if fa_artikel.anz_depn != None:
                    str_list.s = str_list.s + to_string(fa_artikel.anz_depn)
                else:
                    str_list.s = str_list.s + " "
                t_anz =  to_decimal(t_anz) + to_decimal(fa_artikel.anzahl)
                t_oh =  to_decimal(t_oh) + to_decimal(fa_artikel.warenwert)

                if (fa_artikel.anz_depn - diff_n) == 0:
                    t_book =  to_decimal(t_book) + to_decimal(fa_artikel.book_wert)

                elif fa_artikel.anz_depn - diff_n > 0:

                    fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_artikel.katnr)]})

                    if (fa_kateg.methode == 0):
                        diff_wert = ( to_decimal(fa_artikel.depn_wert) / to_decimal(fa_artikel.anz_depn)) * to_decimal(diff_n)

                        if diff_wert == None:
                            diff_wert =  to_decimal("0")
                        t_depn =  to_decimal(t_depn) + to_decimal(fa_artikel.depn_wert) - to_decimal(diff_wert)
                        t_book =  to_decimal(t_book) + to_decimal(fa_artikel.book_wert) + to_decimal(diff_wert)
        tot_anz =  to_decimal(tot_anz) + to_decimal(t_anz)
        tot_oh =  to_decimal(tot_oh) + to_decimal(t_oh)
        tot_depn =  to_decimal(tot_depn) + to_decimal(t_depn)
        tot_book =  to_decimal(tot_book) + to_decimal(t_book)

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, curr_acct)]})
        fibu = convert_fibu(curr_acct)
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("SUBTOTAL ", "x(13)") +\
                to_string(gl_acct.bezeich, "x(48)") +\
                " " +\
                to_string(t_anz, ">>,>>9") +\
                to_string(t_oh, ">>>,>>>,>>>,>>9.99") +\
                to_string(t_depn, ">>>,>>>,>>>,>>9.99") +\
                to_string(t_book, " >>>,>>>,>>>,>>9.99")


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = to_string("", "x(13)") +\
                to_string(translateExtended ("T O T A L", lvcarea, "") , "x(48)") +\
                " " +\
                to_string(tot_anz, ">>,>>9")

        if length(trim(to_string(tot_oh, ">>>,>>>,>>>,>>9.99"))) > 18:
            str_list.s = str_list.s + to_string(tot_oh, ">>>,>>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_oh, ">>>,>>>,>>>,>>9.99")

        if length(trim(to_string(tot_depn, ">>>,>>>,>>>,>>9.99"))) > 18:
            str_list.s = str_list.s + to_string(tot_depn, ">>>,>>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_depn, ">>>,>>>,>>>,>>9.99")

        if length(trim(to_string(tot_book, ">>>,>>>,>>>,>>9.99"))) > 18:
            str_list.s = str_list.s + to_string(tot_book, " >>>,>>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_book, " >>>,>>>,>>>,>>9.99")


    def convert_fibu(konto:string):

        nonlocal str_list_list, do_it, sub_depn, val_dep, datum, flag, p_depn_wert, p_book_wert, lvcarea, fa_lager, mathis, fa_artikel, fa_grup, gl_acct, fa_kateg, htparam
        nonlocal pvilanguage, mi_lager_chk, mi_subgrp_chk, mi_acct_chk, mi_bookvalue_chk, from_grp, from_date, to_lager, from_lager, maxnr, to_date, zero_value_only, last_acctdate, yy, mm, from_subgr, to_subgr


        nonlocal lagerbuff, str_list
        nonlocal str_list_list

        s = ""
        ch:string = ""
        i:int = 0
        j:int = 0

        def generate_inner_output():
            return (s)


        htparam = get_cache (Htparam, {"paramnr": [(eq, 977)]})
        ch = htparam.fchar
        j = 0
        for i in range(1,length(ch)  + 1) :

            if substring(ch, i - 1, 1) >= ("0").lower()  and substring(ch, i - 1, 1) <= ("9").lower() :
                j = j + 1
                s = s + substring(konto, j - 1, 1)
            else:
                s = s + substring(ch, i - 1, 1)

        return generate_inner_output()

    if mi_lager_chk :

        if from_grp == 0:

            if from_date == None:
                create_list()
            else:
                create_list0()
        else:

            if from_date == None:
                create_list1()
            else:
                create_list11()

    elif mi_subgrp_chk :
        create_listsgrp()

    elif mi_acct_chk :
        create_listacct()

    return generate_output()