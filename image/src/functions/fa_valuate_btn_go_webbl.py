from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Fa_lager, Mathis, Fa_artikel, Fa_grup, Gl_acct, Fa_kateg, Htparam

lagerbuff_list, Lagerbuff = create_model_like(Fa_lager)
out_list_list, Out_list = create_model("Out_list", {"flag":int, "fibu":str, "bezeich":str, "refno":str, "location":str, "received":date, "qty":decimal, "init_val":decimal, "depn_val":decimal, "book_val":decimal, "depn_no":int, "first_depn":date, "next_depn":date, "last_depn":date})

def fa_valuate_btn_go_webbl(pvilanguage:int, lagerbuff:[Lagerbuff], mi_lager_chk:bool, mi_subgrp_chk:bool, mi_acct_chk:bool, mi_bookvalue_chk:bool, from_grp:int, from_date:date, to_lager:int, from_lager:int, maxnr:int, to_date:date, zero_value_only:bool, last_acctdate:date, yy:int, mm:int, from_subgr:int, to_subgr:int):
    out_list_list = []
    do_it:bool = False
    sub_depn:int = 0
    val_dep:decimal = 0
    datum:date = None
    flag:bool = False
    p_depn_wert:decimal = 0
    p_book_wert:decimal = 0
    fa_lager = mathis = fa_artikel = fa_grup = gl_acct = fa_kateg = htparam = None

    lagerbuff = out_list = l_oh = None

    
    L_oh = Mathis

    db_session = local_storage.db_session

    def generate_output():
        nonlocal out_list_list, do_it, sub_depn, val_dep, datum, flag, p_depn_wert, p_book_wert, fa_lager, mathis, fa_artikel, fa_grup, gl_acct, fa_kateg, htparam
        nonlocal l_oh


        nonlocal lagerbuff, out_list, l_oh
        nonlocal lagerbuff_list, out_list_list
        return {"out-list": out_list_list}

    def create_list():

        nonlocal out_list_list, do_it, sub_depn, val_dep, datum, flag, p_depn_wert, p_book_wert, fa_lager, mathis, fa_artikel, fa_grup, gl_acct, fa_kateg, htparam
        nonlocal l_oh


        nonlocal lagerbuff, out_list, l_oh
        nonlocal lagerbuff_list, out_list_list

        i:int = 0
        j:int = 0
        t_anz:decimal = 0
        t_val:decimal = 0
        t_val1:decimal = 0
        t_val2:decimal = 0
        tt_anz:decimal = 0
        tt_val:decimal = 0
        tt_val1:decimal = 0
        tt_val2:decimal = 0
        tot_anz:decimal = 0
        tot_val:decimal = 0
        tot_val1:decimal = 0
        tot_val2:decimal = 0
        zwkum:int = 0
        bezeich:str = ""
        qty:decimal = 0
        wert:decimal = 0
        max_lager:int = 0
        L_oh = Mathis
        tot_anz = 0
        tot_val = 0
        tot_val1 = 0
        tot_val2 = 0


        max_lager = to_lager

        if from_lager != to_lager and (maxnr - 1) == to_lager:
            max_lager = maxnr

        for lagerbuff in query(lagerbuff_list, filters=(lambda lagerbuff :lagerBuff.lager_nr >= from_lager and lagerBuff.lager_nr <= maxnr)):
            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.bezeich = to_string(lagerBuff.lager_nr, ">>99") + "-" + lagerBuff.bezeich
            i = 0
            zwkum = 0
            t_anz = 0
            t_val = 0
            t_val1 = 0
            t_val2 = 0
            tt_anz = 0
            tt_val = 0
            tt_val1 = 0
            tt_val2 = 0

            if mi_bookvalue_chk :

                mathis_obj_list = []
                for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr)).join(Fa_grup,(Fa_grup.gnr == fa_artikel.gnr) &  (Fa_grup.flag == 0)).filter(
                        (Mathis.location == lagerBuff.bezeich) &  (Mathis.datum >= from_date) &  (Mathis.datum <= to_date)).all():
                    if mathis._recid in mathis_obj_list:
                        continue
                    else:
                        mathis_obj_list.append(mathis._recid)


                    do_it = False

                    if not zero_value_only:
                        do_it = True
                    else:
                        do_it = fa_artikel.book_wert == 0

                    if do_it:

                        if zwkum != fa_artikel.gnr:

                            if zwkum != 0:
                                out_list = Out_list()
                                out_list_list.append(out_list)

                                out_list.flag = 1
                                out_list.refno = "SUB TOTAL"
                                out_list.qty = t_anz
                                out_list.init_val = t_val
                                out_list.depn_val = t_val1
                                out_list.book_val = t_val2


                            out_list = Out_list()
                            out_list_list.append(out_list)

                            out_list.bezeich = fa_grup.bezeich
                            t_anz = 0
                            t_val = 0
                            t_val1 = 0
                            t_val2 = 0
                            zwkum = fa_artikel.gnr


                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.flag = 1
                        out_list.refno = mathis.asset
                        out_list.bezeich = mathis.name
                        out_list.received = mathis.datum
                        out_list.qty = fa_artikel.anzahl


                        val_dep = fa_artikel.depn_wert / fa_artikel.anz_depn
                        sub_depn = 0
                        flag = False

                        if val_dep == None:
                            val_dep = 0
                        for datum in range(from_date,to_date + 1) :

                            if flag and datum == date_mdy(get_month(datum) + 1, 1, get_year(datum)) - 1:
                                sub_depn = sub_depn + 1

                            if datum == fa_artikel.first_depn:
                                sub_depn = sub_depn + 1
                                flag = True

                            if datum == fa_artikel.last_depn:
                                break
                        p_depn_wert = val_dep * sub_depn
                        p_book_wert = fa_artikel.warenwert - p_depn_wert
                        i = i + 1
                        t_anz = t_anz + fa_artikel.anzahl
                        t_val = t_val + fa_artikel.warenwert
                        t_val1 = t_val1 + p_depn_wert
                        t_val2 = t_val2 + p_book_wert
                        tt_anz = tt_anz + fa_artikel.anzahl
                        tt_val = tt_val + fa_artikel.warenwert
                        tt_val1 = tt_val1 + p_depn_wert
                        tt_val2 = tt_val2 + p_book_wert
                        tot_anz = tot_anz + fa_artikel.anzahl
                        tot_val = tot_val + fa_artikel.warenwert
                        tot_val1 = tot_val1 + p_depn_wert
                        tot_val2 = tot_val2 + p_book_wert
                        out_list.init_val = fa_artikel.warenwert
                        out_list.depn_val = p_depn_wert
                        out_list.book_val = p_book_wert

                        if fa_artikel.first_depn != None:
                            out_list.first_depn = fa_artikel.first_depn

                        if fa_artikel.next_depn != None:
                            out_list.next_depn = fa_artikel.next_depn

                        if fa_artikel.last_depn != None:
                            out_list.last_depn = fa_artikel.last_depn

                        if fa_artikel.anz_depn != None:
                            out_list.depn_no = sub_depn
            else:

                mathis_obj_list = []
                for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr)).join(Fa_grup,(Fa_grup.gnr == fa_artikel.gnr) &  (Fa_grup.flag == 0)).filter(
                        (Mathis.location == lagerBuff.bezeich) &  (Mathis.datum >= from_date) &  (Mathis.datum <= to_date)).all():
                    if mathis._recid in mathis_obj_list:
                        continue
                    else:
                        mathis_obj_list.append(mathis._recid)


                    do_it = False

                    if not zero_value_only:
                        do_it = True
                    else:
                        do_it = fa_artikel.book_wert == 0

                    if do_it:

                        if zwkum != fa_artikel.gnr:

                            if zwkum != 0:
                                out_list = Out_list()
                                out_list_list.append(out_list)

                                out_list.flag = 1
                                out_list.refno = "SUB TOTAL"
                                out_list.qty = t_anz
                                out_list.init_val = t_val
                                out_list.depn_val = t_val1
                                out_list.book_val = t_val2


                            out_list = Out_list()
                            out_list_list.append(out_list)

                            out_list.bezeich = fa_grup.bezeich
                            t_anz = 0
                            t_val = 0
                            t_val1 = 0
                            t_val2 = 0
                            zwkum = fa_artikel.gnr


                        i = i + 1
                        t_anz = t_anz + fa_artikel.anzahl
                        t_val = t_val + fa_artikel.warenwert
                        t_val1 = t_val1 + fa_artikel.depn_wert
                        t_val2 = t_val2 + fa_artikel.book_wert
                        tt_anz = tt_anz + fa_artikel.anzahl
                        tt_val = tt_val + fa_artikel.warenwert
                        tt_val1 = tt_val1 + fa_artikel.depn_wert
                        tt_val2 = tt_val2 + fa_artikel.book_wert
                        tot_anz = tot_anz + fa_artikel.anzahl
                        tot_val = tot_val + fa_artikel.warenwert
                        tot_val1 = tot_val1 + fa_artikel.depn_wert
                        tot_val2 = tot_val2 + fa_artikel.book_wert


                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.flag = 1
                        out_list.bezeich = mathis.name
                        out_list.refno = mathis.asset
                        out_list.received = mathis.datum
                        out_list.qty = fa_artikel.anzahl
                        out_list.init_val = fa_artikel.warenwert
                        out_list.depn_val = depn_wert
                        out_list.book_val = book_wert

                        if fa_artikel.first_depn != None:
                            out_list.first_depn = fa_artikel.first_depn

                        if fa_artikel.next_depn != None:
                            out_list.next_depn = fa_artikel.next_depn

                        if fa_artikel.last_depn != None:
                            out_list.last_depn = fa_artikel.last_depn

                        if fa_artikel.anz_depn != None:
                            out_list.depn_no = fa_artikel.anz_depn

            if t_anz != 0:
                out_list = Out_list()
                out_list_list.append(out_list)

                out_list.flag = 1
                out_list.refno = "SUB TOTAL"
                out_list.qty = t_anz
                out_list.init_val = t_val
                out_list.depn_val = t_val1
                out_list.book_val = t_val2

            if i > 0:
                out_list = Out_list()
                out_list_list.append(out_list)

                out_list.refno = "T O T A L"
                out_list.flag = 1
                out_list.qty = tt_anz
                out_list.init_val = tt_val
                out_list.depn_val = tt_val1
                out_list.book_val = tt_val2

        if from_lager != to_lager and tot_anz != 0:
            out_list = Out_list()
            out_list_list.append(out_list)

            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.flag = 2
            out_list.refno = "GRAND TOTAL"
            out_list.qty = tot_anz
            out_list.init_val = tot_val
            out_list.depn_val = tot_val1
            out_list.book_val = tot_val2

    def create_list0():

        nonlocal out_list_list, do_it, sub_depn, val_dep, datum, flag, p_depn_wert, p_book_wert, fa_lager, mathis, fa_artikel, fa_grup, gl_acct, fa_kateg, htparam
        nonlocal l_oh


        nonlocal lagerbuff, out_list, l_oh
        nonlocal lagerbuff_list, out_list_list

        i:int = 0
        j:int = 0
        t_anz:decimal = 0
        t_val:decimal = 0
        t_val1:decimal = 0
        t_val2:decimal = 0
        tt_anz:decimal = 0
        tt_val:decimal = 0
        tt_val1:decimal = 0
        tt_val2:decimal = 0
        tot_anz:decimal = 0
        tot_val:decimal = 0
        tot_val1:decimal = 0
        tot_val2:decimal = 0
        zwkum:int = 0
        bezeich:str = ""
        qty:decimal = 0
        wert:decimal = 0
        max_lager:int = 0
        L_oh = Mathis
        tot_anz = 0
        tot_val = 0
        tot_val1 = 0
        tot_val2 = 0
        max_lager = to_lager

        if from_lager != to_lager and (maxnr - 1) == to_lager:
            max_lager = maxnr

        for lagerbuff in query(lagerbuff_list, filters=(lambda lagerbuff :lagerBuff.lager_nr >= from_lager and lagerBuff.lager_nr <= maxnr)):
            out_list = Out_list()
            out_list_list.append(out_list)

            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.bezeich = to_string(lagerBuff.lager_nr, ">>99") + "-" + lagerBuff.bezeich
            i = 0
            zwkum = 0
            t_anz = 0
            t_val = 0
            t_val1 = 0
            t_val2 = 0
            tt_anz = 0
            tt_val = 0
            tt_val1 = 0
            tt_val2 = 0

            if mi_bookvalue_chk :

                mathis_obj_list = []
                for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) &  (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == fa_artikel.gnr) &  (Fa_grup.flag == 0)).filter(
                        (Mathis.location == lagerBuff.bezeich) &  (Mathis.datum >= from_date) &  (Mathis.datum <= to_date)).all():
                    if mathis._recid in mathis_obj_list:
                        continue
                    else:
                        mathis_obj_list.append(mathis._recid)


                    do_it = False

                    if not zero_value_only:
                        do_it = True
                    else:
                        do_it = fa_artikel.book_wert == 0

                    if do_it:

                        if zwkum != fa_artikel.gnr:

                            if zwkum != 0:
                                out_list = Out_list()
                                out_list_list.append(out_list)

                                out_list.flag = 1
                                out_list.refno = "SUB TOTAL"
                                out_list.qty = t_anz
                                out_list.init_val = t_val
                                out_list.depn_val = t_val1
                                out_list.book_val = t_val2


                            out_list = Out_list()
                            out_list_list.append(out_list)

                            out_list.bezeich = fa_grup.bezeich
                            t_anz = 0
                            t_val = 0
                            t_val1 = 0
                            t_val2 = 0
                            zwkum = fa_artikel.gnr


                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.flag = 1
                        out_list.refno = mathis.asset
                        out_list.bezeich = mathis.name
                        out_list.received = mathis.datum
                        out_list.qty = fa_artikel.anzahl


                        val_dep = fa_artikel.depn_wert / fa_artikel.anz_depn
                        sub_depn = 0
                        flag = False

                        if val_dep == None:
                            val_dep = 0
                        for datum in range(from_date,to_date + 1) :

                            if flag and datum == date_mdy(get_month(datum) + 1, 1, get_year(datum)) - 1:
                                sub_depn = sub_depn + 1

                            if datum == fa_artikel.first_depn:
                                sub_depn = sub_depn + 1
                                flag = True

                            if datum == fa_artikel.last_depn:
                                break
                        p_depn_wert = val_dep * sub_depn
                        p_book_wert = fa_artikel.warenwert - p_depn_wert
                        i = i + 1
                        t_anz = t_anz + fa_artikel.anzahl
                        t_val = t_val + fa_artikel.warenwert
                        t_val1 = t_val1 + p_depn_wert
                        t_val2 = t_val2 + p_book_wert
                        tt_anz = tt_anz + fa_artikel.anzahl
                        tt_val = tt_val + fa_artikel.warenwert
                        tt_val1 = tt_val1 + p_depn_wert
                        tt_val2 = tt_val2 + p_book_wert
                        tot_anz = tot_anz + fa_artikel.anzahl
                        tot_val = tot_val + fa_artikel.warenwert
                        tot_val1 = tot_val1 + p_depn_wert
                        tot_val2 = tot_val2 + p_book_wert
                        out_list.init_val = fa_artikel.warenwert
                        out_list.depn_val = p_depn_wert
                        out_list.book_val = p_book_wert

                        if fa_artikel.first_depn != None:
                            out_list.first_depn = fa_artikel.first_depn

                        if fa_artikel.next_depn != None:
                            out_list.next_depn = fa_artikel.next_depn

                        if fa_artikel.last_depn != None:
                            out_list.last_depn = fa_artikel.last_depn

                        if fa_artikel.anz_depn != None:
                            out_list.depn_no = sub_depn
            else:

                mathis_obj_list = []
                for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) &  (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == fa_artikel.gnr) &  (Fa_grup.flag == 0)).filter(
                        (Mathis.location == lagerBuff.bezeich) &  (Mathis.datum >= from_date) &  (Mathis.datum <= to_date)).all():
                    if mathis._recid in mathis_obj_list:
                        continue
                    else:
                        mathis_obj_list.append(mathis._recid)


                    do_it = False

                    if not zero_value_only:
                        do_it = True
                    else:
                        do_it = fa_artikel.book_wert == 0

                    if do_it:

                        if zwkum != fa_artikel.gnr:

                            if zwkum != 0:
                                out_list = Out_list()
                                out_list_list.append(out_list)

                                out_list.refno = "SUB TOTAL"
                                out_list.flag = 1
                                out_list.qty = t_anz
                                out_list.init_val = t_val
                                out_list.depn_val = t_val1
                                out_list.book_val = t_val2


                            out_list = Out_list()
                            out_list_list.append(out_list)

                            out_list.bezeich = fa_grup.bezeich
                            t_anz = 0
                            t_val = 0
                            t_val1 = 0
                            t_val2 = 0
                            zwkum = fa_artikel.gnr


                        i = i + 1
                        t_anz = t_anz + fa_artikel.anzahl
                        t_val = t_val + fa_artikel.warenwert
                        t_val1 = t_val1 + fa_artikel.depn_wert
                        t_val2 = t_val2 + fa_artikel.book_wert
                        tt_anz = tt_anz + fa_artikel.anzahl
                        tt_val = tt_val + fa_artikel.warenwert
                        tt_val1 = tt_val1 + fa_artikel.depn_wert
                        tt_val2 = tt_val2 + fa_artikel.book_wert
                        tot_anz = tot_anz + fa_artikel.anzahl
                        tot_val = tot_val + fa_artikel.warenwert
                        tot_val1 = tot_val1 + fa_artikel.depn_wert
                        tot_val2 = tot_val2 + fa_artikel.book_wert


                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.flag = 1
                        out_list.bezeich = mathis.name
                        out_list.refno = mathis.asset
                        out_list.received = mathis.datu
                        out_list.qty = fa_artikel.anzahl
                        out_list.init_val = fa_artikel.warenwert
                        out_list.depn_val = fa_artikel.depn_wert
                        out_list.book_val = fa_artikel.book_wert

                        if fa_artikel.first_depn != None:
                            out_list.first_depn = fa_artikel.first_depn

                        if fa_artikel.next_depn != None:
                            out_list.next_depn = fa_artikel.next_depn

                        if fa_artikel.last_depn != None:
                            out_list.last_depn = fa_artikel.last_depn

                        if fa_artikel.anz_depn != None:
                            out_list.depn_no = fa_artikel.anz_depn

            if t_anz != 0:
                out_list = Out_list()
                out_list_list.append(out_list)

                out_list.refno = "SUB TOTAL"
                out_list.flag = 1
                out_list.qty = t_anz
                out_list.init_val = t_val
                out_list.depn_val = t_val1
                out_list.book_val = t_val2

            if i > 0:
                out_list = Out_list()
                out_list_list.append(out_list)

                out_list.refno = "T O T A L"
                out_list.flag = 1
                out_list.qty = tt_anz
                out_list.init_val = tt_val
                out_list.depn_val = tt_val1
                out_list.book_val = tt_val2

        if from_lager != to_lager and tot_anz != 0:
            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.flag = 2
            out_list.refno = "GRAND TOTAL"
            out_list.qty = tot_anz
            out_list.init_val = tot_val
            out_list.depn_val = tot_val1
            out_list.book_val = tot_val2

    def create_list1():

        nonlocal out_list_list, do_it, sub_depn, val_dep, datum, flag, p_depn_wert, p_book_wert, fa_lager, mathis, fa_artikel, fa_grup, gl_acct, fa_kateg, htparam
        nonlocal l_oh


        nonlocal lagerbuff, out_list, l_oh
        nonlocal lagerbuff_list, out_list_list

        i:int = 0
        j:int = 0
        t_anz:decimal = 0
        t_val:decimal = 0
        t_val1:decimal = 0
        t_val2:decimal = 0
        tt_anz:decimal = 0
        tt_val:decimal = 0
        tt_val1:decimal = 0
        tt_val2:decimal = 0
        tot_anz:decimal = 0
        tot_val:decimal = 0
        tot_val1:decimal = 0
        tot_val2:decimal = 0
        zwkum:int = 0
        bezeich:str = ""
        qty:decimal = 0
        wert:decimal = 0
        L_oh = Mathis
        tot_anz = 0
        tot_val = 0
        tot_val1 = 0
        tot_val2 = 0

        fa_grup = db_session.query(Fa_grup).filter(
                (Fa_grup.gnr == from_grp) &  (Fa_grup.flag == 0)).first()

        for lagerbuff in query(lagerbuff_list, filters=(lambda lagerbuff :lagerBuff.lager_nr >= from_lager and lagerBuff.lager_nr <= to_lager)):
            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.bezeich = to_string(lagerBuff.lager_nr, ">>99") + "-" + lagerBuff.bezeich


            i = 0
            zwkum = 0
            t_anz = 0
            t_val = 0
            t_val1 = 0
            t_val2 = 0
            tt_anz = 0
            tt_val = 0
            tt_val1 = 0
            tt_val2 = 0

            if mi_bookvalue_chk :

                mathis_obj_list = []
                for mathis, fa_artikel in db_session.query(Mathis, Fa_artikel).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) &  (Fa_artikel.loeschflag == 0) &  (Fa_artikel.gnr == from_grp)).filter(
                        (Mathis.location == lagerBuff.bezeich) &  (Mathis.datum >= from_date) &  (Mathis.datum <= to_date)).all():
                    if mathis._recid in mathis_obj_list:
                        continue
                    else:
                        mathis_obj_list.append(mathis._recid)


                    do_it = False

                    if not zero_value_only:
                        do_it = True
                    else:
                        do_it = fa_artikel.book_wert == 0

                    if do_it:

                        if zwkum != fa_artikel.gnr:

                            if zwkum != 0:
                                out_list = Out_list()
                                out_list_list.append(out_list)

                                out_list.refno = "SUB TOTAL"
                                out_list.flag = 1
                                out_list.qty = t_anz
                                out_list.init_val = t_val
                                out_list.depn_val = t_val1
                                out_list.book_val = t_val2


                            out_list = Out_list()
                            out_list_list.append(out_list)

                            out_list.bezeich = fa_grup.bezeich
                            t_anz = 0
                            t_val = 0
                            t_val1 = 0
                            t_val2 = 0
                            zwkum = fa_artikel.gnr


                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.refno = mathis.asset
                        out_list.flag = 1
                        out_list.bezeich = mathis.name
                        out_list.received = mathis.datum
                        out_list.qty = fa_artikel.anzahl
                        val_dep = fa_artikel.depn_wert / fa_artikel.anz_depn
                        sub_depn = 0
                        flag = False

                        if val_dep == None:
                            val_dep = 0
                        for datum in range(from_date,to_date + 1) :

                            if flag and datum == date_mdy(get_month(datum) + 1, 1, get_year(datum)) - 1:
                                sub_depn = sub_depn + 1

                            if datum == fa_artikel.first_depn:
                                sub_depn = sub_depn + 1
                                flag = True

                            if datum == fa_artikel.last_depn:
                                break
                        p_depn_wert = val_dep * sub_depn
                        p_book_wert = fa_artikel.warenwert - p_depn_wert
                        i = i + 1
                        t_anz = t_anz + fa_artikel.anzahl
                        t_val = t_val + fa_artikel.warenwert
                        t_val1 = t_val1 + p_depn_wert
                        t_val2 = t_val2 + p_book_wert
                        tt_anz = tt_anz + fa_artikel.anzahl
                        tt_val = tt_val + fa_artikel.warenwert
                        tt_val1 = tt_val1 + p_depn_wert
                        tt_val2 = tt_val2 + p_book_wert
                        tot_anz = tot_anz + fa_artikel.anzahl
                        tot_val = tot_val + fa_artikel.warenwert
                        tot_val1 = tot_val1 + p_depn_wert
                        tot_val2 = tot_val2 + p_book_wert
                        out_list.init_val = fa_artikel.warenwert
                        out_list.depn_val = p_depn_wert
                        out_list.book_val = p_book_wert

                        if fa_artikel.first_depn != None:
                            out_list.first_depn = fa_artikel.first_depn

                        if fa_artikel.next_depn != None:
                            out_list.next_depn = fa_artikel.next_depn

                        if fa_artikel.last_depn != None:
                            out_list.last_depn = fa_artikel.last_depn

                        if fa_artikel.anz_depn != None:
                            out_list.depn_no = sub_depn

                    if t_anz != 0:
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.refno = "SUB TOTAL"
                        out_list.flag = 1
                        out_list.qty = t_anz
                        out_list.init_val = t_val
                        out_list.depn_val = t_val1
                        out_list.book_val = t_val2

                    if i > 0:
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.refno = "T O T A L"
                        out_list.flag = 1
                        out_list.qty = tt_anz
                        out_list.init_val = tt_val
                        out_list.depn_val = tt_val1
                        out_list.book_val = tt_val2


            else:

                mathis_obj_list = []
                for mathis, fa_artikel in db_session.query(Mathis, Fa_artikel).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) &  (Fa_artikel.loeschflag == 0) &  (Fa_artikel.gnr == from_grp)).filter(
                        (Mathis.location == lagerBuff.bezeich) &  (Mathis.datum >= from_date) &  (Mathis.datum <= to_date)).all():
                    if mathis._recid in mathis_obj_list:
                        continue
                    else:
                        mathis_obj_list.append(mathis._recid)


                    do_it = False

                    if not zero_value_only:
                        do_it = True
                    else:
                        do_it = fa_artikel.book_wert == 0

                    if do_it:

                        if zwkum != fa_artikel.gnr:

                            if zwkum != 0:
                                out_list = Out_list()
                                out_list_list.append(out_list)

                                out_list.refno = "SUB TOTAL"
                                out_list.flag = 1
                                out_list.qty = t_anz
                                out_list.init_val = t_val
                                out_list.depn_val = t_val1
                                out_list.book_val = t_val2


                            out_list = Out_list()
                            out_list_list.append(out_list)

                            out_list.bezeich = fa_grup.bezeich
                            t_anz = 0
                            t_val = 0
                            t_val1 = 0
                            t_val2 = 0
                            zwkum = fa_artikel.gnr


                        i = i + 1
                        t_anz = t_anz + fa_artikel.anzahl
                        t_val = t_val + fa_artikel.warenwert
                        t_val1 = t_val1 + fa_artikel.depn_wert
                        t_val2 = t_val2 + fa_artikel.book_wert
                        tt_anz = tt_anz + fa_artikel.anzahl
                        tt_val = tt_val + fa_artikel.warenwert
                        tt_val1 = tt_val1 + fa_artikel.depn_wert
                        tt_val2 = tt_val2 + fa_artikel.book_wert
                        tot_anz = tot_anz + fa_artikel.anzahl
                        tot_val = tot_val + fa_artikel.warenwert
                        tot_val1 = tot_val1 + fa_artikel.depn_wert
                        tot_val2 = tot_val2 + fa_artikel.book_wert


                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.flag = 1
                        out_list.refno = mathis.asset
                        out_list.bezeich = mathis.name
                        out_list.received = mathis.datum
                        out_list.qty = fa_artikel.anzahl
                        out_list.init_val = fa_artikel.warenwert
                        out_list.depn_val = fa_artikel.depn_wert
                        out_list.book_val = fa_artikel.book_wert

                        if fa_artikel.first_depn != None:
                            out_list.first_depn = fa_artikel.first_depn

                        if fa_artikel.next_depn != None:
                            out_list.next_depn = fa_artikel.next_depn

                        if fa_artikel.last_depn != None:
                            out_list.last_depn = fa_artikel.last_depn

                        if fa_artikel.anz_depn != None:
                            out_list.depn_no = anz_depn

                    if t_anz != 0:
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.refno = "SUB TOTAL"
                        out_list.flag = 1
                        out_list.qty = t_anz
                        out_list.init_val = t_val
                        out_list.depn_val = t_val1
                        out_list.book_val = t_val2

                    if i > 0:
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.refno = "T O T A L"
                        out_list.flag = 1
                        out_list.qty = tt_anz
                        out_list.init_val = tt_val
                        out_list.depn_val = tt_val1
                        out_list.book_val = tt_val2

        if from_lager != to_lager and tot_anz != 0:
            out_list = Out_list()
            out_list_list.append(out_list)

            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.flag = 2
            out_list.refno = "GRAND TOTAL"
            out_list.qty = tot_anz
            out_list.init_val = tot_val
            out_list.depn_val = tot_val1
            out_list.book_val = tot_val2

    def create_list11():

        nonlocal out_list_list, do_it, sub_depn, val_dep, datum, flag, p_depn_wert, p_book_wert, fa_lager, mathis, fa_artikel, fa_grup, gl_acct, fa_kateg, htparam
        nonlocal l_oh


        nonlocal lagerbuff, out_list, l_oh
        nonlocal lagerbuff_list, out_list_list

        i:int = 0
        j:int = 0
        t_anz:decimal = 0
        t_val:decimal = 0
        t_val1:decimal = 0
        t_val2:decimal = 0
        tt_anz:decimal = 0
        tt_val:decimal = 0
        tt_val1:decimal = 0
        tt_val2:decimal = 0
        tot_anz:decimal = 0
        tot_val:decimal = 0
        tot_val1:decimal = 0
        tot_val2:decimal = 0
        zwkum:int = 0
        bezeich:str = ""
        qty:decimal = 0
        wert:decimal = 0
        L_oh = Mathis
        tot_anz = 0
        tot_val = 0
        tot_val1 = 0
        tot_val2 = 0

        fa_grup = db_session.query(Fa_grup).filter(
                (Fa_grup.gnr == from_grp) &  (Fa_grup.flag == 0)).first()

        for lagerbuff in query(lagerbuff_list, filters=(lambda lagerbuff :lagerBuff.lager_nr >= from_lager and lagerBuff.lager_nr <= to_lager)):
            i = 0
            zwkum = 0
            t_anz = 0
            t_val = 0
            t_val1 = 0
            t_val2 = 0
            tt_anz = 0
            tt_val = 0
            tt_val1 = 0
            tt_val2 = 0


            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.bezeich = to_string(lagerBuff.lager_nr, ">>99") + "-" + lagerBuff.bezeich

            if mi_bookvalue_chk :

                mathis_obj_list = []
                for mathis, fa_artikel in db_session.query(Mathis, Fa_artikel).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) &  (Fa_artikel.loeschflag == 0) &  (Fa_artikel.gnr == from_grp)).filter(
                        (Mathis.location == lagerBuff.bezeich) &  (Mathis.datum >= from_date) &  (Mathis.datum <= to_date)).all():
                    if mathis._recid in mathis_obj_list:
                        continue
                    else:
                        mathis_obj_list.append(mathis._recid)


                    do_it = False

                    if not zero_value_only:
                        do_it = True
                    else:
                        do_it = fa_artikel.book_wert == 0

                    if do_it:

                        if zwkum != fa_artikel.gnr:

                            if zwkum != 0:
                                out_list = Out_list()
                                out_list_list.append(out_list)

                                out_list.refno = "SUB TOTAL"
                                out_list.flag = 1
                                out_list.qty = t_anz
                                out_list.init_val = t_val
                                out_list.depn_val = t_val1
                                out_list.book_val = t_val2


                            out_list = Out_list()
                            out_list_list.append(out_list)

                            out_list.bezeich = fa_grup.bezeich
                            t_anz = 0
                            t_val = 0
                            t_val1 = 0
                            t_val2 = 0
                            zwkum = fa_artikel.gnr


                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.flag = 1
                        out_list.refno = mathis.asset
                        out_list.bezeich = mathis.name
                        out_list.received = mathis.datum
                        out_list.qty = fa_artikel.anzahl
                        val_dep = fa_artikel.depn_wert / fa_artikel.anz_depn
                        sub_depn = 0
                        flag = False

                        if val_dep == None:
                            val_dep = 0
                        for datum in range(from_date,to_date + 1) :

                            if flag and datum == date_mdy(get_month(datum) + 1, 1, get_year(datum)) - 1:
                                sub_depn = sub_depn + 1

                            if datum == fa_artikel.first_depn:
                                sub_depn = sub_depn + 1
                                flag = True

                            if datum == fa_artikel.last_depn:
                                break
                        p_depn_wert = val_dep * sub_depn
                        p_book_wert = fa_artikel.warenwert - p_depn_wert
                        i = i + 1
                        t_anz = t_anz + fa_artikel.anzahl
                        t_val = t_val + fa_artikel.warenwert
                        t_val1 = t_val1 + p_depn_wert
                        t_val2 = t_val2 + p_book_wert
                        tt_anz = tt_anz + fa_artikel.anzahl
                        tt_val = tt_val + fa_artikel.warenwert
                        tt_val1 = tt_val1 + p_depn_wert
                        tt_val2 = tt_val2 + p_book_wert
                        tot_anz = tot_anz + fa_artikel.anzahl
                        tot_val = tot_val + fa_artikel.warenwert
                        tot_val1 = tot_val1 + p_depn_wert
                        tot_val2 = tot_val2 + p_book_wert
                        out_list.init_val = fa_artikel.warenwert
                        out_list.depn_val = p_depn_wert
                        out_list.book_val = p_book_wert

                        if fa_artikel.first_depn != None:
                            out_list.first_depn = fa_artikel.first_depn

                        if fa_artikel.next_depn != None:
                            out_list.next_depn = fa_artikel.next_depn

                        if fa_artikel.last_depn != None:
                            out_list.last_depn = fa_artikel.last_depn

                        if fa_artikel.anz_depn != None:
                            out_list.depn_no = sub_depn

                    if t_anz != 0:
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.refno = "SUB TOTAL"
                        out_list.flag = 1
                        out_list.qty = t_anz
                        out_list.init_val = t_val
                        out_list.depn_val = t_val1
                        out_list.book_val = t_val2

                    if i > 0:
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.refno = "T O T A L"
                        out_list.flag = 1
                        out_list.qty = tt_anz
                        out_list.init_val = tt_val
                        out_list.depn_val = tt_val1
                        out_list.book_val = tt_val2


            else:

                mathis_obj_list = []
                for mathis, fa_artikel in db_session.query(Mathis, Fa_artikel).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) &  (Fa_artikel.loeschflag == 0) &  (Fa_artikel.gnr == from_grp)).filter(
                        (Mathis.location == lagerBuff.bezeich) &  (Mathis.datum >= from_date) &  (Mathis.datum <= to_date)).all():
                    if mathis._recid in mathis_obj_list:
                        continue
                    else:
                        mathis_obj_list.append(mathis._recid)


                    do_it = False

                    if not zero_value_only:
                        do_it = True
                    else:
                        do_it = fa_artikel.book_wert == 0

                    if do_it:

                        if zwkum != fa_artikel.gnr:

                            if zwkum != 0:
                                out_list = Out_list()
                                out_list_list.append(out_list)

                                out_list.refno = "SUB TOTAL"
                                out_list.flag = 1
                                out_list.qty = t_anz
                                out_list.init_val = t_val
                                out_list.depn_val = t_val1
                                out_list.book_val = t_val2


                            out_list = Out_list()
                            out_list_list.append(out_list)

                            out_list.bezeich = fa_grup.bezeich
                            t_anz = 0
                            t_val = 0
                            t_val1 = 0
                            t_val2 = 0
                            zwkum = fa_artikel.gnr


                        i = i + 1
                        t_anz = t_anz + fa_artikel.anzahl
                        t_val = t_val + fa_artikel.warenwert
                        t_val1 = t_val1 + fa_artikel.depn_wert
                        t_val2 = t_val2 + fa_artikel.book_wert
                        tt_anz = tt_anz + fa_artikel.anzahl
                        tt_val = tt_val + fa_artikel.warenwert
                        tt_val1 = tt_val1 + fa_artikel.depn_wert
                        tt_val2 = tt_val2 + fa_artikel.book_wert
                        tot_anz = tot_anz + fa_artikel.anzahl
                        tot_val = tot_val + fa_artikel.warenwert
                        tot_val1 = tot_val1 + fa_artikel.depn_wert
                        tot_val2 = tot_val2 + fa_artikel.book_wert


                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.flag = 1
                        out_list.refno = mathis.asset
                        out_list.bezeich = mathis.name
                        out_list.received = mathis.datum
                        out_list.qty = fa_artikel.anzahl
                        out_list.init_val = fa_artikel.warenwert
                        out_list.depn_val = fa_artikel.depn_wert
                        out_list.book_val = fa_artikel.book_wert

                        if fa_artikel.first_depn != None:
                            out_list.first_depn = fa_artikel.first_depn

                        if fa_artikel.next_depn != None:
                            out_list.next_depn = fa_artikel.next_depn

                        if fa_artikel.last_depn != None:
                            out_list.last_depn = fa_artikel.last_depn

                        if fa_artikel.anz_depn != None:
                            out_list.depn_no = fa_artikel.anz_depn

                    if t_anz != 0:
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.refno = "SUB TOTAL"
                        out_list.flag = 1
                        out_list.qty = t_anz
                        out_list.init_val = t_val
                        out_list.depn_val = t_val1
                        out_list.book_val = t_val2

                    if i > 0:
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.refno = "T O T A L"
                        out_list.flag = 1
                        out_list.qty = tt_anz
                        out_list.init_val = tt_val
                        out_list.depn_val = tt_val1
                        out_list.book_val = tt_val2

        if from_lager != to_lager and tot_anz != 0:
            out_list = Out_list()
            out_list_list.append(out_list)

            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.flag = 2
            out_list.refno = "GRAND TOTAL"
            out_list.qty = tot_anz
            out_list.init_val = tot_val
            out_list.depn_val = tot_val1
            out_list.book_val = tot_val2

    def create_listsgrp():

        nonlocal out_list_list, do_it, sub_depn, val_dep, datum, flag, p_depn_wert, p_book_wert, fa_lager, mathis, fa_artikel, fa_grup, gl_acct, fa_kateg, htparam
        nonlocal l_oh


        nonlocal lagerbuff, out_list, l_oh
        nonlocal lagerbuff_list, out_list_list

        i:int = 0
        j:int = 0
        t_anz:decimal = 0
        t_val:decimal = 0
        t_val1:decimal = 0
        t_val2:decimal = 0
        tot_anz:decimal = 0
        tot_val:decimal = 0
        tot_val1:decimal = 0
        tot_val2:decimal = 0
        zwkum:int = 0
        bezeich:str = ""
        qty:decimal = 0
        wert:decimal = 0
        diff_n:int = 0
        diff_wert:decimal = 0
        L_oh = Mathis
        diff_n = (get_year(last_acctdate) - yy) * 12 + get_month(last_acctdate) - mm
        tot_anz = 0
        tot_val = 0
        tot_val1 = 0
        tot_val2 = 0


        i = 0
        zwkum = 0
        t_anz = 0
        t_val = 0
        t_val1 = 0
        t_val2 = 0

        if mi_bookvalue_chk :

            mathis_obj_list = []
            for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) &  (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == fa_artikel.subgrp) &  (Fa_grup.flag == 1) &  (Fa_grup.gnr >= from_subgr) &  (Fa_grup.gnr <= to_subgr)).filter(
                        (Mathis.datum >= from_date) &  (Mathis.datum <= to_date)).all():
                if mathis._recid in mathis_obj_list:
                    continue
                else:
                    mathis_obj_list.append(mathis._recid)

                if zwkum != fa_artikel.subgrp:

                    if zwkum != 0:
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.refno = "SUB TOTAL"
                        out_list.flag = 1
                        out_list.qty = t_anz
                        out_list.init_val = t_val
                        out_list.depn_val = t_val1
                        out_list.book_val = t_val2


                    out_list = Out_list()
                    out_list_list.append(out_list)

                    out_list.bezeich = fa_grup.bezeich
                    t_anz = 0
                    t_val = 0
                    t_val1 = 0
                    t_val2 = 0
                    zwkum = fa_artikel.subgrp


                out_list = Out_list()
                out_list_list.append(out_list)

                out_list.flag = 1
                out_list.refno = mathis.asset
                out_list.location = trim (mathis.location)
                out_list.bezeich = mathis.name
                out_list.received = mathis.datum
                out_list.qty = fa_artikel.anzahl
                out_list.init_val = fa_artikel.warenwert
                val_dep = fa_artikel.depn_wert / fa_artikel.anz_depn
                sub_depn = 0
                flag = False

                if val_dep == None:
                    val_dep = 0
                for datum in range(from_date,to_date + 1) :

                    if flag and datum == date_mdy(get_month(datum) + 1, 1, get_year(datum)) - 1:
                        sub_depn = sub_depn + 1

                    if datum == fa_artikel.first_depn:
                        sub_depn = sub_depn + 1
                        flag = True

                    if datum == fa_artikel.last_depn:
                        break
                p_depn_wert = val_dep * sub_depn
                p_book_wert = fa_artikel.warenwert - p_depn_wert
                i = i + 1
                t_anz = t_anz + fa_artikel.anzahl
                t_val = t_val + fa_artikel.warenwert
                tot_anz = tot_anz + fa_artikel.anzahl
                tot_val = tot_val + fa_artikel.warenwert

                if (fa_artikel.anz_depn - diff_n) == 0:
                    t_val2 = t_val2 + fa_artikel.warenwert
                    tot_val2 = tot_val2 + fa_artikel.warenwert
                else:
                    diff_wert = (p_depn_wert / sub_depn) * diff_n

                    if diff_wert == None:
                        diff_wert = 0
                    t_val1 = t_val1 + p_depn_wert - diff_wert
                    t_val2 = t_val2 + p_book_wert + diff_wert
                    tot_val1 = tot_val1 + p_depn_wert - diff_wert
                    tot_val2 = tot_val2 + p_book_wert + diff_wert

                if (fa_artikel.anz_depn - diff_n) == 0:
                    out_list.depn_val = 0
                    out_list.book_val = fa_artikel.warenwert


                else:
                    out_list.depn_val = p_depn_wert - diff_wert
                    out_list.book_val = p_book_wert + diff_wert

                if fa_artikel.first_depn != None:
                    out_list.first_depn = fa_artikel.first_depn

                if fa_artikel.next_depn != None:
                    out_list.next_depn = fa_artikel.next_depn

                if fa_artikel.last_depn != None:
                    out_list.last_depn = fa_artikel.last_depn

                if fa_artikel.anz_depn != None:
                    out_list.depn_no = sub_depn

            if t_anz != 0:
                out_list = Out_list()
                out_list_list.append(out_list)

                out_list.refno = "SUB TOTAL"
                out_list.flag = 1
                out_list.qty = t_anz
                out_list.init_val = t_val
                out_list.depn_val = t_val1
                out_list.book_val = t_val2


        else:

            mathis_obj_list = []
            for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) &  (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == fa_artikel.subgrp) &  (Fa_grup.flag == 1) &  (Fa_grup.gnr >= from_subgr) &  (Fa_grup.gnr <= to_subgr)).filter(
                        (Mathis.datum >= from_date) &  (Mathis.datum <= to_date)).all():
                if mathis._recid in mathis_obj_list:
                    continue
                else:
                    mathis_obj_list.append(mathis._recid)

                if zwkum != fa_artikel.subgrp:

                    if zwkum != 0:
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.refno = "SUB TOTAL"
                        out_list.flag = 1
                        out_list.qty = t_anz
                        out_list.init_val = t_val
                        out_list.depn_val = t_val1
                        out_list.book_val = t_val2


                    out_list = Out_list()
                    out_list_list.append(out_list)

                    out_list.bezeich = fa_grup.bezeich
                    t_anz = 0
                    t_val = 0
                    t_val1 = 0
                    t_val2 = 0
                    zwkum = fa_artikel.subgrp


                i = i + 1
                t_anz = t_anz + fa_artikel.anzahl
                t_val = t_val + fa_artikel.warenwert
                tot_anz = tot_anz + fa_artikel.anzahl
                tot_val = tot_val + fa_artikel.warenwert

                if (fa_artikel.anz_depn - diff_n) == 0:
                    t_val2 = t_val2 + fa_artikel.warenwert
                    tot_val2 = tot_val2 + fa_artikel.warenwert
                else:
                    diff_wert = (fa_artikel.depn_wert / fa_artikel.anz_depn) * diff_n

                    if diff_wert == None:
                        diff_wert = 0
                    t_val1 = t_val1 + fa_artikel.depn_wert - diff_wert
                    t_val2 = t_val2 + fa_artikel.book_wert + diff_wert
                    tot_val1 = tot_val1 + fa_artikel.depn_wert - diff_wert
                    tot_val2 = tot_val2 + fa_artikel.book_wert + diff_wert
                out_list = Out_list()
                out_list_list.append(out_list)

                out_list.flag = 1
                out_list.refno = mathis.asset
                out_list.location = trim (mathis.location)
                out_list.bezeich = mathis.name
                out_list.received = mathis.datum
                out_list.qty = fa_artikel.anzahl
                out_list.init_val = fa_artikel.warenwert

                if (fa_artikel.anz_depn - diff_n) == 0:
                    out_list.depn_val = 0
                    out_list.book_val = fa_artikel.warenwert


                else:
                    out_list.depn_val = fa_artikel.depn_wert - diff_wert
                    out_list.book_val = fa_artikel.book_wert + diff_wert

                if fa_artikel.first_depn != None:
                    out_list.first_depn = fa_artikel.first_depn

                if fa_artikel.next_depn != None:
                    out_list.next_depn = fa_artikel.next_depn

                if fa_artikel.last_depn != None:
                    out_list.last_depn = fa_artikel.last_depn

                if fa_artikel.anz_depn != None:
                    out_list.depn_no = fa_artikel.anz_depn

            if t_anz != 0:
                out_list = Out_list()
                out_list_list.append(out_list)

                out_list.refno = "SUB TOTAL"
                out_list.flag = 1
                out_list.qty = t_anz
                out_list.init_val = t_val
                out_list.depn_val = t_val1
                out_list.book_val = t_val2

        if tot_anz != 0:
            out_list = Out_list()
            out_list_list.append(out_list)

            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.flag = 2
            out_list.refno = "GRAND TOTAL"
            out_list.qty = tot_anz
            out_list.init_val = tot_val
            out_list.depn_val = tot_val1
            out_list.book_val = tot_val2

    def create_listacct():

        nonlocal out_list_list, do_it, sub_depn, val_dep, datum, flag, p_depn_wert, p_book_wert, fa_lager, mathis, fa_artikel, fa_grup, gl_acct, fa_kateg, htparam
        nonlocal l_oh


        nonlocal lagerbuff, out_list, l_oh
        nonlocal lagerbuff_list, out_list_list

        curr_acct:str = ""
        fibu:str = ""
        diff_n:int = 0
        diff_wert:decimal = 0
        t_oh:decimal = 0
        t_depn:decimal = 0
        tot_oh:decimal = 0
        tot_depn:decimal = 0
        t_book:decimal = 0
        tot_book:decimal = 0
        t_anz:decimal = 0
        tot_anz:decimal = 0
        diff_n = (get_year(last_acctdate) - yy) * 12 + get_month(last_acctdate) - mm

        if mi_bookvalue_chk :

            mathis_obj_list = []
            for mathis, fa_artikel in db_session.query(Mathis, Fa_artikel).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) &  (Fa_artikel.loeschflag == 0)).filter(
                    (Mathis.datum >= from_date) &  (Mathis.datum <= to_date)).all():
                if mathis._recid in mathis_obj_list:
                    continue
                else:
                    mathis_obj_list.append(mathis._recid)

                if curr_acct != fa_artikel.fibukonto and curr_acct != "":
                    tot_anz = tot_anz + t_anz
                    tot_oh = tot_oh + t_oh
                    tot_depn = tot_depn + t_depn
                    tot_book = tot_book + t_book

                    gl_acct = db_session.query(Gl_acct).filter(
                            (func.lower(Gl_acct.fibukonto) == (curr_acct).lower())).first()

                    if gl_acct:
                        fibu = convert_fibu(curr_acct)

                    if curr_acct != "":
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.location = ""
                        out_list.bezeich = "SUBTOTAL"
                        out_list.qty = t_anz
                        out_list.init_val = t_oh
                        out_list.depn_val = t_depn
                        out_list.book_val = t_book


                        out_list = Out_list()
                        out_list_list.append(out_list)

                    curr_acct = fa_artikel.fibukonto
                    t_anz = 0
                    t_oh = 0
                    t_depn = 0
                    t_book = 0

                gl_acct = db_session.query(Gl_acct).filter(
                        (Gl_acct.fibukonto == fa_artikel.fibukonto)).first()
                fibu = convert_fibu(fa_artikel.fibukonto)

                out_list = query(out_list_list, filters=(lambda out_list :out_list.(fibu).lower().lower()  == (fibu).lower()), first=True)

                if out_list:
                    out_list = Out_list()
                    out_list_list.append(out_list)

                    out_list.flag = 1
                    out_list.refno = mathis.asset
                    out_list.location = mathis.location
                    out_list.bezeich = mathis.name
                    out_list.received = mathis.datum
                    out_list.qty = fa_artikel.anzahl


                else:
                    out_list = Out_list()
                    out_list_list.append(out_list)

                    out_list.flag = 1
                    out_list.refno = mathis.asset
                    out_list.location = trim (mathis.location)
                    out_list.fibu = fibu
                    out_list.bezeich = mathis.name
                    out_list.received = mathis.datum
                    out_list.qty = fa_artikel.anzahl


                val_dep = fa_artikel.depn_wert / fa_artikel.anz_depn
                sub_depn = 0
                flag = False

                if val_dep == None:
                    val_dep = 0
                for datum in range(from_date,to_date + 1) :

                    if flag and datum == date_mdy(get_month(datum) + 1, 1, get_year(datum)) - 1:
                        sub_depn = sub_depn + 1

                    if datum == fa_artikel.first_depn:
                        sub_depn = sub_depn + 1
                        flag = True

                    if datum == fa_artikel.last_depn:
                        break
                p_depn_wert = val_dep * sub_depn
                p_book_wert = fa_artikel.warenwert - p_depn_wert

                if (fa_artikel.anz_depn - diff_n) == 0:
                    out_list.init_val = fa_artikel.warenwert
                    out_list.depn_val = 0
                    out_list.book_val = fa_artikel.warenwert


                else:
                    out_list.init_val = fa_artikel.warenwert
                    out_list.depn_val = p_depn_wert - diff_wert
                    out_list.book_val = p_book_wert + diff_wert

                if fa_artikel.first_depn != None:
                    out_list.first_depn = fa_artikel.first_depn

                if fa_artikel.next_depn != None:
                    out_list.next_depn = fa_artikel.next_depn

                if fa_artikel.last_depn != None:
                    out_list.last_depn = fa_artikel.last_depn

                if fa_artikel.anz_depn != None:
                    out_list.depn_no = sub_depn

                if (fa_artikel.anz_depn - diff_n) == 0:
                    t_anz = t_anz + fa_artikel.anzahl
                    t_oh = t_oh + fa_artikel.warenwert
                    t_book = t_book + fa_artikel.book_wert

                elif fa_artikel.anz_depn - diff_n > 0:

                    fa_kateg = db_session.query(Fa_kateg).filter(
                            (Fa_kateg.katnr == fa_artikel.katnr)).first()

                    if (fa_kateg.methode == 0):
                        diff_wert = (p_book_wert / sub_depn) * diff_n

                        if diff_wert == None:
                            diff_wert = 0
                        t_anz = t_anz + fa_artikel.anzahl
                        t_oh = t_oh + fa_artikel.warenwert
                        t_depn = t_depn + p_depn_wert - diff_wert
                        t_book = t_book + p_book_wert + diff_wert
        else:

            mathis_obj_list = []
            for mathis, fa_artikel in db_session.query(Mathis, Fa_artikel).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) &  (Fa_artikel.loeschflag == 0)).filter(
                    (Mathis.datum >= from_date) &  (Mathis.datum <= to_date)).all():
                if mathis._recid in mathis_obj_list:
                    continue
                else:
                    mathis_obj_list.append(mathis._recid)

                if curr_acct != fa_artikel.fibukonto:
                    tot_anz = tot_anz + t_anz
                    tot_oh = tot_oh + t_oh
                    tot_depn = tot_depn + t_depn
                    tot_book = tot_book + t_book

                    gl_acct = db_session.query(Gl_acct).filter(
                            (func.lower(Gl_acct.fibukonto) == (curr_acct).lower())).first()

                    if gl_acct:
                        fibu = convert_fibu(curr_acct)

                    if curr_acct != "":
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.location = ""
                        out_list.bezeich = "SUBTOTAL"
                        out_list.qty = t_anz
                        out_list.init_val = t_oh
                        out_list.depn_val = t_depn
                        out_list.book_val = t_book


                        out_list = Out_list()
                        out_list_list.append(out_list)

                    curr_acct = fa_artikel.fibukonto
                    t_anz = 0
                    t_oh = 0
                    t_depn = 0
                    t_book = 0

                gl_acct = db_session.query(Gl_acct).filter(
                        (Gl_acct.fibukonto == fa_artikel.fibukonto)).first()
                fibu = convert_fibu(fa_artikel.fibukonto)

                out_list = query(out_list_list, filters=(lambda out_list :out_list.(fibu).lower().lower()  == (fibu).lower()), first=True)

                if out_list:
                    out_list = Out_list()
                    out_list_list.append(out_list)

                    out_list.refno = mathis.asset
                    out_list.location = trim (mathis.location)
                    out_list.bezeich = mathis.name
                    out_list.received = mathis.datum
                    out_list.qty = fa_artikel.anzahl


                else:
                    out_list = Out_list()
                    out_list_list.append(out_list)

                    out_list.refno = mathis.asset
                    out_list.location = trim (mathis.location)
                    out_list.bezeich = mathis.name
                    out_list.received = mathis.datum
                    out_list.qty = fa_artikel.anzahl
                    out_list.fibu = fibu

                if (fa_artikel.anz_depn - diff_n) == 0:
                    out_list.init_val = fa_artikel.warenwert
                    out_list.depn_val = 0
                    out_list.book_val = fa_artikel.warenwert


                else:
                    out_list.init_val = fa_artikel.warenwert
                    out_list.depn_val = fa_artikel.depn_wert - diff_wert
                    out_list.book_val = fa_artikel.book_wert + diff_wert

                if fa_artikel.first_depn != None:
                    out_list.first_depn = fa_artikel.first_depn

                if fa_artikel.next_depn != None:
                    out_list.next_depn = fa_artikel.next_depn

                if fa_artikel.last_depn != None:
                    out_list.last_depn = fa_artikel.last_depn

                if fa_artikel.anz_depn != None:
                    out_list.depn_no = fa_artikel.anz_depn

                if (fa_artikel.anz_depn - diff_n) == 0:
                    t_anz = t_anz + fa_artikel.anzahl
                    t_oh = t_oh + fa_artikel.warenwert
                    t_book = t_book + fa_artikel.book_wert

                elif fa_artikel.anz_depn - diff_n > 0:

                    fa_kateg = db_session.query(Fa_kateg).filter(
                            (Fa_kateg.katnr == fa_artikel.katnr)).first()

                    if (fa_kateg.methode == 0):
                        diff_wert = (fa_artikel.depn_wert / fa_artikel.anz_depn) * diff_n

                        if diff_wert == None:
                            diff_wert = 0
                        t_anz = t_anz + fa_artikel.anzahl
                        t_oh = t_oh + fa_artikel.warenwert
                        t_depn = t_depn + fa_artikel.depn_wert - diff_wert
                        t_book = t_book + fa_artikel.book_wert + diff_wert
        tot_anz = tot_anz + t_anz
        tot_oh = tot_oh + t_oh
        tot_depn = tot_depn + t_depn
        tot_book = tot_book + t_book

        gl_acct = db_session.query(Gl_acct).filter(
                (func.lower(Gl_acct.fibukonto) == (curr_acct).lower())).first()
        fibu = convert_fibu(curr_acct)
        out_list = Out_list()
        out_list_list.append(out_list)

        out_list.bezeich = "SUBTOTAL"
        out_list.flag = 1
        out_list.qty = t_anz
        out_list.init_val = t_oh
        out_list.depn_val = t_depn
        out_list.book_val = t_book


        out_list = Out_list()
        out_list_list.append(out_list)

        out_list.bezeich = "T O T A L"
        out_list.qty = tot_anz
        out_list.init_val = tot_oh
        out_list.depn_val = tot_depn
        out_list.book_val = tot_book

    def convert_fibu(konto:str):

        nonlocal out_list_list, do_it, sub_depn, val_dep, datum, flag, p_depn_wert, p_book_wert, fa_lager, mathis, fa_artikel, fa_grup, gl_acct, fa_kateg, htparam
        nonlocal l_oh


        nonlocal lagerbuff, out_list, l_oh
        nonlocal lagerbuff_list, out_list_list

        s = ""
        ch:str = ""
        i:int = 0
        j:int = 0

        def generate_inner_output():
            return s

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 977)).first()
        ch = htparam.fchar
        j = 0
        for i in range(1,len(ch)  + 1) :

            if substring(ch, i - 1, 1) >= "0" and substring(ch, i - 1, 1) <= "9":
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