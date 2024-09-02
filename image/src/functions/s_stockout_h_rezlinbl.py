from functions.additional_functions import *
import decimal
from models import L_bestand, H_rezlin

def s_stockout_h_rezlinbl(p_artnr:int, curr_lager:int):
    t_l_bestand_list = []
    t_h_rezlin_list = []
    l_bestand = h_rezlin = None

    t_l_bestand = t_h_rezlin = None

    t_l_bestand_list, T_l_bestand = create_model_like(L_bestand)
    t_h_rezlin_list, T_h_rezlin = create_model_like(H_rezlin)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_bestand_list, t_h_rezlin_list, l_bestand, h_rezlin


        nonlocal t_l_bestand, t_h_rezlin
        nonlocal t_l_bestand_list, t_h_rezlin_list
        return {"t-l-bestand": t_l_bestand_list, "t-h-rezlin": t_h_rezlin_list}


    for h_rezlin in db_session.query(H_rezlin).filter(
            (H_rezlin.artnrrezept == p_artnr)).all():
        t_h_rezlin = T_h_rezlin()
        t_h_rezlin_list.append(t_h_rezlin)

        buffer_copy(h_rezlin, t_h_rezlin)

        if not h_rezlin.recipe_flag:

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.lager_nr == curr_lager) &  (L_bestand.artnr == h_rezlin.artnrlager)).first()

            if l_bestand:
                t_l_bestand = T_l_bestand()
                t_l_bestand_list.append(t_l_bestand)

                buffer_copy(l_bestand, t_l_bestand)

    return generate_output()