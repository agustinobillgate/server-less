#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_raum, Bk_rset

def prepare_mp_event_detailbl(blockid:string, nr:int):
    resstatus = 0
    guestno = 0
    pax = 0
    t_event_list = []
    t_bkraum_list = []
    t_bkrset_list = []
    bk_raum = bk_rset = None

    t_event = t_bkraum = t_bkrset = None

    t_event_list, T_event = create_model("T_event", {"blockid":string, "counter":int, "nr":int, "eventtype":string, "eventstatus":string, "eventname":string, "startdate":date, "enddate":date, "starttime":string, "endtime":string, "atendees":int, "minguaranted":int, "actual":int, "venue":string, "setup":string, "amount":Decimal})
    t_bkraum_list, T_bkraum = create_model_like(Bk_raum)
    t_bkrset_list, T_bkrset = create_model_like(Bk_rset)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal resstatus, guestno, pax, t_event_list, t_bkraum_list, t_bkrset_list, bk_raum, bk_rset
        nonlocal blockid, nr


        nonlocal t_event, t_bkraum, t_bkrset
        nonlocal t_event_list, t_bkraum_list, t_bkrset_list

        return {"resstatus": resstatus, "guestno": guestno, "pax": pax, "t-event": t_event_list, "t-bkraum": t_bkraum_list, "t-bkrset": t_bkrset_list}

    t_event = query(t_event_list, first=True)

    bk_event_detail = db_session.query(Bk_event_detail).filter(
             (Bk_event_detail.block_id == blockid) & (Bk_event_detail.nr == nr)).first()

    if bk_event_detail:
        t_event = T_event()
        t_event_list.append(t_event)

        t_event.blockid = blockid
        t_event.nr = bk_event_detail.nr
        t_event.eventtype = bk_event_detail.event_status
        t_event.eventname = bk_event_detail.event_name
        t_event.startdate = bk_event_detail.start_date
        t_event.enddate = bk_event_detail.end_date
        t_event.eventtype = bk_event_detail.event_type
        t_event.starttime = to_string(bk_event_detail.start_time, "HH:MM")
        t_event.endtime = to_string(bk_event_detail.end_time, "HH:MM")
        t_event.atendees = bk_event_detail.atendees
        t_event.minguaranted = bk_event_detail.min_guaranteed
        t_event.actual = bk_event_detail.actual
        t_event.venue = bk_event_detail.venue
        t_event.setup = bk_event_detail.setup
        t_event.amount =  to_decimal(bk_event_detail.amount)

        bk_raum = get_cache (Bk_raum, {"bezeich": [(eq, t_event.venue)]})

        if bk_raum:
            t_bkraum = T_bkraum()
            t_bkraum_list.append(t_bkraum)

            buffer_copy(bk_raum, t_bkraum)

        bk_rset = db_session.query(Bk_rset).filter(
                 (entry(0, Bk_rset.bezeichnung, "/") == t_event.venue) & (entry(1, Bk_rset.bezeichnung, "/") == t_event.setup)).first()

        if bk_rset:
            t_bkrset = T_bkrset()
            t_bkrset_list.append(t_bkrset)

            buffer_copy(bk_rset, t_bkrset)
    else:

        bk_catering = db_session.query(Bk_catering).filter(
                 (Bk_catering.block_id == blockid)).first()

        if bk_catering:
            pax = bk_catering.attendees

    bk_master = db_session.query(Bk_master).filter(
             (Bk_master.block_id == blockid)).first()

    if bk_master:

        bk_queasy = db_session.query(Bk_queasy).filter(
                 (Bk_queasy.key == 1) & (Bk_queasy.number1 == bk_master.resstatus)).first()

        if bk_queasy:

            if bk_queasy.number2 >= 1 and bk_queasy.number2 <= 3:
                resstatus = 2

            elif bk_queasy.number2 == 4:
                resstatus = 1

    bk_master = db_session.query(Bk_master).filter(
             (Bk_master.block_id == blockid)).first()

    if bk_master:
        guestno = bk_master.gastnr

    return generate_output()