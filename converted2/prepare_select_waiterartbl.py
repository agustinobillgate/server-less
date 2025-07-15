#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Artikel

def prepare_select_waiterartbl(dept:int):

    prepare_cache ([Artikel])

    t_artikel_data = []
    artikel = None

    t_artikel = None

    t_artikel_data, T_artikel = create_model("T_artikel", {"artnr":int, "departement":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_artikel_data, artikel
        nonlocal dept


        nonlocal t_artikel
        nonlocal t_artikel_data

        return {"t-artikel": t_artikel_data}

    for artikel in db_session.query(Artikel).filter(
             (Artikel.departement == dept) & (Artikel.artart == 1)).order_by(Artikel._recid).all():
        t_artikel = T_artikel()
        t_artikel_data.append(t_artikel)

        t_artikel.artnr = artikel.artnr
        t_artikel.departement = artikel.departement
        t_artikel.bezeich = artikel.bezeich

    return generate_output()