#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Guest, Reservation, Master, Brief, Segment, Sourccod, Bill, Counters, Htparam, Waehrung

def update_mainresbl(pvilanguage:int, res_mode:string, user_init:string, mr_comment:string, letter:string, curr_segm:string, curr_source:string, groupname:string, m_voucher:string, limitdate:date, deposit:Decimal, contact_nr:int, cutoff_days:int, resno:int, gastno:int, l_grpnr:int, fixrateflag:bool):

    prepare_cache ([Res_line, Reservation, Master, Brief, Segment, Sourccod, Bill, Counters, Htparam, Waehrung])

    msg_str = ""
    lvcarea:string = "mk-resline"
    res_line = guest = reservation = master = brief = segment = sourccod = bill = counters = htparam = waehrung = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, res_line, guest, reservation, master, brief, segment, sourccod, bill, counters, htparam, waehrung
        nonlocal pvilanguage, res_mode, user_init, mr_comment, letter, curr_segm, curr_source, groupname, m_voucher, limitdate, deposit, contact_nr, cutoff_days, resno, gastno, l_grpnr, fixrateflag

        return {"msg_str": msg_str}

    def update_mainres():

        nonlocal msg_str, lvcarea, res_line, guest, reservation, master, brief, segment, sourccod, bill, counters, htparam, waehrung
        nonlocal pvilanguage, res_mode, user_init, mr_comment, letter, curr_segm, curr_source, groupname, m_voucher, limitdate, deposit, contact_nr, cutoff_days, resno, gastno, l_grpnr, fixrateflag

        ct:string = ""
        answer:bool = True
        rline = None
        rgast = None
        Rline =  create_buffer("Rline",Res_line)
        Rgast =  create_buffer("Rgast",Guest)

        reservation = get_cache (Reservation, {"resnr": [(eq, resno)]})

        rgast = db_session.query(Rgast).filter(
                 (Rgast.gastnr == gastno)).first()

        master = get_cache (Master, {"resnr": [(eq, resno)]})

        if master and master.active:
            reservation.verstat = 1
        else:
            reservation.verstat = 0

        if res_mode.lower()  == ("new").lower() :
            reservation.useridanlage = user_init
        reservation.bemerk = mr_comment


        ct = letter

        brief = get_cache (Brief, {"briefkateg": [(eq, l_grpnr)],"briefnr": [(eq, to_int(substring(ct, 0, get_index(ct, " "))))]})

        if brief:
            reservation.briefnr = brief.briefnr
        else:
            reservation.briefnr = 0
        ct = curr_segm

        segment = get_cache (Segment, {"segmentcode": [(eq, to_int(substring(ct, 0, get_index(ct, " "))))]})

        if segment:
            reservation.segmentcode = segment.segmentcode
        ct = curr_source

        sourccod = get_cache (Sourccod, {"source_code": [(eq, to_int(substring(ct, 0, get_index(ct, " "))))]})

        if sourccod:
            reservation.resart = sourccod.source_code
        reservation.groupname = groupname
        reservation.grpflag = (groupname != "")
        reservation.limitdate = limitdate
        reservation.depositgef =  to_decimal(deposit)
        reservation.vesrdepot = m_voucher
        reservation.kontakt_nr = contact_nr
        reservation.point_resnr = cutoff_days

        if (reservation.insurance and not fixrateflag) or (not reservation.insurance and fixrateflag):
            reservation.insurance = fixrateflag


            resline_reserve_dec()

        if master:
            pass

            if not master.active:

                bill = get_cache (Bill, {"resnr": [(eq, resno)],"reslinnr": [(eq, 0)]})

                if bill and bill.saldo != 0:
                    master.active = True
            pass

            if master.active:
                reservation.verstat = 1
            else:
                reservation.verstat = 0

            rline = get_cache (Res_line, {"resnr": [(eq, master.resnr)],"active_flag": [(eq, 1)]})

            if rline:

                bill = get_cache (Bill, {"resnr": [(eq, resno)],"reslinnr": [(eq, 0)]})

                if not bill:
                    bill = Bill()
                    db_session.add(bill)

                    bill.resnr = resno
                    bill.reslinnr = 0
                    bill.rgdruck = 1
                    bill.billtyp = 2

                    if master.rechnr != 0:
                        bill.rechnr = master.rechnr
                    else:

                        counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
                        counters.counter = counters.counter + 1
                        bill.rechnr = counters.counter
                        pass
                        pass
                        master.rechnr = bill.rechnr
                        pass
                bill.gastnr = gastno
                bill.name = rgast.name
                bill.segmentcode = reservation.segmentcode


                pass

        if not master and (rgast.karteityp == 1 or rgast.karteityp == 2):

            htparam = get_cache (Htparam, {"paramnr": [(eq, 166)]})

            if htparam.flogical:
                msg_str = "&Q" + translateExtended ("Master Bill does not exist, CREATE IT?", lvcarea, "")
        pass


    def resline_reserve_dec():

        nonlocal msg_str, lvcarea, res_line, guest, reservation, master, brief, segment, sourccod, bill, counters, htparam, waehrung
        nonlocal pvilanguage, res_mode, user_init, mr_comment, letter, curr_segm, curr_source, groupname, m_voucher, limitdate, deposit, contact_nr, cutoff_days, resno, gastno, l_grpnr, fixrateflag

        exchg_rate:Decimal = to_decimal("0.0")
        rline = None
        Rline =  create_buffer("Rline",Res_line)

        if not reservation.insurance:

            for rline in db_session.query(Rline).filter(
                     (Rline.resnr == reservation.resnr) & ((Rline.resstatus == 6) | (Rline.resstatus == 13)) & (Rline.reserve_dec != 0)).order_by(Rline._recid).all():
                rline.reserve_dec =  to_decimal("0")

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

        if exchg_rate != 0:

            for rline in db_session.query(Rline).filter(
                     (Rline.resnr == reservation.resnr) & ((Rline.resstatus == 6) | (Rline.resstatus == 13)) & (Rline.reserve_dec == 0)).order_by(Rline._recid).all():
                rline.reserve_dec =  to_decimal(exchg_rate)

    update_mainres()

    return generate_output()