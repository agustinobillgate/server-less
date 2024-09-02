from functions.additional_functions import *
import decimal
from models import Zimmer, Queasy

def select_flroom2bl(show_all:bool, sel_type:int, etage:int, location:int):
    r_list_list = []
    zimmer = queasy = None

    r_list = None

    r_list_list, R_list = create_model("R_list", {"zinr":str, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal r_list_list, zimmer, queasy


        nonlocal r_list
        nonlocal r_list_list
        return {"r-list": r_list_list}

    def create_list1():

        nonlocal r_list_list, zimmer, queasy


        nonlocal r_list
        nonlocal r_list_list


        r_list_list.clear()

        if sel_type == 0:

            for zimmer in db_session.query(Zimmer).filter(
                    (Zimmer.etage == etage)).all():

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 25) &  (Queasy.number1 == location) &  (Queasy.number2 == etage) &  (Queasy.char1 == zimmer.zinr)).first()

                if not queasy:
                    r_list = R_list()
                    r_list_list.append(r_list)

                    r_list.zinr = zimmer.zinr
                    r_list.bezeich = zimmer.bezeich

        elif sel_type == 1:

            for queasy in db_session.query(Queasy).filter(
                    (Queasy.key == 25) &  (Queasy.number1 == location) &  (Queasy.number2 == etage)).all():

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == queasy.char1)).first()
                r_list = R_list()
                r_list_list.append(r_list)

                r_list.zinr = zimmer.zinr
                r_list.bezeich = zimmer.bezeich

    def create_list2():

        nonlocal r_list_list, zimmer, queasy


        nonlocal r_list
        nonlocal r_list_list


        r_list_list.clear()

        if sel_type == 0:

            for zimmer in db_session.query(Zimmer).all():

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 25) &  (Queasy.number2 == etage) &  (Queasy.char1 == zimmer.zinr)).first()

                if not queasy:
                    r_list = R_list()
                    r_list_list.append(r_list)

                    r_list.zinr = zimmer.zinr
                    r_list.bezeich = zimmer.bezeich

        elif sel_type == 1:

            for queasy in db_session.query(Queasy).filter(
                    (Queasy.key == 25)).all():

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == queasy.char1)).first()
                r_list = R_list()
                r_list_list.append(r_list)

                r_list.zinr = zimmer.zinr
                r_list.bezeich = zimmer.bezeich

    if not show_all:
        create_list1()
    else:
        create_list2()

    return generate_output()