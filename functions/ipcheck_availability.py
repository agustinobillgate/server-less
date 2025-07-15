from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Zimkateg, Zimmer, Outorder, Res_line

def ipcheck_availability(rmtype:str, ci_date:date, co_date:date):
    avail_rm = 0
    clean_rm = 0
    curr_date:date = None
    fr_date:date = None
    to_date:date = None
    tot_rm:int = 0
    curr_avail:int = 0
    do_it:bool = False
    zimkateg = zimmer = outorder = res_line = None

    avail_list = room_list = None

    avail_list_list, Avail_list = create_model("Avail_list", {"datum":date, "avail_rm":int})
    room_list_list, Room_list = create_model("Room_list", {"zinr":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_rm, clean_rm, curr_date, fr_date, to_date, tot_rm, curr_avail, do_it, zimkateg, zimmer, outorder, res_line
        nonlocal rmtype, ci_date, co_date


        nonlocal avail_list, room_list
        nonlocal avail_list_list, room_list_list

        return {"avail_rm": avail_rm, "clean_rm": clean_rm}


    zimkateg = db_session.query(Zimkateg).filter(
             (func.lower(Zimkateg.kurzbez) == (rmtype).lower())).first()

    for zimmer in db_session.query(Zimmer).filter(
             (Zimmer.zikatnr == zimkateg.zikatnr) & (Zimmer.sleeping)).order_by(Zimmer._recid).all():
        tot_rm = tot_rm + 1

        if zimmer.zistatus == 0:
            room_list = Room_list()
            room_list_list.append(room_list)

            room_list.zinr = zimmer.zinr
            clean_rm = clean_rm + 1


    for curr_date in date_range(ci_date,(co_date - 1)) :
        avail_list = Avail_list()
        avail_list_list.append(avail_list)

        avail_list.datum = curr_date
        avail_list.avail_rm = tot_rm

    outorder_obj_list = []
    for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping) & (Zimmer.zikatnr == zimkateg.zikatnr)).filter(
             (not Outorder.gespstart >= co_date) & (not Outorder.gespende < ci_date) & (Outorder.betriebsnr <= 1)).order_by(Outorder._recid).all():
        if outorder._recid in outorder_obj_list:
            continue
        else:
            outorder_obj_list.append(outorder._recid)

        room_list = query(room_list_list, filters=(lambda room_list: room_list.zinr == outorder.zinr), first=True)

        if room_list:
            room_list_list.remove(room_list)
            clean_rm = clean_rm - 1

        if ci_date > outorder.gespstart:
            fr_date = ci_date
        else:
            fr_date = outorder.gespstart

        if co_date <= outorder.gespende:
            to_date = co_date - timedelta(days=1)
        else:
            to_date = outorder.gespende
        for curr_date in date_range(fr_date,to_date) :

            avail_list = query(avail_list_list, filters=(lambda avail_list: avail_list.datum == curr_date), first=True)

            if avail_list:
                avail_list.avail_rm = avail_list.avail_rm - 1

    for res_line in db_session.query(Res_line).filter(
             (not Res_line.ankunft >= co_date) & (not Res_line.abreise <= ci_date) & (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.zikatnr == zimkateg.zikatnr)).order_by(Res_line._recid).all():
        do_it = True

        if res_line.zinr != "":

            room_list = query(room_list_list, filters=(lambda room_list: room_list.zinr == res_line.zinr), first=True)

            if room_list:
                room_list_list.remove(room_list)
                clean_rm = clean_rm - 1

            zimmer = db_session.query(Zimmer).filter(
                     (Zimmer.zinr == res_line.zinr)).first()
            do_it = zimmer.sleeping

        if do_it:

            if ci_date > res_line.ankunft:
                fr_date = ci_date
            else:
                fr_date = res_line.ankunft

            if co_date <= res_line.abreise:
                to_date = co_date - timedelta(days=1)
            else:
                to_date = res_line.abreise - timedelta(days=1)
            for curr_date in date_range(fr_date,to_date) :

                avail_list = query(avail_list_list, filters=(lambda avail_list: avail_list.datum == curr_date), first=True)

                if avail_list:
                    avail_list.avail_rm = avail_list.avail_rm -\
                        res_line.zimmeranz

    for avail_list in query(avail_list_list, sort_by=[("avail_rm",False)]):

        if avail_list.avail_rm > 0:
            avail_rm = avail_list.avail_rm
        break

    return generate_output()