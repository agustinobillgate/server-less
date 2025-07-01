#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_rezept

def mk_rezept_btn_newbl(case_type:int, h_artnr:int):

    prepare_cache ([H_rezept])

    katnr = 0
    h_rezept = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal katnr, h_rezept
        nonlocal case_type, h_artnr

        return {"katnr": katnr}


    if case_type == 1:

        for h_rezept in db_session.query(H_rezept).order_by(H_rezept._recid).all():

            if h_rezept.kategorie > katnr:
                katnr = h_rezept.kategorie


    elif case_type == 2:

        for h_rezept in db_session.query(H_rezept).order_by(H_rezept._recid).all():

            if h_rezept.artnrrezept > h_artnr:
                katnr = h_rezept.artnrrezept


    return generate_output()