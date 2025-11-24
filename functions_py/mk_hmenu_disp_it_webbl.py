#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from models import H_menu, H_artikel, Htparam

payload_list_data, Payload_list = create_model("Payload_list", {"sorttype":int, "dept":int, "from_artnr":int, "from_bezeich":string, "mode":int, "menu_nr":int})
hmenu_list_data, Hmenu_list = create_model_like(H_menu)
menu_list_data, Menu_list = create_model_like(H_menu, {"qty":Decimal})

def mk_hmenu_disp_it_webbl(payload_list_data:[Payload_list], hmenu_list_data:[Hmenu_list], menu_list_data:[Menu_list]):

    prepare_cache ([H_artikel, Htparam])

    q1_list_data = []
    q2_list_data = []
    disc_art1:int = 0
    disc_art2:int = 0
    disc_art3:int = 0
    tips_art:int = 0
    h_menu = h_artikel = htparam = None

    q1_list = q2_list = hmenu_list = menu_list = payload_list = h_art1 = h_art2 = None

    q1_list_data, Q1_list = create_model("Q1_list", {"artnr":int, "bezeich":string})
    q2_list_data, Q2_list = create_model("Q2_list", {"artnr":int, "bezeich":string, "qty":Decimal})

    H_art1 = create_buffer("H_art1",H_artikel)
    H_art2 = create_buffer("H_art2",H_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_data, q2_list_data, disc_art1, disc_art2, disc_art3, tips_art, h_menu, h_artikel, htparam
        nonlocal h_art1, h_art2


        nonlocal q1_list, q2_list, hmenu_list, menu_list, payload_list, h_art1, h_art2
        nonlocal q1_list_data, q2_list_data

        return {"q1-list": q1_list_data, "q2-list": q2_list_data}

    payload_list = query(payload_list_data, first=True)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})

    if htparam:
        disc_art1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 596)]})

    if htparam:
        disc_art2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 556)]})

    if htparam:
        disc_art3 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 856)]})

    if htparam:
        tips_art = htparam.finteger

    if payload_list.mode == 1:

        if payload_list.sorttype == 1:

            h_art1_obj_list = {}
            for h_art1 in db_session.query(H_art1).filter(
                     ((H_art1.departement.in_(list(set([payload_list.dept for payload_list in payload_list_data if hmenu_list.artnr >= payload_list.from_artnr])))) & (H_art1.artnr == hmenu_list.artnr))).order_by(hmenu_list.artnr).all():
                
                if h_art1_obj_list.get(h_art1._recid):
                    continue
                else:
                    h_art1_obj_list[h_art1._recid] = True


                q1_list = Q1_list()
                q1_list_data.append(q1_list)

                q1_list.artnr = h_art1.artnr
                q1_list.bezeich = h_art1.bezeich


        else:

            h_art1_obj_list = {}
            for h_art1 in db_session.query(H_art1).filter(
                     ((H_art1.departement.in_(list(set([payload_list.dept for payload_list in payload_list_data])))) & (H_art1.artnr == hmenu_list.artnr) & (H_art1.bezeich >= payload_list.from_bezeich))).order_by(H_art1.bezeich).all():
                
                if h_art1_obj_list.get(h_art1._recid):
                    continue
                else:
                    h_art1_obj_list[h_art1._recid] = True


                q1_list = Q1_list()
                q1_list_data.append(q1_list)

                q1_list.artnr = h_art1.artnr
                q1_list.bezeich = h_art1.bezeich

        h_art2_obj_list = {}
        for h_art2 in db_session.query(H_art2).filter(
                 ((H_art2.departement.in_(list(set([payload_list.dept for payload_list in payload_list_data])))) & (H_art2.artnr == menu_list.artnr))).order_by(H_art2.zwkum, menu_list.artnr).all():
            
            if h_art2_obj_list.get(h_art2._recid):
                continue
            else:
                h_art2_obj_list[h_art2._recid] = True


            q2_list = Q2_list()
            q2_list_data.append(q2_list)

            q2_list.artnr = h_art2.artnr
            q2_list.bezeich = h_art2.bezeich
            q2_list.qty =  to_decimal(menu_list.qty)


    else:
        q2_list = Q2_list()
        q2_list_data.append(q2_list)

        q2_list.artnr = disc_art1


        q2_list = Q2_list()
        q2_list_data.append(q2_list)

        q2_list.artnr = disc_art2


        q2_list = Q2_list()
        q2_list_data.append(q2_list)

        q2_list.artnr = disc_art3


        q2_list = Q2_list()
        q2_list_data.append(q2_list)

        q2_list.artnr = tips_art

        if payload_list.menu_nr == 0:

            return generate_output()

        h_menu_obj_list = {}
        for h_menu, h_artikel in db_session.query(H_menu, H_artikel).join(H_artikel,(H_artikel.artnr == H_menu.artnr)).filter(
                 (H_menu.nr == payload_list.menu_nr)).order_by(H_menu._recid).all():
            
            if h_menu_obj_list.get(h_menu._recid):
                continue
            else:
                h_menu_obj_list[h_menu._recid] = True


            q1_list = Q1_list()
            q1_list_data.append(q1_list)

            q1_list.bezeich = h_artikel.bezeich

    return generate_output()