#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Zimmer, Zimkateg, Bediener, Res_history, Res_line, Queasy, Ratecode

zimmer_list_data, Zimmer_list = create_model_like(Zimmer)

def add_room_admin_1bl(pvilanguage:int, case_type:int, zimmer_list_data:[Zimmer_list], rm_feature:string, curr_mode:string, rmno:string, rmcatbez:string, user_init:string):

    prepare_cache ([Zimkateg, Bediener, Res_history, Queasy, Ratecode])

    msg_str = ""
    t_zimmer_data = []
    dynarate_list_data = []
    lvcarea:string = "add-room-admin"
    sleeping:bool = False
    zimmer = zimkateg = bediener = res_history = res_line = queasy = ratecode = None

    zimmer_list = t_zimmer = dynarate_list = None

    t_zimmer_data, T_zimmer = create_model_like(Zimmer)
    dynarate_list_data, Dynarate_list = create_model("Dynarate_list", {"prcode":string, "to_room":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, t_zimmer_data, dynarate_list_data, lvcarea, sleeping, zimmer, zimkateg, bediener, res_history, res_line, queasy, ratecode
        nonlocal pvilanguage, case_type, rm_feature, curr_mode, rmno, rmcatbez, user_init


        nonlocal zimmer_list, t_zimmer, dynarate_list
        nonlocal t_zimmer_data, dynarate_list_data

        return {"msg_str": msg_str, "t-zimmer": t_zimmer_data, "dynaRate-list": dynarate_list_data}

    def fill_zimmer():

        nonlocal msg_str, t_zimmer_data, dynarate_list_data, lvcarea, sleeping, zimmer, zimkateg, bediener, res_history, res_line, queasy, ratecode
        nonlocal pvilanguage, case_type, rm_feature, curr_mode, rmno, rmcatbez, user_init


        nonlocal zimmer_list, t_zimmer, dynarate_list
        nonlocal t_zimmer_data, dynarate_list_data

        if (case_type != 1) and (zimmer_list.sleeping != zimmer.sleeping):

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "RoomNo: " + zimmer.zinr + " change room active " +\
                    to_string(zimmer.sleeping) + " to " + to_string(zimmer_list.sleeping)
            res_history.action = "Room Admin"


            pass
            pass
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "RoomNo: " + zimmer.zinr + " change room active " + to_string(zimmer.sleeping) + " to " + to_string(zimmer_list.sleeping)
            res_history.action = "Log Availability"


            pass
            pass
        buffer_copy(zimmer_list, zimmer)
        zimmer.himmelsr = rm_feature

        if curr_mode.lower()  == ("chg").lower()  and zimmer.setup != zimmer_list.setup and zimmer.setup != 0:

            res_line = get_cache (Res_line, {"active_flag": [(eq, 1)],"zinr": [(eq, zimmer.zinr)]})
            while None != res_line:
                pass
                res_line.setup = zimmer_list.setup
                pass

                curr_recid = res_line._recid
                res_line = db_session.query(Res_line).filter(
                         (Res_line.active_flag == 1) & (Res_line.zinr == zimmer.zinr) & (Res_line._recid > curr_recid)).first()

            res_line = get_cache (Res_line, {"active_flag": [(eq, 0)],"zinr": [(eq, zimmer.zinr)]})
            while None != res_line:
                pass
                res_line.setup = zimmer_list.setup
                pass

                curr_recid = res_line._recid
                res_line = db_session.query(Res_line).filter(
                         (Res_line.active_flag == 0) & (Res_line.zinr == zimmer.zinr) & (Res_line._recid > curr_recid)).first()
        zimmer.setup = zimmer_list.setup

        if curr_mode.lower()  == ("chg").lower()  and sleeping != zimmer_list.sleeping:
            update_queasy()


    def check_dynarate():

        nonlocal msg_str, t_zimmer_data, dynarate_list_data, lvcarea, sleeping, zimmer, zimkateg, bediener, res_history, res_line, queasy, ratecode
        nonlocal pvilanguage, case_type, rm_feature, curr_mode, rmno, rmcatbez, user_init


        nonlocal zimmer_list, t_zimmer, dynarate_list
        nonlocal t_zimmer_data, dynarate_list_data

        tokcounter:int = 0
        iftask:string = ""
        ct:string = ""
        mestoken:string = ""
        mesvalue:string = ""
        days1:int = 0
        days2:int = 0
        to_room:int = 0

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 2) & (Queasy.logi2)).first()

        if not queasy:

            return

        zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, rmcatbez)]})

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 2) & (Queasy.logi2)).order_by(Queasy._recid).all():
            dynarate_list = Dynarate_list()
            dynarate_list_data.append(dynarate_list)

            dynarate_list.prcode = queasy.char1
            dynarate_list.to_room = 0
            to_room = 0
            days1 = 0
            days2 = 0

            for ratecode in db_session.query(Ratecode).filter(
                     (Ratecode.code == queasy.char1)).order_by(Ratecode._recid).all():
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

                if days1 == 0 and days2 == 0 and dynarate_list.to_room < to_room:
                    dynarate_list.to_room = to_room

            if dynarate_list.to_room == 0:
                dynarate_list_data.remove(dynarate_list)

        for dynarate_list in query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.dynarate_list.to_room < zimkateg.maxzimanz)):
            ct = ct + dynarate_list.prcode + " " + to_string(dynarate_list.to_room) + "; "

        if ct != "":
            msg_str = msg_str + chr_unicode(2) + translateExtended ("The MAX To-Room of following Ratecode(s) < Room QTY of the related Room Type", lvcarea, "") + " (= " + to_string(zimkateg.maxzimanz) + ")." + chr_unicode(10) + ct


    def update_queasy():

        nonlocal msg_str, t_zimmer_data, dynarate_list_data, lvcarea, sleeping, zimmer, zimkateg, bediener, res_history, res_line, queasy, ratecode
        nonlocal pvilanguage, case_type, rm_feature, curr_mode, rmno, rmcatbez, user_init


        nonlocal zimmer_list, t_zimmer, dynarate_list
        nonlocal t_zimmer_data, dynarate_list_data

        cat_flag:bool = False
        zikatnr:int = 0
        qsy = None
        Qsy =  create_buffer("Qsy",Queasy)

        queasy = get_cache (Queasy, {"key": [(eq, 152)]})

        if queasy:
            cat_flag = True

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer_list.zikatnr)]})

        if zimkateg:

            if cat_flag:
                zikatnr = zimkateg.typ
            else:
                zikatnr = zimkateg.zikatnr

        queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(ge, get_current_date())],"number1": [(eq, zikatnr)]})
        while None != queasy and queasy.logi1 == False and queasy.logi2 == False :

            qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

            if qsy:
                qsy.logi2 = True
                pass
                pass

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 171) & (Queasy.date1 >= get_current_date()) & (Queasy.number1 == zikatnr) & (Queasy._recid > curr_recid)).first()

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "RoomNo: " + zimmer.zinr
        res_history.action = "Log Availability"


        pass
        pass


    zimmer_list = query(zimmer_list_data, first=True)

    if case_type == 1:

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer_list.zikatnr)]})
        zimkateg.maxzimanz = zimkateg.maxzimanz + 1
        pass
        zimmer = Zimmer()
        db_session.add(zimmer)

        fill_zimmer()
        update_queasy()
    else:

        zimmer = get_cache (Zimmer, {"zinr": [(eq, rmno)]})
        sleeping = zimmer.sleeping
        fill_zimmer()
    dynarate_list_data.clear()

    for zimmer in db_session.query(Zimmer).order_by(Zimmer.zinr).all():
        t_zimmer = T_zimmer()
        t_zimmer_data.append(t_zimmer)

        buffer_copy(zimmer, t_zimmer)

    return generate_output()