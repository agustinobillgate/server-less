from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
import re
from models import Htparam, L_lieferant, L_ophis, L_artikel, L_untergrup

def supply_hinlist_btn_go_1bl(pvilanguage:int, from_supp:str, from_doc:str, sorttype:int, from_grp:int, to_grp:int, store:int, all_supp:bool, all_doc:bool, from_date:date, to_date:date, taxcode_list:[Taxcode_list]):
    err_code = 0
    str_list_list = []
    i:int = 0
    supp_nr:int = 0
    tot_anz:decimal = 0
    tot_amount:decimal = 0
    long_digit:bool = False
    tot_tax:decimal = 0
    tot_amt:decimal = 0
    loopi:int = 0
    lvcarea:str = "supply_hinlist"
    htparam = l_lieferant = l_ophis = l_artikel = l_untergrup = None

    str_list = taxcode_list = None

    str_list_list, Str_list = create_model("Str_list", {"artnr":int, "lager_nr":int, "docu_nr":str, "lscheinnr":str, "qty":decimal, "epreis":decimal, "warenwert":decimal, "datum":date, "st":int, "supplier":str, "article":int, "description":str, "d_unit":str, "price":decimal, "inc_qty":decimal, "amount":decimal, "docu_no":str, "deliv_no":str, "gstid":str, "tax_code":str, "tax_amount":decimal, "tot_amt":decimal, "lief_nr":int})
    taxcode_list_list, Taxcode_list = create_model("Taxcode_list", {"taxcode":str, "taxamount":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup


        nonlocal str_list, taxcode_list
        nonlocal str_list_list, taxcode_list_list
        return {"err_code": err_code, "str-list": str_list_list}

    def create_list1a():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup


        nonlocal str_list, taxcode_list
        nonlocal str_list_list, taxcode_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        lief_nr:int = 0
        lscheinnr:str = ""
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0

        if store == 0:

            l_ophis_obj_list = []
            for l_ophis, l_artikel, l_lieferant in db_session.query(L_ophis, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr > 0) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr

                if lscheinnr != l_ophis.lscheinnr:
                    lscheinnr = l_ophis.lscheinnr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.supplier = "T O T A L"
                    str_list.qty = t_anz
                    str_list.inc_qty = t_anz
                    str_list.amount = t_amt


                    t_anz = 0
                    t_amt = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_ophis.anzahl
                t_amt = t_amt + l_ophis.warenwert
                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.lager_nr == l_ophis.lager_nr and str_list.artnr == l_ophis.artnr and str_list.artnr == l_ophis.artnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert
                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.lief_nr = l_ophis.lief_nr

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase   "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr


        else:

            l_ophis_obj_list = []
            for l_ophis, l_artikel, l_lieferant in db_session.query(L_ophis, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr > 0) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (L_ophis.lager_nr == store) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr

                if lscheinnr != l_ophis.lscheinnr:
                    lscheinnr = l_ophis.lscheinnr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.supplier = "T O T A L"
                    str_list.qty = t_anz
                    str_list.inc_qty = t_anz
                    str_list.amount = t_amt


                    t_anz = 0
                    t_amt = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_ophis.anzahl
                t_amt = t_amt + l_ophis.warenwert
                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.lager_nr == l_ophis.lager_nr and str_list.artnr == l_ophis.artnr and str_list.artnr == l_ophis.artnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert
                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.lief_nr = l_ophis.lief_nr

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase   "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "T O T A L"
        str_list.qty = t_anz
        str_list.inc_qty = t_anz
        str_list.amount = t_amt


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty = tot_anz
        str_list.inc_qty = tot_anz
        str_list.amount = tot_amount

    def create_list1ar():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup


        nonlocal str_list, taxcode_list
        nonlocal str_list_list, taxcode_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        lief_nr:int = 0
        lscheinnr:str = ""
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0

        if store == 0:

            l_ophis_obj_list = []
            for l_ophis, l_artikel, l_lieferant in db_session.query(L_ophis, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr > 0) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (func.lower(L_ophis.docu_nr) == (from_doc).lower()) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr

                if lscheinnr != l_ophis.lscheinnr:
                    lscheinnr = l_ophis.lscheinnr
                    t_anz = 0
                    t_amt = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_ophis.anzahl
                t_amt = t_amt + l_ophis.warenwert
                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.lager_nr == l_ophis.lager_nr and str_list.artnr == l_ophis.artnr and str_list.artnr == l_ophis.artnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert
                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.lief_nr = l_ophis.lief_nr

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase   "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        else:

            l_ophis_obj_list = []
            for l_ophis, l_artikel, l_lieferant in db_session.query(L_ophis, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr > 0) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (L_ophis.lager_nr == store) &  (func.lower(L_ophis.docu_nr) == (from_doc).lower()) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr

                if lscheinnr != l_ophis.lscheinnr:
                    lscheinnr = l_ophis.lscheinnr
                    t_anz = 0
                    t_amt = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_ophis.anzahl
                t_amt = t_amt + l_ophis.warenwert
                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.lager_nr == l_ophis.lager_nr and str_list.artnr == l_ophis.artnr and str_list.artnr == l_ophis.artnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert
                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.lief_nr = l_ophis.lief_nr

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase   "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty = tot_anz
        str_list.inc_qty = tot_anz
        str_list.amount = tot_amount

    def create_list11():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup


        nonlocal str_list, taxcode_list
        nonlocal str_list_list, taxcode_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        t_tax:decimal = 0
        t_inv:decimal = 0
        lief_nr:int = 0
        amt:decimal = 0
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0
        tot_tax = 0
        tot_amt = 0

        if store == 0:

            l_ophis_obj_list = []
            for l_ophis, l_artikel, l_lieferant in db_session.query(L_ophis, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr > 0) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                if lief_nr == 0:
                    lief_nr = l_lieferant.lief_nr

                if lief_nr != l_lieferant.lief_nr:
                    lief_nr = l_lieferant.lief_nr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.supplier = "T O T A L"
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

                t_anz = t_anz + l_ophis.anzahl
                t_amt = t_amt + l_ophis.warenwert
                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_ophis.warenwert * taxcode_list.taxamount
                        str_list.tax_amount = str_list.tax_amount + (l_ophis.warenwert * taxcode_list.taxamount)
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = str_list.tot_amt + (l_ophis.warenwert + amt)
                        t_inv = t_inv + (l_ophis.warenwert + amt)
                        tot_amt = tot_amt + (l_ophis.warenwert + amt)


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if re.match(".*#.*",l_lieferant.plz):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount = l_ophis.warenwert * taxcode_list.taxamount
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = l_ophis.warenwert + str_list.tax_amount
                        t_inv = t_inv + (l_ophis.warenwert + str_list.tax_amount)
                        tot_amt = tot_amt + (l_ophis.warenwert + str_list.tax_amount)

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase   "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr


        else:

            l_ophis_obj_list = []
            for l_ophis, l_artikel, l_lieferant in db_session.query(L_ophis, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr > 0) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (L_ophis.lager_nr == store) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                if lief_nr == 0:
                    lief_nr = l_lieferant.lief_nr

                if lief_nr != l_lieferant.lief_nr:
                    lief_nr = l_lieferant.lief_nr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.supplier = "T O T A L"
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

                t_anz = t_anz + l_ophis.anzahl
                t_amt = t_amt + l_ophis.warenwert
                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_ophis.warenwert * taxcode_list.taxamount
                        str_list.tax_amount = str_list.tax_amount + (l_ophis.warenwert * taxcode_list.taxamount)
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = str_list.tot_amt + (l_ophis.warenwert + amt)
                        t_inv = t_inv + (l_ophis.warenwert + amt)
                        tot_amt = tot_amt + (l_ophis.warenwert + amt)


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if re.match(".*#.*",l_lieferant.plz):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount = l_ophis.warenwert * taxcode_list.taxamount
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = l_ophis.warenwert + str_list.tax_amount
                        t_inv = t_inv + (l_ophis.warenwert + str_list.tax_amount)
                        tot_amt = tot_amt + (l_ophis.warenwert + str_list.tax_amount)

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase   "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "T O T A L"
        str_list.qty = t_anz
        str_list.inc_qty = t_anz
        str_list.amount = t_amt
        str_list.tax_amount = t_tax
        str_list.tot_amt = t_inv


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty = tot_anz
        str_list.inc_qty = tot_anz
        str_list.amount = tot_amount
        str_list.tax_amount = tot_tax
        str_list.tot_amt = tot_amt

    def create_list11a():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup


        nonlocal str_list, taxcode_list
        nonlocal str_list_list, taxcode_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        t_tax:decimal = 0
        t_inv:decimal = 0
        lscheinnr:str = ""
        amt:decimal = 0
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0
        tot_tax = 0
        tot_amt = 0

        if store == 0:

            l_ophis_obj_list = []
            for l_ophis, l_artikel, l_lieferant in db_session.query(L_ophis, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr > 0) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr

                if lscheinnr != l_ophis.lscheinnr:
                    lscheinnr = l_ophis.lscheinnr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.supplier = "T O T A L"
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

                t_anz = t_anz + l_ophis.anzahl
                t_amt = t_amt + l_ophis.warenwert
                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_ophis.warenwert * taxcode_list.taxamount
                        str_list.tax_amount = str_list.tax_amount + (l_ophis.warenwert * taxcode_list.taxamount)
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = str_list.tot_amt + (l_ophis.warenwert + amt)
                        t_inv = t_inv + (l_ophis.warenwert + amt)
                        tot_amt = tot_amt + (l_ophis.warenwert + amt)


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if re.match(".*#.*",l_lieferant.plz):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount = l_ophis.warenwert * taxcode_list.taxamount
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = l_ophis.warenwert + str_list.tax_amount
                        t_inv = t_inv + (l_ophis.warenwert + str_list.tax_amount)
                        tot_amt = tot_amt + (l_ophis.warenwert + str_list.tax_amount)

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase   "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        else:

            l_ophis_obj_list = []
            for l_ophis, l_artikel, l_lieferant in db_session.query(L_ophis, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr > 0) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (L_ophis.lager_nr == store) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr

                if lscheinnr != l_ophis.lscheinnr:
                    lscheinnr = l_ophis.lscheinnr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.supplier = "T O T A L"
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

                t_anz = t_anz + l_ophis.anzahl
                t_amt = t_amt + l_ophis.warenwert
                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_ophis.warenwert * taxcode_list.taxamount
                        str_list.tax_amount = str_list.tax_amount + (l_ophis.warenwert * taxcode_list.taxamount)
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = str_list.tot_amt + (l_ophis.warenwert + amt)
                        t_inv = t_inv + (l_ophis.warenwert + amt)
                        tot_amt = tot_amt + (l_ophis.warenwert + amt)


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if re.match(".*#.*",l_lieferant.plz):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount = l_ophis.warenwert * taxcode_list.taxamount
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = l_ophis.warenwert + str_list.tax_amount
                        t_inv = t_inv + (l_ophis.warenwert + str_list.tax_amount)
                        tot_amt = tot_amt + (l_ophis.warenwert + str_list.tax_amount)

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase   "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "T O T A L"
        str_list.qty = t_anz
        str_list.inc_qty = t_anz
        str_list.amount = t_amt
        str_list.tax_amount = t_tax
        str_list.tot_amt = t_inv


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty = tot_anz
        str_list.inc_qty = tot_anz
        str_list.amount = tot_amount
        str_list.tax_amount = tot_tax
        str_list.tot_amt = tot_amt

    def create_list11ar():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup


        nonlocal str_list, taxcode_list
        nonlocal str_list_list, taxcode_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        t_tax:decimal = 0
        t_inv:decimal = 0
        lscheinnr:str = ""
        amt:decimal = 0
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0
        tot_tax = 0
        tot_amt = 0

        if store == 0:

            l_ophis_obj_list = []
            for l_ophis, l_artikel, l_lieferant in db_session.query(L_ophis, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr > 0) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (func.lower(L_ophis.docu_nr) == (from_doc).lower()) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr

                if lscheinnr != l_ophis.lscheinnr:
                    lscheinnr = l_ophis.lscheinnr
                    t_anz = 0
                    t_amt = 0
                    t_tax = 0
                    t_inv = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_ophis.anzahl
                t_amt = t_amt + l_ophis.warenwert
                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_ophis.warenwert * taxcode_list.taxamount
                        str_list.tax_amount = str_list.tax_amount + (l_ophis.warenwert * taxcode_list.taxamount)
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = str_list.tot_amt + (l_ophis.warenwert + amt)
                        t_inv = t_inv + (l_ophis.warenwert + amt)
                        tot_amt = tot_amt + (l_ophis.warenwert + amt)


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if re.match(".*#.*",l_lieferant.plz):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount = l_ophis.warenwert * taxcode_list.taxamount
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = l_ophis.warenwert + str_list.tax_amount
                        t_inv = t_inv + (l_ophis.warenwert + str_list.tax_amount)
                        tot_amt = tot_amt + (l_ophis.warenwert + str_list.tax_amount)

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase   "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        else:

            l_ophis_obj_list = []
            for l_ophis, l_artikel, l_lieferant in db_session.query(L_ophis, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr > 0) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (L_ophis.lager_nr == store) &  (func.lower(L_ophis.docu_nr) == (from_doc).lower()) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr

                if lscheinnr != l_ophis.lscheinnr:
                    lscheinnr = l_ophis.lscheinnr
                    t_anz = 0
                    t_amt = 0
                    t_tax = 0
                    t_inv = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_ophis.anzahl
                t_amt = t_amt + l_ophis.warenwert
                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_ophis.warenwert * taxcode_list.taxamount
                        str_list.tax_amount = str_list.tax_amount + (l_ophis.warenwert * taxcode_list.taxamount)
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = str_list.tot_amt + (l_ophis.warenwert + amt)
                        t_inv = t_inv + (l_ophis.warenwert + amt)
                        tot_amt = tot_amt + (l_ophis.warenwert + amt)


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if re.match(".*#.*",l_lieferant.plz):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount = l_ophis.warenwert * taxcode_list.taxamount
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = l_ophis.warenwert + str_list.tax_amount
                        t_inv = t_inv + (l_ophis.warenwert + str_list.tax_amount)
                        tot_amt = tot_amt + (l_ophis.warenwert + str_list.tax_amount)

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase   "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty = tot_anz
        str_list.inc_qty = tot_anz
        str_list.amount = tot_amount
        str_list.tax_amount = tot_tax
        str_list.tot_amt = tot_amt

    def create_list22():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup


        nonlocal str_list, taxcode_list
        nonlocal str_list_list, taxcode_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        t_tax:decimal = 0
        t_inv:decimal = 0
        amt:decimal = 0
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0
        t_tax = 0
        t_inv = 0
        tot_tax = 0
        tot_amt = 0

        if store == 0:

            l_ophis_obj_list = []
            for l_ophis, l_artikel in db_session.query(L_ophis, L_artikel).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr == l_lieferant.lief_nr) &  (L_ophis.anzahl != 0) &  (L_ophis.op_art == 1) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)


                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_ophis.warenwert * taxcode_list.taxamount
                        str_list.tax_amount = str_list.tax_amount + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = str_list.tot_amt + (l_ophis.warenwert + amt)
                        tot_amt = tot_amt + (l_ophis.warenwert + amt)


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if re.match(".*#.*",l_lieferant.plz):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount = l_ophis.warenwert * taxcode_list.taxamount
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = l_ophis.warenwert + str_list.tax_amount
                        tot_amt = tot_amt + (l_ophis.warenwert + str_list.tax_amount)


        else:

            l_ophis_obj_list = []
            for l_ophis, l_artikel in db_session.query(L_ophis, L_artikel).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr == l_lieferant.lief_nr) &  (L_ophis.anzahl != 0) &  (L_ophis.lager_nr == store) &  (L_ophis.op_art == 1) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)


                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_ophis.warenwert * taxcode_list.taxamount
                        str_list.tax_amount = str_list.tax_amount + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = str_list.tot_amt + (l_ophis.warenwert + amt)
                        tot_amt = tot_amt + (l_ophis.warenwert + amt)


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if re.match(".*#.*",l_lieferant.plz):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount = l_ophis.warenwert * taxcode_list.taxamount
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = l_ophis.warenwert + str_list.tax_amount
                        tot_amt = tot_amt + (l_ophis.warenwert + str_list.tax_amount)


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty = tot_anz
        str_list.inc_qty = tot_anz
        str_list.amount = tot_amount
        str_list.tax_amount = tot_tax
        str_list.tot_amt = tot_amt

    def create_list1b():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup


        nonlocal str_list, taxcode_list
        nonlocal str_list_list, taxcode_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        t_tax:decimal = 0
        t_inv:decimal = 0
        lief_nr:int = 0
        lscheinnr:str = ""
        amt:decimal = 0
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0
        tot_tax = 0
        tot_amt = 0

        if store == 0:

            l_ophis_obj_list = []
            for l_ophis, l_artikel, l_untergrup in db_session.query(L_ophis, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr > 0) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                l_lieferant = db_session.query(L_lieferant).filter(
                        (L_lieferant.lief_nr == l_ophis.lief_nr)).first()

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.DESCRIPTION = lscheinnr
                    str_list.supplier = "T O T A L"
                    str_list.qty = t_anz
                    str_list.inc_qty = t_anz
                    str_list.amount = t_amt
                    str_list.tax_amount = t_tax
                    str_list.tot_amt = t_inv


                    lscheinnr = l_untergrup.bezeich
                    t_anz = 0
                    t_amt = 0
                    t_tax = 0
                    t_inv = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_ophis.anzahl
                t_amt = t_amt + l_ophis.warenwert
                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.lager_nr == l_ophis.lager_nr and str_list.artnr == l_ophis.artnr and str_list.artnr == l_ophis.artnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_ophis.warenwert * taxcode_list.taxamount
                        str_list.tax_amount = str_list.tax_amount + (l_ophis.warenwert * taxcode_list.taxamount)
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = str_list.tot_amt + (l_ophis.warenwert + amt)
                        t_inv = t_inv + (l_ophis.warenwert + amt)
                        tot_amt = tot_amt + (l_ophis.warenwert + amt)


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if re.match(".*#.*",l_lieferant.plz):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount = l_ophis.warenwert * taxcode_list.taxamount
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = l_ophis.warenwert + str_list.tax_amount
                        t_inv = t_inv + (l_ophis.warenwert + str_list.tax_amount)
                        tot_amt = tot_amt + (l_ophis.warenwert + str_list.tax_amount)

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase   "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        else:

            l_ophis_obj_list = []
            for l_ophis, l_artikel, l_untergrup in db_session.query(L_ophis, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr > 0) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (L_ophis.lager_nr == store) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                l_lieferant = db_session.query(L_lieferant).filter(
                        (L_lieferant.lief_nr == l_ophis.lief_nr)).first()

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.DESCRIPTION = lscheinnr
                    str_list.supplier = "T O T A L"
                    str_list.qty = t_anz
                    str_list.inc_qty = t_anz
                    str_list.amount = t_amt
                    str_list.tax_amount = t_tax
                    str_list.tot_amt = t_inv


                    lscheinnr = l_untergrup.bezeich
                    t_anz = 0
                    t_amt = 0
                    t_tax = 0
                    t_inv = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_ophis.anzahl
                t_amt = t_amt + l_ophis.warenwert
                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.lager_nr == l_ophis.lager_nr and str_list.artnr == l_ophis.artnr and str_list.artnr == l_ophis.artnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_ophis.warenwert * taxcode_list.taxamount
                        str_list.tax_amount = str_list.tax_amount + (l_ophis.warenwert * taxcode_list.taxamount)
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = str_list.tot_amt + (l_ophis.warenwert + amt)
                        t_inv = t_inv + (l_ophis.warenwert + amt)
                        tot_amt = tot_amt + (l_ophis.warenwert + amt)


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if re.match(".*#.*",l_lieferant.plz):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount = l_ophis.warenwert * taxcode_list.taxamount
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = l_ophis.warenwert + str_list.tax_amount
                        t_inv = t_inv + (l_ophis.warenwert + str_list.tax_amount)
                        tot_amt = tot_amt + (l_ophis.warenwert + str_list.tax_amount)

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase   "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.DESCRIPTION = lscheinnr
        str_list.supplier = "T O T A L"
        str_list.qty = t_anz
        str_list.inc_qty = t_anz
        str_list.amount = t_amt
        str_list.tax_amount = t_tax
        str_list.tot_amt = t_inv


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty = tot_anz
        str_list.inc_qty = tot_anz
        str_list.amount = tot_amount
        str_list.tax_amount = tot_tax
        str_list.tot_amt = tot_amt

    def create_list11b():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup


        nonlocal str_list, taxcode_list
        nonlocal str_list_list, taxcode_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        t_tax:decimal = 0
        t_inv:decimal = 0
        lscheinnr:str = ""
        amt:decimal = 0
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0
        tot_tax = 0
        tot_amt = 0

        if store == 0:

            l_ophis_obj_list = []
            for l_ophis, l_artikel, l_untergrup in db_session.query(L_ophis, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr > 0) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                l_lieferant = db_session.query(L_lieferant).filter(
                        (L_lieferant.lief_nr == l_ophis.lief_nr)).first()

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.DESCRIPTION = lscheinnr
                    str_list.supplier = "T O T A L"
                    str_list.qty = t_anz
                    str_list.inc_qty = t_anz
                    str_list.amount = t_amt
                    str_list.tax_amount = t_tax
                    str_list.tot_amt = t_inv


                    lscheinnr = l_untergrup.bezeich
                    t_anz = 0
                    t_amt = 0
                    t_tax = 0
                    t_inv = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_ophis.anzahl
                t_amt = t_amt + l_ophis.warenwert
                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_ophis.warenwert * taxcode_list.taxamount
                        str_list.tax_amount = str_list.tax_amount + (l_ophis.warenwert * taxcode_list.taxamount)
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = str_list.tot_amt + (l_ophis.warenwert + amt)
                        t_inv = t_inv + (l_ophis.warenwert + amt)
                        tot_amt = tot_amt + (l_ophis.warenwert + amt)


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if re.match(".*#.*",l_lieferant.plz):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount = l_ophis.warenwert * taxcode_list.taxamount
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = l_ophis.warenwert + str_list.tax_amount
                        t_inv = t_inv + (l_ophis.warenwert + str_list.tax_amount)
                        tot_amt = tot_amt + (l_ophis.warenwert + str_list.tax_amount)

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase   "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        else:

            l_ophis_obj_list = []
            for l_ophis, l_artikel, l_untergrup in db_session.query(L_ophis, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr > 0) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (L_ophis.lager_nr == store) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                l_lieferant = db_session.query(L_lieferant).filter(
                        (L_lieferant.lief_nr == l_ophis.lief_nr)).first()

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.DESCRIPTION = lscheinnr
                    str_list.supplier = "T O T A L"
                    str_list.qty = t_anz
                    str_list.inc_qty = t_anz
                    str_list.amount = t_amt
                    str_list.tax_amount = t_tax
                    str_list.tot_amt = t_inv


                    lscheinnr = l_untergrup.bezeich
                    t_anz = 0
                    t_amt = 0
                    t_tax = 0
                    t_inv = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_ophis.anzahl
                t_amt = t_amt + l_ophis.warenwert
                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_ophis.warenwert * taxcode_list.taxamount
                        str_list.tax_amount = str_list.tax_amount + (l_ophis.warenwert * taxcode_list.taxamount)
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = str_list.tot_amt + (l_ophis.warenwert + amt)
                        t_inv = t_inv + (l_ophis.warenwert + amt)
                        tot_amt = tot_amt + (l_ophis.warenwert + amt)


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if re.match(".*#.*",l_lieferant.plz):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount = l_ophis.warenwert * taxcode_list.taxamount
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = l_ophis.warenwert + str_list.tax_amount
                        t_inv = t_inv + (l_ophis.warenwert + str_list.tax_amount)
                        tot_amt = tot_amt + (l_ophis.warenwert + str_list.tax_amount)

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase   "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.DESCRIPTION = lscheinnr
        str_list.supplier = "T O T A L"
        str_list.qty = t_anz
        str_list.inc_qty = t_anz
        str_list.amount = t_amt


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty = tot_anz
        str_list.inc_qty = tot_anz
        str_list.amount = tot_amount
        str_list.tax_amount = tot_tax
        str_list.tot_amt = tot_amt

    def create_list1br():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup


        nonlocal str_list, taxcode_list
        nonlocal str_list_list, taxcode_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        t_tax:decimal = 0
        t_inv:decimal = 0
        lief_nr:int = 0
        lscheinnr:str = ""
        amt:decimal = 0
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0
        tot_tax = 0
        tot_amt = 0

        if store == 0:

            l_ophis_obj_list = []
            for l_ophis, l_artikel, l_untergrup in db_session.query(L_ophis, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr > 0) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (func.lower(L_ophis.docu_nr) == (from_doc).lower()) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                l_lieferant = db_session.query(L_lieferant).filter(
                        (L_lieferant.lief_nr == l_ophis.lief_nr)).first()

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.DESCRIPTION = lscheinnr
                    str_list.supplier = "T O T A L"
                    str_list.qty = t_anz
                    str_list.inc_qty = t_anz
                    str_list.amount = t_amt
                    str_list.tax_amount = t_tax
                    str_list.tot_amt = t_inv


                    lscheinnr = l_untergrup.bezeich
                    t_anz = 0
                    t_amt = 0
                    t_tax = 0
                    t_inv = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_ophis.anzahl
                t_amt = t_amt + l_ophis.warenwert
                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.lager_nr == l_ophis.lager_nr and str_list.artnr == l_ophis.artnr and str_list.artnr == l_ophis.artnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_ophis.warenwert * taxcode_list.taxamount
                        str_list.tax_amount = str_list.tax_amount + (l_ophis.warenwert * taxcode_list.taxamount)
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = str_list.tot_amt + (l_ophis.warenwert + amt)
                        t_inv = t_inv + (l_ophis.warenwert + amt)
                        tot_amt = tot_amt + (l_ophis.warenwert + amt)


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if re.match(".*#.*",l_lieferant.plz):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount = l_ophis.warenwert * taxcode_list.taxamount
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = l_ophis.warenwert + str_list.tax_amount
                        t_inv = t_inv + (l_ophis.warenwert + str_list.tax_amount)
                        tot_amt = tot_amt + (l_ophis.warenwert + str_list.tax_amount)

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase   "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        else:

            l_ophis_obj_list = []
            for l_ophis, l_artikel, l_untergrup in db_session.query(L_ophis, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr > 0) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (L_ophis.lager_nr == store) &  (func.lower(L_ophis.docu_nr) == (from_doc).lower()) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                l_lieferant = db_session.query(L_lieferant).filter(
                        (L_lieferant.lief_nr == l_ophis.lief_nr)).first()

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.DESCRIPTION = lscheinnr
                    str_list.supplier = "T O T A L"
                    str_list.qty = t_anz
                    str_list.inc_qty = t_anz
                    str_list.amount = t_amt
                    str_list.tax_amount = t_tax
                    str_list.tot_amt = t_inv


                    lscheinnr = l_untergrup.bezeich
                    t_anz = 0
                    t_amt = 0
                    t_tax = 0
                    t_inv = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_ophis.anzahl
                t_amt = t_amt + l_ophis.warenwert
                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.lager_nr == l_ophis.lager_nr and str_list.artnr == l_ophis.artnr and str_list.artnr == l_ophis.artnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_ophis.warenwert * taxcode_list.taxamount
                        str_list.tax_amount = str_list.tax_amount + (l_ophis.warenwert * taxcode_list.taxamount)
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = str_list.tot_amt + (l_ophis.warenwert + amt)
                        t_inv = t_inv + (l_ophis.warenwert + amt)
                        tot_amt = tot_amt + (l_ophis.warenwert + amt)


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if re.match(".*#.*",l_lieferant.plz):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount = l_ophis.warenwert * taxcode_list.taxamount
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = l_ophis.warenwert + str_list.tax_amount
                        t_inv = t_inv + (l_ophis.warenwert + str_list.tax_amount)
                        tot_amt = tot_amt + (l_ophis.warenwert + str_list.tax_amount)

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase   "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.DESCRIPTION = lscheinnr
        str_list.supplier = "T O T A L"
        str_list.qty = t_anz
        str_list.inc_qty = t_anz
        str_list.amount = t_amt
        str_list.tax_amount = t_tax
        str_list.tot_amt = t_inv


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty = tot_anz
        str_list.inc_qty = tot_anz
        str_list.amount = tot_amount
        str_list.tax_amount = tot_tax
        str_list.tot_amt = tot_amt

    def create_list11br():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup


        nonlocal str_list, taxcode_list
        nonlocal str_list_list, taxcode_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        t_tax:decimal = 0
        t_inv:decimal = 0
        lscheinnr:str = ""
        amt:decimal = 0
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0
        tot_tax = 0
        tot_amt = 0

        if store == 0:

            l_ophis_obj_list = []
            for l_ophis, l_artikel, l_untergrup in db_session.query(L_ophis, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr > 0) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (func.lower(L_ophis.docu_nr) == (from_doc).lower()) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                l_lieferant = db_session.query(L_lieferant).filter(
                        (L_lieferant.lief_nr == l_ophis.lief_nr)).first()

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.DESCRIPTION = lscheinnr
                    str_list.supplier = "T O T A L"
                    str_list.qty = t_anz
                    str_list.inc_qty = t_anz
                    str_list.amount = t_amt
                    str_list.tax_amount = t_tax
                    str_list.tot_amt = t_inv


                    lscheinnr = l_untergrup.bezeich
                    t_anz = 0
                    t_amt = 0
                    t_tax = 0
                    t_inv = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_ophis.anzahl
                t_amt = t_amt + l_ophis.warenwert
                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_ophis.warenwert * taxcode_list.taxamount
                        str_list.tax_amount = str_list.tax_amount + (l_ophis.warenwert * taxcode_list.taxamount)
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = str_list.tot_amt + (l_ophis.warenwert + amt)
                        t_inv = t_inv + (l_ophis.warenwert + amt)
                        tot_amt = tot_amt + (l_ophis.warenwert + amt)


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if re.match(".*#.*",l_lieferant.plz):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount = l_ophis.warenwert * taxcode_list.taxamount
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = l_ophis.warenwert + str_list.tax_amount
                        t_inv = t_inv + (l_ophis.warenwert + str_list.tax_amount)
                        tot_amt = tot_amt + (l_ophis.warenwert + str_list.tax_amount)

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase   "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        else:

            l_ophis_obj_list = []
            for l_ophis, l_artikel, l_untergrup in db_session.query(L_ophis, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr > 0) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (L_ophis.lager_nr == store) &  (func.lower(L_ophis.docu_nr) == (from_doc).lower()) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                l_lieferant = db_session.query(L_lieferant).filter(
                        (L_lieferant.lief_nr == l_ophis.lief_nr)).first()

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.DESCRIPTION = lscheinnr
                    str_list.supplier = "T O T A L"
                    str_list.qty = t_anz
                    str_list.inc_qty = t_anz
                    str_list.amount = t_amt
                    str_list.tax_amount = t_tax
                    str_list.tot_amt = t_inv


                    lscheinnr = l_untergrup.bezeich
                    t_anz = 0
                    t_amt = 0
                    t_tax = 0
                    t_inv = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_ophis.anzahl
                t_amt = t_amt + l_ophis.warenwert
                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_ophis.warenwert * taxcode_list.taxamount
                        str_list.tax_amount = str_list.tax_amount + (l_ophis.warenwert * taxcode_list.taxamount)
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = str_list.tot_amt + (l_ophis.warenwert + amt)
                        t_inv = t_inv + (l_ophis.warenwert + amt)
                        tot_amt = tot_amt + (l_ophis.warenwert + amt)


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if re.match(".*#.*",l_lieferant.plz):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount = l_ophis.warenwert * taxcode_list.taxamount
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = l_ophis.warenwert + str_list.tax_amount
                        t_inv = t_inv + (l_ophis.warenwert + str_list.tax_amount)
                        tot_amt = tot_amt + (l_ophis.warenwert + str_list.tax_amount)

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase   "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.DESCRIPTION = lscheinnr
        str_list.supplier = "T O T A L"
        str_list.qty = t_anz
        str_list.inc_qty = t_anz
        str_list.amount = t_amt
        str_list.tax_amount = t_tax
        str_list.tot_amt = t_inv


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty = tot_anz
        str_list.inc_qty = tot_anz
        str_list.amount = tot_amount
        str_list.tax_amount = tot_tax
        str_list.tot_amt = tot_amt

    def create_list1as():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup


        nonlocal str_list, taxcode_list
        nonlocal str_list_list, taxcode_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        t_tax:decimal = 0
        t_inv:decimal = 0
        lief_nr:int = 0
        lscheinnr:str = ""
        amt:decimal = 0
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0
        tot_tax = 0
        tot_amt = 0

        if store == 0:

            l_ophis_obj_list = []
            for l_ophis, l_artikel, l_lieferant in db_session.query(L_ophis, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr == l_lieferant.lief_nr) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr

                if lscheinnr != l_ophis.lscheinnr:
                    lscheinnr = l_ophis.lscheinnr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.supplier = "T O T A L"
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

                t_anz = t_anz + l_ophis.anzahl
                t_amt = t_amt + l_ophis.warenwert
                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.lager_nr == l_ophis.lager_nr and str_list.artnr == l_ophis.artnr and str_list.artnr == l_ophis.artnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_ophis.warenwert * taxcode_list.taxamount
                        str_list.tax_amount = str_list.tax_amount + (l_ophis.warenwert * taxcode_list.taxamount)
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = str_list.tot_amt + (l_ophis.warenwert + amt)
                        t_inv = t_inv + (l_ophis.warenwert + amt)
                        tot_amt = tot_amt + (l_ophis.warenwert + amt)


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if re.match(".*#.*",l_lieferant.plz):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount = l_ophis.warenwert * taxcode_list.taxamount
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = l_ophis.warenwert + str_list.tax_amount
                        t_inv = t_inv + (l_ophis.warenwert + str_list.tax_amount)
                        tot_amt = tot_amt + (l_ophis.warenwert + str_list.tax_amount)

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase   "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        else:

            l_ophis_obj_list = []
            for l_ophis, l_artikel, l_lieferant in db_session.query(L_ophis, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr == l_lieferant.lief_nr) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (L_ophis.lager_nr == store) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr

                if lscheinnr != l_ophis.lscheinnr:
                    lscheinnr = l_ophis.lscheinnr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.supplier = "T O T A L"
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

                t_anz = t_anz + l_ophis.anzahl
                t_amt = t_amt + l_ophis.warenwert
                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.lager_nr == l_ophis.lager_nr and str_list.artnr == l_ophis.artnr and str_list.artnr == l_ophis.artnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_ophis.warenwert * taxcode_list.taxamount
                        str_list.tax_amount = str_list.tax_amount + (l_ophis.warenwert * taxcode_list.taxamount)
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = str_list.tot_amt + (l_ophis.warenwert + amt)
                        t_inv = t_inv + (l_ophis.warenwert + amt)
                        tot_amt = tot_amt + (l_ophis.warenwert + amt)


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if re.match(".*#.*",l_lieferant.plz):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount = l_ophis.warenwert * taxcode_list.taxamount
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = l_ophis.warenwert + str_list.tax_amount
                        t_inv = t_inv + (l_ophis.warenwert + str_list.tax_amount)
                        tot_amt = tot_amt + (l_ophis.warenwert + str_list.tax_amount)

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase   "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "T O T A L"
        str_list.qty = t_anz
        str_list.inc_qty = t_anz
        str_list.amount = t_amt
        str_list.tax_amount = t_tax
        str_list.tot_amt = t_inv


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty = tot_anz
        str_list.inc_qty = tot_anz
        str_list.amount = tot_amount
        str_list.tax_amount = tot_tax
        str_list.tot_amt = tot_amt

    def create_list11as():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup


        nonlocal str_list, taxcode_list
        nonlocal str_list_list, taxcode_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        t_tax:decimal = 0
        t_inv:decimal = 0
        lscheinnr:str = ""
        amt:decimal = 0
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0
        tot_tax = 0
        tot_amt = 0

        if store == 0:

            l_ophis_obj_list = []
            for l_ophis, l_artikel, l_lieferant in db_session.query(L_ophis, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr == l_lieferant.lief_nr) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr

                if lscheinnr != l_ophis.lscheinnr:
                    lscheinnr = l_ophis.lscheinnr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.supplier = "T O T A L"
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

                t_anz = t_anz + l_ophis.anzahl
                t_amt = t_amt + l_ophis.warenwert
                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_ophis.warenwert * taxcode_list.taxamount
                        str_list.tax_amount = str_list.tax_amount + (l_ophis.warenwert * taxcode_list.taxamount)
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = str_list.tot_amt + (l_ophis.warenwert + amt)
                        t_inv = t_inv + (l_ophis.warenwert + amt)
                        tot_amt = tot_amt + (l_ophis.warenwert + amt)


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if re.match(".*#.*",l_lieferant.plz):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount = l_ophis.warenwert * taxcode_list.taxamount
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = l_ophis.warenwert + str_list.tax_amount
                        t_inv = t_inv + (l_ophis.warenwert + str_list.tax_amount)
                        tot_amt = tot_amt + (l_ophis.warenwert + str_list.tax_amount)

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase   "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        else:

            l_ophis_obj_list = []
            for l_ophis, l_artikel, l_lieferant in db_session.query(L_ophis, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr == l_lieferant.lief_nr) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (L_ophis.lager_nr == store) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr

                if lscheinnr != l_ophis.lscheinnr:
                    lscheinnr = l_ophis.lscheinnr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.supplier = "T O T A L"
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

                t_anz = t_anz + l_ophis.anzahl
                t_amt = t_amt + l_ophis.warenwert
                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_ophis.warenwert * taxcode_list.taxamount
                        str_list.tax_amount = str_list.tax_amount + (l_ophis.warenwert * taxcode_list.taxamount)
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = str_list.tot_amt + (l_ophis.warenwert + amt)
                        t_inv = t_inv + (l_ophis.warenwert + amt)
                        tot_amt = tot_amt + (l_ophis.warenwert + amt)


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if re.match(".*#.*",l_lieferant.plz):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount = l_ophis.warenwert * taxcode_list.taxamount
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = l_ophis.warenwert + str_list.tax_amount
                        t_inv = t_inv + (l_ophis.warenwert + str_list.tax_amount)
                        tot_amt = tot_amt + (l_ophis.warenwert + str_list.tax_amount)

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase   "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "T O T A L"
        str_list.qty = t_anz
        str_list.inc_qty = t_anz
        str_list.amount = t_amt
        str_list.tax_amount = t_tax
        str_list.tot_amt = t_inv


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty = tot_anz
        str_list.inc_qty = tot_anz
        str_list.amount = tot_amount
        str_list.tax_amount = tot_tax
        str_list.tot_amt = tot_amt

    def create_list1bs():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup


        nonlocal str_list, taxcode_list
        nonlocal str_list_list, taxcode_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        t_tax:decimal = 0
        t_inv:decimal = 0
        lief_nr:int = 0
        lscheinnr:str = ""
        amt:decimal = 0
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0
        tot_tax = 0
        tot_amt = 0

        if store == 0:

            l_ophis_obj_list = []
            for l_ophis, l_artikel, l_untergrup in db_session.query(L_ophis, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr == l_lieferant.lief_nr) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                l_lieferant = db_session.query(L_lieferant).filter(
                        (L_lieferant.lief_nr == l_ophis.lief_nr)).first()

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.DESCRIPTION = lscheinnr
                    str_list.supplier = "T O T A L"
                    str_list.qty = t_anz
                    str_list.inc_qty = t_anz
                    str_list.amount = t_amt
                    str_list.tax_amount = t_tax
                    str_list.tot_amt = t_inv


                    lscheinnr = l_untergrup.bezeich
                    t_anz = 0
                    t_amt = 0
                    t_tax = 0
                    t_inv = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_ophis.anzahl
                t_amt = t_amt + l_ophis.warenwert
                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.lager_nr == l_ophis.lager_nr and str_list.artnr == l_ophis.artnr and str_list.artnr == l_ophis.artnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_ophis.warenwert * taxcode_list.taxamount
                        str_list.tax_amount = str_list.tax_amount + (l_ophis.warenwert * taxcode_list.taxamount)
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = str_list.tot_amt + (l_ophis.warenwert + amt)
                        t_inv = t_inv + (l_ophis.warenwert + amt)
                        tot_amt = tot_amt + (l_ophis.warenwert + amt)


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if re.match(".*#.*",l_lieferant.plz):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount = l_ophis.warenwert * taxcode_list.taxamount
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = l_ophis.warenwert + str_list.tax_amount
                        t_inv = t_inv + (l_ophis.warenwert + str_list.tax_amount)
                        tot_amt = tot_amt + (l_ophis.warenwert + str_list.tax_amount)

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase   "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        else:

            l_ophis_obj_list = []
            for l_ophis, l_artikel, l_untergrup in db_session.query(L_ophis, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr == l_lieferant.lief_nr) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (L_ophis.lager_nr == store) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                l_lieferant = db_session.query(L_lieferant).filter(
                        (L_lieferant.lief_nr == l_ophis.lief_nr)).first()

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.DESCRIPTION = lscheinnr
                    str_list.supplier = "T O T A L"
                    str_list.qty = t_anz
                    str_list.inc_qty = t_anz
                    str_list.amount = t_amt
                    str_list.tax_amount = t_tax
                    str_list.tot_amt = t_inv


                    lscheinnr = l_untergrup.bezeich
                    t_anz = 0
                    t_amt = 0
                    t_tax = 0
                    t_inv = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_ophis.anzahl
                t_amt = t_amt + l_ophis.warenwert
                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.lager_nr == l_ophis.lager_nr and str_list.artnr == l_ophis.artnr and str_list.artnr == l_ophis.artnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_ophis.warenwert * taxcode_list.taxamount
                        str_list.tax_amount = str_list.tax_amount + (l_ophis.warenwert * taxcode_list.taxamount)
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = str_list.tot_amt + (l_ophis.warenwert + amt)
                        t_inv = t_inv + (l_ophis.warenwert + amt)
                        tot_amt = tot_amt + (l_ophis.warenwert + amt)


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if re.match(".*#.*",l_lieferant.plz):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount = l_ophis.warenwert * taxcode_list.taxamount
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = l_ophis.warenwert + str_list.tax_amount
                        t_inv = t_inv + (l_ophis.warenwert + str_list.tax_amount)
                        tot_amt = tot_amt + (l_ophis.warenwert + str_list.tax_amount)

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase   "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.DESCRIPTION = lscheinnr
        str_list.supplier = "T O T A L"
        str_list.qty = t_anz
        str_list.inc_qty = t_anz
        str_list.amount = t_amt
        str_list.tax_amount = t_tax
        str_list.tot_amt = t_inv


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty = tot_anz
        str_list.inc_qty = tot_anz
        str_list.amount = tot_amount
        str_list.tax_amount = tot_tax
        str_list.tot_amt = tot_amt

    def create_list11bs():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup


        nonlocal str_list, taxcode_list
        nonlocal str_list_list, taxcode_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        t_tax:decimal = 0
        t_inv:decimal = 0
        lscheinnr:str = ""
        amt:decimal = 0
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0
        tot_tax = 0
        tot_amt = 0

        if store == 0:

            l_ophis_obj_list = []
            for l_ophis, l_artikel, l_untergrup in db_session.query(L_ophis, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr == l_lieferant.lief_nr) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                l_lieferant = db_session.query(L_lieferant).filter(
                        (L_lieferant.lief_nr == l_ophis.lief_nr)).first()

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.DESCRIPTION = lscheinnr
                    str_list.supplier = "T O T A L"
                    str_list.qty = t_anz
                    str_list.inc_qty = t_anz
                    str_list.amount = t_amt
                    str_list.tax_amount = t_tax
                    str_list.tot_amt = t_inv


                    lscheinnr = l_untergrup.bezeich
                    t_anz = 0
                    t_amt = 0
                    t_tax = 0
                    t_inv = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_ophis.anzahl
                t_amt = t_amt + l_ophis.warenwert
                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_ophis.warenwert * taxcode_list.taxamount
                        str_list.tax_amount = str_list.tax_amount + (l_ophis.warenwert * taxcode_list.taxamount)
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = str_list.tot_amt + (l_ophis.warenwert + amt)
                        t_inv = t_inv + (l_ophis.warenwert + amt)
                        tot_amt = tot_amt + (l_ophis.warenwert + amt)


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if re.match(".*#.*",l_lieferant.plz):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount = l_ophis.warenwert * taxcode_list.taxamount
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = l_ophis.warenwert + str_list.tax_amount
                        t_inv = t_inv + (l_ophis.warenwert + str_list.tax_amount)
                        tot_amt = tot_amt + (l_ophis.warenwert + str_list.tax_amount)

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase   "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        else:

            l_ophis_obj_list = []
            for l_ophis, l_artikel, l_untergrup in db_session.query(L_ophis, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) &  (L_artikel.endkum >= from_grp) &  (L_artikel.endkum <= to_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.lief_nr == l_lieferant.lief_nr) &  (L_ophis.op_art == 1) &  (L_ophis.anzahl != 0) &  (L_ophis.lager_nr == store) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                if l_ophis._recid in l_ophis_obj_list:
                    continue
                else:
                    l_ophis_obj_list.append(l_ophis._recid)

                l_lieferant = db_session.query(L_lieferant).filter(
                        (L_lieferant.lief_nr == l_ophis.lief_nr)).first()

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.DESCRIPTION = lscheinnr
                    str_list.supplier = "T O T A L"
                    str_list.qty = t_anz
                    str_list.inc_qty = t_anz
                    str_list.amount = t_amt
                    str_list.tax_amount = t_tax
                    str_list.tot_amt = t_inv


                    lscheinnr = l_untergrup.bezeich
                    t_anz = 0
                    t_amt = 0
                    t_tax = 0
                    t_inv = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_ophis.anzahl
                t_amt = t_amt + l_ophis.warenwert
                tot_anz = tot_anz + l_ophis.anzahl
                tot_amount = tot_amount + l_ophis.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_ophis.anzahl
                    str_list.warenwert = str_list.warenwert + l_ophis.warenwert
                    str_list.inc_qty = str_list.qty
                    str_list.amount = str_list.warenwert

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt = l_ophis.warenwert * taxcode_list.taxamount
                        str_list.tax_amount = str_list.tax_amount + (l_ophis.warenwert * taxcode_list.taxamount)
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = str_list.tot_amt + (l_ophis.warenwert + amt)
                        t_inv = t_inv + (l_ophis.warenwert + amt)
                        tot_amt = tot_amt + (l_ophis.warenwert + amt)


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty = l_ophis.anzahl
                    str_list.epreis = l_ophis.einzelpreis
                    str_list.warenwert = l_ophis.warenwert
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.DESCRIPTION = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensort
                    str_list.price = l_ophis.einzelpreis
                    str_list.inc_qty = l_ophis.anzahl
                    str_list.amount = l_ophis.warenwert
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if re.match(".*#.*",l_lieferant.plz):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list :taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount = l_ophis.warenwert * taxcode_list.taxamount
                        t_tax = t_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        tot_tax = tot_tax + (l_ophis.warenwert * taxcode_list.taxamount)
                        str_list.tot_amt = l_ophis.warenwert + str_list.tax_amount
                        t_inv = t_inv + (l_ophis.warenwert + str_list.tax_amount)
                        tot_amt = tot_amt + (l_ophis.warenwert + str_list.tax_amount)

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase   "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.DESCRIPTION = lscheinnr
        str_list.supplier = "T O T A L"
        str_list.qty = t_anz
        str_list.inc_qty = t_anz
        str_list.amount = t_amt
        str_list.tax_amount = t_tax
        str_list.tot_amt = t_inv


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty = tot_anz
        str_list.inc_qty = tot_anz
        str_list.amount = tot_amount
        str_list.tax_amount = tot_tax
        str_list.tot_amt = tot_amt


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    if from_supp != "":

        l_lieferant = db_session.query(L_lieferant).filter(
                (func.lower(L_lieferant.firma) == (from_supp).lower())).first()

        if not l_lieferant:
            err_code = 1

            return generate_output()
        else:
            supp_nr = l_lieferant.lief_nr

    if from_doc != "":

        l_ophis = db_session.query(L_ophis).filter(
                (func.lower(L_ophis.docu_nr) == (from_doc).lower())).first()

        if not l_ophis:
            err_code = 4

            return generate_output()

    if sorttype == 1:

        if not all_supp and from_supp == "":
            err_code = 2

            return generate_output()

        if all_supp:
            create_list11()
        else:

            if supp_nr != 0:
                create_list22()

    elif sorttype == 2:

        if not all_doc and from_doc == "":
            err_code = 3

            return generate_output()

        if all_doc:

            if from_supp != "" and supp_nr != 0:

                if from_grp == 0:
                    create_list1as()
                else:
                    create_list11as()
            else:

                if from_grp == 0:
                    create_list1a()
                else:
                    create_list11a()
        else:

            if from_grp == 0:
                create_list1ar()
            else:
                create_list11ar()

    elif sorttype == 3:

        if not all_doc and from_doc == "":

            return generate_output()

        if all_doc:

            if from_supp != "" and supp_nr != 0:

                if from_grp == 0:
                    create_list1bs()
                else:
                    create_list11bs()
            else:

                if from_grp == 0:
                    create_list1b()
                else:
                    create_list11b()
        else:

            if from_grp == 0:
                create_list1br()
            else:
                create_list11br()

    return generate_output()