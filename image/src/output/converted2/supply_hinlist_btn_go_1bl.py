#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, L_lieferant, L_ophis, L_artikel, L_untergrup

taxcode_list_list, Taxcode_list = create_model("Taxcode_list", {"taxcode":string, "taxamount":Decimal})

def supply_hinlist_btn_go_1bl(pvilanguage:int, from_supp:string, from_doc:string, sorttype:int, from_grp:int, to_grp:int, store:int, all_supp:bool, all_doc:bool, from_date:date, to_date:date, taxcode_list_list:[Taxcode_list]):

    prepare_cache ([Htparam, L_lieferant, L_ophis, L_artikel, L_untergrup])

    err_code = 0
    str_list_list = []
    i:int = 0
    supp_nr:int = 0
    tot_anz:Decimal = to_decimal("0.0")
    tot_amount:Decimal = to_decimal("0.0")
    long_digit:bool = False
    tot_tax:Decimal = to_decimal("0.0")
    tot_amt:Decimal = to_decimal("0.0")
    loopi:int = 0
    lvcarea:string = "supply-hinlist"
    htparam = l_lieferant = l_ophis = l_artikel = l_untergrup = None

    str_list = taxcode_list = None

    str_list_list, Str_list = create_model("Str_list", {"artnr":int, "lager_nr":int, "docu_nr":string, "lscheinnr":string, "qty":Decimal, "epreis":Decimal, "warenwert":Decimal, "datum":date, "st":int, "supplier":string, "article":int, "description":string, "d_unit":string, "price":Decimal, "inc_qty":Decimal, "amount":Decimal, "docu_no":string, "deliv_no":string, "gstid":string, "tax_code":string, "tax_amount":Decimal, "tot_amt":Decimal, "lief_nr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date


        nonlocal str_list, taxcode_list
        nonlocal str_list_list

        return {"err_code": err_code, "str-list": str_list_list}

    def create_list1a():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date


        nonlocal str_list, taxcode_list
        nonlocal str_list_list

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")

        if store == 0:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.firma, l_lieferant.lief_nr, l_lieferant.plz, l_lieferant._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.firma, L_lieferant.lief_nr, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.lscheinnr, L_ophis.artnr, L_ophis.datum).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr

                if lscheinnr != l_ophis.lscheinnr:
                    lscheinnr = l_ophis.lscheinnr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.supplier = "T O T A L"
                    str_list.qty =  to_decimal(t_anz)
                    str_list.inc_qty =  to_decimal(t_anz)
                    str_list.amount =  to_decimal(t_amt)


                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.lager_nr == l_ophis.lager_nr and str_list.artnr == l_ophis.artnr and str_list.artnr == l_ophis.artnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)
                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.lief_nr = l_ophis.lief_nr

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr


        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.firma, l_lieferant.lief_nr, l_lieferant.plz, l_lieferant._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.firma, L_lieferant.lief_nr, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (L_ophis.lager_nr == store) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.lscheinnr, L_ophis.artnr, L_ophis.datum).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr

                if lscheinnr != l_ophis.lscheinnr:
                    lscheinnr = l_ophis.lscheinnr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.supplier = "T O T A L"
                    str_list.qty =  to_decimal(t_anz)
                    str_list.inc_qty =  to_decimal(t_anz)
                    str_list.amount =  to_decimal(t_amt)


                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.lager_nr == l_ophis.lager_nr and str_list.artnr == l_ophis.artnr and str_list.artnr == l_ophis.artnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)
                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.lief_nr = l_ophis.lief_nr

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "T O T A L"
        str_list.qty =  to_decimal(t_anz)
        str_list.inc_qty =  to_decimal(t_anz)
        str_list.amount =  to_decimal(t_amt)


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty =  to_decimal(tot_anz)
        str_list.inc_qty =  to_decimal(tot_anz)
        str_list.amount =  to_decimal(tot_amount)


    def create_list1ar():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date


        nonlocal str_list, taxcode_list
        nonlocal str_list_list

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")

        if store == 0:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.firma, l_lieferant.lief_nr, l_lieferant.plz, l_lieferant._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.firma, L_lieferant.lief_nr, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (L_ophis.docu_nr == (from_doc).lower()) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.lscheinnr, L_ophis.artnr, L_ophis.datum).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr

                if lscheinnr != l_ophis.lscheinnr:
                    lscheinnr = l_ophis.lscheinnr
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.lager_nr == l_ophis.lager_nr and str_list.artnr == l_ophis.artnr and str_list.artnr == l_ophis.artnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)
                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.lief_nr = l_ophis.lief_nr

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.firma, l_lieferant.lief_nr, l_lieferant.plz, l_lieferant._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.firma, L_lieferant.lief_nr, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (L_ophis.lager_nr == store) & (L_ophis.docu_nr == (from_doc).lower()) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.lscheinnr, L_ophis.artnr, L_ophis.datum).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr

                if lscheinnr != l_ophis.lscheinnr:
                    lscheinnr = l_ophis.lscheinnr
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.lager_nr == l_ophis.lager_nr and str_list.artnr == l_ophis.artnr and str_list.artnr == l_ophis.artnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)
                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.lief_nr = l_ophis.lief_nr

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty =  to_decimal(tot_anz)
        str_list.inc_qty =  to_decimal(tot_anz)
        str_list.amount =  to_decimal(tot_amount)


    def create_list11():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date


        nonlocal str_list, taxcode_list
        nonlocal str_list_list

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        amt:Decimal = to_decimal("0.0")
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.firma, l_lieferant.lief_nr, l_lieferant.plz, l_lieferant._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.firma, L_lieferant.lief_nr, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_lieferant.firma, L_ophis.datum, L_ophis.artnr).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                if lief_nr == 0:
                    lief_nr = l_lieferant.lief_nr

                if lief_nr != l_lieferant.lief_nr:
                    lief_nr = l_lieferant.lief_nr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.supplier = "T O T A L"
                    str_list.qty =  to_decimal(t_anz)
                    str_list.inc_qty =  to_decimal(t_anz)
                    str_list.amount =  to_decimal(t_amt)
                    str_list.tax_amount =  to_decimal(t_tax)
                    str_list.tot_amt =  to_decimal(t_inv)


                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    t_tax =  to_decimal("0")
                    t_inv =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if matches(l_lieferant.plz,r"*#*"):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(l_ophis.warenwert) + to_decimal(str_list.tax_amount)
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr


        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.firma, l_lieferant.lief_nr, l_lieferant.plz, l_lieferant._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.firma, L_lieferant.lief_nr, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (L_ophis.lager_nr == store) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.datum, L_lieferant.firma, L_ophis.artnr).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                if lief_nr == 0:
                    lief_nr = l_lieferant.lief_nr

                if lief_nr != l_lieferant.lief_nr:
                    lief_nr = l_lieferant.lief_nr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.supplier = "T O T A L"
                    str_list.qty =  to_decimal(t_anz)
                    str_list.inc_qty =  to_decimal(t_anz)
                    str_list.amount =  to_decimal(t_amt)
                    str_list.tax_amount =  to_decimal(t_tax)
                    str_list.tot_amt =  to_decimal(t_inv)


                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    t_tax =  to_decimal("0")
                    t_inv =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if matches(l_lieferant.plz,r"*#*"):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(l_ophis.warenwert) + to_decimal(str_list.tax_amount)
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "T O T A L"
        str_list.qty =  to_decimal(t_anz)
        str_list.inc_qty =  to_decimal(t_anz)
        str_list.amount =  to_decimal(t_amt)
        str_list.tax_amount =  to_decimal(t_tax)
        str_list.tot_amt =  to_decimal(t_inv)


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty =  to_decimal(tot_anz)
        str_list.inc_qty =  to_decimal(tot_anz)
        str_list.amount =  to_decimal(tot_amount)
        str_list.tax_amount =  to_decimal(tot_tax)
        str_list.tot_amt =  to_decimal(tot_amt)


    def create_list11a():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date


        nonlocal str_list, taxcode_list
        nonlocal str_list_list

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        lscheinnr:string = ""
        amt:Decimal = to_decimal("0.0")
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.firma, l_lieferant.lief_nr, l_lieferant.plz, l_lieferant._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.firma, L_lieferant.lief_nr, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.lscheinnr, L_ophis.artnr, L_ophis.datum).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr

                if lscheinnr != l_ophis.lscheinnr:
                    lscheinnr = l_ophis.lscheinnr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.supplier = "T O T A L"
                    str_list.qty =  to_decimal(t_anz)
                    str_list.inc_qty =  to_decimal(t_anz)
                    str_list.amount =  to_decimal(t_amt)
                    str_list.tax_amount =  to_decimal(t_tax)
                    str_list.tot_amt =  to_decimal(t_inv)


                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    t_tax =  to_decimal("0")
                    t_inv =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if matches(l_lieferant.plz,r"*#*"):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(l_ophis.warenwert) + to_decimal(str_list.tax_amount)
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.firma, l_lieferant.lief_nr, l_lieferant.plz, l_lieferant._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.firma, L_lieferant.lief_nr, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (L_ophis.lager_nr == store) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.lscheinnr, L_ophis.artnr, L_ophis.datum).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                pass

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr

                if lscheinnr != l_ophis.lscheinnr:
                    lscheinnr = l_ophis.lscheinnr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.supplier = "T O T A L"
                    str_list.qty =  to_decimal(t_anz)
                    str_list.inc_qty =  to_decimal(t_anz)
                    str_list.amount =  to_decimal(t_amt)
                    str_list.tax_amount =  to_decimal(t_tax)
                    str_list.tot_amt =  to_decimal(t_inv)


                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    t_tax =  to_decimal("0")
                    t_inv =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if matches(l_lieferant.plz,r"*#*"):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(l_ophis.warenwert) + to_decimal(str_list.tax_amount)
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "T O T A L"
        str_list.qty =  to_decimal(t_anz)
        str_list.inc_qty =  to_decimal(t_anz)
        str_list.amount =  to_decimal(t_amt)
        str_list.tax_amount =  to_decimal(t_tax)
        str_list.tot_amt =  to_decimal(t_inv)


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty =  to_decimal(tot_anz)
        str_list.inc_qty =  to_decimal(tot_anz)
        str_list.amount =  to_decimal(tot_amount)
        str_list.tax_amount =  to_decimal(tot_tax)
        str_list.tot_amt =  to_decimal(tot_amt)


    def create_list11ar():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date


        nonlocal str_list, taxcode_list
        nonlocal str_list_list

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        lscheinnr:string = ""
        amt:Decimal = to_decimal("0.0")
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.firma, l_lieferant.lief_nr, l_lieferant.plz, l_lieferant._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.firma, L_lieferant.lief_nr, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (L_ophis.docu_nr == (from_doc).lower()) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.lscheinnr, L_ophis.artnr, L_ophis.datum).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr

                if lscheinnr != l_ophis.lscheinnr:
                    lscheinnr = l_ophis.lscheinnr
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    t_tax =  to_decimal("0")
                    t_inv =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if matches(l_lieferant.plz,r"*#*"):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(l_ophis.warenwert) + to_decimal(str_list.tax_amount)
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.firma, l_lieferant.lief_nr, l_lieferant.plz, l_lieferant._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.firma, L_lieferant.lief_nr, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (L_ophis.lager_nr == store) & (L_ophis.docu_nr == (from_doc).lower()) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.lscheinnr, L_ophis.artnr, L_ophis.datum).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr

                if lscheinnr != l_ophis.lscheinnr:
                    lscheinnr = l_ophis.lscheinnr
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    t_tax =  to_decimal("0")
                    t_inv =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if matches(l_lieferant.plz,r"*#*"):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(l_ophis.warenwert) + to_decimal(str_list.tax_amount)
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty =  to_decimal(tot_anz)
        str_list.inc_qty =  to_decimal(tot_anz)
        str_list.amount =  to_decimal(tot_amount)
        str_list.tax_amount =  to_decimal(tot_tax)
        str_list.tot_amt =  to_decimal(tot_amt)


    def create_list22():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date


        nonlocal str_list, taxcode_list
        nonlocal str_list_list

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        amt:Decimal = to_decimal("0.0")
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        t_tax =  to_decimal("0")
        t_inv =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr == l_lieferant.lief_nr) & (L_ophis.anzahl != 0) & (L_ophis.op_art == 1) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.datum, L_ophis.artnr).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if matches(l_lieferant.plz,r"*#*"):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(l_ophis.warenwert) + to_decimal(str_list.tax_amount)
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )


        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr == l_lieferant.lief_nr) & (L_ophis.anzahl != 0) & (L_ophis.lager_nr == store) & (L_ophis.op_art == 1) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.datum, L_ophis.artnr).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if matches(l_lieferant.plz,r"*#*"):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(l_ophis.warenwert) + to_decimal(str_list.tax_amount)
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty =  to_decimal(tot_anz)
        str_list.inc_qty =  to_decimal(tot_anz)
        str_list.amount =  to_decimal(tot_amount)
        str_list.tax_amount =  to_decimal(tot_tax)
        str_list.tot_amt =  to_decimal(tot_amt)


    def create_list1b():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date


        nonlocal str_list, taxcode_list
        nonlocal str_list_list

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        amt:Decimal = to_decimal("0.0")
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.datum, L_ophis.artnr, L_untergrup.bezeich, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_ophis.lief_nr)]})

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.description = lscheinnr
                    str_list.supplier = "T O T A L"
                    str_list.qty =  to_decimal(t_anz)
                    str_list.inc_qty =  to_decimal(t_anz)
                    str_list.amount =  to_decimal(t_amt)
                    str_list.tax_amount =  to_decimal(t_tax)
                    str_list.tot_amt =  to_decimal(t_inv)


                    lscheinnr = l_untergrup.bezeich
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    t_tax =  to_decimal("0")
                    t_inv =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.lager_nr == l_ophis.lager_nr and str_list.artnr == l_ophis.artnr and str_list.artnr == l_ophis.artnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if matches(l_lieferant.plz,r"*#*"):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(l_ophis.warenwert) + to_decimal(str_list.tax_amount)
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (L_ophis.lager_nr == store) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.datum, L_ophis.artnr, L_untergrup.bezeich, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_ophis.lief_nr)]})

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.description = lscheinnr
                    str_list.supplier = "T O T A L"
                    str_list.qty =  to_decimal(t_anz)
                    str_list.inc_qty =  to_decimal(t_anz)
                    str_list.amount =  to_decimal(t_amt)
                    str_list.tax_amount =  to_decimal(t_tax)
                    str_list.tot_amt =  to_decimal(t_inv)


                    lscheinnr = l_untergrup.bezeich
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    t_tax =  to_decimal("0")
                    t_inv =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.lager_nr == l_ophis.lager_nr and str_list.artnr == l_ophis.artnr and str_list.artnr == l_ophis.artnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if matches(l_lieferant.plz,r"*#*"):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(l_ophis.warenwert) + to_decimal(str_list.tax_amount)
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.description = lscheinnr
        str_list.supplier = "T O T A L"
        str_list.qty =  to_decimal(t_anz)
        str_list.inc_qty =  to_decimal(t_anz)
        str_list.amount =  to_decimal(t_amt)
        str_list.tax_amount =  to_decimal(t_tax)
        str_list.tot_amt =  to_decimal(t_inv)


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty =  to_decimal(tot_anz)
        str_list.inc_qty =  to_decimal(tot_anz)
        str_list.amount =  to_decimal(tot_amount)
        str_list.tax_amount =  to_decimal(tot_tax)
        str_list.tot_amt =  to_decimal(tot_amt)


    def create_list11b():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date


        nonlocal str_list, taxcode_list
        nonlocal str_list_list

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        lscheinnr:string = ""
        amt:Decimal = to_decimal("0.0")
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.datum, L_ophis.artnr, L_untergrup.bezeich, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_ophis.lief_nr)]})

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.description = lscheinnr
                    str_list.supplier = "T O T A L"
                    str_list.qty =  to_decimal(t_anz)
                    str_list.inc_qty =  to_decimal(t_anz)
                    str_list.amount =  to_decimal(t_amt)
                    str_list.tax_amount =  to_decimal(t_tax)
                    str_list.tot_amt =  to_decimal(t_inv)


                    lscheinnr = l_untergrup.bezeich
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    t_tax =  to_decimal("0")
                    t_inv =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if matches(l_lieferant.plz,r"*#*"):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(l_ophis.warenwert) + to_decimal(str_list.tax_amount)
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (L_ophis.lager_nr == store) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.datum, L_ophis.artnr, L_untergrup.bezeich, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_ophis.lief_nr)]})

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.description = lscheinnr
                    str_list.supplier = "T O T A L"
                    str_list.qty =  to_decimal(t_anz)
                    str_list.inc_qty =  to_decimal(t_anz)
                    str_list.amount =  to_decimal(t_amt)
                    str_list.tax_amount =  to_decimal(t_tax)
                    str_list.tot_amt =  to_decimal(t_inv)


                    lscheinnr = l_untergrup.bezeich
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    t_tax =  to_decimal("0")
                    t_inv =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if matches(l_lieferant.plz,r"*#*"):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(l_ophis.warenwert) + to_decimal(str_list.tax_amount)
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.description = lscheinnr
        str_list.supplier = "T O T A L"
        str_list.qty =  to_decimal(t_anz)
        str_list.inc_qty =  to_decimal(t_anz)
        str_list.amount =  to_decimal(t_amt)


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty =  to_decimal(tot_anz)
        str_list.inc_qty =  to_decimal(tot_anz)
        str_list.amount =  to_decimal(tot_amount)
        str_list.tax_amount =  to_decimal(tot_tax)
        str_list.tot_amt =  to_decimal(tot_amt)


    def create_list1br():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date


        nonlocal str_list, taxcode_list
        nonlocal str_list_list

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        amt:Decimal = to_decimal("0.0")
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (L_ophis.docu_nr == (from_doc).lower()) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.artnr, L_untergrup.bezeich, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_ophis.lief_nr)]})

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.description = lscheinnr
                    str_list.supplier = "T O T A L"
                    str_list.qty =  to_decimal(t_anz)
                    str_list.inc_qty =  to_decimal(t_anz)
                    str_list.amount =  to_decimal(t_amt)
                    str_list.tax_amount =  to_decimal(t_tax)
                    str_list.tot_amt =  to_decimal(t_inv)


                    lscheinnr = l_untergrup.bezeich
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    t_tax =  to_decimal("0")
                    t_inv =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.lager_nr == l_ophis.lager_nr and str_list.artnr == l_ophis.artnr and str_list.artnr == l_ophis.artnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if matches(l_lieferant.plz,r"*#*"):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(l_ophis.warenwert) + to_decimal(str_list.tax_amount)
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (L_ophis.lager_nr == store) & (L_ophis.docu_nr == (from_doc).lower()) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.artnr, L_untergrup.bezeich, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_ophis.lief_nr)]})

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.description = lscheinnr
                    str_list.supplier = "T O T A L"
                    str_list.qty =  to_decimal(t_anz)
                    str_list.inc_qty =  to_decimal(t_anz)
                    str_list.amount =  to_decimal(t_amt)
                    str_list.tax_amount =  to_decimal(t_tax)
                    str_list.tot_amt =  to_decimal(t_inv)


                    lscheinnr = l_untergrup.bezeich
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    t_tax =  to_decimal("0")
                    t_inv =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.lager_nr == l_ophis.lager_nr and str_list.artnr == l_ophis.artnr and str_list.artnr == l_ophis.artnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if matches(l_lieferant.plz,r"*#*"):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(l_ophis.warenwert) + to_decimal(str_list.tax_amount)
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.description = lscheinnr
        str_list.supplier = "T O T A L"
        str_list.qty =  to_decimal(t_anz)
        str_list.inc_qty =  to_decimal(t_anz)
        str_list.amount =  to_decimal(t_amt)
        str_list.tax_amount =  to_decimal(t_tax)
        str_list.tot_amt =  to_decimal(t_inv)


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty =  to_decimal(tot_anz)
        str_list.inc_qty =  to_decimal(tot_anz)
        str_list.amount =  to_decimal(tot_amount)
        str_list.tax_amount =  to_decimal(tot_tax)
        str_list.tot_amt =  to_decimal(tot_amt)


    def create_list11br():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date


        nonlocal str_list, taxcode_list
        nonlocal str_list_list

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        lscheinnr:string = ""
        amt:Decimal = to_decimal("0.0")
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (L_ophis.docu_nr == (from_doc).lower()) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.artnr, L_untergrup.bezeich, L_artikel.bezeich, L_ophis.datum).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_ophis.lief_nr)]})

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.description = lscheinnr
                    str_list.supplier = "T O T A L"
                    str_list.qty =  to_decimal(t_anz)
                    str_list.inc_qty =  to_decimal(t_anz)
                    str_list.amount =  to_decimal(t_amt)
                    str_list.tax_amount =  to_decimal(t_tax)
                    str_list.tot_amt =  to_decimal(t_inv)


                    lscheinnr = l_untergrup.bezeich
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    t_tax =  to_decimal("0")
                    t_inv =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if matches(l_lieferant.plz,r"*#*"):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(l_ophis.warenwert) + to_decimal(str_list.tax_amount)
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (L_ophis.lager_nr == store) & (L_ophis.docu_nr == (from_doc).lower()) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.artnr, L_untergrup.bezeich, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_ophis.lief_nr)]})

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.description = lscheinnr
                    str_list.supplier = "T O T A L"
                    str_list.qty =  to_decimal(t_anz)
                    str_list.inc_qty =  to_decimal(t_anz)
                    str_list.amount =  to_decimal(t_amt)
                    str_list.tax_amount =  to_decimal(t_tax)
                    str_list.tot_amt =  to_decimal(t_inv)


                    lscheinnr = l_untergrup.bezeich
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    t_tax =  to_decimal("0")
                    t_inv =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if matches(l_lieferant.plz,r"*#*"):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(l_ophis.warenwert) + to_decimal(str_list.tax_amount)
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.description = lscheinnr
        str_list.supplier = "T O T A L"
        str_list.qty =  to_decimal(t_anz)
        str_list.inc_qty =  to_decimal(t_anz)
        str_list.amount =  to_decimal(t_amt)
        str_list.tax_amount =  to_decimal(t_tax)
        str_list.tot_amt =  to_decimal(t_inv)


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty =  to_decimal(tot_anz)
        str_list.inc_qty =  to_decimal(tot_anz)
        str_list.amount =  to_decimal(tot_amount)
        str_list.tax_amount =  to_decimal(tot_tax)
        str_list.tot_amt =  to_decimal(tot_amt)


    def create_list1as():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date


        nonlocal str_list, taxcode_list
        nonlocal str_list_list

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        amt:Decimal = to_decimal("0.0")
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.firma, l_lieferant.lief_nr, l_lieferant.plz, l_lieferant._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.firma, L_lieferant.lief_nr, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr == l_lieferant.lief_nr) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.lscheinnr, L_ophis.artnr, L_ophis.datum).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr

                if lscheinnr != l_ophis.lscheinnr:
                    lscheinnr = l_ophis.lscheinnr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.supplier = "T O T A L"
                    str_list.qty =  to_decimal(t_anz)
                    str_list.inc_qty =  to_decimal(t_anz)
                    str_list.amount =  to_decimal(t_amt)
                    str_list.tax_amount =  to_decimal(t_tax)
                    str_list.tot_amt =  to_decimal(t_inv)


                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    t_tax =  to_decimal("0")
                    t_inv =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.lager_nr == l_ophis.lager_nr and str_list.artnr == l_ophis.artnr and str_list.artnr == l_ophis.artnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if matches(l_lieferant.plz,r"*#*"):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(l_ophis.warenwert) + to_decimal(str_list.tax_amount)
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.firma, l_lieferant.lief_nr, l_lieferant.plz, l_lieferant._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.firma, L_lieferant.lief_nr, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr == l_lieferant.lief_nr) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (L_ophis.lager_nr == store) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.lscheinnr, L_ophis.artnr, L_ophis.datum).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr

                if lscheinnr != l_ophis.lscheinnr:
                    lscheinnr = l_ophis.lscheinnr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.supplier = "T O T A L"
                    str_list.qty =  to_decimal(t_anz)
                    str_list.inc_qty =  to_decimal(t_anz)
                    str_list.amount =  to_decimal(t_amt)
                    str_list.tax_amount =  to_decimal(t_tax)
                    str_list.tot_amt =  to_decimal(t_inv)


                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    t_tax =  to_decimal("0")
                    t_inv =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.lager_nr == l_ophis.lager_nr and str_list.artnr == l_ophis.artnr and str_list.artnr == l_ophis.artnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if matches(l_lieferant.plz,r"*#*"):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(l_ophis.warenwert) + to_decimal(str_list.tax_amount)
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "T O T A L"
        str_list.qty =  to_decimal(t_anz)
        str_list.inc_qty =  to_decimal(t_anz)
        str_list.amount =  to_decimal(t_amt)
        str_list.tax_amount =  to_decimal(t_tax)
        str_list.tot_amt =  to_decimal(t_inv)


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty =  to_decimal(tot_anz)
        str_list.inc_qty =  to_decimal(tot_anz)
        str_list.amount =  to_decimal(tot_amount)
        str_list.tax_amount =  to_decimal(tot_tax)
        str_list.tot_amt =  to_decimal(tot_amt)


    def create_list11as():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date


        nonlocal str_list, taxcode_list
        nonlocal str_list_list

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        lscheinnr:string = ""
        amt:Decimal = to_decimal("0.0")
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.firma, l_lieferant.lief_nr, l_lieferant.plz, l_lieferant._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.firma, L_lieferant.lief_nr, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr == l_lieferant.lief_nr) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.lscheinnr, L_ophis.artnr, L_ophis.datum).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr

                if lscheinnr != l_ophis.lscheinnr:
                    lscheinnr = l_ophis.lscheinnr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.supplier = "T O T A L"
                    str_list.qty =  to_decimal(t_anz)
                    str_list.inc_qty =  to_decimal(t_anz)
                    str_list.amount =  to_decimal(t_amt)
                    str_list.tax_amount =  to_decimal(t_tax)
                    str_list.tot_amt =  to_decimal(t_inv)


                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    t_tax =  to_decimal("0")
                    t_inv =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if matches(l_lieferant.plz,r"*#*"):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(l_ophis.warenwert) + to_decimal(str_list.tax_amount)
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.firma, l_lieferant.lief_nr, l_lieferant.plz, l_lieferant._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.firma, L_lieferant.lief_nr, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr == l_lieferant.lief_nr) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (L_ophis.lager_nr == store) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.lscheinnr, L_ophis.artnr, L_ophis.datum).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr

                if lscheinnr != l_ophis.lscheinnr:
                    lscheinnr = l_ophis.lscheinnr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.supplier = "T O T A L"
                    str_list.qty =  to_decimal(t_anz)
                    str_list.inc_qty =  to_decimal(t_anz)
                    str_list.amount =  to_decimal(t_amt)
                    str_list.tax_amount =  to_decimal(t_tax)
                    str_list.tot_amt =  to_decimal(t_inv)


                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    t_tax =  to_decimal("0")
                    t_inv =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if matches(l_lieferant.plz,r"*#*"):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(l_ophis.warenwert) + to_decimal(str_list.tax_amount)
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "T O T A L"
        str_list.qty =  to_decimal(t_anz)
        str_list.inc_qty =  to_decimal(t_anz)
        str_list.amount =  to_decimal(t_amt)
        str_list.tax_amount =  to_decimal(t_tax)
        str_list.tot_amt =  to_decimal(t_inv)


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty =  to_decimal(tot_anz)
        str_list.inc_qty =  to_decimal(tot_anz)
        str_list.amount =  to_decimal(tot_amount)
        str_list.tax_amount =  to_decimal(tot_tax)
        str_list.tot_amt =  to_decimal(tot_amt)


    def create_list1bs():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date


        nonlocal str_list, taxcode_list
        nonlocal str_list_list

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        amt:Decimal = to_decimal("0.0")
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr == l_lieferant.lief_nr) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.artnr, L_untergrup.bezeich, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_ophis.lief_nr)]})

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.description = lscheinnr
                    str_list.supplier = "T O T A L"
                    str_list.qty =  to_decimal(t_anz)
                    str_list.inc_qty =  to_decimal(t_anz)
                    str_list.amount =  to_decimal(t_amt)
                    str_list.tax_amount =  to_decimal(t_tax)
                    str_list.tot_amt =  to_decimal(t_inv)


                    lscheinnr = l_untergrup.bezeich
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    t_tax =  to_decimal("0")
                    t_inv =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.lager_nr == l_ophis.lager_nr and str_list.artnr == l_ophis.artnr and str_list.artnr == l_ophis.artnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if matches(l_lieferant.plz,r"*#*"):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(l_ophis.warenwert) + to_decimal(str_list.tax_amount)
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr == l_lieferant.lief_nr) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (L_ophis.lager_nr == store) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.artnr, L_untergrup.bezeich, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_ophis.lief_nr)]})

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.description = lscheinnr
                    str_list.supplier = "T O T A L"
                    str_list.qty =  to_decimal(t_anz)
                    str_list.inc_qty =  to_decimal(t_anz)
                    str_list.amount =  to_decimal(t_amt)
                    str_list.tax_amount =  to_decimal(t_tax)
                    str_list.tot_amt =  to_decimal(t_inv)


                    lscheinnr = l_untergrup.bezeich
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    t_tax =  to_decimal("0")
                    t_inv =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.lager_nr == l_ophis.lager_nr and str_list.artnr == l_ophis.artnr and str_list.artnr == l_ophis.artnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if matches(l_lieferant.plz,r"*#*"):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(l_ophis.warenwert) + to_decimal(str_list.tax_amount)
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.description = lscheinnr
        str_list.supplier = "T O T A L"
        str_list.qty =  to_decimal(t_anz)
        str_list.inc_qty =  to_decimal(t_anz)
        str_list.amount =  to_decimal(t_amt)
        str_list.tax_amount =  to_decimal(t_tax)
        str_list.tot_amt =  to_decimal(t_inv)


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty =  to_decimal(tot_anz)
        str_list.inc_qty =  to_decimal(tot_anz)
        str_list.amount =  to_decimal(tot_amount)
        str_list.tax_amount =  to_decimal(tot_tax)
        str_list.tot_amt =  to_decimal(tot_amt)


    def create_list11bs():

        nonlocal err_code, str_list_list, i, supp_nr, tot_anz, tot_amount, long_digit, tot_tax, tot_amt, loopi, lvcarea, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date


        nonlocal str_list, taxcode_list
        nonlocal str_list_list

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        lscheinnr:string = ""
        amt:Decimal = to_decimal("0.0")
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr == l_lieferant.lief_nr) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.artnr, L_untergrup.bezeich, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_ophis.lief_nr)]})

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.description = lscheinnr
                    str_list.supplier = "T O T A L"
                    str_list.qty =  to_decimal(t_anz)
                    str_list.inc_qty =  to_decimal(t_anz)
                    str_list.amount =  to_decimal(t_amt)
                    str_list.tax_amount =  to_decimal(t_tax)
                    str_list.tot_amt =  to_decimal(t_inv)


                    lscheinnr = l_untergrup.bezeich
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    t_tax =  to_decimal("0")
                    t_inv =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if matches(l_lieferant.plz,r"*#*"):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(l_ophis.warenwert) + to_decimal(str_list.tax_amount)
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_ophis.lscheinnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.artnr, l_ophis.einzelpreis, l_ophis.datum, l_ophis.lief_nr, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.lscheinnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.artnr, L_ophis.einzelpreis, L_ophis.datum, L_ophis.lief_nr, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr == l_lieferant.lief_nr) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (L_ophis.lager_nr == store) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.artnr, L_untergrup.bezeich, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_ophis.lief_nr)]})

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.description = lscheinnr
                    str_list.supplier = "T O T A L"
                    str_list.qty =  to_decimal(t_anz)
                    str_list.inc_qty =  to_decimal(t_anz)
                    str_list.amount =  to_decimal(t_amt)
                    str_list.tax_amount =  to_decimal(t_tax)
                    str_list.tot_amt =  to_decimal(t_inv)


                    lscheinnr = l_untergrup.bezeich
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    t_tax =  to_decimal("0")
                    t_inv =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                    str_list.inc_qty =  to_decimal(str_list.qty)
                    str_list.amount =  to_decimal(str_list.warenwert)

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        amt =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )


                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.artnr = l_ophis.artnr
                    str_list.lager_nr = l_ophis.lager_nr
                    str_list.docu_nr = l_ophis.docu_nr
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.epreis =  to_decimal(l_ophis.einzelpreis)
                    str_list.warenwert =  to_decimal(l_ophis.warenwert)
                    str_list.datum = l_ophis.datum
                    str_list.st = l_ophis.lager_nr
                    str_list.supplier = l_lieferant.firma
                    str_list.article = l_artikel.artnr
                    str_list.description = l_artikel.bezeich
                    str_list.d_unit = l_artikel.traubensorte
                    str_list.price =  to_decimal(l_ophis.einzelpreis)
                    str_list.inc_qty =  to_decimal(l_ophis.anzahl)
                    str_list.amount =  to_decimal(l_ophis.warenwert)
                    str_list.lief_nr = l_ophis.lief_nr
                    str_list.tax_code = l_artikel.lief_artnr[2]

                    if l_lieferant.plz != " ":

                        if matches(l_lieferant.plz,r"*#*"):
                            for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                                if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                                    str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                                    break

                    taxcode_list = query(taxcode_list_list, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

                    if taxcode_list:
                        str_list.tax_amount =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                        t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                        str_list.tot_amt =  to_decimal(l_ophis.warenwert) + to_decimal(str_list.tax_amount)
                        t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )
                        tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )

                    if l_ophis.docu_nr == l_ophis.lscheinnr:
                        str_list.docu_no = "Direct Pchase "
                    else:
                        str_list.docu_no = l_ophis.docu_nr
                    str_list.deliv_no = l_ophis.lscheinnr
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.description = lscheinnr
        str_list.supplier = "T O T A L"
        str_list.qty =  to_decimal(t_anz)
        str_list.inc_qty =  to_decimal(t_anz)
        str_list.amount =  to_decimal(t_amt)
        str_list.tax_amount =  to_decimal(t_tax)
        str_list.tot_amt =  to_decimal(t_inv)


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.supplier = "GRAND TOTAL"
        str_list.qty =  to_decimal(tot_anz)
        str_list.inc_qty =  to_decimal(tot_anz)
        str_list.amount =  to_decimal(tot_amount)
        str_list.tax_amount =  to_decimal(tot_tax)
        str_list.tot_amt =  to_decimal(tot_amt)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    if from_supp != "":

        l_lieferant = get_cache (L_lieferant, {"firma": [(eq, from_supp)]})

        if not l_lieferant:
            err_code = 1

            return generate_output()
        else:
            supp_nr = l_lieferant.lief_nr

    if from_doc != "":

        l_ophis = get_cache (L_ophis, {"docu_nr": [(eq, from_doc)]})

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