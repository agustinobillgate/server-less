from functions.additional_functions import *
import decimal
from models import Fa_lager, Mathis, Fa_artikel

def prepare_fa_movebl(artnr:int):
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


        nonlocal t_fa_lager
        nonlocal t_fa_lager_list
        return {"mathis_name": mathis_name, "fa_artikel_anzahl": fa_artikel_anzahl, "mathis_location": mathis_location, "t-fa-lager": t_fa_lager_list}

    mathis = db_session.query(Mathis).filter(
            (Mathis.nr == artnr)).first()

    fa_artikel = db_session.query(Fa_artikel).filter(
            (Fa_artikel.nr == artnr)).first()
    mathis_name = mathis.name
    fa_artikel_anzahl = fa_artikel.anzahl
    mathis_location = mathis.location

    for fa_lager in db_session.query(Fa_lager).all():
        t_fa_lager = T_fa_lager()
        t_fa_lager_list.append(t_fa_lager)

        buffer_copy(fa_lager, t_fa_lager)

    return generate_output()