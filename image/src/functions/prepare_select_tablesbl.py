from functions.additional_functions import *
import decimal
from models import Tisch, Queasy

def prepare_select_tablesbl(sel_type:int, location:int):
    r_list_list = []
    tisch = queasy = None

    r_list = None

    r_list_list, R_list = create_model("R_list", {"tischnr":int, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal r_list_list, tisch, queasy


        nonlocal r_list
        nonlocal r_list_list
        return {"r-list": r_list_list}

    if sel_type == 0:

        for tisch in db_session.query(Tisch).filter(
                (Tisch.departement == location) &  (not Tisch.roomcharge)).all():

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 31) &  (Queasy.number1 == location) &  (Queasy.number2 == tischnr)).first()

            if not queasy:
                r_list = R_list()
                r_list_list.append(r_list)

                r_list.tischnr = tischnr
                r_list.bezeich = tisch.bezeich

    elif sel_type == 1:

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 31) &  (Queasy.number1 == location)).all():

            tisch = db_session.query(Tisch).filter(
                    (Tisch.departement == location) &  (Tischnr == queasy.number2)).first()

            if tisch:
                r_list = R_list()
                r_list_list.append(r_list)

                r_list.tischnr = tischnr
                r_list.bezeich = tisch.bezeich

    return generate_output()