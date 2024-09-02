from functions.additional_functions import *
import decimal
from datetime import date
from models import Zimkateg, Res_line, Reservation, Guest

def res_list_webbl(case_type:int, from_date:date, to_date:date, resnr:int, gastnr:int, search_resno:int):
    curr_select:str = ""
    res_listmain_list = []
    res_listmember_list = []
    zimkateg = res_line = reservation = guest = None

    res_listmain = res_listmember = None

    res_listmain_list, Res_listmain = create_model("Res_listmain", {"resdat":date, "resnr":int, "name":str, "groupname":str, "depositgef":decimal, "limitdate":date, "depositbez":decimal, "zahldatum":date, "depositbez2":decimal, "zahldatum2":date, "useridanlage":str, "mutdat":date, "useridmutat":str, "gastnr":int, "bemerk":str, "grpflag":bool, "activeflag":int, "resname":str, "address":str, "city":str})
    res_listmember_list, Res_listmember = create_model("Res_listmember", {"name":str, "ankunft":date, "abreise":date, "zinr":str, "kurzbez":str, "zipreis":decimal, "arrangement":str, "erwachs":int, "gratis":int, "zimmeranz":int, "anztage":int, "changed_id":str, "changed":date, "gastnr":int, "resstatus":int, "zikatnr":int, "resnr":int, "bemerk":str, "active_flag":int, "l_zuordnung":[int], "reslinnr":int, "res_recid":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_select, res_listmain_list, res_listmember_list, zimkateg, res_line, reservation, guest


        nonlocal res_listmain, res_listmember
        nonlocal res_listmain_list, res_listmember_list
        return {"res-listmain": res_listmain_list, "res-listmember": res_listmember_list}

    def calc_br1():

        nonlocal curr_select, res_listmain_list, res_listmember_list, zimkateg, res_line, reservation, guest


        nonlocal res_listmain, res_listmember
        nonlocal res_listmain_list, res_listmember_list


        res_listmain_list.clear()
        res_listmember_list.clear()
        curr_select = ""

        res_line_obj_list = []
        for res_line, zimkateg in db_session.query(Res_line, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                (Res_line.resnr == resnr) &  (Res_line.resstatus != 12) &  (Res_line.resstatus != 99)).all():
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

    def update_browse_b2():

        nonlocal curr_select, res_listmain_list, res_listmember_list, zimkateg, res_line, reservation, guest


        nonlocal res_listmain, res_listmember
        nonlocal res_listmain_list, res_listmember_list


        res_listmain_list.clear()
        res_listmember_list.clear()

        if search_resno == 0:
            curr_select = ""

            for reservation in db_session.query(Reservation).filter(
                    (Reservation.resdat >= from_date) &  (Reservation.resdat <= to_date) &  (Reservation.activeflag <= 1)).all():

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == reservation.resnr) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (Res_line.resstatus != 99)).first()

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

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resdat >= from_date) &  (Reservation.resdat <= to_date) &  (Reservation.activeflag <= 1)).first()

            if reservation:
                curr_select = "mainres"
        else:
            curr_select = ""

            for reservation in db_session.query(Reservation).filter(
                    (Reservation.resnr == search_resno) &  (Reservation.activeflag <= 1)).all():

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == reservation.resnr) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12)).first()

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

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == search_resno) &  (Reservation.activeflag <= 1)).first()

            if reservation:
                curr_select = "mainres"

    res_listmain_list.clear()
    res_listmember_list.clear()

    if case_type == 1:
        update_browse_b2()
    else:
        calc_br1()

    return generate_output()