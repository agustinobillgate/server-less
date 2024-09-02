from functions.additional_functions import *
import decimal
from models import L_artikel, Queasy, L_untergrup

def inv_checking_create_subbl():
    artikel2_list = []
    l_artikel = queasy = l_untergrup = None

    artikel2 = None

    artikel2_list, Artikel2 = create_model("Artikel2", {"art":int, "ekum":int, "zeich":str, "zeich2":str, "numb":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal artikel2_list, l_artikel, queasy, l_untergrup


        nonlocal artikel2
        nonlocal artikel2_list
        return {"artikel2": artikel2_list}

    def create_sub():

        nonlocal artikel2_list, l_artikel, queasy, l_untergrup


        nonlocal artikel2
        nonlocal artikel2_list


        artikel2_list.clear()

        for l_artikel in db_session.query(L_artikel).all():

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 29) &  (Queasy.number2 == l_artikel.zwkum)).first()

            if queasy and queasy.number1 != l_artikel.endkum:

                l_untergrup = db_session.query(L_untergrup).filter(
                        (L_untergrup.zwkum == l_artikel.zwkum)).first()
                artikel2 = Artikel2()
                artikel2_list.append(artikel2)

                artikel2.art = l_artikel.artnr
                artikel2.zeich = l_artikel.bezeich
                artikel2.ekum = l_artikel.endkum
                artikel2.zeich2 = l_untergrup.bezeich
                artikel2.numb = queasy.number1


    create_sub()

    return generate_output()