#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 30/7/2025
# (to_decimal(Queasy.char2) == l_op.einzelpreis) -> (func.cast(Queasy.char2, Numeric) == l_op.einzelpreis)
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from sqlalchemy import and_, or_, func, cast, Numeric
from models import Htparam, Bediener, L_orderhdr, L_lieferant, L_op, L_artikel, L_lager, Queasy, L_ophis, Gl_acct

def prepare_print_receiving_cld_3bl(pvilanguage:int, docu_nr:string, user_init:string, po_nr:string, lief_nr:int, store:int, to_date:date):

    prepare_cache ([Htparam, Bediener, L_orderhdr, L_lieferant, L_op, L_artikel, L_lager, Queasy, L_ophis, Gl_acct])

    show_price = False
    crterm = 0
    d_purchase = False
    unit_price = to_decimal("0.0")
    l_lieferant_firma = ""
    avail_l_lager = False
    t_lager_nr = 0
    t_bezeich = ""
    str_list_data = []
    tot_anz:Decimal = to_decimal("0.0")
    tot_amount:Decimal = to_decimal("0.0")
    lvcarea:string = "print-receiving1"
    htparam = bediener = l_orderhdr = l_lieferant = l_op = l_artikel = l_lager = queasy = l_ophis = gl_acct = None

    str_list = None

    str_list_data, Str_list = create_model("Str_list", {"artnr":string, "qty":Decimal, "warenwert":string, "munit":string, "dunit":string, "fibu":string, "fibu_ze":string, "addvat_value":Decimal, "bezeich":string, "lscheinnr":string, "unit_price":Decimal, "disc_amount":Decimal, "addvat_amount":Decimal, "disc_amount2":Decimal, "vat_amount":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal show_price, crterm, d_purchase, unit_price, l_lieferant_firma, avail_l_lager, t_lager_nr, t_bezeich, str_list_data, tot_anz, tot_amount, lvcarea, htparam, bediener, l_orderhdr, l_lieferant, l_op, l_artikel, l_lager, queasy, l_ophis, gl_acct
        nonlocal pvilanguage, docu_nr, user_init, po_nr, lief_nr, store, to_date


        nonlocal str_list
        nonlocal str_list_data

        return {"show_price": show_price, "crterm": crterm, "d_purchase": d_purchase, "unit_price": unit_price, "l_lieferant_firma": l_lieferant_firma, "avail_l_lager": avail_l_lager, "t_lager_nr": t_lager_nr, "t_bezeich": t_bezeich, "str-list": str_list_data}

    def create_list():

        nonlocal show_price, crterm, d_purchase, unit_price, l_lieferant_firma, avail_l_lager, t_lager_nr, t_bezeich, str_list_data, tot_anz, tot_amount, lvcarea, htparam, bediener, l_orderhdr, l_lieferant, l_op, l_artikel, l_lager, queasy, l_ophis, gl_acct
        nonlocal pvilanguage, docu_nr, user_init, po_nr, lief_nr, store, to_date


        nonlocal str_list
        nonlocal str_list_data

        i:int = 0
        create_it:bool = False
        b_lop = None
        B_lop =  create_buffer("B_lop",L_op)
        str_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        i = 0
        d_purchase = False

        b_lop = get_cache (L_op, {"datum": [(eq, to_date)],"lief_nr": [(eq, lief_nr)],"op_art": [(eq, 1)],"loeschflag": [(le, 1)],"anzahl": [(ne, 0)],"lscheinnr": [(eq, docu_nr)]})

        if b_lop:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            for l_op.lscheinnr, l_op.lager_nr, l_op.anzahl, l_op.warenwert, l_op.einzelpreis, l_op.artnr, l_op._recid, l_op.stornogrund, l_op.docu_nr, l_artikel.traubensorte, l_artikel.masseinheit, l_artikel.bezeich, l_artikel._recid in db_session.query(L_op.lscheinnr, L_op.lager_nr, L_op.anzahl, L_op.warenwert, L_op.einzelpreis, L_op.artnr, L_op._recid, L_op.stornogrund, L_op.docu_nr, L_artikel.traubensorte, L_artikel.masseinheit, L_artikel.bezeich, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                     (L_op.datum == to_date) & (L_op.lief_nr == lief_nr) & (L_op.op_art == 1) & (L_op.loeschflag <= 1) & (L_op.anzahl != 0) & (L_op.lscheinnr == (docu_nr).lower())).order_by(L_op.pos, L_op.zeit, L_artikel.bezeich).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                i = i + 1

                if l_op.docu_nr == l_op.lscheinnr:
                    d_purchase = True

                if i == 1:

                    l_lager = get_cache (L_lager, {"lager_nr": [(eq, l_op.lager_nr)]})
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

                if show_price:

                    if l_artikel.masseinheit != l_artikel.traubensorte:
                        unit_price = ( to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl))
                        unit_price = to_decimal(round(unit_price , 2))
                        tot_amount =  to_decimal(tot_amount) + to_decimal((l_op.warenwert))
                    else:
                        unit_price =  to_decimal(l_op.einzelpreis)
                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                if l_op.stornogrund != "":
                    create_it = True
                else:

                    str_list = query(str_list_data, filters=(lambda str_list: str_list.artnr == to_string(l_op.artnr, ">>>>>>>>")), first=True)
                    create_it = not None != str_list

                if not create_it:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

                    if show_price:

                        if l_artikel.masseinheit != l_artikel.traubensorte:
                            str_list.warenwert = to_string(to_decimal(tot_amount) , "->>>,>>>,>>>,>>9.99")
                    else:
                        str_list.warenwert = to_string(to_decimal(str_list.warenwert) + l_op.warenwert, "->>>,>>>,>>>,>>9.99")

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 336) & (Queasy.char1 == l_op.lscheinnr) & (Queasy.number2 == l_op.artnr) & (to_decimal(Queasy.char2) == l_op.einzelpreis) & (Queasy.number1 == to_int(l_op._recid))).first()

                    if queasy:
                        str_list.disc_amount =  to_decimal(str_list.disc_amount) + to_decimal(queasy.deci1) + to_decimal(queasy.deci2)
                        str_list.vat_amount =  to_decimal(str_list.vat_amount)
                        str_list.addvat_amount =  to_decimal(str_list.addvat_amount) + to_decimal(to_decimal(queasy.char3) )


                else:
                    str_list = Str_list()
                    str_list_data.append(str_list)

                    str_list.artnr = to_string(l_op.artnr, ">>>>>>>>")
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.munit = l_artikel.masseinheit
                    str_list.dunit = l_artikel.traubensorte

                    queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

                    if queasy:
                        str_list.addvat_value =  to_decimal(queasy.deci1)

                    # Rd, 30/7/2025
                    # queasy = db_session.query(Queasy).filter(
                    #          (Queasy.key == 336) & (Queasy.char1 == l_op.lscheinnr) & 
                    #          (Queasy.number2 == l_op.artnr) & 
                    #          (to_decimal(Queasy.char2) == l_op.einzelpreis) & 
                    #          (Queasy.number1 == to_int(l_op._recid))).first()

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 336) & (Queasy.char1 == l_op.lscheinnr) & 
                             (Queasy.number2 == l_op.artnr) & 
                             (func.cast(Queasy.char2, Numeric) == l_op.einzelpreis) &
                             (Queasy.number1 == to_int(l_op._recid))).first()

                    if queasy:
                        str_list.disc_amount =  to_decimal(queasy.deci1) + to_decimal(queasy.deci2)
                        str_list.vat_amount =  to_decimal(queasy.deci3)
                        str_list.addvat_amount =  to_decimal(to_decimal(queasy.char3) )

                    if show_price:

                        if l_artikel.masseinheit != l_artikel.traubensorte:
                            str_list.warenwert = to_string(to_decimal(tot_amount) , "->>>,>>>,>>>,>>9.99")
                        else:
                            str_list.warenwert = to_string(to_decimal(str_list.warenwert) + l_op.warenwert, "->>>,>>>,>>>,>>9.99")
                    str_list.bezeich = l_artikel.bezeich
                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.unit_price =  to_decimal(unit_price)


                    str_list.fibu, str_list.fibu_ze = convert_fibu(l_op.stornogrund)
        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            for l_ophis.lscheinnr, l_ophis.lager_nr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.einzelpreis, l_ophis.artnr, l_ophis.fibukonto, l_ophis.docu_nr, l_ophis._recid, l_artikel.traubensorte, l_artikel.masseinheit, l_artikel.bezeich, l_artikel._recid in db_session.query(L_ophis.lscheinnr, L_ophis.lager_nr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.einzelpreis, L_ophis.artnr, L_ophis.fibukonto, L_ophis.docu_nr, L_ophis._recid, L_artikel.traubensorte, L_artikel.masseinheit, L_artikel.bezeich, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).filter(
                     (L_ophis.datum == to_date) & (L_ophis.lief_nr == lief_nr) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (L_ophis.lscheinnr == (docu_nr).lower()) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                i = i + 1

                if l_ophis.docu_nr == l_ophis.lscheinnr:
                    d_purchase = True

                if i == 1:

                    l_lager = get_cache (L_lager, {"lager_nr": [(eq, l_ophis.lager_nr)]})
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)

                if show_price:

                    if l_artikel.masseinheit != l_artikel.traubensorte:
                        unit_price = ( to_decimal(l_ophis.warenwert) / to_decimal(l_ophis.anzahl))
                        unit_price = to_decimal(round(unit_price , 2))
                        tot_amount =  to_decimal(tot_amount) + to_decimal((l_ophis.warenwert))
                    else:
                        unit_price =  to_decimal(l_ophis.einzelpreis)
                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_data, filters=(lambda str_list: str_list.to_int(str_list.artnr) == l_ophis.artnr), first=True)
                create_it = not None != str_list

                if not create_it:
                    str_list.artnr = to_string(l_ophis.artnr, ">>>>>>>>")
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)

                    if show_price:

                        if l_artikel.masseinheit != l_artikel.traubensorte:
                            str_list.warenwert = to_string(to_decimal(tot_amount) , "->>>,>>>,>>>,>>9.99")
                    else:
                        str_list.warenwert = to_string(to_decimal(str_list.warenwert) + l_ophis.warenwert, "->>>,>>>,>>>,>>9.99")

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 336) & (Queasy.char1 == l_ophis.lscheinnr) & (Queasy.number2 == l_ophis.artnr) & (to_decimal(Queasy.char2) == l_ophis.einzelpreis)).first()

                    if queasy:
                        str_list.disc_amount =  to_decimal(str_list.disc_amount) + to_decimal(queasy.deci1) + to_decimal(queasy.deci2)
                        str_list.vat_amount =  to_decimal(str_list.vat_amount)
                        str_list.addvat_amount =  to_decimal(str_list.addvat_amount) + to_decimal(to_decimal(queasy.char3) )


                else:
                    str_list = Str_list()
                    str_list_data.append(str_list)

                    str_list.artnr = to_string(l_ophis.artnr, ">>>>>>>>")
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.munit = l_artikel.masseinheit
                    str_list.dunit = l_artikel.traubensorte

                    queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)]})

                    if queasy:
                        str_list.addvat_value =  to_decimal(queasy.deci1)

                    if show_price:

                        if l_artikel.masseinheit != l_artikel.traubensorte:
                            str_list.warenwert = to_string(to_decimal(tot_amount) , "->>>,>>>,>>>,>>9.99")
                        else:
                            str_list.warenwert = to_string(to_decimal(str_list.warenwert) + l_ophis.warenwert, "->>>,>>>,>>>,>>9.99")
                    str_list.bezeich = l_artikel.bezeich
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.unit_price =  to_decimal(unit_price)

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 336) & (Queasy.char1 == l_ophis.lscheinnr) & (Queasy.number2 == l_ophis.artnr) & (to_decimal(Queasy.char2) == l_ophis.einzelpreis)).first()

                    if queasy:
                        str_list.disc_amount =  to_decimal(queasy.deci1) + to_decimal(queasy.deci2)
                        str_list.vat_amount =  to_decimal(queasy.deci3)
                        str_list.addvat_amount =  to_decimal(to_decimal(queasy.char3) )


                    str_list.fibu, str_list.fibu_ze = convert_fibu(l_ophis.fibukonto)
        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.bezeich = translateExtended ("T O T A L", lvcarea, "")
        str_list.qty =  to_decimal(tot_anz)
        str_list.warenwert = to_string(tot_amount, "->>>,>>>,>>>,>>9.99")

        if l_lager:
            avail_l_lager = True
            t_lager_nr = l_lager.lager_nr
            t_bezeich = l_lager.bezeich


    def create_list1():

        nonlocal show_price, crterm, d_purchase, unit_price, l_lieferant_firma, avail_l_lager, t_lager_nr, t_bezeich, str_list_data, tot_anz, tot_amount, lvcarea, htparam, bediener, l_orderhdr, l_lieferant, l_op, l_artikel, l_lager, queasy, l_ophis, gl_acct
        nonlocal pvilanguage, docu_nr, user_init, po_nr, lief_nr, store, to_date


        nonlocal str_list
        nonlocal str_list_data

        i:int = 0
        create_it:bool = False
        b_lop = None
        B_lop =  create_buffer("B_lop",L_op)
        str_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        i = 0
        d_purchase = False

        b_lop = get_cache (L_op, {"datum": [(eq, to_date)],"lief_nr": [(eq, lief_nr)],"op_art": [(eq, 1)],"loeschflag": [(le, 1)],"anzahl": [(ne, 0)],"lager_nr": [(eq, store)],"lscheinnr": [(eq, docu_nr)]})

        if b_lop:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            for l_op.lscheinnr, l_op.lager_nr, l_op.anzahl, l_op.warenwert, l_op.einzelpreis, l_op.artnr, l_op._recid, l_op.stornogrund, l_op.docu_nr, l_artikel.traubensorte, l_artikel.masseinheit, l_artikel.bezeich, l_artikel._recid in db_session.query(L_op.lscheinnr, L_op.lager_nr, L_op.anzahl, L_op.warenwert, L_op.einzelpreis, L_op.artnr, L_op._recid, L_op.stornogrund, L_op.docu_nr, L_artikel.traubensorte, L_artikel.masseinheit, L_artikel.bezeich, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                     (L_op.datum == to_date) & (L_op.lief_nr == lief_nr) & (L_op.op_art == 1) & (L_op.loeschflag <= 1) & (L_op.anzahl != 0) & (L_op.lager_nr == store) & (L_op.lscheinnr == (docu_nr).lower())).order_by(L_op.pos, L_op.zeit, L_artikel.bezeich).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                i = i + 1

                if l_op.docu_nr == l_op.lscheinnr:
                    d_purchase = True

                if i == 1:

                    l_lager = get_cache (L_lager, {"lager_nr": [(eq, l_op.lager_nr)]})
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

                if show_price:

                    if l_artikel.masseinheit != l_artikel.traubensorte:
                        unit_price =  to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl)
                        unit_price = to_decimal(round(unit_price , 2))
                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                    else:
                        unit_price =  to_decimal(l_op.einzelpreis)
                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                if l_op.stornogrund != "":
                    create_it = True
                else:

                    str_list = query(str_list_data, filters=(lambda str_list: str_list.to_int(str_list.artnr) == l_op.artnr), first=True)
                    create_it = not None != str_list

                if not create_it:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

                    if show_price:

                        if l_artikel.masseinheit != l_artikel.traubensorte:
                            str_list.warenwert = to_string(to_decimal(tot_amount) , "->>>,>>>,>>>,>>9.99")
                    else:
                        str_list.warenwert = to_string(to_decimal(str_list.warenwert) + l_op.warenwert, "->>>,>>>,>>>,>>9.99")

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 336) & (Queasy.char1 == l_op.lscheinnr) & (Queasy.number2 == l_op.artnr) & (to_decimal(Queasy.char2) == l_op.einzelpreis) & (Queasy.number1 == to_int(l_op._recid))).first()

                    if queasy:
                        str_list.disc_amount =  to_decimal(str_list.disc_amount) + to_decimal(queasy.deci1) + to_decimal(queasy.deci2)
                        str_list.vat_amount =  to_decimal(str_list.vat_amount)
                        str_list.addvat_amount =  to_decimal(str_list.addvat_amount) + to_decimal(to_decimal(queasy.char3) )


                else:
                    str_list = Str_list()
                    str_list_data.append(str_list)

                    str_list.artnr = to_string(l_op.artnr, ">>>>>>>>")
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.munit = l_artikel.masseinheit
                    str_list.dunit = l_artikel.traubensorte

                    queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

                    if queasy:
                        str_list.addvat_value =  to_decimal(queasy.deci1)

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 336) & (Queasy.char1 == l_op.lscheinnr) & (Queasy.number2 == l_op.artnr) & (to_decimal(Queasy.char2) == l_op.einzelpreis) & (Queasy.number1 == to_int(l_op._recid))).first()

                    if queasy:
                        str_list.disc_amount =  to_decimal(queasy.deci1) + to_decimal(queasy.deci2)
                        str_list.vat_amount =  to_decimal(queasy.deci3)
                        str_list.addvat_amount =  to_decimal(to_decimal(queasy.char3) )

                    if show_price:

                        if l_artikel.masseinheit != l_artikel.traubensorte:
                            str_list.warenwert = to_string(to_decimal(tot_amount) , "->>>,>>>,>>>,>>9.99")
                        else:
                            str_list.warenwert = to_string(to_decimal(str_list.warenwert) + l_op.warenwert, "->>>,>>>,>>>,>>9.99")
                    str_list.bezeich = l_artikel.bezeich
                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.unit_price =  to_decimal(unit_price)


                    str_list.fibu, str_list.fibu_ze = convert_fibu(l_op.stornogrund)
        else:

            l_ophis_obj_list = {}
            l_ophis = L_ophis()
            l_artikel = L_artikel()
            for l_ophis.lscheinnr, l_ophis.lager_nr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.einzelpreis, l_ophis.artnr, l_ophis.fibukonto, l_ophis.docu_nr, l_ophis._recid, l_artikel.traubensorte, l_artikel.masseinheit, l_artikel.bezeich, l_artikel._recid in db_session.query(L_ophis.lscheinnr, L_ophis.lager_nr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.einzelpreis, L_ophis.artnr, L_ophis.fibukonto, L_ophis.docu_nr, L_ophis._recid, L_artikel.traubensorte, L_artikel.masseinheit, L_artikel.bezeich, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).filter(
                     (L_ophis.datum == to_date) & (L_ophis.lief_nr == lief_nr) & (L_ophis.op_art == 1) & (L_ophis.anzahl != 0) & (L_ophis.lscheinnr == (docu_nr).lower()) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                i = i + 1

                if l_ophis.docu_nr == l_ophis.lscheinnr:
                    d_purchase = True

                if i == 1:

                    l_lager = get_cache (L_lager, {"lager_nr": [(eq, l_ophis.lager_nr)]})
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_ophis.anzahl)

                if show_price:

                    if l_artikel.masseinheit != l_artikel.traubensorte:
                        unit_price = ( to_decimal(l_ophis.warenwert) / to_decimal(l_ophis.anzahl))
                        unit_price = to_decimal(round(unit_price , 2))
                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)
                    else:
                        unit_price =  to_decimal(l_ophis.einzelpreis)
                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)

                str_list = query(str_list_data, filters=(lambda str_list: str_list.to_int(str_list.artnr) == l_ophis.artnr), first=True)
                create_it = not None != str_list

                if not create_it:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_ophis.anzahl)

                    if show_price:

                        if l_artikel.masseinheit != l_artikel.traubensorte:
                            str_list.warenwert = to_string(to_decimal(tot_amount) , "->>>,>>>,>>>,>>9.99")
                    else:
                        str_list.warenwert = to_string(to_decimal(str_list.warenwert) + l_ophis.warenwert, "->>>,>>>,>>>,>>9.99")

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 336) & (Queasy.char1 == l_ophis.lscheinnr) & (Queasy.number2 == l_ophis.artnr) & (to_decimal(Queasy.char2) == l_ophis.einzelpreis)).first()

                    if queasy:
                        str_list.disc_amount =  to_decimal(str_list.disc_amount) + to_decimal(queasy.deci1) + to_decimal(queasy.deci2)
                        str_list.vat_amount =  to_decimal(str_list.vat_amount)
                        str_list.addvat_amount =  to_decimal(str_list.addvat_amount) + to_decimal(to_decimal(queasy.char3) )


                else:
                    str_list = Str_list()
                    str_list_data.append(str_list)

                    str_list.artnr = to_string(l_ophis.artnr, ">>>>>>>>")
                    str_list.qty =  to_decimal(l_ophis.anzahl)
                    str_list.munit = l_artikel.masseinheit
                    str_list.dunit = l_artikel.traubensorte

                    queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_op.artnr)]})

                    if queasy:
                        str_list.addvat_value =  to_decimal(queasy.deci1)

                    if show_price:

                        if l_artikel.masseinheit != l_artikel.traubensorte:
                            str_list.warenwert = to_string(to_decimal(tot_amount) , "->>>,>>>,>>>,>>9.99")
                        else:
                            str_list.warenwert = to_string(to_decimal(str_list.warenwert) + l_ophis.warenwert, "->>>,>>>,>>>,>>9.99")
                    str_list.bezeich = l_artikel.bezeich
                    str_list.lscheinnr = l_ophis.lscheinnr
                    str_list.unit_price =  to_decimal(unit_price)

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 336) & (Queasy.char1 == l_ophis.lscheinnr) & (Queasy.number2 == l_ophis.artnr) & (to_decimal(Queasy.char2) == l_ophis.einzelpreis)).first()

                    if queasy:
                        str_list.disc_amount =  to_decimal(queasy.deci1) + to_decimal(queasy.deci2)
                        str_list.vat_amount =  to_decimal(queasy.deci3)
                        str_list.addvat_amount =  to_decimal(to_decimal(queasy.char3) )


                    str_list.fibu, str_list.fibu_ze = convert_fibu(l_ophis.fibukonto)
        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.bezeich = translateExtended ("T O T A L", lvcarea, "")
        str_list.qty =  to_decimal(tot_anz)
        str_list.warenwert = to_string(tot_amount, "->>>,>>>,>>>,>>9.99")

        if l_lager:
            avail_l_lager = True
            t_lager_nr = l_lager.lager_nr
            t_bezeich = l_lager.bezeich


    def convert_fibu(konto:string):

        nonlocal show_price, crterm, d_purchase, unit_price, l_lieferant_firma, avail_l_lager, t_lager_nr, t_bezeich, str_list_data, tot_anz, tot_amount, lvcarea, htparam, bediener, l_orderhdr, l_lieferant, l_op, l_artikel, l_lager, queasy, l_ophis, gl_acct
        nonlocal pvilanguage, docu_nr, user_init, po_nr, lief_nr, store, to_date


        nonlocal str_list
        nonlocal str_list_data

        s = ""
        bezeich = ""
        ch:string = ""
        i:int = 0
        j:int = 0

        def generate_inner_output():
            return (s, bezeich)


        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, konto)]})

        if not gl_acct:

            return generate_inner_output()
        bezeich = gl_acct.bezeich

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


    htparam = get_cache (Htparam, {"paramnr": [(eq, 43)]})
    show_price = htparam.flogical

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if substring(bediener.permissions, 21, 1) != ("0").lower() :
        show_price = True

    l_orderhdr = get_cache (L_orderhdr, {"lief_nr": [(eq, lief_nr)],"docu_nr": [(eq, po_nr)]})

    if l_orderhdr:
        crterm = l_orderhdr.angebot_lief[1]

    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, lief_nr)]})

    if l_lieferant:
        l_lieferant_firma = l_lieferant.firma

    if store == 0:
        create_list()
    else:
        create_list1()

    return generate_output()