#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 26/8/2025
# data kosong
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_kredit, Htparam, L_lieferant, L_ophis, L_artikel, L_untergrup, Gl_acct, L_ophhis, Queasy

from sqlalchemy import cast, Numeric

taxcode_list_data, Taxcode_list = create_model("Taxcode_list", {"taxcode":string, "taxamount":Decimal})

def supply_hinlist_btn_go_1_webbl(pvilanguage:int, from_supp:string, from_doc:string, sorttype:int, from_grp:int, to_grp:int, store:int, all_supp:bool, all_doc:bool, from_date:date, to_date:date, taxcode_list_data:[Taxcode_list]):

    prepare_cache ([L_kredit, Htparam, L_lieferant, L_ophis, L_artikel, L_untergrup, Gl_acct, L_ophhis, Queasy])
    # Rd 26/8/2025
    from_supp = from_supp.strip()
    from_doc = from_doc.strip()
    err_code = 0
    str_list_data = []
    supp_nr:int = 0
    long_digit:bool = False
    tot_anz:Decimal = to_decimal("0.0")
    tot_amount:Decimal = to_decimal("0.0")
    tot_amountexcl:Decimal = to_decimal("0.0")
    tot_tax:Decimal = to_decimal("0.0")
    tot_amt:Decimal = to_decimal("0.0")
    tot_price:Decimal = to_decimal("0.0")
    counter:int = 0
    loopi:int = 0
    unit_price:Decimal = to_decimal("0.0")
    lvcarea:string = "supply-hinlist"
    l_kredit = htparam = l_lieferant = l_ophis = l_artikel = l_untergrup = gl_acct = l_ophhis = queasy = None

    str_list = taxcode_list = buff_l_kredit = None

    str_list_data, Str_list = create_model("Str_list", {"artnr":int, "lager_nr":int, "docu_nr":string, "lscheinnr":string, "qty":Decimal, "epreis":Decimal, "warenwert":Decimal, "datum":date, "st":int, "supplier":string, "article":int, "description":string, "d_unit":string, "price":Decimal, "inc_qty":Decimal, "amount":Decimal, "docu_no":string, "deliv_no":string, "id":string, "gstid":string, "tax_code":string, "tax_amount":Decimal, "tot_amt":Decimal, "lief_nr":int, "fibu":string, "fibu_bez":string, "addvat_value":Decimal, "amountexcl":Decimal, "invoice_nr":string, "serial_number":string, "invoice_date":date, "remark_artikel":string, "ap_voucher":int, "disc_amount":Decimal, "addvat_amount":Decimal, "disc_amount2":Decimal, "vat_amount":Decimal})

    Buff_l_kredit = create_buffer("Buff_l_kredit",L_kredit)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, str_list_data, supp_nr, long_digit, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, tot_price, counter, loopi, unit_price, lvcarea, l_kredit, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup, gl_acct, l_ophhis, queasy
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        return {"err_code": err_code, "str-list": str_list_data}

    def create_list1a():

        nonlocal err_code, str_list_data, supp_nr, long_digit, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, tot_price, counter, loopi, unit_price, lvcarea, l_kredit, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup, gl_acct, l_ophhis, queasy
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        t_price:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        utt_bezeich:string = ""
        t_amountexcl:Decimal = to_decimal("0.0")
        count_data:int = 0
        show_total:bool = True
        amt:Decimal = to_decimal("0.0")
        pure_bundle_unit_price:Decimal = to_decimal("0.0")
        str_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_price =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_amountexcl =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, l_ophis.fibukonto, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid in db_session.query(L_ophis.lscheinnr, L_ophis.datum, L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.einzelpreis, L_ophis.lief_nr, L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & 
                     (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & 
                     # Rd 26/8/2025
                     (not_ ((length(L_ophis.fibukonto) > 8) & 
                                                (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                     ).order_by(L_ophis.lscheinnr, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                count_data = count_data + 1

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)
        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, l_ophis.fibukonto, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid in db_session.query(L_ophis.lscheinnr, L_ophis.datum, L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.einzelpreis, L_ophis.lief_nr, L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & 
                     (L_ophis.lager_nr == store) & 
                     # Rd 26/8/2025
                     (not_ ((length(L_ophis.fibukonto) > 8) & 
                                                (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                     ).order_by(L_ophis.lscheinnr, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                count_data = count_data + 1

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)

        if show_total:

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                str_list.description = "T O T A L"
                str_list.qty =  to_decimal(t_anz)
                str_list.inc_qty =  to_decimal(t_anz)
                str_list.amount =  to_decimal(t_amt)
                str_list.warenwert =  to_decimal(t_amt)
                str_list.amountexcl =  to_decimal(t_amountexcl)
                str_list.tax_amount =  to_decimal(t_tax)
                str_list.tot_amt =  to_decimal(t_inv)
                str_list.price =  to_decimal("0")

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                # str_list = Str_list()
                # str_list_data.append(str_list)

                str_list.description = "GRAND TOTAL"
                str_list.qty =  to_decimal(tot_anz)
                str_list.inc_qty =  to_decimal(tot_anz)
                str_list.amount =  to_decimal(tot_amount)
                str_list.warenwert =  to_decimal(tot_amount)
                str_list.amountexcl =  to_decimal(tot_amountexcl)
                str_list.tax_amount =  to_decimal(tot_tax)
                str_list.tot_amt =  to_decimal(tot_amt)
                str_list.price =  to_decimal("0")


        else:
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.description = "GRAND TOTAL"
            str_list.qty =  to_decimal(tot_anz)
            str_list.inc_qty =  to_decimal(tot_anz)
            str_list.amount =  to_decimal(tot_amount)
            str_list.warenwert =  to_decimal(tot_amount)
            str_list.amountexcl =  to_decimal(tot_amountexcl)
            str_list.tax_amount =  to_decimal(tot_tax)
            str_list.tot_amt =  to_decimal(tot_amt)
            str_list.price =  to_decimal("0")


    def create_list1ar():

        nonlocal err_code, str_list_data, supp_nr, long_digit, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, tot_price, counter, loopi, unit_price, lvcarea, l_kredit, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup, gl_acct, l_ophhis, queasy
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        t_price:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        utt_bezeich:string = ""
        t_amountexcl:Decimal = to_decimal("0.0")
        count_data:int = 0
        show_total:bool = True
        amt:Decimal = to_decimal("0.0")
        pure_bundle_unit_price:Decimal = to_decimal("0.0")
        str_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_price =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_amountexcl =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, l_ophis.fibukonto, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid in db_session.query(L_ophis.lscheinnr, L_ophis.datum, L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.einzelpreis, L_ophis.lief_nr, L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & 
                     (L_ophis.docu_nr == (from_doc).lower()) & 
                     # Rd 26/8/2025
                     (not_ ((length(L_ophis.fibukonto) > 8) & 
                                                (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                     ).order_by(L_ophis.lscheinnr, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                count_data = count_data + 1

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)
        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, l_ophis.fibukonto, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid in db_session.query(L_ophis.lscheinnr, L_ophis.datum, L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.einzelpreis, L_ophis.lief_nr, L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & 
                     (L_ophis.lager_nr == store) & (L_ophis.docu_nr == (from_doc).lower()) & 
                     # Rd 26/8/2025
                     (not_ ((length(L_ophis.fibukonto) > 8) & 
                                                (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                     ).order_by(L_ophis.lscheinnr, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                count_data = count_data + 1

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)

        if show_total:

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                str_list.description = "T O T A L"
                str_list.qty =  to_decimal(t_anz)
                str_list.inc_qty =  to_decimal(t_anz)
                str_list.amount =  to_decimal(t_amt)
                str_list.warenwert =  to_decimal(t_amt)
                str_list.amountexcl =  to_decimal(t_amountexcl)
                str_list.tax_amount =  to_decimal(t_tax)
                str_list.tot_amt =  to_decimal(t_inv)
                str_list.price =  to_decimal("0")

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                # str_list = Str_list()
                # str_list_data.append(str_list)

                str_list.description = "GRAND TOTAL"
                str_list.qty =  to_decimal(tot_anz)
                str_list.inc_qty =  to_decimal(tot_anz)
                str_list.amount =  to_decimal(tot_amount)
                str_list.warenwert =  to_decimal(tot_amount)
                str_list.amountexcl =  to_decimal(tot_amountexcl)
                str_list.tax_amount =  to_decimal(tot_tax)
                str_list.tot_amt =  to_decimal(tot_amt)
                str_list.price =  to_decimal("0")


        else:
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.description = "GRAND TOTAL"
            str_list.qty =  to_decimal(tot_anz)
            str_list.inc_qty =  to_decimal(tot_anz)
            str_list.amount =  to_decimal(tot_amount)
            str_list.warenwert =  to_decimal(tot_amount)
            str_list.amountexcl =  to_decimal(tot_amountexcl)
            str_list.tax_amount =  to_decimal(tot_tax)
            str_list.tot_amt =  to_decimal(tot_amt)
            str_list.price =  to_decimal("0")


    def create_list11():

        nonlocal err_code, str_list_data, supp_nr, long_digit, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, tot_price, counter, loopi, unit_price, lvcarea, l_kredit, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup, gl_acct, l_ophhis, queasy
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        t_price:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        utt_bezeich:string = ""
        t_amountexcl:Decimal = to_decimal("0.0")
        count_data:int = 0
        show_total:bool = True
        amt:Decimal = to_decimal("0.0")
        pure_bundle_unit_price:Decimal = to_decimal("0.0")
        str_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_price =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_amountexcl =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, \
                l_ophis.fibukonto, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.lief_nr, \
                l_lieferant.firma, l_lieferant.plz, l_lieferant._recid \
                    in db_session.query(L_ophis.lscheinnr, L_ophis.datum, L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, \
                                        L_ophis.einzelpreis, L_ophis.lief_nr, L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, \
                                        L_artikel.lief_artnr, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid)\
                                .join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp))\
                                .join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr))\
                                .filter(
                                        (L_ophis.datum >= from_date) & 
                                        (L_ophis.datum <= to_date) & 
                                        (L_ophis.lief_nr > 0) & 
                                        (L_ophis.op_art == 1) & 
                                        (L_ophis.anzahl != 0) & 
                                        (not_ ((length(L_ophis.fibukonto) > 8) & 
                                                (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                                ).order_by(L_lieferant.firma, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                count_data = count_data + 1

                if lief_nr == 0:
                    lief_nr = l_lieferant.lief_nr
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)
        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, \
                l_ophis.fibukonto, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.lief_nr, \
                    l_lieferant.firma, l_lieferant.plz, l_lieferant._recid \
                in db_session.query(L_ophis.lscheinnr, L_ophis.datum, L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, \
                                    L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.einzelpreis, L_ophis.lief_nr, L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, \
                                    L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, \
                                    L_lieferant.plz, L_lieferant._recid)\
                .join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp))\
                .join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr))\
                .filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & 
                     (L_ophis.op_art == 1) & 
                     (L_ophis.anzahl != 0) & 
                     (L_ophis.lager_nr == store) & 
                     # Rd 26/8/2025
                     (not_ ((length(L_ophis.fibukonto) > 8) & 
                                                (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                     ).order_by(L_lieferant.firma, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                count_data = count_data + 1

                if lief_nr == 0:
                    lief_nr = l_lieferant.lief_nr
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)

        if show_total:

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                str_list.description = "T O T A L"
                str_list.qty =  to_decimal(t_anz)
                str_list.inc_qty =  to_decimal(t_anz)
                str_list.amount =  to_decimal(t_amt)
                str_list.warenwert =  to_decimal(t_amt)
                str_list.amountexcl =  to_decimal(t_amountexcl)
                str_list.tax_amount =  to_decimal(t_tax)
                str_list.tot_amt =  to_decimal(t_inv)
                str_list.price =  to_decimal("0")

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                # str_list = Str_list()
                # str_list_data.append(str_list)

                str_list.description = "GRAND TOTAL"
                str_list.qty =  to_decimal(tot_anz)
                str_list.inc_qty =  to_decimal(tot_anz)
                str_list.amount =  to_decimal(tot_amount)
                str_list.warenwert =  to_decimal(tot_amount)
                str_list.amountexcl =  to_decimal(tot_amountexcl)
                str_list.tax_amount =  to_decimal(tot_tax)
                str_list.tot_amt =  to_decimal(tot_amt)
                str_list.price =  to_decimal("0")


        else:
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.description = "GRAND TOTAL"
            str_list.qty =  to_decimal(tot_anz)
            str_list.inc_qty =  to_decimal(tot_anz)
            str_list.amount =  to_decimal(tot_amount)
            str_list.warenwert =  to_decimal(tot_amount)
            str_list.amountexcl =  to_decimal(tot_amountexcl)
            str_list.tax_amount =  to_decimal(tot_tax)
            str_list.tot_amt =  to_decimal(tot_amt)
            str_list.price =  to_decimal("0")


    def create_list11a():

        nonlocal err_code, str_list_data, supp_nr, long_digit, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, tot_price, counter, loopi, unit_price, lvcarea, l_kredit, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup, gl_acct, l_ophhis, queasy
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        t_price:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        utt_bezeich:string = ""
        t_amountexcl:Decimal = to_decimal("0.0")
        count_data:int = 0
        show_total:bool = True
        amt:Decimal = to_decimal("0.0")
        pure_bundle_unit_price:Decimal = to_decimal("0.0")
        str_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_price =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_amountexcl =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:
           
            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, \
                l_ophis.fibukonto, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.lief_nr, \
                    l_lieferant.firma, l_lieferant.plz, l_lieferant._recid \
                in db_session.query(L_ophis.lscheinnr, L_ophis.datum, L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.einzelpreis, \
                                    L_ophis.lief_nr, L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, \
                                    L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid)\
                            .join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & 
                                  (L_artikel.endkum >= from_grp) & 
                                  (L_artikel.endkum <= to_grp)) \
                            .join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr))\
                .filter(
                        (L_ophis.datum >= from_date) & 
                        (L_ophis.datum <= to_date) & 
                        (L_ophis.lief_nr > 0) & 
                        (L_ophis.op_art == 1) & 
                        (L_ophis.anzahl != 0) &
                        # Rd 26/8/2025
                        (not_ ((length(L_ophis.fibukonto) > 8) & 
                                                    (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                ).order_by(L_ophis.lscheinnr, L_ophis.datum, L_artikel.bezeich).all():
                
                """
                        (
                            not_   (length(L_ophis.fibukonto) > 8) & 
                                (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")
                        )

                """
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True

 
                count_data = count_data + 1
                # print("LS:", lscheinnr, l_ophis.fibukonto , "|")
                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr
                
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)
                
        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, l_ophis.fibukonto, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid \
                in db_session.query(L_ophis.lscheinnr, L_ophis.datum, L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.einzelpreis, L_ophis.lief_nr, L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr))\
                .filter(
                     (L_ophis.datum >= from_date) & 
                     (L_ophis.datum <= to_date) & 
                     (L_ophis.lief_nr > 0) & 
                     (L_ophis.op_art == 1) & 
                     (L_ophis.anzahl != 0) & 
                     (L_ophis.lager_nr == store) & 
                     # Rd 26/8/2025
                     (not_ ((length(L_ophis.fibukonto) > 8) & 
                                                (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                    ).order_by(L_ophis.lscheinnr, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                count_data = count_data + 1

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)

        if show_total:

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                str_list.description = "T O T A L"
                str_list.qty =  to_decimal(t_anz)
                str_list.inc_qty =  to_decimal(t_anz)
                str_list.amount =  to_decimal(t_amt)
                str_list.warenwert =  to_decimal(t_amt)
                str_list.amountexcl =  to_decimal(t_amountexcl)
                str_list.tax_amount =  to_decimal(t_tax)
                str_list.tot_amt =  to_decimal(t_inv)
                str_list.price =  to_decimal("0")

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                # str_list = Str_list()
                # str_list_data.append(str_list)

                str_list.description = "GRAND TOTAL"
                str_list.qty =  to_decimal(tot_anz)
                str_list.inc_qty =  to_decimal(tot_anz)
                str_list.amount =  to_decimal(tot_amount)
                str_list.warenwert =  to_decimal(tot_amount)
                str_list.amountexcl =  to_decimal(tot_amountexcl)
                str_list.tax_amount =  to_decimal(tot_tax)
                str_list.tot_amt =  to_decimal(tot_amt)
                str_list.price =  to_decimal("0")


        else:
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.description = "GRAND TOTAL"
            str_list.qty =  to_decimal(tot_anz)
            str_list.inc_qty =  to_decimal(tot_anz)
            str_list.amount =  to_decimal(tot_amount)
            str_list.warenwert =  to_decimal(tot_amount)
            str_list.amountexcl =  to_decimal(tot_amountexcl)
            str_list.tax_amount =  to_decimal(tot_tax)
            str_list.tot_amt =  to_decimal(tot_amt)
            str_list.price =  to_decimal("0")


    def create_list11ar():

        nonlocal err_code, str_list_data, supp_nr, long_digit, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, tot_price, counter, loopi, unit_price, lvcarea, l_kredit, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup, gl_acct, l_ophhis, queasy
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        t_price:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        utt_bezeich:string = ""
        t_amountexcl:Decimal = to_decimal("0.0")
        count_data:int = 0
        show_total:bool = True
        amt:Decimal = to_decimal("0.0")
        pure_bundle_unit_price:Decimal = to_decimal("0.0")
        str_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_price =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_amountexcl =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, l_ophis.fibukonto, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid in db_session.query(L_ophis.lscheinnr, L_ophis.datum, L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.einzelpreis, L_ophis.lief_nr, L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & 
                     (L_ophis.anzahl != 0) & 
                     (L_ophis.docu_nr == (from_doc).lower()) & 
                    #  (not_ (length(L_ophis.fibukonto) > 8) & (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length(("CANCELLED").lower() ) + 1 - 1, length(L_ophis.fibukonto)) == ("CANCELLED").lower()))
                    # Rd 26/8/2025
                     (not_ ((length(L_ophis.fibukonto) > 8) & 
                                                (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                     ).order_by(L_ophis.lscheinnr, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                count_data = count_data + 1

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)
        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, l_ophis.fibukonto, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid in db_session.query(L_ophis.lscheinnr, L_ophis.datum, L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.einzelpreis, L_ophis.lief_nr, L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & 
                     (L_ophis.lief_nr > 0) & 
                     (L_ophis.op_art == 1) & 
                     (L_ophis.anzahl != 0) & 
                     (L_ophis.lager_nr == store) & 
                     (L_ophis.docu_nr == (from_doc).lower()) & 
                     # Rd 26/8/2025
                     (not_ ((length(L_ophis.fibukonto) > 8) & 
                                                (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                     ).order_by(L_ophis.lscheinnr, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                count_data = count_data + 1

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)

        if show_total:

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                str_list.description = "T O T A L"
                str_list.qty =  to_decimal(t_anz)
                str_list.inc_qty =  to_decimal(t_anz)
                str_list.amount =  to_decimal(t_amt)
                str_list.warenwert =  to_decimal(t_amt)
                str_list.amountexcl =  to_decimal(t_amountexcl)
                str_list.tax_amount =  to_decimal(t_tax)
                str_list.tot_amt =  to_decimal(t_inv)
                str_list.price =  to_decimal("0")

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                # str_list = Str_list()
                # str_list_data.append(str_list)

                str_list.description = "GRAND TOTAL"
                str_list.qty =  to_decimal(tot_anz)
                str_list.inc_qty =  to_decimal(tot_anz)
                str_list.amount =  to_decimal(tot_amount)
                str_list.warenwert =  to_decimal(tot_amount)
                str_list.amountexcl =  to_decimal(tot_amountexcl)
                str_list.tax_amount =  to_decimal(tot_tax)
                str_list.tot_amt =  to_decimal(tot_amt)
                str_list.price =  to_decimal("0")


        else:
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.description = "GRAND TOTAL"
            str_list.qty =  to_decimal(tot_anz)
            str_list.inc_qty =  to_decimal(tot_anz)
            str_list.amount =  to_decimal(tot_amount)
            str_list.warenwert =  to_decimal(tot_amount)
            str_list.amountexcl =  to_decimal(tot_amountexcl)
            str_list.tax_amount =  to_decimal(tot_tax)
            str_list.tot_amt =  to_decimal(tot_amt)
            str_list.price =  to_decimal("0")


    def create_list22():

        nonlocal err_code, str_list_data, supp_nr, long_digit, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, tot_price, counter, loopi, unit_price, lvcarea, l_kredit, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup, gl_acct, l_ophhis, queasy
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        t_price:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        utt_bezeich:string = ""
        t_amountexcl:Decimal = to_decimal("0.0")
        count_data:int = 0
        show_total:bool = False
        amt:Decimal = to_decimal("0.0")
        pure_bundle_unit_price:Decimal = to_decimal("0.0")
        str_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_price =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_amountexcl =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, \
                l_ophis.fibukonto, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid \
                in db_session.query(L_ophis.lscheinnr, L_ophis.datum, L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, \
                                    L_ophis.einzelpreis, L_ophis.lief_nr, L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, \
                                    L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid)\
                    .join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & 
                                    (L_artikel.endkum >= from_grp) & 
                                    (L_artikel.endkum <= to_grp)) \
                    .join(L_lieferant, L_lieferant.lief_nr == L_ophis.lief_nr) \
                    .filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & 
                     (L_ophis.lief_nr == l_lieferant.lief_nr) & 
                     (L_ophis.anzahl != 0) & 
                     (L_ophis.op_art == 1) & 
                    #  (not_ (length(L_ophis.fibukonto) > 8) & (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length(("CANCELLED").lower() ) + 1 - 1, length(L_ophis.fibukonto)) == ("CANCELLED").lower()))
                    # Rd 26/8/2025
                     (not_ ((length(L_ophis.fibukonto) > 8) & 
                            (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                     ).order_by(L_lieferant.firma, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                count_data = count_data + 1

                if lief_nr == 0:
                    lief_nr = l_lieferant.lief_nr
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)
        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, l_ophis.fibukonto, \
                l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid \
                in db_session.query(L_ophis.lscheinnr, L_ophis.datum, \
                                L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.einzelpreis, L_ophis.lief_nr, \
                                L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid)\
                        .join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp))\
                        .join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr))\
                        .filter(
                            (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & 
                            (L_ophis.lief_nr == l_lieferant.lief_nr) & 
                            (L_ophis.anzahl != 0) & (L_ophis.op_art == 1) & 
                            (L_ophis.lager_nr == store) & 
                            #  (not_ (length(L_ophis.fibukonto) > 8) & (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length(("CANCELLED").lower() ) + 1 - 1, length(L_ophis.fibukonto)) == ("CANCELLED").lower()))
                            # Rd 26/8/2025
                            (not_ ((length(L_ophis.fibukonto) > 8) & 
                                                        (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                            ).order_by(L_lieferant.firma, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                count_data = count_data + 1

                if lief_nr == 0:
                    lief_nr = l_lieferant.lief_nr
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)

        if show_total:

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                str_list.description = "T O T A L"
                str_list.qty =  to_decimal(t_anz)
                str_list.inc_qty =  to_decimal(t_anz)
                str_list.amount =  to_decimal(t_amt)
                str_list.warenwert =  to_decimal(t_amt)
                str_list.amountexcl =  to_decimal(t_amountexcl)
                str_list.tax_amount =  to_decimal(t_tax)
                str_list.tot_amt =  to_decimal(t_inv)
                str_list.price =  to_decimal("0")

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                # str_list = Str_list()
                # str_list_data.append(str_list)

                str_list.description = "GRAND TOTAL"
                str_list.qty =  to_decimal(tot_anz)
                str_list.inc_qty =  to_decimal(tot_anz)
                str_list.amount =  to_decimal(tot_amount)
                str_list.warenwert =  to_decimal(tot_amount)
                str_list.amountexcl =  to_decimal(tot_amountexcl)
                str_list.tax_amount =  to_decimal(tot_tax)
                str_list.tot_amt =  to_decimal(tot_amt)
                str_list.price =  to_decimal("0")


        else:
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.description = "GRAND TOTAL"
            str_list.qty =  to_decimal(tot_anz)
            str_list.inc_qty =  to_decimal(tot_anz)
            str_list.amount =  to_decimal(tot_amount)
            str_list.warenwert =  to_decimal(tot_amount)
            str_list.amountexcl =  to_decimal(tot_amountexcl)
            str_list.tax_amount =  to_decimal(tot_tax)
            str_list.tot_amt =  to_decimal(tot_amt)
            str_list.price =  to_decimal("0")


    def create_list1b():

        nonlocal err_code, str_list_data, supp_nr, long_digit, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, tot_price, counter, loopi, unit_price, lvcarea, l_kredit, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup, gl_acct, l_ophhis, queasy
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        t_price:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        utt_bezeich:string = ""
        t_amountexcl:Decimal = to_decimal("0.0")
        count_data:int = 0
        show_total:bool = True
        amt:Decimal = to_decimal("0.0")
        pure_bundle_unit_price:Decimal = to_decimal("0.0")
        str_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_price =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_amountexcl =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            l_untergrup = L_untergrup()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, l_ophis.fibukonto, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.lscheinnr, L_ophis.datum, L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.einzelpreis, L_ophis.lief_nr, L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & 
                     (L_ophis.op_art == 1) & 
                     (L_ophis.anzahl != 0) & 
                    #   (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length(("CANCELLED").lower() ) + 1 - 1, length(L_ophis.fibukonto)) == ("CANCELLED").lower()))
                    # Rd 26/8/2025
                     (not_ ((length(L_ophis.fibukonto) > 8) & 
                                                (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                      ).order_by(L_untergrup.bezeich, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                count_data = count_data + 1

                if utt_bezeich == "":
                    utt_bezeich = l_untergrup.bezeich
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)
        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            l_untergrup = L_untergrup()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, l_ophis.fibukonto, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.lscheinnr, L_ophis.datum, L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.einzelpreis, L_ophis.lief_nr, L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & 
                     (L_ophis.lief_nr > 0) & 
                     (L_ophis.op_art == 1) &
                       (L_ophis.anzahl != 0) & 
                       (L_ophis.lager_nr == store) & 
                    #    (not_ (length(L_ophis.fibukonto) > 8) & (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length(("CANCELLED").lower() ) + 1 - 1, length(L_ophis.fibukonto)) == ("CANCELLED").lower()))
                    # Rd 26/8/2025
                     (not_ ((length(L_ophis.fibukonto) > 8) & 
                                                (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                       ).order_by(L_untergrup.bezeich, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                count_data = count_data + 1

                if utt_bezeich == "":
                    utt_bezeich = l_untergrup.bezeich
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)

        if show_total:

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                str_list.description = "TOTAL SUB-GROUP: " + utt_bezeich
                str_list.qty =  to_decimal(t_anz)
                str_list.inc_qty =  to_decimal(t_anz)
                str_list.amount =  to_decimal(t_amt)
                str_list.warenwert =  to_decimal(t_amt)
                str_list.amountexcl =  to_decimal(t_amountexcl)
                str_list.tax_amount =  to_decimal(t_tax)
                str_list.tot_amt =  to_decimal(t_inv)
                str_list.price =  to_decimal("0")

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                # str_list = Str_list()
                # str_list_data.append(str_list)

                str_list.description = "GRAND TOTAL"
                str_list.qty =  to_decimal(tot_anz)
                str_list.inc_qty =  to_decimal(tot_anz)
                str_list.amount =  to_decimal(tot_amount)
                str_list.warenwert =  to_decimal(tot_amount)
                str_list.amountexcl =  to_decimal(tot_amountexcl)
                str_list.tax_amount =  to_decimal(tot_tax)
                str_list.tot_amt =  to_decimal(tot_amt)
                str_list.price =  to_decimal("0")


        else:
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.description = "TOTAL SUB-GROUP: " + utt_bezeich
            str_list.qty =  to_decimal(tot_anz)
            str_list.inc_qty =  to_decimal(tot_anz)
            str_list.amount =  to_decimal(tot_amount)
            str_list.warenwert =  to_decimal(tot_amount)
            str_list.amountexcl =  to_decimal(tot_amountexcl)
            str_list.tax_amount =  to_decimal(tot_tax)
            str_list.tot_amt =  to_decimal(tot_amt)
            str_list.price =  to_decimal("0")


    def create_list11b():

        nonlocal err_code, str_list_data, supp_nr, long_digit, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, tot_price, counter, loopi, unit_price, lvcarea, l_kredit, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup, gl_acct, l_ophhis, queasy
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        t_price:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        utt_bezeich:string = ""
        t_amountexcl:Decimal = to_decimal("0.0")
        count_data:int = 0
        show_total:bool = True
        amt:Decimal = to_decimal("0.0")
        pure_bundle_unit_price:Decimal = to_decimal("0.0")
        str_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_price =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_amountexcl =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            l_untergrup = L_untergrup()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, l_ophis.fibukonto, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.lscheinnr, L_ophis.datum, L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.einzelpreis, L_ophis.lief_nr, L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & 
                     (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & 
                     (L_ophis.anzahl != 0) & 
                     # Rd 26/8/2025
                     (not_ ((length(L_ophis.fibukonto) > 8) & 
                                                (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                     ).order_by(L_untergrup.bezeich, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                count_data = count_data + 1

                if utt_bezeich == "":
                    utt_bezeich = l_untergrup.bezeich
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)
        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            l_untergrup = L_untergrup()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, l_ophis.fibukonto, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.lscheinnr, L_ophis.datum, L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.einzelpreis, L_ophis.lief_nr, L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & 
                     (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & 
                     (L_ophis.anzahl != 0) & (L_ophis.lager_nr == store) & 
                    #  (not_ (length(L_ophis.fibukonto) > 8) & (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length(("CANCELLED").lower() ) + 1 - 1, length(L_ophis.fibukonto)) == ("CANCELLED").lower()))
                    # Rd 26/8/2025
                     (not_ ((length(L_ophis.fibukonto) > 8) & 
                                                (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                     ).order_by(L_untergrup.bezeich, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                count_data = count_data + 1

                if utt_bezeich == "":
                    utt_bezeich = l_untergrup.bezeich
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)

        if show_total:

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                str_list.description = "TOTAL SUB-GROUP: " + utt_bezeich
                str_list.qty =  to_decimal(t_anz)
                str_list.inc_qty =  to_decimal(t_anz)
                str_list.amount =  to_decimal(t_amt)
                str_list.warenwert =  to_decimal(t_amt)
                str_list.amountexcl =  to_decimal(t_amountexcl)
                str_list.tax_amount =  to_decimal(t_tax)
                str_list.tot_amt =  to_decimal(t_inv)
                str_list.price =  to_decimal("0")

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                # str_list = Str_list()
                # str_list_data.append(str_list)

                str_list.description = "GRAND TOTAL"
                str_list.qty =  to_decimal(tot_anz)
                str_list.inc_qty =  to_decimal(tot_anz)
                str_list.amount =  to_decimal(tot_amount)
                str_list.warenwert =  to_decimal(tot_amount)
                str_list.amountexcl =  to_decimal(tot_amountexcl)
                str_list.tax_amount =  to_decimal(tot_tax)
                str_list.tot_amt =  to_decimal(tot_amt)
                str_list.price =  to_decimal("0")


        else:
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.description = "TOTAL SUB-GROUP: " + utt_bezeich
            str_list.qty =  to_decimal(tot_anz)
            str_list.inc_qty =  to_decimal(tot_anz)
            str_list.amount =  to_decimal(tot_amount)
            str_list.warenwert =  to_decimal(tot_amount)
            str_list.amountexcl =  to_decimal(tot_amountexcl)
            str_list.tax_amount =  to_decimal(tot_tax)
            str_list.tot_amt =  to_decimal(tot_amt)
            str_list.price =  to_decimal("0")


    def create_list1br():

        nonlocal err_code, str_list_data, supp_nr, long_digit, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, tot_price, counter, loopi, unit_price, lvcarea, l_kredit, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup, gl_acct, l_ophhis, queasy
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        t_price:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        utt_bezeich:string = ""
        t_amountexcl:Decimal = to_decimal("0.0")
        count_data:int = 0
        show_total:bool = True
        amt:Decimal = to_decimal("0.0")
        pure_bundle_unit_price:Decimal = to_decimal("0.0")
        str_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_price =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_amountexcl =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            l_untergrup = L_untergrup()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, l_ophis.fibukonto, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.lscheinnr, L_ophis.datum, L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.einzelpreis, L_ophis.lief_nr, L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & 
                     (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & 
                     (L_ophis.anzahl != 0) & (L_ophis.docu_nr == (from_doc).lower()) & 
                    #  (not_ (length(L_ophis.fibukonto) > 8) & (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length(("CANCELLED").lower() ) + 1 - 1, length(L_ophis.fibukonto)) == ("CANCELLED").lower()))
                    # Rd 26/8/2025
                     (not_ ((length(L_ophis.fibukonto) > 8) & 
                                                (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                     ).order_by(L_untergrup.bezeich, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                count_data = count_data + 1

                if utt_bezeich == "":
                    utt_bezeich = l_untergrup.bezeich
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)
        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            l_untergrup = L_untergrup()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, l_ophis.fibukonto, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.lscheinnr, L_ophis.datum, L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.einzelpreis, L_ophis.lief_nr, L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & 
                     (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & 
                     (L_ophis.anzahl != 0) & (L_ophis.lager_nr == store) & 
                     (L_ophis.docu_nr == (from_doc).lower()) & 
                    #  (not_ (length(L_ophis.fibukonto) > 8) & (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length(("CANCELLED").lower() ) + 1 - 1, length(L_ophis.fibukonto)) == ("CANCELLED").lower()))
                    # Rd 26/8/2025
                     (not_ ((length(L_ophis.fibukonto) > 8) & 
                                                (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                     ).order_by(L_untergrup.bezeich, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                count_data = count_data + 1

                if utt_bezeich == "":
                    utt_bezeich = l_untergrup.bezeich
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)

        if show_total:

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                str_list.description = "TOTAL SUB-GROUP: " + utt_bezeich
                str_list.qty =  to_decimal(t_anz)
                str_list.inc_qty =  to_decimal(t_anz)
                str_list.amount =  to_decimal(t_amt)
                str_list.warenwert =  to_decimal(t_amt)
                str_list.amountexcl =  to_decimal(t_amountexcl)
                str_list.tax_amount =  to_decimal(t_tax)
                str_list.tot_amt =  to_decimal(t_inv)
                str_list.price =  to_decimal("0")

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                # str_list = Str_list()
                # str_list_data.append(str_list)

                str_list.description = "GRAND TOTAL"
                str_list.qty =  to_decimal(tot_anz)
                str_list.inc_qty =  to_decimal(tot_anz)
                str_list.amount =  to_decimal(tot_amount)
                str_list.warenwert =  to_decimal(tot_amount)
                str_list.amountexcl =  to_decimal(tot_amountexcl)
                str_list.tax_amount =  to_decimal(tot_tax)
                str_list.tot_amt =  to_decimal(tot_amt)
                str_list.price =  to_decimal("0")


        else:
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.description = "TOTAL SUB-GROUP: " + utt_bezeich
            str_list.qty =  to_decimal(tot_anz)
            str_list.inc_qty =  to_decimal(tot_anz)
            str_list.amount =  to_decimal(tot_amount)
            str_list.warenwert =  to_decimal(tot_amount)
            str_list.amountexcl =  to_decimal(tot_amountexcl)
            str_list.tax_amount =  to_decimal(tot_tax)
            str_list.tot_amt =  to_decimal(tot_amt)
            str_list.price =  to_decimal("0")


    def create_list11br():

        nonlocal err_code, str_list_data, supp_nr, long_digit, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, tot_price, counter, loopi, unit_price, lvcarea, l_kredit, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup, gl_acct, l_ophhis, queasy
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        t_price:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        utt_bezeich:string = ""
        t_amountexcl:Decimal = to_decimal("0.0")
        count_data:int = 0
        show_total:bool = True
        amt:Decimal = to_decimal("0.0")
        pure_bundle_unit_price:Decimal = to_decimal("0.0")
        str_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_price =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_amountexcl =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            l_untergrup = L_untergrup()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, l_ophis.fibukonto, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.lscheinnr, L_ophis.datum, L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.einzelpreis, L_ophis.lief_nr, L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & 
                     (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & 
                     (L_ophis.anzahl != 0) & (L_ophis.docu_nr == (from_doc).lower()) & 
                    #  (not_ (length(L_ophis.fibukonto) > 8) & (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length(("CANCELLED").lower() ) + 1 - 1, length(L_ophis.fibukonto)) == ("CANCELLED").lower()))
                    # Rd 26/8/2025
                     (not_ ((length(L_ophis.fibukonto) > 8) & 
                                                (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                     ).order_by(L_untergrup.bezeich, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                count_data = count_data + 1

                if utt_bezeich == "":
                    utt_bezeich = l_untergrup.bezeich
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)
        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            l_untergrup = L_untergrup()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, l_ophis.fibukonto, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.lscheinnr, L_ophis.datum, L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.einzelpreis, L_ophis.lief_nr, L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr > 0) & 
                     (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (L_ophis.lager_nr == store) & 
                     (L_ophis.docu_nr == (from_doc).lower()) & 
                    #  (not_ (length(L_ophis.fibukonto) > 8) & (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length(("CANCELLED").lower() ) + 1 - 1, length(L_ophis.fibukonto)) == ("CANCELLED").lower()))
                    # Rd 26/8/2025
                     (not_ ((length(L_ophis.fibukonto) > 8) & 
                                                (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                     ).order_by(L_untergrup.bezeich, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                count_data = count_data + 1

                if utt_bezeich == "":
                    utt_bezeich = l_untergrup.bezeich
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)

        if show_total:

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                str_list.description = "TOTAL SUB-GROUP: " + utt_bezeich
                str_list.qty =  to_decimal(t_anz)
                str_list.inc_qty =  to_decimal(t_anz)
                str_list.amount =  to_decimal(t_amt)
                str_list.warenwert =  to_decimal(t_amt)
                str_list.amountexcl =  to_decimal(t_amountexcl)
                str_list.tax_amount =  to_decimal(t_tax)
                str_list.tot_amt =  to_decimal(t_inv)
                str_list.price =  to_decimal("0")

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                # str_list = Str_list()
                # str_list_data.append(str_list)

                str_list.description = "GRAND TOTAL"
                str_list.qty =  to_decimal(tot_anz)
                str_list.inc_qty =  to_decimal(tot_anz)
                str_list.amount =  to_decimal(tot_amount)
                str_list.warenwert =  to_decimal(tot_amount)
                str_list.amountexcl =  to_decimal(tot_amountexcl)
                str_list.tax_amount =  to_decimal(tot_tax)
                str_list.tot_amt =  to_decimal(tot_amt)
                str_list.price =  to_decimal("0")


        else:
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.description = "TOTAL SUB-GROUP: " + utt_bezeich
            str_list.qty =  to_decimal(tot_anz)
            str_list.inc_qty =  to_decimal(tot_anz)
            str_list.amount =  to_decimal(tot_amount)
            str_list.warenwert =  to_decimal(tot_amount)
            str_list.amountexcl =  to_decimal(tot_amountexcl)
            str_list.tax_amount =  to_decimal(tot_tax)
            str_list.tot_amt =  to_decimal(tot_amt)
            str_list.price =  to_decimal("0")


    def create_list1as():

        nonlocal err_code, str_list_data, supp_nr, long_digit, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, tot_price, counter, loopi, unit_price, lvcarea, l_kredit, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup, gl_acct, l_ophhis, queasy
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        t_price:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        utt_bezeich:string = ""
        t_amountexcl:Decimal = to_decimal("0.0")
        count_data:int = 0
        show_total:bool = True
        amt:Decimal = to_decimal("0.0")
        pure_bundle_unit_price:Decimal = to_decimal("0.0")
        str_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_price =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_amountexcl =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, l_ophis.fibukonto, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid in db_session.query(L_ophis.lscheinnr, L_ophis.datum, L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.einzelpreis, L_ophis.lief_nr, L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr == l_lieferant.lief_nr) & 
                     (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & 
                    #  (not_ (length(L_ophis.fibukonto) > 8) & (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length(("CANCELLED").lower() ) + 1 - 1, length(L_ophis.fibukonto)) == ("CANCELLED").lower()))
                    # Rd 26/8/2025
                     (not_ ((length(L_ophis.fibukonto) > 8) & 
                                                (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                     ).order_by(L_ophis.lscheinnr, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                count_data = count_data + 1

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)
        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, l_ophis.fibukonto, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid in db_session.query(L_ophis.lscheinnr, L_ophis.datum, L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.einzelpreis, L_ophis.lief_nr, L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr == l_lieferant.lief_nr) & 
                     (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (L_ophis.lager_nr == store) & 
                    #  (not_ (length(L_ophis.fibukonto) > 8) & (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length(("CANCELLED").lower() ) + 1 - 1, length(L_ophis.fibukonto)) == ("CANCELLED").lower()))
                    # Rd 26/8/2025
                     (not_ ((length(L_ophis.fibukonto) > 8) & 
                                                (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                     ).order_by(L_ophis.lscheinnr, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                count_data = count_data + 1

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)

        if show_total:

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                str_list.description = "T O T A L"
                str_list.qty =  to_decimal(t_anz)
                str_list.inc_qty =  to_decimal(t_anz)
                str_list.amount =  to_decimal(t_amt)
                str_list.warenwert =  to_decimal(t_amt)
                str_list.amountexcl =  to_decimal(t_amountexcl)
                str_list.tax_amount =  to_decimal(t_tax)
                str_list.tot_amt =  to_decimal(t_inv)
                str_list.price =  to_decimal("0")

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                # str_list = Str_list()
                # str_list_data.append(str_list)

                str_list.description = "GRAND TOTAL"
                str_list.qty =  to_decimal(tot_anz)
                str_list.inc_qty =  to_decimal(tot_anz)
                str_list.amount =  to_decimal(tot_amount)
                str_list.warenwert =  to_decimal(tot_amount)
                str_list.amountexcl =  to_decimal(tot_amountexcl)
                str_list.tax_amount =  to_decimal(tot_tax)
                str_list.tot_amt =  to_decimal(tot_amt)
                str_list.price =  to_decimal("0")


        else:
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.description = "GRAND TOTAL"
            str_list.qty =  to_decimal(tot_anz)
            str_list.inc_qty =  to_decimal(tot_anz)
            str_list.amount =  to_decimal(tot_amount)
            str_list.warenwert =  to_decimal(tot_amount)
            str_list.amountexcl =  to_decimal(tot_amountexcl)
            str_list.tax_amount =  to_decimal(tot_tax)
            str_list.tot_amt =  to_decimal(tot_amt)
            str_list.price =  to_decimal("0")


    def create_list11as():

        nonlocal err_code, str_list_data, supp_nr, long_digit, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, tot_price, counter, loopi, unit_price, lvcarea, l_kredit, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup, gl_acct, l_ophhis, queasy
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        t_price:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        utt_bezeich:string = ""
        t_amountexcl:Decimal = to_decimal("0.0")
        count_data:int = 0
        show_total:bool = True
        amt:Decimal = to_decimal("0.0")
        pure_bundle_unit_price:Decimal = to_decimal("0.0")
        str_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_price =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_amountexcl =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, l_ophis.fibukonto, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid in db_session.query(L_ophis.lscheinnr, L_ophis.datum, L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.einzelpreis, L_ophis.lief_nr, L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr == l_lieferant.lief_nr) & 
                     (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & 
                    #  (not_ (length(L_ophis.fibukonto) > 8) & (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length(("CANCELLED").lower() ) + 1 - 1, length(L_ophis.fibukonto)) == ("CANCELLED").lower()))
                    # Rd 26/8/2025
                     (not_ ((length(L_ophis.fibukonto) > 8) & 
                                                (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                     ).order_by(L_ophis.lscheinnr, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                count_data = count_data + 1

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)
        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, l_ophis.fibukonto, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid in db_session.query(L_ophis.lscheinnr, L_ophis.datum, L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.einzelpreis, L_ophis.lief_nr, L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & 
                     (L_ophis.lief_nr == l_lieferant.lief_nr) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (L_ophis.lager_nr == store) & 
                    #  (not_ (length(L_ophis.fibukonto) > 8) & (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length(("CANCELLED").lower() ) + 1 - 1, length(L_ophis.fibukonto)) == ("CANCELLED").lower()))
                    # Rd 26/8/2025
                     (not_ ((length(L_ophis.fibukonto) > 8) & 
                                                (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                     ).order_by(L_ophis.lscheinnr, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                count_data = count_data + 1

                if lscheinnr == "":
                    lscheinnr = l_ophis.lscheinnr
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)

        if show_total:

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                str_list.description = "T O T A L"
                str_list.qty =  to_decimal(t_anz)
                str_list.inc_qty =  to_decimal(t_anz)
                str_list.amount =  to_decimal(t_amt)
                str_list.warenwert =  to_decimal(t_amt)
                str_list.amountexcl =  to_decimal(t_amountexcl)
                str_list.tax_amount =  to_decimal(t_tax)
                str_list.tot_amt =  to_decimal(t_inv)
                str_list.price =  to_decimal("0")

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                # str_list = Str_list()
                # str_list_data.append(str_list)

                str_list.description = "GRAND TOTAL"
                str_list.qty =  to_decimal(tot_anz)
                str_list.inc_qty =  to_decimal(tot_anz)
                str_list.amount =  to_decimal(tot_amount)
                str_list.warenwert =  to_decimal(tot_amount)
                str_list.amountexcl =  to_decimal(tot_amountexcl)
                str_list.tax_amount =  to_decimal(tot_tax)
                str_list.tot_amt =  to_decimal(tot_amt)
                str_list.price =  to_decimal("0")


        else:
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.description = "GRAND TOTAL"
            str_list.qty =  to_decimal(tot_anz)
            str_list.inc_qty =  to_decimal(tot_anz)
            str_list.amount =  to_decimal(tot_amount)
            str_list.warenwert =  to_decimal(tot_amount)
            str_list.amountexcl =  to_decimal(tot_amountexcl)
            str_list.tax_amount =  to_decimal(tot_tax)
            str_list.tot_amt =  to_decimal(tot_amt)
            str_list.price =  to_decimal("0")


    def create_list1bs():

        nonlocal err_code, str_list_data, supp_nr, long_digit, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, tot_price, counter, loopi, unit_price, lvcarea, l_kredit, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup, gl_acct, l_ophhis, queasy
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        t_price:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        utt_bezeich:string = ""
        t_amountexcl:Decimal = to_decimal("0.0")
        count_data:int = 0
        show_total:bool = True
        amt:Decimal = to_decimal("0.0")
        pure_bundle_unit_price:Decimal = to_decimal("0.0")
        str_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_price =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_amountexcl =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, l_ophis.fibukonto, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.lscheinnr, L_ophis.datum, L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.einzelpreis, L_ophis.lief_nr, L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr == l_lieferant.lief_nr) & 
                     (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & 
                    #  (not_ (length(L_ophis.fibukonto) > 8) & (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length(("CANCELLED").lower() ) + 1 - 1, length(L_ophis.fibukonto)) == ("CANCELLED").lower()))
                    # Rd 26/8/2025
                     (not_ ((length(L_ophis.fibukonto) > 8) & 
                                                (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                     ).order_by(L_untergrup.bezeich, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                count_data = count_data + 1

                if utt_bezeich == "":
                    utt_bezeich = l_untergrup.bezeich
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)
        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, l_ophis.fibukonto, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.lscheinnr, L_ophis.datum, L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.einzelpreis, L_ophis.lief_nr, L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr == l_lieferant.lief_nr) & 
                     (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (L_ophis.lager_nr == store) & 
                    #  (not_ (length(L_ophis.fibukonto) > 8) & (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length(("CANCELLED").lower() ) + 1 - 1, length(L_ophis.fibukonto)) == ("CANCELLED").lower()))
                    # Rd 26/8/2025
                     (not_ ((length(L_ophis.fibukonto) > 8) & 
                                                (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                     ).order_by(L_untergrup.bezeich, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                count_data = count_data + 1

                if utt_bezeich == "":
                    utt_bezeich = l_untergrup.bezeich
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)

        if show_total:

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                str_list.description = "TOTAL SUB-GROUP: " + utt_bezeich
                str_list.qty =  to_decimal(t_anz)
                str_list.inc_qty =  to_decimal(t_anz)
                str_list.amount =  to_decimal(t_amt)
                str_list.warenwert =  to_decimal(t_amt)
                str_list.amountexcl =  to_decimal(t_amountexcl)
                str_list.tax_amount =  to_decimal(t_tax)
                str_list.tot_amt =  to_decimal(t_inv)
                str_list.price =  to_decimal("0")

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                # str_list = Str_list()
                # str_list_data.append(str_list)

                str_list.description = "GRAND TOTAL"
                str_list.qty =  to_decimal(tot_anz)
                str_list.inc_qty =  to_decimal(tot_anz)
                str_list.amount =  to_decimal(tot_amount)
                str_list.warenwert =  to_decimal(tot_amount)
                str_list.amountexcl =  to_decimal(tot_amountexcl)
                str_list.tax_amount =  to_decimal(tot_tax)
                str_list.tot_amt =  to_decimal(tot_amt)
                str_list.price =  to_decimal("0")


        else:
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.description = "TOTAL SUB-GROUP: " + utt_bezeich
            str_list.qty =  to_decimal(tot_anz)
            str_list.inc_qty =  to_decimal(tot_anz)
            str_list.amount =  to_decimal(tot_amount)
            str_list.warenwert =  to_decimal(tot_amount)
            str_list.amountexcl =  to_decimal(tot_amountexcl)
            str_list.tax_amount =  to_decimal(tot_tax)
            str_list.tot_amt =  to_decimal(tot_amt)
            str_list.price =  to_decimal("0")


    def create_list11bs():

        nonlocal err_code, str_list_data, supp_nr, long_digit, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, tot_price, counter, loopi, unit_price, lvcarea, l_kredit, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup, gl_acct, l_ophhis, queasy
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        t_price:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        utt_bezeich:string = ""
        t_amountexcl:Decimal = to_decimal("0.0")
        count_data:int = 0
        show_total:bool = True
        amt:Decimal = to_decimal("0.0")
        pure_bundle_unit_price:Decimal = to_decimal("0.0")
        str_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_price =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_amountexcl =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, l_ophis.fibukonto, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.lscheinnr, L_ophis.datum, L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.einzelpreis, L_ophis.lief_nr, L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr == l_lieferant.lief_nr) & 
                     (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & 
                    #  (not_ (length(L_ophis.fibukonto) > 8) & (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length(("CANCELLED").lower() ) + 1 - 1, length(L_ophis.fibukonto)) == ("CANCELLED").lower()))
                    # Rd 26/8/2025
                     (not_ ((length(L_ophis.fibukonto) > 8) & 
                                                (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                     ).order_by(L_untergrup.bezeich, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                count_data = count_data + 1

                if utt_bezeich == "":
                    utt_bezeich = l_untergrup.bezeich
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)
        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_ophis.lscheinnr, l_ophis.datum, l_ophis.anzahl, l_ophis.artnr, l_ophis.warenwert, l_ophis.docu_nr, l_ophis.lager_nr, l_ophis.einzelpreis, l_ophis.lief_nr, l_ophis.fibukonto, l_ophis._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.lief_artnr, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.lscheinnr, L_ophis.datum, L_ophis.anzahl, L_ophis.artnr, L_ophis.warenwert, L_ophis.docu_nr, L_ophis.lager_nr, L_ophis.einzelpreis, L_ophis.lief_nr, L_ophis.fibukonto, L_ophis._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.lief_artnr, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.lief_nr == l_lieferant.lief_nr) & 
                     (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (L_ophis.lager_nr == store) & 
                    #  (not_ (length(L_ophis.fibukonto) > 8) & (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length(("CANCELLED").lower() ) + 1 - 1, length(L_ophis.fibukonto)) == ("CANCELLED").lower()))
                    # Rd 26/8/2025
                     (not_ ((length(L_ophis.fibukonto) > 8) & 
                                                (substring(L_ophis.fibukonto, length(L_ophis.fibukonto) - length("CANCELLED" ), length(L_ophis.fibukonto)) == "CANCELLED")))
                     ).order_by(L_untergrup.bezeich, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                count_data = count_data + 1

                if utt_bezeich == "":
                    utt_bezeich = l_untergrup.bezeich
                lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt = processing_data_in_loop(sorttype, show_total, lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)

        if show_total:

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                str_list.description = "TOTAL SUB-GROUP: " + utt_bezeich
                str_list.qty =  to_decimal(t_anz)
                str_list.inc_qty =  to_decimal(t_anz)
                str_list.amount =  to_decimal(t_amt)
                str_list.warenwert =  to_decimal(t_amt)
                str_list.amountexcl =  to_decimal(t_amountexcl)
                str_list.tax_amount =  to_decimal(t_tax)
                str_list.tot_amt =  to_decimal(t_inv)
                str_list.price =  to_decimal("0")

            if count_data > 0:
                str_list = Str_list()
                str_list_data.append(str_list)

                # str_list = Str_list()
                # str_list_data.append(str_list)

                str_list.description = "GRAND TOTAL"
                str_list.qty =  to_decimal(tot_anz)
                str_list.inc_qty =  to_decimal(tot_anz)
                str_list.amount =  to_decimal(tot_amount)
                str_list.warenwert =  to_decimal(tot_amount)
                str_list.amountexcl =  to_decimal(tot_amountexcl)
                str_list.tax_amount =  to_decimal(tot_tax)
                str_list.tot_amt =  to_decimal(tot_amt)
                str_list.price =  to_decimal("0")


        else:
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.description = "TOTAL SUB-GROUP: " + utt_bezeich
            str_list.qty =  to_decimal(tot_anz)
            str_list.inc_qty =  to_decimal(tot_anz)
            str_list.amount =  to_decimal(tot_amount)
            str_list.warenwert =  to_decimal(tot_amount)
            str_list.amountexcl =  to_decimal(tot_amountexcl)
            str_list.tax_amount =  to_decimal(tot_tax)
            str_list.tot_amt =  to_decimal(tot_amt)
            str_list.price =  to_decimal("0")


    def convert_fibu(konto:string):

        nonlocal err_code, str_list_data, supp_nr, long_digit, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, tot_price, counter, loopi, unit_price, lvcarea, l_kredit, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup, gl_acct, l_ophhis, queasy
        nonlocal pvilanguage, from_supp, from_doc, sorttype, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        s = ""
        bez = ""
        ch:string = ""
        i:int = 0
        j:int = 0

        def generate_inner_output():
            return (s, bez)


        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, konto)]})

        if not gl_acct:

            return generate_inner_output()
        bez = gl_acct.bezeich

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


    def processing_data_in_loop(sorttype:int, show_total:bool, lief_nr:int, lscheinnr:string, utt_bezeich:string, t_anz:Decimal, t_amt:Decimal, t_tax:Decimal, t_inv:Decimal, t_price:Decimal, t_amountexcl:Decimal, amt:Decimal):

        nonlocal err_code, str_list_data, supp_nr, long_digit, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, tot_price, counter, loopi, unit_price, lvcarea, l_kredit, htparam, l_lieferant, l_ophis, l_artikel, l_untergrup, gl_acct, l_ophhis, queasy
        nonlocal pvilanguage, from_supp, from_doc, from_grp, to_grp, store, all_supp, all_doc, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        def generate_inner_output():
            return (lief_nr, lscheinnr, utt_bezeich, t_anz, t_amt, t_tax, t_inv, t_price, t_amountexcl, amt)


        l_ophhis = get_cache (L_ophhis, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_ophis.lscheinnr)],"datum": [(eq, l_ophis.datum)]})

        if show_total:

            if sorttype == 1:

                if lief_nr != l_lieferant.lief_nr:
                    lief_nr = l_lieferant.lief_nr
                    str_list = Str_list()
                    str_list_data.append(str_list)

                    str_list.description = "T O T A L"
                    str_list.inc_qty =  to_decimal(t_anz)
                    str_list.qty =  to_decimal(t_anz)
                    str_list.amount =  to_decimal(t_amt)
                    str_list.warenwert =  to_decimal(t_amt)
                    str_list.amountexcl =  to_decimal(t_amountexcl)
                    str_list.tax_amount =  to_decimal(t_tax)
                    str_list.tot_amt =  to_decimal(t_inv)
                    str_list.price =  to_decimal("0")
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    t_amountexcl =  to_decimal("0")
                    t_tax =  to_decimal("0")
                    t_inv =  to_decimal("0")
                    t_price =  to_decimal("0")


                    # str_list = Str_list()
                    # str_list_data.append(str_list)


            elif sorttype == 2:

                if lscheinnr != l_ophis.lscheinnr:
                    lscheinnr = l_ophis.lscheinnr
                    str_list = Str_list()
                    str_list_data.append(str_list)

                    str_list.description = "T O T A L"
                    str_list.inc_qty =  to_decimal(t_anz)
                    str_list.qty =  to_decimal(t_anz)
                    str_list.amount =  to_decimal(t_amt)
                    str_list.warenwert =  to_decimal(t_amt)
                    str_list.amountexcl =  to_decimal(t_amountexcl)
                    str_list.tax_amount =  to_decimal(t_tax)
                    str_list.tot_amt =  to_decimal(t_inv)
                    str_list.price =  to_decimal("0")
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    t_amountexcl =  to_decimal("0")
                    t_tax =  to_decimal("0")
                    t_inv =  to_decimal("0")
                    t_price =  to_decimal("0")


                    # str_list = Str_list()
                    # str_list_data.append(str_list)


            elif sorttype == 3:

                if utt_bezeich != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_data.append(str_list)

                    str_list.description = "TOTAL SUB-GROUP: " + utt_bezeich
                    str_list.inc_qty =  to_decimal(t_anz)
                    str_list.qty =  to_decimal(t_anz)
                    str_list.amount =  to_decimal(t_amt)
                    str_list.warenwert =  to_decimal(t_amt)
                    str_list.amountexcl =  to_decimal(t_amountexcl)
                    str_list.tax_amount =  to_decimal(t_tax)
                    str_list.tot_amt =  to_decimal(t_inv)
                    str_list.price =  to_decimal("0")
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    t_amountexcl =  to_decimal("0")
                    t_tax =  to_decimal("0")
                    t_inv =  to_decimal("0")
                    t_price =  to_decimal("0")


                    utt_bezeich = l_untergrup.bezeich
                    str_list = Str_list()
                    str_list_data.append(str_list)

        t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
        tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)

        queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)]})

        if queasy:
            t_amt =  to_decimal(t_amt) + to_decimal((l_ophis.warenwert) + to_decimal((l_ophis.warenwert) * to_decimal((queasy.deci1) / to_decimal(100))) )
            tot_amount =  to_decimal(tot_amount) + to_decimal((l_ophis.warenwert) + to_decimal((l_ophis.warenwert) * to_decimal((queasy.deci1) / to_decimal(100))) )
            t_amountexcl =  to_decimal(t_amountexcl) + to_decimal(l_ophis.warenwert)
            tot_amountexcl =  to_decimal(tot_amountexcl) + to_decimal(l_ophis.warenwert)


        else:
            t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)
            tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)
            t_amountexcl =  to_decimal(t_amountexcl) + to_decimal(l_ophis.warenwert)
            tot_amountexcl =  to_decimal(tot_amountexcl) + to_decimal(l_ophis.warenwert)

        str_list = query(str_list_data, filters=(lambda str_list: str_list.docu_nr == l_ophis.docu_nr and str_list.artnr == l_ophis.artnr and str_list.lager_nr == l_ophis.lager_nr and str_list.lscheinnr == l_ophis.lscheinnr and str_list.epreis == l_ophis.einzelpreis), first=True)

        if str_list:
            str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)
            str_list.inc_qty =  to_decimal(str_list.inc_qty) + to_decimal(l_ophis.anzahl)

            queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)]})

            if queasy:
                str_list.addvat_value =  to_decimal(queasy.deci1)
                str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal((l_ophis.warenwert) + to_decimal((l_ophis.warenwert) * to_decimal((queasy.deci1) / to_decimal(100))) )
                str_list.amountexcl =  to_decimal(str_list.amountexcl) + to_decimal(l_ophis.warenwert)
                str_list.addvat_amount =  to_decimal(str_list.addvat_amount) + to_decimal((l_ophis.warenwert) * to_decimal((queasy.deci1) / to_decimal(100)) )


            else:
                str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_ophis.warenwert)
                str_list.amountexcl =  to_decimal(str_list.amountexcl) + to_decimal(l_ophis.warenwert)


            str_list.amount =  to_decimal(str_list.warenwert)

            taxcode_list = query(taxcode_list_data, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

            if taxcode_list:
                amt =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )
                tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(amt) )

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 336) & (Queasy.char1 == l_ophis.lscheinnr) & (Queasy.number2 == l_ophis.artnr) & (cast(Queasy.char2, Numeric) == l_ophis.einzelpreis)).first()

            if queasy:
                str_list.disc_amount =  to_decimal(str_list.disc_amount) + to_decimal(queasy.deci1) + to_decimal(queasy.deci2)
                str_list.vat_amount =  to_decimal(str_list.vat_amount)
                # str_list.addvat_amount =  to_decimal(str_list.addvat_amount) + to_decimal(to_decimal(queasy.char3) )


        else:
            str_list = Str_list()
            str_list_data.append(str_list)


            if l_ophhis:
                str_list.invoice_nr = l_ophhis.fibukonto
            str_list.lief_nr = l_ophis.lief_nr
            str_list.artnr = l_ophis.artnr
            str_list.lager_nr = l_ophis.lager_nr
            str_list.docu_nr = l_ophis.docu_nr
            str_list.lscheinnr = l_ophis.lscheinnr
            str_list.epreis =  to_decimal(l_ophis.einzelpreis)

            buff_l_kredit = get_cache (L_kredit, {"lscheinnr": [(eq, l_ophis.lscheinnr)]})

            if buff_l_kredit:
                str_list.ap_voucher = buff_l_kredit.rechnr
            else:
                str_list.ap_voucher = 0

            queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)]})

            if queasy:
                str_list.addvat_value =  to_decimal(queasy.deci1)
                str_list.warenwert =  to_decimal(l_ophis.warenwert) + (to_decimal(l_ophis.warenwert) * to_decimal((queasy.deci1) / to_decimal(100)) )
                str_list.amountexcl =  to_decimal(l_ophis.warenwert)
                str_list.addvat_amount = ( to_decimal(l_ophis.warenwert) * to_decimal((queasy.deci1) / to_decimal(100)) )


            else:
                str_list.warenwert =  to_decimal(l_ophis.warenwert)
                str_list.amountexcl =  to_decimal(l_ophis.warenwert)

            queasy = get_cache (Queasy, {"key": [(eq, 335)],"char1": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)]})

            if queasy:
                str_list.serial_number = queasy.char2
                str_list.invoice_date = queasy.date2
            else:
                str_list.serial_number = ""
                str_list.invoice_date = None

            queasy = get_cache (Queasy, {"key": [(eq, 340)],"char1": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)],"deci1": [(eq, l_ophis.einzelpreis)]})

            if queasy:
                str_list.remark_artikel = queasy.char2
            else:
                str_list.remark_artikel = ""

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 336) & (Queasy.char1 == l_ophis.lscheinnr) & (Queasy.number2 == l_ophis.artnr) & (cast(Queasy.char2, Numeric) == l_ophis.einzelpreis)).first()

            if queasy:
                str_list.disc_amount =  to_decimal(queasy.deci1) + to_decimal(queasy.deci2)
                str_list.vat_amount =  to_decimal(queasy.deci3)
                # str_list.addvat_amount =  to_decimal(to_decimal(queasy.char3) )


            str_list.fibu, str_list.fibu_bez = convert_fibu(l_ophis.fibukonto)
            str_list.datum = l_ophis.datum
            str_list.st = l_ophis.lager_nr
            str_list.article = l_artikel.artnr
            str_list.description = l_artikel.bezeich
            str_list.d_unit = l_artikel.traubensorte
            str_list.qty =  to_decimal(l_ophis.anzahl)
            str_list.inc_qty =  to_decimal(l_ophis.anzahl)
            str_list.amount =  to_decimal(l_ophis.warenwert)
            str_list.supplier = l_lieferant.firma
            str_list.tax_code = l_artikel.lief_artnr[2]

            if l_lieferant.plz != " ":

                if matches(l_lieferant.plz,r"*#*"):
                    for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                        if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                            str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                            return generate_inner_output()

            taxcode_list = query(taxcode_list_data, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

            if taxcode_list:
                str_list.tax_amount =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                tot_tax =  to_decimal(tot_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                str_list.tot_amt =  to_decimal(l_ophis.warenwert) + to_decimal(str_list.tax_amount)
                t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )
                tot_amt =  to_decimal(tot_amt) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )

            if l_ophis.docu_nr == l_ophis.lscheinnr:
                str_list.docu_no = translateExtended ("Direct Purchase ", lvcarea, "")
            else:
                str_list.docu_no = l_ophis.docu_nr
            str_list.deliv_no = l_ophis.lscheinnr
            str_list.price =  to_decimal(l_ophis.einzelpreis)
            t_price =  to_decimal(t_price) + to_decimal(str_list.price)


            tot_price =  to_decimal(tot_price) + to_decimal(str_list.price)

        return generate_inner_output()

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