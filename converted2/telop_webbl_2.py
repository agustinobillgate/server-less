from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Guest, Waehrung, Reservation, Zimkateg, Res_line, Zkstat, Reslin_queasy, Messages

def telop_webbl(sorttype:int, room:str, fdate1:date, fdate2:date, ci_date:date, lname:str, last_sort:int, lnat:str, lresnr:int):
    troom = ""
    tpax = ""
    telop_list_list = []
    rmlen:int = 0
    temp_total:int = 0
    temp_total2:int = 0
    guest = waehrung = reservation = zimkateg = res_line = zkstat = reslin_queasy = messages = None
    gmember = telop_list = None
    telop_list_list, Telop_list = create_model("Telop_list", {"resli_wabkurz":str, "voucher_nr":str, "grpflag":bool, "reser_name":str, "zinr":str, "resli_name":str, "segmentcode":int, "nation1":str, "resstatus":int, "l_zuordnung":int, "ankunft":date, "abreise":date, "ankzeit":int, "abreisezeit":int, "flight_nr":str, "zimmeranz":int, "kurzbez":str, "erwachs":int, "kind1":int, "gratis":int, "waeh_wabkurz":str, "resnr":int, "reslinnr":int, "betrieb_gast":int, "groupname":str, "cancelled_id":str, "changed_id":str, "bemerk":str, "active_flag":int, "gastnrmember":int, "gastnr":int, "betrieb_gastmem":int, "pseudofix":bool, "zikatnr":int, "arrangement":str, "zipreis":decimal, "resname":str, "address":str, "city":str, "b_comments":str, "message_flag":bool, "flag_color":int, "flight1":str, "eta":str, "flight2":str, "etd":str})
    Gmember = create_buffer("Gmember",Guest)
    lname = lname.strip()
    room = room.strip()

    db_session = local_storage.db_session

    def generate_output():
        nonlocal troom, tpax, telop_list_list, rmlen, temp_total, temp_total2, guest, waehrung, reservation, zimkateg, res_line, zkstat, reslin_queasy, messages
        nonlocal sorttype, room, fdate1, fdate2, ci_date, lname, last_sort, lnat, lresnr
        nonlocal gmember

        nonlocal gmember, telop_list
        nonlocal telop_list_list
        return {"troom": troom, "tpax": tpax, "telop-list": telop_list_list}

    def disp_arl1():
        nonlocal troom, tpax, telop_list_list, rmlen, temp_total, temp_total2, guest, waehrung, reservation, zimkateg, res_line, zkstat, reslin_queasy, messages
        nonlocal sorttype, room, fdate1, fdate2, ci_date, lname, last_sort, lnat, lresnr
        nonlocal gmember
        nonlocal gmember, telop_list
        nonlocal telop_list_list

        to_name:str = ""
        rmlen = len(room)
        local_storage.debugging = local_storage.debugging + ",42"
        if fdate1 == None:
            if fdate2 != None:
                fdate1 = fdate2
            else:
                fdate1 = ci_date
                fdate2 = ci_date + timedelta(days=30)

        if fdate2 == None:
            if fdate1 != None:
                fdate2 = fdate1
            else:
                fdate1 = ci_date
                fdate2 = ci_date + timedelta(days=30)

        if lname != "" and substring(lname, 0, 1) != ("*").lower() :
            to_name = chr (ord(substring(lname, 0, 1)) + 1)

        if last_sort == 1:
            local_storage.debugging = local_storage.debugging + ",61"
            if lname == "":
                res_line_obj_list = []
                recs = (
                    db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember)
                    .join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr))
                    .join(Reservation,(Reservation.resnr == Res_line.resnr))
                    .join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr))
                    .join(Gmember,(Gmember.gastnr == Res_line.gastnrmember))
                    .filter(
                        (Res_line.active_flag == 0) &  
                        (Res_line.ankunft >= fdate1) &  
                        (Res_line.ankunft <= fdate2))
                    .order_by((Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name)
                    .all()
                )
                for res_line, waehrung, reservation, zimkateg, gmember in recs:
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)
                    assign_it()


            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = []
                recs = (
                    db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember)
                    .join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr))
                    .join(Reservation,(Reservation.resnr == Res_line.resnr))
                    .join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr))
                    .join(Gmember,(Gmember.gastnr == Res_line.gastnrmember))
                    .filter(
                        (Res_line.active_flag == 0) &  
                        (Res_line.ankunft >= fdate1) &  
                        (Res_line.ankunft <= fdate2) &  
                        (func.lower(Res_line.name) >= lname.lower()) &  
                        (func.lower(Res_line.name) <= (to_name).lower()))
                    .order_by(Res_line.name)
                    .all()
                )
                for res_line, waehrung, reservation, zimkateg, gmember in recs:
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)
                    assign_it()


            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :
                res_line_obj_list = []
                recs = (
                     db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember)
                     .join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr))
                     .join(Reservation,(Reservation.resnr == Res_line.resnr))
                     .join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr))
                     .join(Gmember,(Gmember.gastnr == Res_line.gastnrmember))
                     .filter(
                        (Res_line.active_flag == 0) &  
                        (Res_line.ankunft >= fdate1) &  
                        (Res_line.ankunft <= fdate2) &  
                        (func.lower(Res_line.name).op("~")((lname).lower().replace("*",".*"))))
                    .order_by(Res_line.name)
                    .all()
                )
                for res_line, waehrung, reservation, zimkateg, gmember in recs:
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)
                    assign_it()

        elif last_sort == 2:
            if lname == "":

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.active_flag == 0) &  (Res_line.ankunft >= fdate1) &  (Res_line.ankunft <= fdate2)).order_by(Reservation.name, Res_line.ankunft, Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) &  (func.lower(Reservation.name) >= lname.lower()) &  (func.lower(Reservation.name) <= (to_name).lower())).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.active_flag == 0) &  (Res_line.ankunft >= fdate1) &  (Res_line.ankunft <= fdate2)).order_by(Reservation.name, Res_line.ankunft, Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.active_flag == 0) &  (Res_line.ankunft >= fdate1) &  (Res_line.ankunft <= fdate2) &  (func.lower(Res_line.resname).op("~")(((lname)).lower().replace("*",".*")))).order_by(Res_line.resname, Res_line.ankunft, Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()

        elif last_sort == 3 and lnat == "":

            if lname == "":

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.active_flag == 0) &  (Res_line.ankunft == fdate2)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.active_flag == 0) &  (Res_line.ankunft == fdate2) &  (func.lower(Res_line.name) >= lname.lower()) &  (func.lower(Res_line.name) <= (to_name).lower())).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.active_flag == 0) &  (Res_line.ankunft == fdate2) &  (func.lower(Res_line.name).op("~")(((lname)).lower().replace("*",".*")))).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()

        elif last_sort == 3 and lnat != "":

            if lname == "":

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) &  (func.lower(Gmember.nation1) == (lnat).lower())).filter(
                        (Res_line.active_flag == 0) &  (Res_line.ankunft == fdate2)).order_by((Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) &  (func.lower(Gmember.nation1) == (lnat).lower())).filter(
                        (Res_line.active_flag == 0) &  (Res_line.ankunft == fdate2) &  (func.lower(Res_line.name) >= lname.lower()) &  (func.lower(Res_line.name) <= (to_name).lower())).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) &  (func.lower(Gmember.nation1) == (lnat).lower())).filter(
                        (Res_line.active_flag == 0) &  (Res_line.ankunft == fdate2) &  (func.lower(Res_line.name).op("~")(((lname)).lower().replace("*",".*")))).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()

        elif last_sort == 4:

            if lresnr == 0:

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.active_flag == 0) &  (Res_line.ankunft == ci_date)).order_by(Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()

            else:

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.active_flag == 0) &  (Res_line.resnr == lresnr)).order_by((Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()

    def disp_arl2():
        nonlocal troom, tpax, telop_list_list, rmlen, temp_total, temp_total2, guest, waehrung, reservation, zimkateg, res_line, zkstat, reslin_queasy, messages
        nonlocal sorttype, room, fdate1, fdate2, ci_date, lname, last_sort, lnat, lresnr
        nonlocal gmember

        nonlocal gmember, telop_list
        nonlocal telop_list_list

        to_name:str = ""
        rmlen = len(room)

        if lname != "" and substring(lname, 0, 1) != ("*").lower() :
            to_name = chr (ord(substring(lname, 0, 1)) + 1)

        lname = lname.strip()
        room = room.strip()
        local_storage.debugging = local_storage.debugging + ",309"
        if last_sort == 1:
            if room != "":
                if lname == "":
                    res_line_obj_list = []
                    
                    recs = (
                        db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember)
                            .join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr))
                            .join(Reservation,(Reservation.resnr == Res_line.resnr))
                            .join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr))
                            .join(Gmember,(Gmember.gastnr == Res_line.gastnrmember))
                        .filter(
                            (Res_line.active_flag == 1) &  
                            (Res_line.resstatus != 12) &  
                            ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  
                            (Res_line.ankunft <= ci_date) &  
                            (Res_line.abreise >= ci_date))
                        .order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name)
                        .all()
                    )
                    for res_line, waehrung, reservation, zimkateg, gmember in recs:
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)
                        assign_it()


                elif lname != "" and substring(lname, 0, 1) == ("*").lower() :
                    local_storage.debugging = ",309"
                    res_line_obj_list = []
                    recs = (
                        db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember)
                            .join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr))
                            .join(Reservation,(Reservation.resnr == Res_line.resnr))
                            .join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr))
                            .join(Gmember,(Gmember.gastnr == Res_line.gastnrmember))
                        .filter(
                            (Res_line.active_flag == 1) &  
                            (Res_line.resstatus != 12) &  
                            ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  
                            (func.lower(Res_line.name).op("~")(((lname)).lower().replace("*",".*"))) &  
                            (Res_line.ankunft <= ci_date) &  
                            (Res_line.abreise >= ci_date)
                        )
                        .order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name)
                        .all()
                    )
                    for res_line, waehrung, reservation, zimkateg, gmember in recs:
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()


                elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                    res_line_obj_list = []
                    for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                            (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Res_line.name) >= lname.lower()) &  (func.lower(Res_line.name) <= (to_name).lower()) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)
                        assign_it()

            elif room == "":
                if lname == "":
                    res_line_obj_list = []
                    for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                            (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)).order_by((Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)

                        assign_it()


                elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                    res_line_obj_list = []
                    for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                            (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (func.lower(Res_line.name).op("~")(((lname)).lower().replace("*",".*"))) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)).order_by(Res_line.name).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()


                elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                    res_line_obj_list = []
                    for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                            (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (func.lower(Res_line.name) >= lname.lower()) &  (func.lower(Res_line.name) <= (to_name).lower()) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)).order_by(Res_line.name).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

        elif last_sort == 2:

            if lname == "" and room == "":

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)).order_by(Res_line.resname, Res_line.resnr, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


            elif lname == "" and room != "":

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)).order_by(Res_line.zinr, Res_line.resname, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Res_line.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)).order_by(Res_line.resname, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Res_line.resname) >= lname.lower()) &  (func.lower(Res_line.resname) <= (to_name).lower()) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)).order_by(Res_line.resname, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


        elif last_sort == 3 and lnat == "":

            if lname == "":

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (func.lower(Res_line.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (func.lower(Res_line.resname) >= lname.lower()) &  (func.lower(Res_line.resname) <= (to_name).lower()) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


        elif last_sort == 3 and lnat != "":

            if lname == "":

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) &  (func.lower(Gmember.nation1) == (lnat).lower())).filter(
                        (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) &  (func.lower(Gmember.nation1) == (lnat).lower())).filter(
                        (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (func.lower(Res_line.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) &  (func.lower(Gmember.nation1) == (lnat).lower())).filter(
                        (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (func.lower(Res_line.resname) >= lname.lower()) &  (func.lower(Res_line.resname) <= (to_name).lower()) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


        elif last_sort == 4:

            if lresnr == 0:

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.active_flag == 1) &  (Res_line.resstatus != 12)).order_by(Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()

            else:

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.resnr == lresnr)).order_by(Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()

    def disp_arl4():

        nonlocal troom, tpax, telop_list_list, rmlen, temp_total, temp_total2, guest, waehrung, reservation, zimkateg, res_line, zkstat, reslin_queasy, messages
        nonlocal sorttype, room, fdate1, fdate2, ci_date, lname, last_sort, lnat, lresnr
        nonlocal gmember


        nonlocal gmember, telop_list
        nonlocal telop_list_list

        to_name:str = ""
        rmlen = len(room)
        lname = lname.strip()
        room = room.strip()
        local_storage.debugging = local_storage.debugging + ",610"
        if lname != "" and substring(lname, 0, 1) != ("*").lower() :
            to_name = chr (ord(substring(lname, 0, 1)) + 1)

        if last_sort == 1:

            if room != "":

                if lname == "" and room == "":

                    res_line_obj_list = []
                    for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                            (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Res_line.abreise == ci_date)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()


                elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                    res_line_obj_list = []
                    for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                            (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Res_line.name).op("~")(((lname)).lower().replace("*",".*"))) &  (Res_line.abreise == ci_date)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()


                elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                    res_line_obj_list = []
                    for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                            (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Res_line.name) >= lname.lower()) &  (func.lower(Res_line.name) <= (to_name).lower()) &  (Res_line.abreise == ci_date)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()


            elif room == "":

                if lname == "":

                    res_line_obj_list = []
                    for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                            (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.abreise == ci_date)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()


                elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                    res_line_obj_list = []
                    for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                            (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (func.lower(Res_line.name).op("~")(((lname)).lower().replace("*",".*"))) &  (Res_line.abreise == ci_date)).order_by(Res_line.name, Res_line.zinr).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()


                elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                    res_line_obj_list = []
                    for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                            (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (func.lower(Res_line.name) >= lname.lower()) &  (func.lower(Res_line.name) <= (to_name).lower()) &  (Res_line.abreise == ci_date)).order_by(Res_line.name, Res_line.zinr).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()


        elif last_sort == 2:

            if lname == "":

                if room == "":

                    res_line_obj_list = []
                    for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                            (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Res_line.abreise == ci_date)).order_by(Res_line.resname, Res_line.resnr, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()


                elif room != "":

                    res_line_obj_list = []
                    for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                            (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Res_line.abreise == ci_date)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()


            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Res_line.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Res_line.abreise == ci_date)).order_by(Res_line.resname, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Res_line.resname) >= lname.lower()) &  (func.lower(Res_line.resname) <= (to_name).lower()) &  (Res_line.abreise == ci_date)).order_by(Res_line.resname, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


        elif last_sort == 3 and lnat == "":

            if lname == "":

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.abreise == ci_date)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) &  (func.lower(Gmember.nation1) == (lnat).lower())).filter(
                        (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (func.lower(Res_line.name).op("~")(((lname)).lower().replace("*",".*"))) &  (Res_line.abreise == ci_date)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (func.lower(Res_line.name) >= lname.lower()) &  (func.lower(Res_line.name) <= (to_name).lower()) &  (Res_line.abreise == ci_date)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


        elif last_sort == 3 and lnat != "":

            if lname == "":

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) &  (func.lower(Gmember.nation1) == (lnat).lower())).filter(
                        (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.abreise == ci_date)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) &  (func.lower(Gmember.nation1) == (lnat).lower())).filter(
                        (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (func.lower(Res_line.name).op("~")(((lname)).lower().replace("*",".*"))) &  (Res_line.abreise == ci_date)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) &  (func.lower(Gmember.nation1) == (lnat).lower())).filter(
                        (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (func.lower(Res_line.name) >= lname.lower()) &  (func.lower(Res_line.name) <= (to_name).lower()) &  (Res_line.abreise == ci_date)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


        elif last_sort == 4:

            if lresnr == 0:

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.abreise == ci_date)).order_by(Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()

            else:

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.resnr == lresnr) &  (Res_line.abreise == ci_date)).order_by(Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()

    def disp_arl5():
        nonlocal troom, tpax, telop_list_list, rmlen, temp_total, temp_total2, guest, waehrung, reservation, zimkateg, res_line, zkstat, reslin_queasy, messages
        nonlocal sorttype, room, fdate1, fdate2, ci_date, lname, last_sort, lnat, lresnr
        nonlocal gmember
        nonlocal gmember, telop_list
        nonlocal telop_list_list

        local_storage.debugging = local_storage.debugging + ",890"
        to_name:str = "zzz"
        rmlen = len(room)

        if lname != "" and substring(lname, 0, 1) != ("*").lower() :
            to_name = chr (ord(substring(lname, 0, 1)) + 1)

        if fdate2 == None:
            fdate2 = ci_date

        if last_sort == 1 and room != "":

            if lname == "":

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.resstatus == 8) &  (Res_line.abreise == fdate2) &  (func.lower(Res_line.zinr) >= (room).lower())).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.resstatus == 8) &  (func.lower(Res_line.name).op("~")(((lname)).lower().replace("*",".*"))) &  (Res_line.abreise == fdate2) &  (func.lower(Res_line.zinr) >= (room).lower())).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.resstatus == 8) &  (func.lower(Res_line.name) >= lname.lower()) &  (func.lower(Res_line.name) <= (to_name).lower()) &  (Res_line.abreise == fdate2) &  (func.lower(Res_line.zinr) >= (room).lower())).order_by(Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)

                    assign_it()

        elif last_sort == 1 and room == "":
            if lname == "":

                res_line_obj_list = []
                recs = (
                    db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember)
                    .join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr))
                    .join(Reservation,(Reservation.resnr == Res_line.resnr))
                    .join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr))
                    .join(Gmember,(Gmember.gastnr == Res_line.gastnrmember))
                    .filter(
                        (Res_line.resstatus == 8) &  
                        (Res_line.abreise == fdate2))
                    .order_by((Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all()
                )
                local_storage.debugging = local_storage.debugging + ",nRec:" + str(len(recs))
                for res_line, waehrung, reservation, zimkateg, gmember in recs:
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)

                    assign_it()


            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = []
                recs = (
                    db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember)
                        .join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr))
                        .join(Reservation,(Reservation.resnr == Res_line.resnr))
                        .join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr))
                        .join(Gmember,(Gmember.gastnr == Res_line.gastnrmember))
                        .filter((Res_line.resstatus == 8) &  
                                (func.lower(Res_line.name).op("~")(((lname)).lower().replace("*",".*"))) &  
                                (Res_line.abreise == fdate2))
                        .order_by(Res_line.name).all()
                )
                for res_line, waehrung, reservation, zimkateg, gmember in recs:
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)
                    assign_it()

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :
                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.resstatus == 8) &  (func.lower(Res_line.name) >= lname.lower()) &  (func.lower(Res_line.name) <= (to_name).lower()) &  (Res_line.abreise == fdate2)).order_by(Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)

                    assign_it()

        elif last_sort == 2 and room != "":
            if lname == "":
                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.resstatus == 8) &  (Res_line.abreise == fdate2) &  (func.lower(Res_line.zinr) >= (room).lower())).order_by(Res_line.zinr, Reservation.name, Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)

                    assign_it()

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :
                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.resstatus == 8) &  (func.lower(Res_line.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Res_line.abreise == fdate2) &  (func.lower(Res_line.zinr) >= (room).lower())).order_by(Res_line.zinr, Res_line.resname, Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)

                    assign_it()

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.resstatus == 8) &  (func.lower(Res_line.resname) >= lname.lower()) &  (func.lower(Res_line.resname) <= (to_name).lower()) &  (Res_line.abreise == fdate2) &  (func.lower(Res_line.zinr) >= (room).lower())).order_by(Res_line.zinr, Res_line.resname, Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)

                    assign_it()

        elif last_sort == 2 and room == "":
            if lname == "":
                res_line_obj_list = []
                recs = (
                    db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember)
                    .join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr))
                    .join(Reservation,(Reservation.resnr == Res_line.resnr))
                    .join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr))
                    .join(Gmember,(Gmember.gastnr == Res_line.gastnrmember))
                    .filter(
                        (Res_line.resstatus == 8) &  
                        (Res_line.abreise == fdate2))
                    .order_by(Reservation.name, Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all()
                )
                for res_line, waehrung, reservation, zimkateg, gmember in recs:
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)
                    assign_it()

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :
                res_line_obj_list = []
                recs = (
                    db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember)
                    .join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr))
                    .join(Reservation,(Reservation.resnr == Res_line.resnr))
                    .join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr))
                    .join(Gmember,(Gmember.gastnr == Res_line.gastnrmember))
                    .filter(
                        (Res_line.resstatus == 8) &  
                        (func.lower(Res_line.resname).op("~")(((lname)).lower().replace("*",".*"))) &  
                        (Res_line.abreise == fdate2))
                        .order_by(Res_line.resname, Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all()
                )
                for res_line, waehrung, reservation, zimkateg, gmember in recs:
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)

                    assign_it()


            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :
                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) &  (func.lower(Reservation.name) >= lname.lower()) &  (func.lower(Reservation.name) <= (to_name).lower())).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.resstatus == 8) &  (Res_line.abreise == fdate2)).order_by(Reservation.name, Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)

                    assign_it()

        elif last_sort == 3 and lnat == "":
            if lname == "":
                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.resstatus == 8) &  (Res_line.abreise == fdate2)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)

                    assign_it()

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :
                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.resstatus == 8) &  (func.lower(Res_line.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Res_line.abreise == fdate2)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)

                    assign_it()


            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :
                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.resstatus == 8) &  (func.lower(Res_line.resname) >= lname.lower()) &  (func.lower(Res_line.resname) <= (to_name).lower()) &  (Res_line.abreise == fdate2)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)

                    assign_it()

        elif last_sort == 3 and lnat != "":
            if lname == "":
                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) &  (func.lower(Gmember.nation1) == (lnat).lower())).filter(
                        (Res_line.resstatus == 8) &  (Res_line.abreise == fdate2)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)

                    assign_it()


            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :
                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) &  (func.lower(Gmember.nation1) == (lnat).lower())).filter(
                        (Res_line.resstatus == 8) &  (func.lower(Res_line.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Res_line.abreise == fdate2)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)

                    assign_it()


            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :
                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) &  (func.lower(Gmember.nation1) == (lnat).lower())).filter(
                        (Res_line.resstatus == 8) &  (func.lower(Res_line.resname) >= lname.lower()) &  (func.lower(Res_line.resname) <= (to_name).lower()) &  (Res_line.abreise == fdate2)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)

                    assign_it()

        elif last_sort == 4:
            if lresnr == 0:
                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.active_flag == 2) &  (Res_line.resstatus == 8)).order_by(Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)

                    assign_it()
            else:
                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        (Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (Res_line.resnr == lresnr)).order_by((Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)

                    assign_it()

    def disp_arl6():

        nonlocal troom, tpax, telop_list_list, rmlen, temp_total, temp_total2, guest, waehrung, reservation, zimkateg, res_line, zkstat, reslin_queasy, messages
        nonlocal sorttype, room, fdate1, fdate2, ci_date, lname, last_sort, lnat, lresnr
        nonlocal gmember

        nonlocal gmember, telop_list
        nonlocal telop_list_list

        lname = lname.strip()
        room = room.strip()
        local_storage.debugging = local_storage.debugging + ",1203"
        to_name:str = ""
        rmlen = len(room)

        if lname != "" and substring(lname, 0, 1) != ("*").lower() :
            to_name = chr (ord(substring(lname, 0, 1)) + 1)

        if last_sort == 1:
            if room != "":
                if lname == "":
                    res_line_obj_list = []
                    for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                            ((Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)) |  ((Res_line.active_flag == 0) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Res_line.ankunft == ci_date)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Res_line.abreise == ci_date))).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)

                        assign_it()


                elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                    res_line_obj_list = []
                    for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                            ((Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Res_line.name).op("~")(((lname)).lower().replace("*",".*"))) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)) |  ((Res_line.active_flag == 0) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Res_line.name).op("~")(((lname)).lower().replace("*",".*"))) &  (Res_line.ankunft == ci_date)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Res_line.name).op("~")(((lname)).lower().replace("*",".*"))) &  (Res_line.abreise == ci_date))).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)

                        assign_it()

                elif lname != "" and substring(lname, 0, 1) != ("*").lower() :
                    res_line_obj_list = []
                    for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                            ((Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Res_line.name) >= lname.lower()) &  (func.lower(Res_line.name) <= (to_name).lower()) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)) |  ((Res_line.active_flag == 0) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Res_line.name) >= lname.lower()) &  (func.lower(Res_line.name) <= (to_name).lower()) &  (Res_line.ankunft == ci_date)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Res_line.name) >= lname.lower()) &  (func.lower(Res_line.name) <= (to_name).lower()) &  (Res_line.abreise == ci_date))).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)

                        assign_it()

            elif room == "":
                if lname == "":
                    local_storage.debugging = local_storage.debugging + ",1229"
                    res_line_obj_list = []
                    recs = (
                        db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember)
                        .join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr))
                        .join(Reservation,(Reservation.resnr == Res_line.resnr))
                        .join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr))
                        .join(Gmember,(Gmember.gastnr == Res_line.gastnrmember))
                        .filter(
                            (Res_line.active_flag == 1) &  
                            (Res_line.resstatus != 12) &  
                            (Res_line.ankunft <= ci_date) &  
                            ((Res_line.abreise >= ci_date) |  (Res_line.active_flag == 0)) &  
                            ((Res_line.ankunft == ci_date) |  (Res_line.active_flag == 2)) &  
                            (Res_line.resstatus == 8) &  
                            (Res_line.abreise == ci_date)
                             )
                            .order_by((Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name)
                            .all()
                        )
                    local_storage.debugging = local_storage.debugging + ",nRec:" + str(len(recs))
                    for res_line, waehrung, reservation, zimkateg, gmember in recs:
                        if res_line._recid in res_line_obj_list:                    
                                continue
                        else:
                            res_line_obj_list.append(res_line._recid)

                        assign_it()

                elif lname != "" and substring(lname, 0, 1) == ("*").lower() :
                    res_line_obj_list = []
                    recs = (
                        db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember)
                        .join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr))
                        .join(Reservation,(Reservation.resnr == Res_line.resnr))
                        .join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr))
                        .join(Gmember,(Gmember.gastnr == Res_line.gastnrmember))
                        .filter(
                            (   (Res_line.active_flag == 1) &  
                                (Res_line.resstatus != 12) &  
                                (func.lower(Res_line.name).op("~")(lname.lower().replace("*",".*"))) &  
                                (Res_line.ankunft <= ci_date) &  
                                (Res_line.abreise >= ci_date)) |  
                            (   (Res_line.active_flag == 0) & 
                                (func.lower(Res_line.name).op("~")(lname.lower().replace("*",".*"))) &  
                                (Res_line.ankunft == ci_date)) |  
                            (   (Res_line.active_flag == 2) &  
                                (Res_line.resstatus == 8) &  
                                (func.lower(Res_line.name).op("~")(lname.lower().replace("*",".*"))) &  
                                (Res_line.abreise == ci_date)
                                )
                            )
                            .order_by(Res_line.name).all()
                    )
                    for res_line, waehrung, reservation, zimkateg, gmember in recs:
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)

                        assign_it()

                elif lname != "" and substring(lname, 0, 1) != ("*").lower() :
                    res_line_obj_list = []
                    for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                            ((Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (func.lower(Res_line.name) >= lname.lower()) &  (func.lower(Res_line.name) <= (to_name).lower()) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)) |  ((Res_line.active_flag == 0) &  (func.lower(Res_line.name) >= lname.lower()) &  (func.lower(Res_line.name) <= (to_name).lower()) &  (Res_line.ankunft == ci_date)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (func.lower(Res_line.name) >= lname.lower()) &  (func.lower(Res_line.name) <= (to_name).lower()) &  (Res_line.abreise == ci_date))).order_by(Res_line.name).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)
                        assign_it()

        elif last_sort == 2:
            if lname == "" and room == "":
                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        ((Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)) |  ((Res_line.active_flag == 0) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Res_line.ankunft == ci_date)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Res_line.abreise == ci_date))).order_by(Res_line.resname, Res_line.resnr, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()

            elif lname == "" and room != "":
                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        ((Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)) |  ((Res_line.active_flag == 0) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Res_line.ankunft == ci_date)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Res_line.abreise == ci_date))).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :
                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        ((Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Res_line.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)) |  ((Res_line.active_flag == 0) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Res_line.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Res_line.ankunft == ci_date)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Res_line.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Res_line.abreise == ci_date))).order_by(Res_line.resname, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :
                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        ((Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Res_line.resname) >= lname.lower()) &  (func.lower(Res_line.resname) <= (to_name).lower()) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)) |  ((Res_line.active_flag == 0) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Res_line.resname) >= lname.lower()) &  (func.lower(Res_line.resname) <= (to_name).lower()) &  (Res_line.ankunft == ci_date)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Res_line.resname) >= lname.lower()) &  (func.lower(Res_line.resname) <= (to_name).lower()) &  (Res_line.abreise == ci_date))).order_by(Res_line.resname, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()

        elif last_sort == 3 and lnat == "":
            if lname == "":
                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        ((Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)) |  ((Res_line.active_flag == 0) &  (Res_line.ankunft == ci_date)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (Res_line.abreise == ci_date))).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        ((Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (func.lower(Res_line.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)) |  ((Res_line.active_flag == 0) &  (func.lower(Res_line.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Res_line.ankunft == ci_date)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (func.lower(Res_line.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Res_line.abreise == ci_date))).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        ((Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (func.lower(Res_line.resname) >= lname.lower()) &  (func.lower(Res_line.resname) <= (to_name).lower()) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)) |  ((Res_line.active_flag == 0) &  (func.lower(Res_line.resname) >= lname.lower()) &  (func.lower(Res_line.resname) <= (to_name).lower()) &  (Res_line.ankunft == ci_date)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (func.lower(Res_line.resname) >= lname.lower()) &  (func.lower(Res_line.resname) <= (to_name).lower()) &  (Res_line.abreise == ci_date))).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()

        elif last_sort == 3 and lnat != "":
            if lname == "":

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) &  (func.lower(Gmember.nation1) == (lnat).lower())).filter(
                        ((Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)) |  ((Res_line.active_flag == 0) &  (Res_line.ankunft == ci_date)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (Res_line.abreise == ci_date))).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) &  (func.lower(Gmember.nation1) == (lnat).lower())).filter(
                        ((Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (func.lower(Res_line.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)) |  ((Res_line.active_flag == 0) &  (func.lower(Res_line.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Res_line.ankunft == ci_date)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (func.lower(Res_line.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Res_line.abreise == ci_date))).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) &  (func.lower(Gmember.nation1) == (lnat).lower())).filter(
                        ((Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (func.lower(Res_line.resname) >= lname.lower()) &  (func.lower(Res_line.resname) <= (to_name).lower()) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)) |  ((Res_line.active_flag == 0) &  (func.lower(Res_line.resname) >= lname.lower()) &  (func.lower(Res_line.resname) <= (to_name).lower()) &  (Res_line.ankunft == ci_date)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (func.lower(Res_line.resname) >= lname.lower()) &  (func.lower(Res_line.resname) <= (to_name).lower()) &  (Res_line.abreise == ci_date))).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()

        elif last_sort == 4:
            if lresnr == 0:
                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        ((Res_line.active_flag == 1) &  (Res_line.resstatus != 12)) |  ((Res_line.active_flag == 0) &  (Res_line.ankunft == ci_date)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (Res_line.abreise == ci_date))).order_by(Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()

            else:

                res_line_obj_list = []
                for res_line, waehrung, reservation, zimkateg, gmember in db_session.query(Res_line, Waehrung, Reservation, Zimkateg, Gmember).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                        ((Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.resnr == lresnr)) |  ((Res_line.active_flag == 0) &  (Res_line.resnr == lresnr) &  (Res_line.ankunft == ci_date)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (Res_line.resnr == lresnr) &  (Res_line.abreise == ci_date))).order_by((Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()

    def count_al1():

        nonlocal troom, tpax, telop_list_list, rmlen, temp_total, temp_total2, guest, waehrung, reservation, zimkateg, res_line, zkstat, reslin_queasy, messages
        nonlocal sorttype, room, fdate1, fdate2, ci_date, lname, last_sort, lnat, lresnr
        nonlocal gmember

        nonlocal gmember, telop_list
        nonlocal telop_list_list

        to_name:str = ""
        rline = None
        whrg = None
        reservation = None
        gmember = None
        zkstat = None
        Rline =  create_buffer("Rline",Res_line)
        Whrg =  create_buffer("Whrg",Waehrung)
        Reserv =  create_buffer("Reserv",Reservation)
        Gme =  create_buffer("Gme",Guest)
        Zk =  create_buffer("Zk",Zkstat)

        if fdate1 == None:

            if fdate2 != None:
                fdate1 = fdate2
            else:
                fdate1 = ci_date
                fdate2 = ci_date + timedelta(days=30)

        if fdate2 == None:

            if fdate1 != None:
                fdate2 = fdate1
            else:
                fdate1 = ci_date
                fdate2 = ci_date + timedelta(days=30)
                fdate2 = ci_date + timedelta(days=3)

        if lname != "" and substring(lname, 0, 1) != ("*").lower() :
            to_name = chr (ord(substring(lname, 0, 1)) + 1)

        if last_sort == 1:
            local_storage.debugging = local_storage.debugging + ",:sorttype 1"
            if lname == "":
                local_storage.debugging = local_storage.debugging + ",Date:" + str(fdate1) + "|" + str(fdate2)
                rline_obj_list = []
                recs = (
                    db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember)
                    .join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr))
                    .join(Reservation,(Reservation.resnr == Rline.resnr))
                    .join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr))
                    .join(Gmember,(Gmember.gastnr == Rline.gastnrmember))
                    .filter(
                        (Rline.active_flag == 1) &
                        (Rline.ankunft >= fdate1) &  
                        (Rline.ankunft <= fdate2)
                        ).order_by((Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name)
                        .all()
                )
                local_storage.debugging = local_storage.debugging + ",nRec:" + str(len(recs))
                # for rline, whrg, reservation, zkstat, gmember in recs:
                #     if rline._recid in rline_obj_list:
                #         continue
                #     else:
                #         rline_obj_list.append(rline._recid)

                #     if (rline.resstatus != 13 and 
                #         rline.resstatus != 11 and 
                #         rline.l_zuordnung[2] != 1):
                #         temp_total2 = temp_total2 + rline.zimmeranz
                #     temp_total = to_int(temp_total) + to_int(rline.erwachs)
                # troom = to_string(temp_total2)
                # tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :
                rline_obj_list = []
                recs = (
                    db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember)
                    .join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr))
                    .join(Reservation,(Reservation.resnr == Rline.resnr))
                    .join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr))
                    .join(Gmember,(Gmember.gastnr == Rline.gastnrmember))
                    .filter(
                        (Rline.active_flag == 0) &  
                        (Rline.ankunft >= fdate1) &  
                        (Rline.ankunft <= fdate2) &  
                        (func.lower(Rline.name) >= (lname).lower()) &  
                        (func.lower(Rline.name) <= (to_name).lower())
                        ).order_by(Rline.name).all()
                )
                for rline, whrg, reservation, zkstat, gmember in recs:
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)

                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :
                rline_obj_list = []
                recs = (
                    db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember)
                    .join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr))
                    .join(Reservation,(Reservation.resnr == Rline.resnr))
                    .join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr))
                    .join(Gmember,(Gmember.gastnr == Rline.gastnrmember))
                    .filter(
                        (Rline.active_flag == 0) &  
                        (Rline.ankunft >= fdate1) &  
                        (Rline.ankunft <= fdate2) &  
                        (func.lower(Rline.name).op("~")((lname).lower().replace("*",".*")))
                        ).order_by(Rline.name)
                        .all()
                )
                for rline, whrg, reservation, zkstat, gmember in recs:
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

        elif last_sort == 2:
            if lname == "":

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.active_flag == 0) &  (Rline.ankunft >= fdate1) &  (Rline.ankunft <= fdate2)).order_by(Rline.resname, Rline.ankunft, Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.active_flag == 0) &  (Rline.ankunft >= fdate1) &  (Rline.ankunft <= fdate2) &  (func.lower(Rline.resname) >= lname.lower()) &  (func.lower(Rline.resname) <= (to_name).lower())).order_by(Rline.resname, Rline.ankunft, Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.active_flag == 0) &  (Rline.ankunft >= fdate1) &  (Rline.ankunft <= fdate2) &  (func.lower(Rline.resname).op("~")(((lname)).lower().replace("*",".*")))).order_by(Rline.resname, Rline.ankunft, Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat == "":

            if lname == "":

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.active_flag == 0) &  (Rline.ankunft == fdate2)).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.active_flag == 0) &  (Rline.ankunft == fdate2) &  (func.lower(Rline.name) >= lname.lower()) &  (func.lower(Rline.name) <= (to_name).lower())).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.active_flag == 0) &  (Rline.ankunft == fdate2) &  (func.lower(Rline.name).op("~")(((lname)).lower().replace("*",".*")))).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat != "":

            if lname == "":

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember) &  (Gmember.nation1 == (lnat).lower())).filter(
                        (Rline.active_flag == 0) &  (Rline.ankunft == fdate2)).order_by((Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember) &  (Gmember.nation1 == (lnat).lower())).filter(
                        (Rline.active_flag == 0) &  (Rline.ankunft == fdate2) &  (func.lower(Rline.name) >= lname.lower()) &  (func.lower(Rline.name) <= (to_name).lower())).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember) &  (Gmember.nation1 == (lnat).lower())).filter(
                        (Rline.active_flag == 0) &  (Rline.ankunft == fdate2) &  (func.lower(Rline.name).op("~")(((lname)).lower().replace("*",".*")))).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 4:

            if lresnr == 0:

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.active_flag == 0) &  (Rline.ankunft == ci_date)).order_by(Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)


            else:

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.active_flag == 0) &  (Rline.resnr == lresnr)).order_by((Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

    def count_all2():

        nonlocal troom, tpax, telop_list_list, rmlen, temp_total, temp_total2, guest, waehrung, reservation, zimkateg, res_line, zkstat, reslin_queasy, messages
        nonlocal sorttype, room, fdate1, fdate2, ci_date, lname, last_sort, lnat, lresnr
        nonlocal gmember


        nonlocal gmember, telop_list
        nonlocal telop_list_list

        to_name:str = ""
        rline = None
        whrg = None
        reservation = None
        gmember = None
        zkstat = None
        Rline =  create_buffer("Rline",Res_line)
        Whrg =  create_buffer("Whrg",Waehrung)
        Reserv =  create_buffer("Reserv",Reservation)
        Gme =  create_buffer("Gme",Guest)
        Zk =  create_buffer("Zk",Zkstat)

        if lname != "" and substring(lname, 0, 1) != ("*").lower() :
            to_name = chr (ord(substring(lname, 0, 1)) + 1)

        if last_sort == 1:
            if room != "":
                if lname == "":

                    rline_obj_list = []
                    recs = (
                        db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember)
                        .join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr))
                        .join(Reservation,(Reservation.resnr == Rline.resnr))
                        .join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr))
                        .join(Gmember,(Gmember.gastnr == Rline.gastnrmember))
                        .filter(
                            (Rline.active_flag == 1) &  
                            (Rline.resstatus != 12) &  
                            ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &
                            (Rline.ankunft <= ci_date) &  
                            (Rline.abreise >= ci_date)
                            ).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all()
                    )
                    for rline, whrg, reservation, zkstat, gmember in recs:
                        if rline._recid in rline_obj_list:
                            continue
                        else:
                            rline_obj_list.append(rline._recid)

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                    rline_obj_list = []
                    for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                            (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Rline.name).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                        if rline._recid in rline_obj_list:
                            continue
                        else:
                            rline_obj_list.append(rline._recid)

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                    rline_obj_list = []
                    for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                            (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Rline.name) >= lname.lower()) &  (func.lower(Rline.name) <= (to_name).lower()) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                        if rline._recid in rline_obj_list:
                            continue
                        else:
                            rline_obj_list.append(rline._recid)

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

            elif room == "":
                if lname == "":
                    rline_obj_list = []
                    for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                            (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)).order_by((Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                        if rline._recid in rline_obj_list:
                            continue
                        else:
                            rline_obj_list.append(rline._recid)

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                    rline_obj_list = []
                    for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                            (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (func.lower(Rline.name).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)).order_by(Rline.name).all():
                        if rline._recid in rline_obj_list:
                            continue
                        else:
                            rline_obj_list.append(rline._recid)

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                    rline_obj_list = []
                    for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                            (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (func.lower(Rline.name) >= lname.lower()) &  (func.lower(Rline.name) <= (to_name).lower()) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)).order_by(Rline.name).all():
                        if rline._recid in rline_obj_list:
                            continue
                        else:
                            rline_obj_list.append(rline._recid)

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

        elif last_sort == 2:

            if lname == "" and room == "":

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)).order_by(Rline.resname, Rline.resnr, Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname == "" and room != "":

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)).order_by(Rline.zinr, Rline.resname, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Rline.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)).order_by(Rline.resname, Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Rline.resname) >= lname.lower()) &  (func.lower(Rline.resname) <= (to_name).lower()) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)).order_by(Rline.resname, Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat == "":

            if lname == "":

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (func.lower(Rline.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (func.lower(Rline.resname) >= lname.lower()) &  (func.lower(Rline.resname) <= (to_name).lower()) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat != "":

            if lname == "":

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember) &  (Gmember.nation1 == (lnat).lower())).filter(
                        (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember) &  (Gmember.nation1 == (lnat).lower())).filter(
                        (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (func.lower(Rline.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember) &  (Gmember.nation1 == (lnat).lower())).filter(
                        (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (func.lower(Rline.resname) >= lname.lower()) &  (func.lower(Rline.resname) <= (to_name).lower()) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 4:

            if lresnr == 0:

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.active_flag == 1) &  (Rline.resstatus != 12)).order_by(Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)


            else:

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (Rline.resnr == lresnr)).order_by(Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

    def count_all4():

        nonlocal troom, tpax, telop_list_list, rmlen, temp_total, temp_total2, guest, waehrung, reservation, zimkateg, res_line, zkstat, reslin_queasy, messages
        nonlocal sorttype, room, fdate1, fdate2, ci_date, lname, last_sort, lnat, lresnr
        nonlocal gmember


        nonlocal gmember, telop_list
        nonlocal telop_list_list

        to_name:str = ""
        rline = None
        whrg = None
        reservation = None
        gmember = None
        zkstat = None
        Rline =  create_buffer("Rline",Res_line)
        Whrg =  create_buffer("Whrg",Waehrung)
        Reserv =  create_buffer("Reserv",Reservation)
        Gme =  create_buffer("Gme",Guest)
        Zk =  create_buffer("Zk",Zkstat)

        if lname != "" and substring(lname, 0, 1) != ("*").lower() :
            to_name = chr (ord(substring(lname, 0, 1)) + 1)

        if last_sort == 1:

            if room != "":

                if lname == "" and room == "":

                    rline_obj_list = []
                    for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                            (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Rline.abreise == ci_date)).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                        if rline._recid in rline_obj_list:
                            continue
                        else:
                            rline_obj_list.append(rline._recid)

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                    rline_obj_list = []
                    for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                            (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Rline.name).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.abreise == ci_date)).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                        if rline._recid in rline_obj_list:
                            continue
                        else:
                            rline_obj_list.append(rline._recid)

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                    rline_obj_list = []
                    for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                            (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Rline.name) >= lname.lower()) &  (func.lower(Rline.name) <= (to_name).lower()) &  (Rline.abreise == ci_date)).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                        if rline._recid in rline_obj_list:
                            continue
                        else:
                            rline_obj_list.append(rline._recid)

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

            elif room == "":

                if lname == "":

                    rline_obj_list = []
                    for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                            (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (Rline.abreise == ci_date)).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                        if rline._recid in rline_obj_list:
                            continue
                        else:
                            rline_obj_list.append(rline._recid)

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                    rline_obj_list = []
                    for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                            (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (func.lower(Rline.name).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.abreise == ci_date)).order_by(Rline.name, Rline.zinr).all():
                        if rline._recid in rline_obj_list:
                            continue
                        else:
                            rline_obj_list.append(rline._recid)

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                    rline_obj_list = []
                    for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                            (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (func.lower(Rline.name) >= lname.lower()) &  (func.lower(Rline.name) <= (to_name).lower()) &  (Rline.abreise == ci_date)).order_by(Rline.name, Rline.zinr).all():
                        if rline._recid in rline_obj_list:
                            continue
                        else:
                            rline_obj_list.append(rline._recid)

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

        elif last_sort == 2:

            if lname == "":

                if room == "":

                    rline_obj_list = []
                    for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                            (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Rline.abreise == ci_date)).order_by(Rline.resname, Rline.resnr, Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                        if rline._recid in rline_obj_list:
                            continue
                        else:
                            rline_obj_list.append(rline._recid)

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

                elif room != "":

                    rline_obj_list = []
                    for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                            (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Rline.abreise == ci_date)).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                        if rline._recid in rline_obj_list:
                            continue
                        else:
                            rline_obj_list.append(rline._recid)

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Rline.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.abreise == ci_date)).order_by(Rline.resname, Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Rline.resname) >= lname.lower()) &  (func.lower(Rline.resname) <= (to_name).lower()) &  (Rline.abreise == ci_date)).order_by(Rline.resname, Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat == "":

            if lname == "":

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (Rline.abreise == ci_date)).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember) &  (Gmember.nation1 == (lnat).lower())).filter(
                        (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (func.lower(Rline.name).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.abreise == ci_date)).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (func.lower(Rline.name) >= lname.lower()) &  (func.lower(Rline.name) <= (to_name).lower()) &  (Rline.abreise == ci_date)).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat != "":

            if lname == "":

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember) &  (Gmember.nation1 == (lnat).lower())).filter(
                        (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (Rline.abreise == ci_date)).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember) &  (Gmember.nation1 == (lnat).lower())).filter(
                        (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (func.lower(Rline.name).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.abreise == ci_date)).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember) &  (Gmember.nation1 == (lnat).lower())).filter(
                        (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (func.lower(Rline.name) >= lname.lower()) &  (func.lower(Rline.name) <= (to_name).lower()) &  (Rline.abreise == ci_date)).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 4:

            if lresnr == 0:

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (Rline.abreise == ci_date)).order_by(Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)


            else:

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (Rline.resnr == lresnr) &  (Rline.abreise == ci_date)).order_by(Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

    def count_all5():
        nonlocal troom, tpax, telop_list_list, rmlen, temp_total, temp_total2, guest, waehrung, reservation, zimkateg, res_line, zkstat, reslin_queasy, messages
        nonlocal sorttype, room, fdate1, fdate2, ci_date, lname, last_sort, lnat, lresnr
        nonlocal gmember

        nonlocal gmember, telop_list
        nonlocal telop_list_list

        to_name:str = ""
        rline = None
        whrg = None
        reservation = None
        gmember = None
        zkstat = None
        Rline =  create_buffer("Rline",Res_line)
        Whrg =  create_buffer("Whrg",Waehrung)
        Reserv =  create_buffer("Reserv",Reservation)
        Gme =  create_buffer("Gme",Guest)
        Zk =  create_buffer("Zk",Zimkateg)

        if lname != "" and substring(lname, 0, 1) != ("*").lower() :
            to_name = chr (ord(substring(lname, 0, 1)) + 1)

        if last_sort == 1 and room != "":
            if lname == "":
                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.resstatus == 8) &  (Rline.abreise == fdate2) &  (func.lower(Rline.zinr) >= (room).lower())).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :
                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.resstatus == 8) &  (func.lower(Rline.name).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.abreise == fdate2) &  (func.lower(Rline.zinr) >= (room).lower())).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.resstatus == 8) &  (func.lower(Rline.name) >= lname.lower()) &  (func.lower(Rline.name) <= (to_name).lower()) &  (Rline.abreise == fdate2) &  (func.lower(Rline.zinr) >= (room).lower())).order_by(Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 1 and room == "":

            if lname == "":

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.resstatus == 8) &  (Rline.abreise == fdate2)).order_by((Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.resstatus == 8) &  (func.lower(Rline.name).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.abreise == fdate2)).order_by(Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.resstatus == 8) &  (func.lower(Rline.name) >= lname.lower()) &  (func.lower(Rline.name) <= (to_name).lower()) &  (Rline.abreise == fdate2)).order_by(Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 2 and room != "":

            if lname == "":

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.resstatus == 8) &  (Rline.abreise == fdate2) &  (func.lower(Rline.zinr) >= (room).lower())).order_by(Rline.zinr, reservation.name, Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.resstatus == 8) &  (func.lower(Rline.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.abreise == fdate2) &  (func.lower(Rline.zinr) >= (room).lower())).order_by(Rline.zinr, Rline.resname, Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.resstatus == 8) &  (func.lower(Rline.resname) >= lname.lower()) &  (func.lower(Rline.resname) <= (to_name).lower()) &  (Rline.abreise == fdate2) &  (func.lower(Rline.zinr) >= (room).lower())).order_by(Rline.zinr, Rline.resname, Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 2 and room == "":

            if lname == "":

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.resstatus == 8) &  (Rline.abreise == fdate2)).order_by(reservation.name, Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.resstatus == 8) &  (func.lower(Rline.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.abreise == fdate2)).order_by(Rline.resname, Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr) &  (Reservation.name >= lname.lower()) &  (Reservation.name <= (to_name).lower())).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.resstatus == 8) &  (Rline.abreise == fdate2)).order_by(Rline.resname, Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat == "":

            if lname == "":

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.resstatus == 8) &  (Rline.abreise == fdate2)).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.resstatus == 8) &  (func.lower(Rline.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.abreise == fdate2)).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.resstatus == 8) &  (func.lower(Rline.resname) >= lname.lower()) &  (func.lower(Rline.resname) <= (to_name).lower()) &  (Rline.abreise == fdate2)).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat != "":

            if lname == "":

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember) &  (Gmember.nation1 == (lnat).lower())).filter(
                        (Rline.resstatus == 8) &  (Rline.abreise == fdate2)).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember) &  (Gmember.nation1 == (lnat).lower())).filter(
                        (Rline.resstatus == 8) &  (func.lower(Rline.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.abreise == fdate2)).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember) &  (Gmember.nation1 == (lnat).lower())).filter(
                        (Rline.resstatus == 8) &  (func.lower(Rline.resname) >= lname.lower()) &  (func.lower(Rline.resname) <= (to_name).lower()) &  (Rline.abreise == fdate2)).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 4:

            if lresnr == 0:

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.active_flag == 2) &  (Rline.resstatus == 8)).order_by(Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)


            else:

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        (Rline.active_flag == 2) &  (Rline.resstatus == 8) &  (Rline.resnr == lresnr)).order_by((Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

    def count_all6():

        nonlocal troom, tpax, telop_list_list, rmlen, temp_total, temp_total2, guest, waehrung, reservation, zimkateg, res_line, zkstat, reslin_queasy, messages
        nonlocal sorttype, room, fdate1, fdate2, ci_date, lname, last_sort, lnat, lresnr
        nonlocal gmember

        nonlocal gmember, telop_list
        nonlocal telop_list_list

        to_name:str = ""
        rline = None
        whrg = None
        reservation = None
        gmember = None
        zkstat = None
        Rline =  create_buffer("Rline",Res_line)
        Whrg =  create_buffer("Whrg",Waehrung)
        Reserv =  create_buffer("Reserv",Reservation)
        Gme =  create_buffer("Gme",Guest)
        Zk =  create_buffer("Zk",Zkstat)

        if lname != "" and substring(lname, 0, 1) != ("*").lower() :
            to_name = chr (ord(substring(lname, 0, 1)) + 1)

        if last_sort == 1:

            if room != "":
                if lname == "":

                    rline_obj_list = []
                    for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                            ((Rline.active_flag == 1) &  (Rline.resstatus != 12) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)) |  ((Rline.active_flag == 0) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Rline.ankunft == ci_date)) |  ((Rline.active_flag == 2) &  (Rline.resstatus == 8) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Rline.abreise == ci_date))).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                        if rline._recid in rline_obj_list:
                            continue
                        else:
                            rline_obj_list.append(rline._recid)

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                    rline_obj_list = []
                    for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                            ((Rline.active_flag == 1) &  (Rline.resstatus != 12) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Rline.name).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)) |  ((Rline.active_flag == 0) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Rline.name).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.ankunft == ci_date)) |  ((Rline.active_flag == 2) &  (Rline.resstatus == 8) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Rline.name).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.abreise == ci_date))).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                        if rline._recid in rline_obj_list:
                            continue
                        else:
                            rline_obj_list.append(rline._recid)

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)
                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                    rline_obj_list = []
                    for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                            ((Rline.active_flag == 1) &  (Rline.resstatus != 12) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Rline.name) >= lname.lower()) &  (func.lower(Rline.name) <= (to_name).lower()) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)) |  ((Rline.active_flag == 0) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Rline.name) >= lname.lower()) &  (func.lower(Rline.name) <= (to_name).lower()) &  (Rline.ankunft == ci_date)) |  ((Rline.active_flag == 2) &  (Rline.resstatus == 8) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Rline.name) >= lname.lower()) &  (func.lower(Rline.name) <= (to_name).lower()) &  (Rline.abreise == ci_date))).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                        if rline._recid in rline_obj_list:
                            continue
                        else:
                            rline_obj_list.append(rline._recid)

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)
                    tpax = to_string(temp_total)

            elif room == "":
                if lname == "":
                    rline_obj_list = []
                    recs = (
                        db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember)
                        .join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr))
                        .join(Reservation,(Reservation.resnr == Rline.resnr))
                        .join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr))
                        .join(Gmember,(Gmember.gastnr == Rline.gastnrmember))
                        .filter(
                            ((Rline.active_flag == 1) &  
                             (Rline.resstatus != 12) &  
                             (Rline.ankunft <= ci_date) &  
                             (Rline.abreise >= ci_date)) |  
                            ((Rline.active_flag == 0) &  (Rline.ankunft == ci_date)) |  
                            ((Rline.active_flag == 2) &  
                             (Rline.resstatus == 8) &  
                             (Rline.abreise == ci_date))
                            )
                            .order_by((Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all()
                    )
                    for rline, whrg, reservation, zkstat, gmember in recs:
                        if rline._recid in rline_obj_list:
                            continue
                        else:
                            rline_obj_list.append(rline._recid)

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)
                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                    rline_obj_list = []
                    for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                            ((Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (func.lower(Rline.name).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)) |  ((Rline.active_flag == 0) &  (func.lower(Rline.name).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.ankunft == ci_date)) |  ((Rline.active_flag == 2) &  (Rline.resstatus == 8) &  (func.lower(Rline.name).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.abreise == ci_date))).order_by(Rline.name).all():
                        if rline._recid in rline_obj_list:
                            continue
                        else:
                            rline_obj_list.append(rline._recid)

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)
                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                    rline_obj_list = []
                    for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                            ((Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (func.lower(Rline.name) >= lname.lower()) &  (func.lower(Rline.name) <= (to_name).lower()) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)) |  ((Rline.active_flag == 0) &  (func.lower(Rline.name) >= lname.lower()) &  (func.lower(Rline.name) <= (to_name).lower()) &  (Rline.ankunft == ci_date)) |  ((Rline.active_flag == 2) &  (Rline.resstatus == 8) &  (func.lower(Rline.name) >= lname.lower()) &  (func.lower(Rline.name) <= (to_name).lower()) &  (Rline.abreise == ci_date))).order_by(Rline.name).all():
                        if rline._recid in rline_obj_list:
                            continue
                        else:
                            rline_obj_list.append(rline._recid)

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)
                    tpax = to_string(temp_total)

        elif last_sort == 2:

            if lname == "" and room == "":

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        ((Rline.active_flag == 1) &  (Rline.resstatus != 12) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)) |  ((Rline.active_flag == 0) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Rline.ankunft == ci_date)) |  ((Rline.active_flag == 2) &  (Rline.resstatus == 8) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Rline.abreise == ci_date))).order_by(Rline.resname, Rline.resnr, Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname == "" and room != "":

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        ((Rline.active_flag == 1) &  (Rline.resstatus != 12) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)) |  ((Rline.active_flag == 0) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Rline.ankunft == ci_date)) |  ((Rline.active_flag == 2) &  (Rline.resstatus == 8) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (Rline.abreise == ci_date))).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        ((Rline.active_flag == 1) &  (Rline.resstatus != 12) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Rline.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)) |  ((Rline.active_flag == 0) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Rline.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.ankunft == ci_date)) |  ((Rline.active_flag == 2) &  (Rline.resstatus == 8) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Rline.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.abreise == ci_date))).order_by(Rline.resname, Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        ((Rline.active_flag == 1) &  (Rline.resstatus != 12) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Rline.resname) >= lname.lower()) &  (func.lower(Rline.resname) <= (to_name).lower()) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)) |  ((Rline.active_flag == 0) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Rline.resname) >= lname.lower()) &  (func.lower(Rline.resname) <= (to_name).lower()) &  (Rline.ankunft == ci_date)) |  ((Rline.active_flag == 2) &  (Rline.resstatus == 8) &  ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) &  (func.lower(Rline.resname) >= lname.lower()) &  (func.lower(Rline.resname) <= (to_name).lower()) &  (Rline.abreise == ci_date))).order_by(Rline.resname, Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat == "":

            if lname == "":

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        ((Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)) |  ((Rline.active_flag == 0) &  (Rline.ankunft == ci_date)) |  ((Rline.active_flag == 2) &  (Rline.resstatus == 8) &  (Rline.abreise == ci_date))).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        ((Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (func.lower(Rline.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)) |  ((Rline.active_flag == 0) &  (func.lower(Rline.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.ankunft == ci_date)) |  ((Rline.active_flag == 2) &  (Rline.resstatus == 8) &  (func.lower(Rline.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.abreise == ci_date))).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        ((Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (func.lower(Rline.resname) >= lname.lower()) &  (func.lower(Rline.resname) <= (to_name).lower()) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)) |  ((Rline.active_flag == 0) &  (func.lower(Rline.resname) >= lname.lower()) &  (func.lower(Rline.resname) <= (to_name).lower()) &  (Rline.ankunft == ci_date)) |  ((Rline.active_flag == 2) &  (Rline.resstatus == 8) &  (func.lower(Rline.resname) >= lname.lower()) &  (func.lower(Rline.resname) <= (to_name).lower()) &  (Rline.abreise == ci_date))).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat != "":

            if lname == "":

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember) &  (Gmember.nation1 == (lnat).lower())).filter(
                        ((Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)) |  ((Rline.active_flag == 0) &  (Rline.ankunft == ci_date)) |  ((Rline.active_flag == 2) &  (Rline.resstatus == 8) &  (Rline.abreise == ci_date))).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember) &  (Gmember.nation1 == (lnat).lower())).filter(
                        ((Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (func.lower(Rline.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)) |  ((Rline.active_flag == 0) &  (func.lower(Rline.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.ankunft == ci_date)) |  ((Rline.active_flag == 2) &  (Rline.resstatus == 8) &  (func.lower(Rline.resname).op("~")(((lname)).lower().replace("*",".*"))) &  (Rline.abreise == ci_date))).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember) &  (Gmember.nation1 == (lnat).lower())).filter(
                        ((Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (func.lower(Rline.resname) >= lname.lower()) &  (func.lower(Rline.resname) <= (to_name).lower()) &  (Rline.ankunft <= ci_date) &  (Rline.abreise >= ci_date)) |  ((Rline.active_flag == 0) &  (func.lower(Rline.resname) >= lname.lower()) &  (func.lower(Rline.resname) <= (to_name).lower()) &  (Rline.ankunft == ci_date)) |  ((Rline.active_flag == 2) &  (Rline.resstatus == 8) &  (func.lower(Rline.resname) >= lname.lower()) &  (func.lower(Rline.resname) <= (to_name).lower()) &  (Rline.abreise == ci_date))).order_by(gmember.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 4:

            if lresnr == 0:

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        ((Rline.active_flag == 1) &  (Rline.resstatus != 12)) |  ((Rline.active_flag == 0) &  (Rline.ankunft == ci_date)) |  ((Rline.active_flag == 2) &  (Rline.resstatus == 8) &  (Rline.abreise == ci_date))).order_by(Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)


            else:

                rline_obj_list = []
                for rline, whrg, reservation, zkstat, gmember in db_session.query(Rline, Whrg, Reservation, Zkstat, Gmember).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reservation,(Reservation.resnr == Rline.resnr)).join(Zkstat,(Zkstat.zikatnr == Rline.zikatnr)).join(Gmember,(Gmember.gastnr == Rline.gastnrmember)).filter(
                        ((Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (Rline.resnr == lresnr)) |  ((Rline.active_flag == 0) &  (Rline.resnr == lresnr) &  (Rline.ankunft == ci_date)) |  ((Rline.active_flag == 2) &  (Rline.resstatus == 8) &  (Rline.resnr == lresnr) &  (Rline.abreise == ci_date))).order_by((Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline._recid in rline_obj_list:
                        continue
                    else:
                        rline_obj_list.append(rline._recid)

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

    def assign_it():

        nonlocal troom, tpax, telop_list_list, rmlen, temp_total, temp_total2, guest, waehrung, reservation, zimkateg, res_line, zkstat, reslin_queasy, messages
        nonlocal sorttype, room, fdate1, fdate2, ci_date, lname, last_sort, lnat, lresnr
        nonlocal gmember
        nonlocal gmember, telop_list
        nonlocal telop_list_list

        if not guest or not(guest.gastnr == reservation.gastnr):
            guest = db_session.query(Guest).filter(
                (Guest.gastnr == reservation.gastnr)).first()
        telop_list = Telop_list()
        telop_list_list.append(telop_list)

        telop_list.resli_wabkurz = res_line.wabkurz
        telop_list.voucher_nr = res_line.voucher_nr
        telop_list.grpflag = reservation.grpflag
        telop_list.reser_name = reservation.name
        telop_list.zinr = res_line.zinr
        telop_list.resli_name = res_line.name
        telop_list.segmentcode = reservation.segmentcode
        telop_list.nation1 = gmember.nation1
        telop_list.resstatus = res_line.resstatus
        telop_list.l_zuordnung = res_line.l_zuordnung[2]
        telop_list.ankunft = res_line.ankunft
        telop_list.abreise = res_line.abreise
        telop_list.ankzeit = res_line.ankzeit
        telop_list.abreisezeit = res_line.abreisezeit
        telop_list.flight_nr = res_line.flight_nr
        telop_list.flight1 = substring(res_line.flight_nr, 0, 6)
        telop_list.eta = to_string(substring(res_line.flight_nr, 6, 5) , "99:99")
        telop_list.flight2 = substring(res_line.flight_nr, 11, 6)
        telop_list.etd = to_string(substring(res_line.flight_nr, 17, 5) , "99:99")
        telop_list.zimmeranz = res_line.zimmeranz
        telop_list.kurzbez = zimkateg.kurzbez
        telop_list.erwachs = res_line.erwachs
        telop_list.kind1 = res_line.kind1
        telop_list.gratis = res_line.gratis
        telop_list.waeh_wabkurz = waehrung.wabkurz
        telop_list.resnr = res_line.resnr
        telop_list.reslinnr = res_line.reslinnr
        telop_list.betrieb_gast = res_line.betrieb_gast
        telop_list.groupname = reservation.groupname
        telop_list.cancelled_id = res_line.cancelled_id
        telop_list.changed_id = res_line.changed_id
        telop_list.bemerk = res_line.bemerk
        telop_list.active_flag = res_line.active_flag
        telop_list.gastnrmember = res_line.gastnrmember
        telop_list.gastnr = res_line.gastnr
        telop_list.betrieb_gastmem = res_line.betrieb_gastmem
        telop_list.pseudofix = res_line.pseudofix
        telop_list.zikatnr = res_line.zikatnr
        telop_list.arrangement = res_line.arrangement
        telop_list.zipreis =  to_decimal(res_line.zipreis)
        telop_list.resname = reservation.name
        telop_list.address = guest.adresse1
        telop_list.city = guest.wohnort + " " + guest.plz
        telop_list.b_comments = reservation.bemerk

        if not reslin_queasy or not(reslin_queasy.key.lower()  == ("flag").lower()  and reslin_queasy.resnr == res_line.resnr and reslin_queasy.reslinnr == res_line.reslinnr and reslin_queasy.betriebsnr == 0):
            reslin_queasy = db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == ("flag").lower()) &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.betriebsnr == 0)).first()

        if reslin_queasy:

            if (reslin_queasy.char1 != "" and reslin_queasy.deci1 == 0) or (reslin_queasy.char2 != "" and reslin_queasy.deci2 == 0) or (reslin_queasy.char3 != "" and reslin_queasy.deci3 == 0):
                telop_list.flag_color = 1
            else:
                telop_list.flag_color = 9

        if not messages or not(messages.resnr == res_line.resnr and messages.reslinnr == res_line.reslinnr):
            messages = db_session.query(Messages).filter(
                (Messages.resnr == res_line.resnr) &  (Messages.reslinnr == res_line.reslinnr)).first()
        telop_list.message_flag = None != messages

    if sorttype == 1:
        local_storage.debugging = "masuk sorttype  1"
        disp_arl1()
        count_al1()
        local_storage.debugging = local_storage.debugging + ", lolos sorttype 1"

    elif sorttype == 2:
        local_storage.debugging = "masuk 2a"
        disp_arl2()
        count_all2()
        local_storage.debugging = local_storage.debugging + ", lolos 2a"

    elif sorttype == 4:
        local_storage.debugging = "masuk 4"
        disp_arl4()
        count_all4()
        local_storage.debugging = local_storage.debugging + ", lolos 4"

    elif sorttype == 5:
        local_storage.debugging = "masuk 5"
        disp_arl5()
        count_all5()
        local_storage.debugging = local_storage.debugging + ", lolos 5"

    elif sorttype == 6:
        local_storage.debugging = "masuk 6"
        disp_arl6()
        count_all6()
        local_storage.debugging = local_storage.debugging + ", lolos 6"

    return generate_output()