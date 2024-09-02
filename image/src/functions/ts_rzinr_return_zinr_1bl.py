from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Res_line, Bill, Queasy, Guest

def ts_rzinr_return_zinr_1bl(pvilanguage:int, case_type:int, room:str, dept:int, dept_mbar:int, dept_ldry:int):
    zinr = ""
    lastzinr = ""
    comments = ""
    resline = False
    q1_list_list = []
    lvcarea:str = "TS_rzinr"
    res_line = bill = queasy = guest = None

    q1_list = rline = bbuff = None

    q1_list_list, Q1_list = create_model("Q1_list", {"resnr":int, "zinr":str, "code":str, "resstatus":int, "erwachs":int, "kind1":int, "gratis":int, "bemerk":str, "billnr":int, "g_name":str, "vorname1":str, "anrede1":str, "anredefirma":str, "bill_name":str, "ankunft":date, "abreise":date, "nation1":str, "parent_nr":int, "reslinnr":int, "resname":str, "name_bg_col":int, "name_fg_col":int, "bill_bg_col":int, "bill_fg_col":int}, {"name_bg_col": 15, "bill_bg_col": 15})

    Rline = Res_line
    Bbuff = Bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal zinr, lastzinr, comments, resline, q1_list_list, lvcarea, res_line, bill, queasy, guest
        nonlocal rline, bbuff


        nonlocal q1_list, rline, bbuff
        nonlocal q1_list_list
        return {"zinr": zinr, "lastzinr": lastzinr, "comments": comments, "resline": resline, "q1-list": q1_list_list}

    if case_type == 1:

        rline = db_session.query(Rline).filter(
                (Rline.active_flag == 1) &  (func.lower(Rline.pin_code) == (room).lower()) &  (Rline.resstatus != 12)).first()

        if not rline:

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 16) &  (func.lower(Queasy.char1) == (room).lower())).first()

            if queasy:

                rline = db_session.query(Rline).filter(
                        (Rline.active_flag == 1) &  (Rline.resnr == queasy.number1) &  (Rline.reslinnr == queasy.number2)).first()

        if rline:
            resline = True
            zinr = rline.zinr
            lastzinr = zinr
            comments = translateExtended ("A/Ch/CO:", lvcarea, "") + " " +\
                    to_string(rline.erwachs) + "/" +\
                    to_string(rline.kind1) + "/" +\
                    to_string(rline.gratis) + chr(10) +\
                    rline.bemerk

            res_line_obj_list = []
            for res_line, guest, bbuff in db_session.query(Res_line, Guest, Bbuff).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).join(Bbuff,(Bbuff.resnr == Res_line.resnr) &  (Bbuff.parent_nr == rline.reslinnr)).filter(
                    (Res_line.zinr == zinr) &  (Res_line.active_flag == 1) &  (Res_line.resnr == rline.resnr)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                q1_list = Q1_list()
                q1_list_list.append(q1_list)

                q1_list.resnr = res_line.resnr
                q1_list.zinr = res_line.zinr
                q1_list.code = res_line.code
                q1_list.resstatus = res_line.resstatus
                q1_list.erwachs = res_line.erwachs
                q1_list.kind1 = res_line.kind1
                q1_list.gratis = res_line.gratis
                q1_list.bemerk = res_line.bemerk
                q1_list.billnr = bbuff.billnr
                q1_list.g_name = guest.name
                q1_list.vorname1 = guest.vorname1
                q1_list.anrede1 = guest.anrede1
                q1_list.anredefirma = guest.anredefirma
                q1_list.bill_name = bbuff.name
                q1_list.ankunft = res_line.ankunft
                q1_list.abreise = res_line.abreise
                q1_list.nation1 = guest.nation1
                q1_list.parent_nr = bbuff.parent_nr
                q1_list.reslinnr = res_line.reslinnr
                q1_list.resname = res_line.name

                if (dept != dept_mbar and dept != dept_ldry):

                    if res_line.code != "":

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 9) &  (Queasy.number1 == to_int(res_line.code))).first()

                        if queasy and queasy.logi1:
                            q1_list.name_bg_col = 12
                            q1_list.name_fg_col = 15

                if res_line.resstatus == 12:
                    q1_list.bill_bg_col = 2
                    q1_list.bill_fg_col = 15

    elif case_type == 2:
        zinr = room
        lastzinr = zinr

        res_line_obj_list = []
        for res_line, guest, bbuff in db_session.query(Res_line, Guest, Bbuff).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).join(Bbuff,(Bbuff.resnr == Res_line.resnr) &  (Bbuff.parent_nr == Res_line.reslinnr)).filter(
                (func.lower(Res_line.zinr) == (room).lower()) &  (Res_line.active_flag == 1)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            resline = True
            q1_list = Q1_list()
            q1_list_list.append(q1_list)

            q1_list.resnr = res_line.resnr
            q1_list.zinr = res_line.zinr
            q1_list.code = res_line.code
            q1_list.resstatus = res_line.resstatus
            q1_list.erwachs = res_line.erwachs
            q1_list.kind1 = res_line.kind1
            q1_list.gratis = res_line.gratis
            q1_list.bemerk = res_line.bemerk
            q1_list.billnr = bbuff.billnr
            q1_list.g_name = guest.name
            q1_list.vorname1 = guest.vorname1
            q1_list.anrede1 = guest.anrede1
            q1_list.anredefirma = guest.anredefirma
            q1_list.bill_name = bbuff.name
            q1_list.ankunft = res_line.ankunft
            q1_list.abreise = res_line.abreise
            q1_list.nation1 = guest.nation1
            q1_list.parent_nr = bbuff.parent_nr
            q1_list.reslinnr = res_line.reslinnr
            q1_list.resname = res_line.name

            if (dept != dept_mbar and dept != dept_ldry):

                if res_line.code != "":

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 9) &  (Queasy.number1 == to_int(res_line.code))).first()

                    if queasy and queasy.logi1:
                        q1_list.name_bg_col = 12
                        q1_list.name_fg_col = 15

            if res_line.resstatus == 12:
                q1_list.bill_bg_col = 2
                q1_list.bill_fg_col = 15


            comments = translateExtended ("A/Ch/CO:", lvcarea, "") + " " + to_string(res_line.erwachs) + "/" + to_string(res_line.kind1) + "/" + to_string(res_line.gratis) + chr(10) + res_line.bemerk

    return generate_output()