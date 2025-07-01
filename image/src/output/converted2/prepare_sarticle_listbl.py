#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel

def prepare_sarticle_listbl():

    prepare_cache ([L_artikel])

    first_artnr = 0
    curr_art = ""
    t_l_artikel_list = []
    counter:int = 0
    l_artikel = None

    t_l_artikel = None

    t_l_artikel_list, T_l_artikel = create_model_like(L_artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal first_artnr, curr_art, t_l_artikel_list, counter, l_artikel


        nonlocal t_l_artikel
        nonlocal t_l_artikel_list

        return {"first_artnr": first_artnr, "curr_art": curr_art, "t-l-artikel": t_l_artikel_list}

    def add_sunits():

        nonlocal first_artnr, curr_art, t_l_artikel_list, counter, l_artikel


        nonlocal t_l_artikel
        nonlocal t_l_artikel_list

        sbuff = None
        Sbuff =  create_buffer("Sbuff",L_artikel)

        l_artikel = db_session.query(L_artikel).first()
        while None != l_artikel:

            if not matches(l_artikel.herkunft,r"*;*"):

                sbuff = get_cache (L_artikel, {"_recid": [(eq, l_artikel._recid)]})
                sbuff.herkunft = sbuff.herkunft + ";;"
                pass

            curr_recid = l_artikel._recid
            l_artikel = db_session.query(L_artikel).filter(L_artikel._recid > curr_recid).first()


    l_artikel = db_session.query(L_artikel).first()

    if l_artikel and not matches(l_artikel.herkunft,r"*;*"):
        add_sunits()

    for l_artikel in db_session.query(L_artikel).order_by(L_artikel.bezeich).yield_per(100):
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