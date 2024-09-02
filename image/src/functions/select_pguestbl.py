from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bill, Res_line

def select_pguestbl(roomno:str, sorttype:int, gname:str):
    b1_list_list = []
    bill = res_line = None

    b1_list = bbuff = None

    b1_list_list, B1_list = create_model("B1_list", {"resnr":int, "reslinnr":int, "zinr":str, "name":str, "arrangement":str, "ankunft":date, "abreise":date})

    Bbuff = Bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal b1_list_list, bill, res_line
        nonlocal bbuff


        nonlocal b1_list, bbuff
        nonlocal b1_list_list
        return {"b1-list": b1_list_list}

    def disp_it():

        nonlocal b1_list_list, bill, res_line
        nonlocal bbuff


        nonlocal b1_list, bbuff
        nonlocal b1_list_list

        name:str = ""
        rmlen:int = 0
        rmlen = len(roomno)

        if sorttype == 1:

            res_line_obj_list = []
            for res_line, bbuff in db_session.query(Res_line, Bbuff).join(Bbuff,(Bbuff.resnr == Res_line.resnr) &  (Bbuff.reslinnr == Res_line.reslinnr)).filter(
                    (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (roomno))).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                assign_it()

        elif sorttype == 2:

            res_line_obj_list = []
            for res_line, bbuff in db_session.query(Res_line, Bbuff).join(Bbuff,(Bbuff.resnr == Res_line.resnr) &  (Bbuff.reslinnr == Res_line.reslinnr)).filter(
                    (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (roomno)) &  (func.lower(Res_line.name) >= (gname).lower())).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                assign_it()

            if res_line:
                roomno = res_line.zinr

    def assign_it():

        nonlocal b1_list_list, bill, res_line
        nonlocal bbuff


        nonlocal b1_list, bbuff
        nonlocal b1_list_list


        b1_list = B1_list()
        b1_list_list.append(b1_list)

        b1_list.resnr = res_line.resnr
        b1_list.reslinnr = res_line.reslinnr
        b1_list.zinr = res_line.zinr
        b1_list.name = res_line.name
        b1_list.arrangement = res_line.arrangement
        b1_list.ankunft = res_line.ankunft
        b1_list.abreise = res_line.abreise


    disp_it()

    return generate_output()