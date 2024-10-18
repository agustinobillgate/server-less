from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.intevent_1 import intevent_1
from models import Zimmer, Interface, Res_line

def update_rmextbl(froom:str, troom:str, curr_zinr:str, gname:str, ci_date:date):
    zimmer = interface = res_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal zimmer, interface, res_line
        nonlocal froom, troom, curr_zinr, gname, ci_date


        return {}


    for zimmer in db_session.query(Zimmer).filter(
             (func.lower(Zimmer.zinr) >= (froom).lower()) & (func.lower(Zimmer.zinr) <= (troom).lower())).order_by((Zimmer.zinr)).all():

        interface = db_session.query(Interface).filter(
                 (Interface.key == 2) & (Interface.zinr == zimmer.zinr) & (Interface.decfield <= 3)).first()
        while None != interface:
            db_session.delete(interface)

            curr_recid = interface._recid
            interface = db_session.query(Interface).filter(
                     (Interface.key == 2) & (Interface.zinr == zimmer.zinr) & (Interface.decfield <= 3)).filter(Interface._recid > curr_recid).first()
        curr_zinr = zimmer.zinr

        res_line = db_session.query(Res_line).filter(
                 (Res_line.zinr == zimmer.zinr) & (Res_line.resstatus == 6)).first()

        if not res_line:

            res_line = db_session.query(Res_line).filter(
                     (Res_line.zinr == zimmer.zinr) & (Res_line.resstatus == 13)).first()

        if res_line:
            gname = res_line.name
            get_output(intevent_1(1, res_line.zinr, "Manual Checkin!", res_line.resnr, res_line.reslinnr))
        else:
            gname = "Vacant"

            res_line = db_session.query(Res_line).filter(
                     (Res_line.resstatus == 8) & (Res_line.abreise == ci_date) & (not Res_line.zimmerfix)).first()

            if not res_line:

                res_line = db_session.query(Res_line).filter(
                         (Res_line.resstatus == 8) & (Res_line.abreise == ci_date)).first()

            if res_line:
                get_output(intevent_1(2, zimmer.zinr, "Manual Checkout!", res_line.resnr, res_line.reslinnr))
            else:
                get_output(intevent_1(2, zimmer.zinr, "Manual Checkout!", 0, 0))

    return generate_output()