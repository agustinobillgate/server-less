#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.intevent_1 import intevent_1
from models import Zimmer, Interface, Res_line

def update_rmextbl(froom:string, troom:string, curr_zinr:string, gname:string, ci_date:date):

    prepare_cache ([Zimmer, Res_line])

    zimmer = interface = res_line = None

    db_session = local_storage.db_session
    froom = froom.strip()
    troom = troom.strip()
    curr_zinr = curr_zinr.strip()
    gname = gname.strip()

    def generate_output():
        nonlocal zimmer, interface, res_line
        nonlocal froom, troom, curr_zinr, gname, ci_date

        return {}


    for zimmer in db_session.query(Zimmer).filter(
             (Zimmer.zinr >= (froom).lower()) & (Zimmer.zinr <= (troom).lower())).order_by((Zimmer.zinr)).all():

        # interface = get_cache (Interface, {"key": [(eq, 2)],"zinr": [(eq, zimmer.zinr)],"decfield": [(le, 3)]})
        interface = db_session.query(Interface).filter(
                 (Interface.key == 2) & (Interface.zinr == zimmer.zinr) & (Interface.decfield <= 3)).with_for_update().first()
        while None != interface:
            pass
            db_session.delete(interface)

            curr_recid = interface._recid
            interface = db_session.query(Interface).filter(
                     (Interface.key == 2) & (Interface.zinr == zimmer.zinr) & (Interface.decfield <= 3) & (Interface._recid > curr_recid)).first()
        curr_zinr = zimmer.zinr

        res_line = get_cache (Res_line, {"zinr": [(eq, zimmer.zinr)],"resstatus": [(eq, 6)]})

        if not res_line:

            res_line = get_cache (Res_line, {"zinr": [(eq, zimmer.zinr)],"resstatus": [(eq, 13)]})

        if res_line:
            gname = res_line.name
            get_output(intevent_1(1, res_line.zinr, "Manual Checkin!", res_line.resnr, res_line.reslinnr))
        else:
            gname = "Vacant"

            res_line = db_session.query(Res_line).filter(
                     (Res_line.resstatus == 8) & (Res_line.abreise == ci_date) & not_ (Res_line.zimmerfix)).first()

            if not res_line:

                res_line = get_cache (Res_line, {"resstatus": [(eq, 8)],"abreise": [(eq, ci_date)]})

            if res_line:
                get_output(intevent_1(2, zimmer.zinr, "Manual Checkout!", res_line.resnr, res_line.reslinnr))
            else:
                get_output(intevent_1(2, zimmer.zinr, "Manual Checkout!", 0, 0))

    return generate_output()