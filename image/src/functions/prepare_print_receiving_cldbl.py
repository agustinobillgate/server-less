from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Bediener, L_orderhdr, L_lieferant, L_op, L_artikel, L_lager, L_ophis, Gl_acct

def prepare_print_receiving_cldbl(pvilanguage:int, docu_nr:str, user_init:str, po_nr:str, lief_nr:int, store:int, to_date:date):
    show_price = False
    crterm = 0
    d_purchase = False
    unit_price = 0
    l_lieferant_firma = ""
    avail_l_lager = False
    t_lager_nr = 0
    t_bezeich = ""
    str_list_list = []
    tot_anz:decimal = 0
    tot_amount:decimal = 0
    lvcarea:str = "print_receiving1"
    htparam = bediener = l_orderhdr = l_lieferant = l_op = l_artikel = l_lager = l_ophis = gl_acct = None

    str_list = b_lop = None

    str_list_list, Str_list = create_model("Str_list", {"artnr":int, "qty":decimal, "warenwert":decimal, "munit":str, "s":str, "fibu":str})

    B_lop = L_op

    db_session = local_storage.db_session

    def generate_output():
        nonlocal show_price, crterm, d_purchase, unit_price, l_lieferant_firma, avail_l_lager, t_lager_nr, t_bezeich, str_list_list, tot_anz, tot_amount, lvcarea, htparam, bediener, l_orderhdr, l_lieferant, l_op, l_artikel, l_lager, l_ophis, gl_acct
        nonlocal b_lop


        nonlocal str_list, b_lop
        nonlocal str_list_list
        return {"show_price": show_price, "crterm": crterm, "d_purchase": d_purchase, "unit_price": unit_price, "l_lieferant_firma": l_lieferant_firma, "avail_l_lager": avail_l_lager, "t_lager_nr": t_lager_nr, "t_bezeich": t_bezeich, "str-list": str_list_list}

    def create_list():

        nonlocal show_price, crterm, d_purchase, unit_price, l_lieferant_firma, avail_l_lager, t_lager_nr, t_bezeich, str_list_list, tot_anz, tot_amount, lvcarea, htparam, bediener, l_orderhdr, l_lieferant, l_op, l_artikel, l_lager, l_ophis, gl_acct
        nonlocal b_lop


        nonlocal str_list, b_lop
        nonlocal str_list_list

        i:int = 0
        create_it:bool = False
        B_lop = L_op
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0
        i = 0
        d_purchase = False

        b_lop = db_session.query(B_lop).filter(
                (B_lop.datum == to_date) &  (B_lop.lief_nr == lief_nr) &  (B_lop.op_art == 1) &  (B_lop.loeschflag <= 1) &  (B_lop.anzahl != 0) &  (func.lower(B_lop.lscheinnr) == (docu_nr).lower())).first()

        if b_lop:

            l_op_obj_list = []
            for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                    (L_op.datum == to_date) &  (L_op.lief_nr == lief_nr) &  (L_op.op_art == 1) &  (L_op.loeschflag <= 1) &  (L_op.anzahl != 0) &  (func.lower(L_op.lscheinnr) == (docu_nr).lower())).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                i = i + 1

                if l_op.docu_nr == l_op.lscheinnr:
                    d_purchase = True

                if i == 1:

                    l_lager = db_session.query(L_lager).filter(
                            (L_lager.lager_nr == l_op.lager_nr)).first()
                tot_anz = tot_anz + l_op.anzahl

                if show_price:
                    tot_amount = tot_amount + l_op.warenwert

                if show_price:
                    unit_price = l_op.einzelpreis

                if l_op.stornogrund != "":
                    create_it = True
                else:

                    str_list = query(str_list_list, filters=(lambda str_list :str_list.artnr == l_op.artnr), first=True)
                    create_it = not None != str_list

                if not create_it:
                    str_list.qty = str_list.qty + l_op.anzahl

                    if show_price:
                        str_list.warenwert = str_list.warenwert + l_op.warenwert
                    substring(str_list.s, 31, 15) = to_string(str_list.qty, "->>>,>>>,>>9.99")
                    substring(str_list.s, 46, 15) = to_string(str_list.warenwert, "->>>,>>>,>>9.99")
                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.qty = l_op.anzahl
                    str_list.munit = l_artikel.masseinheit

                    if show_price:
                        str_list.warenwert = l_op.warenwert
                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(24)") + to_string(unit_price, "->>>,>>>,>>9.99") + to_string(l_op.anzahl, "->>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_op.lscheinnr, "x(20)")
                    str_list.fibu = convert_fibu(l_op.stornogrund)
        else:

            l_ophis_obj_list = []
            for l_ophis, l_artikel in db_session.query(L_ophis, L_artikel).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).filter(
                    (L_ophis.datum == to_date) &  (L_ophis.lief_nr == lief_nr) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (func.lower(L_ophis.lscheinnr) == (docu_nr).lower()) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)


                i = i + 1

                if l_ophis.docu_nr == l_ophis.lscheinnr:
                    d_purchase = True

                if i == 1:

                    l_lager = db_session.query(L_lager).filter(
                            (L_lager.lager_nr == l_ophis.lager_nr)).first()
                tot_anz = tot_anz + l_ophis.anzahl

                if show_price:
                    tot_amount = tot_amount + l_ophis.warenwert

                if show_price:
                    unit_price = l_ophis.einzelpreis

                str_list = query(str_list_list, filters=(lambda str_list :str_list.artnr == l_ophis.artnr), first=True)
                create_it = not None != str_list

                if not create_it:
                    str_list.qty = str_list.qty + l_ophis.anzahl

                    if show_price:
                        str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    substring(str_list.s, 31, 15) = to_string(str_list.qty, "->>>,>>>,>>9.99")
                    substring(str_list.s, 46, 15) = to_string(str_list.warenwert, "->>>,>>>,>>9.99")
                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.qty = l_ophis.anzahl
                    str_list.munit = l_artikel.masseinheit

                    if show_price:
                        str_list.warenwert = l_ophis.warenwert
                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(24)") + to_string(unit_price, "->>>,>>>,>>9.99") + to_string(l_ophis.anzahl, "->>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(20)")
                    str_list.fibu = convert_fibu(l_ophis.fibukonto)
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,7 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + translateExtended ("T O T A L", lvcarea, "")
        for i in range(1,27 + 1) :
            str_list.s = str_list.s + " "
        str_list.qty = tot_anz
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>>,>>>,>>9.99")

        if l_lager:
            avail_l_lager = True
            t_lager_nr = l_lager.lager_nr
            t_bezeich = l_lager.bezeich

    def create_list1():

        nonlocal show_price, crterm, d_purchase, unit_price, l_lieferant_firma, avail_l_lager, t_lager_nr, t_bezeich, str_list_list, tot_anz, tot_amount, lvcarea, htparam, bediener, l_orderhdr, l_lieferant, l_op, l_artikel, l_lager, l_ophis, gl_acct
        nonlocal b_lop


        nonlocal str_list, b_lop
        nonlocal str_list_list

        i:int = 0
        create_it:bool = False
        B_lop = L_op
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0
        i = 0
        d_purchase = False

        b_lop = db_session.query(B_lop).filter(
                (B_lop.datum == to_date) &  (B_lop.lief_nr == lief_nr) &  (B_lop.op_art == 1) &  (B_lop.loeschflag <= 1) &  (B_lop.anzahl != 0) &  (B_lop.lager_nr == store) &  (func.lower(B_lop.lscheinnr) == (docu_nr).lower())).first()

        if b_lop:

            l_op_obj_list = []
            for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                    (L_op.datum == to_date) &  (L_op.lief_nr == lief_nr) &  (L_op.op_art == 1) &  (L_op.loeschflag <= 1) &  (L_op.anzahl != 0) &  (L_op.lager_nr == store) &  (func.lower(L_op.lscheinnr) == (docu_nr).lower())).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                i = i + 1

                if l_op.docu_nr == l_op.lscheinnr:
                    d_purchase = True

                if i == 1:

                    l_lager = db_session.query(L_lager).filter(
                            (L_lager.lager_nr == l_op.lager_nr)).first()
                tot_anz = tot_anz + l_op.anzahl

                if show_price:
                    tot_amount = tot_amount + l_op.warenwert

                if show_price:
                    unit_price = l_op.einzelpreis

                if l_op.stornogrund != "":
                    create_it = True
                else:

                    str_list = query(str_list_list, filters=(lambda str_list :str_list.artnr == l_op.artnr), first=True)
                    create_it = not None != str_list

                if not create_it:
                    str_list.qty = str_list.qty + l_op.anzahl

                    if show_price:
                        str_list.warenwert = str_list.warenwert + l_op.warenwert
                    substring(str_list.s, 31, 15) = to_string(str_list.qty, "->>>,>>>,>>9.99")
                    substring(str_list.s, 46, 14) = to_string(str_list.warenwert, "->>,>>>,>>9.99")
                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.qty = l_op.anzahl
                    str_list.munit = l_artikel.masseinheit

                    if show_price:
                        str_list.warenwert = l_op.warenwert
                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(24)") + to_string(unit_price, "->>>,>>>,>>9.99") + to_string(l_op.anzahl, "->>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>9.99") + to_string(l_op.lscheinnr, "x(20)")
                    str_list.fibu = convert_fibu(l_op.stornogrund)
        else:

            l_ophis_obj_list = []
            for l_ophis, l_artikel in db_session.query(L_ophis, L_artikel).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).filter(
                    (L_ophis.datum == to_date) &  (L_ophis.lief_nr == lief_nr) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (func.lower(L_ophis.lscheinnr) == (docu_nr).lower()) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)


                i = i + 1

                if l_ophis.docu_nr == l_ophis.lscheinnr:
                    d_purchase = True

                if i == 1:

                    l_lager = db_session.query(L_lager).filter(
                            (L_lager.lager_nr == l_ophis.lager_nr)).first()
                tot_anz = tot_anz + l_ophis.anzahl

                if show_price:
                    tot_amount = tot_amount + l_ophis.warenwert

                if show_price:
                    unit_price = l_ophis.einzelpreis

                str_list = query(str_list_list, filters=(lambda str_list :str_list.artnr == l_ophis.artnr), first=True)
                create_it = not None != str_list

                if not create_it:
                    str_list.qty = str_list.qty + l_ophis.anzahl

                    if show_price:
                        str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    substring(str_list.s, 31, 15) = to_string(str_list.qty, "->>>,>>>,>>9.99")
                    substring(str_list.s, 46, 14) = to_string(str_list.warenwert, "->>,>>>,>>9.99")
                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.qty = l_ophis.anzahl
                    str_list.munit = l_artikel.masseinheit

                    if show_price:
                        str_list.warenwert = l_ophis.warenwert
                    str_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(24)") + to_string(unit_price, "->>>,>>>,>>9.99") + to_string(l_ophis.anzahl, "->>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>9.99") + to_string(l_ophis.lscheinnr, "x(20)")
                    str_list.fibu = convert_fibu(l_ophis.fibukonto)
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,7 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + translateExtended ("T O T A L", lvcarea, "")
        for i in range(1,27 + 1) :
            str_list.s = str_list.s + " "
        str_list.qty = tot_anz
        str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>9.99")

        if l_lager:
            avail_l_lager = True
            t_lager_nr = l_lager.lager_nr
            t_bezeich = l_lager.bezeich

    def convert_fibu(konto:str):

        nonlocal show_price, crterm, d_purchase, unit_price, l_lieferant_firma, avail_l_lager, t_lager_nr, t_bezeich, str_list_list, tot_anz, tot_amount, lvcarea, htparam, bediener, l_orderhdr, l_lieferant, l_op, l_artikel, l_lager, l_ophis, gl_acct
        nonlocal b_lop


        nonlocal str_list, b_lop
        nonlocal str_list_list

        s = ""
        ch:str = ""
        i:int = 0
        j:int = 0

        def generate_inner_output():
            return s

        gl_acct = db_session.query(Gl_acct).filter(
                (func.lower(Gl_acct.fibukonto) == (konto).lower())).first()

        if not gl_acct:

            return generate_inner_output()

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

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 43)).first()
    show_price = htparam.flogical

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    if substring(bediener.permissions, 21, 1) != "0":
        show_price = True

    l_orderhdr = db_session.query(L_orderhdr).filter(
            (L_orderhdr.lief_nr == lief_nr) &  (func.lower(L_orderhdr.docu_nr) == (po_nr).lower())).first()

    if l_orderhdr:
        crterm = l_orderhdr.angebot_lief[1]

    l_lieferant = db_session.query(L_lieferant).filter(
            (L_lieferant.lief_nr == lief_nr)).first()

    if l_lieferant:
        l_lieferant_firma = l_lieferant.firma

    if store == 0:
        create_list()
    else:
        create_list1()

    return generate_output()