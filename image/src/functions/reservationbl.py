from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from models import Res_line, Reservation, Zimkateg, Guest, Kontline

def reservationbl(case_type:int, gastno:int, resno:int):
    mainres_list_list = []
    res_list_list = []
    ci_date:date = None
    i:int = 0
    str:str = ""
    res_bemerk:str = ""
    loopk:int = 0
    res_line = reservation = zimkateg = guest = kontline = None

    mainres_list = res_list = bresline = None

    mainres_list_list, Mainres_list = create_model("Mainres_list", {"resnr":int, "zimanz":int, "ankunft":date, "abreise":date, "segm":int, "deposit":decimal, "until":date, "paid":decimal, "id1":str, "id2":str, "id2_date":date, "groupname":str, "grpflag":bool, "bemerk":str, "voucher":str, "vesrdepot2":str, "arrival":bool, "resident":bool, "arr_today":bool}, {"ankunft": 01/01/2099, "abreise": 01/01/1998})
    res_list_list, Res_list = create_model("Res_list", {"name":str, "abreise":date, "zinr":str, "kurzbez":str, "zipreis":decimal, "arrangement":str, "erwachs":int, "gratis":int, "kind1":int, "kind2":int, "ankunft":date, "resstatus":int, "kontakt_nr":int, "zimmeranz":int, "anztage":int, "changed_id":str, "changed":date, "ratecode":str, "bemerk":str, "l_zuord3":int, "resnr":int, "reslinnr":int, "gastnrmember":int, "betrieb_gast":int, "zikatnr":int, "reserve_int":int, "kontignr":int, "karteityp":int, "allot_flag":int, "kontcode":str})

    Bresline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mainres_list_list, res_list_list, ci_date, i, str, res_bemerk, loopk, res_line, reservation, zimkateg, guest, kontline
        nonlocal bresline


        nonlocal mainres_list, res_list, bresline
        nonlocal mainres_list_list, res_list_list
        return {"mainres-list": mainres_list_list, "res-list": res_list_list}

    def update_mainres():

        nonlocal mainres_list_list, res_list_list, ci_date, i, str, res_bemerk, loopk, res_line, reservation, zimkateg, guest, kontline
        nonlocal bresline


        nonlocal mainres_list, res_list, bresline
        nonlocal mainres_list_list, res_list_list


        mainres_list.ankunft = 01/01/2099
        mainres_list.abreise = 01/01/1998
        mainres_list.zimanz = 0
        mainres_list.arrival = False
        mainres_list.arr_today = False
        mainres_list.resident = False

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == mainres_list.resnr) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (Res_line.resstatus != 99)).all():

            if res_line.resstatus <= 6:
                mainres_list.zimanz = mainres_list.zimanz + res_line.zimmeranz

            if mainres_list.ankunft > res_line.ankunft:
                mainres_list.ankunft = res_line.ankunft

            if mainres_list.abreise < res_line.abreise:
                mainres_list.abreise = res_line.abreise

            if (res_line.resstatus <= 5 or res_line.resstatus == 11):
                mainres_list.arrival = True

            if mainres_list.arrival  and res_line.ankunft == ci_date:
                mainres_list.arr_today = True

            if res_line.resstatus == 6 or res_line.resstatus == 13:
                mainres_list.resident = True

    def update_gcfinfo():

        nonlocal mainres_list_list, res_list_list, ci_date, i, str, res_bemerk, loopk, res_line, reservation, zimkateg, guest, kontline
        nonlocal bresline


        nonlocal mainres_list, res_list, bresline
        nonlocal mainres_list_list, res_list_list

        ci_date:date = None
        ci_date = get_output(htpdate(87))

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.gastnr == gastno) &  (Res_line.active_flag <= 1) &  (Res_line.resstatus != 12) &  (Res_line.resstatus != 99)).all():

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == res_line.gastnrmember)).first()

            if guest.erste_res == None:
                guest.erste_res = ci_date

            if guest.naechste_res == None or guest.naechste_res < res_line.ankunft:
                guest.naechste_res = res_line.ankunft
            guest.letzte_res = ci_date


    ci_date = get_output(htpdate(87))

    if case_type == 1:

        if resno == 0:

            reservation_obj_list = []
            for reservation, res_line in db_session.query(Reservation, Res_line).join(Res_line,(Res_line.resnr == Reservation.resnr) &  (Res_line.active_flag <= 1)).filter(
                    (Reservation.gastnr == gastno) &  (Reservation.activeflag == 0)).all():
                if reservation._recid in reservation_obj_list:
                    continue
                else:
                    reservation_obj_list.append(reservation._recid)


                mainres_list = Mainres_list()
                mainres_list_list.append(mainres_list)

                mainres_list.resnr = reservation.resnr
                mainres_list.deposit = reservation.depositgef
                mainres_list.until = reservation.limitdate
                mainres_list.paid = depositbez + depositbez2
                mainres_list.segm = reservation.segmentcode
                mainres_list.groupname = reservation.groupname
                mainres_list.bemerk = reservation.bemerk
                mainres_list.id1 = reservation.useridanlage
                mainres_list.id2 = reservation.useridmutat
                mainres_list.id2_date = reservation.mutdat
                mainres_list.grpflag = reservation.grpflag
                mainres_list.voucher = reservation.vesrdepot


                update_mainres()

        else:

            reservation = db_session.query(Reservation).filter(
                    (Reservation.gastnr == gastno) &  (Reservation.resnr == resno) &  (Reservation.activeflag == 0)).first()

            if reservation:
                mainres_list = Mainres_list()
                mainres_list_list.append(mainres_list)

                mainres_list.resnr = reservation.resnr
                mainres_list.deposit = reservation.depositgef
                mainres_list.until = reservation.limitdate
                mainres_list.paid = depositbez + depositbez2
                mainres_list.segm = reservation.segmentcode
                mainres_list.groupname = reservation.groupname
                mainres_list.bemerk = reservation.bemerk
                mainres_list.id1 = reservation.useridanlage
                mainres_list.id2 = reservation.useridmutat
                mainres_list.id2_date = reservation.mutdat
                mainres_list.grpflag = reservation.grpflag
                mainres_list.voucher = reservation.vesrdepot


                update_mainres()
    elif case_type == 2:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.active_flag <= 1) &  (Res_line.resstatus != 12) &  (Res_line.resstatus != 99)).all():

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == res_line.zikatnr)).first()

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == res_line.gastnrmember)).first()
            res_list = Res_list()
            res_list_list.append(res_list)

            buffer_copy(res_line, res_list)
            res_list.bemerk = replace_str(res_list.bemerk, chr(10) , "")


            res_list.bemerk = replace_str(res_list.bemerk, chr(13) , "")
            res_list.bemerk = replace_str(res_list.bemerk, "~n", "")
            res_list.bemerk = replace_str(res_list.bemerk, "\\n", "")
            res_list.bemerk = replace_str(res_list.bemerk, "~r", "")
            res_list.bemerk = replace_str(res_list.bemerk, "~r~n", "")
            res_list.bemerk = replace_str(res_list.bemerk, chr(10) + chr(13) , "")
            res_bemerk = ""
            for loopk in range(1,len(res_list.bemerk)  + 1) :

                if ord(substring(res_list.bemerk, loopk - 1, 1)) == 0:
                    pass
                else:
                    res_bemerk = res_bemerk + substring(res_list.bemerk, loopk - 1, 1)
            res_list.bemerk = res_bemerk

            if len(res_list.bemerk) < 3:
                res_list.bemerk = replace_str(res_list.bemerk, chr(32) , "")

            if len(res_list.bemerk) == None:
                res_list.bemerk = ""
            for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                str = entry(i - 1, res_line.zimmer_wunsch, ";")

                if substring(str, 0, 6) == "$CODE$":
                    res_list.ratecode = substring(str, 6)
            res_list.karteityp = guest.karteityp
            res_list.l_zuord3 = res_line.l_zuordnung[2]
            res_list.kurzbez = zimkateg.kurzbez

            kontline = db_session.query(Kontline).filter(
                    (Kontline.kontignr == res_line.kontignr) &  (Kontline.betriebsnr == 0) &  (Kontline.kontstat == 1)).first()

            if kontline:
                res_list.allot_flag = 1
                res_list.kontcode = kontline.kontcode


            else:

                kontline = db_session.query(Kontline).filter(
                        (Kontline.kontignr == - res_line.kontignr) &  (Kontline.betriebsnr == 1) &  (Kontline.kontstat == 1)).first()

                if kontline:
                    res_list.allot_flag = -1
                    res_list.kontcode = kontline.kontcode


    elif case_type == 3:
        update_gcfinfo()

    return generate_output()