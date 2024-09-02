from functions.additional_functions import *
import decimal
from models import Guest, Zimkateg, Res_line

def approve_list_disp_rsvbl(resnr:int, reslinnr:int, gastnr:int):
    b3_list_list = []
    guest = zimkateg = res_line = None

    b3_list = None

    b3_list_list, B3_list = create_model("B3_list", {"resnr":int, "ankunft":date, "abreise":date, "name":str, "vorname1":str, "zimmeranz":int, "kurzbez":str, "zinr":str, "resstatus":int, "erwachs":int, "kind1":int, "kind2":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal b3_list_list, guest, zimkateg, res_line


        nonlocal b3_list
        nonlocal b3_list_list
        return {"b3-list": b3_list_list}

    def assign_it():

        nonlocal b3_list_list, guest, zimkateg, res_line


        nonlocal b3_list
        nonlocal b3_list_list


        b3_list = B3_list()
        b3_list_list.append(b3_list)

        b3_list.resnr = res_line.resnr
        b3_list.ankunft = res_line.ankunft
        b3_list.abreise = res_line.abreise
        b3_list.name = guest.name
        b3_list.vorname1 = guest.vorname1
        b3_list.zimmeranz = res_line.zimmeranz
        b3_list.kurzbez = zimkateg.kurzbez
        b3_list.zinr = res_line.zinr
        b3_list.resstatus = res_line.resstatus
        b3_list.erwachs = res_line.erwachs
        b3_list.kind1 = res_line.kind1
        b3_list.kind2 = res_line.kind2

    if resnr != 0:

        if reslinnr == 0:

            res_line_obj_list = []
            for res_line, guest, zimkateg in db_session.query(Res_line, Guest, Zimkateg).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                    (Res_line.resnr == resnr) &  ((Res_line.active_flag == 1) |  (Res_line.active_flag == 0)) &  (Res_line.resstatus != 12)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                assign_it()
        else:

            res_line_obj_list = []
            for res_line, guest, zimkateg in db_session.query(Res_line, Guest, Zimkateg).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                    (Res_line.resnr == resnr) &  ((Res_line.active_flag == 1) |  (Res_line.active_flag == 0)) &  (Res_line.resstatus != 12) &  (Res_line.reslinnr == reslinnr)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                assign_it()
    else:

        res_line_obj_list = []
        for res_line, guest, zimkateg in db_session.query(Res_line, Guest, Zimkateg).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                (Res_line.gastnr == gastnr) &  ((Res_line.active_flag == 1) |  (Res_line.active_flag == 0)) &  (Res_line.resstatus != 12)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            assign_it()

    return generate_output()