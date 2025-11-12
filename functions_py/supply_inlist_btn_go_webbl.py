#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 25/7/2025
# gitlab: 667
#-----------------------------------------
"""_yusufwijasena_20/10/2025

    TicketID: 01EBC4
        _issue_:    - update from RAGUNG: A92782
"""

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_lieferant, L_kredit, L_artikel, L_op, L_ophdr, Queasy, L_untergrup, Htparam, L_ophis, L_ophhis, Bediener, Gl_acct

from sqlalchemy import cast, Numeric

taxcode_list_data, Taxcode_list = create_model("Taxcode_list", {"taxcode":string, "taxamount":Decimal})


#---- Quick& Dirty-----
# perlu update di additional_functions later
def to_decimal(input_value):
    # Only use this for Python values, NOT SQLAlchemy expressions
    if isinstance(input_value, str) and input_value == "?":
        return Decimal("0")
    try:
        return Decimal(input_value)
    except:
        return Decimal("0")
    

def supply_inlist_btn_go_webbl(pvilanguage:int, last_artnr:int, lieferant_recid:int, l_kredit_recid:int, ap_recid:int, long_digit:bool, show_price:bool, store:int, all_supp:bool, sorttype:int, from_grp:int, to_grp:int, from_date:date, to_date:date, taxcode_list_data:[Taxcode_list]):

    prepare_cache ([L_lieferant, L_kredit, L_artikel, L_op, L_ophdr, Queasy, L_untergrup, Htparam, L_ophis, L_ophhis, Gl_acct])

    first_artnr = 0
    curr_artnr = 0
    last_artnr1 = 0
    unit_price = to_decimal("0.0")
    str_list_data = []
    lvcarea:string = "supply-inlist"
    tot_anz:Decimal = to_decimal("0.0")
    tot_amount:Decimal = to_decimal("0.0")
    tot_amountexcl:Decimal = to_decimal("0.0")
    tot_tax:Decimal = to_decimal("0.0")
    tot_amt:Decimal = to_decimal("0.0")
    i:int = 0
    counter:int = 0
    loopi:int = 0
    l_lieferant = l_kredit = l_artikel = l_op = l_ophdr = queasy = l_untergrup = htparam = l_ophis = l_ophhis = bediener = gl_acct = None

    str_list = taxcode_list = buff_l_kredit = None

    str_list_data, Str_list = create_model("Str_list", {"h_recid":int, "l_recid":int, "lief_nr":int, "billdate":date, "artnr":int, "lager_nr":int, "docu_nr":string, "lscheinnr":string, "invoice_nr":string, "qty":Decimal, "epreis":Decimal, "warenwert":Decimal, "date":date, "st":int, "supplier":string, "article":int, "description":string, "d_unit":string, "m_unit":string, "price":Decimal, "inc_qty":Decimal, "amount":Decimal, "docu_no":string, "deliv_note":string, "id":string, "fibu":string, "gstid":string, "tax_code":string, "tax_amount":Decimal, "tot_amt":Decimal, "desc1":string, "fibu_bez":string, "pos":int, "addvat_value":Decimal, "amountexcl":Decimal, "serial_number":string, "invoice_date":date, "remark_artikel":string, "ap_voucher":int, "disc_amount":Decimal, "addvat_amount":Decimal, "disc_amount2":Decimal, "vat_amount":Decimal, "direct_flag":bool}, {"lscheinnr": ""})

    Buff_l_kredit = create_buffer("Buff_l_kredit",L_kredit)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_data, lvcarea, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, queasy, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal pvilanguage, last_artnr, lieferant_recid, l_kredit_recid, ap_recid, long_digit, show_price, store, all_supp, sorttype, from_grp, to_grp, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        return {"first_artnr": first_artnr, "curr_artnr": curr_artnr, "last_artnr1": last_artnr1, "unit_price": unit_price, "str-list": str_list_data}

    def create_list11():

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_data, lvcarea, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, queasy, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal pvilanguage, last_artnr, lieferant_recid, l_kredit_recid, ap_recid, long_digit, show_price, store, all_supp, sorttype, from_grp, to_grp, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        t_amountexcl:Decimal = to_decimal("0.0")
        str_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_amountexcl =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_op.lscheinnr, l_op.datum, l_op.anzahl, l_op.artnr, l_op.warenwert, l_op.docu_nr, l_op.lager_nr, l_op.einzelpreis, l_op._recid, l_op.lief_nr, l_op.pos, l_op.stornogrund, l_op.fuellflag, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.masseinheit, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.anzahl, L_op.artnr, L_op.warenwert, L_op.docu_nr, L_op.lager_nr, L_op.einzelpreis, L_op._recid, L_op.lief_nr, L_op.pos, L_op.stornogrund, L_op.fuellflag, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.masseinheit, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr > 0) & (L_op.loeschflag <= 1) & (L_op.op_art == 1) & (L_op.anzahl != 0)).order_by(L_lieferant.firma, L_op.datum, L_artikel.bezeich).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                t_anz, t_amt, t_amountexcl, t_tax, t_inv, lief_nr = assign_create_list11(t_anz, t_amt, t_amountexcl, t_tax, t_inv, lief_nr)
        else:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_op.lscheinnr, l_op.datum, l_op.anzahl, l_op.artnr, l_op.warenwert, l_op.docu_nr, l_op.lager_nr, l_op.einzelpreis, l_op._recid, l_op.lief_nr, l_op.pos, l_op.stornogrund, l_op.fuellflag, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.masseinheit, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.anzahl, L_op.artnr, L_op.warenwert, L_op.docu_nr, L_op.lager_nr, L_op.einzelpreis, L_op._recid, L_op.lief_nr, L_op.pos, L_op.stornogrund, L_op.fuellflag, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.masseinheit, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr > 0) & (L_op.loeschflag <= 1) & (L_op.op_art == 1) & (L_op.lager_nr == store) & (L_op.anzahl != 0)).order_by(L_lieferant.firma, L_op.datum, L_artikel.bezeich).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                t_anz, t_amt, t_amountexcl, t_tax, t_inv, lief_nr = assign_create_list11(t_anz, t_amt, t_amountexcl, t_tax, t_inv, lief_nr)
        t_anz, t_amt, t_amountexcl, t_tax, t_inv = create_hislist(t_anz, t_amt, t_amountexcl, t_tax, t_inv)
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


        str_list = Str_list()
        str_list_data.append(str_list)

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


    def assign_create_list11(t_anz:Decimal, t_amt:Decimal, t_amountexcl:Decimal, t_tax:Decimal, t_inv:Decimal, lief_nr:int):

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_data, lvcarea, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, queasy, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal pvilanguage, last_artnr, lieferant_recid, l_kredit_recid, ap_recid, long_digit, show_price, store, all_supp, sorttype, from_grp, to_grp, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        amt:Decimal = to_decimal("0.0")

        def generate_inner_output():
            return (t_anz, t_amt, t_amountexcl, t_tax, t_inv, lief_nr)


        l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})

        if lief_nr == 0:
            lief_nr = l_lieferant.lief_nr

        if lief_nr != l_lieferant.lief_nr:
            lief_nr = l_lieferant.lief_nr
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
            t_anz =  to_decimal("0")
            t_amt =  to_decimal("0")
            t_amountexcl =  to_decimal("0")
            t_tax =  to_decimal("0")
            t_inv =  to_decimal("0")


            str_list = Str_list()
            str_list_data.append(str_list)

        t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)

        if show_price:

            queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

            if queasy:
                t_amt =  to_decimal(t_amt) + to_decimal((l_op.warenwert) + to_decimal((l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100))) )
                tot_amount =  to_decimal(tot_amount) + to_decimal((l_op.warenwert) + to_decimal((l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100))) )
                t_amountexcl =  to_decimal(t_amountexcl) + to_decimal(l_op.warenwert)
                tot_amountexcl =  to_decimal(tot_amountexcl) + to_decimal(l_op.warenwert)


            else:
                t_amt =  to_decimal(t_amt) + to_decimal(l_op.warenwert)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                t_amountexcl =  to_decimal(t_amountexcl) + to_decimal(l_op.warenwert)
                tot_amountexcl =  to_decimal(tot_amountexcl) + to_decimal(l_op.warenwert)


        tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

        if show_price:
            # unit_price =  to_decimal(l_op.einzelpreis)
            unit_price = ( to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl))
            unit_price = to_decimal(round(unit_price , 2)) # RAGUNG: A92782

        str_list = query(str_list_data, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis), first=True)

        if str_list:
            str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

            if show_price:

                queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

                if queasy:
                    str_list.addvat_value =  to_decimal(queasy.deci1)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal((l_op.warenwert) + to_decimal((l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100))) )
                    str_list.amountexcl =  to_decimal(str_list.amountexcl) + to_decimal(l_op.warenwert)
                    str_list.addvat_amount =  to_decimal(str_list.addvat_amount) + to_decimal((l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100)) )


                else:
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.amountexcl =  to_decimal(str_list.amountexcl) + to_decimal(l_op.warenwert)


            str_list.inc_qty =  to_decimal(str_list.qty)
            str_list.amount =  to_decimal(str_list.warenwert)

            taxcode_list = query(taxcode_list_data, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

            if taxcode_list:
                amt =  to_decimal(l_op.warenwert) * to_decimal(taxcode_list.taxamount)
                str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                t_tax =  to_decimal(t_tax) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                tot_tax =  to_decimal(tot_tax) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_op.warenwert) + to_decimal(amt) )
                t_inv =  to_decimal(t_inv) + to_decimal((l_op.warenwert) + to_decimal(amt) )
                tot_amt =  to_decimal(tot_amt) + to_decimal((l_op.warenwert) + to_decimal(amt) )

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 336) & (Queasy.char1 == l_op.lscheinnr) & (Queasy.number2 == l_op.artnr) & (cast(Queasy.char2, Numeric) == l_op.einzelpreis) & (Queasy.number1 == cast(l_op._recid, Numeric))).first()

            if queasy:
                str_list.disc_amount =  to_decimal(str_list.disc_amount) + to_decimal(queasy.deci1) + to_decimal(queasy.deci2)
                str_list.vat_amount =  to_decimal(str_list.vat_amount)
                # str_list.addvat_amount =  to_decimal(str_list.addvat_amount) + to_decimal(to_decimal(queasy.char3) )

        else:
            str_list = Str_list()
            str_list_data.append(str_list)

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
            str_list.qty =  to_decimal(l_op.anzahl)
            str_list.epreis =  to_decimal(l_op.einzelpreis)
            str_list.pos = l_op.pos

            buff_l_kredit = get_cache (L_kredit, {"lscheinnr": [(eq, l_op.lscheinnr)]})

            if buff_l_kredit:
                str_list.ap_voucher = buff_l_kredit.rechnr
            else:
                str_list.ap_voucher = 0

            if show_price:

                queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

                if queasy:
                    str_list.addvat_value =  to_decimal(queasy.deci1)
                    str_list.warenwert =  to_decimal(l_op.warenwert) + (to_decimal(l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100)) )
                    str_list.amountexcl =  to_decimal(l_op.warenwert)
                    str_list.addvat_amount = ( to_decimal(l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100)) )


                else:
                    str_list.warenwert =  to_decimal(l_op.warenwert)
                    str_list.amountexcl =  to_decimal(l_op.warenwert)

            queasy = get_cache (Queasy, {"key": [(eq, 335)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

            if queasy:
                str_list.serial_number = queasy.char2
                str_list.invoice_date = queasy.date2
            else:
                str_list.serial_number = ""
                str_list.invoice_date = None

            queasy = get_cache (Queasy, {"key": [(eq, 340)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)],"deci1": [(eq, l_op.einzelpreis)]})

            if queasy:
                str_list.remark_artikel = queasy.char2
            else:
                str_list.remark_artikel = ""

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 336) & (Queasy.char1 == l_op.lscheinnr) & (Queasy.number2 == l_op.artnr) & (cast(Queasy.char2, Numeric) == l_op.einzelpreis) & (Queasy.number1 == cast(l_op._recid, Numeric))).first()

            if queasy:
                str_list.disc_amount =  to_decimal(queasy.deci1) + to_decimal(queasy.deci2)
                str_list.vat_amount =  to_decimal(queasy.deci3)


            str_list.fibu, str_list.fibu_bez = convert_fibu(l_op.stornogrund)
            str_list.date = l_op.datum
            str_list.st = l_op.lager_nr
            str_list.article = l_artikel.artnr
            str_list.description = l_artikel.bezeich
            str_list.d_unit = l_artikel.traubensorte
            str_list.m_unit = l_artikel.masseinheit
            str_list.inc_qty =  to_decimal(l_op.anzahl)
            str_list.amount =  to_decimal(str_list.warenwert)
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
                str_list.tax_amount =  to_decimal(l_op.warenwert) * to_decimal(taxcode_list.taxamount)
                t_tax =  to_decimal(t_tax) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                tot_tax =  to_decimal(tot_tax) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                str_list.tot_amt =  to_decimal(l_op.warenwert) + to_decimal(str_list.tax_amount)
                t_inv =  to_decimal(t_inv) + to_decimal((l_op.warenwert) + to_decimal(str_list.tax_amount) )
                tot_amt =  to_decimal(tot_amt) + to_decimal((l_op.warenwert) + to_decimal(str_list.tax_amount) )

            if l_op.docu_nr == l_op.lscheinnr:
                str_list.direct_flag = True
                str_list.docu_no = translateExtended ("Direct Purchase ", lvcarea, "")


            else:
                str_list.docu_no = l_op.docu_nr
            str_list.deliv_note = l_op.lscheinnr
            str_list.price =  to_decimal(unit_price)

        return generate_inner_output()


    def create_list11a():

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_data, lvcarea, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, queasy, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal pvilanguage, last_artnr, lieferant_recid, l_kredit_recid, ap_recid, long_digit, show_price, store, all_supp, sorttype, from_grp, to_grp, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        lscheinnr:string = ""
        t_amountexcl:Decimal = to_decimal("0.0")
        str_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_amountexcl =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_op.lscheinnr, l_op.datum, l_op.anzahl, l_op.artnr, l_op.warenwert, l_op.docu_nr, l_op.lager_nr, l_op.einzelpreis, l_op._recid, l_op.lief_nr, l_op.pos, l_op.stornogrund, l_op.fuellflag, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.masseinheit, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.anzahl, L_op.artnr, L_op.warenwert, L_op.docu_nr, L_op.lager_nr, L_op.einzelpreis, L_op._recid, L_op.lief_nr, L_op.pos, L_op.stornogrund, L_op.fuellflag, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.masseinheit, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr > 0) & (L_op.loeschflag <= 1) & (L_op.op_art == 1) & (L_op.anzahl != 0)).order_by(L_op.datum, L_op.lscheinnr, L_artikel.bezeich).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                t_anz, t_amt, t_tax, t_inv, lscheinnr, t_amountexcl = assign_create_list11a(t_anz, t_amt, t_tax, t_inv, lscheinnr, t_amountexcl)
        else:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_op.lscheinnr, l_op.datum, l_op.anzahl, l_op.artnr, l_op.warenwert, l_op.docu_nr, l_op.lager_nr, l_op.einzelpreis, l_op._recid, l_op.lief_nr, l_op.pos, l_op.stornogrund, l_op.fuellflag, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.masseinheit, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.anzahl, L_op.artnr, L_op.warenwert, L_op.docu_nr, L_op.lager_nr, L_op.einzelpreis, L_op._recid, L_op.lief_nr, L_op.pos, L_op.stornogrund, L_op.fuellflag, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.masseinheit, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr > 0) & (L_op.loeschflag <= 1) & (L_op.op_art == 1) & (L_op.anzahl != 0) & (L_op.lager_nr == store)).order_by(L_op.datum, L_op.lscheinnr, L_artikel.bezeich).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                t_anz, t_amt, t_tax, t_inv, lscheinnr, t_amountexcl = assign_create_list11a(t_anz, t_amt, t_tax, t_inv, lscheinnr, t_amountexcl)
        t_anz, t_amt, t_tax, t_inv, t_amountexcl = create_hislist(t_anz, t_amt, t_tax, t_inv, t_amountexcl)
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


        str_list = Str_list()
        str_list_data.append(str_list)

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


    def assign_create_list11a(t_anz:Decimal, t_amt:Decimal, t_tax:Decimal, t_inv:Decimal, lscheinnr:string, t_amountexcl:Decimal):

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_data, lvcarea, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, queasy, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal pvilanguage, last_artnr, lieferant_recid, l_kredit_recid, ap_recid, long_digit, show_price, store, all_supp, sorttype, from_grp, to_grp, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        amt:Decimal = to_decimal("0.0")

        def generate_inner_output():
            return (t_anz, t_amt, t_tax, t_inv, lscheinnr, t_amountexcl)


        l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})

        if lscheinnr == "":
            lscheinnr = l_op.lscheinnr

        if lscheinnr != l_op.lscheinnr:
            lscheinnr = l_op.lscheinnr
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
            t_anz =  to_decimal("0")
            t_amt =  to_decimal("0")
            t_amountexcl =  to_decimal("0")
            t_tax =  to_decimal("0")
            t_inv =  to_decimal("0")


            str_list = Str_list()
            str_list_data.append(str_list)

        t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)

        if show_price:

            queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

            if queasy:
                t_amt =  to_decimal(t_amt) + to_decimal((l_op.warenwert) + to_decimal((l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100))) )
                tot_amount =  to_decimal(tot_amount) + to_decimal((l_op.warenwert) + to_decimal((l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100))) )
                t_amountexcl =  to_decimal(t_amountexcl) + to_decimal(l_op.warenwert)
                tot_amountexcl =  to_decimal(tot_amountexcl) + to_decimal(l_op.warenwert)


            else:
                t_amt =  to_decimal(t_amt) + to_decimal(l_op.warenwert)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                t_amountexcl =  to_decimal(t_amountexcl) + to_decimal(l_op.warenwert)
                tot_amountexcl =  to_decimal(tot_amountexcl) + to_decimal(l_op.warenwert)


        tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

        if show_price:
            # unit_price =  to_decimal(l_op.einzelpreis)
            unit_price = ( to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl))
            unit_price = to_decimal(round(unit_price , 2)) # RAGUNG: A92782

        str_list = query(str_list_data, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis and str_list.billdate == l_op.datum), first=True)

        if str_list:
            str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

            if show_price:

                queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

                if queasy:
                    str_list.addvat_value =  to_decimal(queasy.deci1)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal((l_op.warenwert) + to_decimal((l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100))) )
                    str_list.amountexcl =  to_decimal(str_list.amountexcl) + to_decimal(l_op.warenwert)
                    str_list.addvat_amount =  to_decimal(str_list.addvat_amount) + to_decimal((l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100)) )


                else:
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.amountexcl =  to_decimal(str_list.amountexcl) + to_decimal(l_op.warenwert)


            str_list.inc_qty =  to_decimal(str_list.qty)
            str_list.amount =  to_decimal(str_list.warenwert)
            str_list.amountexcl =  to_decimal(str_list.amountexcl)

            taxcode_list = query(taxcode_list_data, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

            if taxcode_list:
                amt =  to_decimal(l_op.warenwert) * to_decimal(taxcode_list.taxamount)
                str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                t_tax =  to_decimal(t_tax) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                tot_tax =  to_decimal(tot_tax) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_op.warenwert) + to_decimal(amt) )
                t_inv =  to_decimal(t_inv) + to_decimal((l_op.warenwert) + to_decimal(amt) )
                tot_amt =  to_decimal(tot_amt) + to_decimal((l_op.warenwert) + to_decimal(amt) )

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 336) & (Queasy.char1 == l_op.lscheinnr) & (Queasy.number2 == l_op.artnr) & (cast(Queasy.char2, Numeric) == l_op.einzelpreis) & (Queasy.number1 == cast(l_op._recid, Numeric))).first()

            if queasy:
                str_list.disc_amount =  to_decimal(str_list.disc_amount) + to_decimal(queasy.deci1) + to_decimal(queasy.deci2)
                str_list.vat_amount =  to_decimal(str_list.vat_amount)
                # str_list.addvat_amount =  to_decimal(str_list.addvat_amount) + to_decimal(to_decimal(queasy.char3) )

        else:
            str_list = Str_list()
            str_list_data.append(str_list)

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
            str_list.qty =  to_decimal(l_op.anzahl)
            str_list.epreis =  to_decimal(l_op.einzelpreis)
            str_list.pos = l_op.pos

            buff_l_kredit = get_cache (L_kredit, {"lscheinnr": [(eq, l_op.lscheinnr)]})

            if buff_l_kredit:
                str_list.ap_voucher = buff_l_kredit.rechnr
            else:
                str_list.ap_voucher = 0

            if show_price:

                queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

                if queasy:
                    str_list.addvat_value =  to_decimal(queasy.deci1)
                    str_list.warenwert =  to_decimal(l_op.warenwert) + (to_decimal(l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100)) )
                    str_list.amountexcl =  to_decimal(l_op.warenwert)
                    str_list.addvat_amount = ( to_decimal(l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100)) )


                else:
                    str_list.warenwert =  to_decimal(l_op.warenwert)
                    str_list.amountexcl =  to_decimal(l_op.warenwert)

            queasy = get_cache (Queasy, {"key": [(eq, 335)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

            if queasy:
                str_list.serial_number = queasy.char2
                str_list.invoice_date = queasy.date2
            else:
                str_list.serial_number = ""
                str_list.invoice_date = None

            queasy = get_cache (Queasy, {"key": [(eq, 340)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)],"deci1": [(eq, l_op.einzelpreis)]})

            if queasy:
                str_list.remark_artikel = queasy.char2
            else:
                str_list.remark_artikel = ""

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 336) & (Queasy.char1 == l_op.lscheinnr) & (Queasy.number2 == l_op.artnr) & (cast(Queasy.char2, Numeric) == l_op.einzelpreis) & (Queasy.number1 == cast(l_op._recid, Numeric))).first()

            if queasy:
                str_list.disc_amount =  to_decimal(queasy.deci1) + to_decimal(queasy.deci2)
                str_list.vat_amount =  to_decimal(queasy.deci3)
                # str_list.addvat_amount =  to_decimal(to_decimal(queasy.char3) )

            str_list.fibu, str_list.fibu_bez = convert_fibu(l_op.stornogrund)
            str_list.date = l_op.datum
            str_list.st = l_op.lager_nr
            str_list.article = l_artikel.artnr
            str_list.description = l_artikel.bezeich
            str_list.d_unit = l_artikel.traubensorte
            str_list.m_unit = l_artikel.masseinheit # RAGUNG: A92782
            str_list.inc_qty =  to_decimal(l_op.anzahl)
            str_list.amount =  to_decimal(str_list.warenwert)
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
                str_list.tax_amount =  to_decimal(l_op.warenwert) * to_decimal(taxcode_list.taxamount)
                t_tax =  to_decimal(t_tax) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                tot_tax =  to_decimal(tot_tax) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                str_list.tot_amt =  to_decimal(l_op.warenwert) + to_decimal(str_list.tax_amount)
                t_inv =  to_decimal(t_inv) + to_decimal((l_op.warenwert) + to_decimal(str_list.tax_amount) )
                tot_amt =  to_decimal(tot_amt) + to_decimal((l_op.warenwert) + to_decimal(str_list.tax_amount) )

            if l_op.docu_nr == l_op.lscheinnr:
                str_list.direct_flag = True
                str_list.docu_no = translateExtended ("Direct Purchase ", lvcarea, "")


            else:
                str_list.docu_no = l_op.docu_nr
            str_list.deliv_note = l_op.lscheinnr
            str_list.price =  to_decimal(unit_price)

        return generate_inner_output()


    def create_list11b():

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_data, lvcarea, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, queasy, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal pvilanguage, last_artnr, lieferant_recid, l_kredit_recid, ap_recid, long_digit, show_price, store, all_supp, sorttype, from_grp, to_grp, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        t_amountexcl:Decimal = to_decimal("0.0")
        str_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_amountexcl =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            l_lieferant = L_lieferant()
            for l_op.lscheinnr, l_op.datum, l_op.anzahl, l_op.artnr, l_op.warenwert, l_op.docu_nr, l_op.lager_nr, l_op.einzelpreis, l_op._recid, l_op.lief_nr, l_op.pos, l_op.stornogrund, l_op.fuellflag, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.masseinheit, l_artikel.lief_artnr, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.anzahl, L_op.artnr, L_op.warenwert, L_op.docu_nr, L_op.lager_nr, L_op.einzelpreis, L_op._recid, L_op.lief_nr, L_op.pos, L_op.stornogrund, L_op.fuellflag, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.masseinheit, L_artikel.lief_artnr, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr > 0) & (L_op.loeschflag <= 1) & (L_op.anzahl != 0) & (L_op.op_art == 1)).order_by(L_untergrup.bezeich, L_artikel.bezeich, L_op.datum).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                t_anz, t_amt, t_tax, t_inv, lscheinnr, t_amountexcl = assign_create_list11b(t_anz, t_amt, t_tax, t_inv, lscheinnr, t_amountexcl)
        else:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            l_lieferant = L_lieferant()
            for l_op.lscheinnr, l_op.datum, l_op.anzahl, l_op.artnr, l_op.warenwert, l_op.docu_nr, l_op.lager_nr, l_op.einzelpreis, l_op._recid, l_op.lief_nr, l_op.pos, l_op.stornogrund, l_op.fuellflag, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.masseinheit, l_artikel.lief_artnr, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.anzahl, L_op.artnr, L_op.warenwert, L_op.docu_nr, L_op.lager_nr, L_op.einzelpreis, L_op._recid, L_op.lief_nr, L_op.pos, L_op.stornogrund, L_op.fuellflag, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.masseinheit, L_artikel.lief_artnr, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr > 0) & (L_op.anzahl != 0) & (L_op.loeschflag <= 1) & (L_op.op_art == 1) & (L_op.lager_nr == store)).order_by(L_untergrup.bezeich, L_op.datum, L_artikel.bezeich).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                t_anz, t_amt, t_tax, t_inv, lscheinnr, t_amountexcl = assign_create_list11b(t_anz, t_amt, t_tax, t_inv, lscheinnr, t_amountexcl)
        t_anz, t_amt, t_tax, t_inv, t_amountexcl = create_hislist(t_anz, t_amt, t_tax, t_inv, t_amountexcl)
        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.description = lscheinnr
        str_list.qty =  to_decimal(t_anz)
        str_list.inc_qty =  to_decimal(t_anz)
        str_list.amount =  to_decimal(t_amt)
        str_list.warenwert =  to_decimal(t_amt)
        str_list.amountexcl =  to_decimal(t_amountexcl)
        str_list.tax_amount =  to_decimal(t_tax)
        str_list.tot_amt =  to_decimal(t_inv)
        str_list.supplier = "T O T A L"


        str_list = Str_list()
        str_list_data.append(str_list)

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


    def assign_create_list11b(t_anz:Decimal, t_amt:Decimal, t_tax:Decimal, t_inv:Decimal, lscheinnr:string, t_amountexcl:Decimal):

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_data, lvcarea, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, queasy, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal pvilanguage, last_artnr, lieferant_recid, l_kredit_recid, ap_recid, long_digit, show_price, store, all_supp, sorttype, from_grp, to_grp, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        amt:Decimal = to_decimal("0.0")

        def generate_inner_output():
            return (t_anz, t_amt, t_tax, t_inv, lscheinnr, t_amountexcl)


        l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})

        if lscheinnr == "":
            lscheinnr = l_untergrup.bezeich

        if lscheinnr != l_untergrup.bezeich:
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.description = lscheinnr
            str_list.qty =  to_decimal(t_anz)
            str_list.inc_qty =  to_decimal(t_anz)
            str_list.amount =  to_decimal(t_amt)
            str_list.warenwert =  to_decimal(t_amt)
            str_list.amountexcl =  to_decimal(t_amountexcl)
            str_list.supplier = "T O T A L"
            str_list.tax_amount =  to_decimal(t_tax)
            str_list.tot_amt =  to_decimal(t_inv)


            lscheinnr = l_untergrup.bezeich
            t_anz =  to_decimal("0")
            t_amt =  to_decimal("0")
            t_amountexcl =  to_decimal("0")
            t_tax =  to_decimal("0")
            t_inv =  to_decimal("0")
            str_list = Str_list()
            str_list_data.append(str_list)

        t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)

        if show_price:

            queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

            if queasy:
                t_amt =  to_decimal(t_amt) + to_decimal((l_op.warenwert) + to_decimal((l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100))) )
                tot_amount =  to_decimal(tot_amount) + to_decimal((l_op.warenwert) + to_decimal((l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100))) )
                t_amountexcl =  to_decimal(t_amountexcl) + to_decimal(l_op.warenwert)
                tot_amountexcl =  to_decimal(tot_amountexcl) + to_decimal(l_op.warenwert)


            else:
                t_amt =  to_decimal(t_amt) + to_decimal(l_op.warenwert)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                t_amountexcl =  to_decimal(t_amountexcl) + to_decimal(l_op.warenwert)
                tot_amountexcl =  to_decimal(tot_amountexcl) + to_decimal(l_op.warenwert)


        tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

        if show_price:
            # unit_price =  to_decimal(l_op.einzelpreis)
            unit_price = ( to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl))
            unit_price = to_decimal(round(unit_price , 2)) # RAGUNG: A92782

        str_list = query(str_list_data, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

        if str_list:
            str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

            if show_price:

                queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

                if queasy:
                    str_list.addvat_value =  to_decimal(queasy.deci1)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal((l_op.warenwert) + to_decimal((l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100))) )
                    str_list.amountexcl =  to_decimal(str_list.amountexcl) + to_decimal(l_op.warenwert)
                    str_list.addvat_amount =  to_decimal(str_list.addvat_amount) + to_decimal((l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100)) )


                else:
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.amountexcl =  to_decimal(str_list.amountexcl) + to_decimal(l_op.warenwert)


            str_list.inc_qty =  to_decimal(str_list.qty)
            str_list.amount =  to_decimal(str_list.warenwert)

            taxcode_list = query(taxcode_list_data, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

            if taxcode_list:
                amt =  to_decimal(l_op.warenwert) * to_decimal(taxcode_list.taxamount)
                str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                t_tax =  to_decimal(t_tax) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                tot_tax =  to_decimal(tot_tax) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_op.warenwert) + to_decimal(amt) )
                t_inv =  to_decimal(t_inv) + to_decimal((l_op.warenwert) + to_decimal(amt) )
                tot_amt =  to_decimal(tot_amt) + to_decimal((l_op.warenwert) + to_decimal(amt) )

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 336) & (Queasy.char1 == l_op.lscheinnr) & (Queasy.number2 == l_op.artnr) & (cast(Queasy.char2, Numeric) == l_op.einzelpreis) & (Queasy.number1 == cast(l_op._recid, Numeric))).first()

            if queasy:
                str_list.disc_amount =  to_decimal(str_list.disc_amount) + to_decimal(queasy.deci1) + to_decimal(queasy.deci2)
                str_list.vat_amount =  to_decimal(str_list.vat_amount)
                # str_list.addvat_amount =  to_decimal(str_list.addvat_amount) + to_decimal(to_decimal(queasy.char3) )

        else:
            str_list = Str_list()
            str_list_data.append(str_list)

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
            str_list.qty =  to_decimal(l_op.anzahl)
            str_list.epreis =  to_decimal(l_op.einzelpreis)
            str_list.pos = l_op.pos

            buff_l_kredit = get_cache (L_kredit, {"lscheinnr": [(eq, l_op.lscheinnr)]})

            if buff_l_kredit:
                str_list.ap_voucher = buff_l_kredit.rechnr
            else:
                str_list.ap_voucher = 0

            if show_price:

                queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

                if queasy:
                    str_list.addvat_value =  to_decimal(queasy.deci1)
                    str_list.warenwert = ( to_decimal(l_op.warenwert) + (to_decimal(l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100))) )
                    str_list.amountexcl =  to_decimal(l_op.warenwert)
                    str_list.addvat_amount = ( to_decimal(l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100)) )


                else:
                    str_list.warenwert =  to_decimal(l_op.warenwert)
                    str_list.amountexcl =  to_decimal(l_op.warenwert)

            queasy = get_cache (Queasy, {"key": [(eq, 335)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

            if queasy:
                str_list.serial_number = queasy.char2
                str_list.invoice_date = queasy.date2
            else:
                str_list.serial_number = ""
                str_list.invoice_date = None

            queasy = get_cache (Queasy, {"key": [(eq, 340)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)],"deci1": [(eq, l_op.einzelpreis)]})

            if queasy:
                str_list.remark_artikel = queasy.char2
            else:
                str_list.remark_artikel = ""

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 336) & (Queasy.char1 == l_op.lscheinnr) & (Queasy.number2 == l_op.artnr) & (cast(Queasy.char2, Numeric) == l_op.einzelpreis) & (Queasy.number1 == cast(l_op._recid, Numeric))).first()

            if queasy:
                str_list.disc_amount =  to_decimal(queasy.deci1) + to_decimal(queasy.deci2)
                str_list.vat_amount =  to_decimal(queasy.deci3)
                # str_list.addvat_amount =  to_decimal(to_decimal(queasy.char3) )

            str_list.fibu, str_list.fibu_bez = convert_fibu(l_op.stornogrund)
            str_list.date = l_op.datum
            str_list.st = l_op.lager_nr
            str_list.article = l_artikel.artnr
            str_list.description = l_artikel.bezeich
            str_list.d_unit = l_artikel.traubensorte
            str_list.m_unit = l_artikel.masseinheit # RAGUNG: A92782
            str_list.inc_qty =  to_decimal(l_op.anzahl)
            str_list.amount =  to_decimal(str_list.warenwert)
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
                str_list.tax_amount =  to_decimal(l_op.warenwert) * to_decimal(taxcode_list.taxamount)
                t_tax =  to_decimal(t_tax) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                tot_tax =  to_decimal(tot_tax) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                str_list.tot_amt =  to_decimal(l_op.warenwert) + to_decimal(str_list.tax_amount)
                t_inv =  to_decimal(t_inv) + to_decimal((l_op.warenwert) + to_decimal(str_list.tax_amount) )
                tot_amt =  to_decimal(tot_amt) + to_decimal((l_op.warenwert) + to_decimal(str_list.tax_amount) )

            if l_op.docu_nr == l_op.lscheinnr:
                str_list.direct_flag = True
                str_list.docu_no = translateExtended ("Direct Purchase ", lvcarea, "")


            else:
                str_list.docu_no = l_op.docu_nr
            str_list.deliv_note = l_op.lscheinnr
            str_list.price =  to_decimal(unit_price)

        return generate_inner_output()


    def create_hislist(t_anz:Decimal, t_amt:Decimal, t_amountexcl:Decimal, t_tax:Decimal, t_inv:Decimal):

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_data, lvcarea, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, queasy, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal pvilanguage, last_artnr, lieferant_recid, l_kredit_recid, ap_recid, long_digit, show_price, store, all_supp, sorttype, from_grp, to_grp, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        close_date:date = None
        close_date2:date = None

        def generate_inner_output():
            return (t_anz, t_amt, t_amountexcl, t_tax, t_inv)


        htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})

        if htparam:
            close_date = htparam.fdate

        htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})

        if htparam:
            close_date2 = htparam.fdate

        if ap_recid == 0:

            return generate_inner_output()

        if from_date != to_date:

            return generate_inner_output()

        if close_date < close_date2:
            close_date = close_date2
        close_date = date_mdy(get_month(close_date) , 1, get_year(close_date))

        if to_date >= close_date:

            return generate_inner_output()

        for l_ophis in db_session.query(L_ophis).filter(
                 (L_ophis.docu_nr == l_kredit.name) & (L_ophis.lscheinnr == l_kredit.lscheinnr) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (L_ophis.datum == to_date)).order_by(L_ophis._recid).all():
            t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
            t_amt =  to_decimal(t_amt) + to_decimal(l_ophis.warenwert)

            l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_ophis.lief_nr)]})

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_ophis.artnr)]})

            l_ophhis = get_cache (L_ophhis, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_ophis.lscheinnr)],"datum": [(eq, l_ophis.datum)]})
            str_list = Str_list()
            str_list_data.append(str_list)


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
            str_list.qty =  to_decimal(l_ophis.anzahl)
            str_list.epreis =  to_decimal(l_ophis.einzelpreis)
            str_list.warenwert =  to_decimal(l_ophis.warenwert)
            str_list.date = l_ophis.datum
            str_list.st = l_ophis.lager_nr
            str_list.article = l_artikel.artnr
            str_list.description = l_artikel.bezeich
            str_list.d_unit = l_artikel.traubensorte
            str_list.m_unit = l_artikel.masseinheit # RAGUNG: A92782
            str_list.inc_qty =  to_decimal(l_ophis.anzahl)
            str_list.amount =  to_decimal(str_list.warenwert)
            str_list.amountexcl =  to_decimal(l_ophis.warenwert)
            str_list.supplier = l_lieferant.firma
            str_list.tax_code = l_artikel.lief_artnr[2]

            taxcode_list = query(taxcode_list_data, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

            if taxcode_list:
                str_list.tax_amount =  to_decimal(l_ophis.warenwert) * to_decimal(taxcode_list.taxamount)
                t_tax =  to_decimal(t_tax) + to_decimal((l_ophis.warenwert) * to_decimal(taxcode_list.taxamount) )
                str_list.tot_amt =  to_decimal(l_ophis.warenwert) + to_decimal(str_list.tax_amount)
                t_inv =  to_decimal(t_inv) + to_decimal((l_ophis.warenwert) + to_decimal(str_list.tax_amount) )

            if l_kredit:
                str_list.ap_voucher = l_kredit.rechnr
            else:
                str_list.ap_voucher = 0

            queasy = get_cache (Queasy, {"key": [(eq, 335)],"char1": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)]})

            if queasy:
                str_list.serial_number = queasy.char2
                str_list.invoice_date = queasy.date2
            else:
                str_list.serial_number = ""
                str_list.invoice_date = None

            queasy = get_cache (Queasy, {"key": [(eq, 340)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)],"deci1": [(eq, l_op.einzelpreis)]})

            if queasy:
                str_list.remark_artikel = queasy.char2
            else:
                str_list.remark_artikel = ""

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 336) & (Queasy.char1 == l_op.lscheinnr) & (Queasy.number2 == l_op.artnr) & (cast(Queasy.char2, Numeric) == l_op.einzelpreis) & (Queasy.number1 == cast(l_op._recid, Numeric))).first()

            if queasy:
                str_list.disc_amount =  to_decimal(str_list.disc_amount) + to_decimal(queasy.deci1) + to_decimal(queasy.deci2)
                str_list.vat_amount =  to_decimal(str_list.vat_amount)
                # str_list.addvat_amount =  to_decimal(str_list.addvat_amount) + to_decimal(to_decimal(queasy.char3) )

            if l_ophis.docu_nr == l_ophis.lscheinnr:
                str_list.direct_flag = True
                str_list.docu_no = "Direct Purchase"


            else:
                str_list.docu_no = l_ophis.docu_nr
            str_list.deliv_note = l_ophis.lscheinnr
            str_list.price =  to_decimal(unit_price)


            str_list.fibu, str_list.fibu_bez = convert_fibu(l_ophis.fibukonto)

        return generate_inner_output()


    def create_list22():

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_data, lvcarea, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, queasy, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal pvilanguage, last_artnr, lieferant_recid, l_kredit_recid, ap_recid, long_digit, show_price, store, all_supp, sorttype, from_grp, to_grp, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        lscheinnr:string = " "
        t_amountexcl:Decimal = to_decimal("0.0")
        str_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_amountexcl =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            for l_op.lscheinnr, l_op.datum, l_op.anzahl, l_op.artnr, l_op.warenwert, l_op.docu_nr, l_op.lager_nr, l_op.einzelpreis, l_op._recid, l_op.lief_nr, l_op.pos, l_op.stornogrund, l_op.fuellflag, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.masseinheit, l_artikel.lief_artnr, l_artikel._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.anzahl, L_op.artnr, L_op.warenwert, L_op.docu_nr, L_op.lager_nr, L_op.einzelpreis, L_op._recid, L_op.lief_nr, L_op.pos, L_op.stornogrund, L_op.fuellflag, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.masseinheit, L_artikel.lief_artnr, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr == l_lieferant.lief_nr) & (L_op.loeschflag <= 1) & (L_op.anzahl != 0) & (L_op.op_art == 1)).order_by(L_op.datum, L_artikel.bezeich).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                t_anz, t_amt, t_tax, t_inv, lscheinnr, t_amountexcl = assign_create_list22(t_anz, t_amt, t_tax, t_inv, lscheinnr, t_amountexcl)

        else:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            for l_op.lscheinnr, l_op.datum, l_op.anzahl, l_op.artnr, l_op.warenwert, l_op.docu_nr, l_op.lager_nr, l_op.einzelpreis, l_op._recid, l_op.lief_nr, l_op.pos, l_op.stornogrund, l_op.fuellflag, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.masseinheit, l_artikel.lief_artnr, l_artikel._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.anzahl, L_op.artnr, L_op.warenwert, L_op.docu_nr, L_op.lager_nr, L_op.einzelpreis, L_op._recid, L_op.lief_nr, L_op.pos, L_op.stornogrund, L_op.fuellflag, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.masseinheit, L_artikel.lief_artnr, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr == l_lieferant.lief_nr) & (L_op.loeschflag <= 1) & (L_op.lager_nr == store) & (L_op.anzahl != 0) & (L_op.op_art == 1)).order_by(L_op.datum, L_artikel.bezeich).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                t_anz, t_amt, t_tax, t_inv, lscheinnr, t_amountexcl = assign_create_list22(t_anz, t_amt, t_tax, t_inv, lscheinnr, t_amountexcl)

        t_anz, t_amt, t_amountexcl, t_tax, t_inv = create_hislist(t_anz, t_amt, t_amountexcl, t_tax, t_inv)
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


        str_list = Str_list()
        str_list_data.append(str_list)

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


    def assign_create_list22(t_anz:Decimal, t_amt:Decimal, t_tax:Decimal, t_inv:Decimal, lscheinnr:string, t_amountexcl:Decimal):

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_data, lvcarea, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, queasy, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal pvilanguage, last_artnr, lieferant_recid, l_kredit_recid, ap_recid, long_digit, show_price, store, all_supp, sorttype, from_grp, to_grp, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        amt:Decimal = to_decimal("0.0")

        def generate_inner_output():
            return (t_anz, t_amt, t_tax, t_inv, lscheinnr, t_amountexcl)


        l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})

        if lscheinnr == "":
            lscheinnr = l_op.lscheinnr

        if lscheinnr != l_op.lscheinnr:
            lscheinnr = l_op.lscheinnr
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


            t_anz =  to_decimal("0")
            t_amt =  to_decimal("0")
            t_amountexcl =  to_decimal("0")
            t_tax =  to_decimal("0")
            t_inv =  to_decimal("0")
            str_list = Str_list()
            str_list_data.append(str_list)

        tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

        queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

        if queasy:
            tot_amount =  to_decimal(tot_amount) + to_decimal((l_op.warenwert) + to_decimal((l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100))) )
            tot_amountexcl =  to_decimal(tot_amountexcl) + to_decimal(l_op.warenwert)


        else:
            tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
            tot_amountexcl =  to_decimal(tot_amountexcl) + to_decimal(l_op.warenwert)

        if show_price:
            unit_price = ( to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl))
            unit_price = to_decimal(round(unit_price , 2))

        str_list = query(str_list_data, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis), first=True)

        if str_list:
            str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

            if show_price:

                queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

                if queasy:
                    str_list.addvat_value =  to_decimal(queasy.deci1)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal((l_op.warenwert) + to_decimal((l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100))) )
                    str_list.amountexcl =  to_decimal(str_list.amountexcl) + to_decimal(l_op.warenwert)
                    str_list.addvat_amount =  to_decimal(str_list.addvat_amount) + to_decimal((l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100)) )


                else:
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.amountexcl =  to_decimal(str_list.amountexcl) + to_decimal(l_op.warenwert)


            str_list.inc_qty =  to_decimal(str_list.qty)
            str_list.amount =  to_decimal(str_list.warenwert)

            taxcode_list = query(taxcode_list_data, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

            if taxcode_list:
                amt =  to_decimal(l_op.warenwert) * to_decimal(taxcode_list.taxamount)
                str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                tot_tax =  to_decimal(tot_tax) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_op.warenwert) + to_decimal(amt) )
                tot_amt =  to_decimal(tot_amt) + to_decimal((l_op.warenwert) + to_decimal(amt) )

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 336) & (Queasy.char1 == l_op.lscheinnr) & (Queasy.number2 == l_op.artnr) & (cast(Queasy.char2, Numeric) == l_op.einzelpreis) & (Queasy.number1 == cast(l_op._recid, Numeric))).first()

            if queasy:
                str_list.disc_amount =  to_decimal(str_list.disc_amount) + to_decimal(queasy.deci1) + to_decimal(queasy.deci2)
                str_list.vat_amount =  to_decimal(str_list.vat_amount)
                # str_list.addvat_amount =  to_decimal(str_list.addvat_amount) + to_decimal(to_decimal(queasy.char3) )

        else:
            str_list = Str_list()
            str_list_data.append(str_list)

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
            str_list.qty =  to_decimal(l_op.anzahl)
            str_list.epreis =  to_decimal(l_op.einzelpreis)
            str_list.pos = l_op.pos

            buff_l_kredit = get_cache (L_kredit, {"lscheinnr": [(eq, l_op.lscheinnr)]})

            if buff_l_kredit:
                str_list.ap_voucher = buff_l_kredit.rechnr
            else:
                str_list.ap_voucher = 0

            if show_price:

                queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

                if queasy:
                    str_list.addvat_value =  to_decimal(queasy.deci1)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal((l_op.warenwert) + to_decimal((l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100))) )
                    str_list.amountexcl =  to_decimal(l_op.warenwert)
                    str_list.addvat_amount = ( to_decimal(l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100)) )


                else:
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.amountexcl =  to_decimal(l_op.warenwert)

            queasy = get_cache (Queasy, {"key": [(eq, 335)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

            if queasy:
                str_list.serial_number = queasy.char2
                str_list.invoice_date = queasy.date2
            else:
                str_list.serial_number = ""
                str_list.invoice_date = None

            queasy = get_cache (Queasy, {"key": [(eq, 340)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)],"deci1": [(eq, l_op.einzelpreis)]})

            if queasy:
                str_list.remark_artikel = queasy.char2
            else:
                str_list.remark_artikel = ""

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 336) & (Queasy.char1 == l_op.lscheinnr) & (Queasy.number2 == l_op.artnr) & (cast(Queasy.char2, Numeric) == l_op.einzelpreis) & (Queasy.number1 == cast(l_op._recid, Numeric))).first()

            if queasy:
                str_list.disc_amount =  to_decimal(queasy.deci1) + to_decimal(queasy.deci2)
                str_list.vat_amount =  to_decimal(queasy.deci3)
                # str_list.addvat_amount =  to_decimal(to_decimal(queasy.char3) )

            str_list.fibu, str_list.fibu_bez = convert_fibu(l_op.stornogrund)
            str_list.date = l_op.datum
            str_list.st = l_op.lager_nr
            str_list.article = l_artikel.artnr
            str_list.description = l_artikel.bezeich
            str_list.d_unit = l_artikel.traubensorte
            str_list.m_unit = l_artikel.masseinheit # RAGUNG: A92782
            str_list.inc_qty =  to_decimal(l_op.anzahl)
            str_list.amount =  to_decimal(str_list.warenwert)
            str_list.supplier = l_lieferant.firma
            str_list.docu_no = l_op.docu_nr
            str_list.deliv_note = l_op.lscheinnr
            str_list.price =  to_decimal(unit_price)
            str_list.tax_code = l_artikel.lief_artnr[2]

            if l_lieferant.plz != " ":

                if matches(l_lieferant.plz,r"*#*"):
                    for loopi in range(1,num_entries(l_lieferant.plz, "#")  + 1) :

                        if entry(loopi + 1 - 1, l_lieferant.plz, "#") != " ":
                            str_list.gstid = entry(loopi + 1 - 1, l_lieferant.plz, "#")


                            return generate_inner_output()

            taxcode_list = query(taxcode_list_data, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

            if taxcode_list:
                str_list.tax_amount =  to_decimal(l_op.warenwert) * to_decimal(taxcode_list.taxamount)
                tot_tax =  to_decimal(tot_tax) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                str_list.tot_amt =  to_decimal(l_op.warenwert) + to_decimal(str_list.tax_amount)
                tot_amt =  to_decimal(tot_amt) + to_decimal((l_op.warenwert) + to_decimal(str_list.tax_amount) )

            if l_op.docu_nr == l_op.lscheinnr:
                str_list.direct_flag = True

        return generate_inner_output()


    def create_list22a():

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_data, lvcarea, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, queasy, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal pvilanguage, last_artnr, lieferant_recid, l_kredit_recid, ap_recid, long_digit, show_price, store, all_supp, sorttype, from_grp, to_grp, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        lscheinnr:string = ""
        t_amountexcl:Decimal = to_decimal("0.0")
        str_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_amountexcl =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_op.lscheinnr, l_op.datum, l_op.anzahl, l_op.artnr, l_op.warenwert, l_op.docu_nr, l_op.lager_nr, l_op.einzelpreis, l_op._recid, l_op.lief_nr, l_op.pos, l_op.stornogrund, l_op.fuellflag, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.masseinheit, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.anzahl, L_op.artnr, L_op.warenwert, L_op.docu_nr, L_op.lager_nr, L_op.einzelpreis, L_op._recid, L_op.lief_nr, L_op.pos, L_op.stornogrund, L_op.fuellflag, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.masseinheit, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr == l_lieferant.lief_nr) & (L_op.loeschflag <= 1) & (L_op.op_art == 1) & (L_op.anzahl != 0)).order_by(L_op.datum, L_op.lscheinnr, L_artikel.bezeich).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                t_anz, t_amt, t_tax, t_inv, lscheinnr, t_amountexcl = assign_create_list22a(t_anz, t_amt, t_tax, t_inv, lscheinnr, t_amountexcl)

        else:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_op.lscheinnr, l_op.datum, l_op.anzahl, l_op.artnr, l_op.warenwert, l_op.docu_nr, l_op.lager_nr, l_op.einzelpreis, l_op._recid, l_op.lief_nr, l_op.pos, l_op.stornogrund, l_op.fuellflag, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.masseinheit, l_artikel.lief_artnr, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant.plz, l_lieferant._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.anzahl, L_op.artnr, L_op.warenwert, L_op.docu_nr, L_op.lager_nr, L_op.einzelpreis, L_op._recid, L_op.lief_nr, L_op.pos, L_op.stornogrund, L_op.fuellflag, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.masseinheit, L_artikel.lief_artnr, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant.plz, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr == l_lieferant.lief_nr) & (L_op.loeschflag <= 1) & (L_op.op_art == 1) & (L_op.lager_nr == store) & (L_op.anzahl != 0)).order_by(L_op.datum, L_op.lscheinnr, L_artikel.bezeich).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                t_anz, t_amt, t_tax, t_inv, lscheinnr, t_amountexcl = assign_create_list22a(t_anz, t_amt, t_tax, t_inv, lscheinnr, t_amountexcl)

        t_anz, t_amt, t_tax, t_inv, t_amountexcl = create_hislist(t_anz, t_amt, t_tax, t_inv, t_amountexcl)
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


        str_list = Str_list()
        str_list_data.append(str_list)

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


    def assign_create_list22a(t_anz:Decimal, t_amt:Decimal, t_tax:Decimal, t_inv:Decimal, lscheinnr:string, t_amountexcl:Decimal):

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_data, lvcarea, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, queasy, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal pvilanguage, last_artnr, lieferant_recid, l_kredit_recid, ap_recid, long_digit, show_price, store, all_supp, sorttype, from_grp, to_grp, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        amt:Decimal = to_decimal("0.0")

        def generate_inner_output():
            return (t_anz, t_amt, t_tax, t_inv, lscheinnr, t_amountexcl)


        l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})

        if lscheinnr == "":
            lscheinnr = l_op.lscheinnr

        if lscheinnr != l_op.lscheinnr:
            lscheinnr = l_op.lscheinnr
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


            t_anz =  to_decimal("0")
            t_amt =  to_decimal("0")
            t_amountexcl =  to_decimal("0")
            t_tax =  to_decimal("0")
            t_inv =  to_decimal("0")
            str_list = Str_list()
            str_list_data.append(str_list)

        t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)

        if show_price:

            queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

            if queasy:
                t_amt =  to_decimal(t_amt) + to_decimal((l_op.warenwert) + to_decimal((l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100))) )
                tot_amount =  to_decimal(tot_amount) + to_decimal((l_op.warenwert) + to_decimal((l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100))) )
                t_amountexcl =  to_decimal(t_amountexcl) + to_decimal(l_op.warenwert)
                tot_amountexcl =  to_decimal(tot_amountexcl) + to_decimal(l_op.warenwert)


            else:
                t_amt =  to_decimal(t_amt) + to_decimal(l_op.warenwert)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                t_amountexcl =  to_decimal(t_amountexcl) + to_decimal(l_op.warenwert)
                tot_amountexcl =  to_decimal(tot_amountexcl) + to_decimal(l_op.warenwert)


        tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

        if show_price:
            # unit_price =  to_decimal(l_op.einzelpreis)
            unit_price = ( to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl))
            unit_price = to_decimal(round(unit_price , 2)) # RAGUNG: A92782

        str_list = query(str_list_data, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis), first=True)

        if str_list:
            str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

            if show_price:

                queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

                if queasy:
                    str_list.addvat_value =  to_decimal(queasy.deci1)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal((l_op.warenwert) + to_decimal((l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100))) )
                    str_list.amountexcl =  to_decimal(str_list.amountexcl) + to_decimal(l_op.warenwert)
                    str_list.addvat_amount =  to_decimal(str_list.addvat_amount) + to_decimal((l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100)) )


                else:
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.amountexcl =  to_decimal(str_list.amountexcl) + to_decimal(l_op.warenwert)


            str_list.inc_qty =  to_decimal(str_list.qty)
            str_list.amount =  to_decimal(str_list.warenwert)

            taxcode_list = query(taxcode_list_data, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

            if taxcode_list:
                amt =  to_decimal(l_op.warenwert) * to_decimal(taxcode_list.taxamount)
                str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                t_tax =  to_decimal(t_tax) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                tot_tax =  to_decimal(tot_tax) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_op.warenwert) + to_decimal(amt) )
                t_inv =  to_decimal(t_inv) + to_decimal((l_op.warenwert) + to_decimal(amt) )
                tot_amt =  to_decimal(tot_amt) + to_decimal((l_op.warenwert) + to_decimal(amt) )

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 336) & (Queasy.char1 == l_op.lscheinnr) & (Queasy.number2 == l_op.artnr) & (cast(Queasy.char2, Numeric) == l_op.einzelpreis) & (Queasy.number1 == cast(l_op._recid, Numeric))).first()

            if queasy:
                str_list.disc_amount =  to_decimal(str_list.disc_amount) + to_decimal(queasy.deci1) + to_decimal(queasy.deci2)
                str_list.vat_amount =  to_decimal(str_list.vat_amount)
                # str_list.addvat_amount =  to_decimal(str_list.addvat_amount) + to_decimal(to_decimal(queasy.char3) )

        else:
            str_list = Str_list()
            str_list_data.append(str_list)

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
            str_list.qty =  to_decimal(l_op.anzahl)
            str_list.epreis =  to_decimal(l_op.einzelpreis)
            str_list.pos = l_op.pos

            buff_l_kredit = get_cache (L_kredit, {"lscheinnr": [(eq, l_op.lscheinnr)]})

            if buff_l_kredit:
                str_list.ap_voucher = buff_l_kredit.rechnr
            else:
                str_list.ap_voucher = 0

            if show_price:

                queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

                if queasy:
                    str_list.addvat_value =  to_decimal(queasy.deci1)
                    str_list.warenwert = ( to_decimal(l_op.warenwert) + (to_decimal(l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100))) )
                    str_list.amountexcl =  to_decimal(l_op.warenwert)
                    str_list.addvat_amount = ( to_decimal(l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100)) )


                else:
                    str_list.warenwert =  to_decimal(l_op.warenwert)
                    str_list.amountexcl =  to_decimal(l_op.warenwert)

            queasy = get_cache (Queasy, {"key": [(eq, 335)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

            if queasy:
                str_list.serial_number = queasy.char2
                str_list.invoice_date = queasy.date2
            else:
                str_list.serial_number = ""
                str_list.invoice_date = None

            queasy = get_cache (Queasy, {"key": [(eq, 340)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)],"deci1": [(eq, l_op.einzelpreis)]})

            if queasy:
                str_list.remark_artikel = queasy.char2
            else:
                str_list.remark_artikel = ""

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 336) & (Queasy.char1 == l_op.lscheinnr) & (Queasy.number2 == l_op.artnr) & (cast(Queasy.char2, Numeric) == l_op.einzelpreis) & (Queasy.number1 == cast(l_op._recid, Numeric))).first()

            if queasy:
                str_list.disc_amount =  to_decimal(queasy.deci1) + to_decimal(queasy.deci2)
                str_list.vat_amount =  to_decimal(queasy.deci3)


            str_list.fibu, str_list.fibu_bez = convert_fibu(l_op.stornogrund)
            str_list.date = l_op.datum
            str_list.st = l_op.lager_nr
            str_list.article = l_artikel.artnr
            str_list.description = l_artikel.bezeich
            str_list.d_unit = l_artikel.traubensorte
            str_list.m_unit = l_artikel.masseinheit # RAGUNG: A92782
            str_list.inc_qty =  to_decimal(l_op.anzahl)
            str_list.amount =  to_decimal(str_list.warenwert)
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
                str_list.tax_amount =  to_decimal(l_op.warenwert) * to_decimal(taxcode_list.taxamount)
                t_tax =  to_decimal(t_tax) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                tot_tax =  to_decimal(tot_tax) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                str_list.tot_amt =  to_decimal(l_op.warenwert) + to_decimal(str_list.tax_amount)
                t_inv =  to_decimal(t_inv) + to_decimal((l_op.warenwert) + to_decimal(str_list.tax_amount) )
                tot_amt =  to_decimal(tot_amt) + to_decimal((l_op.warenwert) + to_decimal(str_list.tax_amount) )

            if l_op.docu_nr == l_op.lscheinnr:
                str_list.direct_flag = True
                str_list.docu_no = translateExtended ("Direct Purchase ", lvcarea, "")


            else:
                str_list.docu_no = l_op.docu_nr
            str_list.deliv_note = l_op.lscheinnr
            str_list.price =  to_decimal(unit_price)

        return generate_inner_output()


    def create_list22b():

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_data, lvcarea, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, queasy, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal pvilanguage, last_artnr, lieferant_recid, l_kredit_recid, ap_recid, long_digit, show_price, store, all_supp, sorttype, from_grp, to_grp, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        t_tax:Decimal = to_decimal("0.0")
        t_inv:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        t_amountexcl:Decimal = to_decimal("0.0")
        str_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        tot_amountexcl =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_amt =  to_decimal("0")

        if store == 0:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_op.lscheinnr, l_op.datum, l_op.anzahl, l_op.artnr, l_op.warenwert, l_op.docu_nr, l_op.lager_nr, l_op.einzelpreis, l_op._recid, l_op.lief_nr, l_op.pos, l_op.stornogrund, l_op.fuellflag, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.masseinheit, l_artikel.lief_artnr, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.anzahl, L_op.artnr, L_op.warenwert, L_op.docu_nr, L_op.lager_nr, L_op.einzelpreis, L_op._recid, L_op.lief_nr, L_op.pos, L_op.stornogrund, L_op.fuellflag, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.masseinheit, L_artikel.lief_artnr, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr == l_lieferant.lief_nr) & (L_op.loeschflag <= 1) & (L_op.anzahl != 0) & (L_op.op_art == 1)).order_by(L_untergrup.bezeich, L_artikel.bezeich, L_op.datum).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                t_anz, t_amt, t_tax, t_inv, lscheinnr, t_amountexcl = assign_create_list22b(t_anz, t_amt, t_tax, t_inv, lscheinnr, t_amountexcl)

        else:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_op.lscheinnr, l_op.datum, l_op.anzahl, l_op.artnr, l_op.warenwert, l_op.docu_nr, l_op.lager_nr, l_op.einzelpreis, l_op._recid, l_op.lief_nr, l_op.pos, l_op.stornogrund, l_op.fuellflag, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel.masseinheit, l_artikel.lief_artnr, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.anzahl, L_op.artnr, L_op.warenwert, L_op.docu_nr, L_op.lager_nr, L_op.einzelpreis, L_op._recid, L_op.lief_nr, L_op.pos, L_op.stornogrund, L_op.fuellflag, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel.masseinheit, L_artikel.lief_artnr, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum >= from_grp) & (L_artikel.endkum <= to_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr == l_lieferant.lief_nr) & (L_op.loeschflag <= 1) & (L_op.anzahl != 0) & (L_op.op_art == 1) & (L_op.lager_nr == store)).order_by(L_untergrup.bezeich, L_op.datum, L_artikel.bezeich).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                t_anz, t_amt, t_tax, t_inv, lscheinnr, t_amountexcl = assign_create_list22b(t_anz, t_amt, t_tax, t_inv, lscheinnr, t_amountexcl)

        t_anz, t_amt, t_amountexcl, t_tax, t_inv = create_hislist(t_anz, t_amt, t_amountexcl, t_tax, t_inv)
        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.description = lscheinnr
        str_list.qty =  to_decimal(t_anz)
        str_list.inc_qty =  to_decimal(t_anz)
        str_list.amount =  to_decimal(t_amt)
        str_list.warenwert =  to_decimal(t_amt)
        str_list.amountexcl =  to_decimal(t_amountexcl)
        str_list.tax_amount =  to_decimal(t_tax)
        str_list.tot_amt =  to_decimal(t_inv)


        str_list.supplier = "T O T A L"
        str_list = Str_list()
        str_list_data.append(str_list)

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


    def assign_create_list22b(t_anz:Decimal, t_amt:Decimal, t_tax:Decimal, t_inv:Decimal, lscheinnr:string, t_amountexcl:Decimal):

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_data, lvcarea, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, queasy, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal pvilanguage, last_artnr, lieferant_recid, l_kredit_recid, ap_recid, long_digit, show_price, store, all_supp, sorttype, from_grp, to_grp, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        amt:Decimal = to_decimal("0.0")

        def generate_inner_output():
            return (t_anz, t_amt, t_tax, t_inv, lscheinnr, t_amountexcl)


        l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})

        if lscheinnr == "":
            lscheinnr = l_untergrup.bezeich

        if lscheinnr != l_untergrup.bezeich:
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.description = lscheinnr
            str_list.qty =  to_decimal(t_anz)
            str_list.inc_qty =  to_decimal(t_anz)
            str_list.amount =  to_decimal(t_amt)
            str_list.warenwert =  to_decimal(t_amt)
            str_list.amountexcl =  to_decimal(t_amountexcl)
            str_list.tax_amount =  to_decimal(t_tax)
            str_list.tot_amt =  to_decimal(t_inv)
            str_list.supplier = "T O T A L"
            lscheinnr = l_untergrup.bezeich


            t_anz =  to_decimal("0")
            t_amt =  to_decimal("0")
            t_amountexcl =  to_decimal("0")
            t_tax =  to_decimal("0")
            t_inv =  to_decimal("0")
            str_list = Str_list()
            str_list_data.append(str_list)

        t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)

        if show_price:

            queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

            if queasy:
                t_amt =  to_decimal(t_amt) + to_decimal((l_op.warenwert) + to_decimal((l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100))) )
                tot_amount =  to_decimal(tot_amount) + to_decimal((l_op.warenwert) + to_decimal((l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100))) )
                t_amountexcl =  to_decimal(t_amountexcl) + to_decimal(l_op.warenwert)
                tot_amountexcl =  to_decimal(tot_amountexcl) + to_decimal(l_op.warenwert)


            else:
                t_amt =  to_decimal(t_amt) + to_decimal(l_op.warenwert)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                t_amountexcl =  to_decimal(t_amountexcl) + to_decimal(l_op.warenwert)
                tot_amountexcl =  to_decimal(tot_amountexcl) + to_decimal(l_op.warenwert)


        tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

        if show_price:
            # unit_price =  to_decimal(l_op.einzelpreis)
            unit_price = ( to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl))
            unit_price = to_decimal(round(unit_price , 2)) # RAGUNG: A92782

        str_list = query(str_list_data, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

        if str_list:
            str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

            if show_price:

                queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

                if queasy:
                    str_list.addvat_value =  to_decimal(queasy.deci1)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal((l_op.warenwert) + to_decimal((l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100))) )
                    str_list.amountexcl =  to_decimal(str_list.amountexcl) + to_decimal(l_op.warenwert)
                    str_list.addvat_amount =  to_decimal(str_list.addvat_amount) + to_decimal((l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100)) )


                else:
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.amountexcl =  to_decimal(str_list.amountexcl) + to_decimal(l_op.warenwert)


            str_list.inc_qty =  to_decimal(str_list.qty)
            str_list.amount =  to_decimal(str_list.warenwert)

            taxcode_list = query(taxcode_list_data, filters=(lambda taxcode_list: taxcode_list.taxcode == str_list.tax_code), first=True)

            if taxcode_list:
                amt =  to_decimal(l_op.warenwert) * to_decimal(taxcode_list.taxamount)
                str_list.tax_amount =  to_decimal(str_list.tax_amount) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                t_tax =  to_decimal(t_tax) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                tot_tax =  to_decimal(tot_tax) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                str_list.tot_amt =  to_decimal(str_list.tot_amt) + to_decimal((l_op.warenwert) + to_decimal(amt) )
                t_inv =  to_decimal(t_inv) + to_decimal((l_op.warenwert) + to_decimal(amt) )
                tot_amt =  to_decimal(tot_amt) + to_decimal((l_op.warenwert) + to_decimal(amt) )

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 336) & (Queasy.char1 == l_op.lscheinnr) & (Queasy.number2 == l_op.artnr) & (cast(Queasy.char2, Numeric) == l_op.einzelpreis) & (Queasy.number1 == cast(l_op._recid, Numeric))).first()

            if queasy:
                str_list.disc_amount =  to_decimal(str_list.disc_amount) + to_decimal(queasy.deci1) + to_decimal(queasy.deci2)
                str_list.vat_amount =  to_decimal(str_list.vat_amount)
                # str_list.addvat_amount =  to_decimal(str_list.addvat_amount) + to_decimal(to_decimal(queasy.char3) )

        else:
            str_list = Str_list()
            str_list_data.append(str_list)

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
            str_list.qty =  to_decimal(l_op.anzahl)
            str_list.epreis =  to_decimal(l_op.einzelpreis)
            str_list.pos = l_op.pos

            buff_l_kredit = get_cache (L_kredit, {"lscheinnr": [(eq, l_op.lscheinnr)]})

            if buff_l_kredit:
                str_list.ap_voucher = buff_l_kredit.rechnr
            else:
                str_list.ap_voucher = 0

            if show_price:

                queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

                if queasy:
                    str_list.addvat_value =  to_decimal(queasy.deci1)
                    str_list.warenwert = ( to_decimal(l_op.warenwert) + (to_decimal(l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100))) )
                    str_list.amountexcl =  to_decimal(l_op.warenwert)
                    str_list.addvat_amount = ( to_decimal(l_op.warenwert) * to_decimal((queasy.deci1) / to_decimal(100)) )


                else:
                    str_list.warenwert =  to_decimal(l_op.warenwert)
                    str_list.amountexcl =  to_decimal(l_op.warenwert)

            queasy = get_cache (Queasy, {"key": [(eq, 335)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

            if queasy:
                str_list.serial_number = queasy.char2
                str_list.invoice_date = queasy.date2
            else:
                str_list.serial_number = ""
                str_list.invoice_date = None

            queasy = get_cache (Queasy, {"key": [(eq, 340)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)],"deci1": [(eq, l_op.einzelpreis)]})

            if queasy:
                str_list.remark_artikel = queasy.char2
            else:
                str_list.remark_artikel = ""

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 336) & (Queasy.char1 == l_op.lscheinnr) & (Queasy.number2 == l_op.artnr) & (cast(Queasy.char2, Numeric) == l_op.einzelpreis) & (Queasy.number1 == cast(l_op._recid, Numeric))).first()

            if queasy:
                str_list.disc_amount =  to_decimal(queasy.deci1) + to_decimal(queasy.deci2)
                str_list.vat_amount =  to_decimal(queasy.deci3)
                # str_list.addvat_amount =  to_decimal(to_decimal(queasy.char3) )

            str_list.fibu, str_list.fibu_bez = convert_fibu(l_op.stornogrund)
            str_list.date = l_op.datum
            str_list.st = l_op.lager_nr
            str_list.article = l_artikel.artnr
            str_list.description = l_artikel.bezeich
            str_list.d_unit = l_artikel.traubensorte
            str_list.m_unit = l_artikel.masseinheit # RAGUNG: A92782
            str_list.inc_qty =  to_decimal(l_op.anzahl)
            str_list.amount =  to_decimal(str_list.warenwert)
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
                str_list.tax_amount =  to_decimal(l_op.warenwert) * to_decimal(taxcode_list.taxamount)
                t_tax =  to_decimal(t_tax) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                tot_tax =  to_decimal(tot_tax) + to_decimal((l_op.warenwert) * to_decimal(taxcode_list.taxamount) )
                str_list.tot_amt =  to_decimal(l_op.warenwert) + to_decimal(str_list.tax_amount)
                t_inv =  to_decimal(t_inv) + to_decimal((l_op.warenwert) + to_decimal(str_list.tax_amount) )
                tot_amt =  to_decimal(tot_amt) + to_decimal((l_op.warenwert) + to_decimal(str_list.tax_amount) )

            if l_op.docu_nr == l_op.lscheinnr:
                str_list.direct_flag = True
                str_list.docu_no = translateExtended ("Direct Purchase ", lvcarea, "")


            else:
                str_list.docu_no = l_op.docu_nr
            str_list.deliv_note = l_op.lscheinnr
            str_list.price =  to_decimal(unit_price)

        return generate_inner_output()


    def add_id():

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_data, lvcarea, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, i, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, queasy, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal pvilanguage, last_artnr, lieferant_recid, l_kredit_recid, ap_recid, long_digit, show_price, store, all_supp, sorttype, from_grp, to_grp, from_date, to_date
        nonlocal buff_l_kredit


        nonlocal str_list, taxcode_list, buff_l_kredit
        nonlocal str_list_data

        usr = None
        Usr =  create_buffer("Usr",Bediener)

        usr = db_session.query(Usr).filter(
                 (Usr.nr == l_op.fuellflag)).first()

        if usr:
            str_list.id = usr.userinit
        else:
            str_list.id = "??"


    def convert_fibu(konto:string):

        nonlocal first_artnr, curr_artnr, last_artnr1, unit_price, str_list_data, lvcarea, tot_anz, tot_amount, tot_amountexcl, tot_tax, tot_amt, counter, loopi, l_lieferant, l_kredit, l_artikel, l_op, l_ophdr, queasy, l_untergrup, htparam, l_ophis, l_ophhis, bediener, gl_acct
        nonlocal pvilanguage, last_artnr, lieferant_recid, l_kredit_recid, ap_recid, long_digit, show_price, store, all_supp, sorttype, from_grp, to_grp, from_date, to_date
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

        if htparam:
            ch = htparam.fchar
            j = 0
            for i in range(1,length(ch)  + 1) :

                if substring(ch, i - 1, 1) >= ("0").lower()  and substring(ch, i - 1, 1) <= ("9").lower() :
                    j = j + 1
                    s = s + substring(konto, j - 1, 1)
                else:
                    s = s + substring(ch, i - 1, 1)

        return generate_inner_output()

    l_lieferant = get_cache (L_lieferant, {"_recid": [(eq, lieferant_recid)]})

    l_kredit = get_cache (L_kredit, {"_recid": [(eq, l_kredit_recid)]})

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

    for str_list in query(str_list_data, filters=(lambda str_list: str_list.description.lower()  != ("T O T A L").lower()  and str_list.description.lower()  != ("GRAND TOTAL").lower())):

        if str_list.disc_amount != 0:
            str_list.price =  to_decimal(str_list.price) + to_decimal(str_list.disc_amount)

        if str_list.vat_amount != 0:
            str_list.price =  to_decimal(str_list.price) - to_decimal(str_list.vat_amount)

    return generate_output()