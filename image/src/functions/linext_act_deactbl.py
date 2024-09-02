from functions.additional_functions import *
import decimal
from functions.intevent_1 import intevent_1
from models import Res_line, Interface, Htparam

def linext_act_deactbl(case_type:int, sameresno:bool, resnr:int, reslinnr:int):
    success_flag = False
    res_line = interface = htparam = None

    intbuff = rbuff = None

    Intbuff = Interface
    Rbuff = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, res_line, interface, htparam
        nonlocal intbuff, rbuff


        nonlocal intbuff, rbuff
        return {"success_flag": success_flag}

    def activate_linext():

        nonlocal success_flag, res_line, interface, htparam
        nonlocal intbuff, rbuff
        nonlocal intbuff, rbuff
        Intbuff = Interface
        local_storage.debugging = local_storage.debugging + ",Activate"
        htparam = db_session.query(Htparam).filter((Htparam.paramnr == 307)).first()

        if not htparam.flogical:
            local_storage.debugging = local_storage.debugging + ",par307:False"
            # return
        
        local_storage.debugging = local_storage.debugging + ",par307"
        interface = db_session.query(Interface).filter(
                (Interface.key == 2) &  (Interface.zinr == res_line.zinr) &  (Interface.decfield <= 3)).first()
        while None != interface:
            local_storage.debugging = local_storage.debugging + ",while"
            intbuff = db_session.query(Intbuff).filter(
                        (Intbuff._recid == interface._recid)).first()
            if intbuff:
                db_session.delete(intbuff)

            interface = db_session.query(Interface).filter(
                    (Interface.key == 2) &  (Interface.zinr == res_line.zinr) &  (Interface.decfield <= 3)).first()
            
        if res_line:
            # remark, TF update
            print("ResLine:", res_line.resnr)
            get_output(intevent_1(1, res_line.zinr, "Activate!", res_line.resnr, res_line.reslinnr))
            local_storage.debugging = local_storage.debugging + ",54:activate"
            success_flag = True
        else:
            local_storage.debugging = local_storage.debugging + ",57:No_resline"

    def deactivate_linext():

        nonlocal success_flag, res_line, interface, htparam
        nonlocal intbuff, rbuff

        nonlocal intbuff, rbuff

        Rbuff = Res_line
        local_storage.debugging = local_storage.debugging + ",Deactivate"
        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 307)).first()

        if not htparam.flogical:
            # return
            pass

        local_storage.debugging = local_storage.debugging + ",76:par307"
        interface = db_session.query(Interface).filter(
                (Interface.key == 2) &  (Interface.zinr == res_line.zinr) &  (Interface.decfield <= 3)).first()
        while None != interface:
            local_storage.debugging = local_storage.debugging + ",80:par307"
            db_session.delete(interface)
            interface = db_session.query(Interface).filter(
                    (Interface.key == 2) &  (Interface.zinr == res_line.zinr) &  (Interface.decfield <= 3)).first()
            
            local_storage.debugging = local_storage.debugging + ",85:delete"
        # remark, TF update
        get_output(intevent_1(2, res_line.zinr, "Deactivate!", res_line.resnr, res_line.reslinnr))

        if sameresno:

            for rbuff in db_session.query(Rbuff).filter(
                    (Rbuff.resnr == res_line.resnr) &  (Rbuff.active_flag == 1) &  (Rbuff.resstatus == 6) &  (Rbuff.zinr != res_line.zinr)).all():

                interface = db_session.query(Interface).filter(
                        (Interface.key == 2) &  (Interface.zinr == rbuff.zinr) &  (Interface.decfield <= 3)).first()
                while None != interface:

                    interface = db_session.query(Interface).first()
                    db_session.delete(interface)

                    interface = db_session.query(Interface).filter(
                            (Interface.key == 2) &  (Interface.zinr == rbuff.zinr) &  (Interface.decfield <= 3)).first()
                # remark, TF update
                get_output(intevent_1(2, rbuff.zinr, "Deactivate!", rbuff.resnr, rbuff.reslinnr))

        success_flag = True


    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()

    if case_type == 1:
        activate_linext()
    elif case_type == 2:
        deactivate_linext()

    local_storage.debugging = local_storage.debugging + ",117"
    return generate_output()