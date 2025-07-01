#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Zimkateg, Res_line

def approve_list_disp_rsvbl(resnr:int, reslinnr:int, gastnr:int):

    prepare_cache ([Guest, Zimkateg, Res_line])

    b3_list_list = []
    guest = zimkateg = res_line = None

    b3_list = None

    b3_list_list, B3_list = create_model("B3_list", {"resnr":int, "ankunft":date, "abreise":date, "name":string, "vorname1":string, "zimmeranz":int, "kurzbez":string, "zinr":string, "resstatus":int, "erwachs":int, "kind1":int, "kind2":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal b3_list_list, guest, zimkateg, res_line
        nonlocal resnr, reslinnr, gastnr


        nonlocal b3_list
        nonlocal b3_list_list

        return {"b3-list": b3_list_list}

    def assign_it():

        nonlocal b3_list_list, guest, zimkateg, res_line
        nonlocal resnr, reslinnr, gastnr


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

            res_line_obj_list = {}
            res_line = Res_line()
            guest = Guest()
            zimkateg = Zimkateg()
            for res_line.resnr, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zinr, res_line.resstatus, res_line.erwachs, res_line.kind1, res_line.kind2, res_line._recid, guest.name, guest.vorname1, guest._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zinr, Res_line.resstatus, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line._recid, Guest.name, Guest.vorname1, Guest._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     (Res_line.resnr == resnr) & ((Res_line.active_flag == 1) | (Res_line.active_flag == 0)) & (Res_line.resstatus != 12)).order_by(Res_line.ankunft).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                assign_it()
        else:

            res_line_obj_list = {}
            res_line = Res_line()
            guest = Guest()
            zimkateg = Zimkateg()
            for res_line.resnr, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zinr, res_line.resstatus, res_line.erwachs, res_line.kind1, res_line.kind2, res_line._recid, guest.name, guest.vorname1, guest._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zinr, Res_line.resstatus, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line._recid, Guest.name, Guest.vorname1, Guest._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     (Res_line.resnr == resnr) & ((Res_line.active_flag == 1) | (Res_line.active_flag == 0)) & (Res_line.resstatus != 12) & (Res_line.reslinnr == reslinnr)).order_by(Res_line.ankunft).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                assign_it()
    else:

        res_line_obj_list = {}
        res_line = Res_line()
        guest = Guest()
        zimkateg = Zimkateg()
        for res_line.resnr, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zinr, res_line.resstatus, res_line.erwachs, res_line.kind1, res_line.kind2, res_line._recid, guest.name, guest.vorname1, guest._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zinr, Res_line.resstatus, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line._recid, Guest.name, Guest.vorname1, Guest._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                 (Res_line.gastnr == gastnr) & ((Res_line.active_flag == 1) | (Res_line.active_flag == 0)) & (Res_line.resstatus != 12)).order_by(Res_line.ankunft).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            assign_it()

    return generate_output()