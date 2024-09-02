from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Zimkateg, Res_line, Guest, Reservation, Segment, Sourccod, Reslin_queasy, Guestseg

def res_list_1_webbl(case_type:int, from_date:date, to_date:date, resnr:int, gastnr:int, search_resno:int, search_voucher:str):
    curr_select:str = ""
    res_listmain_list = []
    res_listmember_list = []
    vip_nr:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    res_bemerk:str = ""
    loopk:int = 0
    htparam = zimkateg = res_line = guest = reservation = segment = sourccod = reslin_queasy = guestseg = None

    res_listmain = res_listmember = None

    res_listmain_list, Res_listmain = create_model("Res_listmain", {"resdat":date, "resnr":int, "name":str, "groupname":str, "depositgef":decimal, "limitdate":date, "depositbez":decimal, "zahldatum":date, "depositbez2":decimal, "zahldatum2":date, "useridanlage":str, "mutdat":date, "useridmutat":str, "gastnr":int, "bemerk":str, "grpflag":bool, "activeflag":int, "resname":str, "address":str, "city":str, "sob":str})
    res_listmember_list, Res_listmember = create_model("Res_listmember", {"name":str, "ankunft":date, "abreise":date, "zinr":str, "kurzbez":str, "zipreis":decimal, "arrangement":str, "erwachs":int, "gratis":int, "zimmeranz":int, "anztage":int, "changed_id":str, "changed":date, "gastnr":int, "resstatus":int, "zikatnr":int, "resnr":int, "bemerk":str, "active_flag":int, "l_zuordnung":[int], "reslinnr":int, "res_recid":int, "vip":str, "nat":str, "rate_code":str, "segment":str, "sp_req":str, "usr_id":str, "ratecode":str, "voucher_no":str, "child":int, "email":str, "phone_no":str, "sob":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_select, res_listmain_list, res_listmember_list, vip_nr, res_bemerk, loopk, htparam, zimkateg, res_line, guest, reservation, segment, sourccod, reslin_queasy, guestseg


        nonlocal res_listmain, res_listmember
        nonlocal res_listmain_list, res_listmember_list
        return {"res-listmain": res_listmain_list, "res-listmember": res_listmember_list}

    def calc_br1():

        nonlocal curr_select, res_listmain_list, res_listmember_list, vip_nr, res_bemerk, loopk, htparam, zimkateg, res_line, guest, reservation, segment, sourccod, reslin_queasy, guestseg


        nonlocal res_listmain, res_listmember
        nonlocal res_listmain_list, res_listmember_list

        loopi:int = 0
        str:str = ""
        res_listmain_list.clear()
        res_listmember_list.clear()
        curr_select = ""

        res_line_obj_list = []
        for res_line, zimkateg in db_session.query(Res_line, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                (Res_line.resnr == resnr) &  (Res_line.resstatus != 12)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            res_listmember = Res_listmember()
            res_listmember_list.append(res_listmember)

            res_listmember.name = res_line.name
            res_listmember.ankunft = res_line.ankunft
            res_listmember.abreise = res_line.abreise
            res_listmember.zinr = res_line.zinr
            res_listmember.kurzbez = zimkateg.kurzbez
            res_listmember.zipreis = res_line.zipreis
            res_listmember.arrangement = res_line.arrangement
            res_listmember.erwachs = res_line.erwachs
            res_listmember.gratis = res_line.gratis
            res_listmember.zimmeranz = res_line.zimmeranz
            res_listmember.anztage = res_line.anztage
            res_listmember.changed_id = res_line.changed_id
            res_listmember.changed = res_line.changed
            res_listmember.gastnr = res_line.gastnr
            res_listmember.resstatus = res_line.resstatus + res_line.l_zuordnung[2]
            res_listmember.zikatnr = res_line.zikatnr
            res_listmember.resnr = res_line.resnr
            res_listmember.bemerk = res_line.bemerk
            res_listmember.active_flag = res_line.active_flag
            res_listmember.l_zuordnung[2] = res_line.l_zuordnung[2]
            res_listmember.reslinnr = res_line.reslinnr
            res_listmember.res_recid = res_line._recid
            res_listmember.child = res_line.kind1


            res_listmember.bemerk = replace_str(res_listmember.bemerk, chr(10) , "")


            res_listmember.bemerk = replace_str(res_listmember.bemerk, chr(13) , "")
            res_listmember.bemerk = replace_str(res_listmember.bemerk, "~n", "")
            res_listmember.bemerk = replace_str(res_listmember.bemerk, "\\n", "")
            res_listmember.bemerk = replace_str(res_listmember.bemerk, "~r", "")
            res_listmember.bemerk = replace_str(res_listmember.bemerk, "~r~n", "")
            res_listmember.bemerk = replace_str(res_listmember.bemerk, chr(10) + chr(13) , "")
            res_bemerk = ""
            for loopk in range(1,len(res_listmember.bemerk)  + 1) :

                if ord(substring(res_listmember.bemerk, loopk - 1, 1)) == 0:
                    pass
                else:
                    res_bemerk = res_bemerk + substring(res_listmember.bemerk, loopk - 1, 1)
            res_listmember.bemerk = res_bemerk

            if len(res_listmember.bemerk) < 3:
                res_listmember.bemerk = replace_str(res_listmember.bemerk, chr(32) , "")

            if len(res_listmember.bemerk) == None:
                res_listmember.bemerk = ""

            if reslin_queasy:
                res_listmember.ratecode = reslin_queasy.char2


            else:
                res_listmember.ratecode = "Undefined"

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == res_line.gastnrmember)).first()

            if guest:

                if guest.mobil_telefon != "":
                    res_listmember.phone_no = guest.mobil_telefon

                if guest.mobil_telefon == "" and guest.telefon != "":
                    res_listmember.phone_no = guest.telefon

                if guest.email_adr != "":
                    res_listmember.email = guest.email_adr


            else:
                res_listmember.email = ""
                res_listmember.phone_no = ""

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == res_line.resnr)).first()

            if reservation:

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == reservation.segmentcode)).first()

                if segment:
                    res_listmember.segment = entry(0, segment.bezeich, "$$0")
                res_listmember.usr_id = reservation.useridanlage
                res_listmember.voucher_no = reservation.vesrdepot

                sourccod = db_session.query(Sourccod).filter(
                        (Sourccod.betriebsnr == reservation.betriebsnr)).first()

                if sourccod:
                    res_listmember.sob = sourccod.bezeich


            for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                if substring(str, 0, 6) == "$CODE$":
                    res_listmember.rate_code = substring(str, 6)
                    break

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                    (func.lower(Reslin_queasy.key) == "specialRequest") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

            if reslin_queasy:
                res_listmember.sp_req = reslin_queasy.char3 + "," + res_listmember.sp_req
                res_listmember.ratecode = reslin_queasy.char2


            else:
                res_listmember.ratecode = "Undefined"

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == res_line.gastnrmember)).first()

            if guest:

                guestseg = db_session.query(Guestseg).filter(
                        (Guestseg.gastnr == guest.gastnr) &  ((Guestseg.segmentcode == vip_nr[0]) |  (Guestseg.segmentcode == vip_nr[1]) |  (Guestseg.segmentcode == vip_nr[2]) |  (Guestseg.segmentcode == vip_nr[3]) |  (Guestseg.segmentcode == vip_nr[4]) |  (Guestseg.segmentcode == vip_nr[5]) |  (Guestseg.segmentcode == vip_nr[6]) |  (Guestseg.segmentcode == vip_nr[7]) |  (Guestseg.segmentcode == vip_nr[8]) |  (Guestseg.segmentcode == vip_nr[9]))).first()

                if guestseg:

                    segment = db_session.query(Segment).filter(
                            (Segment.segmentcode == guestseg.segmentcode)).first()

                    if segment:
                        res_listmember.vip = segment.bezeich


                res_listmember.nat = guest.nation1

    def update_browse_b2():

        nonlocal curr_select, res_listmain_list, res_listmember_list, vip_nr, res_bemerk, loopk, htparam, zimkateg, res_line, guest, reservation, segment, sourccod, reslin_queasy, guestseg


        nonlocal res_listmain, res_listmember
        nonlocal res_listmain_list, res_listmember_list


        res_listmain_list.clear()
        res_listmember_list.clear()

        if search_resno == 0 and search_voucher == "":
            curr_select = ""

            for reservation in db_session.query(Reservation).filter(
                    (Reservation.resdat >= from_date) &  (Reservation.resdat <= to_date) &  (Reservation.activeflag <= 1)).all():

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == reservation.resnr) &  (Res_line.resstatus != 12)).first()

                if res_line:
                    res_listmain = Res_listmain()
                    res_listmain_list.append(res_listmain)

                    res_listmain.resdat = reservation.resdat
                    res_listmain.resnr = reservation.resnr
                    res_listmain.name = reservation.name
                    res_listmain.groupname = reservation.groupname
                    res_listmain.depositgef = reservation.depositgef
                    res_listmain.limitdate = reservation.limitdate
                    res_listmain.depositbez = reservation.depositbez
                    res_listmain.zahldatum = reservation.zahldatum
                    res_listmain.depositbez2 = reservation.depositbez2
                    res_listmain.zahldatum2 = reservation.zahldatum2
                    res_listmain.useridanlage = reservation.useridanlage
                    res_listmain.mutdat = reservation.mutdat
                    res_listmain.useridmutat = reservation.useridmutat
                    res_listmain.gastnr = reservation.gastnr
                    res_listmain.bemerk = reservation.bemerk
                    res_listmain.grpflag = reservation.grpflag
                    res_listmain.activeflag = reservation.activeflag

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == reservation.gastnr)).first()

                    if guest:
                        res_listmain.resname = guest.name + ", " + guest.vorname1 +\
                                guest.anredefirma + " " + guest.anrede1
                        res_listmain.address = guest.adresse1 + " " + guest.adresse2
                        res_listmain.city = guest.land + " " + guest.wohnort + " " +\
                                guest.plz


                    res_listmain.bemerk = replace_str(res_listmain.bemerk, chr(10) , "")


                    res_listmain.bemerk = replace_str(res_listmain.bemerk, chr(13) , "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, "~n", "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, "\\n", "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, "~r", "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, "~r~n", "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, chr(10) + chr(13) , "")
                    res_bemerk = ""
                    for loopk in range(1,len(res_listmain.bemerk)  + 1) :

                        if ord(substring(res_listmain.bemerk, loopk - 1, 1)) == 0:
                            pass
                        else:
                            res_bemerk = res_bemerk + substring(res_listmain.bemerk, loopk - 1, 1)
                    res_listmain.bemerk = res_bemerk

                    if len(res_listmain.bemerk) < 3:
                        res_listmain.bemerk = replace_str(res_listmain.bemerk, chr(32) , "")

                    if len(res_listmain.bemerk) == None:
                        res_listmain.bemerk = ""

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resdat >= from_date) &  (Reservation.resdat <= to_date) &  (Reservation.activeflag <= 1)).first()

            if reservation:
                curr_select = "mainres"

        elif search_resno != 0:
            curr_select = ""

            for reservation in db_session.query(Reservation).filter(
                    (Reservation.resnr == search_resno) &  (Reservation.activeflag <= 1)).all():

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == reservation.resnr) &  (Res_line.resstatus != 12)).first()

                if res_line:
                    res_listmain = Res_listmain()
                    res_listmain_list.append(res_listmain)

                    res_listmain.resdat = reservation.resdat
                    res_listmain.resnr = reservation.resnr
                    res_listmain.name = reservation.name
                    res_listmain.groupname = reservation.groupname
                    res_listmain.depositgef = reservation.depositgef
                    res_listmain.limitdate = reservation.limitdate
                    res_listmain.depositbez = reservation.depositbez
                    res_listmain.zahldatum = reservation.zahldatum
                    res_listmain.depositbez2 = reservation.depositbez2
                    res_listmain.zahldatum2 = reservation.zahldatum2
                    res_listmain.useridanlage = reservation.useridanlage
                    res_listmain.mutdat = reservation.mutdat
                    res_listmain.useridmutat = reservation.useridmutat
                    res_listmain.gastnr = reservation.gastnr
                    res_listmain.bemerk = reservation.bemerk
                    res_listmain.grpflag = reservation.grpflag
                    res_listmain.activeflag = reservation.activeflag

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == reservation.gastnr)).first()

                    if guest:
                        res_listmain.resname = guest.name + ", " + guest.vorname1 +\
                                guest.anredefirma + " " + guest.anrede1
                        res_listmain.address = guest.adresse1 + " " + guest.adresse2
                        res_listmain.city = guest.land + " " + guest.wohnort + " " +\
                                guest.plz


                    res_listmain.bemerk = replace_str(res_listmain.bemerk, chr(10) , "")


                    res_listmain.bemerk = replace_str(res_listmain.bemerk, chr(13) , "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, "~n", "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, "\\n", "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, "~r", "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, "~r~n", "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, chr(10) + chr(13) , "")
                    res_bemerk = ""
                    for loopk in range(1,len(res_listmain.bemerk)  + 1) :

                        if ord(substring(res_listmain.bemerk, loopk - 1, 1)) == 0:
                            pass
                        else:
                            res_bemerk = res_bemerk + substring(res_listmain.bemerk, loopk - 1, 1)
                    res_listmain.bemerk = res_bemerk

                    if len(res_listmain.bemerk) < 3:
                        res_listmain.bemerk = replace_str(res_listmain.bemerk, chr(32) , "")

                    if len(res_listmain.bemerk) == None:
                        res_listmain.bemerk = ""

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == search_resno) &  (Reservation.activeflag <= 1)).first()

            if reservation:
                curr_select = "mainres"

        elif search_voucher != "":
            curr_select = ""

            for reservation in db_session.query(Reservation).filter(
                    (func.lower(Reservation.vesrdepot) == (search_voucher).lower()) &  (Reservation.activeflag <= 1)).all():

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == reservation.resnr) &  (Res_line.resstatus != 12)).first()

                if res_line:
                    res_listmain = Res_listmain()
                    res_listmain_list.append(res_listmain)

                    res_listmain.resdat = reservation.resdat
                    res_listmain.resnr = reservation.resnr
                    res_listmain.name = reservation.name
                    res_listmain.groupname = reservation.groupname
                    res_listmain.depositgef = reservation.depositgef
                    res_listmain.limitdate = reservation.limitdate
                    res_listmain.depositbez = reservation.depositbez
                    res_listmain.zahldatum = reservation.zahldatum
                    res_listmain.depositbez2 = reservation.depositbez2
                    res_listmain.zahldatum2 = reservation.zahldatum2
                    res_listmain.useridanlage = reservation.useridanlage
                    res_listmain.mutdat = reservation.mutdat
                    res_listmain.useridmutat = reservation.useridmutat
                    res_listmain.gastnr = reservation.gastnr
                    res_listmain.bemerk = reservation.bemerk
                    res_listmain.grpflag = reservation.grpflag
                    res_listmain.activeflag = reservation.activeflag

                    sourccod = db_session.query(Sourccod).filter(
                            (Sourccod.betriebsnr == reservation.betriebsnr)).first()

                    if sourccod:
                        res_listmain.sob = sourccod.bezeich

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == reservation.gastnr)).first()

                    if guest:
                        res_listmain.resname = guest.name + ", " + guest.vorname1 +\
                                guest.anredefirma + " " + guest.anrede1
                        res_listmain.address = guest.adresse1 + " " + guest.adresse2
                        res_listmain.city = guest.land + " " + guest.wohnort + " " +\
                                guest.plz

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == search_resno) &  (Reservation.activeflag <= 1)).first()

            if reservation:
                curr_select = "mainres"


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 700)).first()
    vip_nr[0] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 701)).first()
    vip_nr[1] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 702)).first()
    vip_nr[2] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 703)).first()
    vip_nr[3] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 704)).first()
    vip_nr[4] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 705)).first()
    vip_nr[5] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 706)).first()
    vip_nr[6] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 707)).first()
    vip_nr[7] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 708)).first()
    vip_nr[8] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 712)).first()
    vip_nr[9] = htparam.finteger
    res_listmain_list.clear()
    res_listmember_list.clear()

    if case_type == 1:
        update_browse_b2()
    else:
        calc_br1()

    return generate_output()