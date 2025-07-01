#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Artikel

def read_artikelbl(artno:int, dept:int, aname:string):
    t_artikel_list = []
    artikel = None

    t_artikel = None

    t_artikel_list, T_artikel = create_model_like(Artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_artikel_list, artikel
        nonlocal artno, dept, aname


        nonlocal t_artikel
        nonlocal t_artikel_list

        return {"t-artikel": t_artikel_list}

    if artno != 0:

        artikel = get_cache (Artikel, {"artnr": [(eq, artno)],"departement": [(eq, dept)]})

    elif aname != "":

        artikel = get_cache (Artikel, {"bezeich": [(eq, aname)],"departement": [(eq, dept)]})

    if artikel:
        t_artikel = T_artikel()
        t_artikel_list.append(t_artikel)

        buffer_copy(artikel, t_artikel)

    return generate_output()