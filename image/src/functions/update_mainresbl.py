from functions.additional_functions import *
import decimal
from datetime import date
from models import Res_line, Guest, Reservation, Master, Brief, Segment, Sourccod, Bill, Counters, Htparam, Waehrung

def update_mainresbl(pvilanguage:int, res_mode:str, user_init:str, mr_comment:str, letter:str, curr_segm:str, curr_source:str, groupname:str, m_voucher:str, limitdate:date, deposit:decimal, contact_nr:int, cutoff_days:int, resno:int, gastno:int, l_grpnr:int, fixrateflag:bool):
    msg_str = ""
    lvcarea:str = "mk_resline"
    res_line = guest = reservation = master = brief = segment = sourccod = bill = counters = htparam = waehrung = None

    rline = rgast = None

    Rline = Res_line
    Rgast = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, res_line, guest, reservation, master, brief, segment, sourccod, bill, counters, htparam, waehrung
        nonlocal rline, rgast


        nonlocal rline, rgast
        return {"msg_str": msg_str}

    def update_mainres():

        nonlocal msg_str, lvcarea, res_line, guest, reservation, master, brief, segment, sourccod, bill, counters, htparam, waehrung
        nonlocal rline, rgast


        nonlocal rline, rgast

        ct:str = ""
        answer:bool = True
        Rline = Res_line
        Rgast = Guest

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == resno)).first()

        rgast = db_session.query(Rgast).filter(
                (Rgast.gastnr == gastno)).first()

        master = db_session.query(Master).filter(
                (Master.resnr == resno)).first()

        if master and master.active:
            reservation.verstat = 1
        else:
            reservation.verstat = 0

        if res_mode.lower()  == "new":
            reservation.useridanlage = user_init
        reservation.bemerk = mr_comment


        ct = letter

        brief = db_session.query(Brief).filter(
                (Briefkateg == l_grpnr) &  (Briefnr == to_int(substring(ct, 0,1 + get_index(ct, " "))))).first()

        if brief:
            reservation.briefnr = briefnr
        else:
            reservation.briefnr = 0
        ct = curr_segm

        segment = db_session.query(Segment).filter(
                (Segment.segmentcode == to_int(substring(ct, 0,1 + get_index(ct, " "))))).first()

        if segment:
            reservation.segmentcode = segmentcode
        ct = curr_source

        sourccod = db_session.query(Sourccod).filter(
                (Sourccod.source_code == to_int(substring(ct, 0,1 + get_index(ct, " "))))).first()

        if sourccod:
            reservation.resart = sourccod.source_code
        reservation.groupname = groupname
        reservation.grpflag = (groupname != "")
        reservation.limitdate = limitdate
        reservation.depositgef = deposit
        reservation.vesrdepot = m_voucher
        reservation.kontakt_nr = contact_nr
        reservation.point_resnr = cutoff_days

        if (reservation.insurance and not fixrateflag) or (not reservation.insurance and fixrateflag):
            reservation.insurance = fixrateflag


            resline_reserve_dec()

        if master:

            master = db_session.query(Master).first()

            if not master.active:

                bill = db_session.query(Bill).filter(
                        (Bill.resnr == resno) &  (Bill.reslinnr == 0)).first()

                if bill and bill.saldo != 0:
                    master.active = True

            master = db_session.query(Master).first()

            if master.active:
                reservation.verstat = 1
            else:
                reservation.verstat = 0

            rline = db_session.query(Rline).filter(
                    (Rline.resnr == master.resnr) &  (Rline.active_flag == 1)).first()

            if rline:

                bill = db_session.query(Bill).filter(
                        (Bill.resnr == resno) &  (Bill.reslinnr == 0)).first()

                if not bill:
                    bill = Bill()
                    db_session.add(bill)

                    bill.resnr = resno
                    bill.reslinnr = 0
                    bill.rgdruck = 1
                    billtyp = 2

                    if master.rechnr != 0:
                        bill.rechnr = master.rechnr
                    else:

                        counters = db_session.query(Counters).filter(
                                (Counters.counter_no == 3)).first()
                        counters = counters + 1
                        bill.rechnr = counters

                        counters = db_session.query(Counters).first()

                        master = db_session.query(Master).first()
                        master.rechnr = bill.rechnr

                        master = db_session.query(Master).first()
                bill.gastnr = gastno
                bill.name = rgast.name
                bill.segmentcode = reservation.segmentcode

                bill = db_session.query(Bill).first()

        if not master and (rgast.karteityp == 1 or rgast.karteityp == 2):

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 166)).first()

            if htparam.flogical:
                msg_str = "&Q" + translateExtended ("Master Bill does not exist, CREATE IT?", lvcarea, "")

        reservation = db_session.query(Reservation).first()

    def resline_reserve_dec():

        nonlocal msg_str, lvcarea, res_line, guest, reservation, master, brief, segment, sourccod, bill, counters, htparam, waehrung
        nonlocal rline, rgast


        nonlocal rline, rgast

        exchg_rate:decimal = 0
        Rline = Res_line

        if not reservation.insurance:

            for rline in db_session.query(Rline).filter(
                    (Rline.resnr == reservation.resnr) &  ((Rline.resstatus == 6) |  (Rline.resstatus == 13)) &  (Rline.reserve_dec != 0)).all():
                rline.reserve_dec = 0

            return

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            exchg_rate = waehrung.ankauf / waehrung.einheit

        if exchg_rate != 0:

            for rline in db_session.query(Rline).filter(
                    (Rline.resnr == reservation.resnr) &  ((Rline.resstatus == 6) |  (Rline.resstatus == 13)) &  (Rline.reserve_dec == 0)).all():
                rline.reserve_dec = exchg_rate


    update_mainres()

    return generate_output()