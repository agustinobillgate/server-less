#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Nation, Nationstat

def nationstat_webbl(printer_nr:int, call_from:int, txt_file:string, from_month:string, hide_zero:bool, mi_arrival:bool, mi_comp:bool, mi_show_d_percent:bool):

    prepare_cache ([Htparam, Nation, Nationstat])

    room_list_data = []
    tot_all:int = 0
    from_date:date = None
    to_date:date = None
    ci_date:date = None
    curr_day:int = 0
    diff_one:int = 0
    ok:bool = False
    i:int = 0
    htparam = nation = nationstat = None

    room_list = total_per_day = None

    room_list_data, Room_list = create_model("Room_list", {"nationnr":int, "name":string, "bezeich":string, "summe":int, "room":[int,31], "proz":Decimal, "d_percent":[Decimal,31]})
    total_per_day_data, Total_per_day = create_model("Total_per_day", {"date_day":int, "total_nat":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal room_list_data, tot_all, from_date, to_date, ci_date, curr_day, diff_one, ok, i, htparam, nation, nationstat
        nonlocal printer_nr, call_from, txt_file, from_month, hide_zero, mi_arrival, mi_comp, mi_show_d_percent


        nonlocal room_list, total_per_day
        nonlocal room_list_data, total_per_day_data

        return {"room-list": room_list_data}

    def create_browse():

        nonlocal room_list_data, tot_all, from_date, to_date, ci_date, curr_day, diff_one, ok, htparam, nation, nationstat
        nonlocal printer_nr, call_from, txt_file, from_month, hide_zero, mi_arrival, mi_comp, mi_show_d_percent


        nonlocal room_list, total_per_day
        nonlocal room_list_data, total_per_day_data

        mm:int = 0
        yy:int = 0
        datum:date = None
        i:int = 0
        incl_comp:bool = True
        bezeich:string = ""
        incl_comp = not mi_comp
        tot_all = 0
        room_list_data.clear()
        mm = to_int(substring(from_month, 0, 2))
        yy = to_int(substring(from_month, 2, 4))
        from_date = date_mdy(mm, 1, yy)
        mm = mm + 1

        if mm == 13:
            mm = 1
            yy = yy + 1
        to_date = date_mdy(mm, 1, yy) - timedelta(days=1)

        if to_date > ci_date:
            to_date = ci_date
        bezeich = None
        i = 0

        for nation in db_session.query(Nation).filter(
                 (Nation.natcode == 0)).order_by(Nation.bezeich).all():
            room_list = Room_list()
            room_list_data.append(room_list)

            room_list.name = entry(0, nation.bezeich , ";")
            room_list.bezeich = nation.kurzbez
            room_list.nationnr = nation.nationnr

        for nationstat in db_session.query(Nationstat).filter(
                 ((Nationstat.nationnr.in_(list(set([room_list.nationnr for room_list in room_list_data])))) & (Nationstat.datum >= from_date) & (Nationstat.datum <= to_date))).order_by(room_list.bezeich, Nationstat.datum).all():            room_list = query(room_list_data, (lambda room_list: (nationstat.nationnr == room_list.nationnr)), first=True)
            i = get_day(nationstat.datum)

            total_per_day = query(total_per_day_data, filters=(lambda total_per_day: total_per_day.date_day == i), first=True)

            if not total_per_day:
                total_per_day = Total_per_day()
                total_per_day_data.append(total_per_day)

                total_per_day.date_day = i

            if incl_comp:
                room_list.room[i - 1] = nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2 + nationstat.loggratis
                room_list.summe = room_list.summe + nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2 + nationstat.loggratis
                total_per_day.total_nat = total_per_day.total_nat + nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2 + nationstat.loggratis
            else:
                room_list.room[i - 1] = nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2
                room_list.summe = room_list.summe + nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2
                total_per_day.total_nat = total_per_day.total_nat + nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2

        for room_list in query(room_list_data, filters=(lambda room_list: room_list.summe != 0)):
            tot_all = tot_all + room_list.summe

            if mi_show_d_percent:

                for total_per_day in query(total_per_day_data):
                    i = total_per_day.date_day
                    room_list.d_percent[i - 1] = (room_list.room[i - 1] / total_per_day.total_nat) * 100

        if tot_all > 0:

            for room_list in query(room_list_data, filters=(lambda room_list: room_list.summe != 0)):
                room_list.proz =  to_decimal(room_list.summe) / to_decimal(tot_all) * to_decimal("100")

    def create_browse1():

        nonlocal room_list_data, tot_all, from_date, to_date, ci_date, curr_day, diff_one, ok, htparam, nation, nationstat
        nonlocal printer_nr, call_from, txt_file, from_month, hide_zero, mi_arrival, mi_comp, mi_show_d_percent


        nonlocal room_list, total_per_day
        nonlocal room_list_data, total_per_day_data

        mm:int = 0
        yy:int = 0
        curr_datum:date = None
        i:int = 0
        incl_comp:bool = True
        bezeich:string = ""
        incl_comp = not mi_comp
        room_list_data.clear()
        tot_all = 0
        mm = to_int(substring(from_month, 0, 2))
        yy = to_int(substring(from_month, 2, 4))
        from_date = date_mdy(mm, 1, yy)
        mm = mm + 1

        if mm == 13:
            mm = 1
            yy = yy + 1
        to_date = date_mdy(mm, 1, yy) - timedelta(days=1)

        if to_date > ci_date:
            to_date = ci_date

        for nation in db_session.query(Nation).filter(
                 (Nation.natcode == 0)).order_by(Nation.bezeich).all():
            room_list = Room_list()
            room_list_data.append(room_list)

            room_list.name = entry(0, nation.bezeich , ";")
            room_list.bezeich = nation.kurzbez
            room_list.nationnr = nation.nationnr

        for nationstat in db_session.query(Nationstat).filter(
                 ((Nationstat.nationnr.in_(list(set([room_list.nationnr for room_list in room_list_data])))) & (Nationstat.datum >= from_date) & (Nationstat.datum <= to_date))).order_by(room_list.bezeich, Nationstat.datum).all():            room_list = query(room_list_data, (lambda room_list: (nationstat.nationnr == room_list.nationnr)), first=True)
            i = get_day(nationstat.datum)

            total_per_day = query(total_per_day_data, filters=(lambda total_per_day: total_per_day.date_day == i), first=True)

            if not total_per_day:
                total_per_day = Total_per_day()
                total_per_day_data.append(total_per_day)

                total_per_day.date_day = i

            if incl_comp:
                room_list.room[i - 1] = nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2 + nationstat.loggratis
                room_list.summe = room_list.summe + nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2 + nationstat.loggratis
                total_per_day.total_nat = total_per_day.total_nat + nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2 + nationstat.loggratis
            else:
                room_list.room[i - 1] = nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2
                room_list.summe = room_list.summe + nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2
                total_per_day.total_nat = total_per_day.total_nat + nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2

        for room_list in query(room_list_data, filters=(lambda room_list: room_list.summe != 0)):
            tot_all = tot_all + room_list.summe

            if mi_show_d_percent:

                for total_per_day in query(total_per_day_data):
                    i = total_per_day.date_day
                    room_list.d_percent[i - 1] = (room_list.room[i - 1] / total_per_day.total_nat) * 100

        if tot_all > 0:

            for room_list in query(room_list_data, filters=(lambda room_list: room_list.summe != 0)):
                room_list.proz =  to_decimal(room_list.summe) / to_decimal(tot_all) * to_decimal("100")


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    if not mi_arrival:
        create_browse()
    else:
        create_browse1()

    if hide_zero:

        for room_list in query(room_list_data, filters=(lambda room_list: room_list.summe == 0)):
            room_list_data.remove(room_list)


    return generate_output()