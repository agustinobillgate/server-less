from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from sqlalchemy import func
from models import Zimkateg, Guest, Reservation, Res_line

def check_outbl(sorttype:int, input_resnr:int, lzinr:str, lname:str, gname:str):
    ci_date = None
    check_out_list_list = []
    zimkateg = guest = reservation = res_line = None

    check_out_list = None

    check_out_list_list, Check_out_list = create_model("Check_out_list", {"zinr":str, "reser_name":str, "resli_name":str, "g_name":str, "ankunft":date, "abreise":date, "kurzbez":str, "erwachs":int, "gratis":int, "resstatus":int, "arrangement":str, "zipreis":decimal, "groupname":str, "resnr":int, "gastnr":int, "bemerk":str, "gastnrmember":int, "reslinnr":int, "zimmeranz":int, "res_address":str, "res_city":str, "res_bemerk":str, "recid_resline":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, check_out_list_list, zimkateg, guest, reservation, res_line


        nonlocal check_out_list
        nonlocal check_out_list_list
        return {"ci_date": ci_date, "check-out-list": check_out_list_list}

    def disp_arlist():

        nonlocal ci_date, check_out_list_list, zimkateg, guest, reservation, res_line


        nonlocal check_out_list
        nonlocal check_out_list_list

        if sorttype == 1:

            if input_resnr == 0:

                res_line_obj_list = []
                for res_line, zimkateg, guest, reservation in db_session.query(Res_line, Zimkateg, Guest, Reservation).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                        ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (func.lower(Res_line.zinr) >= (lzinr).lower()) &  (Res_line.abreise == ci_date)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()

            else:

                res_line_obj_list = []
                for res_line, zimkateg, guest, reservation in db_session.query(Res_line, Zimkateg, Guest, Reservation).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                        ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (func.lower(Res_line.zinr) >= (lzinr).lower()) &  (Res_line.resnr == input_resnr)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


        elif sorttype == 2:

            if input_resnr == 0:

                res_line_obj_list = []
                for res_line, zimkateg, guest, reservation in db_session.query(Res_line, Zimkateg, Guest, Reservation).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember) &  (func.lower(Guest.name) >= (lname).lower())).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                        ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (func.lower(Res_line.zinr) >= (lzinr).lower()) &  (Res_line.abreise == ci_date)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()

            else:

                res_line_obj_list = []
                for res_line, zimkateg, guest, reservation in db_session.query(Res_line, Zimkateg, Guest, Reservation).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember) &  (func.lower(Guest.name) >= (lname).lower())).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                        ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (func.lower(Res_line.zinr) >= (lzinr).lower()) &  (Res_line.resnr == input_resnr)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


        elif sorttype == 3:

            if input_resnr == 0:

                res_line_obj_list = []
                for res_line, zimkateg, guest, reservation in db_session.query(Res_line, Zimkateg, Guest, Reservation).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (func.lower(Guest.name) >= (gname).lower())).join(Reservation,(Reservation.resnr == Res_line.resnr) &  (Reservation.grpflag)).filter(
                        ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.abreise == ci_date)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()

            else:

                res_line_obj_list = []
                for res_line, zimkateg, guest, reservation in db_session.query(Res_line, Zimkateg, Guest, Reservation).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (func.lower(Guest.name) >= (gname).lower())).join(Reservation,(Reservation.resnr == Res_line.resnr) &  (Reservation.grpflag)).filter(
                        ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.resnr == input_resnr)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


    def assign_it():

        nonlocal ci_date, check_out_list_list, zimkateg, guest, reservation, res_line


        nonlocal check_out_list
        nonlocal check_out_list_list


        check_out_list = Check_out_list()
        check_out_list_list.append(check_out_list)

        check_out_list.zinr = res_line.zinr
        check_out_list.reser_name = reservation.name
        check_out_list.resli_name = res_line.name
        check_out_list.g_name = guest.name
        check_out_list.ankunft = res_line.ankunft
        check_out_list.abreise = res_line.abreise
        check_out_list.kurzbez = zimkateg.kurzbez
        check_out_list.erwachs = res_line.erwachs
        check_out_list.gratis = res_line.gratis
        check_out_list.resstatus = res_line.resstatus
        check_out_list.arrangement = res_line.arrangement
        check_out_list.zipreis = res_line.zipreis
        check_out_list.groupname = reservation.groupname
        check_out_list.resnr = res_line.resnr
        check_out_list.gastnr = res_line.gastnr
        check_out_list.bemerk = res_line.bemerk
        check_out_list.gastnrmember = res_line.gastnrmember
        check_out_list.reslinnr = res_line.reslinnr
        check_out_list.zimmeranz = res_line.zimmeranz
        check_out_list.res_address = guest.adresse1
        check_out_list.res_city = guest.wohnort + " " + guest.plz
        check_out_list.res_bemerk = reservation.bemerk
        check_out_list.recid_resline = res_line._recid


    ci_date = get_output(htpdate(87))
    disp_arlist()

    return generate_output()