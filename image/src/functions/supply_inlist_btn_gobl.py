from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
import re
from models import L_lieferant, L_kredit, L_artikel, L_op, L_ophdr, L_untergrup, Htparam, L_ophis, L_ophhis, Bediener, Gl_acct

def supply_inlist_btn_gobl(pvilanguage:int, last_artnr:int, lieferant_recid:int, l_kredit_recid:int, ap_recid:int, long_digit:bool, show_price:bool, store:int, all_supp:bool, sorttype:int, from_grp:int, to_grp:int, from_date:date, to_date:date, taxcode_list:[Taxcode_list]):
    first_artnr = 0
    curr_artnr = 0
    last_artnr1 = 0
    unit_price = 0
    str_list_list = []
    lvcarea:str = "supply_inlist"
    tot_anz:decimal = 0
    tot_amount:decimal = 0
    tot_tax:decimal = 0
    tot_amt:decimal = 0
    i:int = 0
    counter:int = 0
    loopi:int = 0
    l_lieferant = l_kredit = l_artikel = l_op = l_ophdr = l_untergrup = htparam = l_ophis = l_ophhis = bediener = gl_acct = None

    str_list = taxcode_list = usr = None

    str_list_list, Str_list = create_model("Str_list", {"h_recid":int, "l_recid":int, "lief_nr":int, "billdate":date, "artnr":int, "lager_nr":int, "docu_nr":str, "lscheinnr":str, "invoice_nr":str, "qty":decimal, "epreis":decimal, "warenwert":decimal, "date":date, "st":int, "supplier":str, "article":int, "description":str, "d_unit":str, "price":decimal, "inc_qty":decimal, "amount":decimal, "docu_no":str, "deliv_note":str, "id":str, "fibu":str, "gstid":str, "tax_code":str, "tax_amount":decimal, "tot_amt":decimal, "desc1":str}, {"lscheinnr": ""})
    taxcode_list_list, Taxcode_list = create_model("Taxcode_list", {"taxcode":str, "taxamount":decimal})

    Usr = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_list, lvcarea, tot_anz, tot_amount, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal usr


        nonlocal str_list, taxcode_list, usr
        nonlocal str_list_list, taxcode_list_list
        return {"first_artnr": first_artnr, "curr_artnr": curr_artnr, "last_artnr1": last_artnr1, "unit_price": unit_price, "str-list": str_list_list}

    def create_list11():

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_list, lvcarea, tot_anz, tot_amount, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal usr


        nonlocal str_list, taxcode_list, usr
        nonlocal str_list_list, taxcode_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        t_tax:decimal = 0
        t_inv:decimal = 0
        lief_nr:int = 0
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0
        tot_tax = 0
        tot_amt = 0

        if store == 0:

            l_op_obj_list = []
            for l_op, l_artikel, l_lieferant in db_session.query(L_op, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr > 0) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                t_anz, t_amt, t_tax, t_inv, lief_nr = assign_create_list11(t_anz, t_amt, t_tax, t_inv, lief_nr)

        else:

            l_op_obj_list = []
            for l_op, l_artikel, l_lieferant in db_session.query(L_op, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr > 0) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 1) &  (L_op.lager_nr == store)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                t_anz, t_amt, t_tax, t_inv, lief_nr = assign_create_list11(t_anz, t_amt, t_tax, t_inv, lief_nr)

        t_anz, t_amt, t_tax, t_inv = create_hislist(t_anz, t_amt, t_tax, t_inv)
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.DESCRIPTION = "T O T A L"
        str_list.qty = t_anz
        str_list.inc_qty = t_anz
        str_list.amount = t_amt
        str_list.tax_amount = t_tax
        str_list.tot_amt = t_inv


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.DESCRIPTION = "GRAND TOTAL"
        str_list.qty = tot_anz
        str_list.inc_qty = tot_anz
        str_list.amount = tot_amount
        str_list.tax_amount = tot_tax
        str_list.tot_amt = tot_amt

    def assign_create_list11(t_anz:decimal, t_amt:decimal, t_tax:decimal, t_inv:decimal, lief_nr:int):

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_list, lvcarea, tot_anz, tot_amount, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal usr


        nonlocal str_list, taxcode_list, usr
        nonlocal str_list_list, taxcode_list_list

        amt:decimal = 0

        l_ophdr = db_session.query(L_ophdr).filter(
                (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()

        if lief_nr == 0:
            lief_nr = l_lieferant.lief_nr

        if lief_nr != l_lieferant.lief_nr:
            lief_nr = l_lieferant.lief_nr
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.DESCRIPTION = "T O T A L"
            str_list.qty = t_anz
            str_list.inc_qty = t_anz
            str_list.amount = t_amt
            str_list.tax_amount = t_tax
            str_list.tot_amt = t_inv
            t_anz = 0
            t_amt = 0
            t_tax = 0
            t_inv = 0


            str_list = Str_list()
            str_list_list.append(str_list)

        t_anz = t_anz + l_op.anzahl

        if show_price:
            t_amt = t_amt + l_op.warenwert
        tot_anz = tot_anz + l_op.anzahl

        if show_price:
            tot_amount = tot_amount + l_op.warenwert

        if show_price:
            unit_price = l_op.einzelpreis

        str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis), first=True)

        if str_list:
            str_list.qty = str_list.qty + l_op.anzahl

            if show_price:
                str_list.warenwert = str_list.warenwert + l_op.warenwert
            str_list.inc_qty = str_list.qty
            str_list.amount = str_list.warenwert

            taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

            if taxcode_list:
                amt = l_op.warenwert * taxcode_list.taxamount
                str_list.tax_amount = str_list.tax_amount + (l_op.warenwert * taxcode_list.taxamount)
                t_tax = t_tax + (l_op.warenwert * taxcode_list.taxamount)
                tot_tax = tot_tax + (l_op.warenwert * taxcode_list.taxamount)
                str_list.tot_amt = str_list.tot_amt + (l_op.warenwert + amt)
                t_inv = t_inv + (l_op.warenwert + amt)
                tot_amt = tot_amt + (l_op.warenwert + amt)


        else:
            str_list = Str_list()
            str_list_list.append(str_list)

            add_id()

            if l_ophdr:
                str_list.invoice_nr = l_ophdr.fibukonto
                str_list.h_recid = l_ophdr._recid
            str_list.l_recid = l_op._recid
            str_list.lief_nr = l_op.lief_nr
            str_list.billdate = l_op.datum
            str_list.artnr = l_op.artnr
            str_list.lager_nr = l_op.lager_nr
            str_list.docu_nr = l_op.docu_nr
            str_list.lscheinnr = l_op.lscheinnr
            str_list.qty = l_op.anzahl
            str_list.epreis = l_op.einzelpreis

            if show_price:
                str_list.warenwert = l_op.warenwert
            str_list.fibu = convert_fibu(l_op.stornogrund)
            str_list.DATE = l_op.datum
            str_list.st = l_op.lager_nr
            str_list.article = l_artikel.artnr
            str_list.DESCRIPTION = l_artikel.bezeich
            str_list.d_unit = l_artikel.traubensort
            str_list.inc_qty = l_op.anzahl
            str_list.amount = str_list.warenwert
            str_list.supplier = l_lieferant.firma
            str_list.tax_code = l_artikel.lief_artnr[2]

            if l_lieferant.plz != " ":

                if re.match(".*#.*",l_lieferant.plz):
                    for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                        if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                            str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                            return

            taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

            if taxcode_list:
                str_list.tax_amount = l_op.warenwert * taxcode_list.taxamount
                t_tax = t_tax + (l_op.warenwert * taxcode_list.taxamount)
                tot_tax = tot_tax + (l_op.warenwert * taxcode_list.taxamount)
                str_list.tot_amt = l_op.warenwert + str_list.tax_amount
                t_inv = t_inv + (l_op.warenwert + str_list.tax_amount)
                tot_amt = tot_amt + (l_op.warenwert + str_list.tax_amount)

            if l_op.docu_nr == l_op.lscheinnr:
                str_list.docu_no = translateExtended ("Direct Purchase   ", lvcarea, "")
            else:
                str_list.docu_no = l_op.docu_nr
            str_list.deliv_note = l_op.lscheinnr
            str_list.price = unit_price

    def create_list11a():

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_list, lvcarea, tot_anz, tot_amount, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal usr


        nonlocal str_list, taxcode_list, usr
        nonlocal str_list_list, taxcode_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        t_tax:decimal = 0
        t_inv:decimal = 0
        lscheinnr:str = ""
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0
        tot_tax = 0
        tot_amt = 0

        if store == 0:

            l_op_obj_list = []
            for l_op, l_artikel, l_lieferant in db_session.query(L_op, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr > 0) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                t_anz, t_amt, t_tax, t_inv, lscheinnr = assign_create_list11a(t_anz, t_amt, t_tax, t_inv, lscheinnr)

        else:

            l_op_obj_list = []
            for l_op, l_artikel, l_lieferant in db_session.query(L_op, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr > 0) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 1) &  (L_op.lager_nr == store)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                t_anz, t_amt, t_tax, t_inv, lscheinnr = assign_create_list11a(t_anz, t_amt, t_tax, t_inv, lscheinnr)

        t_anz, t_amt, t_tax, t_inv = create_hislist(t_anz, t_amt, t_tax, t_inv)
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.DESCRIPTION = "T O T A L"
        str_list.qty = t_anz
        str_list.inc_qty = t_anz
        str_list.amount = t_amt
        str_list.tax_amount = t_tax
        str_list.tot_amt = t_inv


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.DESCRIPTION = "GRAND TOTAL"
        str_list.qty = tot_anz
        str_list.inc_qty = tot_anz
        str_list.amount = tot_amount
        str_list.tax_amount = tot_tax
        str_list.tot_amt = tot_amt

    def assign_create_list11a(t_anz:decimal, t_amt:decimal, t_tax:decimal, t_inv:decimal, lscheinnr:str):

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_list, lvcarea, tot_anz, tot_amount, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal usr


        nonlocal str_list, taxcode_list, usr
        nonlocal str_list_list, taxcode_list_list

        amt:decimal = 0

        l_ophdr = db_session.query(L_ophdr).filter(
                (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()

        if lscheinnr == "":
            lscheinnr = l_op.lscheinnr

        if lscheinnr != l_op.lscheinnr:
            lscheinnr = l_op.lscheinnr
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.DESCRIPTION = "T O T A L"
            str_list.qty = t_anz
            str_list.inc_qty = t_anz
            str_list.amount = t_amt
            str_list.tax_amount = t_tax
            str_list.tot_amt = t_inv
            t_anz = 0
            t_amt = 0
            t_tax = 0
            t_inv = 0


            str_list = Str_list()
            str_list_list.append(str_list)

        t_anz = t_anz + l_op.anzahl

        if show_price:
            t_amt = t_amt + l_op.warenwert
        tot_anz = tot_anz + l_op.anzahl

        if show_price:
            tot_amount = tot_amount + l_op.warenwert

        if show_price:
            unit_price = l_op.einzelpreis

        str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis), first=True)

        if str_list:
            str_list.qty = str_list.qty + l_op.anzahl

            if show_price:
                str_list.warenwert = str_list.warenwert + l_op.warenwert
            str_list.inc_qty = str_list.qty
            str_list.amount = str_list.warenwert

            taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

            if taxcode_list:
                amt = l_op.warenwert * taxcode_list.taxamount
                str_list.tax_amount = str_list.tax_amount + (l_op.warenwert * taxcode_list.taxamount)
                t_tax = t_tax + (l_op.warenwert * taxcode_list.taxamount)
                tot_tax = tot_tax + (l_op.warenwert * taxcode_list.taxamount)
                str_list.tot_amt = str_list.tot_amt + (l_op.warenwert + amt)
                t_inv = t_inv + (l_op.warenwert + amt)
                tot_amt = tot_amt + (l_op.warenwert + amt)


        else:
            str_list = Str_list()
            str_list_list.append(str_list)

            add_id()

            if l_ophdr:
                str_list.invoice_nr = l_ophdr.fibukonto
                str_list.h_recid = l_ophdr._recid
            str_list.l_recid = l_op._recid
            str_list.lief_nr = l_op.lief_nr
            str_list.billdate = l_op.datum
            str_list.artnr = l_op.artnr
            str_list.lager_nr = l_op.lager_nr
            str_list.docu_nr = l_op.docu_nr
            str_list.lscheinnr = l_op.lscheinnr
            str_list.qty = l_op.anzahl
            str_list.epreis = l_op.einzelpreis

            if show_price:
                str_list.warenwert = l_op.warenwert
            str_list.fibu = convert_fibu(l_op.stornogrund)
            str_list.DATE = l_op.datum
            str_list.st = l_op.lager_nr
            str_list.article = l_artikel.artnr
            str_list.DESCRIPTION = l_artikel.bezeich
            str_list.d_unit = l_artikel.traubensort
            str_list.inc_qty = l_op.anzahl
            str_list.amount = str_list.warenwert
            str_list.supplier = l_lieferant.firma
            str_list.tax_code = l_artikel.lief_artnr[2]

            if l_lieferant.plz != " ":

                if re.match(".*#.*",l_lieferant.plz):
                    for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                        if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                            str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                            return

            taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

            if taxcode_list:
                str_list.tax_amount = l_op.warenwert * taxcode_list.taxamount
                t_tax = t_tax + (l_op.warenwert * taxcode_list.taxamount)
                tot_tax = tot_tax + (l_op.warenwert * taxcode_list.taxamount)
                str_list.tot_amt = l_op.warenwert + str_list.tax_amount
                t_inv = t_inv + (l_op.warenwert + str_list.tax_amount)
                tot_amt = tot_amt + (l_op.warenwert + str_list.tax_amount)

            if l_op.docu_nr == l_op.lscheinnr:
                str_list.docu_no = translateExtended ("Direct Purchase   ", lvcarea, "")
            else:
                str_list.docu_no = l_op.docu_nr
            str_list.deliv_note = l_op.lscheinnr
            str_list.price = unit_price

    def create_list11b():

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_list, lvcarea, tot_anz, tot_amount, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal usr


        nonlocal str_list, taxcode_list, usr
        nonlocal str_list_list, taxcode_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        t_tax:decimal = 0
        t_inv:decimal = 0
        lief_nr:int = 0
        lscheinnr:str = ""
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0
        tot_tax = 0
        tot_tax = 0
        tot_amt = 0

        if store == 0:

            l_op_obj_list = []
            for l_op, l_artikel, l_untergrup, l_lieferant in db_session.query(L_op, L_artikel, L_untergrup, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr > 0) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                t_anz, t_amt, t_tax, t_inv, lscheinnr = assign_create_list11b(t_anz, t_amt, t_tax, t_inv, lscheinnr)

        else:

            l_op_obj_list = []
            for l_op, l_artikel, l_untergrup, l_lieferant in db_session.query(L_op, L_artikel, L_untergrup, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr > 0) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 1) &  (L_op.lager_nr == store)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                t_anz, t_amt, t_tax, t_inv, lscheinnr = assign_create_list11b(t_anz, t_amt, t_tax, t_inv, lscheinnr)

        t_anz, t_amt, t_tax, t_inv = create_hislist(t_anz, t_amt, t_tax, t_inv)
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.DESCRIPTION = lscheinnr
        str_list.qty = t_anz
        str_list.inc_qty = t_anz
        str_list.amount = t_amt
        str_list.tax_amount = t_tax
        str_list.tot_amt = t_inv
        str_list.supplier = "T O T A L"


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.DESCRIPTION = "GRAND TOTAL"
        str_list.qty = tot_anz
        str_list.inc_qty = tot_anz
        str_list.amount = tot_amount
        str_list.tax_amount = tot_tax
        str_list.tot_amt = tot_amt

    def assign_create_list11b(t_anz:decimal, t_amt:decimal, t_tax:decimal, t_inv:decimal, lscheinnr:str):

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_list, lvcarea, tot_anz, tot_amount, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal usr


        nonlocal str_list, taxcode_list, usr
        nonlocal str_list_list, taxcode_list_list

        amt:decimal = 0

        l_ophdr = db_session.query(L_ophdr).filter(
                (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()

        if lscheinnr == "":
            lscheinnr = l_untergrup.bezeich

        if lscheinnr != l_untergrup.bezeich:
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.DESCRIPTION = lscheinnr
            str_list.qty = t_anz
            str_list.inc_qty = t_anz
            str_list.amount = t_amt
            str_list.supplier = "T O T A L"
            str_list.tax_amount = t_tax
            str_list.tot_amt = t_inv


            lscheinnr = l_untergrup.bezeich
            t_anz = 0
            t_amt = 0
            t_tax = 0
            t_inv = 0
            str_list = Str_list()
            str_list_list.append(str_list)

        t_anz = t_anz + l_op.anzahl

        if show_price:
            t_amt = t_amt + l_op.warenwert
        tot_anz = tot_anz + l_op.anzahl

        if show_price:
            tot_amount = tot_amount + l_op.warenwert

        if show_price:
            unit_price = l_op.einzelpreis

        str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

        if str_list:
            str_list.qty = str_list.qty + l_op.anzahl

            if show_price:
                str_list.warenwert = str_list.warenwert + l_op.warenwert
            str_list.inc_qty = str_list.qty
            str_list.amount = str_list.warenwert

            taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

            if taxcode_list:
                amt = l_op.warenwert * taxcode_list.taxamount
                str_list.tax_amount = str_list.tax_amount + (l_op.warenwert * taxcode_list.taxamount)
                t_tax = t_tax + (l_op.warenwert * taxcode_list.taxamount)
                tot_tax = tot_tax + (l_op.warenwert * taxcode_list.taxamount)
                str_list.tot_amt = str_list.tot_amt + (l_op.warenwert + amt)
                t_inv = t_inv + (l_op.warenwert + amt)
                tot_amt = tot_amt + (l_op.warenwert + amt)


        else:
            str_list = Str_list()
            str_list_list.append(str_list)

            add_id()

            if l_ophdr:
                str_list.invoice_nr = l_ophdr.fibukonto
                str_list.h_recid = l_ophdr._recid
            str_list.l_recid = l_op._recid
            str_list.lief_nr = l_op.lief_nr
            str_list.billdate = l_op.datum
            str_list.artnr = l_op.artnr
            str_list.lager_nr = l_op.lager_nr
            str_list.docu_nr = l_op.docu_nr
            str_list.lscheinnr = l_op.lscheinnr
            str_list.qty = l_op.anzahl
            str_list.epreis = l_op.einzelpreis

            if show_price:
                str_list.warenwert = l_op.warenwert
            str_list.fibu = convert_fibu(l_op.stornogrund)
            str_list.DATE = l_op.datum
            str_list.st = l_op.lager_nr
            str_list.article = l_artikel.artnr
            str_list.DESCRIPTION = l_artikel.bezeich
            str_list.d_unit = l_artikel.traubensort
            str_list.inc_qty = l_op.anzahl
            str_list.amount = str_list.warenwert
            str_list.supplier = l_lieferant.firma
            str_list.tax_code = l_artikel.lief_artnr[2]

            if l_lieferant.plz != " ":

                if re.match(".*#.*",l_lieferant.plz):
                    for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                        if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                            str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                            return

            taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

            if taxcode_list:
                str_list.tax_amount = l_op.warenwert * taxcode_list.taxamount
                t_tax = t_tax + (l_op.warenwert * taxcode_list.taxamount)
                tot_tax = tot_tax + (l_op.warenwert * taxcode_list.taxamount)
                str_list.tot_amt = l_op.warenwert + str_list.tax_amount
                t_inv = t_inv + (l_op.warenwert + str_list.tax_amount)
                tot_amt = tot_amt + (l_op.warenwert + str_list.tax_amount)

            if l_op.docu_nr == l_op.lscheinnr:
                str_list.docu_no = translateExtended ("Direct Purchase   ", lvcarea, "")
            else:
                str_list.docu_no = l_op.docu_nr
            str_list.deliv_note = l_op.lscheinnr
            str_list.price = unit_price

    def create_hislist(t_anz:decimal, t_amt:decimal, t_tax:decimal, t_inv:decimal):

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_list, lvcarea, tot_anz, tot_amount, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal usr


        nonlocal str_list, taxcode_list, usr
        nonlocal str_list_list, taxcode_list_list

        close_date:date = None
        close_date2:date = None

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 224)).first()
        close_date = htparam.fdate

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 221)).first()
        close_date2 = htparam.fdate

        if ap_recid == 0:

            return

        if from_date != to_date:

            return

        if close_date < close_date2:
            close_date = close_date2
        close_date = date_mdy(get_month(close_date) , 1, get_year(close_date))

        if to_date >= close_date:

            return

        for l_ophis in db_session.query(L_ophis).filter(
                (L_ophis.docu_nr == l_kredit.name) &  (L_ophis.lscheinnr == l_kredit.lscheinnr) &  (L_ophis.op_art == 1) &  (L_ophis.datum == to_date)).all():
            t_anz = t_anz + l_ophis.anzahl
            t_amt = t_amt + l_ophis.warenwert

            l_lieferant = db_session.query(L_lieferant).filter(
                    (L_lieferant.lief_nr == l_ophis.lief_nr)).first()

            l_artikel = db_session.query(L_artikel).filter(
                    (L_artikel.artnr == l_ophis.artnr)).first()

            l_ophhis = db_session.query(L_ophhis).filter(
                    (func.lower(L_ophhis.op_typ) == "STI") &  (L_ophhis.lscheinnr == l_ophis.lscheinnr) &  (L_ophhis.datum == l_ophis.datum)).first()
            str_list = Str_list()
            str_list_list.append(str_list)


            if l_ophhis:
                str_list.invoice_nr = l_ophhis.fibukonto
                str_list.h_recid = 0
            str_list.l_recid = 0
            str_list.lief_nr = l_ophis.lief_nr
            str_list.billdate = l_ophis.datum
            str_list.artnr = l_ophis.artnr
            str_list.lager_nr = l_ophis.lager_nr
            str_list.docu_nr = l_ophis.docu_nr
            str_list.lscheinnr = l_ophis.lscheinnr
            str_list.qty = l_ophis.anzahl
            str_list.epreis = l_ophis.einzelpreis
            str_list.warenwert = l_ophis.warenwert
            str_list.DATE = l_ophis.datum
            str_list.st = l_ophis.lager_nr
            str_list.article = l_artikel.artnr
            str_list.DESCRIPTION = l_artikel.bezeich
            str_list.d_unit = l_artikel.traubensort
            str_list.inc_qty = l_ophis.anzahl
            str_list.amount = str_list.warenwert
            str_list.supplier = l_lieferant.firma
            str_list.tax_code = l_artikel.lief_artnr[2]

            taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

            if taxcode_list:
                str_list.tax_amount = l_ophis.warenwert * taxcode_list.taxamount
                t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                str_list.tot_amt = l_ophis.warenwert + str_list.tax_amount
                t_inv = t_inv + (l_ophis.warenwert + str_list.tax_amount)

            if l_ophis.docu_nr == l_ophis.lscheinnr:
                str_list.docu_no = "Direct Purchase"
            else:
                str_list.docu_no = l_ophis.docu_nr
            str_list.deliv_note = l_ophis.lscheinnr
            str_list.price = unit_price


            str_list.fibu = convert_fibu(l_ophhis.fibukonto)

    def create_list22():

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_list, lvcarea, tot_anz, tot_amount, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal usr


        nonlocal str_list, taxcode_list, usr
        nonlocal str_list_list, taxcode_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        t_tax:decimal = 0
        t_inv:decimal = 0
        lscheinnr:str = " "
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0
        tot_tax = 0
        tot_amt = 0

        if store == 0:

            l_op_obj_list = []
            for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr == l_lieferant.lief_nr) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                t_anz, t_amt, t_tax, t_inv, lscheinnr = assign_create_list22(t_anz, t_amt, t_tax, t_inv, lscheinnr)

        else:

            l_op_obj_list = []
            for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr == l_lieferant.lief_nr) &  (L_op.loeschflag <= 1) &  (L_op.lager_nr == store) &  (L_op.op_art == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                t_anz, t_amt, t_tax, t_inv, lscheinnr = assign_create_list22(t_anz, t_amt, t_tax, t_inv, lscheinnr)

        t_anz, t_amt, t_tax, t_inv = create_hislist(t_anz, t_amt, t_tax, t_inv)
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.DESCRIPTION = "T O T A L"
        str_list.qty = t_anz
        str_list.inc_qty = t_anz
        str_list.amount = t_amt
        str_list.tax_amount = t_tax
        str_list.tot_amt = t_inv


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.DESCRIPTION = "GRAND TOTAL"
        str_list.qty = tot_anz
        str_list.inc_qty = tot_anz
        str_list.amount = tot_amount
        str_list.tax_amount = tot_tax
        str_list.tot_amt = tot_amt

    def assign_create_list22(t_anz:decimal, t_amt:decimal, t_tax:decimal, t_inv:decimal, lscheinnr:str):

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_list, lvcarea, tot_anz, tot_amount, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal usr


        nonlocal str_list, taxcode_list, usr
        nonlocal str_list_list, taxcode_list_list

        amt:decimal = 0

        l_ophdr = db_session.query(L_ophdr).filter(
                (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()

        if lscheinnr == "":
            lscheinnr = l_op.lscheinnr

        if lscheinnr != l_op.lscheinnr:
            lscheinnr = l_op.lscheinnr
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.DESCRIPTION = "T O T A L"
            str_list.qty = t_anz
            str_list.inc_qty = t_anz
            str_list.amount = t_amt
            str_list.tax_amount = t_tax
            str_list.tot_amt = t_inv


            t_anz = 0
            t_amt = 0
            t_tax = 0
            t_inv = 0
            str_list = Str_list()
            str_list_list.append(str_list)

        tot_anz = tot_anz + l_op.anzahl
        tot_amount = tot_amount + l_op.warenwert

        if show_price:
            unit_price = l_op.einzelpreis

        str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis), first=True)

        if str_list:
            str_list.qty = str_list.qty + l_op.anzahl

            if show_price:
                str_list.warenwert = str_list.warenwert + l_op.warenwert
            str_list.inc_qty = str_list.qty
            str_list.amount = str_list.warenwert

            taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

            if taxcode_list:
                amt = l_op.warenwert * taxcode_list.taxamount
                str_list.tax_amount = str_list.tax_amount + (l_op.warenwert * taxcode_list.taxamount)
                tot_tax = tot_tax + (l_op.warenwert * taxcode_list.taxamount)
                str_list.tot_amt = str_list.tot_amt + (l_op.warenwert + amt)
                tot_amt = tot_amt + (l_op.warenwert + amt)


        else:
            str_list = Str_list()
            str_list_list.append(str_list)

            add_id()

            if l_ophdr:
                str_list.invoice_nr = l_ophdr.fibukonto
                str_list.h_recid = l_ophdr._recid
            str_list.l_recid = l_op._recid
            str_list.lief_nr = l_op.lief_nr
            str_list.billdate = l_op.datum
            str_list.artnr = l_op.artnr
            str_list.lager_nr = l_op.lager_nr
            str_list.docu_nr = l_op.docu_nr
            str_list.lscheinnr = l_op.lscheinnr
            str_list.qty = l_op.anzahl
            str_list.epreis = l_op.einzelpreis

            if show_price:
                str_list.warenwert = l_op.warenwert
            str_list.fibu = convert_fibu(l_op.stornogrund)
            str_list.DATE = l_op.datum
            str_list.st = l_op.lager_nr
            str_list.article = l_artikel.artnr
            str_list.DESCRIPTION = l_artikel.bezeich
            str_list.d_unit = l_artikel.traubensort
            str_list.inc_qty = l_op.anzahl
            str_list.amount = str_list.warenwert
            str_list.supplier = l_lieferant.firma
            str_list.docu_no = l_op.docu_nr
            str_list.deliv_note = l_op.lscheinnr
            str_list.price = unit_price
            str_list.tax_code = l_artikel.lief_artnr[2]

            if l_lieferant.plz != " ":

                if re.match(".*#.*",l_lieferant.plz):
                    for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                        if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                            str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                            return

            taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

            if taxcode_list:
                str_list.tax_amount = l_op.warenwert * taxcode_list.taxamount
                tot_tax = tot_tax + (l_op.warenwert * taxcode_list.taxamount)
                str_list.tot_amt = l_op.warenwert + str_list.tax_amount
                tot_amt = tot_amt + (l_op.warenwert + str_list.tax_amount)

    def create_list22a():

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_list, lvcarea, tot_anz, tot_amount, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal usr


        nonlocal str_list, taxcode_list, usr
        nonlocal str_list_list, taxcode_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        t_tax:decimal = 0
        t_inv:decimal = 0
        lscheinnr:str = ""
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0
        tot_tax = 0
        tot_tax = 0
        tot_amt = 0

        if store == 0:

            l_op_obj_list = []
            for l_op, l_artikel, l_lieferant in db_session.query(L_op, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr == l_lieferant.lief_nr) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                t_anz, t_amt, t_tax, t_inv, lscheinnr = assign_create_list22a(t_anz, t_amt, t_tax, t_inv, lscheinnr)

        else:

            l_op_obj_list = []
            for l_op, l_artikel, l_lieferant in db_session.query(L_op, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr == l_lieferant.lief_nr) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 1) &  (L_op.lager_nr == store)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                t_anz, t_amt, t_tax, t_inv, lscheinnr = assign_create_list22a(t_anz, t_amt, t_tax, t_inv, lscheinnr)

        t_anz, t_amt, t_tax, t_inv = create_hislist(t_anz, t_amt, t_tax, t_inv)
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.DESCRIPTION = "T O T A L"
        str_list.qty = t_anz
        str_list.inc_qty = t_anz
        str_list.amount = t_amt
        str_list.tax_amount = t_tax
        str_list.tot_amt = t_inv


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.DESCRIPTION = "GRAND TOTAL"
        str_list.qty = tot_anz
        str_list.inc_qty = tot_anz
        str_list.amount = tot_amount
        str_list.tax_amount = tot_tax
        str_list.tot_amt = tot_amt

    def assign_create_list22a(t_anz:decimal, t_amt:decimal, t_tax:decimal, t_inv:decimal, lscheinnr:str):

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_list, lvcarea, tot_anz, tot_amount, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal usr


        nonlocal str_list, taxcode_list, usr
        nonlocal str_list_list, taxcode_list_list

        amt:decimal = 0

        l_ophdr = db_session.query(L_ophdr).filter(
                (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()

        if lscheinnr == "":
            lscheinnr = l_op.lscheinnr

        if lscheinnr != l_op.lscheinnr:
            lscheinnr = l_op.lscheinnr
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.DESCRIPTION = "T O T A L"
            str_list.qty = t_anz
            str_list.inc_qty = t_anz
            str_list.amount = t_amt
            str_list.tax_amount = t_tax
            str_list.tot_amt = t_inv


            t_anz = 0
            t_amt = 0
            t_tax = 0
            t_inv = 0
            str_list = Str_list()
            str_list_list.append(str_list)

        t_anz = t_anz + l_op.anzahl

        if show_price:
            t_amt = t_amt + l_op.warenwert
        tot_anz = tot_anz + l_op.anzahl

        if show_price:
            tot_amount = tot_amount + l_op.warenwert

        if show_price:
            unit_price = l_op.einzelpreis

        str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis), first=True)

        if str_list:
            str_list.qty = str_list.qty + l_op.anzahl

            if show_price:
                str_list.warenwert = str_list.warenwert + l_op.warenwert
            str_list.inc_qty = str_list.qty
            str_list.amount = str_list.warenwert

            taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

            if taxcode_list:
                amt = l_op.warenwert * taxcode_list.taxamount
                str_list.tax_amount = str_list.tax_amount + (l_op.warenwert * taxcode_list.taxamount)
                t_tax = t_tax + (l_op.warenwert * taxcode_list.taxamount)
                tot_tax = tot_tax + (l_op.warenwert * taxcode_list.taxamount)
                str_list.tot_amt = str_list.tot_amt + (l_op.warenwert + amt)
                t_inv = t_inv + (l_op.warenwert + amt)
                tot_amt = tot_amt + (l_op.warenwert + amt)


        else:
            str_list = Str_list()
            str_list_list.append(str_list)

            add_id()

            if l_ophdr:
                str_list.invoice_nr = l_ophdr.fibukonto
                str_list.h_recid = l_ophdr._recid
            str_list.l_recid = l_op._recid
            str_list.lief_nr = l_op.lief_nr
            str_list.billdate = l_op.datum
            str_list.artnr = l_op.artnr
            str_list.lager_nr = l_op.lager_nr
            str_list.docu_nr = l_op.docu_nr
            str_list.lscheinnr = l_op.lscheinnr
            str_list.qty = l_op.anzahl
            str_list.epreis = l_op.einzelpreis

            if show_price:
                str_list.warenwert = l_op.warenwert
            str_list.fibu = convert_fibu(l_op.stornogrund)
            str_list.DATE = l_op.datum
            str_list.st = l_op.lager_nr
            str_list.article = l_artikel.artnr
            str_list.DESCRIPTION = l_artikel.bezeich
            str_list.d_unit = l_artikel.traubensort
            str_list.inc_qty = l_op.anzahl
            str_list.amount = str_list.warenwert
            str_list.supplier = l_lieferant.firma
            str_list.tax_code = l_artikel.lief_artnr[2]

            if l_lieferant.plz != " ":

                if re.match(".*#.*",l_lieferant.plz):
                    for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                        if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                            str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                            return

            taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

            if taxcode_list:
                str_list.tax_amount = l_op.warenwert * taxcode_list.taxamount
                t_tax = t_tax + (l_op.warenwert * taxcode_list.taxamount)
                tot_tax = tot_tax + (l_op.warenwert * taxcode_list.taxamount)
                str_list.tot_amt = l_op.warenwert + str_list.tax_amount
                t_inv = t_inv + (l_op.warenwert + str_list.tax_amount)
                tot_amt = tot_amt + (l_op.warenwert + str_list.tax_amount)

            if l_op.docu_nr == l_op.lscheinnr:
                str_list.docu_no = translateExtended ("Direct Purchase   ", lvcarea, "")
            else:
                str_list.docu_no = l_op.docu_nr
            str_list.deliv_note = l_op.lscheinnr
            str_list.price = unit_price

    def create_list22b():

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_list, lvcarea, tot_anz, tot_amount, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal usr


        nonlocal str_list, taxcode_list, usr
        nonlocal str_list_list, taxcode_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        t_tax:decimal = 0
        t_inv:decimal = 0
        lief_nr:int = 0
        lscheinnr:str = ""
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0
        tot_tax = 0
        tot_tax = 0
        tot_amt = 0

        if store == 0:

            l_op_obj_list = []
            for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr == l_lieferant.lief_nr) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                t_anz, t_amt, t_tax, t_inv, lscheinnr = assign_create_list22b(t_anz, t_amt, t_tax, t_inv, lscheinnr)

        else:

            l_op_obj_list = []
            for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr == l_lieferant.lief_nr) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 1) &  (L_op.lager_nr == store)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                t_anz, t_amt, t_tax, t_inv, lscheinnr = assign_create_list22b(t_anz, t_amt, t_tax, t_inv, lscheinnr)

        t_anz, t_amt, t_tax, t_inv = create_hislist(t_anz, t_amt, t_tax, t_inv)
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.DESCRIPTION = lscheinnr
        str_list.qty = t_anz
        str_list.inc_qty = t_anz
        str_list.amount = t_amt
        str_list.tax_amount = t_tax
        str_list.tot_amt = t_inv


        str_list.supplier = "T O T A L"
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.DESCRIPTION = "GRAND TOTAL"
        str_list.qty = tot_anz
        str_list.inc_qty = tot_anz
        str_list.amount = tot_amount
        str_list.tax_amount = tot_tax
        str_list.tot_amt = tot_amt

    def assign_create_list22b(t_anz:decimal, t_amt:decimal, t_tax:decimal, t_inv:decimal, lscheinnr:str):

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_list, lvcarea, tot_anz, tot_amount, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal usr


        nonlocal str_list, taxcode_list, usr
        nonlocal str_list_list, taxcode_list_list

        amt:decimal = 0

        l_ophdr = db_session.query(L_ophdr).filter(
                (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()

        if lscheinnr == "":
            lscheinnr = l_untergrup.bezeich

        if lscheinnr != l_untergrup.bezeich:
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.DESCRIPTION = lscheinnr
            str_list.qty = t_anz
            str_list.inc_qty = t_anz
            str_list.amount = t_amt
            str_list.tax_amount = t_tax
            str_list.tot_amt = t_inv
            str_list.supplier = "T O T A L"
            lscheinnr = l_untergrup.bezeich


            t_anz = 0
            t_amt = 0
            t_tax = 0
            t_inv = 0
            str_list = Str_list()
            str_list_list.append(str_list)

        t_anz = t_anz + l_op.anzahl

        if show_price:
            t_amt = t_amt + l_op.warenwert
        tot_anz = tot_anz + l_op.anzahl

        if show_price:
            tot_amount = tot_amount + l_op.warenwert

        if show_price:
            unit_price = l_op.einzelpreis

        str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

        if str_list:
            str_list.qty = str_list.qty + l_op.anzahl

            if show_price:
                str_list.warenwert = str_list.warenwert + l_op.warenwert
            str_list.inc_qty = str_list.qty
            str_list.amount = str_list.warenwert

            taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

            if taxcode_list:
                amt = l_op.warenwert * taxcode_list.taxamount
                str_list.tax_amount = str_list.tax_amount + (l_op.warenwert * taxcode_list.taxamount)
                t_tax = t_tax + (l_op.warenwert * taxcode_list.taxamount)
                tot_tax = tot_tax + (l_op.warenwert * taxcode_list.taxamount)
                str_list.tot_amt = str_list.tot_amt + (l_op.warenwert + amt)
                t_inv = t_inv + (l_op.warenwert + amt)
                tot_amt = tot_amt + (l_op.warenwert + amt)


        else:
            str_list = Str_list()
            str_list_list.append(str_list)

            add_id()

            if l_ophdr:
                str_list.invoice_nr = l_ophdr.fibukonto
                str_list.h_recid = l_ophdr._recid
            str_list.l_recid = l_op._recid
            str_list.lief_nr = l_op.lief_nr
            str_list.billdate = l_op.datum
            str_list.artnr = l_op.artnr
            str_list.lager_nr = l_op.lager_nr
            str_list.docu_nr = l_op.docu_nr
            str_list.lscheinnr = l_op.lscheinnr
            str_list.qty = l_op.anzahl
            str_list.epreis = l_op.einzelpreis

            if show_price:
                str_list.warenwert = l_op.warenwert
            str_list.fibu = convert_fibu(l_op.stornogrund)
            str_list.DATE = l_op.datum
            str_list.st = l_op.lager_nr
            str_list.article = l_artikel.artnr
            str_list.DESCRIPTION = l_artikel.bezeich
            str_list.d_unit = l_artikel.traubensort
            str_list.inc_qty = l_op.anzahl
            str_list.amount = str_list.warenwert
            str_list.supplier = l_lieferant.firma
            str_list.tax_code = l_artikel.lief_artnr[2]

            if l_lieferant.plz != " ":

                if re.match(".*#.*",l_lieferant.plz):
                    for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                        if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                            str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                            return

            taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

            if taxcode_list:
                str_list.tax_amount = l_op.warenwert * taxcode_list.taxamount
                t_tax = t_tax + (l_op.warenwert * taxcode_list.taxamount)
                tot_tax = tot_tax + (l_op.warenwert * taxcode_list.taxamount)
                str_list.tot_amt = l_op.warenwert + str_list.tax_amount
                t_inv = t_inv + (l_op.warenwert + str_list.tax_amount)
                tot_amt = tot_amt + (l_op.warenwert + str_list.tax_amount)

            if l_op.docu_nr == l_op.lscheinnr:
                str_list.docu_no = translateExtended ("Direct Purchase ", lvcarea, "")
            else:
                str_list.docu_no = l_op.docu_nr
            str_list.deliv_note = l_op.lscheinnr
            str_list.price = unit_price

    def add_id():

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_list, lvcarea, tot_anz, tot_amount, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal usr


        nonlocal str_list, taxcode_list, usr
        nonlocal str_list_list, taxcode_list_list


        Usr = Bediener

        usr = db_session.query(Usr).filter(
                (Usr.nr == l_op.fuellflag)).first()

        if usr:
            str_list.id = usr.userinit
        else:
            str_list.id = "??"

    def convert_fibu(konto:str):

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_list, lvcarea, tot_anz, tot_amount, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal usr


        nonlocal str_list, taxcode_list, usr
        nonlocal str_list_list, taxcode_list_list

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


    l_lieferant = db_session.query(L_lieferant).filter(
            (L_lieferant._recid == lieferant_recid)).first()

    l_kredit = db_session.query(L_kredit).filter(
            (L_kredit._recid == l_kredit_recid)).first()

    if all_supp and sorttype == 1:
        create_list11()

    elif not all_supp and sorttype == 1:
        create_list22()

    elif all_supp and sorttype == 2:
        create_list11a()

    elif not all_supp and sorttype == 2:
        create_list22a()

    elif all_supp and sorttype == 3:
        create_list11b()

    elif not all_supp and sorttype == 3:
        create_list22b()

    return generate_output()