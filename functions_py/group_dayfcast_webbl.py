#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Reservation

input_param_data, Input_param = create_model("Input_param", {"input_date":date})

def group_dayfcast_webbl(input_param_data:[Input_param]):

    prepare_cache ([Res_line, Reservation])

    summary_status_data = []
    res_output_data = []
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
    num_month:int = 0
    num_date:int = 0
    tmp_date:date = None
    res_line = reservation = None

    tt_reslin = res_output = summary_status = input_param = None

    tt_reslin_data, Tt_reslin = create_model("Tt_reslin", {"group_name":string, "name":string, "resnr":int, "room_qty":[int,30], "zimmeranz":int, "ankunft":date, "resstatus":int})
    res_output_data, Res_output = create_model("Res_output", {"group_name":string, "name":string, "resnr":int, "room_qty":[int,31], "resstatus":int, "tot_room_qty":int, "description":string})
    summary_status_data, Summary_status = create_model("Summary_status", {"room_qty":[int,31], "resstatus":int, "description":string, "tot_room_qty":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal summary_status_data, res_output_data, start_date, end_date, curr_date, i, room_count, day_number, tot_qty, last_day, counter, prev_resnr, max_abreise, grand_total, summary_total, stat_list, num_month, num_date, tmp_date, res_line, reservation


        nonlocal tt_reslin, res_output, summary_status, input_param
        nonlocal tt_reslin_data, res_output_data, summary_status_data

        return {"summary-status": summary_status_data, "res-output": res_output_data}

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

    input_param = query(input_param_data, first=True)
    num_month = get_month(input_param.input_date)
    num_month = num_month + 1
    tmp_date = date_mdy(num_month, 1, get_year(input_param.input_date))
    tmp_date = tmp_date - timedelta(days=1)

    last_day = get_day(tmp_date)
    start_date = date_mdy(get_month(input_param.input_date) , 1, get_year(input_param.input_date))
    end_date = date_mdy(get_month(input_param.input_date) , last_day, get_year(input_param.input_date))

    print("Start Date : " + str(start_date))
    print("End Date : " + str(end_date))

    for res_line in db_session.query(Res_line).filter(
             (Res_line.ankunft >= start_date) & (Res_line.abreise > end_date)).order_by(Res_line._recid).all():

        if max_abreise == None:
            max_abreise = res_line.abreise
        else:

            if res_line.abreise > max_abreise:
                max_abreise = res_line.abreise

    if max_abreise > end_date:
        end_date = max_abreise
    tt_reslin_data.clear()

    res_line_obj_list = {}
    res_line = Res_line()
    reservation = Reservation()
    for res_line.abreise, res_line.resnr, res_line.zimmeranz, res_line.ankunft, res_line.resstatus, res_line._recid, reservation.groupname, reservation.name, reservation._recid in db_session.query(Res_line.abreise, Res_line.resnr, Res_line.zimmeranz, Res_line.ankunft, Res_line.resstatus, Res_line._recid, Reservation.groupname, Reservation.name, Reservation._recid).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.grpflag)).filter(
             (Res_line.ankunft >= start_date) & (Res_line.abreise <= end_date) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.resstatus != 9) & (Res_line.resstatus != 11) & (Res_line.resstatus != 13)).order_by(Res_line._recid).all():
        if res_line_obj_list.get(res_line._recid):
            continue
        else:
            res_line_obj_list[res_line._recid] = True


        tt_reslin = Tt_reslin()
        tt_reslin_data.append(tt_reslin)

        tt_reslin.group_name = reservation.groupname
        tt_reslin.name = reservation.name
        tt_reslin.resnr = res_line.resnr
        tt_reslin.room_qty = 0
        tt_reslin.zimmeranz = res_line.zimmeranz
        tt_reslin.ankunft = res_line.ankunft
        tt_reslin.resstatus = res_line.resstatus

    for tt_reslin in query(tt_reslin_data, sort_by=[("resnr",False)]):

        res_output = query(res_output_data, filters=(lambda res_output: res_output.resnr == tt_reslin.resnr), first=True)

        if not res_output:
            for i in range(1,last_day + 1) :
                room_count[i - 1] = 0
            tot_qty = 0
            for curr_date in date_range(start_date,end_date) :
                day_number = get_day(curr_date)

                if day_number >= 1 and day_number <= last_day:

                    if tt_reslin.ankunft == curr_date:
                        room_count[day_number - 1] = room_count[day_number - 1] + tt_reslin.zimmeranz
                        tot_qty = tot_qty + tt_reslin.zimmeranz
                        grand_total = grand_total + tot_qty
            res_output = Res_output()
            res_output_data.append(res_output)

            res_output.group_name = tt_reslin.group_name
            res_output.name = tt_reslin.name
            res_output.resstatus = tt_reslin.resstatus
            res_output.description = stat_list[res_output.resstatus - 1]
            res_output.resnr = tt_reslin.resnr
            res_output.tot_room_qty = tot_qty


            for i in range(1,last_day + 1) :
                res_output.room_qty[i - 1] = room_count[i - 1]
        else:
            for curr_date in date_range(start_date,end_date) :
                day_number = get_day(curr_date)

                if day_number >= 1 and day_number <= last_day:

                    if tt_reslin.ankunft == curr_date:
                        room_count[day_number - 1] = room_count[day_number - 1] + tt_reslin.zimmeranz
                        tot_qty = tot_qty + tt_reslin.zimmeranz
                        grand_total = grand_total + tt_reslin.zimmeranz
            for i in range(1,last_day + 1) :
                res_output.room_qty[i - 1] = room_count[i - 1]
            res_output.tot_room_qty = tot_qty

    res_output = query(res_output_data, filters=(lambda res_output: res_output.resnr == tt_reslin.resnr), first=True)

    if not res_output:
        res_output = Res_output()
        res_output_data.append(res_output)

        res_output.group_name = "TOTAL"
        res_output.tot_room_qty = grand_total
        res_output.resstatus = 0


    summary_status_data.clear()

    for res_output in query(res_output_data, filters=(lambda res_output: res_output.resstatus != 0), sort_by=[("resstatus",False)]):

        summary_status = query(summary_status_data, filters=(lambda summary_status: summary_status.resstatus == res_output.resstatus), first=True)

        if not summary_status:
            summary_status = Summary_status()
            summary_status_data.append(summary_status)

            summary_status.resstatus = res_output.resstatus
            summary_status.description = stat_list[summary_status.resstatus - 1]


            for i in range(1,last_day + 1) :
                summary_status.room_qty[i - 1] = 0
        for i in range(1,last_day + 1) :
            summary_status.room_qty[i - 1] = summary_status.room_qty[i - 1] + res_output.room_qty[i - 1]
            summary_total = summary_total + res_output.room_qty[i - 1]
        summary_status.tot_room_qty = summary_total

    return generate_output()