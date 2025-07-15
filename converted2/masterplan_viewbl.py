#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_raum, Bk_rset

def masterplan_viewbl(mode:string, curr_date:date):

    prepare_cache ([Bk_raum, Bk_rset])

    t_mplan_view_data = []
    curr_week:date = None
    ftdate:date = None
    logi1:bool = False
    bk_raum = bk_rset = None

    t_mplan_view = t_mplan_list = buff_mplan_list = None

    t_mplan_view_data, T_mplan_view = create_model("T_mplan_view", {"block_id":string, "event_name":string, "resno":int, "gname":string, "guest_no":int, "room":string, "room_desc":string, "stat_no":int, "stat_code":string, "invno":int, "fr_date":date, "to_date":date, "fr_time":string, "to_time":string, "amount":Decimal, "setup":string, "rsize":int, "person":int, "preparation":int, "ext":string, "flag":string})
    t_mplan_list_data, T_mplan_list = create_model("T_mplan_list", {"block_id":string, "event_name":string, "resno":int, "gname":string, "guest_no":int, "room":string, "room_desc":string, "stat_no":int, "stat_code":string, "invno":int, "fr_date":date, "to_date":date, "fr_time":string, "to_time":string, "amount":Decimal, "setup":string, "rsize":int, "person":int, "preparation":int, "ext":string, "flag":string})
    buff_mplan_list_data, Buff_mplan_list = create_model("Buff_mplan_list", {"block_id":string, "event_name":string, "resno":int, "gname":string, "guest_no":int, "room":string, "room_desc":string, "stat_no":int, "stat_code":string, "invno":int, "fr_date":date, "to_date":date, "fr_time":string, "to_time":string, "amount":Decimal, "setup":string, "rsize":int, "person":int, "preparation":int, "ext":string, "flag":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_mplan_view_data, curr_week, ftdate, logi1, bk_raum, bk_rset
        nonlocal mode, curr_date


        nonlocal t_mplan_view, t_mplan_list, buff_mplan_list
        nonlocal t_mplan_view_data, t_mplan_list_data, buff_mplan_list_data

        return {"t-mplan-view": t_mplan_view_data}

    def daily_view():

        nonlocal t_mplan_view_data, curr_week, ftdate, logi1, bk_raum, bk_rset
        nonlocal mode, curr_date


        nonlocal t_mplan_view, t_mplan_list, buff_mplan_list
        nonlocal t_mplan_view_data, t_mplan_list_data, buff_mplan_list_data

        bk_event_detail = db_session.query(Bk_event_detail).filter(
                 (Bk_event_detail.start_date == curr_date) & (Bk_event_detail.end_date == curr_date)).first()

        if bk_event_detail:

            bk_master = db_session.query(Bk_master).filter(
                     (Bk_master.block_id == bk_event_detail.block_id) & (Bk_master.cancel_flag[inc_value(0)] == False)).first()

            if bk_master:
                logi1 = True

        if logi1 == False:

            for bk_raum in db_session.query(Bk_raum).order_by(Bk_raum.bezeich).all():
                t_mplan_list = T_mplan_list()
                t_mplan_list_data.append(t_mplan_list)

                t_mplan_list.room = bk_raum.raum
                t_mplan_list.room_desc = bk_raum.bezeich
                t_mplan_list.flag = "*"


        else:

            for bk_event_detail in query(bk_event_detail_data, filters=(lambda bk_event_detail: bk_event_detail.start_date == curr_date and bk_event_detail.end_date == curr_date), sort_by=[("venue",False)]):
                t_mplan_list = T_mplan_list()
                t_mplan_list_data.append(t_mplan_list)

                t_mplan_list.event_name = bk_event_detail.event_name
                t_mplan_list.room_desc = bk_event_detail.venue
                t_mplan_list.setup = bk_event_detail.setup
                t_mplan_list.fr_date = bk_event_detail.start_date
                t_mplan_list.to_date = bk_event_detail.end_date
                t_mplan_list.fr_time = to_string(bk_event_detail.start_time, "HH:MM")
                t_mplan_list.to_time = to_string(bk_event_detail.end_time, "HH:MM")
                t_mplan_list.amount =  to_decimal(bk_event_detail.amount)
                t_mplan_list.flag = "**"

                bk_raum = get_cache (Bk_raum, {"bezeich": [(eq, bk_event_detail.venue)]})

                if bk_raum:
                    t_mplan_list.room = bk_raum.raum

                bk_rset = db_session.query(Bk_rset).filter(
                         (entry(0, Bk_rset.bezeichnung, "/") == bk_event_detail.venue) & (entry(1, Bk_rset.bezeichnung, "/") == bk_event_detail.setup)).first()

                if bk_rset:
                    t_mplan_list.rsize = bk_rset.groesse
                    t_mplan_list.person = bk_rset.personen
                    t_mplan_list.preparation = bk_rset.vorbereit
                    t_mplan_list.ext = bk_rset.nebenstelle

                bk_master = db_session.query(Bk_master).filter(
                         (Bk_master.block_id == bk_event_detail.block_id)).first()

                if bk_master:
                    t_mplan_list.block_id = bk_master.block_id
                    t_mplan_list.resno = bk_master.resnr
                    t_mplan_list.guest_no = bk_master.gastnr
                    t_mplan_list.gname = bk_master.name
                    t_mplan_list.stat_no = bk_master.resstatus

                    bk_queasy = db_session.query(Bk_queasy).filter(
                             (Bk_queasy.key == 1) & (Bk_queasy.number1 == bk_master.resstatus)).first()

                    if bk_queasy:
                        t_mplan_list.stat_code = bk_queasy.char1

            for t_mplan_list in query(t_mplan_list_data):
                buff_mplan_list = Buff_mplan_list()
                buff_mplan_list_data.append(buff_mplan_list)

                buffer_copy(t_mplan_list, buff_mplan_list)

            for bk_raum in db_session.query(Bk_raum).order_by(Bk_raum.raum).all():

                buff_mplan_list = query(buff_mplan_list_data, filters=(lambda buff_mplan_list: buff_mplan_list.room == bk_raum.raum), first=True)

                if not buff_mplan_list:
                    t_mplan_list = T_mplan_list()
                    t_mplan_list_data.append(t_mplan_list)

                    t_mplan_list.room = bk_raum.raum
                    t_mplan_list.room_desc = bk_raum.bezeich
                    t_mplan_list.flag = "*"

        for t_mplan_list in query(t_mplan_list_data, sort_by=[("room",False)]):
            t_mplan_view = T_mplan_view()
            t_mplan_view_data.append(t_mplan_view)

            buffer_copy(t_mplan_list, t_mplan_view)


    def weekly_view():

        nonlocal t_mplan_view_data, curr_week, ftdate, logi1, bk_raum, bk_rset
        nonlocal mode, curr_date


        nonlocal t_mplan_view, t_mplan_list, buff_mplan_list
        nonlocal t_mplan_view_data, t_mplan_list_data, buff_mplan_list_data


        curr_week = curr_date + timedelta(days=6)

        for bk_event_detail in query(bk_event_detail_data, filters=(lambda bk_event_detail: bk_event_detail.start_date >= curr_date and bk_event_detail.start_date <= curr_week)):

            bk_master = db_session.query(Bk_master).filter(
                     (Bk_master.block_id == bk_event_detail.block_id) & (Bk_master.cancel_flag[inc_value(0)] == False)).first()

            if bk_master:
                logi1 = True

            if logi1 :
                break

        if logi1 == False:

            for bk_raum in db_session.query(Bk_raum).order_by(Bk_raum.bezeich).all():
                t_mplan_list = T_mplan_list()
                t_mplan_list_data.append(t_mplan_list)

                t_mplan_list.room = bk_raum.raum
                t_mplan_list.room_desc = bk_raum.bezeich
                t_mplan_list.flag = "*"


        else:

            for bk_event_detail in query(bk_event_detail_data, filters=(lambda bk_event_detail: bk_event_detail.start_date >= curr_date and bk_event_detail.start_date <= curr_week), sort_by=[("venue",False)]):
                t_mplan_list = T_mplan_list()
                t_mplan_list_data.append(t_mplan_list)

                t_mplan_list.event_name = bk_event_detail.event_name
                t_mplan_list.room_desc = bk_event_detail.venue
                t_mplan_list.setup = bk_event_detail.setup
                t_mplan_list.fr_date = bk_event_detail.start_date
                t_mplan_list.to_date = bk_event_detail.end_date
                t_mplan_list.fr_time = to_string(bk_event_detail.start_time, "HH:MM")
                t_mplan_list.to_time = to_string(bk_event_detail.end_time, "HH:MM")
                t_mplan_list.amount =  to_decimal(bk_event_detail.amount)
                t_mplan_list.flag = "**"

                bk_raum = get_cache (Bk_raum, {"bezeich": [(eq, bk_event_detail.venue)]})

                if bk_raum:
                    t_mplan_list.room = bk_raum.raum

                bk_rset = db_session.query(Bk_rset).filter(
                         (entry(0, Bk_rset.bezeichnung, "/") == bk_event_detail.venue) & (entry(1, Bk_rset.bezeichnung, "/") == bk_event_detail.setup)).first()

                if bk_rset:
                    t_mplan_list.rsize = bk_rset.groesse
                    t_mplan_list.person = bk_rset.personen
                    t_mplan_list.preparation = bk_rset.vorbereit
                    t_mplan_list.ext = bk_rset.nebenstelle

                bk_master = db_session.query(Bk_master).filter(
                         (Bk_master.block_id == bk_event_detail.block_id)).first()

                if bk_master:
                    t_mplan_list.block_id = bk_master.block_id
                    t_mplan_list.resno = bk_master.resnr
                    t_mplan_list.guest_no = bk_master.gastnr
                    t_mplan_list.gname = bk_master.name
                    t_mplan_list.stat_no = bk_master.resstatus

                    bk_queasy = db_session.query(Bk_queasy).filter(
                             (Bk_queasy.key == 1) & (Bk_queasy.number1 == bk_master.resstatus)).first()

                    if bk_queasy:
                        t_mplan_list.stat_code = bk_queasy.char1

            for t_mplan_list in query(t_mplan_list_data):
                buff_mplan_list = Buff_mplan_list()
                buff_mplan_list_data.append(buff_mplan_list)

                buffer_copy(t_mplan_list, buff_mplan_list)

            for bk_raum in db_session.query(Bk_raum).order_by(Bk_raum.raum).all():

                buff_mplan_list = query(buff_mplan_list_data, filters=(lambda buff_mplan_list: buff_mplan_list.room == bk_raum.raum), first=True)

                if not buff_mplan_list:
                    t_mplan_list = T_mplan_list()
                    t_mplan_list_data.append(t_mplan_list)

                    t_mplan_list.room = bk_raum.raum
                    t_mplan_list.room_desc = bk_raum.bezeich
                    t_mplan_list.flag = "*"

        for t_mplan_list in query(t_mplan_list_data, sort_by=[("room",False)]):
            t_mplan_view = T_mplan_view()
            t_mplan_view_data.append(t_mplan_view)

            buffer_copy(t_mplan_list, t_mplan_view)


    if mode.lower()  == ("daily").lower() :
        daily_view()
    else:
        weekly_view()

    return generate_output()