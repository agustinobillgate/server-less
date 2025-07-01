#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, Bediener, H_rezept, H_rezlin, Htparam, L_artikel, L_bestand

op_list_list, Op_list = create_model_like(L_op, {"bezeich":string, "username":string})
t_op_list_list, T_op_list = create_model_like(Op_list)

def s_transform_get_recipe_webbl(pvilanguage:int, hrecipe_nr:int, qty:Decimal, curr_lager:int, transdate:date, bediener_nr:int, lscheinnr:string, t_op_list_list:[T_op_list]):

    prepare_cache ([Bediener, H_rezept, H_rezlin, Htparam, L_artikel, L_bestand])

    op_list_list = []
    err_flag = 0
    msg_str = ""
    anzahl:Decimal = to_decimal("0.0")
    stock_oh:Decimal = to_decimal("0.0")
    t_logical:bool = False
    lvcarea:string = "s-transform"
    l_op = bediener = h_rezept = h_rezlin = htparam = l_artikel = l_bestand = None

    op_list = t_op_list = sys_user = brezept = brezlin = None

    Sys_user = create_buffer("Sys_user",Bediener)
    Brezept = create_buffer("Brezept",H_rezept)
    Brezlin = create_buffer("Brezlin",H_rezlin)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal op_list_list, err_flag, msg_str, anzahl, stock_oh, t_logical, lvcarea, l_op, bediener, h_rezept, h_rezlin, htparam, l_artikel, l_bestand
        nonlocal pvilanguage, hrecipe_nr, qty, curr_lager, transdate, bediener_nr, lscheinnr
        nonlocal sys_user, brezept, brezlin


        nonlocal op_list, t_op_list, sys_user, brezept, brezlin
        nonlocal op_list_list

        return {"t-op-list": t_op_list_list, "err_flag": err_flag, "msg_str": msg_str}

    def create_op(recipe_no:int, menge:Decimal):

        nonlocal op_list_list, err_flag, msg_str, anzahl, stock_oh, t_logical, lvcarea, l_op, bediener, h_rezept, h_rezlin, htparam, l_artikel, l_bestand
        nonlocal pvilanguage, hrecipe_nr, qty, curr_lager, transdate, bediener_nr, lscheinnr
        nonlocal sys_user, brezept, brezlin


        nonlocal op_list, t_op_list, sys_user, brezept, brezlin
        nonlocal op_list_list

        brezept = get_cache (H_rezept, {"artnrrezept": [(eq, recipe_no)]})

        if brezept:

            for brezlin in db_session.query(Brezlin).filter(
                     (Brezlin.artnrrezept == recipe_no)).order_by(Brezlin._recid).all():

                if brezlin.recipe_flag :
                    create_op(brezlin.artnrlager, brezlin.menge)
                else:

                    l_artikel = get_cache (L_artikel, {"artnr": [(eq, brezlin.artnrlager)]})

                    if l_artikel:
                        anzahl =  to_decimal(qty) * to_decimal((menge) * to_decimal(((1) * to_decimal(brezlin.menge) / to_decimal(brezept.portion)) / to_decimal(l_artikel.inhalt)))

                        if anzahl == 0:
                            err_flag = 1

                            return

                        elif anzahl < 0:
                            err_flag = 2

                            return
                        else:

                            l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, curr_lager)],"artnr": [(eq, brezlin.artnrlager)]})

                            if l_bestand:
                                stock_oh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                            if anzahl > stock_oh:
                                msg_str = msg_str + chr_unicode(2) +\
                                        translateExtended ("Wrong quantity: ", lvcarea , "") +\
                                        to_string(l_artikel.artnr) + " - " +\
                                        l_artikel.bezeich +\
                                        chr_unicode(10) +\
                                        translateExtended ("Inputted quantity =", lvcarea, "") + " " +\
                                        to_string(anzahl, "->>>,>>>9.99") +\
                                        translateExtended (" - Stock onhand =", lvcarea, "") + " " +\
                                        to_string(stock_oh, "->>>,>>>9.99") +\
                                        chr_unicode(10) +\
                                        translateExtended (" From Recipe No =", lvcarea, "") + " " +\
                                        to_string(brezlin.artnrrezept, ">>>>>>>>9") +\
                                        chr_unicode(10) +\
                                        translateExtended ("POSTING NOT POSSIBLE", lvcarea, "")

                                return
                        op_list = Op_list()
                        op_list_list.append(op_list)

                        op_list.datum = transdate
                        op_list.lager_nr = curr_lager
                        op_list.artnr = brezlin.artnrlager
                        op_list.zeit = get_current_time_in_seconds()
                        op_list.anzahl =  to_decimal(anzahl)
                        op_list.einzelpreis =  to_decimal(l_artikel.vk_preis)
                        op_list.warenwert =  to_decimal(anzahl) * to_decimal(l_artikel.vk_preis)
                        op_list.op_art = 4
                        op_list.herkunftflag = 3
                        op_list.lscheinnr = lscheinnr
                        op_list.fuellflag = bediener_nr
                        op_list.pos = 1
                        op_list.bezeich = l_artikel.bezeich

    htparam = get_cache (Htparam, {"paramnr": [(eq, 232)]})

    if htparam:
        t_logical = htparam.flogical

    if t_logical:
        err_flag = 3

        return generate_output()

    h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, hrecipe_nr)]})

    if h_rezept:

        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == hrecipe_nr)).order_by(H_rezlin._recid).all():

            if h_rezlin.recipe_flag :
                create_op(h_rezlin.artnrlager, h_rezlin.menge)
            else:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_rezlin.artnrlager)]})

                if l_artikel:
                    anzahl =  to_decimal(qty) * to_decimal(((1) * to_decimal(h_rezlin.menge) / to_decimal(h_rezept.portion)) / to_decimal(l_artikel.inhalt))

                    if anzahl == 0:
                        err_flag = 1

                        return generate_output()

                    elif anzahl < 0:
                        err_flag = 2

                        return generate_output()
                    else:

                        l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, curr_lager)],"artnr": [(eq, h_rezlin.artnrlager)]})

                        if l_bestand:
                            stock_oh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                        if anzahl > stock_oh:
                            msg_str = msg_str + chr_unicode(2) +\
                                    translateExtended ("Wrong quantity: ", lvcarea , "") +\
                                    to_string(l_artikel.artnr) + " - " +\
                                    l_artikel.bezeich +\
                                    chr_unicode(10) +\
                                    translateExtended ("Inputted quantity =", lvcarea, "") + " " +\
                                    to_string(anzahl, "->>>,>>>9.99") +\
                                    translateExtended (" - Stock onhand =", lvcarea, "") + " " +\
                                    to_string(stock_oh, "->>>,>>>9.99") +\
                                    chr_unicode(10) +\
                                    translateExtended (" From Recipe No =", lvcarea, "") + " " +\
                                    to_string(h_rezlin.artnrrezept, ">>>>>>>>9") +\
                                    chr_unicode(10) +\
                                    translateExtended ("POSTING NOT POSSIBLE", lvcarea, "")

                            return generate_output()
                    op_list = Op_list()
                    op_list_list.append(op_list)

                    op_list.datum = transdate
                    op_list.lager_nr = curr_lager
                    op_list.artnr = h_rezlin.artnrlager
                    op_list.zeit = get_current_time_in_seconds()
                    op_list.anzahl =  to_decimal(anzahl)
                    op_list.einzelpreis =  to_decimal(l_artikel.vk_preis)
                    op_list.warenwert =  to_decimal(anzahl) * to_decimal(l_artikel.vk_preis)
                    op_list.op_art = 4
                    op_list.herkunftflag = 3
                    op_list.lscheinnr = lscheinnr
                    op_list.fuellflag = bediener_nr
                    op_list.pos = 1
                    op_list.bezeich = l_artikel.bezeich

    for op_list in query(op_list_list):

        sys_user = get_cache (Bediener, {"nr": [(eq, op_list.fuellflag)]})
        t_op_list = T_op_list()
        t_op_list_list.append(t_op_list)

        buffer_copy(op_list, t_op_list)
        t_op_list.username = sys_user.username

    return generate_output()