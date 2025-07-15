#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import L_artikel, L_bestand, L_order, L_op, H_rezlin, H_artikel, Dml_art, Reslin_queasy, Dml_artdep

def sarticle_list1_webbl(sorttype:int, last_art:string, last_art1:int):
    first_artnr = 0
    curr_art = ""
    curr_art1 = 0
    t_l_artikel_data = []
    counter:int = 0
    l_artikel = l_bestand = l_order = l_op = h_rezlin = h_artikel = dml_art = reslin_queasy = dml_artdep = None

    t_l_artikel = None

    t_l_artikel_data, T_l_artikel = create_model_like(L_artikel, {"is_delete":bool, "is_select":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal first_artnr, curr_art, curr_art1, t_l_artikel_data, counter, l_artikel, l_bestand, l_order, l_op, h_rezlin, h_artikel, dml_art, reslin_queasy, dml_artdep
        nonlocal sorttype, last_art, last_art1


        nonlocal t_l_artikel
        nonlocal t_l_artikel_data

        return {"first_artnr": first_artnr, "curr_art": curr_art, "curr_art1": curr_art1, "t-l-artikel": t_l_artikel_data}

    def cr_artikel1():

        nonlocal first_artnr, curr_art, curr_art1, t_l_artikel_data, counter, l_artikel, l_bestand, l_order, l_op, h_rezlin, h_artikel, dml_art, reslin_queasy, dml_artdep
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
        t_l_artikel.is_delete = delete_check(t_l_artikel.artnr)
        curr_art1 = l_artikel.artnr


    def cr_artikel2():

        nonlocal first_artnr, curr_art, curr_art1, t_l_artikel_data, counter, l_artikel, l_bestand, l_order, l_op, h_rezlin, h_artikel, dml_art, reslin_queasy, dml_artdep
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
        t_l_artikel.is_delete = delete_check(t_l_artikel.artnr)
        curr_art = l_artikel.bezeich


    def delete_check(artnr:int):

        nonlocal first_artnr, curr_art, curr_art1, t_l_artikel_data, counter, l_artikel, l_bestand, l_order, l_op, h_rezlin, h_artikel, dml_art, reslin_queasy, dml_artdep
        nonlocal sorttype, last_art, last_art1


        nonlocal t_l_artikel
        nonlocal t_l_artikel_data

        delete_it = False

        def generate_inner_output():
            return (delete_it)

        delete_it = True

        l_bestand = get_cache (L_bestand, {"artnr": [(eq, artnr)],"lager_nr": [(eq, 0)]})

        if l_bestand:
            delete_it = False

            return generate_inner_output()

        l_order = get_cache (L_order, {"artnr": [(eq, artnr)]})

        if l_order:
            delete_it = False

            return generate_inner_output()

        if delete_it:

            l_op = get_cache (L_op, {"artnr": [(eq, artnr)]})

            if l_op:
                delete_it = False

                return generate_inner_output()

        if delete_it:

            h_rezlin = get_cache (H_rezlin, {"artnrlager": [(eq, artnr)]})

            if h_rezlin:
                delete_it = False

                return generate_inner_output()

        if delete_it:

            h_artikel = get_cache (H_artikel, {"artnrlager": [(eq, artnr)]})

            if h_artikel:
                delete_it = False

                return generate_inner_output()

        if delete_it:

            dml_art = get_cache (Dml_art, {"artnr": [(eq, artnr)]})

            if dml_art:
                delete_it = False

                return generate_inner_output()

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                     (Reslin_queasy.key == ("DML").lower()) & (to_int(entry(0, Reslin_queasy.char1, ";")) == artnr)).first()

            if reslin_queasy:
                delete_it = False

                return generate_inner_output()

            dml_artdep = get_cache (Dml_artdep, {"artnr": [(eq, artnr)]})

            if dml_artdep:
                delete_it = False

                return generate_inner_output()

        return generate_inner_output()


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