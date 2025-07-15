#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Zimmer, Zimkateg

def avail_ddown_active_roombl(curr_zikat:int, mi_inactive:bool):

    prepare_cache ([Zimmer, Zimkateg])

    rmcat_list_data = []
    zimmer = zimkateg = None

    rmcat_list = None

    rmcat_list_data, Rmcat_list = create_model("Rmcat_list", {"zikatnr":int, "anzahl":int, "sleeping":bool, "kurzbez":string, "bezeich":string, "zinr":string}, {"sleeping": True})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rmcat_list_data, zimmer, zimkateg
        nonlocal curr_zikat, mi_inactive


        nonlocal rmcat_list
        nonlocal rmcat_list_data

        return {"rmcat-list": rmcat_list_data}

    def active_room():

        nonlocal rmcat_list_data, zimmer, zimkateg
        nonlocal curr_zikat, mi_inactive


        nonlocal rmcat_list
        nonlocal rmcat_list_data

        zikatnr:int = 0
        troom:int = 0

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping) & (Zimmer.zikatnr == curr_zikat) & (Zimmer.zinr != "")).order_by(Zimmer._recid).all():

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

            if zimkateg.verfuegbarkeit:
                rmcat_list = Rmcat_list()
                rmcat_list_data.append(rmcat_list)

                rmcat_list.zikatnr = zimkateg.zikatnr
                rmcat_list.zinr = zimmer.zinr
                rmcat_list.kurzbez = zimkateg.kurzbez
                rmcat_list.bezeich = zimkateg.bezeichnung


                troom = troom + 1
        rmcat_list = Rmcat_list()
        rmcat_list_data.append(rmcat_list)

        rmcat_list.kurzbez = "TOTAL"
        rmcat_list.zinr = to_string(troom)

        if not mi_inactive:

            return
        zikatnr = 0

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping == False) & (Zimmer.zikatnr == curr_zikat) & (Zimmer.zinr != "")).order_by(Zimmer.zikatnr).all():

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

            if zimkateg.verfuegbarkeit:
                rmcat_list = Rmcat_list()
                rmcat_list_data.append(rmcat_list)

                rmcat_list.zikatnr = zimkateg.zikatnr
                rmcat_list.zinr = zimmer.zinr
                rmcat_list.kurzbez = zimkateg.kurzbez
                rmcat_list.bezeich = zimkateg.bezeichnung


                troom = troom + 1

        if troom != 0:
            rmcat_list = Rmcat_list()
            rmcat_list_data.append(rmcat_list)

            rmcat_list.kurzbez = "TOTAL"
            rmcat_list.zinr = to_string(troom)

    active_room()

    return generate_output()