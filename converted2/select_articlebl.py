#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Artikel

def select_articlebl(arttype:string):
    t_artikel_data = []
    artikel = None

    t_artikel = None

    t_artikel_data, T_artikel = create_model_like(Artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_artikel_data, artikel
        nonlocal arttype


        nonlocal t_artikel
        nonlocal t_artikel_data

        return {"t-artikel": t_artikel_data}

    if arttype.lower()  == ("payments").lower() :

        for artikel in db_session.query(Artikel).filter(
                 ((Artikel.artart == 6) | (Artikel.artart == 7))).order_by(Artikel._recid).all():
            t_artikel = T_artikel()
            t_artikel_data.append(t_artikel)

            buffer_copy(artikel, t_artikel)

    return generate_output()