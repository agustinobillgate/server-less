from functions.additional_functions import *
import decimal
from models import Res_line, Bill, Bill_line

def auto_checkoutbl(resnr:int, sorttype:int):
    t_res_line_list = []
    resline1_list = []
    res_line = bill = bill_line = None

    t_res_line = resline1 = buf_resline1 = None

    t_res_line_list, T_res_line = create_model("T_res_line", {"resnr":int, "reslinnr":int, "name":str, "zinr":str, "resstatus":int, "active_flag":int})
    resline1_list, Resline1 = create_model("Resline1", {"resnr":int, "reslinnr":int, "resstatus":int})

    Buf_resline1 = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_res_line_list, resline1_list, res_line, bill, bill_line
        nonlocal buf_resline1


        nonlocal t_res_line, resline1, buf_resline1
        nonlocal t_res_line_list, resline1_list
        return {"t-res-line": t_res_line_list, "resline1": resline1_list}

    def grp_co():

        nonlocal t_res_line_list, resline1_list, res_line, bill, bill_line
        nonlocal buf_resline1


        nonlocal t_res_line, resline1, buf_resline1
        nonlocal t_res_line_list, resline1_list

        checked_out:bool = False
        Buf_resline1 = Res_line

        if sorttype == 1:

            res_line_obj_list = []
            for res_line, bill in db_session.query(Res_line, Bill).join(Bill,(Bill.resnr == Res_line.resnr) &  (Bill.reslinnr == Res_line.reslinnr)).filter(
                    (Res_line.resnr == resnr) &  (Res_line.zinr != "") &  (Res_line.active_flag == 1) &  (Res_line.resstatus != 12)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)

                bill_line = db_session.query(Bill_line).filter(
                        (Bill_line.rechnr == bill.rechnr)).first()

                if not bill_line:
                    t_res_line = T_res_line()
                    t_res_line_list.append(t_res_line)

                    t_res_line.resnr = res_line.resnr
                    t_res_line.reslinnr = res_line.reslinnr
                    t_res_line.name = res_line.name
                    t_res_line.zinr = res_line.zinr
                    t_res_line.resstatus = res_line.resstatus
                    t_res_line.active_flag = res_line.active_flag

                    buf_resline1 = db_session.query(Buf_resline1).filter(
                            (Buf_resline1.resnr == res_line.resnr) &  (Buf_resline1.reslinnr == res_line.reslinnr)).first()

                    if buf_resline1:
                        resline1 = Resline1()
                        resline1_list.append(resline1)

                        resline1.resnr = buf_resline1.resnr
                        resline1.reslinnr = buf_resline1.reslinnr
                        resline1.resstatus = buf_resline1.resstatus


        else:

            res_line_obj_list = []
            for res_line, bill in db_session.query(Res_line, Bill).join(Bill,(Bill.resnr == Res_line.resnr) &  (Bill.reslinnr == Res_line.reslinnr)).filter(
                    (Res_line.resnr == resnr) &  (Res_line.zinr != "") &  (Res_line.active_flag == 1) &  (Res_line.resstatus != 12)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                t_res_line = T_res_line()
                t_res_line_list.append(t_res_line)

                t_res_line.resnr = res_line.resnr
                t_res_line.reslinnr = res_line.reslinnr
                t_res_line.name = res_line.name
                t_res_line.zinr = res_line.zinr
                t_res_line.resstatus = res_line.resstatus
                t_res_line.active_flag = res_line.active_flag

                buf_resline1 = db_session.query(Buf_resline1).filter(
                        (Buf_resline1.resnr == res_line.resnr) &  (Buf_resline1.reslinnr == res_line.reslinnr)).first()

                if buf_resline1:
                    resline1 = Resline1()
                    resline1_list.append(resline1)

                    resline1.resnr = buf_resline1.resnr
                    resline1.reslinnr = buf_resline1.reslinnr
                    resline1.resstatus = buf_resline1.resstatus

    grp_co()

    return generate_output()