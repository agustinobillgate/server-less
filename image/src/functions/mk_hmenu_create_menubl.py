from functions.additional_functions import *
import decimal
from models import H_menu, H_artikel

def mk_hmenu_create_menubl(hmenu_list:[Hmenu_list], menu_list:[Menu_list], menu_nr:int, dept:int, h_artnr:int):
    done = False
    h_menu = h_artikel = None

    hmenu_list = menu_list = h_art = None

    hmenu_list_list, Hmenu_list = create_model_like(H_menu)
    menu_list_list, Menu_list = create_model_like(H_menu)

    H_art = H_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal done, h_menu, h_artikel
        nonlocal h_art


        nonlocal hmenu_list, menu_list, h_art
        nonlocal hmenu_list_list, menu_list_list
        return {"done": done}

    def create_menu():

        nonlocal done, h_menu, h_artikel
        nonlocal h_art


        nonlocal hmenu_list, menu_list, h_art
        nonlocal hmenu_list_list, menu_list_list

        nr:int = 0
        created:bool = False

        if not h_art or h_art.betriebsnr == 0:
            nr = get_nr()
        else:
            nr = h_art.betriebsnr
        menu_nr = nr

        if h_art and h_art.betriebsnr != 0:

            for h_menu in db_session.query(H_menu).filter(
                    (H_menu.departement == dept) &  (H_menu.nr == h_art.betriebsnr)).all():
                db_session.delete(h_menu)


        for menu_list in query(menu_list_list):
            h_menu = H_menu()
            db_session.add(h_menu)

            h_menu.departement = dept
            h_menu.nr = nr
            h_menu.artnr = menu_list.artnr

            created = True
            menu_list_list.remove(menu_list)
        done = True

        if not h_art:

            return

        if created and h_art.betriebsnr == 0:

            h_art = db_session.query(H_art).first()
            h_art.betriebsnr = nr

            h_art = db_session.query(H_art).first()

        elif not created and h_art.betriebsnr != 0:

            h_art = db_session.query(H_art).first()
            h_art.betriebsnr = 0

            h_art = db_session.query(H_art).first()
            menu_nr = 0

    def get_nr():

        nonlocal done, h_menu, h_artikel
        nonlocal h_art


        nonlocal hmenu_list, menu_list, h_art
        nonlocal hmenu_list_list, menu_list_list

        nr = 0

        def generate_inner_output():
            return nr
        H_art = H_artikel

        for h_art in db_session.query(H_art).filter(
                (H_art.departement == dept) &  (H_art.betriebsnr != 0)).all():

            if nr < h_art.betriebsnr:
                nr = h_art.betriebsnr
        nr = nr + 1


        return generate_inner_output()


    h_art = db_session.query(H_art).filter(
            (H_art.departement == dept) &  (H_art.artnr == h_artnr)).first()
    create_menu()

    return generate_output()