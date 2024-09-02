from functions.additional_functions import *
import decimal
from datetime import date
from functions.check_timebl import check_timebl
from sqlalchemy import func
from models import Reservation, Master, Htparam, Bediener, Guest, Guestseg, Res_line, Akt_kont, Segment, Sourccod, Brief

def prepare_mk_mainresbl(gastnr:int, resnr:int, res_mode:str, user_init:str, grpflag:bool):
    record_use = False
    init_time = 0
    init_date = None
    bill_receiver = ""
    f_mainres_list = []
    t_reservation_list = []
    t_master_list = []
    flag_ok:bool = False
    reservation = master = htparam = bediener = guest = guestseg = res_line = akt_kont = segment = sourccod = brief = None

    t_reservation = t_master = f_mainres = None

    t_reservation_list, T_reservation = create_model_like(Reservation)
    t_master_list, T_master = create_model_like(Master)
    f_mainres_list, F_mainres = create_model("F_mainres", {"groupname":str, "comments":str, "voucherno":str, "contact":str, "origin":str, "ta_comm":str, "segmstr":str, "resart_str":str, "letter_str":str, "bill_receiver":str, "fixrate_flag":bool, "fixed_rate":bool, "invno_flag":bool, "double_currency":bool, "deposit_readonly":bool, "deposit_disabled":bool, "master_exist":bool, "umsatz1":bool, "umsatz3":bool, "umsatz4":bool, "karteityp":int, "gastnrherk":int, "gastnrcom":int, "gastnrpay":int, "l_grpnr":int, "resart":int, "letterno":int, "contact_nr":int, "curr_segm":int, "ci_date":date, "limitdate":date, "cutoff_date":date, "res_ankunft":date, "depositgef":decimal, "depositres":decimal}, {"limitdate": None, "cutoff_date": None, "res_ankunft": None})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal record_use, init_time, init_date, bill_receiver, f_mainres_list, t_reservation_list, t_master_list, flag_ok, reservation, master, htparam, bediener, guest, guestseg, res_line, akt_kont, segment, sourccod, brief


        nonlocal t_reservation, t_master, f_mainres
        nonlocal t_reservation_list, t_master_list, f_mainres_list
        return {"record_use": record_use, "init_time": init_time, "init_date": init_date, "bill_receiver": bill_receiver, "f-mainres": f_mainres_list, "t-reservation": t_reservation_list, "t-master": t_master_list}


    flag_ok, init_time, init_date = get_output(check_timebl(1, resnr, None, "reservation", None, None))

    if not flag_ok:
        record_use = True

        return generate_output()
    f_mainres = F_mainres()
    f_mainres_list.append(f_mainres)


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 264)).first()
    f_mainres.fixrate_flag = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    f_mainres.ci_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 391)).first()
    f_mainres.invno_flag = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 440)).first()
    f_mainres.l_grpnr = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()
    f_mainres.double_currency = htparam.flogical

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastnr)).first()

    reservation = db_session.query(Reservation).filter(
            (Reservation.resnr == resnr)).first()

    if res_mode.lower()  == "New":
        reservation.insurance = f_mainres.fixrate_flag

    if f_mainres.fixrate_flag:
        f_mainres.fixed_rate = f_mainres.fixrate_flag
    else:
        f_mainres.fixed_rate = reservation.insurance

    if res_mode.lower()  == "new":

        guestseg = db_session.query(Guestseg).filter(
                (Guestseg.gastnr == guest.gastnr) &  (Guestseg.reihenfolge == 1)).first()

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

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == reservation.resnr) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10)).first()

    if res_line:
        f_mainres.cutoff_date = res_line.ankunft - reservation.point_resnr
        f_mainres.res_ankunft = res_line.ankunft


    f_mainres.groupname = reservation.groupname
    f_mainres.resart = reservation.resart
    f_mainres.limitdate = reservation.limitdate
    f_mainres.depositgef = reservation.depositgef
    f_mainres.gastnrherk = reservation.gastnrherk
    f_mainres.gastnrcom = reservation.guestnrcom[0]
    f_mainres.comments = reservation.bemerk
    f_mainres.letterno = reservation.briefnr
    f_mainres.voucherno = reservation.vesrdepot

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == reservation.gastnrherk)).first()

    if not guest:
        f_mainres.gastnrherk = reservation.gastnr

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == f_mainres.gastnrherk)).first()
    f_mainres.origin = guest.name + ", " + guest.vorname1 +\
            guest.anredefirma
    f_mainres.karteityp = guest.karteityp

    if reservation.kontakt_nr != 0:

        akt_kont = db_session.query(Akt_kont).filter(
                (Akt_kont.gastnr == reservation.gastnr) &  (Akt_kont.kontakt_nr == reservation.kontakt_nr)).first()

        if akt_kont:
            f_mainres.contact = akt_kont.name + ", " + akt_kont.vorname
            f_mainres.contact_nr = akt_kont.kontakt_nr

    if reservation.guestnrcom[0] > 0:

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == reservation.guestnrcom[0])).first()
        f_mainres.ta_comm = guest.name + ", " + guest.vorname1 +\
                guest.anredefirma

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastnr)).first()

    segment = db_session.query(Segment).filter(
            (Segment.segmentcode == reservation.segmentcode)).first()

    if segment:
        f_mainres.curr_segm = segmentcode
        f_mainres.segmstr = entry(0, segment.bezeich, "$$0")


    f_mainres.depositres = reservation.depositgef -\
            reservation.depositbez - reservation.depositbez2

    sourccod = db_session.query(Sourccod).filter(
            (Sourccod.source_code == f_mainres.resart)).first()

    if sourccod:
        f_mainres.resart_str = sourccod.bezeich

    brief = db_session.query(Brief).filter(
            (Briefkateg == f_mainres.l_grpnr) &  (Briefnr == f_mainres.letterno)).first()

    if brief:
        f_mainres.letter_str = briefbezeich

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == reservation.resnr) &  ((Res_line.resstatus == 6) |  (Res_line.resstatus == 8) |  (Res_line.resstatus == 3))).first()

    if res_line:
        f_mainres.deposit_readonly = True
        f_mainres.deposit_disabled = True

    elif reservation.depositgef > 0 and depositres == 0:
        f_mainres.deposit_disabled = True

    master = db_session.query(Master).filter(
            (Master.resnr == reservation.resnr)).first()

    if master:

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == master.gastnrpay)).first()
        f_mainres.master_exist = True
        f_mainres.gastnrpay = master.gastnrpay
        f_mainres.umsatz1 = master.umsatzart[0]
        f_mainres.umsatz3 = master.umsatzart[2]
        f_mainres.umsatz4 = master.umsatzart[3]
        f_mainres.bill_receiver = guest.name + ", " + guest.vorname1 +\
                " " + guest.anrede1 + guest.anredefirma


    t_reservation = T_reservation()
    t_reservation_list.append(t_reservation)

    buffer_copy(reservation, t_reservation)

    master = db_session.query(Master).filter(
            (Master.resnr == resnr)).first()

    if master:
        t_master = T_master()
        t_master_list.append(t_master)

        buffer_copy(master, t_master)

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == master.gastnrpay)).first()
        bill_receiver = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

    return generate_output()