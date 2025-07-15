#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_menu, H_artikel

def menu_eng_show_submenu_webbl(article_no:int, dept_no:int):

    prepare_cache ([H_artikel])

    t_h_menu_data = []
    h_menu = h_artikel = None

    t_h_menu = buff_hart = None

    t_h_menu_data, T_h_menu = create_model_like(H_menu, {"art_desc":string})

    Buff_hart = create_buffer("Buff_hart",H_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_h_menu_data, h_menu, h_artikel
        nonlocal article_no, dept_no
        nonlocal buff_hart


        nonlocal t_h_menu, buff_hart
        nonlocal t_h_menu_data

        return {"t-h-menu": t_h_menu_data}

    h_artikel = get_cache (H_artikel, {"artnr": [(eq, article_no)],"departement": [(eq, dept_no)]})

    if h_artikel:

        h_menu_obj_list = {}
        for h_menu, buff_hart in db_session.query(H_menu, Buff_hart).join(Buff_hart,(Buff_hart.artnr == H_menu.artnr) & (Buff_hart.departement == H_menu.departement)).filter(
                 (H_menu.nr == h_artikel.betriebsnr) & (H_menu.departement == h_artikel.departement)).order_by(H_menu._recid).all():
            if h_menu_obj_list.get(h_menu._recid):
                continue
            else:
                h_menu_obj_list[h_menu._recid] = True


            t_h_menu = T_h_menu()
            t_h_menu_data.append(t_h_menu)

            buffer_copy(h_menu, t_h_menu)
            t_h_menu.art_desc = buff_hart.bezeich

    return generate_output()