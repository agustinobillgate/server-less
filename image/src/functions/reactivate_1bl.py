from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
import re
from models import Reservation, Zimkateg, Res_line, Guest

def reactivate_1bl(fresnr:int, fdate:date, fname:str, comments:str):
    resname = ""
    address = ""
    city = ""
    stat_avail = False
    t_reactivate_list = []
    tname:str = ""
    loopi:int = 0
    str:str = ""
    reservation = zimkateg = res_line = guest = None

    t_reactivate = None

    t_reactivate_list, T_reactivate = create_model("T_reactivate", {"resnr":int, "reslinnr":int, "gastnr":int, "rsvname":str, "rsname":str, "ankunft":date, "abreise":date, "resstatus":int, "zimmeranz":int, "kurzbez":str, "erwachs":int, "gratis":int, "arrangement":str, "zipreis":decimal, "zinr":str, "cancelled":date, "cancelled_id":str, "bemerk":str, "bemerk1":str, "rsv_gastnr":int, "anztage":int, "active_flag":int, "activeflag":int, "betrieb_gastpay":int, "kind1":int, "kind2":int, "changed":date, "changed_id":str, "address":str, "city":str, "deposit":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal resname, address, city, stat_avail, t_reactivate_list, tname, loopi, str, reservation, zimkateg, res_line, guest


        nonlocal t_reactivate
        nonlocal t_reactivate_list
        return {"resname": resname, "address": address, "city": city, "stat_avail": stat_avail, "t-reactivate": t_reactivate_list}

    def create_t_reactive():

        nonlocal resname, address, city, stat_avail, t_reactivate_list, tname, loopi, str, reservation, zimkateg, res_line, guest


        nonlocal t_reactivate
        nonlocal t_reactivate_list

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == res_line.gastnr)).first()
        t_reactivate = T_reactivate()
        t_reactivate_list.append(t_reactivate)

        t_reactivate.resnr = res_line.resnr
        t_reactivate.reslinnr = res_line.reslinnr
        t_reactivate.rsvname = reservation.name
        t_reactivate.rsname = res_line.name
        t_reactivate.ankunft = res_line.ankunft
        t_reactivate.abreise = res_line.abreise
        t_reactivate.resstatus = res_line.resstatus
        t_reactivate.zimmeranz = res_line.zimmeranz
        t_reactivate.kurzbez = zimkateg.kurzbez
        t_reactivate.erwachs = res_line.erwachs
        t_reactivate.gratis = res_line.gratis
        t_reactivate.arrangement = res_line.arrangement
        t_reactivate.zipreis = res_line.zipreis
        t_reactivate.zinr = res_line.zinr
        t_reactivate.cancelled = res_line.cancelled
        t_reactivate.cancelled_id = res_line.cancelled_id
        t_reactivate.bemerk = res_line.bemerk
        t_reactivate.bemerk1 = reservation.bemerk
        t_reactivate.rsv_gastnr = reservation.gastnr
        t_reactivate.anztage = res_line.anztage
        t_reactivate.gastnr = res_line.gastnr
        t_reactivate.active_flag = res_line.active_flag
        t_reactivate.activeflag = reservation.activeflag
        t_reactivate.betrieb_gastpay = res_line.betrieb_gastpay
        t_reactivate.kind1 = res_line.kind1
        t_reactivate.kind2 = res_line.kind2
        t_reactivate.changed = res_line.changed
        t_reactivate.changed_id = res_line.changed_id
        t_reactivate.address = guest.adresse1


        t_reactivate.city = guest.wohnort + " " + guest.plz

        if reservation.depositgef != 0:
            t_reactivate.deposit = True


        else:
            t_reactivate.deposit = False


    stat_avail = False

    if fresnr == 0 and fdate == None:
        tname = chr(ord(substring(fname, 0, 1)) + 1)

        res_line_obj_list = []
        for res_line, reservation, zimkateg in db_session.query(Res_line, Reservation, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                (Res_line.active_flag == 2) &  ((Res_line.resstatus == 9) |  (Res_line.resstatus == 10)) &  (func.lower(Res_line.resname) >= (fname).lower()) &  (func.lower(Res_line.resname) < (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            create_t_reactive()

        res_line_obj_list = []
        for res_line, reservation, zimkateg in db_session.query(Res_line, Reservation, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                (Res_line.active_flag == 0) &  (Res_line.zimmer_wunsch.op("~")(".*cancel.*")) &  (func.lower(Res_line.resname) >= (fname).lower()) &  (func.lower(Res_line.resname) < (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            create_t_reactive()
    else:

        if fresnr == 0:

            res_line_obj_list = []
            for res_line, reservation, zimkateg in db_session.query(Res_line, Reservation, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr) &  (func.lower(Reservation.name) >= (fname).lower())).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                    (Res_line.active_flag == 2) &  (Res_line.l_zuordnung[2] == 0) &  ((Res_line.resstatus == 9) |  (Res_line.resstatus == 10)) &  (Res_line.ankunft == fdate)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                create_t_reactive()

            res_line_obj_list = []
            for res_line, reservation, zimkateg in db_session.query(Res_line, Reservation, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr) &  (func.lower(Reservation.name) >= (fname).lower())).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                    (Res_line.active_flag == 0) &  (Res_line.l_zuordnung[2] == 0) &  (Res_line.zimmer_wunsch.op("~")(".*cancel.*"))).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                    if re.match(".*\$arrival\$.*",str):

                        if date_mdy(to_int(substring(str, 12, 2)) , to_int(substring(str, 9, 2)) , to_int(substring(str, 15, 4))) == fdate:
                            create_t_reactive()
                            break
        else:

            res_line_obj_list = []
            for res_line, reservation, zimkateg in db_session.query(Res_line, Reservation, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr) &  (func.lower(Reservation.name) >= (fname).lower())).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                    (Res_line.active_flag == 2) &  ((Res_line.resstatus == 9) |  (Res_line.resstatus == 10)) &  (Res_line.resnr >= fresnr) &  (Res_line.resnr <= (fresnr + 100)) &  (Res_line.l_zuordnung[2] == 0)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                create_t_reactive()

            res_line_obj_list = []
            for res_line, reservation, zimkateg in db_session.query(Res_line, Reservation, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr) &  (func.lower(Reservation.name) >= (fname).lower())).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                    (Res_line.active_flag == 0) &  (Res_line.zimmer_wunsch.op("~")(".*cancel.*")) &  (Res_line.resnr >= fresnr) &  (Res_line.resnr <= (fresnr + 100)) &  (Res_line.l_zuordnung[2] == 0)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                create_t_reactive()

    t_reactivate = query(t_reactivate_list, first=True)

    if t_reactivate:
        stat_avail = True
        resname = t_reactivate.rsvname

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == t_reactivate.rsv_gastnr)).first()
        address = guest.adresse1
        city = guest.wohnort + " " + guest.plz
        comments = t_reactivate.bemerk1 + chr (10) + t_reactivate.bemerk

    return generate_output()