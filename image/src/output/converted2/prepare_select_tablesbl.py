#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Tisch, Queasy

def prepare_select_tablesbl(sel_type:int, location:int):

    prepare_cache ([Tisch, Queasy])

    r_list_list = []
    tisch = queasy = None

    r_list = None

    r_list_list, R_list = create_model("R_list", {"tischnr":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal r_list_list, tisch, queasy
        nonlocal sel_type, location


        nonlocal r_list
        nonlocal r_list_list

        return {"r-list": r_list_list}

    if sel_type == 0:

        for tisch in db_session.query(Tisch).filter(
                 (Tisch.departement == location) & not_ (Tisch.roomcharge)).order_by(Tisch.tischnr).all():

            queasy = get_cache (Queasy, {"key": [(eq, 31)],"number1": [(eq, location)],"number2": [(eq, tisch.tischnr)]})

            if not queasy:
                r_list = R_list()
                r_list_list.append(r_list)

                r_list.tischnr = tisch.tischnr
                r_list.bezeich = tisch.bezeich

    elif sel_type == 1:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 31) & (Queasy.number1 == location)).order_by(Queasy._recid).all():

            tisch = get_cache (Tisch, {"departement": [(eq, location)],"tischnr": [(eq, queasy.number2)]})

            if tisch:
                r_list = R_list()
                r_list_list.append(r_list)

                r_list.tischnr = tisch.tischnr
                r_list.bezeich = tisch.bezeich

    return generate_output()