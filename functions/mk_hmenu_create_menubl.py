#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_menu, H_artikel

hmenu_list_data, Hmenu_list = create_model_like(H_menu)
menu_list_data, Menu_list = create_model_like(H_menu)

def mk_hmenu_create_menubl(hmenu_list_data:[Hmenu_list], menu_list_data:[Menu_list], menu_nr:int, dept:int, h_artnr:int):

    prepare_cache ([H_artikel])

    done = False
    h_menu = h_artikel = None

    hmenu_list = menu_list = h_art = None

    H_art = create_buffer("H_art",H_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal done, h_menu, h_artikel
        nonlocal menu_nr, dept, h_artnr
        nonlocal h_art


        nonlocal hmenu_list, menu_list, h_art

        return {"hmenu-list": hmenu_list_data, "menu-list": menu_list_data, "menu_nr": menu_nr, "done": done}

    def create_menu():

        nonlocal done, h_menu, h_artikel
        nonlocal menu_nr, dept, h_artnr
        nonlocal h_art


        nonlocal hmenu_list, menu_list, h_art

        nr:int = 0
        created:bool = False

        if not h_art or h_art.betriebsnr == 0:
            nr = get_nr()
        else:
            nr = h_art.betriebsnr
        menu_nr = nr

        if h_art and h_art.betriebsnr != 0:

            for h_menu in db_session.query(H_menu).filter(
                     (H_menu.departement == dept) & (H_menu.nr == h_art.betriebsnr)).order_by(H_menu._recid).all():
                db_session.delete(h_menu)


        for menu_list in query(menu_list_data):
            h_menu = H_menu()
            db_session.add(h_menu)

            h_menu.departement = dept
            h_menu.nr = nr
            h_menu.artnr = menu_list.artnr


            pass
            created = True
            menu_list_data.remove(menu_list)
        done = True

        if not h_art:

            return

        if created and h_art.betriebsnr == 0:
            pass
            h_art.betriebsnr = nr
            pass

        elif not created and h_art.betriebsnr != 0:
            pass
            h_art.betriebsnr = 0
            pass
            menu_nr = 0


    def get_nr():

        nonlocal done, h_menu, h_artikel
        nonlocal menu_nr, dept, h_artnr
        nonlocal h_art


        nonlocal hmenu_list, menu_list, h_art

        nr = 0
        h_art = None

        def generate_inner_output():
            return (nr)

        H_art =  create_buffer("H_art",H_artikel)

        for h_art in db_session.query(H_art).filter(
                 (H_art.departement == dept) & (H_art.betriebsnr != 0)).order_by(H_art._recid).all():

            if nr < h_art.betriebsnr:
                nr = h_art.betriebsnr
        nr = nr + 1

        return generate_inner_output()

    h_art = get_cache (H_artikel, {"departement": [(eq, dept)],"artnr": [(eq, h_artnr)]})
    create_menu()

    return generate_output()