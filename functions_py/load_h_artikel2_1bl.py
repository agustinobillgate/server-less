#using conversion tools version: 1.0.0.117
# pyright: reportAttributeAccessIssue=false

"""_yusufwijasena_

    TICKET ID:
    ISSUE:  - fix definition variabel
            - fix python indentation
            - add type ignore to avoid warning
            - activate model H_menu, Wgrpdep, H_artikel
            - change to_string() = str()
""" 

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel, Wgrpdep, H_menu

def load_h_artikel2_1bl(case_type:int, dept:int, arttype:int, int1:int):
    t_h_artikel_data = []
    t_wgrpdep_data = []
    t_h_menu_data = []
    t_menu_list_data = []
    
    h_menu = H_menu()
    wgrpdep = Wgrpdep()
    h_artikel = H_artikel()

    t_h_artikel = t_wgrpdep = t_h_menu = t_menu_list = hart = None

    t_h_artikel_data, T_h_artikel = create_model_like(H_artikel)
    t_wgrpdep_data, T_wgrpdep = create_model_like(Wgrpdep)
    t_h_menu_data, T_h_menu = create_model_like(H_menu)
    t_menu_list_data, T_menu_list = create_model(
        "T_menu_list", {
            "artnr":int, 
            "zknr":int, 
            "bezeich":string, 
            "selected":bool, 
            "request":string
            }
        )

    Hart = create_buffer("Hart",H_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_h_artikel_data, t_wgrpdep_data, t_h_menu_data, t_menu_list_data, h_artikel, wgrpdep, h_menu
        nonlocal case_type, dept, arttype, int1
        nonlocal hart


        nonlocal t_h_artikel, t_wgrpdep, t_h_menu, t_menu_list, hart
        nonlocal t_h_artikel_data, t_wgrpdep_data, t_h_menu_data, t_menu_list_data

        return {
            "t-h-artikel": t_h_artikel_data, 
            "t-wgrpdep": t_wgrpdep_data, 
            "t-h-menu": t_h_menu_data, 
            "t-menu-list": t_menu_list_data}


    if case_type == 1:
        for h_artikel in db_session.query(H_artikel).filter(
            (H_artikel.departement == dept) & (H_artikel.artart == arttype) & (H_artikel.activeflag)).order_by(H_artikel._recid).all():

            if h_artikel.artnr == 0:
                hart = db_session.query(Hart).filter(
                    (Hart._recid == h_artikel._recid)).first()
                db_session.delete(hart)
            
            else:
                t_h_artikel = T_h_artikel()
                t_h_artikel_data.append(t_h_artikel)
                buffer_copy(h_artikel, t_h_artikel)
                
                wgrpdep = get_cache (Wgrpdep, {
                    "departement": [(eq, dept)],
                    "zknr": [(eq, h_artikel.zwkum)]})

                if wgrpdep:
                    t_wgrpdep = query(t_wgrpdep_data, filters=(lambda t_wgrpdep: t_wgrpdep.zknr == wgrpdep.zknr), first=True)

                    if not t_wgrpdep:
                        t_wgrpdep = T_wgrpdep()
                        t_wgrpdep_data.append(t_wgrpdep)

                        buffer_copy(wgrpdep, t_wgrpdep)
                
                else:
                    t_wgrpdep = query(t_wgrpdep_data, filters=(lambda t_wgrpdep: t_wgrpdep.zknr == h_artikel.zwkum), first=True)

                    if not t_wgrpdep:
                        t_wgrpdep = T_wgrpdep()
                        t_wgrpdep_data.append(t_wgrpdep)

                        t_wgrpdep.zknr = h_artikel.zwkum
                        t_wgrpdep.bezeich = str(h_artikel.zwkum) + " - NOT DEFINED!!"

        for h_menu in db_session.query(H_menu).order_by(H_menu._recid).all():
            t_h_menu = T_h_menu()
            t_h_menu_data.append(t_h_menu)

            buffer_copy(h_menu, t_h_menu)

    elif case_type == 2:

        for h_artikel in db_session.query(H_artikel).filter(
            (H_artikel.departement == dept) & (H_artikel.artart == arttype) & (H_artikel.activeflag)).order_by(H_artikel._recid).all():

            if h_artikel.artnr == 0:

                hart = db_session.query(Hart).filter(
                    (Hart._recid == h_artikel._recid)).first()
                db_session.delete(hart)
                
            else:
                t_h_artikel = T_h_artikel()
                t_h_artikel_data.append(t_h_artikel)

                buffer_copy(h_artikel, t_h_artikel)

                wgrpdep = get_cache (Wgrpdep, {
                    "departement": [(eq, dept)],
                    "zknr": [(eq, h_artikel.zwkum)]})

                if wgrpdep:
                    t_wgrpdep = query(t_wgrpdep_data, filters=(lambda t_wgrpdep: t_wgrpdep.zknr == wgrpdep.zknr), first=True)

                    if not t_wgrpdep:
                        t_wgrpdep = T_wgrpdep()
                        t_wgrpdep_data.append(t_wgrpdep)

                        buffer_copy(wgrpdep, t_wgrpdep)
                else:

                    t_wgrpdep = query(t_wgrpdep_data, filters=(lambda t_wgrpdep: t_wgrpdep.zknr == h_artikel.zwkum), first=True)

                    if not t_wgrpdep:
                        t_wgrpdep = T_wgrpdep()
                        t_wgrpdep_data.append(t_wgrpdep)

                        t_wgrpdep.zknr = h_artikel.zwkum
                        t_wgrpdep.bezeich = str(h_artikel.zwkum) + " - NOT DEFINED!!"

        h_menu_obj_list = {}
        for h_menu in db_session.query(H_menu).filter(
                (H_menu.departement == dept) & (H_menu.nr == int1)).order_by(t_h_artikel.zwkum).all():  # type: ignore t_h_artikel.zwkum
            t_h_artikel = query(t_h_artikel_data, (lambda t_h_artikel: t_h_artikel.artnr == h_menu.artnr), first=True) 
            if not t_h_artikel:
                continue

            if h_menu_obj_list.get(h_menu._recid):
                continue
            else:
                h_menu_obj_list[h_menu._recid] = True


            t_menu_list = T_menu_list()
            t_menu_list_data.append(t_menu_list)

            t_menu_list.artnr = t_h_artikel.artnr
            t_menu_list.zknr = t_h_artikel.zwkum
            t_menu_list.bezeich = t_h_artikel.bezeich

    return generate_output()