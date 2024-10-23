from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Resplan, Zimplan

na_list_list, Na_list = create_model("Na_list", {"reihenfolge":int, "flag":int, "bezeich":str, "anz":int})

def del_roomplanbl(na_list_list:[Na_list], ci_date:date):
    i = 0
    htparam = resplan = zimplan = None

    na_list = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, htparam, resplan, zimplan
        nonlocal ci_date


        nonlocal na_list
        nonlocal na_list_list
        return {"na-list": na_list_list, "i": i}

    def del_roomplan():

        nonlocal i, htparam, resplan, zimplan
        nonlocal ci_date


        nonlocal na_list
        nonlocal na_list_list

        resplan = db_session.query(Resplan).filter(
                 (Resplan.datum >= ci_date)).first()

        na_list = query(na_list_list, filters=(lambda na_list: na_list.reihenfolge == 1), first=True)
        while None != resplan:
            i = i + 1
            na_list.anz = na_list.anz + 1
            db_session.delete(resplan)
            pass


            curr_recid = resplan._recid
            resplan = db_session.query(Resplan).filter(
                     (Resplan.datum >= ci_date)).filter(Resplan._recid > curr_recid).first()

        zimplan = db_session.query(Zimplan).filter(
                 (Zimplan.datum >= ci_date)).first()
        while None != zimplan:
            i = i + 1
            na_list.anz = na_list.anz + 1
            db_session.delete(zimplan)
            pass


            curr_recid = zimplan._recid
            zimplan = db_session.query(Zimplan).filter(
                     (Zimplan.datum >= ci_date)).filter(Zimplan._recid > curr_recid).first()


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 592)).first()
    htparam.flogical = True


    del_roomplan()

    return generate_output()