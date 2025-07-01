#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_menu, H_artikel

hmenu_list_list, Hmenu_list = create_model_like(H_menu)
menu_list_list, Menu_list = create_model_like(H_menu)

def mk_hmenu_disp_itbl(hmenu_list_list:[Hmenu_list], menu_list_list:[Menu_list], sorttype:int, dept:int, from_artnr:int, from_bezeich:string):

    prepare_cache ([H_artikel])

    q1_list_list = []
    q2_list_list = []
    h_menu = h_artikel = None

    q1_list = q2_list = hmenu_list = menu_list = h_art1 = h_art2 = None

    q1_list_list, Q1_list = create_model("Q1_list", {"artnr":int, "bezeich":string})
    q2_list_list, Q2_list = create_model("Q2_list", {"artnr":int, "bezeich":string})

    H_art1 = create_buffer("H_art1",H_artikel)
    H_art2 = create_buffer("H_art2",H_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_list, q2_list_list, h_menu, h_artikel
        nonlocal sorttype, dept, from_artnr, from_bezeich
        nonlocal h_art1, h_art2


        nonlocal q1_list, q2_list, hmenu_list, menu_list, h_art1, h_art2
        nonlocal q1_list_list, q2_list_list

        return {"hmenu-list": hmenu_list_list, "menu-list": menu_list_list, "q1-list": q1_list_list, "q2-list": q2_list_list}


    if sorttype == 1:

        h_art1_obj_list = {}
        for h_art1 in db_session.query(H_art1).filter(
                 ((H_art1.departement.in_(list(set([hmenu_list.dept for hmenu_list in hmenu_list_list if hmenu_list.artnr >= from_artnr])))) & (H_art1.artnr == hmenu_list.artnr))).order_by(hmenu_list.artnr).all():
            if h_art1_obj_list.get(h_art1._recid):
                continue
            else:
                h_art1_obj_list[h_art1._recid] = True

            hmenu_list = query(hmenu_list_list, (lambda hmenu_list: (h_art1.departement == dept)), first=True)
            q1_list = Q1_list()
            q1_list_list.append(q1_list)

            q1_list.artnr = h_art1.artnr
            q1_list.bezeich = h_art1.bezeich

    else:

        h_art1_obj_list = {}
        for h_art1 in db_session.query(H_art1).filter(
                 ((H_art1.departement.in_(list(set([hmenu_list.dept for hmenu_list in hmenu_list_list])))) & (H_art1.artnr == hmenu_list.artnr) & (H_art1.bezeich >= (from_bezeich).lower()))).order_by(H_art1.bezeich).all():
            if h_art1_obj_list.get(h_art1._recid):
                continue
            else:
                h_art1_obj_list[h_art1._recid] = True

            hmenu_list = query(hmenu_list_list, (lambda hmenu_list: (h_art1.departement == dept)), first=True)
            q1_list = Q1_list()
            q1_list_list.append(q1_list)

            q1_list.artnr = h_art1.artnr
            q1_list.bezeich = h_art1.bezeich


    h_art2_obj_list = {}
    for h_art2 in db_session.query(H_art2).filter(
             ((H_art2.departement.in_(list(set([menu_list.dept for menu_list in menu_list_list])))) & (H_art2.artnr == menu_list.artnr))).order_by(H_art2.zwkum, menu_list.artnr).all():
        if h_art2_obj_list.get(h_art2._recid):
            continue
        else:
            h_art2_obj_list[h_art2._recid] = True


        q2_list = Q2_list()
        q2_list_list.append(q2_list)

        q2_list.artnr = h_art2.artnr
        q2_list.bezeich = h_art2.bezeich

    return generate_output()