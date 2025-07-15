#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Artikel

def neo_load_artikelbl(deptno:int):
    artikel_list_data = []
    t_artikel_data = []
    artikel = None

    t_artikel = artikel_list = None

    t_artikel_data, T_artikel = create_model_like(Artikel)
    artikel_list_data, Artikel_list = create_model("Artikel_list", {"artnr":int, "departement":int, "bezeich":string, "artart":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal artikel_list_data, t_artikel_data, artikel
        nonlocal deptno


        nonlocal t_artikel, artikel_list
        nonlocal t_artikel_data, artikel_list_data

        return {"artikel-list": artikel_list_data, "t-artikel": t_artikel_data}


    for artikel in db_session.query(Artikel).filter(
             (Artikel.departement == deptno) & ((Artikel.artart == 0) | (Artikel.artart == 1) | (Artikel.artart == 8) | (Artikel.artart == 9))).order_by(Artikel._recid).all():
        artikel_list = Artikel_list()
        artikel_list_data.append(artikel_list)

        buffer_copy(artikel, artikel_list)

    return generate_output()