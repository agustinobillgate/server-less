#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Zimmer, Queasy

def select_flroom_web2bl(show_all:bool, sel_type:int, etage:int, location:int):

    prepare_cache ([Zimmer, Queasy])

    r_list_list = []
    zimmer = queasy = None

    r_list = None

    r_list_list, R_list = create_model("R_list", {"zinr":string, "bezeich":string, "location":int, "floor":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal r_list_list, zimmer, queasy
        nonlocal show_all, sel_type, etage, location


        nonlocal r_list
        nonlocal r_list_list

        return {"r-list": r_list_list}

    def create_list1():

        nonlocal r_list_list, zimmer, queasy
        nonlocal show_all, sel_type, etage, location


        nonlocal r_list
        nonlocal r_list_list


        r_list_list.clear()

        if sel_type == 0:

            for zimmer in db_session.query(Zimmer).filter(
                     (Zimmer.etage == etage)).order_by(Zimmer.zinr).all():

                queasy = get_cache (Queasy, {"key": [(eq, 25)],"number1": [(eq, location)],"number2": [(eq, etage)],"char1": [(eq, zimmer.zinr)]})

                if not queasy:
                    r_list = R_list()
                    r_list_list.append(r_list)

                    r_list.zinr = zimmer.zinr
                    r_list.bezeich = zimmer.bezeich
                    r_list.location = to_int(zimmer.code)
                    r_list.floor = zimmer.etage

        elif sel_type == 1:

            for queasy in db_session.query(Queasy).filter(
                     (Queasy.key == 25) & (Queasy.number1 == location) & (Queasy.number2 == etage)).order_by(Queasy._recid).all():

                zimmer = get_cache (Zimmer, {"zinr": [(eq, queasy.char1)]})

                if not zimmer:
                    continue
                r_list = R_list()
                r_list_list.append(r_list)

                r_list.zinr = zimmer.zinr
                r_list.bezeich = zimmer.bezeich
                r_list.location = to_int(zimmer.code)
                r_list.floor = zimmer.etage


    def create_list2():

        nonlocal r_list_list, zimmer, queasy
        nonlocal show_all, sel_type, etage, location


        nonlocal r_list
        nonlocal r_list_list


        r_list_list.clear()

        if sel_type == 0:

            for zimmer in db_session.query(Zimmer).order_by(Zimmer.zinr).all():

                queasy = get_cache (Queasy, {"key": [(eq, 25)],"number2": [(eq, etage)],"char1": [(eq, zimmer.zinr)]})

                if not queasy:
                    r_list = R_list()
                    r_list_list.append(r_list)

                    r_list.zinr = zimmer.zinr
                    r_list.bezeich = zimmer.bezeich
                    r_list.location = to_int(zimmer.code)
                    r_list.floor = zimmer.etage

        elif sel_type == 1:

            for queasy in db_session.query(Queasy).filter(
                     (Queasy.key == 25)).order_by(Queasy._recid).all():

                zimmer = get_cache (Zimmer, {"zinr": [(eq, queasy.char1)]})

                if not zimmer:
                    continue
                r_list = R_list()
                r_list_list.append(r_list)

                r_list.zinr = zimmer.zinr
                r_list.bezeich = zimmer.bezeich
                r_list.location = to_int(zimmer.code)
                r_list.floor = zimmer.etage


    if not show_all:
        create_list1()
    else:
        create_list2()

    return generate_output()