#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 26/11/2025, with_for_update
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.check_timebl import check_timebl
from models import Reservation, Master, Htparam, Bediener, Guest, Guestseg, Res_line, Akt_kont, Segment, Sourccod, Brief

def prepare_mk_mainresbl(gastnr:int, resnr:int, res_mode:string, user_init:string, grpflag:bool):

    prepare_cache ([Htparam, Guest, Guestseg, Res_line, Akt_kont, Segment, Sourccod, Brief])

    record_use = False
    init_time = 0
    init_date = None
    bill_receiver = ""
    f_mainres_data = []
    t_reservation_data = []
    t_master_data = []
    flag_ok:bool = False
    reservation = master = htparam = bediener = guest = guestseg = res_line = akt_kont = segment = sourccod = brief = None

    t_reservation = t_master = f_mainres = None

    t_reservation_data, T_reservation = create_model_like(Reservation)
    t_master_data, T_master = create_model_like(Master)
    f_mainres_data, F_mainres = create_model("F_mainres", {"groupname":string, "comments":string, "voucherno":string, "contact":string, "origin":string, "ta_comm":string, "segmstr":string, "resart_str":string, "letter_str":string, "bill_receiver":string, "fixrate_flag":bool, "fixed_rate":bool, "invno_flag":bool, "double_currency":bool, "deposit_readonly":bool, "deposit_disabled":bool, "master_exist":bool, "umsatz1":bool, "umsatz3":bool, "umsatz4":bool, "karteityp":int, "gastnrherk":int, "gastnrcom":int, "gastnrpay":int, "l_grpnr":int, "resart":int, "letterno":int, "contact_nr":int, "curr_segm":int, "ci_date":date, "limitdate":date, "cutoff_date":date, "res_ankunft":date, "depositgef":Decimal, "depositres":Decimal}, {"limitdate": None, "cutoff_date": None, "res_ankunft": None})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal record_use, init_time, init_date, bill_receiver, f_mainres_data, t_reservation_data, t_master_data, flag_ok, reservation, master, htparam, bediener, guest, guestseg, res_line, akt_kont, segment, sourccod, brief
        nonlocal gastnr, resnr, res_mode, user_init, grpflag


        nonlocal t_reservation, t_master, f_mainres
        nonlocal t_reservation_data, t_master_data, f_mainres_data

        return {"record_use": record_use, "init_time": init_time, "init_date": init_date, "bill_receiver": bill_receiver, "f-mainres": f_mainres_data, "t-reservation": t_reservation_data, "t-master": t_master_data}


    flag_ok, init_time, init_date = get_output(check_timebl(1, resnr, None, "reservation", None, None))

    if not flag_ok:
        record_use = True

        return generate_output()
    f_mainres = F_mainres()
    f_mainres_data.append(f_mainres)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 264)]})
    f_mainres.fixrate_flag = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    f_mainres.ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 391)]})
    f_mainres.invno_flag = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 440)]})
    f_mainres.l_grpnr = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    f_mainres.double_currency = htparam.flogical

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

    # reservation = get_cache (Reservation, {"resnr": [(eq, resnr)]})
    reservation = db_session.query(Reservation).filter(
                 (Reservation.resnr == resnr)).with_for_update().first()

    if reservation:
        pass

        if res_mode.lower()  == ("New").lower() :
            reservation.insurance = f_mainres.fixrate_flag

        if f_mainres.fixrate_flag:
            f_mainres.fixed_rate = f_mainres.fixrate_flag
        else:
            f_mainres.fixed_rate = reservation.insurance

        if res_mode.lower()  == ("new").lower() :

            guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)],"reihenfolge": [(eq, 1)]})

            if guestseg:
                reservation.segmentcode = guestseg.segmentcode
            reservation.gastnr = guest.gastnr
            reservation.gastnrherk = guest.gastnr
            reservation.useridanlage = user_init
            reservation.name = guest.name + ", " +\
                    guest.vorname1 + guest.anredefirma
            reservation.grpflag = grpflag
            reservation.resart = 1
            reservation.resdat = f_mainres.ci_date


        pass

        res_line = get_cache (Res_line, {"resnr": [(eq, reservation.resnr)],"resstatus": [(ne, 9),(ne, 10)]})

        if res_line:
            f_mainres.cutoff_date = res_line.ankunft - timedelta(days=reservation.point_resnr)
            f_mainres.res_ankunft = res_line.ankunft


        f_mainres.groupname = reservation.groupname
        f_mainres.resart = reservation.resart
        f_mainres.limitdate = reservation.limitdate
        f_mainres.depositgef =  to_decimal(reservation.depositgef)
        f_mainres.gastnrherk = reservation.gastnrherk
        f_mainres.gastnrcom = reservation.guestnrcom[0]
        f_mainres.comments = reservation.bemerk
        f_mainres.letterno = reservation.briefnr
        f_mainres.voucherno = reservation.vesrdepot

        guest = get_cache (Guest, {"gastnr": [(eq, reservation.gastnrherk)]})

        if not guest:
            f_mainres.gastnrherk = reservation.gastnr

            guest = get_cache (Guest, {"gastnr": [(eq, f_mainres.gastnrherk)]})
        f_mainres.origin = guest.name + ", " + guest.vorname1 +\
                guest.anredefirma
        f_mainres.karteityp = guest.karteityp

        if reservation.kontakt_nr != 0:

            akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, reservation.gastnr)],"kontakt_nr": [(eq, reservation.kontakt_nr)]})

            if akt_kont:
                f_mainres.contact = akt_kont.name + ", " + akt_kont.vorname
                f_mainres.contact_nr = akt_kont.kontakt_nr

        if reservation.guestnrcom[0] > 0:

            guest = get_cache (Guest, {"gastnr": [(eq, reservation.guestnrcom[0])]})
            f_mainres.ta_comm = guest.name + ", " + guest.vorname1 +\
                    guest.anredefirma

        guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

        if segment:
            f_mainres.curr_segm = segment.segmentcode
            f_mainres.segmstr = entry(0, segment.bezeich, "$$0")


        f_mainres.depositres =  to_decimal(reservation.depositgef) -\
                reservation.depositbez - to_decimal(reservation.depositbez2)

        sourccod = get_cache (Sourccod, {"source_code": [(eq, f_mainres.resart)]})

        if sourccod:
            f_mainres.resart_str = sourccod.bezeich

        brief = get_cache (Brief, {"briefkateg": [(eq, f_mainres.l_grpnr)],"briefnr": [(eq, f_mainres.letterno)]})

        if brief:
            f_mainres.letter_str = brief.briefbezeich

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == reservation.resnr) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 8) | (Res_line.resstatus == 3))).first()

        if res_line:
            f_mainres.deposit_readonly = True
            f_mainres.deposit_disabled = True

        elif reservation.depositgef > 0 and f_mainres.depositres == 0:
            f_mainres.deposit_disabled = True

        master = get_cache (Master, {"resnr": [(eq, reservation.resnr)]})

        if master:

            guest = get_cache (Guest, {"gastnr": [(eq, master.gastnrpay)]})
            f_mainres.master_exist = True
            f_mainres.gastnrpay = master.gastnrpay
            f_mainres.umsatz1 = master.umsatzart[0]
            f_mainres.umsatz3 = master.umsatzart[2]
            f_mainres.umsatz4 = master.umsatzart[3]
            f_mainres.bill_receiver = guest.name + ", " + guest.vorname1 +\
                    " " + guest.anrede1 + guest.anredefirma


        t_reservation = T_reservation()
        t_reservation_data.append(t_reservation)

        buffer_copy(reservation, t_reservation)

        master = get_cache (Master, {"resnr": [(eq, resnr)]})

        if master:
            t_master = T_master()
            t_master_data.append(t_master)

            buffer_copy(master, t_master)

            guest = get_cache (Guest, {"gastnr": [(eq, master.gastnrpay)]})
            bill_receiver = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
        pass

    return generate_output()