from functions.additional_functions import *
import decimal
from models import L_artikel

def inv_checking_create_main_cldbl():
    artikel1_list = []
    l_artikel = None

    artikel1 = None

    artikel1_list, Artikel1 = create_model("Artikel1", {"art":int, "ekum":int, "zeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal artikel1_list, l_artikel


        nonlocal artikel1
        nonlocal artikel1_list
        return {"artikel1": artikel1_list}

    def create_main():

        nonlocal artikel1_list, l_artikel


        nonlocal artikel1
        nonlocal artikel1_list


        artikel1_list.clear()

        for l_artikel in db_session.query(L_artikel).order_by(L_artikel._recid).all():

            if substring(to_string(l_artikel.artnr) , 0, 1) != to_string(l_artikel.endkum):
                artikel1 = Artikel1()
                artikel1_list.append(artikel1)

                artikel1.art = l_artikel.artnr
                artikel1.ekum = l_artikel.endkum
                artikel1.zeich = l_artikel.bezeich

    create_main()

    return generate_output()