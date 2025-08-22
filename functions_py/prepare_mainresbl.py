#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 13/8/2025
# num_entries
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Reservation, Res_line, Htparam, Brief, Guest, Guestseg, Queasy, Segment, Akt_kont, Sourccod, Master

def prepare_mainresbl(res_mode:string, user_init:string, origcode:string, gastnr:int, resnr:int, reslinnr:int):

    prepare_cache ([Res_line, Htparam, Brief, Guest, Guestseg, Queasy, Segment, Akt_kont, Sourccod, Master])

    msg_str = ""
    f_mainres_data = []
    t_reservation_data = []
    ci_date:date = None
    confletter:int = 0
    curr_resart:int = 0
    reservation = res_line = htparam = brief = guest = guestseg = queasy = segment = akt_kont = sourccod = master = None

    t_reservation = f_mainres = rline = None

    t_reservation_data, T_reservation = create_model_like(Reservation)
    f_mainres_data, F_mainres = create_model("F_mainres", {"mainres_comment":string, "groupname":string, "main_voucher":string, "contact":string, "main_segm":string, "curr_segm":string, "curr_source":string, "letter":string, "rc_fname":string, "l_grpnr":int, "cutoff_days":int, "contact_nr":int, "curr_resart":int, "masterno":int, "rc_briefnr":int, "deposit":Decimal, "depopay1":Decimal, "depopay2":Decimal, "depobalan":Decimal, "cutoff_date":date, "limitdate":date, "paydate1":date, "paydate2":date, "init_fixrate":bool, "invno_flag":bool, "master_active":bool}, {"rc_fname": ""})

    Rline = create_buffer("Rline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, f_mainres_data, t_reservation_data, ci_date, confletter, curr_resart, reservation, res_line, htparam, brief, guest, guestseg, queasy, segment, akt_kont, sourccod, master
        nonlocal res_mode, user_init, origcode, gastnr, resnr, reslinnr
        nonlocal rline


        nonlocal t_reservation, f_mainres, rline
        nonlocal t_reservation_data, f_mainres_data

        return {"msg_str": msg_str, "f-mainres": f_mainres_data, "t-reservation": t_reservation_data}

    def prepare_mainres():

        nonlocal msg_str, f_mainres_data, t_reservation_data, ci_date, confletter, curr_resart, reservation, res_line, htparam, brief, guest, guestseg, queasy, segment, akt_kont, sourccod, master
        nonlocal res_mode, user_init, origcode, gastnr, resnr, reslinnr
        nonlocal rline


        nonlocal t_reservation, f_mainres, rline
        nonlocal t_reservation_data, f_mainres_data

        segmcode:string = ""

        htparam = get_cache (Htparam, {"paramnr": [(eq, 435)]})
        f_mainres.rc_briefnr = htparam.finteger

        brief = get_cache (Brief, {"briefnr": [(eq, f_mainres.rc_briefnr)]})

        if brief:
            f_mainres.rc_fname = brief.fname

        htparam = get_cache (Htparam, {"paramnr": [(eq, 440)]})
        f_mainres.l_grpnr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 264)]})
        f_mainres.init_fixrate = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 391)]})
        f_mainres.invno_flag = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
        ci_date = htparam.fdate

        reservation = get_cache (Reservation, {"resnr": [(eq, resnr)]})

        if not reservation:

            return
        t_reservation = T_reservation()
        t_reservation_data.append(t_reservation)

        buffer_copy(reservation, t_reservation)

        if reslinnr != 0:

            res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})
        else:

            res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"active_flag": [(le, 1)]})

        if res_mode.lower()  == ("new").lower()  or res_mode.lower()  == ("qci").lower() :
            pass

            guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

            guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)],"reihenfolge": [(eq, 1)]})

            if not guestseg:

                guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)]})
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

        if res_mode.lower()  == ("new").lower()  or res_mode.lower()  == ("qci").lower() :

            queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, origcode)]})

            if queasy and entry(0, queasy.char3, ";") != "":

                segment = get_cache (Segment, {"bezeich": [(eq, entry(0, queasy.char3, ";"))]})

                if segment:

                    rline = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(ne, reslinnr)],"zipreis": [(gt, 0)]})

                    if res_mode.lower()  == ("modify").lower()  and not rline and res_line.gratis > 0 and res_line.erwachs == 0 and res_line.zipreis == 0:
                        pass

                    elif (res_mode.lower()  == ("modify").lower()  and rline) or (res_mode.lower()  != ("modify").lower() ):
                        pass
                        reservation.segmentcode = segment.segmentcode
        f_mainres.cutoff_days = reservation.point_resnr

        if f_mainres.cutoff_days != 0:
            f_mainres.cutoff_date = res_line.ankunft - timedelta(days=f_mainres.cutoff_days)
        f_mainres.mainres_comment = reservation.bemerk
        f_mainres.groupname = reservation.groupname
        f_mainres.contact_nr = reservation.kontakt_nr
        f_mainres.main_voucher = reservation.vesrdepot
        f_mainres.limitdate = reservation.limitdate
        f_mainres.deposit =  to_decimal(reservation.depositgef)
        f_mainres.depopay1 =  to_decimal(reservation.depositbez)
        f_mainres.depopay2 =  to_decimal(reservation.depositbez2)
        f_mainres.paydate1 = reservation.zahldatum
        f_mainres.paydate2 = reservation.zahldatum2
        f_mainres.depobalan =  to_decimal(f_mainres.deposit) - to_decimal(f_mainres.depopay1) -\
                f_mainres.depopay2

        if f_mainres.depopay1 == 0:
            f_mainres.paydate1 = None

        if f_mainres.depopay2 == 0:
            f_mainres.paydate2 = None

        if f_mainres.contact_nr != 0:

            akt_kont = get_cache (Akt_kont, {"kontakt_nr": [(eq, f_mainres.contact_nr)],"gastnr": [(eq, gastnr)]})

            if akt_kont:
                f_mainres.contact = akt_kont.name + ", " + akt_kont.vorname + chr_unicode(2) + akt_kont.telefon + chr_unicode(2) + akt_kont.durchwahl

        if reservation.segmentcode > 0:

            segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
            segmcode = replace_str(segment.bezeich, ",", "/")
            f_mainres.curr_segm = to_string(segment.segmentcode) +\
                    " " + segmcode + ";"

        guestseg_obj_list = {}
        guestseg = Guestseg()
        segment = Segment()
        for guestseg.segmentcode, guestseg.reihenfolge, guestseg._recid, segment.segmentcode, segment.bezeich, segment._recid in \
            db_session.query(Guestseg.segmentcode, Guestseg.reihenfolge, Guestseg._recid, Segment.segmentcode, Segment.bezeich, Segment._recid) \
                    .join(Segment,(Segment.segmentcode == Guestseg.segmentcode) & 
                          (Segment.betriebsnr <= 2) & 
                          (num_entries(Segment.bezeich, "$$0") == 1)) \
                        .filter(
                            (Guestseg.gastnr == reservation.gastnr))\
                        .order_by(Segment.betriebsnr, Segment.segmentcode).all():
            
            if guestseg_obj_list.get(guestseg._recid):
                continue
            else:
                guestseg_obj_list[guestseg._recid] = True

            if guestseg.segmentcode == reservation.segmentcode:
                pass
            else:
                segmcode = replace_str(segment.bezeich, ",", "/")
                f_mainres.curr_segm = f_mainres.curr_segm +\
                    to_string(segment.segmentcode) +\
                    " " + segmcode + ";"

            if guestseg.reihenfolge == 1:
                f_mainres.main_segm = to_string(segment.segmentcode) + " " + segmcode

        # Rd, 13/8/2025
        # for segment in db_session.query(Segment).filter(
        #          (Segment.betriebsnr <= 2) & (Segment.segmentcode != reservation.segmentcode) & (num_entries(Segment.bezeich, "$$0") == 1)).order_by(Segment.betriebsnr, Segment.segmentcode).all():
        for segment in db_session.query(Segment).filter(
                 (Segment.betriebsnr <= 2) & (Segment.segmentcode != reservation.segmentcode) ).order_by(Segment.betriebsnr, Segment.segmentcode).all():
            if (num_entries(segment.bezeich, "$$0") == 1):
                guestseg = get_cache (Guestseg, {"gastnr": [(eq, reservation.gastnr)],"segmentcode": [(eq, segment.segmentcode)]})

                if not guestseg:
                    segmcode = replace_str(segment.bezeich, ",", "/")
                    f_mainres.curr_segm = f_mainres.curr_segm +\
                        to_string(segment.segmentcode) + " " + segmcode + ";"

        if reservation.resart != 0:

            sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)],"betriebsnr": [(eq, 0)]})

            if not sourccod or (sourccod and sourccod.betriebsnr != 0):

                sourccod = get_cache (Sourccod, {"betriebsnr": [(eq, 0)]})

            if sourccod:
                curr_resart = sourccod.source_code
                f_mainres.curr_source = to_string(sourccod.source_code) +\
                        " " + sourccod.bezeich + ";"


                f_mainres.curr_resart = sourccod.source_code

        for sourccod in db_session.query(Sourccod).filter(
                 (Sourccod.betriebsnr == 0) & (Sourccod.source_code != curr_resart)).order_by(Sourccod.source_code).all():
            f_mainres.curr_source = f_mainres.curr_source + to_string(sourccod.source_code) + " " + sourccod.bezeich + ";"

        if reservation.briefnr != 0:

            brief = get_cache (Brief, {"briefnr": [(eq, reservation.briefnr)]})

            if brief:
                f_mainres.letter = to_string(brief.briefnr) + " " + brief.briefbezeich + ";"
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 431)]})

            if htparam.feldtyp == 1:
                confletter = htparam.finteger

            brief = get_cache (Brief, {"briefnr": [(eq, confletter)]})

            if brief:
                f_mainres.letter = to_string(brief.briefnr) + " " + brief.briefbezeich + ";"

        for brief in db_session.query(Brief).filter(
                 (Brief.briefkateg == f_mainres.l_grpnr) & (Brief.briefnr != reservation.briefnr) & (Brief.briefnr != confletter)).order_by(Brief.briefnr).all():
            f_mainres.letter = f_mainres.letter + to_string(brief.briefnr) + " " + brief.briefbezeich + ";"

        master = get_cache (Master, {"resnr": [(eq, resnr)]})

        if master:
            f_mainres.master_active = master.active
            f_mainres.masterno = master.rechnr


        pass


    f_mainres = F_mainres()
    f_mainres_data.append(f_mainres)

    prepare_mainres()

    return generate_output()