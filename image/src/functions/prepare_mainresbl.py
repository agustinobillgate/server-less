from functions.additional_functions import *
import decimal
from datetime import date
from models import Reservation, Res_line, Htparam, Brief, Guest, Guestseg, Queasy, Segment, Akt_kont, Sourccod, Master

def prepare_mainresbl(res_mode:str, user_init:str, origcode:str, gastnr:int, resnr:int, reslinnr:int):
    msg_str = ""
    f_mainres_list = []
    t_reservation_list = []
    ci_date:date = None
    confletter:int = 0
    curr_resart:int = 0
    reservation = res_line = htparam = brief = guest = guestseg = queasy = segment = akt_kont = sourccod = master = None

    t_reservation = f_mainres = rline = None

    t_reservation_list, T_reservation = create_model_like(Reservation)
    f_mainres_list, F_mainres = create_model("F_mainres", {"mainres_comment":str, "groupname":str, "main_voucher":str, "contact":str, "main_segm":str, "curr_segm":str, "curr_source":str, "letter":str, "rc_fname":str, "l_grpnr":int, "cutoff_days":int, "contact_nr":int, "curr_resart":int, "masterno":int, "rc_briefnr":int, "deposit":decimal, "depopay1":decimal, "depopay2":decimal, "depobalan":decimal, "cutoff_date":date, "limitdate":date, "paydate1":date, "paydate2":date, "init_fixrate":bool, "invno_flag":bool, "master_active":bool}, {"rc_fname": ""})

    Rline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, f_mainres_list, t_reservation_list, ci_date, confletter, curr_resart, reservation, res_line, htparam, brief, guest, guestseg, queasy, segment, akt_kont, sourccod, master
        nonlocal rline


        nonlocal t_reservation, f_mainres, rline
        nonlocal t_reservation_list, f_mainres_list
        return {"msg_str": msg_str, "f-mainres": f_mainres_list, "t-reservation": t_reservation_list}

    def prepare_mainres():

        nonlocal msg_str, f_mainres_list, t_reservation_list, ci_date, confletter, curr_resart, reservation, res_line, htparam, brief, guest, guestseg, queasy, segment, akt_kont, sourccod, master
        nonlocal rline


        nonlocal t_reservation, f_mainres, rline
        nonlocal t_reservation_list, f_mainres_list

        segmcode:str = ""

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 435)).first()
        f_mainres.rc_briefnr = htparam.finteger

        brief = db_session.query(Brief).filter(
                (Briefnr == briefnr)).first()

        if brief:
            f_mainres.rc_fname = brief.fname

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 440)).first()
        f_mainres.l_grpnr = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 264)).first()
        f_mainres.init_fixrate = htparam.flogical

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 391)).first()
        f_mainres.invno_flag = htparam.flogical

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 87)).first()
        ci_date = htparam.fdate

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == resnr)).first()
        t_reservation = T_reservation()
        t_reservation_list.append(t_reservation)

        buffer_copy(reservation, t_reservation)

        if reslinnr != 0:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()
        else:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == resnr) &  (Res_line.active_flag <= 1)).first()

        if res_mode.lower()  == "new" or res_mode.lower()  == "qci":

            reservation = db_session.query(Reservation).first()

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == gastnr)).first()

            guestseg = db_session.query(Guestseg).filter(
                    (Guestseg.gastnr == guest.gastnr) &  (Guestseg.reihenfolge == 1)).first()

            if not guestseg:

                guestseg = db_session.query(Guestseg).filter(
                        (Guestseg.gastnr == guest.gastnr)).first()
            reservation.gastnr = guest.gastnr
            reservation.gastnrherk = guest.gastnr
            reservation.useridanlage = user_init
            reservation.name = guest.name + ", " +\
                    guest.vorname1 + guest.anredefirma
            reservation.resart = 1
            reservation.resdat = ci_date
            reservation.insurance = f_mainres.init_fixrate

            if guest.segment3 != 0:
                reservation.resart = guest.segment3

            if guestseg:
                reservation.segmentcode = guestseg.segmentcode

        if res_mode.lower()  == "new" or res_mode.lower()  == "qci":

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 2) &  (Queasy.char1 == origcode)).first()

            if queasy and entry(0, queasy.char3, ";") != "":

                segment = db_session.query(Segment).filter(
                        (Segment.bezeich == entry(0, queasy.char3, ";"))).first()

                if segment:

                    rline = db_session.query(Rline).filter(
                            (Rline.resnr == resnr) &  (Rline.reslinnr != reslinnr) &  (Rline.zipreis > 0)).first()

                    if res_mode.lower()  == "modify" and not rline and res_line.gratis > 0 and res_line.erwachs == 0 and res_line.zipreis == 0:
                        pass

                    elif (res_mode == "modify" and rline) or (res_mode != "modify"):

                        reservation = db_session.query(Reservation).first()
                        reservation.segmentcode = segmentcode
        f_mainres.cutoff_days = reservation.point_resnr

        if f_mainres.cutoff_days != 0:
            f_mainres.cutoff_date = res_line.ankunft - f_mainres.cutoff_days
        f_mainres.mainres_comment = reservation.bemerk
        f_mainres.groupname = reservation.groupname
        f_mainres.contact_nr = reservation.kontakt_nr
        f_mainres.main_voucher = reservation.vesrdepot
        f_mainres.limitdate = reservation.limitdate
        f_mainres.deposit = reservation.depositgef
        f_mainres.depopay1 = reservation.depositbez
        f_mainres.depopay2 = reservation.depositbez2
        f_mainres.paydate1 = reservation.zahldatum
        f_mainres.paydate2 = reservation.zahldatum2
        f_mainres.depobalan = f_mainres.deposit - f_mainres.depopay1 -\
                f_mainres.depopay2

        if f_mainres.depopay1 == 0:
            f_mainres.paydate1 = None

        if f_mainres.depopay2 == 0:
            f_mainres.paydate2 = None

        if f_mainres.contact_nr != 0:

            akt_kont = db_session.query(Akt_kont).filter(
                    (Akt_kont.kontakt_nr == f_mainres.contact_nr) &  (Akt_kont.gastnr == gastnr)).first()

            if akt_kont:
                f_mainres.contact = akt_kont.name + ", " + akt_kont.vorname + chr(2) + akt_kont.telefon + chr(2) + akt_kont.durchwahl

        if reservation.segmentcode > 0:

            segment = db_session.query(Segment).filter(
                    (Segment.segmentcode == reservation.segmentcode)).first()
            segmcode = replace_str(segment.bezeich, ",", "/")
            f_mainres.curr_segm = to_string(segmentcode) +\
                    " " + segmcode + ";"

        guestseg_obj_list = []
        for guestseg, segment in db_session.query(Guestseg, Segment).join(Segment,(Segment.segmentcode == Guestseg.segmentcode) &  (Segment.betriebsnr <= 2) &  (num_entries(Segment.bezeich, "$$0") == 1)).filter(
                (Guestseg.gastnr == reservation.gastnr)).all():
            if guestseg._recid in guestseg_obj_list:
                continue
            else:
                guestseg_obj_list.append(guestseg._recid)

            if guestseg.segmentcode == reservation.segmentcode:
                1
            else:
                segmcode = replace_str(segment.bezeich, ",", "/")
                f_mainres.curr_segm = f_mainres.curr_segm +\
                    to_string(segmentcode) +\
                    " " + segmcode + ";"

            if guestseg.reihenfolge == 1:
                f_mainres.main_segm = to_string(segmentcode) + " " + segmcode

        for segment in db_session.query(Segment).filter(
                (Segment.betriebsnr <= 2) &  (Segmentcode != reservation.segmentcode) &  (num_entries(Segment.bezeich, "$$0") == 1)).all():

            guestseg = db_session.query(Guestseg).filter(
                    (Guestseg.gastnr == reservation.gastnr) &  (Guestseg.segmentcode == segmentcode)).first()

            if not guestseg:
                segmcode = replace_str(segment.bezeich, ",", "/")
                f_mainres.curr_segm = f_mainres.curr_segm +\
                    to_string(segmentcode) + " " + segmcode + ";"

        if reservation.resart != 0:

            sourccod = db_session.query(Sourccod).filter(
                    (Sourccod.source_code == reservation.resart) &  (Sourccod.betriebsnr == 0)).first()

            if not sourccod or (sourccod and sourccod.betriebsnr != 0):

                sourccod = db_session.query(Sourccod).filter(
                        (Sourccod.betriebsnr == 0)).first()

            if sourccod:
                curr_resart = sourccod.source_code
                f_mainres.curr_source = to_string(sourccod.source_code) +\
                        " " + sourccod.bezeich + ";"


                f_mainres.curr_resart = sourccod.source_code

        for sourccod in db_session.query(Sourccod).filter(
                (Sourccod.betriebsnr == 0) &  (Sourccod.source_code != curr_resart)).all():
            f_mainres.curr_source = f_mainres.curr_source + to_string(sourccod.source_code) + " " + sourccod.bezeich + ";"

        if reservation.briefnr != 0:

            brief = db_session.query(Brief).filter(
                    (Briefnr == reservation.briefnr)).first()

            if brief:
                f_mainres.letter = to_string(briefnr) + " " + briefbezeich + ";"
        else:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 431)).first()

            if htparam.feldtyp == 1:
                confletter = htparam.finteger

            brief = db_session.query(Brief).filter(
                    (Briefnr == confletter)).first()

            if brief:
                f_mainres.letter = to_string(briefnr) + " " + briefbezeich + ";"

        for brief in db_session.query(Brief).filter(
                (Briefkateg == l_grpnr) &  (Briefnr != reservation.briefnr) &  (Briefnr != confletter)).all():
            f_mainres.letter = f_mainres.letter + to_string(briefnr) + " " + briefbezeich + ";"

        master = db_session.query(Master).filter(
                (Master.resnr == resnr)).first()

        if master:
            f_mainres.master_active = master.ACTIVE
            f_mainres.masterno = master.rechnr

        reservation = db_session.query(Reservation).first()

    f_mainres = F_mainres()
    f_mainres_list.append(f_mainres)

    prepare_mainres()

    return generate_output()