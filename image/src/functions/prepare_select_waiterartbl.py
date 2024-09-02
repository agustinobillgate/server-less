from functions.additional_functions import *
import decimal
from models import Artikel

def prepare_select_waiterartbl(dept:int):
    t_artikel_list = []
    artikel = None

    t_artikel = None

    t_artikel_list, T_artikel = create_model("T_artikel", {"artnr":int, "departement":int, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_artikel_list, artikel


        nonlocal t_artikel
        nonlocal t_artikel_list
        return {"t-artikel": t_artikel_list}

    for artikel in db_session.query(Artikel).filter(
            (Artikel.departement == dept) &  (Artikel.artart == 1)).all():
        t_artikel = T_artikel()
        t_artikel_list.append(t_artikel)

        t_artikel.artnr = artikel.artnr
        t_artikel.departement = artikel.departement
        t_artikel.bezeich = artikel.bezeich

    return generate_output()