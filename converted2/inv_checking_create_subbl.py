#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel, Queasy, L_untergrup

def inv_checking_create_subbl():

    prepare_cache ([L_artikel, Queasy, L_untergrup])

    artikel2_data = []
    l_artikel = queasy = l_untergrup = None

    artikel2 = None

    artikel2_data, Artikel2 = create_model("Artikel2", {"art":int, "ekum":int, "zeich":string, "zeich2":string, "numb":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal artikel2_data, l_artikel, queasy, l_untergrup


        nonlocal artikel2
        nonlocal artikel2_data

        return {"artikel2": artikel2_data}

    def create_sub():

        nonlocal artikel2_data, l_artikel, queasy, l_untergrup


        nonlocal artikel2
        nonlocal artikel2_data


        artikel2_data.clear()

        for l_artikel in db_session.query(L_artikel).order_by(L_artikel._recid).all():

            queasy = get_cache (Queasy, {"key": [(eq, 29)],"number2": [(eq, l_artikel.zwkum)]})

            if queasy and queasy.number1 != l_artikel.endkum:

                l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, l_artikel.zwkum)]})
                artikel2 = Artikel2()
                artikel2_data.append(artikel2)

                artikel2.art = l_artikel.artnr
                artikel2.zeich = l_artikel.bezeich
                artikel2.ekum = l_artikel.endkum
                artikel2.zeich2 = l_untergrup.bezeich
                artikel2.numb = queasy.number1

    create_sub()

    return generate_output()