#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, Queasy, Res_history

def activities_history_webbl(usrid:string, action:string, from_date:date, to_date:date, idflag:string):

    prepare_cache ([Bediener, Queasy, Res_history])

    b1_list_list = []
    counter:int = 0
    bediener = queasy = res_history = None

    ubuff = bqueasy = b1_list = None

    b1_list_list, B1_list = create_model("B1_list", {"datum":date, "action":string, "aenderung":string, "username":string, "zeit":int})

    Ubuff = create_buffer("Ubuff",Bediener)
    Bqueasy = create_buffer("Bqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal b1_list_list, counter, bediener, queasy, res_history
        nonlocal usrid, action, from_date, to_date, idflag
        nonlocal ubuff, bqueasy


        nonlocal ubuff, bqueasy, b1_list
        nonlocal b1_list_list

        return {"b1-list": b1_list_list}

    def disp_it():

        nonlocal b1_list_list, counter, bediener, queasy, res_history
        nonlocal usrid, action, from_date, to_date, idflag
        nonlocal ubuff, bqueasy


        nonlocal ubuff, bqueasy, b1_list
        nonlocal b1_list_list

        if ((usrid != None)) and (action == None):

            bediener = get_cache (Bediener, {"userinit": [(eq, trim(entry(0, usrid, "-")))]})

            res_history_obj_list = {}
            res_history = Res_history()
            ubuff = Bediener()
            for res_history.nr, res_history.datum, res_history.action, res_history.aenderung, res_history.zeit, res_history._recid, ubuff.nr, ubuff._recid, ubuff.username in db_session.query(Res_history.nr, Res_history.datum, Res_history.action, Res_history.aenderung, Res_history.zeit, Res_history._recid, Ubuff.nr, Ubuff._recid, Ubuff.username).join(Ubuff,(Ubuff.nr == Res_history.nr)).filter(
                     (Res_history.datum >= from_date) & (Res_history.datum <= to_date) & (Res_history.nr == bediener.nr)).order_by(Res_history._recid).all():
                if res_history_obj_list.get(res_history._recid):
                    continue
                else:
                    res_history_obj_list[res_history._recid] = True


                assign_it()

            return

        if ((usrid == None)) and (action != None):

            res_history_obj_list = {}
            res_history = Res_history()
            ubuff = Bediener()
            for res_history.nr, res_history.datum, res_history.action, res_history.aenderung, res_history.zeit, res_history._recid, ubuff.nr, ubuff._recid, ubuff.username in db_session.query(Res_history.nr, Res_history.datum, Res_history.action, Res_history.aenderung, Res_history.zeit, Res_history._recid, Ubuff.nr, Ubuff._recid, Ubuff.username).join(Ubuff,(Ubuff.nr == Res_history.nr)).filter(
                     (Res_history.datum >= from_date) & (Res_history.datum <= to_date) & (Res_history.action == (action).lower())).order_by(Res_history.datum, Res_history.action, Res_history.zeit).all():
                if res_history_obj_list.get(res_history._recid):
                    continue
                else:
                    res_history_obj_list[res_history._recid] = True


                assign_it()

            return

        if ((usrid != None)) and (action != None):

            bediener = get_cache (Bediener, {"userinit": [(eq, trim(entry(0, usrid, "-")))]})

            res_history_obj_list = {}
            res_history = Res_history()
            ubuff = Bediener()
            for res_history.nr, res_history.datum, res_history.action, res_history.aenderung, res_history.zeit, res_history._recid, ubuff.nr, ubuff._recid, ubuff.username in db_session.query(Res_history.nr, Res_history.datum, Res_history.action, Res_history.aenderung, Res_history.zeit, Res_history._recid, Ubuff.nr, Ubuff._recid, Ubuff.username).join(Ubuff,(Ubuff.nr == Res_history.nr)).filter(
                     (Res_history.datum >= from_date) & (Res_history.datum <= to_date) & (Res_history.nr == bediener.nr) & (Res_history.action == (action).lower())).order_by(Res_history.datum, Res_history.action, Res_history.zeit).all():
                if res_history_obj_list.get(res_history._recid):
                    continue
                else:
                    res_history_obj_list[res_history._recid] = True


                assign_it()

            return

        for res_history in db_session.query(Res_history).filter(
                 (Res_history.datum >= from_date) & (Res_history.datum <= to_date)).order_by(Res_history.datum, Res_history.action, Res_history.zeit).all():

            ubuff = get_cache (Bediener, {"nr": [(eq, res_history.nr)]})
            assign_it()


    def assign_it():

        nonlocal b1_list_list, counter, bediener, queasy, res_history
        nonlocal usrid, action, from_date, to_date, idflag
        nonlocal ubuff, bqueasy


        nonlocal ubuff, bqueasy, b1_list
        nonlocal b1_list_list


        b1_list = B1_list()
        b1_list_list.append(b1_list)

        b1_list.datum = res_history.datum
        b1_list.action = res_history.action
        b1_list.aenderung = res_history.aenderung
        b1_list.zeit = res_history.zeit

        if ubuff:
            b1_list.username = ubuff.username

    queasy = Queasy()
    db_session.add(queasy)

    queasy.key = 285
    queasy.char1 = "System Logfiles"
    queasy.number1 = 1
    queasy.char2 = idflag


    pass
    disp_it()

    b1_list = query(b1_list_list, first=True)
    while None != b1_list:
        counter = counter + 1


        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 280
        queasy.char1 = "System Logfiles"
        queasy.char2 = idflag
        queasy.char3 = to_string(b1_list.datum) + "$" +\
                to_string(b1_list.action) + "$" +\
                to_string(b1_list.aenderung) + "$" +\
                to_string(b1_list.username) + "$" +\
                to_string(b1_list.zeit, "HH:MM:SS")


        queasy.number1 = counter

        b1_list = query(b1_list_list, next=True)

    bqueasy = get_cache (Queasy, {"key": [(eq, 285)],"char1": [(eq, "system logfiles")],"char2": [(eq, idflag)]})

    if bqueasy:
        pass
        bqueasy.number1 = 0


        pass
        pass

    return generate_output()