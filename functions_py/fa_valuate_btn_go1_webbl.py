#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 25/7/2025
# fix lagerbuff
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Fa_lager, Mathis, Fa_artikel, Fa_grup, Fa_kateg, Gl_acct, Htparam

lagerbuff_data, Lagerbuff = create_model_like(Fa_lager)

def fa_valuate_btn_go1_webbl(pvilanguage:int, lagerbuff_data:[Lagerbuff], mi_lager_chk:bool, mi_subgrp_chk:bool, mi_acct_chk:bool, mi_bookvalue_chk:bool, from_grp:int, from_date:date, to_lager:int, from_lager:int, maxnr:int, to_date:date, zero_value_only:bool, last_acctdate:date, yy:int, mm:int, from_subgr:int, to_subgr:int, show_all:bool):

    prepare_cache ([Mathis, Fa_artikel, Fa_grup, Fa_kateg, Htparam])

    out_list_data = []
    do_it:bool = False
    sub_depn:int = 0
    val_dep:Decimal = to_decimal("0.0")
    datum:date = None
    flag:bool = False
    p_depn_wert:Decimal = to_decimal("0.0")
    p_book_wert:Decimal = to_decimal("0.0")
    fa_lager = mathis = fa_artikel = fa_grup = fa_kateg = gl_acct = htparam = None

    lagerbuff = out_list = None

    out_list_data, Out_list = create_model("Out_list", {"flag":int, "fibu":string, "bezeich":string, "refno":string, "location":string, "received":date, "qty":Decimal, "init_val":Decimal, "depn_val":Decimal, "book_val":Decimal, "depn_no":int, "first_depn":date, "next_depn":date, "last_depn":date, "kateg":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal out_list_data, do_it, sub_depn, val_dep, datum, flag, p_depn_wert, p_book_wert, fa_lager, mathis, fa_artikel, fa_grup, fa_kateg, gl_acct, htparam
        nonlocal pvilanguage, mi_lager_chk, mi_subgrp_chk, mi_acct_chk, mi_bookvalue_chk, from_grp, from_date, to_lager, from_lager, maxnr, to_date, zero_value_only, last_acctdate, yy, mm, from_subgr, to_subgr, show_all


        nonlocal lagerbuff, out_list
        nonlocal out_list_data

        return {"out-list": out_list_data}

    def create_list():

        nonlocal out_list_data, do_it, sub_depn, val_dep, datum, flag, p_depn_wert, p_book_wert, fa_lager, mathis, fa_artikel, fa_grup, fa_kateg, gl_acct, htparam
        nonlocal pvilanguage, mi_lager_chk, mi_subgrp_chk, mi_acct_chk, mi_bookvalue_chk, from_grp, from_date, to_lager, from_lager, maxnr, to_date, zero_value_only, last_acctdate, yy, mm, from_subgr, to_subgr, show_all


        nonlocal lagerbuff, out_list
        nonlocal out_list_data

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
        tot_anz =  to_decimal("0")
        tot_val =  to_decimal("0")
        tot_val1 =  to_decimal("0")
        tot_val2 =  to_decimal("0")

        for lagerbuff in query(lagerbuff_data, filters=(lambda lagerbuff: lagerbuff.lagerBuff.lager_nr >= from_lager and lagerBuff.lager_nr <= to_lager)):
            out_list = Out_list()
            out_list_data.append(out_list)

            out_list.bezeich = to_string(lagerBuff.lager_nr, ">>99") + "-" + lagerBuff.bezeich
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

            if mi_bookvalue_chk :

                if show_all:

                    mathis_obj_list = {}
                    mathis = Mathis()
                    fa_artikel = Fa_artikel()
                    fa_grup = Fa_grup()
                    for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.katnr, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel._recid, fa_grup.bezeich, fa_grup._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.katnr, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel._recid, Fa_grup.bezeich, Fa_grup._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.gnr) & (Fa_grup.flag == 0)).filter(
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
                                    out_list = Out_list()
                                    out_list_data.append(out_list)

                                    out_list.flag = 1
                                    out_list.refno = "SUB TOTAL"
                                    out_list.qty =  to_decimal(t_anz)
                                    out_list.init_val =  to_decimal(t_val)
                                    out_list.depn_val =  to_decimal(t_val1)
                                    out_list.book_val =  to_decimal(t_val2)


                                out_list = Out_list()
                                out_list_data.append(out_list)

                                out_list.bezeich = fa_grup.bezeich
                                t_anz =  to_decimal("0")
                                t_val =  to_decimal("0")
                                t_val1 =  to_decimal("0")
                                t_val2 =  to_decimal("0")
                                zwkum = fa_artikel.gnr


                            out_list = Out_list()
                            out_list_data.append(out_list)

                            out_list.flag = 1
                            out_list.refno = mathis.asset
                            out_list.bezeich = mathis.name
                            out_list.received = mathis.datum
                            out_list.qty =  to_decimal(fa_artikel.anzahl)


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
                            out_list.init_val =  to_decimal(fa_artikel.warenwert)
                            out_list.depn_val =  to_decimal(p_depn_wert)
                            out_list.book_val =  to_decimal(p_book_wert)

                            fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_artikel.katnr)]})

                            if fa_kateg:
                                out_list.kateg = fa_kateg.bezeich + " - " + to_string(fa_kateg.rate) + "%"

                            if fa_artikel.first_depn != None:
                                out_list.first_depn = fa_artikel.first_depn

                            if fa_artikel.next_depn != None:
                                out_list.next_depn = fa_artikel.next_depn

                            if fa_artikel.last_depn != None:
                                out_list.last_depn = fa_artikel.last_depn

                            if fa_artikel.anz_depn != None:
                                out_list.depn_no = sub_depn
                else:

                    mathis_obj_list = {}
                    mathis = Mathis()
                    fa_artikel = Fa_artikel()
                    fa_grup = Fa_grup()
                    for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.katnr, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel._recid, fa_grup.bezeich, fa_grup._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.katnr, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel._recid, Fa_grup.bezeich, Fa_grup._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.posted)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.gnr) & (Fa_grup.flag == 0)).filter(
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
                                    out_list = Out_list()
                                    out_list_data.append(out_list)

                                    out_list.flag = 1
                                    out_list.refno = "SUB TOTAL"
                                    out_list.qty =  to_decimal(t_anz)
                                    out_list.init_val =  to_decimal(t_val)
                                    out_list.depn_val =  to_decimal(t_val1)
                                    out_list.book_val =  to_decimal(t_val2)


                                out_list = Out_list()
                                out_list_data.append(out_list)

                                out_list.bezeich = fa_grup.bezeich
                                t_anz =  to_decimal("0")
                                t_val =  to_decimal("0")
                                t_val1 =  to_decimal("0")
                                t_val2 =  to_decimal("0")
                                zwkum = fa_artikel.gnr


                            out_list = Out_list()
                            out_list_data.append(out_list)

                            out_list.flag = 1
                            out_list.refno = mathis.asset
                            out_list.bezeich = mathis.name
                            out_list.received = mathis.datum
                            out_list.qty =  to_decimal(fa_artikel.anzahl)


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
                            out_list.init_val =  to_decimal(fa_artikel.warenwert)
                            out_list.depn_val =  to_decimal(p_depn_wert)
                            out_list.book_val =  to_decimal(p_book_wert)

                            fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_artikel.katnr)]})

                            if fa_kateg:
                                out_list.kateg = fa_kateg.bezeich + " - " + to_string(fa_kateg.rate) + "%"

                            if fa_artikel.first_depn != None:
                                out_list.first_depn = fa_artikel.first_depn

                            if fa_artikel.next_depn != None:
                                out_list.next_depn = fa_artikel.next_depn

                            if fa_artikel.last_depn != None:
                                out_list.last_depn = fa_artikel.last_depn

                            if fa_artikel.anz_depn != None:
                                out_list.depn_no = sub_depn
            else:

                if show_all:

                    mathis_obj_list = {}
                    mathis = Mathis()
                    fa_artikel = Fa_artikel()
                    fa_grup = Fa_grup()

                    # Rd, 25/7/2025
                    # lagerbuff
                    # for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.katnr, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel._recid, fa_grup.bezeich, fa_grup._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.katnr, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel._recid, Fa_grup.bezeich, Fa_grup._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.gnr) & (Fa_grup.flag == 0)).filter(
                    #          (Mathis.location == lagerBuff.bezeich) & (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Fa_grup.gnr, Mathis.name).all():
                    for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, \
                        fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.katnr, fa_artikel.next_depn, fa_artikel.subgrp, \
                            fa_artikel.fibukonto, fa_artikel._recid, fa_grup.bezeich, fa_grup._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, \
                            Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.katnr, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel._recid, Fa_grup.bezeich, Fa_grup._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.gnr) & (Fa_grup.flag == 0)).filter(
                             (Mathis.location == lagerbuff.bezeich) & (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Fa_grup.gnr, Mathis.name).all():
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
                                    out_list = Out_list()
                                    out_list_data.append(out_list)

                                    out_list.flag = 1
                                    out_list.refno = "SUB TOTAL"
                                    out_list.qty =  to_decimal(t_anz)
                                    out_list.init_val =  to_decimal(t_val)
                                    out_list.depn_val =  to_decimal(t_val1)
                                    out_list.book_val =  to_decimal(t_val2)


                                out_list = Out_list()
                                out_list_data.append(out_list)

                                out_list.bezeich = fa_grup.bezeich
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


                            out_list = Out_list()
                            out_list_data.append(out_list)

                            out_list.flag = 1
                            out_list.bezeich = mathis.name
                            out_list.refno = mathis.asset
                            out_list.received = mathis.datum
                            out_list.qty =  to_decimal(fa_artikel.anzahl)
                            out_list.init_val =  to_decimal(fa_artikel.warenwert)

                            # Rd 25/7/2025
                            # add fa_artikel.
                            out_list.depn_val =  to_decimal(fa_artikel.depn_wert)
                            out_list.book_val =  to_decimal(fa_artikel.book_wert)

                            fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_artikel.katnr)]})

                            if fa_kateg:
                                out_list.kateg = fa_kateg.bezeich + " - " + to_string(fa_kateg.rate) + "%"

                            if fa_artikel.first_depn != None:
                                out_list.first_depn = fa_artikel.first_depn

                            if fa_artikel.next_depn != None:
                                out_list.next_depn = fa_artikel.next_depn

                            if fa_artikel.last_depn != None:
                                out_list.last_depn = fa_artikel.last_depn

                            if fa_artikel.anz_depn != None:
                                out_list.depn_no = fa_artikel.anz_depn
                else:

                    mathis_obj_list = {}
                    mathis = Mathis()
                    fa_artikel = Fa_artikel()
                    fa_grup = Fa_grup()

                    # Rd 25/7/2025
                    # lagerbuff
                    for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.katnr, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel._recid, fa_grup.bezeich, fa_grup._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.katnr, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel._recid, Fa_grup.bezeich, Fa_grup._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.posted)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.gnr) & (Fa_grup.flag == 0)).filter(
                             (Mathis.location == lagerbuff.bezeich) & (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Fa_grup.gnr, Mathis.name).all():
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
                                    out_list = Out_list()
                                    out_list_data.append(out_list)

                                    out_list.flag = 1
                                    out_list.refno = "SUB TOTAL"
                                    out_list.qty =  to_decimal(t_anz)
                                    out_list.init_val =  to_decimal(t_val)
                                    out_list.depn_val =  to_decimal(t_val1)
                                    out_list.book_val =  to_decimal(t_val2)


                                out_list = Out_list()
                                out_list_data.append(out_list)

                                out_list.bezeich = fa_grup.bezeich
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


                            out_list = Out_list()
                            out_list_data.append(out_list)

                            out_list.flag = 1
                            out_list.bezeich = mathis.name
                            out_list.refno = mathis.asset
                            out_list.received = mathis.datum
                            out_list.qty =  to_decimal(fa_artikel.anzahl)
                            out_list.init_val =  to_decimal(fa_artikel.warenwert)

                            # Rd 25/7/2025
                            # add fa_artikel.
                            # out_list.depn_val =  to_decimal(depn_wert)
                            # out_list.book_val =  to_decimal(book_wert)
                            out_list.depn_val =  to_decimal(fa_artikel.depn_wert)
                            out_list.book_val =  to_decimal(fa_artikel.book_wert)

                            fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_artikel.katnr)]})

                            if fa_kateg:
                                out_list.kateg = fa_kateg.bezeich + " - " + to_string(fa_kateg.rate) + "%"

                            if fa_artikel.first_depn != None:
                                out_list.first_depn = fa_artikel.first_depn

                            if fa_artikel.next_depn != None:
                                out_list.next_depn = fa_artikel.next_depn

                            if fa_artikel.last_depn != None:
                                out_list.last_depn = fa_artikel.last_depn

                            if fa_artikel.anz_depn != None:
                                out_list.depn_no = fa_artikel.anz_depn
            out_list = Out_list()
            out_list_data.append(out_list)

            out_list.flag = 1
            out_list.refno = "SUB TOTAL"
            out_list.qty =  to_decimal(t_anz)
            out_list.init_val =  to_decimal(t_val)
            out_list.depn_val =  to_decimal(t_val1)
            out_list.book_val =  to_decimal(t_val2)


            out_list = Out_list()
            out_list_data.append(out_list)

            out_list.refno = "T O T A L"
            out_list.flag = 1
            out_list.qty =  to_decimal(tt_anz)
            out_list.init_val =  to_decimal(tt_val)
            out_list.depn_val =  to_decimal(tt_val1)
            out_list.book_val =  to_decimal(tt_val2)

        if from_lager != to_lager:
            out_list = Out_list()
            out_list_data.append(out_list)

            out_list = Out_list()
            out_list_data.append(out_list)

            out_list.flag = 2
            out_list.refno = "GRAND TOTAL"
            out_list.qty =  to_decimal(tot_anz)
            out_list.init_val =  to_decimal(tot_val)
            out_list.depn_val =  to_decimal(tot_val1)
            out_list.book_val =  to_decimal(tot_val2)


    def create_list0():

        nonlocal out_list_data, do_it, sub_depn, val_dep, datum, flag, p_depn_wert, p_book_wert, fa_lager, mathis, fa_artikel, fa_grup, fa_kateg, gl_acct, htparam
        nonlocal pvilanguage, mi_lager_chk, mi_subgrp_chk, mi_acct_chk, mi_bookvalue_chk, from_grp, from_date, to_lager, from_lager, maxnr, to_date, zero_value_only, last_acctdate, yy, mm, from_subgr, to_subgr, show_all


        nonlocal lagerbuff, out_list
        nonlocal out_list_data

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
        tot_anz =  to_decimal("0")
        tot_val =  to_decimal("0")
        tot_val1 =  to_decimal("0")
        tot_val2 =  to_decimal("0")
        max_lager = to_lager


        # Rd, 25/7/2025
        # fix lagerbuff
        for lagerbuff in query(lagerbuff_data, filters=(lambda lagerbuff: lagerbuff.lager_nr >= from_lager and lagerbuff.lager_nr <= to_lager)):
            out_list = Out_list()
            out_list_data.append(out_list)

            out_list.bezeich = to_string(lagerbuff.lager_nr, ">>99") + "-" + lagerbuff.bezeich
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

            if mi_bookvalue_chk :

                if show_all:

                    mathis_obj_list = {}
                    mathis = Mathis()
                    fa_artikel = Fa_artikel()
                    fa_grup = Fa_grup()
                    for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.katnr, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel._recid, fa_grup.bezeich, fa_grup._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.katnr, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel._recid, Fa_grup.bezeich, Fa_grup._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.gnr) & (Fa_grup.flag == 0)).filter(
                             (Mathis.location == lagerbuff_data.bezeich) & (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Fa_grup.gnr, Mathis.name).all():
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
                                    out_list = Out_list()
                                    out_list_data.append(out_list)

                                    out_list.flag = 1
                                    out_list.refno = "SUB TOTAL"
                                    out_list.qty =  to_decimal(t_anz)
                                    out_list.init_val =  to_decimal(t_val)
                                    out_list.depn_val =  to_decimal(t_val1)
                                    out_list.book_val =  to_decimal(t_val2)


                                out_list = Out_list()
                                out_list_data.append(out_list)

                                out_list.bezeich = fa_grup.bezeich
                                t_anz =  to_decimal("0")
                                t_val =  to_decimal("0")
                                t_val1 =  to_decimal("0")
                                t_val2 =  to_decimal("0")
                                zwkum = fa_artikel.gnr


                            out_list = Out_list()
                            out_list_data.append(out_list)

                            out_list.flag = 1
                            out_list.refno = mathis.asset
                            out_list.bezeich = mathis.name
                            out_list.received = mathis.datum
                            out_list.qty =  to_decimal(fa_artikel.anzahl)


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
                            out_list.init_val =  to_decimal(fa_artikel.warenwert)
                            out_list.depn_val =  to_decimal(p_depn_wert)
                            out_list.book_val =  to_decimal(p_book_wert)

                            fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_artikel.katnr)]})

                            if fa_kateg:
                                out_list.kateg = fa_kateg.bezeich + " - " + to_string(fa_kateg.rate) + "%"

                            if fa_artikel.first_depn != None:
                                out_list.first_depn = fa_artikel.first_depn

                            if fa_artikel.next_depn != None:
                                out_list.next_depn = fa_artikel.next_depn

                            if fa_artikel.last_depn != None:
                                out_list.last_depn = fa_artikel.last_depn

                            if fa_artikel.anz_depn != None:
                                out_list.depn_no = sub_depn
                else:

                    mathis_obj_list = {}
                    mathis = Mathis()
                    fa_artikel = Fa_artikel()
                    fa_grup = Fa_grup()
                    # Rd 25/7/2025
                    # lagerbuff
                    for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.katnr, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel._recid, fa_grup.bezeich, fa_grup._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.katnr, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel._recid, Fa_grup.bezeich, Fa_grup._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0) & (Fa_artikel.posted)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.gnr) & (Fa_grup.flag == 0)).filter(
                             (Mathis.location == lagerbuff.bezeich) & (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Fa_grup.gnr, Mathis.name).all():
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
                                    out_list = Out_list()
                                    out_list_data.append(out_list)

                                    out_list.flag = 1
                                    out_list.refno = "SUB TOTAL"
                                    out_list.qty =  to_decimal(t_anz)
                                    out_list.init_val =  to_decimal(t_val)
                                    out_list.depn_val =  to_decimal(t_val1)
                                    out_list.book_val =  to_decimal(t_val2)


                                out_list = Out_list()
                                out_list_data.append(out_list)

                                out_list.bezeich = fa_grup.bezeich
                                t_anz =  to_decimal("0")
                                t_val =  to_decimal("0")
                                t_val1 =  to_decimal("0")
                                t_val2 =  to_decimal("0")
                                zwkum = fa_artikel.gnr


                            out_list = Out_list()
                            out_list_data.append(out_list)

                            out_list.flag = 1
                            out_list.refno = mathis.asset
                            out_list.bezeich = mathis.name
                            out_list.received = mathis.datum
                            out_list.qty =  to_decimal(fa_artikel.anzahl)


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
                            out_list.init_val =  to_decimal(fa_artikel.warenwert)
                            out_list.depn_val =  to_decimal(p_depn_wert)
                            out_list.book_val =  to_decimal(p_book_wert)

                            fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_artikel.katnr)]})

                            if fa_kateg:
                                out_list.kateg = fa_kateg.bezeich + " - " + to_string(fa_kateg.rate) + "%"

                            if fa_artikel.first_depn != None:
                                out_list.first_depn = fa_artikel.first_depn

                            if fa_artikel.next_depn != None:
                                out_list.next_depn = fa_artikel.next_depn

                            if fa_artikel.last_depn != None:
                                out_list.last_depn = fa_artikel.last_depn

                            if fa_artikel.anz_depn != None:
                                out_list.depn_no = sub_depn
            else:

                mathis_obj_list = {}
                mathis = Mathis()
                fa_artikel = Fa_artikel()
                fa_grup = Fa_grup()
                # Rd 25/7/2025
                # lagerbuff
                for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.katnr, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel._recid, fa_grup.bezeich, fa_grup._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.katnr, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel._recid, Fa_grup.bezeich, Fa_grup._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0) & (Fa_artikel.posted)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.gnr) & (Fa_grup.flag == 0)).filter(
                         (Mathis.location == lagerbuff.bezeich) & (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Fa_grup.gnr, Mathis.name).all():
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
                                out_list = Out_list()
                                out_list_data.append(out_list)

                                out_list.refno = "SUB TOTAL"
                                out_list.flag = 1
                                out_list.qty =  to_decimal(t_anz)
                                out_list.init_val =  to_decimal(t_val)
                                out_list.depn_val =  to_decimal(t_val1)
                                out_list.book_val =  to_decimal(t_val2)


                            out_list = Out_list()
                            out_list_data.append(out_list)

                            out_list.bezeich = fa_grup.bezeich
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


                        out_list = Out_list()
                        out_list_data.append(out_list)

                        out_list.flag = 1
                        out_list.bezeich = mathis.name
                        out_list.refno = mathis.asset
                        out_list.received = mathis.datu
                        out_list.qty =  to_decimal(fa_artikel.anzahl)
                        out_list.init_val =  to_decimal(fa_artikel.warenwert)
                        out_list.depn_val =  to_decimal(fa_artikel.depn_wert)
                        out_list.book_val =  to_decimal(fa_artikel.book_wert)

                        fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_artikel.katnr)]})

                        if fa_kateg:
                            out_list.kateg = fa_kateg.bezeich + " - " + to_string(fa_kateg.rate) + "%"

                        if fa_artikel.first_depn != None:
                            out_list.first_depn = fa_artikel.first_depn

                        if fa_artikel.next_depn != None:
                            out_list.next_depn = fa_artikel.next_depn

                        if fa_artikel.last_depn != None:
                            out_list.last_depn = fa_artikel.last_depn

                        if fa_artikel.anz_depn != None:
                            out_list.depn_no = fa_artikel.anz_depn
            out_list = Out_list()
            out_list_data.append(out_list)

            out_list.refno = "SUB TOTAL"
            out_list.flag = 1
            out_list.qty =  to_decimal(t_anz)
            out_list.init_val =  to_decimal(t_val)
            out_list.depn_val =  to_decimal(t_val1)
            out_list.book_val =  to_decimal(t_val2)


            out_list = Out_list()
            out_list_data.append(out_list)

            out_list.refno = "T O T A L"
            out_list.flag = 1
            out_list.qty =  to_decimal(tt_anz)
            out_list.init_val =  to_decimal(tt_val)
            out_list.depn_val =  to_decimal(tt_val1)
            out_list.book_val =  to_decimal(tt_val2)

        if from_lager != to_lager:
            out_list = Out_list()
            out_list_data.append(out_list)

            out_list = Out_list()
            out_list_data.append(out_list)

            out_list.flag = 2
            out_list.refno = "GRAND TOTAL"
            out_list.qty =  to_decimal(tot_anz)
            out_list.init_val =  to_decimal(tot_val)
            out_list.depn_val =  to_decimal(tot_val1)
            out_list.book_val =  to_decimal(tot_val2)


    def create_list1():

        nonlocal out_list_data, do_it, sub_depn, val_dep, datum, flag, p_depn_wert, p_book_wert, fa_lager, mathis, fa_artikel, fa_grup, fa_kateg, gl_acct, htparam
        nonlocal pvilanguage, mi_lager_chk, mi_subgrp_chk, mi_acct_chk, mi_bookvalue_chk, from_grp, from_date, to_lager, from_lager, maxnr, to_date, zero_value_only, last_acctdate, yy, mm, from_subgr, to_subgr, show_all


        nonlocal lagerbuff, out_list
        nonlocal out_list_data

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
        tot_anz =  to_decimal("0")
        tot_val =  to_decimal("0")
        tot_val1 =  to_decimal("0")
        tot_val2 =  to_decimal("0")

        fa_grup = get_cache (Fa_grup, {"gnr": [(eq, from_grp)],"flag": [(eq, 0)]})
        # Rd 25/7/2025
        # lagerbuff
        for lagerbuff in query(lagerbuff_data, filters=(lambda lagerbuff: lagerbuff.lagerbuff.lager_nr >= from_lager and lagerbuff.lager_nr <= to_lager)):
            out_list = Out_list()
            out_list_data.append(out_list)

            out_list.bezeich = to_string(lagerbuff.lager_nr, ">>99") + "-" + lagerbuff.bezeich


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

            if mi_bookvalue_chk :

                mathis_obj_list = {}
                mathis = Mathis()
                fa_artikel = Fa_artikel()
                # Rd 25/7/2025
                # lagerbuff
                for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.katnr, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.katnr, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0) & (Fa_artikel.gnr == from_grp)).filter(
                         (Mathis.location == lagerbuff.bezeich) & (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Mathis.name).all():
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
                                out_list = Out_list()
                                out_list_data.append(out_list)

                                out_list.refno = "SUB TOTAL"
                                out_list.flag = 1
                                out_list.qty =  to_decimal(t_anz)
                                out_list.init_val =  to_decimal(t_val)
                                out_list.depn_val =  to_decimal(t_val1)
                                out_list.book_val =  to_decimal(t_val2)


                            out_list = Out_list()
                            out_list_data.append(out_list)

                            out_list.bezeich = fa_grup.bezeich
                            t_anz =  to_decimal("0")
                            t_val =  to_decimal("0")
                            t_val1 =  to_decimal("0")
                            t_val2 =  to_decimal("0")
                            zwkum = fa_artikel.gnr


                        out_list = Out_list()
                        out_list_data.append(out_list)

                        out_list.refno = mathis.asset
                        out_list.flag = 1
                        out_list.bezeich = mathis.name
                        out_list.received = mathis.datum
                        out_list.qty =  to_decimal(fa_artikel.anzahl)
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
                        out_list.init_val =  to_decimal(fa_artikel.warenwert)
                        out_list.depn_val =  to_decimal(p_depn_wert)
                        out_list.book_val =  to_decimal(p_book_wert)

                        fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_artikel.katnr)]})

                        if fa_kateg:
                            out_list.kateg = fa_kateg.bezeich + " - " + to_string(fa_kateg.rate) + "%"

                        if fa_artikel.first_depn != None:
                            out_list.first_depn = fa_artikel.first_depn

                        if fa_artikel.next_depn != None:
                            out_list.next_depn = fa_artikel.next_depn

                        if fa_artikel.last_depn != None:
                            out_list.last_depn = fa_artikel.last_depn

                        if fa_artikel.anz_depn != None:
                            out_list.depn_no = sub_depn
            else:

                mathis_obj_list = {}
                mathis = Mathis()
                fa_artikel = Fa_artikel()
                # Rd 25/7/2025
                # lagerbuff
                for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.katnr, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.katnr, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0) & (Fa_artikel.gnr == from_grp)).filter(
                         (Mathis.location == lagerbuff.bezeich) & (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Mathis.name).all():
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
                                out_list = Out_list()
                                out_list_data.append(out_list)

                                out_list.refno = "SUB TOTAL"
                                out_list.flag = 1
                                out_list.qty =  to_decimal(t_anz)
                                out_list.init_val =  to_decimal(t_val)
                                out_list.depn_val =  to_decimal(t_val1)
                                out_list.book_val =  to_decimal(t_val2)


                            out_list = Out_list()
                            out_list_data.append(out_list)

                            out_list.bezeich = fa_grup.bezeich
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


                        out_list = Out_list()
                        out_list_data.append(out_list)

                        out_list.flag = 1
                        out_list.refno = mathis.asset
                        out_list.bezeich = mathis.name
                        out_list.received = mathis.datum
                        out_list.qty =  to_decimal(fa_artikel.anzahl)
                        out_list.init_val =  to_decimal(fa_artikel.warenwert)
                        out_list.depn_val =  to_decimal(fa_artikel.depn_wert)
                        out_list.book_val =  to_decimal(fa_artikel.book_wert)

                        fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_artikel.katnr)]})

                        if fa_kateg:
                            out_list.kateg = fa_kateg.bezeich + " - " + to_string(fa_kateg.rate) + "%"

                        if fa_artikel.first_depn != None:
                            out_list.first_depn = fa_artikel.first_depn

                        if fa_artikel.next_depn != None:
                            out_list.next_depn = fa_artikel.next_depn

                        if fa_artikel.last_depn != None:
                            out_list.last_depn = fa_artikel.last_depn

                        if fa_artikel.anz_depn != None:
                            # Rd 25/7/2025
                            # fa_artikel
                            # out_list.depn_no = anz_depn
                            out_list.depn_no = fa_artikel.anz_depn
            out_list = Out_list()
            out_list_data.append(out_list)

            out_list.refno = "SUB TOTAL"
            out_list.flag = 1
            out_list.qty =  to_decimal(t_anz)
            out_list.init_val =  to_decimal(t_val)
            out_list.depn_val =  to_decimal(t_val1)
            out_list.book_val =  to_decimal(t_val2)


            out_list = Out_list()
            out_list_data.append(out_list)

            out_list.refno = "T O T A L"
            out_list.flag = 1
            out_list.qty =  to_decimal(tt_anz)
            out_list.init_val =  to_decimal(tt_val)
            out_list.depn_val =  to_decimal(tt_val1)
            out_list.book_val =  to_decimal(tt_val2)

        if from_lager != to_lager and tot_anz != 0:
            out_list = Out_list()
            out_list_data.append(out_list)

            out_list = Out_list()
            out_list_data.append(out_list)

            out_list.flag = 2
            out_list.refno = "GRAND TOTAL"
            out_list.qty =  to_decimal(tot_anz)
            out_list.init_val =  to_decimal(tot_val)
            out_list.depn_val =  to_decimal(tot_val1)
            out_list.book_val =  to_decimal(tot_val2)


    def create_list11():

        nonlocal out_list_data, do_it, sub_depn, val_dep, datum, flag, p_depn_wert, p_book_wert, fa_lager, mathis, fa_artikel, fa_grup, fa_kateg, gl_acct, htparam
        nonlocal pvilanguage, mi_lager_chk, mi_subgrp_chk, mi_acct_chk, mi_bookvalue_chk, from_grp, from_date, to_lager, from_lager, maxnr, to_date, zero_value_only, last_acctdate, yy, mm, from_subgr, to_subgr, show_all


        nonlocal lagerbuff, out_list
        nonlocal out_list_data

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
        tot_anz =  to_decimal("0")
        tot_val =  to_decimal("0")
        tot_val1 =  to_decimal("0")
        tot_val2 =  to_decimal("0")

        fa_grup = get_cache (Fa_grup, {"gnr": [(eq, from_grp)],"flag": [(eq, 0)]})

        for lagerbuff in query(lagerbuff_data, filters=(lambda lagerbuff: lagerbuff.lagerBuff.lager_nr >= from_lager and lagerBuff.lager_nr <= to_lager)):
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


            out_list = Out_list()
            out_list_data.append(out_list)

            out_list.bezeich = to_string(lagerBuff.lager_nr, ">>99") + "-" + lagerBuff.bezeich

            if mi_bookvalue_chk :

                mathis_obj_list = {}
                mathis = Mathis()
                fa_artikel = Fa_artikel()
                for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.katnr, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.katnr, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0) & (Fa_artikel.gnr == from_grp)).filter(
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
                                out_list = Out_list()
                                out_list_data.append(out_list)

                                out_list.refno = "SUB TOTAL"
                                out_list.flag = 1
                                out_list.qty =  to_decimal(t_anz)
                                out_list.init_val =  to_decimal(t_val)
                                out_list.depn_val =  to_decimal(t_val1)
                                out_list.book_val =  to_decimal(t_val2)


                            out_list = Out_list()
                            out_list_data.append(out_list)

                            out_list.bezeich = fa_grup.bezeich
                            t_anz =  to_decimal("0")
                            t_val =  to_decimal("0")
                            t_val1 =  to_decimal("0")
                            t_val2 =  to_decimal("0")
                            zwkum = fa_artikel.gnr


                        out_list = Out_list()
                        out_list_data.append(out_list)

                        out_list.flag = 1
                        out_list.refno = mathis.asset
                        out_list.bezeich = mathis.name
                        out_list.received = mathis.datum
                        out_list.qty =  to_decimal(fa_artikel.anzahl)
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
                        out_list.init_val =  to_decimal(fa_artikel.warenwert)
                        out_list.depn_val =  to_decimal(p_depn_wert)
                        out_list.book_val =  to_decimal(p_book_wert)

                        fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_artikel.katnr)]})

                        if fa_kateg:
                            out_list.kateg = fa_kateg.bezeich + " - " + to_string(fa_kateg.rate) + "%"

                        if fa_artikel.first_depn != None:
                            out_list.first_depn = fa_artikel.first_depn

                        if fa_artikel.next_depn != None:
                            out_list.next_depn = fa_artikel.next_depn

                        if fa_artikel.last_depn != None:
                            out_list.last_depn = fa_artikel.last_depn

                        if fa_artikel.anz_depn != None:
                            out_list.depn_no = sub_depn
            else:

                mathis_obj_list = {}
                mathis = Mathis()
                fa_artikel = Fa_artikel()
                for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.katnr, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.katnr, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0) & (Fa_artikel.gnr == from_grp)).filter(
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
                                out_list = Out_list()
                                out_list_data.append(out_list)

                                out_list.refno = "SUB TOTAL"
                                out_list.flag = 1
                                out_list.qty =  to_decimal(t_anz)
                                out_list.init_val =  to_decimal(t_val)
                                out_list.depn_val =  to_decimal(t_val1)
                                out_list.book_val =  to_decimal(t_val2)


                            out_list = Out_list()
                            out_list_data.append(out_list)

                            out_list.bezeich = fa_grup.bezeich
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


                        out_list = Out_list()
                        out_list_data.append(out_list)

                        out_list.flag = 1
                        out_list.refno = mathis.asset
                        out_list.bezeich = mathis.name
                        out_list.received = mathis.datum
                        out_list.qty =  to_decimal(fa_artikel.anzahl)
                        out_list.init_val =  to_decimal(fa_artikel.warenwert)
                        out_list.depn_val =  to_decimal(fa_artikel.depn_wert)
                        out_list.book_val =  to_decimal(fa_artikel.book_wert)

                        fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_artikel.katnr)]})

                        if fa_kateg:
                            out_list.kateg = fa_kateg.bezeich + " - " + to_string(fa_kateg.rate) + "%"

                        if fa_artikel.first_depn != None:
                            out_list.first_depn = fa_artikel.first_depn

                        if fa_artikel.next_depn != None:
                            out_list.next_depn = fa_artikel.next_depn

                        if fa_artikel.last_depn != None:
                            out_list.last_depn = fa_artikel.last_depn

                        if fa_artikel.anz_depn != None:
                            out_list.depn_no = fa_artikel.anz_depn
            out_list = Out_list()
            out_list_data.append(out_list)

            out_list.refno = "SUB TOTAL"
            out_list.flag = 1
            out_list.qty =  to_decimal(t_anz)
            out_list.init_val =  to_decimal(t_val)
            out_list.depn_val =  to_decimal(t_val1)
            out_list.book_val =  to_decimal(t_val2)


            out_list = Out_list()
            out_list_data.append(out_list)

            out_list.refno = "T O T A L"
            out_list.flag = 1
            out_list.qty =  to_decimal(tt_anz)
            out_list.init_val =  to_decimal(tt_val)
            out_list.depn_val =  to_decimal(tt_val1)
            out_list.book_val =  to_decimal(tt_val2)

        if from_lager != to_lager:
            out_list = Out_list()
            out_list_data.append(out_list)

            out_list = Out_list()
            out_list_data.append(out_list)

            out_list.flag = 2
            out_list.refno = "GRAND TOTAL"
            out_list.qty =  to_decimal(tot_anz)
            out_list.init_val =  to_decimal(tot_val)
            out_list.depn_val =  to_decimal(tot_val1)
            out_list.book_val =  to_decimal(tot_val2)


    def create_listsgrp():

        nonlocal out_list_data, do_it, sub_depn, val_dep, datum, flag, p_depn_wert, p_book_wert, fa_lager, mathis, fa_artikel, fa_grup, fa_kateg, gl_acct, htparam
        nonlocal pvilanguage, mi_lager_chk, mi_subgrp_chk, mi_acct_chk, mi_bookvalue_chk, from_grp, from_date, to_lager, from_lager, maxnr, to_date, zero_value_only, last_acctdate, yy, mm, from_subgr, to_subgr, show_all


        nonlocal lagerbuff, out_list
        nonlocal out_list_data

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
            for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.katnr, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel._recid, fa_grup.bezeich, fa_grup._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.katnr, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel._recid, Fa_grup.bezeich, Fa_grup._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1) & (Fa_grup.gnr >= from_subgr) & (Fa_grup.gnr <= to_subgr)).filter(
                         (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Fa_artikel.subgrp, Mathis.name).all():
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

                    if zwkum != fa_artikel.subgrp:

                        if zwkum != 0:
                            out_list = Out_list()
                            out_list_data.append(out_list)

                            out_list.refno = "SUB TOTAL"
                            out_list.flag = 1
                            out_list.qty =  to_decimal(t_anz)
                            out_list.init_val =  to_decimal(t_val)
                            out_list.depn_val =  to_decimal(t_val1)
                            out_list.book_val =  to_decimal(t_val2)


                        out_list = Out_list()
                        out_list_data.append(out_list)

                        out_list.bezeich = fa_grup.bezeich
                        t_anz =  to_decimal("0")
                        t_val =  to_decimal("0")
                        t_val1 =  to_decimal("0")
                        t_val2 =  to_decimal("0")
                        zwkum = fa_artikel.subgrp


                    out_list = Out_list()
                    out_list_data.append(out_list)

                    out_list.flag = 1
                    out_list.refno = mathis.asset
                    out_list.location = trim (mathis.location)
                    out_list.bezeich = mathis.name
                    out_list.received = mathis.datum
                    out_list.qty =  to_decimal(fa_artikel.anzahl)
                    out_list.init_val =  to_decimal(fa_artikel.warenwert)
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
                        out_list.depn_val =  to_decimal("0")
                        out_list.book_val =  to_decimal(fa_artikel.warenwert)


                    else:
                        out_list.depn_val =  to_decimal(p_depn_wert) - to_decimal(diff_wert)
                        out_list.book_val =  to_decimal(p_book_wert) + to_decimal(diff_wert)

                    fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_artikel.katnr)]})

                    if fa_kateg:
                        out_list.kateg = fa_kateg.bezeich + " - " + to_string(fa_kateg.rate) + "%"

                    if fa_artikel.first_depn != None:
                        out_list.first_depn = fa_artikel.first_depn

                    if fa_artikel.next_depn != None:
                        out_list.next_depn = fa_artikel.next_depn

                    if fa_artikel.last_depn != None:
                        out_list.last_depn = fa_artikel.last_depn

                    if fa_artikel.anz_depn != None:
                        out_list.depn_no = sub_depn
            out_list = Out_list()
            out_list_data.append(out_list)

            out_list.refno = "SUB TOTAL"
            out_list.flag = 1
            out_list.qty =  to_decimal(t_anz)
            out_list.init_val =  to_decimal(t_val)
            out_list.depn_val =  to_decimal(t_val1)
            out_list.book_val =  to_decimal(t_val2)


        else:

            mathis_obj_list = {}
            mathis = Mathis()
            fa_artikel = Fa_artikel()
            fa_grup = Fa_grup()
            for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.katnr, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel._recid, fa_grup.bezeich, fa_grup._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.katnr, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel._recid, Fa_grup.bezeich, Fa_grup._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1) & (Fa_grup.gnr >= from_subgr) & (Fa_grup.gnr <= to_subgr)).filter(
                         (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Fa_artikel.subgrp, Mathis.name).all():
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

                    if zwkum != fa_artikel.subgrp:

                        if zwkum != 0:
                            out_list = Out_list()
                            out_list_data.append(out_list)

                            out_list.refno = "SUB TOTAL"
                            out_list.flag = 1
                            out_list.qty =  to_decimal(t_anz)
                            out_list.init_val =  to_decimal(t_val)
                            out_list.depn_val =  to_decimal(t_val1)
                            out_list.book_val =  to_decimal(t_val2)


                        out_list = Out_list()
                        out_list_data.append(out_list)

                        out_list.bezeich = fa_grup.bezeich
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
                    out_list = Out_list()
                    out_list_data.append(out_list)

                    out_list.flag = 1
                    out_list.refno = mathis.asset
                    out_list.location = trim (mathis.location)
                    out_list.bezeich = mathis.name
                    out_list.received = mathis.datum
                    out_list.qty =  to_decimal(fa_artikel.anzahl)
                    out_list.init_val =  to_decimal(fa_artikel.warenwert)

                    if (fa_artikel.anz_depn - diff_n) == 0:
                        out_list.depn_val =  to_decimal("0")
                        out_list.book_val =  to_decimal(fa_artikel.warenwert)


                    else:
                        out_list.depn_val =  to_decimal(fa_artikel.depn_wert) - to_decimal(diff_wert)
                        out_list.book_val =  to_decimal(fa_artikel.book_wert) + to_decimal(diff_wert)

                    fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_artikel.katnr)]})

                    if fa_kateg:
                        out_list.kateg = fa_kateg.bezeich + " - " + to_string(fa_kateg.rate) + "%"

                    if fa_artikel.first_depn != None:
                        out_list.first_depn = fa_artikel.first_depn

                    if fa_artikel.next_depn != None:
                        out_list.next_depn = fa_artikel.next_depn

                    if fa_artikel.last_depn != None:
                        out_list.last_depn = fa_artikel.last_depn

                    if fa_artikel.anz_depn != None:
                        out_list.depn_no = fa_artikel.anz_depn
            out_list = Out_list()
            out_list_data.append(out_list)

            out_list.refno = "SUB TOTAL"
            out_list.flag = 1
            out_list.qty =  to_decimal(t_anz)
            out_list.init_val =  to_decimal(t_val)
            out_list.depn_val =  to_decimal(t_val1)
            out_list.book_val =  to_decimal(t_val2)

        if tot_anz != 0:
            out_list = Out_list()
            out_list_data.append(out_list)

            out_list = Out_list()
            out_list_data.append(out_list)

            out_list.flag = 2
            out_list.refno = "TOTAL"
            out_list.qty =  to_decimal(tot_anz)
            out_list.init_val =  to_decimal(tot_val)
            out_list.depn_val =  to_decimal(tot_val1)
            out_list.book_val =  to_decimal(tot_val2)


    def create_listsgrp1():

        nonlocal out_list_data, do_it, sub_depn, val_dep, datum, flag, p_depn_wert, p_book_wert, fa_lager, mathis, fa_artikel, fa_grup, fa_kateg, gl_acct, htparam
        nonlocal pvilanguage, mi_lager_chk, mi_subgrp_chk, mi_acct_chk, mi_bookvalue_chk, from_grp, from_date, to_lager, from_lager, maxnr, to_date, zero_value_only, last_acctdate, yy, mm, from_subgr, to_subgr, show_all


        nonlocal lagerbuff, out_list
        nonlocal out_list_data

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
            for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.katnr, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel._recid, fa_grup.bezeich, fa_grup._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.katnr, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel._recid, Fa_grup.bezeich, Fa_grup._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0) & (Fa_artikel.gnr == from_grp)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1) & (Fa_grup.gnr >= from_subgr) & (Fa_grup.gnr <= to_subgr)).filter(
                         (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Fa_artikel.subgrp, Mathis.name).all():
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

                    if zwkum != fa_artikel.subgrp:

                        if zwkum != 0:
                            out_list = Out_list()
                            out_list_data.append(out_list)

                            out_list.refno = "SUB TOTAL"
                            out_list.flag = 1
                            out_list.qty =  to_decimal(t_anz)
                            out_list.init_val =  to_decimal(t_val)
                            out_list.depn_val =  to_decimal(t_val1)
                            out_list.book_val =  to_decimal(t_val2)


                        out_list = Out_list()
                        out_list_data.append(out_list)

                        out_list.bezeich = fa_grup.bezeich
                        t_anz =  to_decimal("0")
                        t_val =  to_decimal("0")
                        t_val1 =  to_decimal("0")
                        t_val2 =  to_decimal("0")
                        zwkum = fa_artikel.subgrp


                    out_list = Out_list()
                    out_list_data.append(out_list)

                    out_list.flag = 1
                    out_list.refno = mathis.asset
                    out_list.location = trim (mathis.location)
                    out_list.bezeich = mathis.name
                    out_list.received = mathis.datum
                    out_list.qty =  to_decimal(fa_artikel.anzahl)
                    out_list.init_val =  to_decimal(fa_artikel.warenwert)
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
                        out_list.depn_val =  to_decimal("0")
                        out_list.book_val =  to_decimal(fa_artikel.warenwert)


                    else:
                        out_list.depn_val =  to_decimal(p_depn_wert) - to_decimal(diff_wert)
                        out_list.book_val =  to_decimal(p_book_wert) + to_decimal(diff_wert)

                    fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_artikel.katnr)]})

                    if fa_kateg:
                        out_list.kateg = fa_kateg.bezeich + " - " + to_string(fa_kateg.rate) + "%"

                    if fa_artikel.first_depn != None:
                        out_list.first_depn = fa_artikel.first_depn

                    if fa_artikel.next_depn != None:
                        out_list.next_depn = fa_artikel.next_depn

                    if fa_artikel.last_depn != None:
                        out_list.last_depn = fa_artikel.last_depn

                    if fa_artikel.anz_depn != None:
                        out_list.depn_no = sub_depn
            out_list = Out_list()
            out_list_data.append(out_list)

            out_list.refno = "SUB TOTAL"
            out_list.flag = 1
            out_list.qty =  to_decimal(t_anz)
            out_list.init_val =  to_decimal(t_val)
            out_list.depn_val =  to_decimal(t_val1)
            out_list.book_val =  to_decimal(t_val2)


        else:

            mathis_obj_list = {}
            mathis = Mathis()
            fa_artikel = Fa_artikel()
            fa_grup = Fa_grup()
            for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.katnr, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel._recid, fa_grup.bezeich, fa_grup._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.katnr, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel._recid, Fa_grup.bezeich, Fa_grup._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0) & (Fa_artikel.gnr == from_grp)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1) & (Fa_grup.gnr >= from_subgr) & (Fa_grup.gnr <= to_subgr)).filter(
                         (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Fa_artikel.subgrp, Mathis.name).all():
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

                    if zwkum != fa_artikel.subgrp:

                        if zwkum != 0:
                            out_list = Out_list()
                            out_list_data.append(out_list)

                            out_list.refno = "SUB TOTAL"
                            out_list.flag = 1
                            out_list.qty =  to_decimal(t_anz)
                            out_list.init_val =  to_decimal(t_val)
                            out_list.depn_val =  to_decimal(t_val1)
                            out_list.book_val =  to_decimal(t_val2)


                        out_list = Out_list()
                        out_list_data.append(out_list)

                        out_list.bezeich = fa_grup.bezeich
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
                    out_list = Out_list()
                    out_list_data.append(out_list)

                    out_list.flag = 1
                    out_list.refno = mathis.asset
                    out_list.location = trim (mathis.location)
                    out_list.bezeich = mathis.name
                    out_list.received = mathis.datum
                    out_list.qty =  to_decimal(fa_artikel.anzahl)
                    out_list.init_val =  to_decimal(fa_artikel.warenwert)

                    if (fa_artikel.anz_depn - diff_n) == 0:
                        out_list.depn_val =  to_decimal("0")
                        out_list.book_val =  to_decimal(fa_artikel.warenwert)


                    else:
                        out_list.depn_val =  to_decimal(fa_artikel.depn_wert) - to_decimal(diff_wert)
                        out_list.book_val =  to_decimal(fa_artikel.book_wert) + to_decimal(diff_wert)

                    fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_artikel.katnr)]})

                    if fa_kateg:
                        out_list.kateg = fa_kateg.bezeich + " - " + to_string(fa_kateg.rate) + "%"

                    if fa_artikel.first_depn != None:
                        out_list.first_depn = fa_artikel.first_depn

                    if fa_artikel.next_depn != None:
                        out_list.next_depn = fa_artikel.next_depn

                    if fa_artikel.last_depn != None:
                        out_list.last_depn = fa_artikel.last_depn

                    if fa_artikel.anz_depn != None:
                        out_list.depn_no = fa_artikel.anz_depn
            out_list = Out_list()
            out_list_data.append(out_list)

            out_list.refno = "SUB TOTAL"
            out_list.flag = 1
            out_list.qty =  to_decimal(t_anz)
            out_list.init_val =  to_decimal(t_val)
            out_list.depn_val =  to_decimal(t_val1)
            out_list.book_val =  to_decimal(t_val2)

        if tot_anz != 0:
            out_list = Out_list()
            out_list_data.append(out_list)

            out_list = Out_list()
            out_list_data.append(out_list)

            out_list.flag = 2
            out_list.refno = "TOTAL"
            out_list.qty =  to_decimal(tot_anz)
            out_list.init_val =  to_decimal(tot_val)
            out_list.depn_val =  to_decimal(tot_val1)
            out_list.book_val =  to_decimal(tot_val2)


    def create_listacct():

        nonlocal out_list_data, do_it, sub_depn, val_dep, datum, flag, p_depn_wert, p_book_wert, fa_lager, mathis, fa_artikel, fa_grup, fa_kateg, gl_acct, htparam
        nonlocal pvilanguage, mi_lager_chk, mi_subgrp_chk, mi_acct_chk, mi_bookvalue_chk, from_grp, from_date, to_lager, from_lager, maxnr, to_date, zero_value_only, last_acctdate, yy, mm, from_subgr, to_subgr, show_all


        nonlocal lagerbuff, out_list
        nonlocal out_list_data

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
        diff_n = (get_year(last_acctdate) - yy) * 12 + get_month(last_acctdate) - mm

        if mi_bookvalue_chk :

            mathis_obj_list = {}
            mathis = Mathis()
            fa_artikel = Fa_artikel()
            for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.katnr, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.katnr, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).filter(
                     (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Fa_artikel.fibukonto).all():
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

                    if curr_acct != fa_artikel.fibukonto:
                        tot_anz =  to_decimal(tot_anz) + to_decimal(t_anz)
                        tot_oh =  to_decimal(tot_oh) + to_decimal(t_oh)
                        tot_depn =  to_decimal(tot_depn) + to_decimal(t_depn)
                        tot_book =  to_decimal(tot_book) + to_decimal(t_book)

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, curr_acct)]})

                        if gl_acct:
                            fibu = convert_fibu(curr_acct)

                        if curr_acct != "":
                            out_list = Out_list()
                            out_list_data.append(out_list)

                            out_list.location = ""
                            out_list.bezeich = "SUBTOTAL"
                            out_list.qty =  to_decimal(t_anz)
                            out_list.init_val =  to_decimal(t_oh)
                            out_list.depn_val =  to_decimal(t_depn)
                            out_list.book_val =  to_decimal(t_book)


                            out_list = Out_list()
                            out_list_data.append(out_list)

                        curr_acct = fa_artikel.fibukonto
                        t_anz =  to_decimal("0")
                        t_oh =  to_decimal("0")
                        t_depn =  to_decimal("0")
                        t_book =  to_decimal("0")

                    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fa_artikel.fibukonto)]})
                    fibu = convert_fibu(fa_artikel.fibukonto)

                    out_list = query(out_list_data, filters=(lambda out_list: out_list.fibu.lower()  == (fibu).lower()), first=True)

                    if out_list:
                        out_list = Out_list()
                        out_list_data.append(out_list)

                        out_list.flag = 1
                        out_list.refno = mathis.asset
                        out_list.location = mathis.location
                        out_list.bezeich = mathis.name
                        out_list.received = mathis.datum
                        out_list.qty =  to_decimal(fa_artikel.anzahl)


                    else:
                        out_list = Out_list()
                        out_list_data.append(out_list)

                        out_list.flag = 1
                        out_list.refno = mathis.asset
                        out_list.location = trim (mathis.location)
                        out_list.fibu = fibu
                        out_list.bezeich = mathis.name
                        out_list.received = mathis.datum
                        out_list.qty =  to_decimal(fa_artikel.anzahl)


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
                        out_list.init_val =  to_decimal(fa_artikel.warenwert)
                        out_list.depn_val =  to_decimal("0")
                        out_list.book_val =  to_decimal(fa_artikel.warenwert)


                    else:
                        out_list.init_val =  to_decimal(fa_artikel.warenwert)
                        out_list.depn_val =  to_decimal(p_depn_wert) - to_decimal(diff_wert)
                        out_list.book_val =  to_decimal(p_book_wert) + to_decimal(diff_wert)

                    fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_artikel.katnr)]})

                    if fa_kateg:
                        out_list.kateg = fa_kateg.bezeich + " - " + to_string(fa_kateg.rate) + "%"

                    if fa_artikel.first_depn != None:
                        out_list.first_depn = fa_artikel.first_depn

                    if fa_artikel.next_depn != None:
                        out_list.next_depn = fa_artikel.next_depn

                    if fa_artikel.last_depn != None:
                        out_list.last_depn = fa_artikel.last_depn

                    if fa_artikel.anz_depn != None:
                        out_list.depn_no = sub_depn

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
            for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.katnr, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.katnr, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).filter(
                     (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Fa_artikel.fibukonto).all():
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

                    if curr_acct != fa_artikel.fibukonto:
                        tot_anz =  to_decimal(tot_anz) + to_decimal(t_anz)
                        tot_oh =  to_decimal(tot_oh) + to_decimal(t_oh)
                        tot_depn =  to_decimal(tot_depn) + to_decimal(t_depn)
                        tot_book =  to_decimal(tot_book) + to_decimal(t_book)

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, curr_acct)]})

                        if gl_acct:
                            fibu = convert_fibu(curr_acct)

                        if curr_acct != "":
                            out_list = Out_list()
                            out_list_data.append(out_list)

                            out_list.location = ""
                            out_list.bezeich = "SUBTOTAL"
                            out_list.qty =  to_decimal(t_anz)
                            out_list.init_val =  to_decimal(t_oh)
                            out_list.depn_val =  to_decimal(t_depn)
                            out_list.book_val =  to_decimal(t_book)


                            out_list = Out_list()
                            out_list_data.append(out_list)

                        curr_acct = fa_artikel.fibukonto
                        t_anz =  to_decimal("0")
                        t_oh =  to_decimal("0")
                        t_depn =  to_decimal("0")
                        t_book =  to_decimal("0")

                    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fa_artikel.fibukonto)]})
                    fibu = convert_fibu(fa_artikel.fibukonto)

                    out_list = query(out_list_data, filters=(lambda out_list: out_list.fibu.lower()  == (fibu).lower()), first=True)

                    if out_list:
                        out_list = Out_list()
                        out_list_data.append(out_list)

                        out_list.refno = mathis.asset
                        out_list.location = trim (mathis.location)
                        out_list.bezeich = mathis.name
                        out_list.received = mathis.datum
                        out_list.qty =  to_decimal(fa_artikel.anzahl)


                    else:
                        out_list = Out_list()
                        out_list_data.append(out_list)

                        out_list.refno = mathis.asset
                        out_list.location = trim (mathis.location)
                        out_list.bezeich = mathis.name
                        out_list.received = mathis.datum
                        out_list.qty =  to_decimal(fa_artikel.anzahl)
                        out_list.fibu = fibu

                    if (fa_artikel.anz_depn - diff_n) == 0:
                        out_list.init_val =  to_decimal(fa_artikel.warenwert)
                        out_list.depn_val =  to_decimal("0")
                        out_list.book_val =  to_decimal(fa_artikel.warenwert)


                    else:
                        out_list.init_val =  to_decimal(fa_artikel.warenwert)
                        out_list.depn_val =  to_decimal(fa_artikel.depn_wert) - to_decimal(diff_wert)
                        out_list.book_val =  to_decimal(fa_artikel.book_wert) + to_decimal(diff_wert)

                    fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_artikel.katnr)]})

                    if fa_kateg:
                        out_list.kateg = fa_kateg.bezeich + " - " + to_string(fa_kateg.rate) + "%"

                    if fa_artikel.first_depn != None:
                        out_list.first_depn = fa_artikel.first_depn

                    if fa_artikel.next_depn != None:
                        out_list.next_depn = fa_artikel.next_depn

                    if fa_artikel.last_depn != None:
                        out_list.last_depn = fa_artikel.last_depn

                    if fa_artikel.anz_depn != None:
                        out_list.depn_no = fa_artikel.anz_depn

                    if (fa_artikel.anz_depn - diff_n) == 0:
                        t_anz =  to_decimal(t_anz) + to_decimal(fa_artikel.anzahl)
                        t_oh =  to_decimal(t_oh) + to_decimal(fa_artikel.warenwert)
                        t_book =  to_decimal(t_book) + to_decimal(fa_artikel.book_wert)

                    elif fa_artikel.anz_depn - diff_n > 0:

                        fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_artikel.katnr)]})

                        if (fa_kateg.methode == 0):
                            diff_wert = ( to_decimal(fa_artikel.depn_wert) / to_decimal(fa_artikel.anz_depn)) * to_decimal(diff_n)

                            if diff_wert == None:
                                diff_wert =  to_decimal("0")
                            t_anz =  to_decimal(t_anz) + to_decimal(fa_artikel.anzahl)
                            t_oh =  to_decimal(t_oh) + to_decimal(fa_artikel.warenwert)
                            t_depn =  to_decimal(t_depn) + to_decimal(fa_artikel.depn_wert) - to_decimal(diff_wert)
                            t_book =  to_decimal(t_book) + to_decimal(fa_artikel.book_wert) + to_decimal(diff_wert)
        tot_anz =  to_decimal(tot_anz) + to_decimal(t_anz)
        tot_oh =  to_decimal(tot_oh) + to_decimal(t_oh)
        tot_depn =  to_decimal(tot_depn) + to_decimal(t_depn)
        tot_book =  to_decimal(tot_book) + to_decimal(t_book)

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, curr_acct)]})
        fibu = convert_fibu(curr_acct)
        out_list = Out_list()
        out_list_data.append(out_list)

        out_list.bezeich = "SUBTOTAL"
        out_list.flag = 1
        out_list.qty =  to_decimal(t_anz)
        out_list.init_val =  to_decimal(t_oh)
        out_list.depn_val =  to_decimal(t_depn)
        out_list.book_val =  to_decimal(t_book)


        out_list = Out_list()
        out_list_data.append(out_list)

        out_list = Out_list()
        out_list_data.append(out_list)

        out_list.bezeich = "T O T A L"
        out_list.qty =  to_decimal(tot_anz)
        out_list.init_val =  to_decimal(tot_oh)
        out_list.depn_val =  to_decimal(tot_depn)
        out_list.book_val =  to_decimal(tot_book)


    def create_listacct1():

        nonlocal out_list_data, do_it, sub_depn, val_dep, datum, flag, p_depn_wert, p_book_wert, fa_lager, mathis, fa_artikel, fa_grup, fa_kateg, gl_acct, htparam
        nonlocal pvilanguage, mi_lager_chk, mi_subgrp_chk, mi_acct_chk, mi_bookvalue_chk, from_grp, from_date, to_lager, from_lager, maxnr, to_date, zero_value_only, last_acctdate, yy, mm, from_subgr, to_subgr, show_all


        nonlocal lagerbuff, out_list
        nonlocal out_list_data

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
        diff_n = (get_year(last_acctdate) - yy) * 12 + get_month(last_acctdate) - mm

        if mi_bookvalue_chk :

            mathis_obj_list = {}
            mathis = Mathis()
            fa_artikel = Fa_artikel()
            for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.katnr, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.katnr, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0) & (Fa_artikel.gnr == from_grp)).filter(
                     (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Fa_artikel.fibukonto).all():
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

                    if curr_acct != fa_artikel.fibukonto:
                        tot_anz =  to_decimal(tot_anz) + to_decimal(t_anz)
                        tot_oh =  to_decimal(tot_oh) + to_decimal(t_oh)
                        tot_depn =  to_decimal(tot_depn) + to_decimal(t_depn)
                        tot_book =  to_decimal(tot_book) + to_decimal(t_book)

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, curr_acct)]})

                        if gl_acct:
                            fibu = convert_fibu(curr_acct)

                        if curr_acct != "":
                            out_list = Out_list()
                            out_list_data.append(out_list)

                            out_list.location = ""
                            out_list.bezeich = "SUBTOTAL"
                            out_list.qty =  to_decimal(t_anz)
                            out_list.init_val =  to_decimal(t_oh)
                            out_list.depn_val =  to_decimal(t_depn)
                            out_list.book_val =  to_decimal(t_book)


                            out_list = Out_list()
                            out_list_data.append(out_list)

                        curr_acct = fa_artikel.fibukonto
                        t_anz =  to_decimal("0")
                        t_oh =  to_decimal("0")
                        t_depn =  to_decimal("0")
                        t_book =  to_decimal("0")

                    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fa_artikel.fibukonto)]})
                    fibu = convert_fibu(fa_artikel.fibukonto)

                    out_list = query(out_list_data, filters=(lambda out_list: out_list.fibu.lower()  == (fibu).lower()), first=True)

                    if out_list:
                        out_list = Out_list()
                        out_list_data.append(out_list)

                        out_list.flag = 1
                        out_list.refno = mathis.asset
                        out_list.location = mathis.location
                        out_list.bezeich = mathis.name
                        out_list.received = mathis.datum
                        out_list.qty =  to_decimal(fa_artikel.anzahl)


                    else:
                        out_list = Out_list()
                        out_list_data.append(out_list)

                        out_list.flag = 1
                        out_list.refno = mathis.asset
                        out_list.location = trim (mathis.location)
                        out_list.fibu = fibu
                        out_list.bezeich = mathis.name
                        out_list.received = mathis.datum
                        out_list.qty =  to_decimal(fa_artikel.anzahl)


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
                        out_list.init_val =  to_decimal(fa_artikel.warenwert)
                        out_list.depn_val =  to_decimal("0")
                        out_list.book_val =  to_decimal(fa_artikel.warenwert)


                    else:
                        out_list.init_val =  to_decimal(fa_artikel.warenwert)
                        out_list.depn_val =  to_decimal(p_depn_wert) - to_decimal(diff_wert)
                        out_list.book_val =  to_decimal(p_book_wert) + to_decimal(diff_wert)

                    fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_artikel.katnr)]})

                    if fa_kateg:
                        out_list.kateg = fa_kateg.bezeich + " - " + to_string(fa_kateg.rate) + "%"

                    if fa_artikel.first_depn != None:
                        out_list.first_depn = fa_artikel.first_depn

                    if fa_artikel.next_depn != None:
                        out_list.next_depn = fa_artikel.next_depn

                    if fa_artikel.last_depn != None:
                        out_list.last_depn = fa_artikel.last_depn

                    if fa_artikel.anz_depn != None:
                        out_list.depn_no = sub_depn

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
            for mathis.asset, mathis.name, mathis.datum, mathis.location, mathis._recid, fa_artikel.book_wert, fa_artikel.gnr, fa_artikel.anzahl, fa_artikel.depn_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel.last_depn, fa_artikel.warenwert, fa_artikel.katnr, fa_artikel.next_depn, fa_artikel.subgrp, fa_artikel.fibukonto, fa_artikel._recid in db_session.query(Mathis.asset, Mathis.name, Mathis.datum, Mathis.location, Mathis._recid, Fa_artikel.book_wert, Fa_artikel.gnr, Fa_artikel.anzahl, Fa_artikel.depn_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel.last_depn, Fa_artikel.warenwert, Fa_artikel.katnr, Fa_artikel.next_depn, Fa_artikel.subgrp, Fa_artikel.fibukonto, Fa_artikel._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0) & (Fa_artikel.gnr == from_grp)).filter(
                     (Mathis.datum >= from_date) & (Mathis.datum <= to_date)).order_by(Fa_artikel.fibukonto).all():
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

                    if curr_acct != fa_artikel.fibukonto:
                        tot_anz =  to_decimal(tot_anz) + to_decimal(t_anz)
                        tot_oh =  to_decimal(tot_oh) + to_decimal(t_oh)
                        tot_depn =  to_decimal(tot_depn) + to_decimal(t_depn)
                        tot_book =  to_decimal(tot_book) + to_decimal(t_book)

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, curr_acct)]})

                        if gl_acct:
                            fibu = convert_fibu(curr_acct)

                        if curr_acct != "":
                            out_list = Out_list()
                            out_list_data.append(out_list)

                            out_list.location = ""
                            out_list.bezeich = "SUBTOTAL"
                            out_list.qty =  to_decimal(t_anz)
                            out_list.init_val =  to_decimal(t_oh)
                            out_list.depn_val =  to_decimal(t_depn)
                            out_list.book_val =  to_decimal(t_book)


                            out_list = Out_list()
                            out_list_data.append(out_list)

                        curr_acct = fa_artikel.fibukonto
                        t_anz =  to_decimal("0")
                        t_oh =  to_decimal("0")
                        t_depn =  to_decimal("0")
                        t_book =  to_decimal("0")

                    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fa_artikel.fibukonto)]})
                    fibu = convert_fibu(fa_artikel.fibukonto)

                    out_list = query(out_list_data, filters=(lambda out_list: out_list.fibu.lower()  == (fibu).lower()), first=True)

                    if out_list:
                        out_list = Out_list()
                        out_list_data.append(out_list)

                        out_list.refno = mathis.asset
                        out_list.location = trim (mathis.location)
                        out_list.bezeich = mathis.name
                        out_list.received = mathis.datum
                        out_list.qty =  to_decimal(fa_artikel.anzahl)


                    else:
                        out_list = Out_list()
                        out_list_data.append(out_list)

                        out_list.refno = mathis.asset
                        out_list.location = trim (mathis.location)
                        out_list.bezeich = mathis.name
                        out_list.received = mathis.datum
                        out_list.qty =  to_decimal(fa_artikel.anzahl)
                        out_list.fibu = fibu

                    if (fa_artikel.anz_depn - diff_n) == 0:
                        out_list.init_val =  to_decimal(fa_artikel.warenwert)
                        out_list.depn_val =  to_decimal("0")
                        out_list.book_val =  to_decimal(fa_artikel.warenwert)


                    else:
                        out_list.init_val =  to_decimal(fa_artikel.warenwert)
                        out_list.depn_val =  to_decimal(fa_artikel.depn_wert) - to_decimal(diff_wert)
                        out_list.book_val =  to_decimal(fa_artikel.book_wert) + to_decimal(diff_wert)

                    fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_artikel.katnr)]})

                    if fa_kateg:
                        out_list.kateg = fa_kateg.bezeich + " - " + to_string(fa_kateg.rate) + "%"

                    if fa_artikel.first_depn != None:
                        out_list.first_depn = fa_artikel.first_depn

                    if fa_artikel.next_depn != None:
                        out_list.next_depn = fa_artikel.next_depn

                    if fa_artikel.last_depn != None:
                        out_list.last_depn = fa_artikel.last_depn

                    if fa_artikel.anz_depn != None:
                        out_list.depn_no = fa_artikel.anz_depn

                    if (fa_artikel.anz_depn - diff_n) == 0:
                        t_anz =  to_decimal(t_anz) + to_decimal(fa_artikel.anzahl)
                        t_oh =  to_decimal(t_oh) + to_decimal(fa_artikel.warenwert)
                        t_book =  to_decimal(t_book) + to_decimal(fa_artikel.book_wert)

                    elif fa_artikel.anz_depn - diff_n > 0:

                        fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_artikel.katnr)]})

                        if (fa_kateg.methode == 0):
                            diff_wert = ( to_decimal(fa_artikel.depn_wert) / to_decimal(fa_artikel.anz_depn)) * to_decimal(diff_n)

                            if diff_wert == None:
                                diff_wert =  to_decimal("0")
                            t_anz =  to_decimal(t_anz) + to_decimal(fa_artikel.anzahl)
                            t_oh =  to_decimal(t_oh) + to_decimal(fa_artikel.warenwert)
                            t_depn =  to_decimal(t_depn) + to_decimal(fa_artikel.depn_wert) - to_decimal(diff_wert)
                            t_book =  to_decimal(t_book) + to_decimal(fa_artikel.book_wert) + to_decimal(diff_wert)
        tot_anz =  to_decimal(tot_anz) + to_decimal(t_anz)
        tot_oh =  to_decimal(tot_oh) + to_decimal(t_oh)
        tot_depn =  to_decimal(tot_depn) + to_decimal(t_depn)
        tot_book =  to_decimal(tot_book) + to_decimal(t_book)

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, curr_acct)]})
        fibu = convert_fibu(curr_acct)
        out_list = Out_list()
        out_list_data.append(out_list)

        out_list.bezeich = "SUBTOTAL"
        out_list.flag = 1
        out_list.qty =  to_decimal(t_anz)
        out_list.init_val =  to_decimal(t_oh)
        out_list.depn_val =  to_decimal(t_depn)
        out_list.book_val =  to_decimal(t_book)


        out_list = Out_list()
        out_list_data.append(out_list)

        out_list = Out_list()
        out_list_data.append(out_list)

        out_list.bezeich = "T O T A L"
        out_list.qty =  to_decimal(tot_anz)
        out_list.init_val =  to_decimal(tot_oh)
        out_list.depn_val =  to_decimal(tot_depn)
        out_list.book_val =  to_decimal(tot_book)


    def convert_fibu(konto:string):

        nonlocal out_list_data, do_it, sub_depn, val_dep, datum, flag, p_depn_wert, p_book_wert, fa_lager, mathis, fa_artikel, fa_grup, fa_kateg, gl_acct, htparam
        nonlocal pvilanguage, mi_lager_chk, mi_subgrp_chk, mi_acct_chk, mi_bookvalue_chk, from_grp, from_date, to_lager, from_lager, maxnr, to_date, zero_value_only, last_acctdate, yy, mm, from_subgr, to_subgr, show_all


        nonlocal lagerbuff, out_list
        nonlocal out_list_data

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


    def asset_show_handler():

        nonlocal out_list_data, do_it, sub_depn, val_dep, datum, flag, p_depn_wert, p_book_wert, fa_lager, mathis, fa_artikel, fa_grup, fa_kateg, gl_acct, htparam
        nonlocal pvilanguage, mi_lager_chk, mi_subgrp_chk, mi_acct_chk, mi_bookvalue_chk, from_grp, from_date, to_lager, from_lager, maxnr, to_date, zero_value_only, last_acctdate, yy, mm, from_subgr, to_subgr, show_all


        nonlocal lagerbuff, out_list
        nonlocal out_list_data

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

        if from_grp == 0:
            create_listsgrp()
        else:
            create_listsgrp1()

    elif mi_acct_chk :

        if from_grp == 0:
            create_listacct()
        else:
            create_listacct1()

    return generate_output()