from functions.additional_functions import *
import decimal
from datetime import date
from models import L_op, Bediener, H_rezept, H_rezlin, Htparam, L_artikel, L_bestand

def s_transform_get_recipebl(pvilanguage:int, hrecipe_nr:int, qty:decimal, curr_lager:int, transdate:date, bediener_nr:int, lscheinnr:str, t_op_list:[T_op_list]):
    err_flag = 0
    msg_str = ""
    anzahl:decimal = 0
    stock_oh:decimal = 0
    t_logical:bool = False
    lvcarea:str = "s_transform"
    l_op = bediener = h_rezept = h_rezlin = htparam = l_artikel = l_bestand = None

    op_list = t_op_list = sys_user = brezept = brezlin = None

    op_list_list, Op_list = create_model_like(L_op, {"bezeich":str, "username":str})
    t_op_list_list, T_op_list = create_model_like(Op_list)

    Sys_user = Bediener
    Brezept = H_rezept
    Brezlin = H_rezlin

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, msg_str, anzahl, stock_oh, t_logical, lvcarea, l_op, bediener, h_rezept, h_rezlin, htparam, l_artikel, l_bestand
        nonlocal sys_user, brezept, brezlin


        nonlocal op_list, t_op_list, sys_user, brezept, brezlin
        nonlocal op_list_list, t_op_list_list
        return {"err_flag": err_flag, "msg_str": msg_str}

    def create_op(recipe_no:int, menge:decimal):

        nonlocal err_flag, msg_str, anzahl, stock_oh, t_logical, lvcarea, l_op, bediener, h_rezept, h_rezlin, htparam, l_artikel, l_bestand
        nonlocal sys_user, brezept, brezlin


        nonlocal op_list, t_op_list, sys_user, brezept, brezlin
        nonlocal op_list_list, t_op_list_list

        brezept = db_session.query(Brezept).filter(
                (Brezept.artnrrezept == recipe_no)).first()

        if brezept:

            for brezlin in db_session.query(Brezlin).filter(
                    (Brezlin.artnrrezept == recipe_no)).all():

                if brezlin.recipe_flag :
                    create_op(brezlin.artnrlager, brezlin.menge)
                else:

                    l_artikel = db_session.query(L_artikel).filter(
                            (L_artikel.artnr == brezlin.artnrlager)).first()

                    if l_artikel:
                        anzahl = qty * (menge * ((1 * brezlin.menge / brezept.portion) / l_artikel.inhalt))

                        if anzahl == 0:
                            err_flag = 1

                            return

                        elif anzahl < 0:
                            err_flag = 2

                            return
                        else:

                            l_bestand = db_session.query(L_bestand).filter(
                                    (L_bestand.lager_nr == curr_lager) &  (L_bestand.artnr == brezlin.artnrlager)).first()

                            if l_bestand:
                                stock_oh = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

                            if anzahl > stock_oh:
                                msg_str = msg_str + chr(2) +\
                                        translateExtended ("Wrong quantity: ", lvcarea , "") +\
                                        to_string(l_artikel.artnr) + " - " +\
                                        l_artikel.bezeich +\
                                        chr(10) +\
                                        translateExtended ("Inputted quantity  == ", lvcarea, "") + " " +\
                                        to_string(anzahl, "->>>,>>>9.99") +\
                                        translateExtended (" - Stock onhand  == ", lvcarea, "") + " " +\
                                        to_string(stock_oh, "->>>,>>>9.99") +\
                                        chr(10) +\
                                        translateExtended (" From Recipe No  == ", lvcarea, "") + " " +\
                                        to_string(brezlin.artnrrezept, ">>>>>>>>9") +\
                                        chr(10) +\
                                        translateExtended ("POSTING NOT POSSIBLE", lvcarea, "")

                                return
                        op_list = Op_list()
                        op_list_list.append(op_list)

                        op_list.datum = transdate
                        op_list.lager_nr = curr_lager
                        op_list.artnr = brezlin.artnrlager
                        op_list.zeit = get_current_time_in_seconds()
                        op_list.anzahl = anzahl
                        op_list.einzelpreis = l_artikel.vk_preis
                        op_list.warenwert = anzahl * l_artikel.vk_preis
                        op_list.op_art = 4
                        op_list.herkunftflag = 3
                        op_list.lscheinnr = lscheinnr
                        op_list.fuellflag = bediener_nr
                        op_list.pos = 1
                        op_list.bezeich = l_artikel.bezeich


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 232)).first()

    if htparam:
        t_logical = htparam.flogical

    if t_logical:
        err_flag = 3

        return generate_output()

    h_rezept = db_session.query(H_rezept).filter(
            (H_rezept.artnrrezept == hrecipe_nr)).first()

    if h_rezept:

        for h_rezlin in db_session.query(H_rezlin).filter(
                (H_rezlin.artnrrezept == hrecipe_nr)).all():

            if h_rezlin.recipe_flag :
                create_op(h_rezlin.artnrlager, h_rezlin.menge)
            else:

                l_artikel = db_session.query(L_artikel).filter(
                        (L_artikel.artnr == h_rezlin.artnrlager)).first()

                if l_artikel:
                    anzahl = qty * ((1 * h_rezlin.menge / h_rezept.portion) / l_artikel.inhalt)

                    if anzahl == 0:
                        err_flag = 1

                        return generate_output()

                    elif anzahl < 0:
                        err_flag = 2

                        return generate_output()
                    else:

                        l_bestand = db_session.query(L_bestand).filter(
                                (L_bestand.lager_nr == curr_lager) &  (L_bestand.artnr == h_rezlin.artnrlager)).first()

                        if l_bestand:
                            stock_oh = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

                        if anzahl > stock_oh:
                            msg_str = msg_str + chr(2) +\
                                    translateExtended ("Wrong quantity: ", lvcarea , "") +\
                                    to_string(l_artikel.artnr) + " - " +\
                                    l_artikel.bezeich +\
                                    chr(10) +\
                                    translateExtended ("Inputted quantity  == ", lvcarea, "") + " " +\
                                    to_string(anzahl, "->>>,>>>9.99") +\
                                    translateExtended (" - Stock onhand  == ", lvcarea, "") + " " +\
                                    to_string(stock_oh, "->>>,>>>9.99") +\
                                    chr(10) +\
                                    translateExtended (" From Recipe No  == ", lvcarea, "") + " " +\
                                    to_string(h_rezlin.artnrrezept, ">>>>>>>>9") +\
                                    chr(10) +\
                                    translateExtended ("POSTING NOT POSSIBLE", lvcarea, "")

                            return generate_output()
                    op_list = Op_list()
                    op_list_list.append(op_list)

                    op_list.datum = transdate
                    op_list.lager_nr = curr_lager
                    op_list.artnr = h_rezlin.artnrlager
                    op_list.zeit = get_current_time_in_seconds()
                    op_list.anzahl = anzahl
                    op_list.einzelpreis = l_artikel.vk_preis
                    op_list.warenwert = anzahl * l_artikel.vk_preis
                    op_list.op_art = 4
                    op_list.herkunftflag = 3
                    op_list.lscheinnr = lscheinnr
                    op_list.fuellflag = bediener_nr
                    op_list.pos = 1
                    op_list.bezeich = l_artikel.bezeich

    for op_list in query(op_list_list):

        sys_user = db_session.query(Sys_user).filter(
                (Sys_user.nr == op_list.fuellflag)).first()
        t_op_list = T_op_list()
        t_op_list_list.append(t_op_list)

        buffer_copy(op_list, t_op_list)
        t_op_list.username = sys_user.username

    return generate_output()