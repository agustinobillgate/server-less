#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Artikel

def select_artikel_display_artbl(departement:int, sub_group:int):

    prepare_cache ([Artikel])

    q2_artikel_list = []
    artikel = None

    q2_artikel = None

    q2_artikel_list, Q2_artikel = create_model("Q2_artikel", {"artnr":int, "bezeich":string, "epreis":Decimal, "anzahl":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q2_artikel_list, artikel
        nonlocal departement, sub_group


        nonlocal q2_artikel
        nonlocal q2_artikel_list

        return {"q2-artikel": q2_artikel_list}

    for artikel in db_session.query(Artikel).filter(
             (Artikel.departement == departement) & (Artikel.zwkum == sub_group) & (Artikel.activeflag)).order_by(Artikel.artnr).all():
        q2_artikel = Q2_artikel()
        q2_artikel_list.append(q2_artikel)

        q2_artikel.artnr = artikel.artnr
        q2_artikel.bezeich = artikel.bezeich
        q2_artikel.epreis =  to_decimal(artikel.epreis)
        q2_artikel.anzahl = artikel.anzahl

    return generate_output()