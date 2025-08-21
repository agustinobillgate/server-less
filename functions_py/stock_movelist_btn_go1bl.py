#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 23/7/20225
# gitlab:656
# requery for each, close_date dikeluarkan
# 21/8/2025, Last Receiving date kosong
#-----------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, L_artikel, Bediener, L_bestand, L_op, L_ophdr, L_lager, L_lieferant, Gl_acct, L_ophis

def stock_movelist_btn_go1bl(pvilanguage:int, s_artnr:int, show_price:bool, from_lager:int, to_lager:int):

    prepare_cache ([Htparam, L_artikel, Bediener, L_bestand, L_op, L_ophdr, L_lager, L_lieferant, Gl_acct, L_ophis])

    stock_movelist_data = []
    lvcarea:string = "stock-movelist"
    tot_anz:Decimal = to_decimal("0.0")
    tot_val:Decimal = to_decimal("0.0")
    t_anz:Decimal = to_decimal("0.0")
    t_val:Decimal = to_decimal("0.0")
    long_digit:bool = False
    t_incoming:Decimal = to_decimal("0.0")
    t_inval:Decimal = to_decimal("0.0")
    t_outgoing:Decimal = to_decimal("0.0")
    t_outval:Decimal = to_decimal("0.0")
    htparam = l_artikel = bediener = l_bestand = l_op = l_ophdr = l_lager = l_lieferant = gl_acct = l_ophis = None

    str_list = str_list2 = stock_movelist = None

    str_list_data, Str_list = create_model("Str_list", {"s":string, "id":string, "m_unit":string})
    str_list2_data, Str_list2 = create_model("Str_list2", {"datum":string, "lscheinnr":string, "init_qty":string, "init_val":string, "in_qty":string, "in_val":string, "out_qty":string, "out_val":string, "note":string, "id":string, "m_unit":string})
    stock_movelist_data, Stock_movelist = create_model("Stock_movelist", {"datum":date, "lscheinnr":string, "init_qty":Decimal, "init_val":Decimal, "in_qty":Decimal, "in_val":Decimal, "out_qty":Decimal, "out_val":Decimal, "note":string, "id":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal stock_movelist_data, lvcarea, tot_anz, tot_val, t_anz, t_val, long_digit, t_incoming, t_inval, t_outgoing, t_outval, htparam, l_artikel, bediener, l_bestand, l_op, l_ophdr, l_lager, l_lieferant, gl_acct, l_ophis
        nonlocal pvilanguage, s_artnr, show_price, from_lager, to_lager


        nonlocal str_list, str_list2, stock_movelist
        nonlocal str_list_data, str_list2_data, stock_movelist_data

        return {"stock-movelist": stock_movelist_data}

    def create_list(pvilanguage:int, s_artnr:int, show_price:bool, from_lager:int, to_lager:int):

        nonlocal stock_movelist_data, lvcarea, tot_anz, tot_val, t_anz, t_val, long_digit, t_incoming, t_inval, t_outgoing, t_outval, htparam, l_artikel, bediener, l_bestand, l_op, l_ophdr, l_lager, l_lieferant, gl_acct, l_ophis
        nonlocal str_list, str_list2, stock_movelist
        nonlocal str_list_data, str_list2_data, stock_movelist_data

        t_qty:Decimal = to_decimal("0.0")
        t_wert:Decimal = to_decimal("0.0")
        bemerk:string = ""
        close_date:date = None
        preis:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        it_exist:bool = False
        last_date:date = None
        first_rec:bool = False
        usr = None
        l_oh = None
        l_op1 = None
        buf_ophdr = None

        def generate_inner_output():
            return (str_list2_data)

        Usr =  create_buffer("Usr",Bediener)
        L_oh =  create_buffer("L_oh",L_bestand)
        L_op1 =  create_buffer("L_op1",L_op)
        Buf_ophdr =  create_buffer("Buf_ophdr",L_ophdr)

        if l_artikel.endkum <= 2:
            htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})

            if htparam:
                close_date = htparam.fdate

        l_oh = get_cache (L_bestand, {"artnr": [(eq, s_artnr)],"lager_nr": [(eq, 0)]})

        if l_oh:
            t_qty =  to_decimal(l_oh.anz_anf_best) + to_decimal(l_oh.anz_eingang) - to_decimal(l_oh.anz_ausgang)

            if show_price:
                t_wert =  to_decimal(l_oh.val_anf_best) + to_decimal(l_oh.wert_eingang) - to_decimal(l_oh.wert_ausgang)


        str_list2_data.clear()
        tot_anz =  to_decimal("0")
        tot_val =  to_decimal("0")

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():

            l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, l_lager.lager_nr)],"artnr": [(eq, s_artnr)]})

            if l_bestand:
                t_anz =  to_decimal(l_bestand.anz_anf_best)

                if show_price:
                    t_val =  to_decimal(l_bestand.val_anf_best)


                str_list2 = Str_list2()
                str_list2_data.append(str_list2)

                str_list2.datum = ""
                str_list2.lscheinnr = to_string(l_lager.lager_nr) + " " + to_string(l_lager.bezeich)


                str_list2 = Str_list2()
                str_list2_data.append(str_list2)

                str_list2.m_unit = l_artikel.masseinheit

                if show_price:

                    if not long_digit:
                        str_list2.datum = to_string(l_bestand.anf_best_dat)
                        str_list2.lscheinnr = ""
                        str_list2.init_qty = to_string(l_bestand.anz_anf_best)
                        str_list2.init_val = to_string(l_bestand.val_anf_best)


                    else:
                        str_list2.datum = to_string(l_bestand.anf_best_dat)
                        str_list2.lscheinnr = ""
                        str_list2.init_qty = to_string(l_bestand.anz_anf_best)
                        str_list2.init_val = to_string(l_bestand.val_anf_best)


                else:

                    if not long_digit:
                        str_list2.datum = to_string(l_bestand.anf_best_dat)
                        str_list2.lscheinnr = ""
                        str_list2.init_qty = to_string(l_bestand.anz_anf_best)
                        str_list2.init_val = to_string(0)


                    else:
                        str_list2.datum = to_string(l_bestand.anf_best_dat)
                        str_list2.lscheinnr = ""
                        str_list2.init_qty = to_string(l_bestand.anz_anf_best)
                        str_list2.init_val = to_string(0)

            # Rd
            # add validation close_date is none
            # for l_op in db_session.query(L_op).filter(
            #          (L_op.lager_nr == l_lager.lager_nr) & (L_op.artnr == s_artnr) & (L_op.loeschflag <= 1) & (L_op.datum <= close_date)).order_by(L_op.datum, L_op.op_art).all():
            query = db_session.query(L_op).filter(
                        (L_op.lager_nr == l_lager.lager_nr) &
                        (L_op.artnr == s_artnr) &
                        (L_op.loeschflag <= 1)
                    )
            if close_date is not None:
                query = query.filter(L_op.datum <= close_date)
            l_op_list = query.order_by(L_op.datum, L_op.op_art).all()
            for l_op in l_op_list:
                it_exist = True

                if show_price:
                    preis =  to_decimal(l_op.einzelpreis)
                    wert =  to_decimal(l_op.warenwert)

                if l_op.op_art == 1:
                    bemerk = ""

                    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_op.lief_nr)]})

                    if l_lieferant:
                        bemerk = l_lieferant.firma


                    t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)
                    t_val =  to_decimal(t_val) + to_decimal(wert)


                    str_list2 = Str_list2()
                    str_list2_data.append(str_list2)

                    add_id()
                    str_list2.m_unit = l_artikel.masseinheit
                    str_list2.datum = to_string(l_op.datum)
                    str_list2.lscheinnr = to_string(l_op.lscheinnr)
                    str_list2.init_qty = to_string(0)
                    str_list2.init_val = to_string(0)
                    str_list2.in_qty = to_string(l_op.anzahl)
                    str_list2.in_val = to_string(wert)
                    str_list2.out_qty = to_string(0)
                    str_list2.out_val = to_string(0)
                    str_list2.note = to_string(bemerk)
                    t_incoming =  to_decimal(t_incoming) + to_decimal(l_op.anzahl)
                    t_inval =  to_decimal(t_inval) + to_decimal(wert)

                elif l_op.op_art == 2:

                    if l_op.herkunftflag == 1:

                        l_op1 = get_cache (L_op, {"op_art": [(eq, 4)],"datum": [(eq, l_op.datum)],"artnr": [(eq, l_op.artnr)],"anzahl": [(eq, l_op.anzahl)],"pos": [(eq, l_op.lager_nr)],"zeit": [(eq, l_op.zeit)]})

                        if l_op1:
                            bemerk = translateExtended ("From", lvcarea, "") + " " + to_string(l_op1.lager_nr)


                        else:
                            bemerk = translateExtended ("Transferred", lvcarea, "")

                    elif l_op.herkunftflag == 3:
                        bemerk = translateExtended ("Transform In", lvcarea, "")


                    t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)
                    t_val =  to_decimal(t_val) + to_decimal(wert)


                    str_list2 = Str_list2()
                    str_list2_data.append(str_list2)

                    add_id()
                    str_list2.m_unit = l_artikel.masseinheit
                    str_list2.datum = to_string(l_op.datum)
                    str_list2.lscheinnr = to_string(l_op.lscheinnr)
                    str_list2.init_qty = to_string(0)
                    str_list2.init_val = to_string(0)
                    str_list2.in_qty = to_string(l_op.anzahl)
                    str_list2.in_val = to_string(wert)
                    str_list2.out_qty = to_string(0)
                    str_list2.out_val = to_string(0)
                    str_list2.note = to_string(bemerk)
                    t_incoming =  to_decimal(t_incoming) + to_decimal(l_op.anzahl)
                    t_inval =  to_decimal(t_inval) + to_decimal(wert)

                elif l_op.op_art == 3:
                    bemerk = ""

                    if l_op.stornogrund != "":

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_op.stornogrund)]})

                        if gl_acct:
                            bemerk = gl_acct.fibukonto


                    else:

                        l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "stt")],"datum": [(eq, l_op.datum)],"lscheinnr": [(eq, l_op.lscheinnr)],"fibukonto": [(ne, "")]})

                        if l_ophdr:

                            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophdr.fibukonto)]})

                            if gl_acct:
                                bemerk = gl_acct.fibukonto


                    t_anz =  to_decimal(t_anz) - to_decimal(l_op.anzahl)
                    t_val =  to_decimal(t_val) - to_decimal(wert)


                    str_list2 = Str_list2()
                    str_list2_data.append(str_list2)

                    add_id()
                    str_list2.m_unit = l_artikel.masseinheit
                    str_list2.datum = to_string(l_op.datum)
                    str_list2.lscheinnr = to_string(l_op.lscheinnr)
                    str_list2.init_qty = to_string(0)
                    str_list2.init_val = to_string(0)
                    str_list2.in_qty = to_string(0)
                    str_list2.in_val = to_string(0)
                    str_list2.out_qty = to_string(l_op.anzahl)
                    str_list2.out_val = to_string(wert)
                    str_list2.note = to_string(bemerk)
                    t_outgoing =  to_decimal(t_outgoing) + to_decimal(l_op.anzahl)
                    t_outval =  to_decimal(t_outval) + to_decimal(wert)

                elif l_op.op_art == 4:

                    if l_op.herkunftflag == 1:
                        bemerk = translateExtended ("To Store", lvcarea, "") + " " + to_string(l_op.pos)


                    else:
                        bemerk = translateExtended ("Transform Out", lvcarea, "")


                    t_anz =  to_decimal(t_anz) - to_decimal(l_op.anzahl)
                    t_val =  to_decimal(t_val) - to_decimal(wert)


                    str_list2 = Str_list2()
                    str_list2_data.append(str_list2)

                    str_list2.m_unit = l_artikel.masseinheit
                    str_list2.datum = to_string(l_op.datum)
                    str_list2.lscheinnr = to_string(l_op.lscheinnr)
                    str_list2.init_qty = to_string(0)
                    str_list2.init_val = to_string(0)
                    str_list2.in_qty = to_string(0)
                    str_list2.in_val = to_string(0)
                    str_list2.out_qty = to_string(l_op.anzahl)
                    str_list2.out_val = to_string(wert)
                    str_list2.note = to_string(bemerk)
                    t_outgoing =  to_decimal(t_outgoing) + to_decimal(l_op.anzahl)
                    t_outval =  to_decimal(t_outval) + to_decimal(wert)

            if l_bestand:
                tot_anz =  to_decimal(tot_anz) + to_decimal(t_anz)
                tot_val =  to_decimal(tot_val) + to_decimal(t_val)

                if l_artikel.vk_preis != 0:
                    t_val =  to_decimal(t_anz) * to_decimal(l_artikel.vk_preis)


                str_list2 = Str_list2()
                str_list2_data.append(str_list2)

                str_list2.m_unit = l_artikel.masseinheit
                str_list2.datum = ""
                str_list2.lscheinnr = to_string(translateExtended ("Stock Onhand:", lvcarea, ""))
                str_list2.init_qty = to_string(t_anz)
                str_list2.init_val = to_string(t_val)


        str_list2 = Str_list2()
        str_list2_data.append(str_list2)

        str_list2 = Str_list2()
        str_list2_data.append(str_list2)


        if l_artikel.vk_preis != 0:
            t_wert =  to_decimal(t_qty) * to_decimal(l_artikel.vk_preis)


        str_list2.datum = ""
        str_list2.lscheinnr = "T O T A L : "
        str_list2.init_qty = to_string(t_qty)
        str_list2.init_val = to_string(t_wert)
        str_list2.in_qty = to_string(t_incoming)
        str_list2.in_val = to_string(t_inval)
        str_list2.out_qty = to_string(t_outgoing)
        str_list2.out_val = to_string(t_outval)

        if not it_exist:

            for l_ophis in db_session.query(L_ophis).filter(
                     (L_ophis.artnr == s_artnr) & (L_ophis.op_art == 1)).order_by(L_ophis.datum.desc()).all():
                last_date = l_ophis.datum


                break
            first_rec = True

            for l_ophis in db_session.query(L_ophis).filter(
                     (L_ophis.artnr == s_artnr) & (L_ophis.op_art == 1) & (L_ophis.datum == last_date)).order_by(L_ophis._recid).all():
                str_list2 = Str_list2()
                str_list2_data.append(str_list2)

                if first_rec:
                    str_list2.m_unit = l_artikel.masseinheit
                    str_list2.datum = to_string(l_ophis.datum)
                    str_list2.lscheinnr = to_string(translateExtended ("Last Receiving:", lvcarea, ""))
                    str_list2.in_qty = to_string(l_ophis.anzahl)
                    str_list2.in_val = to_string(l_ophis.warenwert)


                else:
                    str_list2.m_unit = l_artikel.masseinheit
                    str_list2.datum = to_string(l_ophis.datum)
                    str_list2.in_qty = to_string(l_ophis.anzahl)
                    str_list2.in_val = to_string(l_ophis.warenwert)


                first_rec = False

            for l_ophis in db_session.query(L_ophis).filter(
                     (L_ophis.artnr == s_artnr) & (L_ophis.op_art == 3)).order_by(L_ophis.datum.desc()).all():
                last_date = l_ophis.datum


                break
            first_rec = True

            for l_ophis in db_session.query(L_ophis).filter(
                     (L_ophis.artnr == s_artnr) & (L_ophis.op_art == 3) & (L_ophis.datum == last_date)).order_by(L_ophis._recid).all():
                str_list2 = Str_list2()
                str_list2_data.append(str_list2)

                if first_rec:
                    str_list2.m_unit = l_artikel.masseinheit
                    str_list2.datum = to_string(l_ophis.datum)
                    str_list2.lscheinnr = to_string(translateExtended ("Last Outgoing:", lvcarea, ""))
                    str_list2.out_qty = to_string(l_ophis.anzahl)
                    str_list2.out_val = to_string(l_ophis.warenwert)


                else:
                    str_list2.m_unit = l_artikel.masseinheit
                    str_list2.datum = to_string(l_ophis.datum)
                    str_list2.out_qty = to_string(l_ophis.anzahl)
                    str_list2.out_val = to_string(l_ophis.warenwert)

        return generate_inner_output()


    def add_id():

        nonlocal stock_movelist_data, lvcarea, tot_anz, tot_val, t_anz, t_val, long_digit, t_incoming, t_inval, t_outgoing, t_outval, htparam, l_artikel, bediener, l_bestand, l_op, l_ophdr, l_lager, l_lieferant, gl_acct, l_ophis
        nonlocal pvilanguage, s_artnr, show_price, from_lager, to_lager


        nonlocal str_list, str_list2, stock_movelist
        nonlocal str_list_data, str_list2_data, stock_movelist_data

        usr = None
        Usr =  create_buffer("Usr",Bediener)

        usr = get_cache (Bediener, {"nr": [(eq, l_op.fuellflag)]})

        if usr:
            str_list2.id = usr.userinit


        else:
            str_list2.id = "??"


    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})

    if htparam:
        long_digit = htparam.flogical

    l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})

    if not l_artikel:
        return generate_output()
    
    str_list2_data = create_list(pvilanguage, s_artnr, show_price, from_lager, to_lager)
    stock_movelist_data.clear()

    for str_list2 in query(str_list2_data):
        stock_movelist = Stock_movelist()
        stock_movelist_data.append(stock_movelist)

        # stock_movelist.datum = date_mdy(str_list2.datum)
        stock_movelist.datum = str_list2.datum
        stock_movelist.lscheinnr = str_list2.lscheinnr
        stock_movelist.init_qty =  to_decimal(to_decimal(str_list2.init_qty) )
        stock_movelist.init_val =  to_decimal(to_decimal(str_list2.init_val) )
        stock_movelist.in_qty =  to_decimal(to_decimal(str_list2.in_qty) )
        stock_movelist.in_val =  to_decimal(to_decimal(str_list2.in_val) )
        stock_movelist.out_qty =  to_decimal(to_decimal(str_list2.out_qty) )
        stock_movelist.out_val =  to_decimal(to_decimal(str_list2.out_val) )
        stock_movelist.note = str_list2.note
        stock_movelist.id = str_list2.id

    return generate_output()