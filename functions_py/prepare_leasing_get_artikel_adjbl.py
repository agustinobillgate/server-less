# using conversion tools version: 1.0.0.119
"""_yusufwijasena_06/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix python indentation
                    - only convert
"""
from functions.additional_functions import *
from decimal import Decimal
from models import Artikel, Htparam

def prepare_leasing_get_artikel_adjbl():

    prepare_cache([Htparam])

    art_no = 0
    art_desc = ""
    t_artikel_data = []
    artikel = htparam = None

    t_artikel = None

    t_artikel_data, T_artikel = create_model_like(Artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal art_no, art_desc, t_artikel_data, artikel, htparam
        nonlocal t_artikel
        nonlocal t_artikel_data

        return {
            "art_no": art_no,
            "art_desc": art_desc,
            "t-artikel": t_artikel_data
        }

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 1365)]})

    if htparam:
        art_no = htparam.finteger

        artikel = get_cache(
            Artikel, {"artnr": [(eq, art_no)], "departement": [(eq, 0)]})

        if artikel:
            art_desc = artikel.bezeich

    for artikel in db_session.query(Artikel).filter(
            (Artikel.departement == 0) & ((Artikel.artart == 2) | (Artikel.artart == 6) | (Artikel.artart == 7))).order_by(Artikel._recid).all():
        t_artikel = T_artikel()
        t_artikel_data.append(t_artikel)

        buffer_copy(artikel, t_artikel)

    return generate_output()
