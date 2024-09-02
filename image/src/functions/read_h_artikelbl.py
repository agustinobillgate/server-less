from functions.additional_functions import *
import decimal
from models import H_artikel

def read_h_artikelbl(case_type:int, artno:int, dept:int, aname:str, artart:int, betriebsno:int, actflag:bool):
    t_artikel_list = []
    h_artikel = None

    t_artikel = None

    t_artikel_list, T_artikel = create_model_like(H_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_artikel_list, h_artikel


        nonlocal t_artikel
        nonlocal t_artikel_list
        return {"t-artikel": t_artikel_list}

    def cr_artikel():

        nonlocal t_artikel_list, h_artikel


        nonlocal t_artikel
        nonlocal t_artikel_list


        t_artikel = T_artikel()
        t_artikel_list.append(t_artikel)

        buffer_copy(h_artikel, t_artikel)

    if case_type == 1:

        if artno != 0:

            h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.artnr == artno) &  (H_artikel.departement == dept)).first()

        elif aname != "":

            h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.bezeich == aname) &  (H_artikel.departement == dept)).first()

        if h_artikel:
            cr_artikel()
    elif case_type == 2:

        h_artikel = db_session.query(H_artikel).filter(
                (H_artikel.departement == dept) &  (H_artikel.bezeich == aname) &  (H_artikel.artnr != artno)).first()

        if h_artikel:
            cr_artikel()

    return generate_output()