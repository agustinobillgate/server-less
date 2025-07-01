#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Artikel

def select_frarticle_disp_it_webbl(sorttype:int, artart:int, f_dept:int):

    prepare_cache ([Artikel])

    artnr = 0
    t_artikel_list = []
    artikel = None

    t_artikel = None

    t_artikel_list, T_artikel = create_model("T_artikel", {"artnr":int, "departement":int, "bezeich":string, "activeflag":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal artnr, t_artikel_list, artikel
        nonlocal sorttype, artart, f_dept


        nonlocal t_artikel
        nonlocal t_artikel_list

        return {"artnr": artnr, "t-artikel": t_artikel_list}

    def disp_it():

        nonlocal artnr, t_artikel_list, artikel
        nonlocal sorttype, artart, f_dept


        nonlocal t_artikel
        nonlocal t_artikel_list

        if artart == 0:

            if sorttype == 1:

                for artikel in db_session.query(Artikel).filter(
                         (Artikel.departement == f_dept) & ((Artikel.artart == artart) | ((Artikel.artart == 9) & (Artikel.artgrp != 0)))).order_by(Artikel.artnr).all():
                    create_it()

            else:

                for artikel in db_session.query(Artikel).filter(
                         (Artikel.departement == f_dept) & ((Artikel.artart == artart) | ((Artikel.artart == 9) & (Artikel.artgrp != 0)))).order_by(Artikel.bezeich).all():
                    create_it()

        else:

            if sorttype == 1:

                for artikel in db_session.query(Artikel).filter(
                         (Artikel.departement == f_dept) & (Artikel.artart == artart)).order_by(Artikel.artnr).all():
                    create_it()

            else:

                for artikel in db_session.query(Artikel).filter(
                         (Artikel.departement == f_dept) & (Artikel.artart == artart)).order_by(Artikel.bezeich).all():
                    create_it()


        if artikel:
            artnr = artikel.artnr


    def create_it():

        nonlocal artnr, t_artikel_list, artikel
        nonlocal sorttype, artart, f_dept


        nonlocal t_artikel
        nonlocal t_artikel_list


        t_artikel = T_artikel()
        t_artikel_list.append(t_artikel)

        t_artikel.artnr = artikel.artnr
        t_artikel.departement = artikel.departement
        t_artikel.bezeich = artikel.bezeich
        t_artikel.activeflag = artikel.activeflag

    disp_it()

    return generate_output()