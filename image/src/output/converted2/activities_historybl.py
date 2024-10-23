from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Bediener, Res_history

def activities_historybl(usrid:str, action:str, from_date:date, to_date:date):
    b1_list_list = []
    bediener = res_history = None

    ubuff = b1_list = None

    b1_list_list, B1_list = create_model("B1_list", {"datum":date, "action":str, "aenderung":str, "username":str, "zeit":int})

    Ubuff = create_buffer("Ubuff",Bediener)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal b1_list_list, bediener, res_history
        nonlocal usrid, action, from_date, to_date
        nonlocal ubuff


        nonlocal ubuff, b1_list
        nonlocal b1_list_list
        return {"b1-list": b1_list_list}

    def disp_it():

        nonlocal b1_list_list, bediener, res_history
        nonlocal usrid, action, from_date, to_date
        nonlocal ubuff


        nonlocal ubuff, b1_list
        nonlocal b1_list_list

        if ((usrid != None)) and (action == None):

            bediener = db_session.query(Bediener).filter(
                     (Bediener.userinit == trim(entry(0, usrid, "-")))).first()

            res_history_obj_list = []
            for res_history, ubuff in db_session.query(Res_history, Ubuff).join(Ubuff,(Ubuff.nr == Res_history.nr)).filter(
                     (Res_history.datum >= from_date) & (Res_history.datum <= to_date) & (Res_history.nr == bediener.nr)).order_by(Res_history.datum, Res_history.action, Res_history.zeit).all():
                if res_history._recid in res_history_obj_list:
                    continue
                else:
                    res_history_obj_list.append(res_history._recid)


                assign_it()

            return

        if ((usrid == None)) and (action != None):

            res_history_obj_list = []
            for res_history, ubuff in db_session.query(Res_history, Ubuff).join(Ubuff,(Ubuff.nr == Res_history.nr)).filter(
                     (Res_history.datum >= from_date) & (Res_history.datum <= to_date) & (func.lower(Res_history.action) == (action).lower())).order_by(Res_history.datum, Res_history.action, Res_history.zeit).all():
                if res_history._recid in res_history_obj_list:
                    continue
                else:
                    res_history_obj_list.append(res_history._recid)


                assign_it()

            return

        if ((usrid != None)) and (action != None):

            bediener = db_session.query(Bediener).filter(
                     (Bediener.userinit == trim(entry(0, usrid, "-")))).first()

            res_history_obj_list = []
            for res_history, ubuff in db_session.query(Res_history, Ubuff).join(Ubuff,(Ubuff.nr == Res_history.nr)).filter(
                     (Res_history.datum >= from_date) & (Res_history.datum <= to_date) & (Res_history.nr == bediener.nr) & (func.lower(Res_history.action) == (action).lower())).order_by(Res_history.datum, Res_history.action, Res_history.zeit).all():
                if res_history._recid in res_history_obj_list:
                    continue
                else:
                    res_history_obj_list.append(res_history._recid)


                assign_it()

            return

        for res_history in db_session.query(Res_history).filter(
                 (Res_history.datum >= from_date) & (Res_history.datum <= to_date)).order_by(Res_history.datum, Res_history.action, Res_history.zeit).all():

            ubuff = db_session.query(Ubuff).filter(
                     (Ubuff.nr == res_history.nr)).first()
            assign_it()


    def assign_it():

        nonlocal b1_list_list, bediener, res_history
        nonlocal usrid, action, from_date, to_date
        nonlocal ubuff


        nonlocal ubuff, b1_list
        nonlocal b1_list_list


        b1_list = B1_list()
        b1_list_list.append(b1_list)

        b1_list.datum = res_history.datum
        b1_list.action = res_history.action
        b1_list.aenderung = res_history.aenderung
        b1_list.zeit = res_history.zeit

        if ubuff:
            b1_list.username = ubuff.username

    disp_it()

    return generate_output()