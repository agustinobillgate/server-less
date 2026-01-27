#using conversion tools version: 1.0.0.119
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added

# Rulita, 19-01-2026
# - Fixing error validate query Queasy
#   From (Queasy.char1 == ("Qty-sub-menu"))
#   To (Queasy.char1 == ("fixed-sub-menu"))
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import H_menu, H_artikel, Queasy

hmenu_list_data, Hmenu_list = create_model_like(H_menu)
menu_list_data, Menu_list = create_model_like(H_menu, {"qty":Decimal})
payload_list_data, Payload_list = create_model("Payload_list", {"dept":int, "h_artnr":int})

def mk_hmenu_create_menu_webbl(hmenu_list_data:[Hmenu_list], menu_list_data:[Menu_list], payload_list_data:[Payload_list]):

    prepare_cache ([H_artikel])

    output_list_data = []
    h_menu = h_artikel = queasy = None

    hmenu_list = menu_list = output_list = payload_list = h_art = None

    output_list_data, Output_list = create_model("Output_list", {"menu_nr":int, "done":bool})

    H_art = create_buffer("H_art",H_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, h_menu, h_artikel, queasy
        nonlocal h_art


        nonlocal hmenu_list, menu_list, output_list, payload_list, h_art
        nonlocal output_list_data

        return {"output-list": output_list_data}

    def create_menu():

        nonlocal output_list_data, h_menu, h_artikel, queasy
        nonlocal h_art


        nonlocal hmenu_list, menu_list, output_list, payload_list, h_art
        nonlocal output_list_data

        nr:int = 0
        created:bool = False

        if not h_art or h_art.betriebsnr == 0:
            nr = get_nr()
        else:
            nr = h_art.betriebsnr

        output_list.menu_nr = nr

        if h_art and h_art.betriebsnr != 0:

            for h_menu in db_session.query(H_menu).filter(
                     (H_menu.departement == payload_list.dept) & (H_menu.nr == h_art.betriebsnr)).order_by(H_menu._recid).all():
                db_session.delete(h_menu)

            for queasy in db_session.query(Queasy).filter(
                     (Queasy.key == 361) & (Queasy.number2 == payload_list.dept) & (Queasy.char1 == ("Qty-Sub-Menu").lower()) & (Queasy.number3 == h_art.betriebsnr)).order_by(Queasy._recid).all():
                db_session.delete(queasy)

        for menu_list in query(menu_list_data):
            h_menu = H_menu()
            db_session.add(h_menu)

            h_menu.departement = payload_list.dept
            h_menu.nr = nr
            h_menu.artnr = menu_list.artnr


            pass
            created = True
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 361
            queasy.number1 = menu_list.artnr
            queasy.number2 = payload_list.dept
            queasy.number3 = nr
            queasy.deci1 =  to_decimal(menu_list.qty)
            queasy.char1 = "Qty-Sub-Menu"


            menu_list_data.remove(menu_list)
        output_list.done = True

        if not h_art:

            return

        if created and h_art.betriebsnr == 0:
            pass
            h_art.betriebsnr = nr
            pass

        elif not created and h_art.betriebsnr != 0:

            # queasy = get_cache (Queasy, {"key": [(eq, 361)],"number2": [(eq, payload_list.dept)],"char1": [(eq, "fixed-sub-menu")],"number3": [(eq, h_art.betriebsnr)]})

            # Rulita, 19-01-2026
            # - Fixing error validate query Queasy
            #   where char1 eq "Qty-sub-menu"
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 361) & (Queasy.number2 == payload_list.dept) & 
                     (Queasy.char1 == ("fixed-sub-menu")) & 
                     (Queasy.number3 == h_art.betriebsnr)).with_for_update().first()

            if queasy:
                pass
                db_session.delete(queasy)
            pass
            h_art.betriebsnr = 0
            pass
            output_list.menu_nr = 0


    def get_nr():

        nonlocal output_list_data, h_menu, h_artikel, queasy
        nonlocal h_art


        nonlocal hmenu_list, menu_list, output_list, payload_list, h_art
        nonlocal output_list_data

        nr = 0
        h_art = None

        def generate_inner_output():
            return (nr)

        H_art =  create_buffer("H_art",H_artikel)

        for h_art in db_session.query(H_art).filter(
                 (H_art.departement == payload_list.dept) & (H_art.betriebsnr != 0)).order_by(H_art._recid).all():

            if nr < h_art.betriebsnr:
                nr = h_art.betriebsnr
        nr = nr + 1

        return generate_inner_output()

    payload_list = query(payload_list_data, first=True)
    output_list = Output_list()
    output_list_data.append(output_list)


    # h_art = get_cache (H_artikel, {"departement": [(eq, payload_list.dept)],"artnr": [(eq, payload_list.h_artnr)]})
    h_art = db_session.query(H_artikel).filter(
             (H_artikel.departement == payload_list.dept) &
             (H_artikel.artnr == payload_list.h_artnr)).with_for_update().first()
    create_menu()

    return generate_output()