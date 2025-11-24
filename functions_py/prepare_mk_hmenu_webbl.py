#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import H_menu, H_artikel, Htparam, Artikel, Queasy

payload_list_data, Payload_list = create_model("Payload_list", {"dept":int, "h_artnr":int, "menu_nr":int, "sorttype":int, "from_artnr":int, "from_bezeich":string})

def prepare_mk_hmenu_webbl(payload_list_data:[Payload_list]):

    prepare_cache ([H_menu, H_artikel, Htparam, Artikel, Queasy])

    hmenu_list_data = []
    menu_list_data = []
    q1_list_data = []
    q2_list_data = []
    nested_submenu:bool = False
    disc_art1:int = 0
    disc_art2:int = 0
    disc_art3:int = 0
    h_menu = h_artikel = htparam = artikel = queasy = None

    q1_list = q2_list = hmenu_list = menu_list = payload_list = h_art = h_art1 = h_art2 = None

    q1_list_data, Q1_list = create_model("Q1_list", {"artnr":int, "bezeich":string, "flag":bool})
    q2_list_data, Q2_list = create_model("Q2_list", {"artnr":int, "bezeich":string, "qty":Decimal})
    hmenu_list_data, Hmenu_list = create_model_like(H_menu)
    menu_list_data, Menu_list = create_model_like(H_menu)

    H_art = create_buffer("H_art",H_artikel)
    H_art1 = create_buffer("H_art1",H_artikel)
    H_art2 = create_buffer("H_art2",H_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal hmenu_list_data, menu_list_data, q1_list_data, q2_list_data, nested_submenu, disc_art1, disc_art2, disc_art3, h_menu, h_artikel, htparam, artikel, queasy
        nonlocal h_art, h_art1, h_art2


        nonlocal q1_list, q2_list, hmenu_list, menu_list, payload_list, h_art, h_art1, h_art2
        nonlocal q1_list_data, q2_list_data, hmenu_list_data, menu_list_data

        return {"hmenu-list": hmenu_list_data, "menu-list": menu_list_data, "q1-list": q1_list_data, "q2-list": q2_list_data}

    payload_list = query(payload_list_data, first=True)

    for h_menu in db_session.query(H_menu).filter(
             (H_menu.departement == payload_list.dept) & (H_menu.artnr == payload_list.h_artnr)).order_by(H_menu._recid).all():
        q1_list = Q1_list()
        q1_list_data.append(q1_list)

        q1_list.flag = True
        q1_list.bezeich = "Not Allowed"


        nested_submenu = True
        break

    if nested_submenu:

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})

    if htparam:
        disc_art1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 596)]})

    if htparam:
        disc_art2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 556)]})

    if htparam:
        disc_art3 = htparam.finteger

    for h_artikel in db_session.query(H_artikel).filter(
             (H_artikel.departement == payload_list.dept) & (H_artikel.artart == 0) & (H_artikel.betriebsnr == 0) & (H_artikel.artnr != payload_list.h_artnr) & ((H_artikel.artnr != disc_art1) | (H_artikel.artnr != disc_art2) | (H_artikel.artnr != disc_art3)) & (not_(matches(H_artikel.bezeich,"*tips*"))) & (H_artikel.activeflag)).order_by(H_artikel._recid).all():

        artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})

        if artikel:

            if artikel.artart == 9 and artikel.artgrp != 0:
                pass
            else:
                hmenu_list = Hmenu_list()
                hmenu_list_data.append(hmenu_list)

                hmenu_list.artnr = h_artikel.artnr

    if payload_list.menu_nr != 0:

        for h_menu in db_session.query(H_menu).filter(
                 (H_menu.departement == payload_list.dept) & (H_menu.nr == payload_list.menu_nr)).order_by(H_menu._recid).all():

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_menu.artnr)],"departement": [(eq, payload_list.dept)]})

            if h_artikel:
                menu_list = Menu_list()
                menu_list_data.append(menu_list)

                menu_list.nr = payload_list.menu_nr
                menu_list.artnr = h_artikel.artnr

                hmenu_list = query(hmenu_list_data, filters=(lambda hmenu_list: hmenu_list.artnr == menu_list.artnr), first=True)

                if hmenu_list:
                    hmenu_list_data.remove(hmenu_list)

    if payload_list.sorttype == 1:

        for hmenu_list in query(hmenu_list_data, filters=(lambda hmenu_list: hmenu_list.artnr >= payload_list.from_artnr)):

            h_art1 = get_cache (H_artikel, {"departement": [(eq, payload_list.dept)],"artnr": [(eq, hmenu_list.artnr)]})

            if h_art1:
                q1_list = Q1_list()
                q1_list_data.append(q1_list)

                q1_list.artnr = h_art1.artnr
                q1_list.bezeich = h_art1.bezeich


    else:

        for hmenu_list in query(hmenu_list_data):

            h_art1 = get_cache (H_artikel, {"departement": [(eq, payload_list.dept)],"artnr": [(eq, hmenu_list.artnr)],"bezeich": [(ge, payload_list.from_bezeich)]})

            if h_art1:
                q1_list = Q1_list()
                q1_list_data.append(q1_list)

                q1_list.artnr = h_art1.artnr
                q1_list.bezeich = h_art1.bezeich

    for menu_list in query(menu_list_data):

        h_art2 = get_cache (H_artikel, {"departement": [(eq, payload_list.dept)],"artnr": [(eq, menu_list.artnr)]})

        if h_art2:

            queasy = get_cache (Queasy, {"key": [(eq, 361)],"number2": [(eq, payload_list.dept)],"char1": [(eq, "qty-sub-menu")],"number3": [(eq, payload_list.menu_nr)],"number1": [(eq, menu_list.artnr)]})

            if queasy:
                q2_list = Q2_list()
                q2_list_data.append(q2_list)

                q2_list.artnr = h_art2.artnr
                q2_list.bezeich = h_art2.bezeich
                q2_list.qty =  to_decimal(queasy.deci1)


            else:
                pass

    return generate_output()