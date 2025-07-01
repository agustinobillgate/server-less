#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line

def mbill_assignbl(resnr:int):

    prepare_cache ([Res_line])

    s_list_list = []
    res_line = None

    s_list = buf_s_list = None

    s_list_list, S_list = create_model("S_list", {"resnr":int, "zinr":string, "name":string, "ankunft":date, "abreise":date, "reslinnr":int, "assigned":bool, "ass":bool})
    buf_s_list_list, Buf_s_list = create_model_like(S_list)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_list_list, res_line
        nonlocal resnr


        nonlocal s_list, buf_s_list
        nonlocal s_list_list, buf_s_list_list

        return {"s-list": s_list_list}

    def create_list():

        nonlocal s_list_list, res_line
        nonlocal resnr


        nonlocal s_list, buf_s_list
        nonlocal s_list_list, buf_s_list_list

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == resnr) & (Res_line.resstatus != 12) & (Res_line.active_flag <= 1) & ((Res_line.l_zuordnung[inc_value(4)] == 0) | (Res_line.l_zuordnung[inc_value(4)] == resnr))).order_by(Res_line._recid).all():
            buf_s_list = Buf_s_list()
            buf_s_list_list.append(buf_s_list)

            buf_s_list.resnr = res_line.resnr
            buf_s_list.reslinnr = res_line.reslinnr
            buf_s_list.assigned = not logical(res_line.l_zuordnung[1])
            buf_s_list.ass = buf_s_list.assigned

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.l_zuordnung[inc_value(4)] == resnr) & (Res_line.resstatus != 12) & (Res_line.active_flag <= 1) & (Res_line.resnr != resnr)).order_by(Res_line._recid).all():
            buf_s_list = Buf_s_list()
            buf_s_list_list.append(buf_s_list)

            buf_s_list.resnr = res_line.resnr
            buf_s_list.reslinnr = res_line.reslinnr
            buf_s_list.assigned = not logical(res_line.l_zuordnung[1])
            buf_s_list.ass = buf_s_list.assigned


    create_list()

    res_line_obj_list = {}
    for res_line in db_session.query(Res_line).filter(
             ((Res_line.resnr.in_(list(set([buf_s_list.resnr for buf_s_list in buf_s_list_list])))) & (Res_line.reslinnr == buf_s_list.reslinnr))).order_by(Res_line.resnr, Res_line.zinr, Res_line.name).all():
        if res_line_obj_list.get(res_line._recid):
            continue
        else:
            res_line_obj_list[res_line._recid] = True

        buf_s_list = query(buf_s_list_list, (lambda buf_s_list: (res_line.resnr == buf_s_list.resnr)), first=True)
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.resnr = res_line.resnr
        s_list.zinr = res_line.zinr
        s_list.name = res_line.name
        s_list.ankunft = res_line.ankunft
        s_list.abreise = res_line.abreise
        s_list.reslinnr = buf_s_list.reslinnr
        s_list.assigned = buf_s_list.assigned
        s_list.ass = buf_s_list.ass


    return generate_output()