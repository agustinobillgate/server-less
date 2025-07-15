#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import L_artikel

def sarticle_listbl(sorttype:int, last_art:string, last_art1:int):
    first_artnr = 0
    curr_art = ""
    curr_art1 = 0
    t_l_artikel_data = []
    counter:int = 0
    l_artikel = None

    t_l_artikel = None

    t_l_artikel_data, T_l_artikel = create_model_like(L_artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal first_artnr, curr_art, curr_art1, t_l_artikel_data, counter, l_artikel
        nonlocal sorttype, last_art, last_art1


        nonlocal t_l_artikel
        nonlocal t_l_artikel_data

        return {"first_artnr": first_artnr, "curr_art": curr_art, "curr_art1": curr_art1, "t-l-artikel": t_l_artikel_data}

    def cr_artikel1():

        nonlocal first_artnr, curr_art, curr_art1, t_l_artikel_data, counter, l_artikel
        nonlocal sorttype, last_art, last_art1


        nonlocal t_l_artikel
        nonlocal t_l_artikel_data


        counter = counter + 1

        if counter == 1:
            first_artnr = l_artikel.artnr

        if (counter >= 30) and (curr_art1 != l_artikel.artnr):
            return
        t_l_artikel = T_l_artikel()
        t_l_artikel_data.append(t_l_artikel)

        buffer_copy(l_artikel, t_l_artikel)
        curr_art1 = l_artikel.artnr


    def cr_artikel2():

        nonlocal first_artnr, curr_art, curr_art1, t_l_artikel_data, counter, l_artikel
        nonlocal sorttype, last_art, last_art1


        nonlocal t_l_artikel
        nonlocal t_l_artikel_data


        counter = counter + 1

        if counter == 1:
            first_artnr = l_artikel.artnr

        if (counter >= 30) and (curr_art != l_artikel.bezeich):
            return
        t_l_artikel = T_l_artikel()
        t_l_artikel_data.append(t_l_artikel)

        buffer_copy(l_artikel, t_l_artikel)
        curr_art = l_artikel.bezeich


    if sorttype == 1:

        if last_art1 != 0:

            for l_artikel in db_session.query(L_artikel).filter(
                     (L_artikel.artnr >= last_art1)).order_by(L_artikel.artnr).all():
                cr_artikel1()

        else:

            for l_artikel in db_session.query(L_artikel).order_by(L_artikel.artnr).all():
                cr_artikel1()


    elif sorttype == 2:

        if substring(last_art, 0, 1) == ("*").lower() :

            if substring(last_art, length(last_art) - 1, 1) != ("*").lower() :
                last_art = last_art + "*"

            for l_artikel in db_session.query(L_artikel).filter(
                     (matches(L_artikel.bezeich,last_art))).order_by(L_artikel.bezeich).all():
                cr_artikel2()
        else:

            for l_artikel in db_session.query(L_artikel).filter(
                     (L_artikel.bezeich >= ((last_art).lower()))).order_by(L_artikel.bezeich).all():
                cr_artikel2()

    else:

        if last_art == "":

            for l_artikel in db_session.query(L_artikel).filter(
                     (L_artikel.artnr > last_art1)).order_by(L_artikel.artnr).all():
                cr_artikel1()

        else:

            for l_artikel in db_session.query(L_artikel).filter(
                     (L_artikel.bezeich > (last_art).lower())).order_by(L_artikel.bezeich).all():
                cr_artikel2()


    return generate_output()