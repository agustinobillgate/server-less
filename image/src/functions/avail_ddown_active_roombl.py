from functions.additional_functions import *
import decimal
from models import Zimmer, Zimkateg

def avail_ddown_active_roombl(curr_zikat:int, mi_inactive:bool):
    rmcat_list_list = []
    zimmer = zimkateg = None

    rmcat_list = None

    rmcat_list_list, Rmcat_list = create_model("Rmcat_list", {"zikatnr":int, "anzahl":int, "sleeping":bool, "kurzbez":str, "bezeich":str, "zinr":str}, {"sleeping": True})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rmcat_list_list, zimmer, zimkateg


        nonlocal rmcat_list
        nonlocal rmcat_list_list
        return {"rmcat-list": rmcat_list_list}

    def active_room():

        nonlocal rmcat_list_list, zimmer, zimkateg


        nonlocal rmcat_list
        nonlocal rmcat_list_list

        zikatnr:int = 0
        troom:int = 0

        for zimmer in db_session.query(Zimmer).filter(
                (Zimmer.sleeping) &  (Zimmer.zikatnr == curr_zikat) &  (Zimmer.zinr != "")).all():

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == zimmer.zikatnr)).first()

            if zimkateg.verfuegbarkeit:
                rmcat_list = Rmcat_list()
                rmcat_list_list.append(rmcat_list)

                rmcat_list.zikatnr = zimkateg.zikatnr
                rmcat_list.zinr = zimmer.zinr
                rmcat_list.kurzbez = zimkateg.kurzbez
                rmcat_list.bezeich = zimkateg.bezeich


                troom = troom + 1
        rmcat_list = Rmcat_list()
        rmcat_list_list.append(rmcat_list)

        rmcat_list.kurzbez = "TOTAL"
        rmcat_list.zinr = to_string(troom)

        if not mi_inactive:

            return
        zikatnr = 0

        for zimmer in db_session.query(Zimmer).filter(
                (Zimmer.sleeping == False) &  (Zimmer.zikatnr == curr_zikat) &  (Zimmer.zinr != "")).all():

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == zimmer.zikatnr)).first()

            if zimkateg.verfuegbarkeit:
                rmcat_list = Rmcat_list()
                rmcat_list_list.append(rmcat_list)

                rmcat_list.zikatnr = zimkateg.zikatnr
                rmcat_list.zinr = zimmer.zinr
                rmcat_list.kurzbez = zimkateg.kurzbez
                rmcat_list.bezeich = zimkateg.bezeich


                troom = troom + 1

        if troom != 0:
            rmcat_list = Rmcat_list()
            rmcat_list_list.append(rmcat_list)

            rmcat_list.kurzbez = "TOTAL"
            rmcat_list.zinr = to_string(troom)


    active_room()

    return generate_output()