#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel

def rarticle_admin_h_artikelbl(case_type:int, h_artnr:int, dept:int, h_bezeich:string):
    flag = 0
    h_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, h_artikel
        nonlocal case_type, h_artnr, dept, h_bezeich

        return {"flag": flag}


    if case_type == 1:

        h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_artnr)],"departement": [(eq, dept)]})

    elif case_type == 2:

        h_artikel = get_cache (H_artikel, {"bezeich": [(eq, h_bezeich)],"departement": [(eq, dept)],"artnr": [(ne, h_artnr)]})

    if h_artikel:
        flag = 1

    return generate_output()