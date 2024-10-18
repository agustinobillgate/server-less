from functions.additional_functions import *
import decimal
from functions.intevent_1 import intevent_1
from models import Interface, Res_line, Htparam

def linext_act_deactbl(case_type:int, sameresno:bool, resnr:int, reslinnr:int):
    success_flag = False
    interface = res_line = htparam = None

    intbuff = rbuff = None

    Intbuff = create_buffer("Intbuff",Interface)
    Rbuff = create_buffer("Rbuff",Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, interface, res_line, htparam
        nonlocal case_type, sameresno, resnr, reslinnr
        nonlocal intbuff, rbuff


        nonlocal intbuff, rbuff
        return {"success_flag": success_flag}

    def activate_linext():

        nonlocal success_flag, interface, res_line, htparam
        nonlocal case_type, sameresno, resnr, reslinnr
        nonlocal intbuff, rbuff


        nonlocal intbuff, rbuff

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 307)).first()

        if not htparam.flogical:

            return

        interface = db_session.query(Interface).filter(
                 (Interface.key == 2) & (Interface.zinr == res_line.zinr) & (Interface.decfield <= 3)).first()
        while None != interface:

            intbuff = db_session.query(Intbuff).filter(
                         (Intbuff._recid == interface._recid)).first()
            intbuff_list.remove(intbuff)
            pass


            curr_recid = interface._recid
            interface = db_session.query(Interface).filter(
                     (Interface.key == 2) & (Interface.zinr == res_line.zinr) & (Interface.decfield <= 3)).filter(Interface._recid > curr_recid).first()

        if res_line:
            get_output(intevent_1(1, res_line.zinr, "Activate!", res_line.resnr, res_line.reslinnr))
            success_flag = True


    def deactivate_linext():

        nonlocal success_flag, interface, res_line, htparam
        nonlocal case_type, sameresno, resnr, reslinnr
        nonlocal intbuff, rbuff


        nonlocal intbuff, rbuff

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 307)).first()

        if not htparam.flogical:

            return

        interface = db_session.query(Interface).filter(
                 (Interface.key == 2) & (Interface.zinr == res_line.zinr) & (Interface.decfield <= 3)).first()
        while None != interface:
            db_session.delete(interface)

            curr_recid = interface._recid
            interface = db_session.query(Interface).filter(
                     (Interface.key == 2) & (Interface.zinr == res_line.zinr) & (Interface.decfield <= 3)).filter(Interface._recid > curr_recid).first()
        get_output(intevent_1(2, res_line.zinr, "Deactivate!", res_line.resnr, res_line.reslinnr))

        if sameresno:

            for rbuff in db_session.query(Rbuff).filter(
                     (Rbuff.resnr == res_line.resnr) & (Rbuff.active_flag == 1) & (Rbuff.resstatus == 6) & (Rbuff.zinr != res_line.zinr)).order_by(Rbuff._recid).all():

                interface = db_session.query(Interface).filter(
                         (Interface.key == 2) & (Interface.zinr == rbuff.zinr) & (Interface.decfield <= 3)).first()
                while None != interface:
                    db_session.delete(interface)

                    curr_recid = interface._recid
                    interface = db_session.query(Interface).filter(
                             (Interface.key == 2) & (Interface.zinr == rbuff.zinr) & (Interface.decfield <= 3)).filter(Interface._recid > curr_recid).first()
                get_output(intevent_1(2, rbuff.zinr, "Deactivate!", rbuff.resnr, rbuff.reslinnr))

        success_flag = True

    res_line = db_session.query(Res_line).filter(
             (Res_line.resnr == resnr) & (Res_line.reslinnr == reslinnr)).first()

    if case_type == 1:
        activate_linext()
    elif case_type == 2:
        deactivate_linext()

    return generate_output()