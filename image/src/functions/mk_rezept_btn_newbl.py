from functions.additional_functions import *
import decimal
from models import H_rezept

def mk_rezept_btn_newbl(case_type:int, h_artnr:int):
    katnr = 0
    h_rezept = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal katnr, h_rezept


        return {"katnr": katnr}


    if case_type == 1:

        for h_rezept in db_session.query(H_rezept).all():

            if h_rezept.kategorie > katnr:
                katnr = h_rezept.kategorie


    elif case_type == 2:

        for h_rezept in db_session.query(H_rezept).all():

            if h_rezept.artnrrezept > h_artnr:
                katnr = h_rezept.artnrrezept


    return generate_output()