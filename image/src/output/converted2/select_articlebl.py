#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Artikel

def select_articlebl(arttype:string):
    t_artikel_list = []
    artikel = None

    t_artikel = None

    t_artikel_list, T_artikel = create_model_like(Artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_artikel_list, artikel
        nonlocal arttype


        nonlocal t_artikel
        nonlocal t_artikel_list

        return {"t-artikel": t_artikel_list}

    if arttype.lower()  == ("payments").lower() :

        for artikel in db_session.query(Artikel).filter(
                 ((Artikel.artart == 6) | (Artikel.artart == 7))).order_by(Artikel._recid).all():
            t_artikel = T_artikel()
            t_artikel_list.append(t_artikel)

            buffer_copy(artikel, t_artikel)

    return generate_output()