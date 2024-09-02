from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Eg_maintain, Eg_action, Eg_mdetail, Bediener, Res_history, Eg_property

def eg_mainscheduleed_btn_go_webbl(maintain:[Maintain], action:[Action], user_init:str, mainno:int, str_property:str):
    eg_maintain = eg_action = eg_mdetail = bediener = res_history = eg_property = None

    maintain = action = usr = None

    maintain_list, Maintain = create_model_like(Eg_maintain)
    action_list, Action = create_model_like(Eg_action, {"selected":bool})

    Usr = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal eg_maintain, eg_action, eg_mdetail, bediener, res_history, eg_property
        nonlocal usr


        nonlocal maintain, action, usr
        nonlocal maintain_list, action_list
        return {}

    def create_log():

        nonlocal eg_maintain, eg_action, eg_mdetail, bediener, res_history, eg_property
        nonlocal usr


        nonlocal maintain, action, usr
        nonlocal maintain_list, action_list

        usrnr:int = 0
        char1:str = ""
        char2:str = ""
        ststat:[str] = ["", "", "", ""]
        sttype:[str] = ["", "", "", "", "", ""]
        Usr = Bediener

        usr = db_session.query(Usr).filter(
                (func.lower(Usr.userinit) == (user_init).lower())).first()

        if usr:
            usrnr = usr.nr

        eg_maintain = db_session.query(Eg_maintain).filter(
                (Eg_maintain.maintainnr == mainno)).first()

        if eg_maintain.TYPE != maintain.TYPE:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = usrnr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.Action = "Engineering"
            res_history.aenderung = "Change Status maintainNo " + to_string(mainno) +\
                    ": " + ststat[eg_maintain.TYPE - 1] + " To " + ststat[maintain.TYPE - 1]

        if eg_maintain.estworkdate != None:

            if eg_maintain.estworkdate != maintain.estworkdate:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = usrnr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.Action = "Engineering"
                res_history.aenderung = "Change estimate work date maintainNo " + to_string(mainno) +\
                        ": " + to_string(eg_maintain.estworkdate) + " To " + to_string(maintain.estworkdate)

        if eg_maintain.workdate != None:

            if eg_maintain.workdate != maintain.workdate:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = usrnr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.Action = "Engineering"
                res_history.aenderung = "Change estimate work date maintainNo " + to_string(mainno) +\
                        ": " + to_string(eg_maintain.workdate) + " To " + to_string(maintain.workdate)

        if eg_maintain.typework != maintain.typework:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = usrnr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.Action = "Engineering"
            res_history.aenderung = "Change frequency of work maintainNo " + to_string(mainno) +\
                    ": " + sttype[eg_maintain.typework - 1] + " To " + sttype[maintain.typework - 1]

        if eg_maintain.propertynr != maintain.propertynr:

            eg_property = db_session.query(Eg_property).filter(
                    (Eg_property.nr == eg_maintain.propertynr)).first()

            if eg_property:
                char1 = eg_property.bezeich + "(" + to_string(eg_property.nr) + ")"
            char2 = str_property + "(" + to_string(maintain.propertynr) + ")"
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = usrnr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.Action = "Engineering"
            res_history.aenderung = "Change Object Item maintainNo " + to_string(mainno) +\
                    ": " + char1 + " To " + char2

        if eg_maintain.pic != maintain.pic:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = usrnr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.Action = "Engineering"
            res_history.aenderung = "Change PIC MaintainNo " + to_string(mainno) +\
                    ": " + to_string(eg_maintain.pic) + " To " + to_string(maintain.pic)


    maintain = query(maintain_list, first=True)
    create_log()

    eg_maintain = db_session.query(Eg_maintain).filter(
            (Eg_maintain.maintainnr == maintain.maintainnr)).first()

    if eg_maintain:

        eg_maintain = db_session.query(Eg_maintain).first()
        buffer_copy(maintain, eg_maintain)

        eg_maintain = db_session.query(Eg_maintain).first()

        eg_mdetail = db_session.query(Eg_mdetail).filter(
                (Eg_mdetail.key == 1) &  (Eg_mdetail.maintainnr == maintain.maintainnr)).first()

        if eg_mdetail:

            for eg_mdetail in db_session.query(Eg_mdetail).filter(
                    (Eg_mdetail.key == 1) &  (Eg_mdetail.maintainnr == maintain.maintainnr)).all():
                db_session.delete(eg_mdetail)

            for action in query(action_list, filters=(lambda action :action.SELECTED)):
                eg_mdetail = Eg_mdetail()
                db_session.add(eg_mdetail)

                eg_mdetail.key = 1
                eg_mdetail.maintainnr = maintain.maintainnr
                eg_mdetail.nr = action.actionnr
                eg_mdetail.create_date = get_current_date()
                eg_mdetail.create_time = get_current_time_in_seconds()
                eg_mdetail.create_by = user_init

    return generate_output()