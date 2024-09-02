from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Zimmer, Zimkateg, Bediener, Res_history, Res_line, Queasy, Ratecode

def add_room_admin_1bl(pvilanguage:int, case_type:int, zimmer_list:[Zimmer_list], rm_feature:str, curr_mode:str, rmno:str, rmcatbez:str, user_init:str):
    msg_str = ""
    t_zimmer_list = []
    dynarate_list_list = []
    lvcarea:str = "add_room_admin"
    sleeping:bool = False
    zimmer = zimkateg = bediener = res_history = res_line = queasy = ratecode = None

    zimmer_list = t_zimmer = dynarate_list = qsy = None

    zimmer_list_list, Zimmer_list = create_model_like(Zimmer)
    t_zimmer_list, T_zimmer = create_model_like(Zimmer)
    dynarate_list_list, Dynarate_list = create_model("Dynarate_list", {"prcode":str, "to_room":int})

    Qsy = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, t_zimmer_list, dynarate_list_list, lvcarea, sleeping, zimmer, zimkateg, bediener, res_history, res_line, queasy, ratecode
        nonlocal qsy


        nonlocal zimmer_list, t_zimmer, dynarate_list, qsy
        nonlocal zimmer_list_list, t_zimmer_list, dynarate_list_list
        return {"msg_str": msg_str, "t-zimmer": t_zimmer_list, "dynaRate-list": dynarate_list_list}

    def fill_zimmer():

        nonlocal msg_str, t_zimmer_list, dynarate_list_list, lvcarea, sleeping, zimmer, zimkateg, bediener, res_history, res_line, queasy, ratecode
        nonlocal qsy


        nonlocal zimmer_list, t_zimmer, dynarate_list, qsy
        nonlocal zimmer_list_list, t_zimmer_list, dynarate_list_list

        if (case_type != 1) and (zimmer_list.sleeping != zimmer.sleeping):

            bediener = db_session.query(Bediener).filter(
                    (func.lower(Bediener.userinit) == (user_init).lower())).first()
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "RoomNo: " + zimmer.zinr + " change room active " +\
                    to_string(zimmer.sleeping) + " to " + to_string(zimmer_list.sleeping)


            res_history.action = "Room Admin"

            res_history = db_session.query(Res_history).first()

        buffer_copy(zimmer_list, zimmer)
        zimmer.himmelsr = rm_feature

        if curr_mode.lower()  == "chg" and zimmer.setup != zimmer_list.setup and zimmer.setup != 0:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.active_flag == 1) &  (Res_line.zinr == zimmer.zinr)).first()
            while None != res_line:

                res_line = db_session.query(Res_line).first()
                res_line.setup = zimmer_list.setup

                res_line = db_session.query(Res_line).first()

                res_line = db_session.query(Res_line).filter(
                        (Res_line.active_flag == 1) &  (Res_line.zinr == zimmer.zinr)).first()

            res_line = db_session.query(Res_line).filter(
                    (Res_line.active_flag == 0) &  (Res_line.zinr == zimmer.zinr)).first()
            while None != res_line:

                res_line = db_session.query(Res_line).first()
                res_line.setup = zimmer_list.setup

                res_line = db_session.query(Res_line).first()

                res_line = db_session.query(Res_line).filter(
                        (Res_line.active_flag == 0) &  (Res_line.zinr == zimmer.zinr)).first()
        zimmer.setup = zimmer_list.setup

        if curr_mode.lower()  == "chg" and sleeping != zimmer_list.sleeping:
            update_queasy()

    def check_dynarate():

        nonlocal msg_str, t_zimmer_list, dynarate_list_list, lvcarea, sleeping, zimmer, zimkateg, bediener, res_history, res_line, queasy, ratecode
        nonlocal qsy


        nonlocal zimmer_list, t_zimmer, dynarate_list, qsy
        nonlocal zimmer_list_list, t_zimmer_list, dynarate_list_list

        tokcounter:int = 0
        iftask:str = ""
        ct:str = ""
        mestoken:str = ""
        mesvalue:str = ""
        days1:int = 0
        days2:int = 0
        to_room:int = 0

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 2) &  (Queasy.logi2)).first()

        if not queasy:

            return

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.kurzbez == rmcatbez)).first()

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 2) &  (Queasy.logi2)).all():
            dynarate_list = Dynarate_list()
            dynarate_list_list.append(dynarate_list)

            dynaRate_list.prCode = queasy.char1
            dynaRate_list.to_room = 0
            to_room = 0
            days1 = 0
            days2 = 0

            for ratecode in db_session.query(Ratecode).filter(
                    (Ratecode.CODE == queasy.char1)).all():
                iftask = ratecode.char1[4]
                for tokcounter in range(1,num_entries(iftask, ";") - 1 + 1) :
                    mestoken = substring(entry(tokcounter - 1, iftask, ";") , 0, 2)
                    mesvalue = substring(entry(tokcounter - 1, iftask, ";") , 2)

                    if mestoken == "TR":
                        to_room = to_int(mesvalue)
                    elif mestoken == "D1":
                        days1 = to_int(mesvalue)
                    elif mestoken == "D2":
                        days2 = to_int(mesvalue)

            if days1 == 0 and days2 == 0 and dynaRate_list.to_room < to_room:
                dynaRate_list.to_room = to_room

        if dynaRate_list.to_room == 0:
            dynarate_list_list.remove(dynarate_list)

    def update_queasy():

        nonlocal msg_str, t_zimmer_list, dynarate_list_list, lvcarea, sleeping, zimmer, zimkateg, bediener, res_history, res_line, queasy, ratecode
        nonlocal qsy


        nonlocal zimmer_list, t_zimmer, dynarate_list, qsy
        nonlocal zimmer_list_list, t_zimmer_list, dynarate_list_list

        cat_flag:bool = False
        zikatnr:int = 0
        Qsy = Queasy

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 152)).first()

        if queasy:
            cat_flag = True

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.zikatnr == zimmer_list.zikatnr)).first()

        if zimkateg:

            if cat_flag:
                zikatnr = zimkateg.typ
            else:
                zikatnr = zimkateg.zikatnr

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 171) &  (Queasy.date1 >= get_current_date()) &  (Queasy.number1 == zikatnr)).first()
        while None != queasy and queasy.logi1 == False and queasy.logi2 == False :

            qsy = db_session.query(Qsy).filter(
                    (Qsy._recid == queasy._recid)).first()

            if qsy:
                qsy.logi2 = True

                qsy = db_session.query(Qsy).first()


            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 171) &  (Queasy.date1 >= get_current_date()) &  (Queasy.number1 == zikatnr)).first()

    zimmer_list = query(zimmer_list_list, first=True)

    if case_type == 1:

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.zikatnr == zimmer_list.zikatnr)).first()
        zimkateg.maxzimanz = zimkateg.maxzimanz + 1

        zimkateg = db_session.query(Zimkateg).first()
        zimmer = Zimmer()
        db_session.add(zimmer)

        fill_zimmer()
        update_queasy()
    else:

        zimmer = db_session.query(Zimmer).filter(
                (Zimmer.zinr == rmno)).first()
        sleeping = zimmer.sleeping
        fill_zimmer()
    dynaRate_list_list.clear()

    for zimmer in db_session.query(Zimmer).all():
        t_zimmer = T_zimmer()
        t_zimmer_list.append(t_zimmer)

        buffer_copy(zimmer, t_zimmer)

    for dynarate_list in query(dynarate_list_list, filters=(lambda dynarate_list :dynaRate_list.to_room < zimkateg.maxzimanz)):
        ct = ct + dynaRate_list.prCode + " " + to_string(dynaRate_list.to_room) + "; "

    if ct != "":
        msg_str = msg_str + chr(2) + translateExtended ("The MAX To_Room of following Ratecode(s) < Room QTY of the related Room Type", lvcarea, "") + " ( ==  " + to_string(zimkateg.maxzimanz) + ")." + chr(10) + ct

    return generate_output()