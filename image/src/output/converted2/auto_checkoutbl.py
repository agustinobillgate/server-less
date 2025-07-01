#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Bill, Bill_line

def auto_checkoutbl(resnr:int, sorttype:int):

    prepare_cache ([Res_line, Bill])

    t_res_line_list = []
    resline1_list = []
    res_line = bill = bill_line = None

    t_res_line = resline1 = None

    t_res_line_list, T_res_line = create_model("T_res_line", {"resnr":int, "reslinnr":int, "name":string, "zinr":string, "resstatus":int, "active_flag":int})
    resline1_list, Resline1 = create_model("Resline1", {"resnr":int, "reslinnr":int, "resstatus":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_res_line_list, resline1_list, res_line, bill, bill_line
        nonlocal resnr, sorttype


        nonlocal t_res_line, resline1
        nonlocal t_res_line_list, resline1_list

        return {"t-res-line": t_res_line_list, "resline1": resline1_list}

    def grp_co():

        nonlocal t_res_line_list, resline1_list, res_line, bill, bill_line
        nonlocal resnr, sorttype


        nonlocal t_res_line, resline1
        nonlocal t_res_line_list, resline1_list

        checked_out:bool = False
        buf_resline1 = None
        Buf_resline1 =  create_buffer("Buf_resline1",Res_line)

        if sorttype == 1:

            res_line_obj_list = {}
            res_line = Res_line()
            bill = Bill()
            for res_line.resnr, res_line.reslinnr, res_line.name, res_line.zinr, res_line.resstatus, res_line.active_flag, res_line._recid, bill.rechnr, bill._recid in db_session.query(Res_line.resnr, Res_line.reslinnr, Res_line.name, Res_line.zinr, Res_line.resstatus, Res_line.active_flag, Res_line._recid, Bill.rechnr, Bill._recid).join(Bill,(Bill.resnr == Res_line.resnr) & (Bill.reslinnr == Res_line.reslinnr)).filter(
                     (Res_line.resnr == resnr) & (Res_line.zinr != "") & (Res_line.active_flag == 1) & (Res_line.resstatus != 12)).order_by(Res_line.resstatus.desc(), Res_line.zinr, Res_line.name).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True

                bill_line = get_cache (Bill_line, {"rechnr": [(eq, bill.rechnr)]})

                if not bill_line:
                    t_res_line = T_res_line()
                    t_res_line_list.append(t_res_line)

                    t_res_line.resnr = res_line.resnr
                    t_res_line.reslinnr = res_line.reslinnr
                    t_res_line.name = res_line.name
                    t_res_line.zinr = res_line.zinr
                    t_res_line.resstatus = res_line.resstatus
                    t_res_line.active_flag = res_line.active_flag

                    buf_resline1 = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                    if buf_resline1:
                        resline1 = Resline1()
                        resline1_list.append(resline1)

                        resline1.resnr = buf_resline1.resnr
                        resline1.reslinnr = buf_resline1.reslinnr
                        resline1.resstatus = buf_resline1.resstatus


        else:

            res_line_obj_list = {}
            res_line = Res_line()
            bill = Bill()
            for res_line.resnr, res_line.reslinnr, res_line.name, res_line.zinr, res_line.resstatus, res_line.active_flag, res_line._recid, bill.rechnr, bill._recid in db_session.query(Res_line.resnr, Res_line.reslinnr, Res_line.name, Res_line.zinr, Res_line.resstatus, Res_line.active_flag, Res_line._recid, Bill.rechnr, Bill._recid).join(Bill,(Bill.resnr == Res_line.resnr) & (Bill.reslinnr == Res_line.reslinnr)).filter(
                     (Res_line.resnr == resnr) & (Res_line.zinr != "") & (Res_line.active_flag == 1) & (Res_line.resstatus != 12)).order_by(Res_line.resstatus.desc()).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                t_res_line = T_res_line()
                t_res_line_list.append(t_res_line)

                t_res_line.resnr = res_line.resnr
                t_res_line.reslinnr = res_line.reslinnr
                t_res_line.name = res_line.name
                t_res_line.zinr = res_line.zinr
                t_res_line.resstatus = res_line.resstatus
                t_res_line.active_flag = res_line.active_flag

                buf_resline1 = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                if buf_resline1:
                    resline1 = Resline1()
                    resline1_list.append(resline1)

                    resline1.resnr = buf_resline1.resnr
                    resline1.reslinnr = buf_resline1.reslinnr
                    resline1.resstatus = buf_resline1.resstatus


    grp_co()

    return generate_output()