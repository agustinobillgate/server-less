from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import H_menu, H_artikel

def mk_hmenu_disp_itbl(hmenu_list:[Hmenu_list], menu_list:[Menu_list], sorttype:int, dept:int, from_artnr:int, from_bezeich:str):
    q1_list_list = []
    q2_list_list = []
    h_menu = h_artikel = None

    q1_list = q2_list = hmenu_list = menu_list = h_art1 = h_art2 = None

    q1_list_list, Q1_list = create_model("Q1_list", {"artnr":int, "bezeich":str})
    q2_list_list, Q2_list = create_model("Q2_list", {"artnr":int, "bezeich":str})
    hmenu_list_list, Hmenu_list = create_model_like(H_menu)
    menu_list_list, Menu_list = create_model_like(H_menu)

    H_art1 = H_artikel
    H_art2 = H_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_list, q2_list_list, h_menu, h_artikel
        nonlocal h_art1, h_art2


        nonlocal q1_list, q2_list, hmenu_list, menu_list, h_art1, h_art2
        nonlocal q1_list_list, q2_list_list, hmenu_list_list, menu_list_list
        return {"q1-list": q1_list_list, "q2-list": q2_list_list}


    if sorttype == 1:

        for hmenu_list in query(hmenu_list_list, filters=(lambda hmenu_list :hmenu_list.artnr >= from_artnr)):
            h_art1 = db_session.query(H_art1).filter((H_art1.departement == dept) &  (H_art1.artnr == hmenu_list.artnr)).first()
            if not h_art1:
                continue

            q1_list = Q1_list()
            q1_list_list.append(q1_list)

            q1_list.artnr = h_art1.artnr
            q1_list.bezeich = h_art1.bezeich

    else:

        for hmenu_list in query(hmenu_list_list):
            h_art1 = db_session.query(H_art1).filter((H_art1.departement == dept) &  (H_art1.artnr == hmenu_list.artnr) &  (func.lower(H_art1.bezeich) >= (from_bezeich).lower())).first()
            if not h_art1:
                continue

            q1_list = Q1_list()
            q1_list_list.append(q1_list)

            q1_list.artnr = h_art1.artnr
            q1_list.bezeich = h_art1.bezeich


    for menu_list in query(menu_list_list):
        h_art2 = db_session.query(H_art2).filter((H_art2.departement == dept) &  (H_art2.artnr == menu_list.artnr)).first()
        if not h_art2:
            continue

        q2_list = Q2_list()
        q2_list_list.append(q2_list)

        q2_list.artnr = h_art2.artnr
        q2_list.bezeich = h_art2.bezeich

    return generate_output()