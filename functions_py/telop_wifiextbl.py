#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from functions.intevent_1 import intevent_1
from models import Res_line, Interface

def telop_wifiextbl(case_type:int, resnr:int, reslinnr:int, sameresno:bool):

    prepare_cache ([Res_line])

    res_line = interface = None

    rbuff = None

    Rbuff = create_buffer("Rbuff",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_line, interface
        nonlocal case_type, resnr, reslinnr, sameresno
        nonlocal rbuff


        nonlocal rbuff

        return {}


    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

    if case_type == 1:

        # interface = get_cache (Interface, {"key": [(eq, 9)],"zinr": [(eq, res_line.zinr)],"decfield": [(le, 3)]})
        interface = db_session.query(Interface).filter(
                 (Interface.key == 9) & (Interface.zinr == res_line.zinr) & (Interface.decfield <= 3)).with_for_update().first()
        while None != interface:
            pass
            db_session.delete(interface)

            curr_recid = interface._recid
            interface = db_session.query(Interface).filter(
                     (Interface.key == 9) & (Interface.zinr == res_line.zinr) & 
                     (Interface.decfield <= 3) & (Interface._recid > curr_recid)).with_for_update().first()
        get_output(intevent_1(1, res_line.zinr, "Activate!", res_line.resnr, res_line.reslinnr))

    elif case_type == 2:

        # interface = get_cache (Interface, {"key": [(eq, 10)],"zinr": [(eq, res_line.zinr)],"decfield": [(le, 10)]})
        interface = db_session.query(Interface).filter(
                 (Interface.key == 10) & (Interface.zinr == res_line.zinr) & (Interface.decfield <= 10)).with_for_update().first()
        while None != interface:
            pass
            db_session.delete(interface)

            curr_recid = interface._recid
            interface = db_session.query(Interface).filter(
                     (Interface.key == 10) & (Interface.zinr == res_line.zinr) & 
                     (Interface.decfield <= 10) & (Interface._recid > curr_recid)).with_for_update().first()
        get_output(intevent_1(2, res_line.zinr, "Deactivate!", res_line.resnr, res_line.reslinnr))

        if sameresno:

            for rbuff in db_session.query(Rbuff).filter(
                     (Rbuff.resnr == res_line.resnr) & (Rbuff.active_flag == 1) & (Rbuff.resstatus == 6) & (Rbuff.zinr != res_line.zinr)).order_by(Rbuff._recid).all():

                # interface = get_cache (Interface, {"key": [(eq, 10)],"zinr": [(eq, rbuff.zinr)],"decfield": [(le, 10)]})
                interface = db_session.query(Interface).filter(
                         (Interface.key == 10) & (Interface.zinr == rbuff.zinr) & (Interface.decfield <= 10)).with_for_update().first()
                while None != interface:
                    pass
                    db_session.delete(interface)

                    curr_recid = interface._recid
                    interface = db_session.query(Interface).filter(
                             (Interface.key == 10) & (Interface.zinr == rbuff.zinr) & 
                             (Interface.decfield <= 10) & (Interface._recid > curr_recid)).with_for_update().first()
                get_output(intevent_1(2, rbuff.zinr, "Deactivate!", rbuff.resnr, rbuff.reslinnr))


    return generate_output()