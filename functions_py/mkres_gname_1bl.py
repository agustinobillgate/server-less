#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 21/10/2025
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import Htparam, Guest, Reservation, Zimkateg, Res_line, Segment, Guestseg

def mkres_gname_1bl(case_type:int, temp_flag:int, create_guestseg:bool, gastno:int, sorttype:int, famname:string, inp_compno:int, wiguestflag:bool, adult:int):

    prepare_cache ([Htparam, Guest, Reservation, Zimkateg, Res_line, Segment, Guestseg])

    guest_list_data = []
    resline_list_data = []
    fit_gastnr:int = 0
    htparam = guest = reservation = zimkateg = res_line = segment = guestseg = None

    resline_list = guest_list = None

    resline_list_data, Resline_list = create_model("Resline_list", {"ankunft":date, "abreise":date, "kurzbez":string, "zimmeranz":int, "zipreis":Decimal, "arrangement":string, "resnr":int, "reslinnr":int, "resstatus":int, "groupname":string, "bemerk":string, "active_flag":int})
    guest_list_data, Guest_list = create_model("Guest_list", {"firmen_nr":int, "steuernr":string, "full_name":string, "nation1":string, "wohnort":string, "land":string, "gastnr":int, "karteityp":int, "telefon":string, "overcredit":bool})

    db_session = local_storage.db_session

    famname = famname.strip()


    def generate_output():
        nonlocal guest_list_data, resline_list_data, fit_gastnr, htparam, guest, reservation, zimkateg, res_line, segment, guestseg
        nonlocal case_type, temp_flag, create_guestseg, gastno, sorttype, famname, inp_compno, wiguestflag, adult


        nonlocal resline_list, guest_list
        nonlocal resline_list_data, guest_list_data

        return {"adult": adult, "guest-list": guest_list_data, "resline-list": resline_list_data}

    def create_guest_list():

        nonlocal guest_list_data, resline_list_data, fit_gastnr, htparam, guest, reservation, zimkateg, res_line, segment, guestseg
        nonlocal case_type, temp_flag, create_guestseg, gastno, sorttype, famname, inp_compno, wiguestflag, adult


        nonlocal resline_list, guest_list
        nonlocal resline_list_data, guest_list_data

        if sorttype == 11:
            htparam = get_cache (Htparam, {"paramnr": [(eq, 123)]})
            fit_gastnr = htparam.finteger
            sorttype = 1

        if temp_flag <= 2:

            if famname == "":

                if wiguestflag:

                    htparam = get_cache (Htparam, {"paramnr": [(eq, 109)]})
                else:

                    htparam = get_cache (Htparam, {"paramnr": [(eq, 123)]})

                if htparam.finteger != 0:

                    guest = get_cache (Guest, {"gastnr": [(eq, htparam.finteger)]})

                    if guest:
                        assign_it()
            else:

                if substring(famname, 0, 1) != ("*").lower() :
                    famname = "*" + famname

                if substring(famname, length(famname) - 1) != ("*").lower() :
                    famname = famname + "*"

                for guest in db_session.query(Guest).filter(
                         (matches(Guest.name,famname)) & (Guest.gastnr > 0) & (Guest.karteityp == sorttype) & (Guest.gastnr != fit_gastnr)).order_by(Guest.name).all():
                    assign_it()

        elif temp_flag == 3:

            for guest in db_session.query(Guest).filter(
                     (Guest.gastnr > 0) & (Guest.karteityp == sorttype) & (Guest.firmen_nr >= inp_compno)).order_by(Guest.firmen_nr, Guest.name).all():
                assign_it()


        elif temp_flag == 4:

            for guest in db_session.query(Guest).filter(
                     (Guest.gastnr > 0) & (Guest.karteityp == sorttype) & (Guest.steuernr >= (famname).lower())).order_by(Guest.steuernr, Guest.name).all():
                assign_it()


        elif temp_flag == 5:

            for guest in db_session.query(Guest).filter(
                     (Guest.gastnr == gastno)).order_by(Guest._recid).all():
                assign_it()

    def assign_it():

        nonlocal guest_list_data, resline_list_data, fit_gastnr, htparam, guest, reservation, zimkateg, res_line, segment, guestseg
        nonlocal case_type, temp_flag, create_guestseg, gastno, sorttype, famname, inp_compno, wiguestflag, adult


        nonlocal resline_list, guest_list
        nonlocal resline_list_data, guest_list_data


        guest_list = Guest_list()
        guest_list_data.append(guest_list)

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

        nonlocal guest_list_data, resline_list_data, fit_gastnr, htparam, guest, reservation, zimkateg, res_line, segment, guestseg
        nonlocal case_type, temp_flag, create_guestseg, gastno, sorttype, famname, inp_compno, wiguestflag, adult


        nonlocal resline_list, guest_list
        nonlocal resline_list_data, guest_list_data

        res_line_obj_list = {}
        res_line = Res_line()
        reservation = Reservation()
        zimkateg = Zimkateg()
        for res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.arrangement, res_line.resnr, res_line.reslinnr, res_line.resstatus, res_line.bemerk, res_line.active_flag, res_line.zikatnr, res_line._recid, reservation.groupname, reservation._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.arrangement, Res_line.resnr, Res_line.reslinnr, Res_line.resstatus, Res_line.bemerk, Res_line.active_flag, Res_line.zikatnr, Res_line._recid, Reservation.groupname, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                 (Res_line.gastnr == gastno) & (Res_line.active_flag <= 1) & (Res_line.resstatus != 12)).order_by(Res_line.ankunft, Res_line.resnr, Res_line.resstatus).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            resline_list = Resline_list()
            resline_list_data.append(resline_list)

            resline_list.ankunft = res_line.ankunft
            resline_list.abreise = res_line.abreise
            resline_list.kurzbez = zimkateg.kurzbez
            resline_list.zimmeranz = res_line.zimmeranz
            resline_list.zipreis =  to_decimal(res_line.zipreis)
            resline_list.arrangement = res_line.arrangement
            resline_list.resnr = res_line.resnr
            resline_list.reslinnr = res_line.reslinnr
            resline_list.resstatus = res_line.resstatus
            resline_list.groupname = reservation.groupname
            resline_list.bemerk = res_line.bemerk
            resline_list.active_flag = res_line.active_flag


    def create_res_record():

        nonlocal guest_list_data, resline_list_data, fit_gastnr, htparam, guest, reservation, zimkateg, res_line, segment, guestseg
        nonlocal case_type, temp_flag, create_guestseg, gastno, sorttype, famname, inp_compno, wiguestflag, adult


        nonlocal resline_list, guest_list
        nonlocal resline_list_data, guest_list_data

        inp_resnr:int = 0
        inp_reslinnr:int = 0
        inp_resnr = to_int(entry(0, famname, ","))
        inp_reslinnr = to_int(entry(1, famname, ","))

        res_line = get_cache (Res_line, {"resnr": [(eq, inp_resnr)],"reslinnr": [(eq, inp_reslinnr)]})

        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})
        resline_list = Resline_list()
        resline_list_data.append(resline_list)

        resline_list.ankunft = res_line.ankunft
        resline_list.abreise = res_line.abreise
        resline_list.kurzbez = zimkateg.kurzbez
        resline_list.zimmeranz = res_line.zimmeranz
        resline_list.zipreis =  to_decimal(res_line.zipreis)
        resline_list.arrangement = res_line.arrangement
        resline_list.resnr = res_line.resnr
        resline_list.reslinnr = res_line.reslinnr
        resline_list.resstatus = res_line.resstatus
        resline_list.groupname = reservation.groupname
        resline_list.bemerk = res_line.bemerk
        resline_list.active_flag = res_line.active_flag


    def create_guestseg_proc():

        nonlocal guest_list_data, resline_list_data, fit_gastnr, htparam, guest, reservation, zimkateg, res_line, segment, guestseg
        nonlocal case_type, temp_flag, create_guestseg, gastno, sorttype, famname, inp_compno, wiguestflag, adult


        nonlocal resline_list, guest_list
        nonlocal resline_list_data, guest_list_data

        segment = get_cache (Segment, {"betriebsnr": [(eq, 0)]})

        guestseg = get_cache (Guestseg, {"gastnr": [(eq, gastno)],"reihenfolge": [(eq, 1)],"segmentcode": [(eq, segment.segmentcode)]})

        if not guestseg:
            guestseg = Guestseg()
            db_session.add(guestseg)

            guestseg.gastnr = gastno
            guestseg.reihenfolge = 1
            guestseg.segmentcode = segment.segmentcode


            pass
            pass

    htparam = get_cache (Htparam, {"paramnr": [(eq, 262)]})

    if htparam.finteger > 0:
        adult = htparam.finteger

    if create_guestseg:
        create_guestseg_proc()
    else:

        if case_type == 1:
            create_res_list()
        elif case_type == 2:
            create_guest_list()
        elif case_type == 3:
            create_res_record()

    return generate_output()

    return generate_output()