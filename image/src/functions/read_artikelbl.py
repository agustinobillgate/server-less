from functions.additional_functions import *
import decimal
from models import Artikel

def read_artikelbl(artno:int, dept:int, aname:str):
    t_artikel_list = []
    artikel = None

    t_artikel = None

    t_artikel_list, T_artikel = create_model_like(Artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_artikel_list, artikel


        nonlocal t_artikel
        nonlocal t_artikel_list
        return {"t-artikel": t_artikel_list}

    if artno != 0:

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == artno) &  (Artikel.departement == dept)).first()

    elif aname != "":

        artikel = db_session.query(Artikel).filter(
                (Artikel.bezeich == aname) &  (Artikel.departement == dept)).first()

    if artikel:
        t_artikel = T_artikel()
        t_artikel_list.append(t_artikel)

        buffer_copy(artikel, t_artikel)

    return generate_output()