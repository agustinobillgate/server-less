#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Bediener, Fa_ordheader, L_lieferant, Mathis, Fa_op

def fa_print_receiving_webbl(pvilanguage:int, user_init:string, lief_nr:int, po_nr:string, store:int, to_date:date, deliv_nr:string):

    prepare_cache ([Htparam, Bediener, Fa_ordheader, L_lieferant, Mathis, Fa_op])

    printer_nr = 0
    show_price = False
    crterm = 0
    d_purchase = False
    unit_price = to_decimal("0.0")
    firma = ""
    str_list_data = []
    tot_anz:Decimal = to_decimal("0.0")
    tot_amount:Decimal = to_decimal("0.0")
    lvcarea:string = "fa-print-receiving"
    htparam = bediener = fa_ordheader = l_lieferant = mathis = fa_op = None

    str_list = None

    str_list_data, Str_list = create_model("Str_list", {"artnr":int, "qty":Decimal, "warenwert":Decimal, "munit":string, "bezeich":string, "nr":int, "price":Decimal, "lscheinnr":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal printer_nr, show_price, crterm, d_purchase, unit_price, firma, str_list_data, tot_anz, tot_amount, lvcarea, htparam, bediener, fa_ordheader, l_lieferant, mathis, fa_op
        nonlocal pvilanguage, user_init, lief_nr, po_nr, store, to_date, deliv_nr


        nonlocal str_list
        nonlocal str_list_data

        return {"printer_nr": printer_nr, "show_price": show_price, "crterm": crterm, "d_purchase": d_purchase, "unit_price": unit_price, "firma": firma, "str-list": str_list_data}

    def create_list():

        nonlocal printer_nr, show_price, crterm, d_purchase, unit_price, firma, str_list_data, tot_anz, tot_amount, lvcarea, htparam, bediener, fa_ordheader, l_lieferant, mathis, fa_op
        nonlocal pvilanguage, user_init, lief_nr, po_nr, store, to_date, deliv_nr


        nonlocal str_list
        nonlocal str_list_data

        i:int = 0
        create_it:bool = False
        str_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        i = 0
        d_purchase = False

        fa_op_obj_list = {}
        fa_op = Fa_op()
        mathis = Mathis()
        for fa_op.lscheinnr, fa_op.anzahl, fa_op.warenwert, fa_op.einzelpreis, fa_op.nr, fa_op.docu_nr, fa_op._recid, mathis.nr, mathis.name, mathis._recid in db_session.query(Fa_op.lscheinnr, Fa_op.anzahl, Fa_op.warenwert, Fa_op.einzelpreis, Fa_op.nr, Fa_op.docu_nr, Fa_op._recid, Mathis.nr, Mathis.name, Mathis._recid).join(Mathis,(Mathis.nr == Fa_op.nr)).filter(
                 (Fa_op.datum == to_date) & (Fa_op.lief_nr == lief_nr) & (Fa_op.loeschflag == 0) & (Fa_op.anzahl != 0) & (Fa_op.lscheinnr == (deliv_nr).lower()) & (Fa_op.docu_nr == (po_nr).lower())).order_by(Fa_op.zeit, Mathis.name).all():
            if fa_op_obj_list.get(fa_op._recid):
                continue
            else:
                fa_op_obj_list[fa_op._recid] = True


            i = i + 1

            if fa_op.docu_nr == fa_op.lscheinnr:
                d_purchase = True
            tot_anz =  to_decimal(tot_anz) + to_decimal(fa_op.anzahl)

            if show_price:
                tot_amount =  to_decimal(tot_amount) + to_decimal(fa_op.warenwert)

            if show_price:
                unit_price =  to_decimal(fa_op.einzelpreis)
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.artnr = fa_op.nr
            str_list.qty =  to_decimal(fa_op.anzahl)
            str_list.munit = "unit "
            str_list.nr = mathis.nr
            str_list.bezeich = mathis.name
            str_list.price =  to_decimal(unit_price)
            str_list.warenwert =  to_decimal(fa_op.warenwert)
            str_list.lscheinnr = fa_op.lscheinnr


        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.bezeich = "T O T A L"
        str_list.qty =  to_decimal(tot_anz)
        str_list.warenwert =  to_decimal(tot_amount)


    def create_list1():

        nonlocal printer_nr, show_price, crterm, d_purchase, unit_price, firma, str_list_data, tot_anz, tot_amount, lvcarea, htparam, bediener, fa_ordheader, l_lieferant, mathis, fa_op
        nonlocal pvilanguage, user_init, lief_nr, po_nr, store, to_date, deliv_nr


        nonlocal str_list
        nonlocal str_list_data

        i:int = 0
        create_it:bool = False
        str_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        i = 0
        d_purchase = False

        fa_op_obj_list = {}
        fa_op = Fa_op()
        mathis = Mathis()
        for fa_op.lscheinnr, fa_op.anzahl, fa_op.warenwert, fa_op.einzelpreis, fa_op.nr, fa_op.docu_nr, fa_op._recid, mathis.nr, mathis.name, mathis._recid in db_session.query(Fa_op.lscheinnr, Fa_op.anzahl, Fa_op.warenwert, Fa_op.einzelpreis, Fa_op.nr, Fa_op.docu_nr, Fa_op._recid, Mathis.nr, Mathis.name, Mathis._recid).join(Mathis,(Mathis.nr == Fa_op.nr)).filter(
                 (Fa_op.datum == to_date) & (Fa_op.lief_nr == lief_nr) & (Fa_op.loeschflag == 0) & (Fa_op.anzahl != 0) & (Fa_op.lscheinnr == (deliv_nr).lower()) & (Fa_op.docu_nr == (po_nr).lower())).order_by(Fa_op.zeit, Mathis.name).all():
            if fa_op_obj_list.get(fa_op._recid):
                continue
            else:
                fa_op_obj_list[fa_op._recid] = True


            i = i + 1

            if fa_op.docu_nr == fa_op.lscheinnr:
                d_purchase = True
            tot_anz =  to_decimal(tot_anz) + to_decimal(fa_op.anzahl)

            if show_price:
                tot_amount =  to_decimal(tot_amount) + to_decimal(fa_op.warenwert)

            if show_price:
                unit_price =  to_decimal(fa_op.einzelpreis)
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.artnr = fa_op.nr
            str_list.qty =  to_decimal(fa_op.anzahl)
            str_list.munit = "unit"
            str_list.nr = mathis.nr
            str_list.bezeich = mathis.name
            str_list.price =  to_decimal(unit_price)
            str_list.warenwert =  to_decimal(fa_op.warenwert)
            str_list.lscheinnr = fa_op.lscheinnr


        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.bezeich = "T O T A L"
        str_list.qty =  to_decimal(tot_anz)
        str_list.warenwert =  to_decimal(tot_anz)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 111)]})
    printer_nr = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 43)]})
    show_price = htparam.flogical

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if substring(bediener.permissions, 21, 1) != ("0").lower() :
        show_price = True

    fa_ordheader = get_cache (Fa_ordheader, {"supplier_nr": [(eq, lief_nr)],"order_nr": [(eq, po_nr)]})

    if fa_ordheader:
        crterm = fa_ordheader.credit_term

    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, lief_nr)]})

    if l_lieferant:
        firma = l_lieferant.firma

    if store == 0:
        create_list()
    else:
        create_list1()
    pass

    return generate_output()