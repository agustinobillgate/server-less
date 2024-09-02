from functions.additional_functions import *
import decimal
from datetime import date
from models import Artikel, Htparam

def prepare_ar_subledgerbl(artno:int):
    long_digit = False
    to_date = None
    double_currency = False
    t_artikel_list = []
    artikel = htparam = None

    t_artikel = None

    t_artikel_list, T_artikel = create_model_like(Artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, to_date, double_currency, t_artikel_list, artikel, htparam


        nonlocal t_artikel
        nonlocal t_artikel_list
        return {"long_digit": long_digit, "to_date": to_date, "double_currency": double_currency, "t-artikel": t_artikel_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    to_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()
    double_currency = htparam.flogical

    if artno > 0:

        for artikel in db_session.query(Artikel).filter(
                (Artikel.departement == 0) &  (Artikel.artnr == artno)).all():
            t_artikel = T_artikel()
            t_artikel_list.append(t_artikel)

            buffer_copy(artikel, t_artikel)

    else:

        for artikel in db_session.query(Artikel).filter(
                (Artikel.departement == 0) &  ((Artikel.artart == 2) |  (Artikel.artart == 7)) &  (Artikel.activeflag)).all():
            t_artikel = T_artikel()
            t_artikel_list.append(t_artikel)

            buffer_copy(artikel, t_artikel)


    return generate_output()