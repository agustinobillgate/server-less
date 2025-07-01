#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Artikel

def prepare_ar_paylistbl():
    to_date = None
    t_artikel_list = []
    artikel = None

    t_artikel = None

    t_artikel_list, T_artikel = create_model_like(Artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal to_date, t_artikel_list, artikel


        nonlocal t_artikel
        nonlocal t_artikel_list

        return {"to_date": to_date, "t-artikel": t_artikel_list}


    to_date = get_output(htpdate(110))

    for artikel in db_session.query(Artikel).filter(
             (Artikel.departement == 0) & ((Artikel.artart == 2) | (Artikel.artart == 7)) & (Artikel.activeflag)).order_by(Artikel._recid).all():
        t_artikel = T_artikel()
        t_artikel_list.append(t_artikel)

        buffer_copy(artikel, t_artikel)

    return generate_output()