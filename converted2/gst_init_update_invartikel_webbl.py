#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.gst_init_updatebl import gst_init_updatebl
from models import L_artikel

t_l_artikel_data, T_l_artikel = create_model_like(L_artikel)

def gst_init_update_invartikel_webbl(t_l_artikel_data:[T_l_artikel]):
    gst_supp:int = 483
    l_artikel = None

    t_l_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gst_supp, l_artikel


        nonlocal t_l_artikel

        return {}

    for t_l_artikel in query(t_l_artikel_data, sort_by=[("artnr",False)]):
        t_l_artikel.lief_nr3 = gst_supp


        pass
        t_l_artikel.lief_artnr[2]

        if t_l_artikel.lief_artnr[2] != "":
            get_output(gst_init_updatebl(t_l_artikel.artnr, gst_supp, t_l_artikel.lief_artnr[2]))

    return generate_output()