from functions.additional_functions import *
import decimal
from models import Artikel

def select_artikel_display_artbl(departement:int, sub_group:int):
    q2_artikel_list = []
    artikel = None

    q2_artikel = None

    q2_artikel_list, Q2_artikel = create_model("Q2_artikel", {"artnr":int, "bezeich":str, "epreis":decimal, "anzahl":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal q2_artikel_list, artikel


        nonlocal q2_artikel
        nonlocal q2_artikel_list
        return {"q2-artikel": q2_artikel_list}

    for artikel in db_session.query(Artikel).filter(
            (Artikel.departement == departement) &  (Artikel.zwkum == sub_group) &  (Artikel.activeflag)).all():
        q2_artikel = Q2_artikel()
        q2_artikel_list.append(q2_artikel)

        q2_artikel.artnr = artikel.artnr
        q2_artikel.bezeich = artikel.bezeich
        q2_artikel.epreis = artikel.epreis
        q2_artikel.anzahl = artikel.anzahl

    return generate_output()