from functions.additional_functions import *
import decimal
from models import H_artikel

def copy_hartikel_artnrbl(all_flag:bool, dept1:int):
    art1 = 0
    art2 = 0
    bezeich1 = ""
    bezeich2 = ""
    h_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal art1, art2, bezeich1, bezeich2, h_artikel


        return {"art1": art1, "art2": art2, "bezeich1": bezeich1, "bezeich2": bezeich2}

    def find_artnr():

        nonlocal art1, art2, bezeich1, bezeich2, h_artikel


        art1 = 999999
        art2 = 0

        for h_artikel in db_session.query(H_artikel).filter(
                (H_artikel.departement == dept1) &  (H_artikel.activeflag) &  (H_artikel.artart == 0)).all():

            if art1 > h_artikel.artnr:
                art1 = h_artikel.artnr

            if art2 < h_artikel.artnr:
                art2 = h_artikel.artnr
        bezeich1 = ""
        bezeich2 = ""

        h_artikel = db_session.query(H_artikel).filter(
                (H_artikel.artnr == art1) &  (H_artikel.departement == dept1)).first()

        if h_artikel:
            bezeich1 = h_artikel.bezeich

        h_artikel = db_session.query(H_artikel).filter(
                (H_artikel.artnr == art2) &  (H_artikel.departement == dept1)).first()

        if h_artikel:
            bezeich2 = h_artikel.bezeich

    def find_artnr1():

        nonlocal art1, art2, bezeich1, bezeich2, h_artikel


        art1 = 999999
        art2 = 0

        for h_artikel in db_session.query(H_artikel).filter(
                (H_artikel.departement == dept1) &  (H_artikel.activeflag)).all():

            if art1 > h_artikel.artnr:
                art1 = h_artikel.artnr

            if art2 < h_artikel.artnr:
                art2 = h_artikel.artnr
        bezeich1 = ""
        bezeich2 = ""

        h_artikel = db_session.query(H_artikel).filter(
                (H_artikel.artnr == art1) &  (H_artikel.departement == dept1)).first()

        if h_artikel:
            bezeich1 = h_artikel.bezeich

        h_artikel = db_session.query(H_artikel).filter(
                (H_artikel.artnr == art2) &  (H_artikel.departement == dept1)).first()

        if h_artikel:
            bezeich2 = h_artikel.bezeich


    if not all_flag:
        find_artnr()
    else:
        find_artnr1()

    return generate_output()