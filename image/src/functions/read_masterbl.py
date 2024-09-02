from functions.additional_functions import *
import decimal
from models import Master, Bill, Res_line

def read_masterbl(case_type:int, resno:int, gastno:int):
    t_master_list = []
    billno:int = 0
    master = bill = res_line = None

    t_master = mbill = None

    t_master_list, T_master = create_model_like(Master)

    Mbill = Bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_master_list, billno, master, bill, res_line
        nonlocal mbill


        nonlocal t_master, mbill
        nonlocal t_master_list
        return {"t-master": t_master_list}

    if case_type == 1:

        master = db_session.query(Master).filter(
                (Master.resnr == resno)).first()

        if master:
            t_master = T_master()
            t_master_list.append(t_master)

            buffer_copy(master, t_master)
    elif case_type == 2:

        master = db_session.query(Master).filter(
                (Master.resnr == resno) &  (Master.flag == 0)).first()

        if master:
            t_master = T_master()
            t_master_list.append(t_master)

            buffer_copy(master, t_master)
    elif case_type == 3:

        master = db_session.query(Master).filter(
                (Master.resnr == resno) &  (Master.active) &  (Master.flag == 0)).first()

        if master:
            t_master = T_master()
            t_master_list.append(t_master)

            buffer_copy(master, t_master)
    elif case_type == 4:

        master = db_session.query(Master).filter(
                (Master.gastnr == gastno) &  (Master.resnr == resno)).first()

        if master:
            t_master = T_master()
            t_master_list.append(t_master)

            buffer_copy(master, t_master)
    elif case_type == 5:
        billno = gastno

        bill = db_session.query(Bill).filter(
                (Bill.rechnr == billno)).first()

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.parent_nr)).first()

        if res_line.l_zuordnung[4] != 0:

            mbill = db_session.query(Mbill).filter(
                    (Mbill.resnr == res_line.l_zuordnung[4]) &  (Mbill.reslinnr == 0)).first()
        else:

            mbill = db_session.query(Mbill).filter(
                    (Mbill.resnr == res_line.resnr) &  (Mbill.reslinnr == 0)).first()

        if not mbill:

            return generate_output()

        master = db_session.query(Master).filter(
                (Master.resnr == mbill.resnr)).first()

        if master:
            t_master = T_master()
            t_master_list.append(t_master)

            buffer_copy(master, t_master)

    return generate_output()