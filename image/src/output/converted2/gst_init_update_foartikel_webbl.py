#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.gst_init_update_foartikelbl import gst_init_update_foartikelbl
from models import Artikel

t_artikel_list, T_artikel = create_model_like(Artikel)

def gst_init_update_foartikel_webbl(t_artikel_list:[T_artikel]):
    artikel = None

    t_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal artikel


        nonlocal t_artikel

        return {}

    for t_artikel in query(t_artikel_list, sort_by=[("artnr",False),("departement",False)]):
        pass
        t_artikel.bezeich2

        if t_artikel.bezeich2 != "":
            get_output(gst_init_update_foartikelbl(t_artikel.artnr, t_artikel.departement, t_artikel.bezeich2))

    return generate_output()