from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Htparam, Guest, Reservation, Zimkateg, Res_line, Segment, Guestseg

def mkres_gname_1bl(case_type:int, temp_flag:int, create_guestseg:bool, gastno:int, sorttype:int, famname:str, inp_compno:int, wiguestflag:bool, adult:int):
    guest_list_list = []
    resline_list_list = []
    fit_gastnr:int = 0
    htparam = guest = reservation = zimkateg = res_line = segment = guestseg = None

    resline_list = guest_list = None

    resline_list_list, Resline_list = create_model("Resline_list", {"ankunft":date, "abreise":date, "kurzbez":str, "zimmeranz":int, "zipreis":decimal, "arrangement":str, "resnr":int, "reslinnr":int, "resstatus":int, "groupname":str, "bemerk":str, "active_flag":int})
    guest_list_list, Guest_list = create_model("Guest_list", {"firmen_nr":int, "steuernr":str, "full_name":str, "nation1":str, "wohnort":str, "land":str, "gastnr":int, "karteityp":int, "telefon":str, "overcredit":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest_list_list, resline_list_list, fit_gastnr, htparam, guest, reservation, zimkateg, res_line, segment, guestseg


        nonlocal resline_list, guest_list
        nonlocal resline_list_list, guest_list_list
        return {"guest-list": guest_list_list, "resline-list": resline_list_list}

    def create_guest_list():

        nonlocal guest_list_list, resline_list_list, fit_gastnr, htparam, guest, reservation, zimkateg, res_line, segment, guestseg


        nonlocal resline_list, guest_list
        nonlocal resline_list_list, guest_list_list

        if sorttype == 11:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 123)).first()
            fit_gastnr = htparam.finteger
            sorttype = 1

        if temp_flag <= 2:

            if famname == "":

                if wiguestflag:

                    htparam = db_session.query(Htparam).filter(
                            (Htparam.paramnr == 109)).first()
                else:

                    htparam = db_session.query(Htparam).filter(
                            (Htparam.paramnr == 123)).first()

                if htparam.finteger != 0:

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == htparam.finteger)).first()

                    if guest:
                        assign_it()
            else:

                if substring(famname, 0, 1) != "*":
                    famname = "*" + famname

                if substring(famname, len(famname) - 1) != "*":
                    famname = famname + "*"

                for guest in db_session.query(Guest).filter(
                        (Guest.name.op("~")(famname)) &  (Guest.gastnr > 0) &  (Guest.karteityp == sorttype) &  (Guest.gastnr != fit_gastnr)).all():
                    assign_it()

        elif temp_flag == 3:

            for guest in db_session.query(Guest).filter(
                    (Guest.gastnr > 0) &  (Guest.karteityp == sorttype) &  (Guest.firmen_nr >= inp_compno)).all():
                assign_it()


        elif temp_flag == 4:

            for guest in db_session.query(Guest).filter(
                    (Guest.gastnr > 0) &  (Guest.karteityp == sorttype) &  (func.lower(Guest.steuernr) >= (famname).lower())).all():
                assign_it()


        elif temp_flag == 5:

            for guest in db_session.query(Guest).filter(
                    (Guest.gastnr == gastno)).all():
                assign_it()


    def assign_it():

        nonlocal guest_list_list, resline_list_list, fit_gastnr, htparam, guest, reservation, zimkateg, res_line, segment, guestseg


        nonlocal resline_list, guest_list
        nonlocal resline_list_list, guest_list_list


        guest_list = Guest_list()
        guest_list_list.append(guest_list)

        guest_list.firmen_nr = guest.firmen_nr
        guest_list.steuernr = guest.steuernr
        guest_list.full_name = trim(guest.name + "," + guest.vorname1 + ", " + guest.anrede1)
        guest_list.nation1 = guest.nation1
        guest_list.wohnort = guest.wohnort
        guest_list.land = guest.land
        guest_list.gastnr = guest.gastnr
        guest_list.karteityp = guest.karteityp
        guest_list.telefon = guest.telefon

    def create_res_list():

        nonlocal guest_list_list, resline_list_list, fit_gastnr, htparam, guest, reservation, zimkateg, res_line, segment, guestseg


        nonlocal resline_list, guest_list
        nonlocal resline_list_list, guest_list_list

        res_line_obj_list = []
        for res_line, reservation, zimkateg in db_session.query(Res_line, Reservation, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                (Res_line.gastnr == gastno) &  (Res_line.active_flag <= 1) &  (Res_line.resstatus != 12)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            resline_list = Resline_list()
            resline_list_list.append(resline_list)

            resline_list.ankunft = res_line.ankunft
            resline_list.abreise = res_line.abreise
            resline_list.kurzbez = zimkateg.kurzbez
            resline_list.zimmeranz = res_line.zimmeranz
            resline_list.zipreis = res_line.zipreis
            resline_list.arrangement = res_line.arrangement
            resline_list.resnr = res_line.resnr
            resline_list.reslinnr = res_line.reslinnr
            resline_list.resstatus = res_line.resstatus
            resline_list.groupname = reservation.groupname
            resline_list.bemerk = res_line.bemerk
            resline_list.active_flag = res_line.active_flag

    def create_res_record():

        nonlocal guest_list_list, resline_list_list, fit_gastnr, htparam, guest, reservation, zimkateg, res_line, segment, guestseg


        nonlocal resline_list, guest_list
        nonlocal resline_list_list, guest_list_list

        inp_resnr:int = 0
        inp_reslinnr:int = 0
        inp_resnr = to_int(entry(0, famname, ","))
        inp_reslinnr = to_int(entry(1, famname, ","))

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == inp_resnr) &  (Res_line.reslinnr == inp_reslinnr)).first()

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == res_line.resnr)).first()

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.zikatnr == res_line.zikatnr)).first()
        resline_list = Resline_list()
        resline_list_list.append(resline_list)

        resline_list.ankunft = res_line.ankunft
        resline_list.abreise = res_line.abreise
        resline_list.kurzbez = zimkateg.kurzbez
        resline_list.zimmeranz = res_line.zimmeranz
        resline_list.zipreis = res_line.zipreis
        resline_list.arrangement = res_line.arrangement
        resline_list.resnr = res_line.resnr
        resline_list.reslinnr = res_line.reslinnr
        resline_list.resstatus = res_line.resstatus
        resline_list.groupname = reservation.groupname
        resline_list.bemerk = res_line.bemerk
        resline_list.active_flag = res_line.active_flag

    def create_guestseg():

        nonlocal guest_list_list, resline_list_list, fit_gastnr, htparam, guest, reservation, zimkateg, res_line, segment, guestseg


        nonlocal resline_list, guest_list
        nonlocal resline_list_list, guest_list_list

        segment = db_session.query(Segment).filter(
                (Segment.betriebsnr == 0)).first()

        guestseg = db_session.query(Guestseg).filter(
                (Guestseg.gastnr == gastno) &  (Guestseg.reihenfolge == 1) &  (Guestseg.segmentcode == segmentcode)).first()

        if not guestseg:
            guestseg = Guestseg()
            db_session.add(guestseg)

            guestseg.gastnr = gastno
            guestseg.reihenfolge = 1
            guestseg.segmentcode = segmentcode

            guestseg = db_session.query(Guestseg).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 262)).first()

    if htparam.finteger > 0:
        adult = htparam.finteger

    if create_guestseg:
        create_guestseg()
    else:

        if case_type == 1:
            create_res_list()
        elif case_type == 2:
            create_guest_list()
        elif case_type == 3:
            create_res_record()

    return generate_output()