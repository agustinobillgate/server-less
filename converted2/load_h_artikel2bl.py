#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel, Wgrpdep, H_menu

def load_h_artikel2bl(case_type:int, dept:int, arttype:int):
    t_h_artikel_data = []
    t_wgrpdep_data = []
    t_h_menu_data = []
    h_artikel = wgrpdep = h_menu = None

    t_h_artikel = t_wgrpdep = t_h_menu = hart = None

    t_h_artikel_data, T_h_artikel = create_model_like(H_artikel)
    t_wgrpdep_data, T_wgrpdep = create_model_like(Wgrpdep)
    t_h_menu_data, T_h_menu = create_model_like(H_menu)

    Hart = create_buffer("Hart",H_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_h_artikel_data, t_wgrpdep_data, t_h_menu_data, h_artikel, wgrpdep, h_menu
        nonlocal case_type, dept, arttype
        nonlocal hart


        nonlocal t_h_artikel, t_wgrpdep, t_h_menu, hart
        nonlocal t_h_artikel_data, t_wgrpdep_data, t_h_menu_data

        return {"t-h-artikel": t_h_artikel_data, "t-wgrpdep": t_wgrpdep_data, "t-h-menu": t_h_menu_data}

    if case_type == 1:

        for h_artikel in db_session.query(H_artikel).filter(
                 (H_artikel.departement == dept) & (H_artikel.artart == arttype) & (H_artikel.activeflag)).order_by(H_artikel._recid).all():

            if h_artikel.artnr == 0:

                hart = db_session.query(Hart).filter(
                         (Hart._recid == h_artikel._recid)).first()
                db_session.delete(hart)
                pass
            else:
                t_h_artikel = T_h_artikel()
                t_h_artikel_data.append(t_h_artikel)

                buffer_copy(h_artikel, t_h_artikel)

                wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, dept)],"zknr": [(eq, h_artikel.zwkum)]})

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
                        t_wgrpdep.bezeich = to_string(h_artikel.zwkum) +\
                                " - NOT DEFINED!!"

        for h_menu in db_session.query(H_menu).order_by(H_menu._recid).all():
            t_h_menu = T_h_menu()
            t_h_menu_data.append(t_h_menu)

            buffer_copy(h_menu, t_h_menu)

    return generate_output()