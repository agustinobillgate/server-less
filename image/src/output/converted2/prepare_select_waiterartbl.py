#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Artikel

def prepare_select_waiterartbl(dept:int):

    prepare_cache ([Artikel])

    t_artikel_list = []
    artikel = None

    t_artikel = None

    t_artikel_list, T_artikel = create_model("T_artikel", {"artnr":int, "departement":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_artikel_list, artikel
        nonlocal dept


        nonlocal t_artikel
        nonlocal t_artikel_list

        return {"t-artikel": t_artikel_list}

    for artikel in db_session.query(Artikel).filter(
             (Artikel.departement == dept) & (Artikel.artart == 1)).order_by(Artikel._recid).all():
        t_artikel = T_artikel()
        t_artikel_list.append(t_artikel)

        t_artikel.artnr = artikel.artnr
        t_artikel.departement = artikel.departement
        t_artikel.bezeich = artikel.bezeich

    return generate_output()