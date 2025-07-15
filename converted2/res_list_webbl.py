#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Zimkateg, Res_line, Reservation, Guest

def res_list_webbl(case_type:int, from_date:date, to_date:date, resnr:int, gastnr:int, search_resno:int):

    prepare_cache ([Zimkateg, Res_line, Reservation, Guest])

    curr_select:string = ""
    res_listmain_data = []
    res_listmember_data = []
    zimkateg = res_line = reservation = guest = None

    res_listmain = res_listmember = None

    res_listmain_data, Res_listmain = create_model("Res_listmain", {"resdat":date, "resnr":int, "name":string, "groupname":string, "depositgef":Decimal, "limitdate":date, "depositbez":Decimal, "zahldatum":date, "depositbez2":Decimal, "zahldatum2":date, "useridanlage":string, "mutdat":date, "useridmutat":string, "gastnr":int, "bemerk":string, "grpflag":bool, "activeflag":int, "resname":string, "address":string, "city":string})
    res_listmember_data, Res_listmember = create_model("Res_listmember", {"name":string, "ankunft":date, "abreise":date, "zinr":string, "kurzbez":string, "zipreis":Decimal, "arrangement":string, "erwachs":int, "gratis":int, "zimmeranz":int, "anztage":int, "changed_id":string, "changed":date, "gastnr":int, "resstatus":int, "zikatnr":int, "resnr":int, "bemerk":string, "active_flag":int, "l_zuordnung":[int,5], "reslinnr":int, "res_recid":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_select, res_listmain_data, res_listmember_data, zimkateg, res_line, reservation, guest
        nonlocal case_type, from_date, to_date, resnr, gastnr, search_resno


        nonlocal res_listmain, res_listmember
        nonlocal res_listmain_data, res_listmember_data

        return {"res-listmain": res_listmain_data, "res-listmember": res_listmember_data}

    def calc_br1():

        nonlocal curr_select, res_listmain_data, res_listmember_data, zimkateg, res_line, reservation, guest
        nonlocal case_type, from_date, to_date, resnr, gastnr, search_resno


        nonlocal res_listmain, res_listmember
        nonlocal res_listmain_data, res_listmember_data


        res_listmain_data.clear()
        res_listmember_data.clear()
        curr_select = ""

        res_line_obj_list = {}
        res_line = Res_line()
        zimkateg = Zimkateg()
        for res_line.name, res_line.ankunft, res_line.abreise, res_line.zinr, res_line.zipreis, res_line.arrangement, res_line.erwachs, res_line.gratis, res_line.zimmeranz, res_line.anztage, res_line.changed_id, res_line.changed, res_line.gastnr, res_line.resstatus, res_line.l_zuordnung, res_line.zikatnr, res_line.resnr, res_line.bemerk, res_line.active_flag, res_line.reslinnr, res_line._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zinr, Res_line.zipreis, Res_line.arrangement, Res_line.erwachs, Res_line.gratis, Res_line.zimmeranz, Res_line.anztage, Res_line.changed_id, Res_line.changed, Res_line.gastnr, Res_line.resstatus, Res_line.l_zuordnung, Res_line.zikatnr, Res_line.resnr, Res_line.bemerk, Res_line.active_flag, Res_line.reslinnr, Res_line._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                 (Res_line.resnr == resnr) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99)).order_by(Res_line.resnr, Res_line.reslinnr, Res_line.zinr, Res_line.ankunft, Res_line.resstatus, func.substring(Res_line.name, 0, 32)).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            res_listmember = Res_listmember()
            res_listmember_data.append(res_listmember)

            res_listmember.name = res_line.name
            res_listmember.ankunft = res_line.ankunft
            res_listmember.abreise = res_line.abreise
            res_listmember.zinr = res_line.zinr
            res_listmember.kurzbez = zimkateg.kurzbez
            res_listmember.zipreis =  to_decimal(res_line.zipreis)
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
            res_listmember.l_zuordnung = res_line.l_zuordnung
            res_listmember.reslinnr = res_line.reslinnr
            res_listmember.res_recid = res_line._recid


    def update_browse_b2():

        nonlocal curr_select, res_listmain_data, res_listmember_data, zimkateg, res_line, reservation, guest
        nonlocal case_type, from_date, to_date, resnr, gastnr, search_resno


        nonlocal res_listmain, res_listmember
        nonlocal res_listmain_data, res_listmember_data


        res_listmain_data.clear()
        res_listmember_data.clear()

        if search_resno == 0:
            curr_select = ""

            for reservation in db_session.query(Reservation).filter(
                     (Reservation.resdat >= from_date) & (Reservation.resdat <= to_date) & (Reservation.activeflag <= 1)).order_by(Reservation.resnr, Reservation.resdat, func.substring(Reservation.name, 0, 32)).all():

                res_line = get_cache (Res_line, {"resnr": [(eq, reservation.resnr)],"resstatus": [(ne, 9),(ne, 10),(ne, 12),(ne, 99)]})

                if res_line:
                    res_listmain = Res_listmain()
                    res_listmain_data.append(res_listmain)

                    res_listmain.resdat = reservation.resdat
                    res_listmain.resnr = reservation.resnr
                    res_listmain.name = reservation.name
                    res_listmain.groupname = reservation.groupname
                    res_listmain.depositgef =  to_decimal(reservation.depositgef)
                    res_listmain.limitdate = reservation.limitdate
                    res_listmain.depositbez =  to_decimal(reservation.depositbez)
                    res_listmain.zahldatum = reservation.zahldatum
                    res_listmain.depositbez2 =  to_decimal(reservation.depositbez2)
                    res_listmain.zahldatum2 = reservation.zahldatum2
                    res_listmain.useridanlage = reservation.useridanlage
                    res_listmain.mutdat = reservation.mutdat
                    res_listmain.useridmutat = reservation.useridmutat
                    res_listmain.gastnr = reservation.gastnr
                    res_listmain.bemerk = reservation.bemerk
                    res_listmain.grpflag = reservation.grpflag
                    res_listmain.activeflag = reservation.activeflag

                    guest = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                    if guest:
                        res_listmain.resname = guest.name + ", " + guest.vorname1 +\
                                guest.anredefirma + " " + guest.anrede1
                        res_listmain.address = guest.adresse1 + " " + guest.adresse2
                        res_listmain.city = guest.land + " " + guest.wohnort + " " +\
                                guest.plz

            reservation = get_cache (Reservation, {"resdat": [(ge, from_date),(le, to_date)],"activeflag": [(le, 1)]})

            if reservation:
                curr_select = "mainres"
        else:
            curr_select = ""

            for reservation in db_session.query(Reservation).filter(
                     (Reservation.resnr == search_resno) & (Reservation.activeflag <= 1)).order_by(Reservation.resdat, func.substring(Reservation.name, 0, 32)).all():

                res_line = get_cache (Res_line, {"resnr": [(eq, reservation.resnr)],"resstatus": [(ne, 9),(ne, 10),(ne, 12)]})

                if res_line:
                    res_listmain = Res_listmain()
                    res_listmain_data.append(res_listmain)

                    res_listmain.resdat = reservation.resdat
                    res_listmain.resnr = reservation.resnr
                    res_listmain.name = reservation.name
                    res_listmain.groupname = reservation.groupname
                    res_listmain.depositgef =  to_decimal(reservation.depositgef)
                    res_listmain.limitdate = reservation.limitdate
                    res_listmain.depositbez =  to_decimal(reservation.depositbez)
                    res_listmain.zahldatum = reservation.zahldatum
                    res_listmain.depositbez2 =  to_decimal(reservation.depositbez2)
                    res_listmain.zahldatum2 = reservation.zahldatum2
                    res_listmain.useridanlage = reservation.useridanlage
                    res_listmain.mutdat = reservation.mutdat
                    res_listmain.useridmutat = reservation.useridmutat
                    res_listmain.gastnr = reservation.gastnr
                    res_listmain.bemerk = reservation.bemerk
                    res_listmain.grpflag = reservation.grpflag
                    res_listmain.activeflag = reservation.activeflag

                    guest = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                    if guest:
                        res_listmain.resname = guest.name + ", " + guest.vorname1 +\
                                guest.anredefirma + " " + guest.anrede1
                        res_listmain.address = guest.adresse1 + " " + guest.adresse2
                        res_listmain.city = guest.land + " " + guest.wohnort + " " +\
                                guest.plz

            reservation = get_cache (Reservation, {"resnr": [(eq, search_resno)],"activeflag": [(le, 1)]})

            if reservation:
                curr_select = "mainres"


    res_listmain_data.clear()
    res_listmember_data.clear()

    if case_type == 1:
        update_browse_b2()
    else:
        calc_br1()

    return generate_output()