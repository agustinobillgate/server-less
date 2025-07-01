#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Fa_lager, Mathis, Fa_artikel

def prepare_fa_movebl(artnr:int):

    prepare_cache ([Mathis, Fa_artikel])

    mathis_name = ""
    fa_artikel_anzahl = 0
    mathis_location = ""
    t_fa_lager_list = []
    fa_lager = mathis = fa_artikel = None

    t_fa_lager = None

    t_fa_lager_list, T_fa_lager = create_model_like(Fa_lager)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mathis_name, fa_artikel_anzahl, mathis_location, t_fa_lager_list, fa_lager, mathis, fa_artikel
        nonlocal artnr


        nonlocal t_fa_lager
        nonlocal t_fa_lager_list

        return {"mathis_name": mathis_name, "fa_artikel_anzahl": fa_artikel_anzahl, "mathis_location": mathis_location, "t-fa-lager": t_fa_lager_list}

    mathis = get_cache (Mathis, {"nr": [(eq, artnr)]})

    fa_artikel = get_cache (Fa_artikel, {"nr": [(eq, artnr)]})
    mathis_name = mathis.name
    fa_artikel_anzahl = fa_artikel.anzahl
    mathis_location = mathis.location

    for fa_lager in db_session.query(Fa_lager).order_by(Fa_lager._recid).all():
        t_fa_lager = T_fa_lager()
        t_fa_lager_list.append(t_fa_lager)

        buffer_copy(fa_lager, t_fa_lager)

    return generate_output()