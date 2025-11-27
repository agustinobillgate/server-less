#using conversion tools version: 1.0.0.117

# ==================================
# Rulita, 27-11-2025
# - Added with_for_update all query 
# ==================================

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_maintain, Eg_action, Eg_mdetail, Bediener, Res_history, Eg_property

maintain_data, Maintain = create_model_like(Eg_maintain)
action_data, Action = create_model_like(Eg_action, {"selected":bool})

def eg_mainscheduleed_btn_go_webbl(maintain_data:[Maintain], action_data:[Action], user_init:string, mainno:int, str_property:string):

    prepare_cache ([Eg_maintain, Bediener, Res_history, Eg_property])

    eg_maintain = eg_action = eg_mdetail = bediener = res_history = eg_property = None

    maintain = action = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal eg_maintain, eg_action, eg_mdetail, bediener, res_history, eg_property
        nonlocal user_init, mainno, str_property


        nonlocal maintain, action

        return {}

    def create_log():

        nonlocal eg_maintain, eg_action, eg_mdetail, bediener, res_history, eg_property
        nonlocal user_init, mainno, str_property


        nonlocal maintain, action

        usr = None
        usrnr:int = 0
        char1:string = ""
        char2:string = ""
        ststat:List[string] = ["Scheduled", "Processed", "Done"]
        sttype:List[string] = ["Weekly", "Monthly", "Quarter", "Half Yearly", "Year"]
        Usr =  create_buffer("Usr",Bediener)

        usr = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if usr:
            usrnr = usr.nr

        eg_maintain = get_cache (Eg_maintain, {"maintainnr": [(eq, mainno)]})

        if eg_maintain.type != maintain.type:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = usrnr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Engineering"
            res_history.aenderung = "Change Status maintainNo " + to_string(mainno) +\
                    ": " + ststat[eg_maintain.type - 1] + " To " + ststat[maintain.type - 1]

        if eg_maintain.estworkdate != None:

            if eg_maintain.estworkdate != maintain.estworkdate:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = usrnr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "Engineering"
                res_history.aenderung = "Change estimate work date maintainNo " + to_string(mainno) +\
                        ": " + to_string(eg_maintain.estworkdate) + " To " + to_string(maintain.estworkdate)

        if eg_maintain.workdate != None:

            if eg_maintain.workdate != maintain.workdate:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = usrnr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "Engineering"
                res_history.aenderung = "Change estimate work date maintainNo " + to_string(mainno) +\
                        ": " + to_string(eg_maintain.workdate) + " To " + to_string(maintain.workdate)

        if eg_maintain.typework != maintain.typework:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = usrnr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Engineering"
            res_history.aenderung = "Change frequency of work maintainNo " + to_string(mainno) +\
                    ": " + sttype[eg_maintain.typework - 1] + " To " + sttype[maintain.typework - 1]

        if eg_maintain.propertynr != maintain.propertynr:

            eg_property = get_cache (Eg_property, {"nr": [(eq, eg_maintain.propertynr)]})

            if eg_property:
                char1 = eg_property.bezeich + "(" + to_string(eg_property.nr) + ")"
            char2 = str_property + "(" + to_string(maintain.propertynr) + ")"
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = usrnr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Engineering"
            res_history.aenderung = "Change Object Item maintainNo " + to_string(mainno) +\
                    ": " + char1 + " To " + char2

        if eg_maintain.pic != maintain.pic:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = usrnr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Engineering"
            res_history.aenderung = "Change PIC MaintainNo " + to_string(mainno) +\
                    ": " + to_string(eg_maintain.pic) + " To " + to_string(maintain.pic)

    maintain = query(maintain_data, first=True)
    create_log()

    # eg_maintain = get_cache (Eg_maintain, {"maintainnr": [(eq, maintain.maintainnr)]})
    eg_maintain = db_session.query(Eg_maintain).filter(
             (Eg_maintain.maintainnr == maintain.maintainnr)).with_for_update().first()

    if eg_maintain:
        pass
        buffer_copy(maintain, eg_maintain)
        # pass
        db_session.refresh(eg_maintain,with_for_update=True)

        eg_mdetail = get_cache (Eg_mdetail, {"key": [(eq, 1)],"maintainnr": [(eq, maintain.maintainnr)]})

        if eg_mdetail:

            for eg_mdetail in db_session.query(Eg_mdetail).filter(
                     (Eg_mdetail.key == 1) & (Eg_mdetail.maintainnr == maintain.maintainnr)).order_by(Eg_mdetail._recid).all():
                db_session.delete(eg_mdetail)

            for action in query(action_data, filters=(lambda action: action.selected)):
                eg_mdetail = Eg_mdetail()
                db_session.add(eg_mdetail)

                eg_mdetail.key = 1
                eg_mdetail.maintainnr = maintain.maintainnr
                eg_mdetail.nr = action.actionnr
                eg_mdetail.create_date = get_current_date()
                eg_mdetail.create_time = get_current_time_in_seconds()
                eg_mdetail.create_by = user_init

    return generate_output()
