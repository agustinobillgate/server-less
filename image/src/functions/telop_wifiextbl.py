from functions.additional_functions import *
import decimal
from functions.intevent_1 import intevent_1
from models import Res_line, Interface

def telop_wifiextbl(case_type:int, resnr:int, reslinnr:int, sameresno:bool):
    res_line = interface = None
    rbuff = None
    Rbuff = Res_line
    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_line, interface
        nonlocal rbuff

        nonlocal rbuff
        return {}

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()

    if case_type == 1:
        local_storage.debugging = local_storage.debugging + ",1:"
        interface = db_session.query(Interface).filter(
                (Interface.key == 9) &  (Interface.zinr == res_line.zinr) &  (Interface.decfield <= 3)).first()
        while None != interface:

            interface = db_session.query(Interface).first()
            db_session.delete(interface)

            interface = db_session.query(Interface).filter(
                    (Interface.key == 9) &  (Interface.zinr == res_line.zinr) &  (Interface.decfield <= 3)).first()
        # TF update
        get_output(intevent_1(1, res_line.zinr, "Activate!", res_line.resnr, res_line.reslinnr))

    elif case_type == 2:
        local_storage.debugging = local_storage.debugging + ",2:"
        interface = db_session.query(Interface).filter(
                (Interface.key == 10) &  (Interface.zinr == res_line.zinr) &  (Interface.decfield <= 10)).first()
        while None != interface:

            interface = db_session.query(Interface).first()
            db_session.delete(interface)

            interface = db_session.query(Interface).filter(
                    (Interface.key == 10) &  (Interface.zinr == res_line.zinr) &  (Interface.decfield <= 10)).first()
        # TF update
        get_output(intevent_1(2, res_line.zinr, "Deactivate!", res_line.resnr, res_line.reslinnr))

        if sameresno:

            for rbuff in db_session.query(Rbuff).filter(
                    (Rbuff.resnr == res_line.resnr) &  (Rbuff.active_flag == 1) &  (Rbuff.resstatus == 6) &  (Rbuff.zinr != res_line.zinr)).all():

                interface = db_session.query(Interface).filter(
                        (Interface.key == 10) &  (Interface.zinr == rbuff.zinr) &  (Interface.decfield <= 10)).first()
                while None != interface:

                    interface = db_session.query(Interface).first()
                    db_session.delete(interface)

                    interface = db_session.query(Interface).filter(
                            (Interface.key == 10) &  (Interface.zinr == rbuff.zinr) &  (Interface.decfield <= 10)).first()
                # TF update
                get_output(intevent_1(2, rbuff.zinr, "Deactivate!", rbuff.resnr, rbuff.reslinnr))


    return generate_output()