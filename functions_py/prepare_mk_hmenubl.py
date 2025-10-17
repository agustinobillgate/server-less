#using conversion tools version: 1.0.0.117

# =======================================
# Rulita, 17-10-2025 
# Tiket ID : 6526C2 | New compile program
# =======================================

from functions.additional_functions import *
from decimal import Decimal
from models import H_menu, H_artikel

def prepare_mk_hmenubl(dept:int, h_artnr:int, menu_nr:int, sorttype:int, from_artnr:int, from_bezeich:string):

    prepare_cache ([H_menu, H_artikel])

    hmenu_list_data = []
    menu_list_data = []
    q1_list_data = []
    q2_list_data = []
    h_menu = h_artikel = None

    q1_list = q2_list = hmenu_list = menu_list = h_art = h_art1 = h_art2 = None

    q1_list_data, Q1_list = create_model("Q1_list", {"artnr":int, "bezeich":string})
    q2_list_data, Q2_list = create_model("Q2_list", {"artnr":int, "bezeich":string})
    hmenu_list_data, Hmenu_list = create_model_like(H_menu)
    menu_list_data, Menu_list = create_model_like(H_menu)

    H_art = create_buffer("H_art",H_artikel)
    H_art1 = create_buffer("H_art1",H_artikel)
    H_art2 = create_buffer("H_art2",H_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal hmenu_list_data, menu_list_data, q1_list_data, q2_list_data, h_menu, h_artikel
        nonlocal dept, h_artnr, menu_nr, sorttype, from_artnr, from_bezeich
        nonlocal h_art, h_art1, h_art2


        nonlocal q1_list, q2_list, hmenu_list, menu_list, h_art, h_art1, h_art2
        nonlocal q1_list_data, q2_list_data, hmenu_list_data, menu_list_data

        return {"hmenu-list": hmenu_list_data, "menu-list": menu_list_data, "q1-list": q1_list_data, "q2-list": q2_list_data}


    for h_artikel in db_session.query(H_artikel).filter(
             (H_artikel.departement == dept) & (H_artikel.artart == 0) & (H_artikel.betriebsnr == 0) & (H_artikel.artnr != h_artnr) & (H_artikel.activeflag)).order_by(H_artikel._recid).all():
        hmenu_list = Hmenu_list()
        hmenu_list_data.append(hmenu_list)

        hmenu_list.artnr = h_artikel.artnr

    if menu_nr != 0:

        for h_menu in db_session.query(H_menu).filter(
                 (H_menu.departement == dept) & (H_menu.nr == menu_nr)).order_by(H_menu._recid).all():

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_menu.artnr)],"departement": [(eq, dept)]})

            if h_artikel:
                menu_list = Menu_list()
                menu_list_data.append(menu_list)

                menu_list.nr = menu_nr
                menu_list.artnr = h_artikel.artnr

                hmenu_list = query(hmenu_list_data, filters=(lambda hmenu_list: hmenu_list.artnr == menu_list.artnr), first=True)

                if hmenu_list:
                    hmenu_list_data.remove(hmenu_list)


    if sorttype == 1:

        for hmenu_list in query(hmenu_list_data, filters=(lambda hmenu_list: hmenu_list.artnr >= from_artnr)):

            h_art1 = get_cache (H_artikel, {"departement": [(eq, dept)],"artnr": [(eq, hmenu_list.artnr)]})

            if h_art1:
                q1_list = Q1_list()
                q1_list_data.append(q1_list)

                q1_list.artnr = h_art1.artnr
                q1_list.bezeich = h_art1.bezeich

    else:

        for hmenu_list in query(hmenu_list_data):

            h_art1 = get_cache (H_artikel, {"departement": [(eq, dept)],"artnr": [(eq, hmenu_list.artnr)],"bezeich": [(ge, from_bezeich)]})

            if h_art1:
                q1_list = Q1_list()
                q1_list_data.append(q1_list)

                q1_list.artnr = h_art1.artnr
                q1_list.bezeich = h_art1.bezeich


    for menu_list in query(menu_list_data):

        h_art2 = get_cache (H_artikel, {"departement": [(eq, dept)],"artnr": [(eq, menu_list.artnr)]})

        if h_art2:
            q2_list = Q2_list()
            q2_list_data.append(q2_list)

            q2_list.artnr = h_art2.artnr
            q2_list.bezeich = h_art2.bezeich

    return generate_output()