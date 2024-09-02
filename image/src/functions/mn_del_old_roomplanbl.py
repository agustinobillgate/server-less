from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Resplan, Zimplan

def mn_del_old_roomplanbl():
    i = 0
    ci_date:date = None
    htparam = resplan = zimplan = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, ci_date, htparam, resplan, zimplan


        return {"i": i}

    def del_old_roomplan():

        nonlocal i, ci_date, htparam, resplan, zimplan

        anz:int = 0

        resplan = db_session.query(Resplan).filter(
                (Resplan.datum < ci_date)).first()
        while None != resplan:
            i = i + 1

            resplan = db_session.query(Resplan).first()
            db_session.delete(resplan)

            resplan = db_session.query(Resplan).filter(
                    (Resplan.datum < ci_date)).first()

        zimplan = db_session.query(Zimplan).filter(
                (Zimplan.datum < ci_date)).first()
        while None != zimplan:
            i = i + 1

            zimplan = db_session.query(Zimplan).first()
            db_session.delete(zimplan)

            zimplan = db_session.query(Zimplan).filter(
                    (Zimplan.datum < ci_date)).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    del_old_roomplan()

    return generate_output()