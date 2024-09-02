from functions.additional_functions import *
import decimal
import re
from models import L_artikel

def prepare_sarticle_listbl():
    first_artnr = 0
    curr_art = ""
    t_l_artikel_list = []
    counter:int = 0
    l_artikel = None

    t_l_artikel = sbuff = None

    t_l_artikel_list, T_l_artikel = create_model_like(L_artikel)

    Sbuff = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal first_artnr, curr_art, t_l_artikel_list, counter, l_artikel
        nonlocal sbuff


        nonlocal t_l_artikel, sbuff
        nonlocal t_l_artikel_list
        return {"first_artnr": first_artnr, "curr_art": curr_art, "t-l-artikel": t_l_artikel_list}

    def add_sunits():

        nonlocal first_artnr, curr_art, t_l_artikel_list, counter, l_artikel
        nonlocal sbuff


        nonlocal t_l_artikel, sbuff
        nonlocal t_l_artikel_list


        Sbuff = L_artikel

        l_artikel = db_session.query(L_artikel).first()
        while None != l_artikel:

            if not re.match(".*;.*",l_artikel.herkunft):

                sbuff = db_session.query(Sbuff).filter(
                        (Sbuff._recid == l_artikel._recid)).first()
                sbuff.herkunft = sbuff.herkunft + ";;"

                sbuff = db_session.query(Sbuff).first()

            l_artikel = db_session.query(L_artikel).first()

    l_artikel = db_session.query(L_artikel).first()

    if l_artikel and not re.match(".*;.*",l_artikel.herkunft):
        add_sunits()

    for l_artikel in db_session.query(L_artikel).all():
        counter = counter + 1

        if counter == 1:
            first_artnr = l_artikel.artnr

        if (counter >= 30) and (curr_art != l_artikel.bezeich):
            break
        t_l_artikel = T_l_artikel()
        t_l_artikel_list.append(t_l_artikel)

        buffer_copy(l_artikel, t_l_artikel)
        curr_art = l_artikel.bezeich

    return generate_output()