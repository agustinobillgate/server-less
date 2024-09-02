from functions.additional_functions import *
import decimal
from datetime import date
from models import Eg_request, Htparam, Eg_queasy, Bediener, Eg_property, Counters, Eg_location, Queasy, Res_line, History, Guest

def eg_mkreq_btn_go_webbl(request1:[Request1], sguestflag:bool, sub_str:str, main_str:str, prop_bezeich:str):
    ci_date:date = None
    eg_request = htparam = eg_queasy = bediener = eg_property = counters = eg_location = queasy = res_line = history = guest = None

    request1 = buff = usr = buff_property = resline1 = guest1 = None

    request1_list, Request1 = create_model_like(Eg_request)

    Buff = Eg_queasy
    Usr = Bediener
    Buff_property = Eg_property
    Resline1 = Res_line
    Guest1 = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, eg_request, htparam, eg_queasy, bediener, eg_property, counters, eg_location, queasy, res_line, history, guest
        nonlocal buff, usr, buff_property, resline1, guest1


        nonlocal request1, buff, usr, buff_property, resline1, guest1
        nonlocal request1_list
        return {}

    def create_history():

        nonlocal ci_date, eg_request, htparam, eg_queasy, bediener, eg_property, counters, eg_location, queasy, res_line, history, guest
        nonlocal buff, usr, buff_property, resline1, guest1


        nonlocal request1, buff, usr, buff_property, resline1, guest1
        nonlocal request1_list

        strmemo:str = ""
        nr:int = 0
        prop_nr:int = 0
        Buff = Eg_queasy
        Usr = Bediener
        Buff_property = Eg_property

        counters = db_session.query(Counters).filter(
                    (Counters.counter_no == 34)).first()

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 34
            counters.counter_bez = "Counter for Engineering RequestNo"
            counters.counter = 1

            counters = db_session.query(Counters).first()
        else:

            counters = db_session.query(Counters).first()
            counters.counter = counters.counter + 1

            counters = db_session.query(Counters).first()
        request1.reqnr = counters.counter


        request1.opened_time = get_current_time_in_seconds()

        if request1.propertynr == 0:

            for buff_property in db_session.query(Buff_property).all():
                prop_nr = buff_property.nr
                break
            prop_nr = prop_nr + 1
            eg_property = Eg_property()
            db_session.add(eg_property)

            eg_property.nr = prop_nr
            eg_property.bezeich = prop_bezeich
            eg_property.maintask = request1.maintask
            eg_property.zinr = request1.zinr
            eg_property.datum = get_current_date()

            if sguestflag :

                eg_location = db_session.query(Eg_location).filter(
                            (Eg_location.guestflag)).first()

                if eg_location:
                    eg_property.location = eg_location.nr
            else:
                eg_property.location = request1.reserve_int

            queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 133) &  (Queasy.number1 == request1.maintask)).first()

            if queasy:

                if not queasy:
                    request1.propertynr = prop_nr

            if sguestflag :

                eg_location = db_session.query(Eg_location).filter(
                            (Eg_location.guestflag)).first()

                if eg_location:
                    request1.reserve_int = eg_location.nr

                if request1.zinr != "" or request1.zinr != None:
                    get_guestname()
            request1.subtask_bezeich = sub_str


            eg_request = Eg_request()
            db_session.add(eg_request)

            buffer_copy(request1, eg_request)

            eg_request = db_session.query(Eg_request).first()

            for buff in db_session.query(Buff).filter(
                        (Buff.key == 3) &  (Buff.reqnr == request1.reqnr)).all():

                if buff.hist_nr > nr:
                    nr = buff.hist_nr
            eg_queasy = Eg_queasy()
            db_session.add(eg_queasy)

            eg_queasy.key = 3
            eg_queasy.reqnr = request1.reqnr
            eg_queasy.hist_nr = nr + 1
            eg_queasy.hist_time = get_current_time_in_seconds()
            eg_queasy.hist_fdate = get_current_date()

            if request1.assign_to != 0:
                eg_queasy.usr_nr = request1.assign_to

                eg_queasy = db_session.query(Eg_queasy).first()

            Resline1 = Res_line

            resline1 = db_session.query(Resline1).filter(
                    (Resline1.resnr == request1.resnr) &  (Resline1.reslinnr == request1.reslinnr)).first()
            history = History()
            db_session.add(history)

            history.gastnr = request1.gastnr
            history.resnr = request1.resnr
            history.reslinnr = request1.reslinnr
            history.zi_wechsel = True
            history.bemerk = main_str + ", " + sub_str + ", " + request1.task_def

            if resline1:
                history.ankunft = resline1.ankunft
                history.abreise = resline1.abreise
                history.zinr = resline1.zinr

            history = db_session.query(History).first()

    def get_guestname():

        nonlocal ci_date, eg_request, htparam, eg_queasy, bediener, eg_property, counters, eg_location, queasy, res_line, history, guest
        nonlocal buff, usr, buff_property, resline1, guest1


        nonlocal request1, buff, usr, buff_property, resline1, guest1
        nonlocal request1_list


            Resline1 = Res_line
            Guest1 = Guest

            resline1 = db_session.query(Resline1).filter(
                    (Resline1.active_flag == 1) &  (Resline1.zinr == request1.zinr) &  (Resline1.resstatus != 12) &  (Resline1.ankunft <= ci_date) &  (Resline1.abreise >= ci_date)).first()

            if resline1:

                guest1 = db_session.query(Guest1).filter(
                        (Guest1.gastnr == resline1.gastnrmember)).first()

                if guest1:
                    request1.gastnr = resline1.gastnrmember
                    request1.resnr = resline1.resnr
                    request1.reslinnr = resline1.reslinnr

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    request1 = query(request1_list, first=True)
    create_request()
    create_history()

    return generate_output()