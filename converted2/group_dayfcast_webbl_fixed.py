#using conversion tools version: 1.0.0.115

from functions.additional_functions import *
from decimal import Decimal
from datetime import date, timedelta
from models import Res_line, Reservation

input_param_list, Input_param = create_model("Input_param", {"input_date":date})

def group_dayfcast_webbl(input_param_list:[Input_param]):

    prepare_cache ([Res_line, Reservation])

    summary_status_list = []
    res_output_list = []
    start_date:date = None
    end_date:date = None
    curr_date:date = None
    i:int = 0
    room_count:List[int] = create_empty_list(31,0)
    day_number:int = 0
    tot_qty:int = 0
    last_day:int = 0
    counter:int = 0
    prev_resnr:int = 0
    max_abreise:date = None
    grand_total:int = 0
    summary_total:int = 0
    stat_list:List[string] = create_empty_list(14,"")
    res_line = reservation = None

    tt_reslin = res_output = summary_status = input_param = None

    tt_reslin_list, Tt_reslin = create_model("Tt_reslin", {"group_name":string, "name":string, "resnr":int, "room_qty":[int,30], "zimmeranz":int, "ankunft":date, "resstatus":int})
    res_output_list, Res_output = create_model("Res_output", {"group_name":string, "name":string, "resnr":int, "room_qty":[int,31], "resstatus":int, "tot_room_qty":int, "description":string})
    summary_status_list, Summary_status = create_model("Summary_status", {"room_qty":[int,31], "resstatus":int, "description":string, "tot_room_qty":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal summary_status_list, res_output_list, start_date, end_date, curr_date, i, room_count, day_number, tot_qty, last_day, counter, prev_resnr, max_abreise, grand_total, summary_total, stat_list, res_line, reservation


        nonlocal tt_reslin, res_output, summary_status, input_param
        nonlocal tt_reslin_list, res_output_list, summary_status_list

        return {"summary-status": summary_status_list, "res-output": res_output_list}

    stat_list[0] = "Guaranted"
    stat_list[1] = "6 PM"
    stat_list[2] = "Tentative"
    stat_list[3] = "WaitList"
    stat_list[4] = "VerbalConfirm"
    stat_list[5] = "Inhouse"
    stat_list[6] = ""
    stat_list[7] = "Departed"
    stat_list[8] = "Cancelled"
    stat_list[9] = "NoShow"
    stat_list[10] = "ShareRes"
    stat_list[11] = "AccGuest"
    stat_list[12] = "RmSharer"
    stat_list[13] = "AccGuest"

    input_param = query(input_param_list, first=True)

    if input_param:
        next_month_start = date_mdy(get_month(input_param.input_date) + 1, 1, get_year(input_param.input_date))
        last_day = get_day(next_month_start - timedelta(days=1))
        start_date = date_mdy(get_month(input_param.input_date) , 1, get_year(input_param.input_date))
        end_date = date_mdy(get_month(input_param.input_date) , last_day, get_year(input_param.input_date))

        for res_line in db_session.query(Res_line).filter(
                (Res_line.ankunft >= start_date) & (Res_line.abreise > end_date)).order_by(Res_line._recid).all():

            if max_abreise is None or res_line.abreise > max_abreise:
                max_abreise = res_line.abreise

        if max_abreise and max_abreise > end_date:
            end_date = max_abreise
        tt_reslin_list.clear()

        res_line_obj_list = {}
        res_line = Res_line()
        reservation = Reservation()
        for res_line.abreise, res_line.resnr, res_line.zimmeranz, res_line.ankunft, res_line.resstatus, res_line._recid, reservation.groupname, reservation.name, reservation._recid in db_session.query(Res_line.abreise, Res_line.resnr, Res_line.zimmeranz, Res_line.ankunft, Res_line.resstatus, Res_line._recid, Reservation.groupname, Reservation.name, Reservation._recid).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.grpFlag)).filter(
                 (Res_line.ankunft >= start_date) & (Res_line.abreise <= end_date) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.resstatus != 9) & (Res_line.resstatus != 11) & (Res_line.resstatus != 13)).order_by(Res_line._recid).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            tt_reslin = Tt_reslin()
            tt_reslin_list.append(tt_reslin)

            tt_reslin.group_name = reservation.groupname
            tt_reslin.name = reservation.name
            tt_reslin.resnr = res_line.resnr
            tt_reslin.room_qty = 0
            tt_reslin.zimmeranz = res_line.zimmeranz
            tt_reslin.ankunft = res_line.ankunft
            tt_reslin.resstatus = res_line.resstatus

        # ... (rest of the code remains unchanged)

    return generate_output()