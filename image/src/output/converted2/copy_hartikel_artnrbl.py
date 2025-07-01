#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel

def copy_hartikel_artnrbl(all_flag:bool, dept1:int):

    prepare_cache ([H_artikel])

    art1 = 0
    art2 = 0
    bezeich1 = ""
    bezeich2 = ""
    h_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal art1, art2, bezeich1, bezeich2, h_artikel
        nonlocal all_flag, dept1

        return {"art1": art1, "art2": art2, "bezeich1": bezeich1, "bezeich2": bezeich2}

    def find_artnr():

        nonlocal art1, art2, bezeich1, bezeich2, h_artikel
        nonlocal all_flag, dept1


        art1 = 999999
        art2 = 0

        for h_artikel in db_session.query(H_artikel).filter(
                 (H_artikel.departement == dept1) & (H_artikel.activeflag) & (H_artikel.artart == 0)).order_by(H_artikel._recid).all():

            if art1 > h_artikel.artnr:
                art1 = h_artikel.artnr

            if art2 < h_artikel.artnr:
                art2 = h_artikel.artnr
        bezeich1 = ""
        bezeich2 = ""

        h_artikel = get_cache (H_artikel, {"artnr": [(eq, art1)],"departement": [(eq, dept1)]})

        if h_artikel:
            bezeich1 = h_artikel.bezeich

        h_artikel = get_cache (H_artikel, {"artnr": [(eq, art2)],"departement": [(eq, dept1)]})

        if h_artikel:
            bezeich2 = h_artikel.bezeich


    def find_artnr1():

        nonlocal art1, art2, bezeich1, bezeich2, h_artikel
        nonlocal all_flag, dept1


        art1 = 999999
        art2 = 0

        for h_artikel in db_session.query(H_artikel).filter(
                 (H_artikel.departement == dept1) & (H_artikel.activeflag)).order_by(H_artikel._recid).all():

            if art1 > h_artikel.artnr:
                art1 = h_artikel.artnr

            if art2 < h_artikel.artnr:
                art2 = h_artikel.artnr
        bezeich1 = ""
        bezeich2 = ""

        h_artikel = get_cache (H_artikel, {"artnr": [(eq, art1)],"departement": [(eq, dept1)]})

        if h_artikel:
            bezeich1 = h_artikel.bezeich

        h_artikel = get_cache (H_artikel, {"artnr": [(eq, art2)],"departement": [(eq, dept1)]})

        if h_artikel:
            bezeich2 = h_artikel.bezeich

    if not all_flag:
        find_artnr()
    else:
        find_artnr1()

    return generate_output()