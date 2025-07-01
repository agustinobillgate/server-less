#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Nation, Nationstat

def nationstatbl(printer_nr:int, call_from:int, txt_file:string, from_month:string, hide_zero:bool, mi_arrival:bool, mi_comp:bool):

    prepare_cache ([Htparam, Nation, Nationstat])

    room_list_list = []
    tot_all:int = 0
    from_date:date = None
    to_date:date = None
    ci_date:date = None
    curr_day:int = 0
    diff_one:int = 0
    ok:bool = False
    i:int = 0
    htparam = nation = nationstat = None

    room_list = None

    room_list_list, Room_list = create_model("Room_list", {"name":string, "bezeich":string, "summe":int, "room":[int,31], "proz":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal room_list_list, tot_all, from_date, to_date, ci_date, curr_day, diff_one, ok, i, htparam, nation, nationstat
        nonlocal printer_nr, call_from, txt_file, from_month, hide_zero, mi_arrival, mi_comp


        nonlocal room_list
        nonlocal room_list_list

        return {"room-list": room_list_list}

    def create_browse():

        nonlocal room_list_list, tot_all, from_date, to_date, ci_date, curr_day, diff_one, ok, htparam, nation, nationstat
        nonlocal printer_nr, call_from, txt_file, from_month, hide_zero, mi_arrival, mi_comp


        nonlocal room_list
        nonlocal room_list_list

        mm:int = 0
        yy:int = 0
        datum:date = None
        i:int = 0
        incl_comp:bool = True
        incl_comp = not mi_comp
        tot_all = 0
        room_list_list.clear()
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
            room_list_list.append(room_list)

            room_list.name = entry(0, nation.bezeich , ";")
            room_list.bezeich = nation.kurzbez

            for nationstat in db_session.query(Nationstat).filter(
                     (Nationstat.nationnr == nation.nationnr) & (Nationstat.datum >= from_date) & (Nationstat.datum <= to_date)).order_by(Nationstat.datum).all():
                i = get_day(nationstat.datum)

                if incl_comp:
                    room_list.room[i - 1] = nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2 + nationstat.loggratis
                    room_list.summe = room_list.summe + nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2 + nationstat.loggratis
                else:
                    room_list.room[i - 1] = nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2
                    room_list.summe = room_list.summe + nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2

        for room_list in query(room_list_list, filters=(lambda room_list: room_list.summe != 0)):
            tot_all = tot_all + room_list.summe

        if tot_all > 0:

            for room_list in query(room_list_list, filters=(lambda room_list: room_list.summe != 0)):
                room_list.proz =  to_decimal(room_list.summe) / to_decimal(tot_all) * to_decimal("100")


    def create_browse1():

        nonlocal room_list_list, tot_all, from_date, to_date, ci_date, curr_day, diff_one, ok, htparam, nation, nationstat
        nonlocal printer_nr, call_from, txt_file, from_month, hide_zero, mi_arrival, mi_comp


        nonlocal room_list
        nonlocal room_list_list

        mm:int = 0
        yy:int = 0
        curr_datum:date = None
        i:int = 0
        incl_comp:bool = True
        incl_comp = not mi_comp
        tot_all = 0
        room_list_list.clear()
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
            room_list_list.append(room_list)

            room_list.name = entry(0, nation.bezeich , ";")
            room_list.bezeich = nation.kurzbez

            for nationstat in db_session.query(Nationstat).filter(
                     (Nationstat.nationnr == nation.nationnr) & (Nationstat.datum >= from_date) & (Nationstat.datum <= to_date)).order_by(Nationstat.datum).all():
                i = get_day(nationstat.datum)

                if incl_comp:
                    room_list.room[i - 1] = nationstat.ankerwachs + nationstat.ankkind1 + nationstat.ankkind2 + nationstat.ankgratis
                    room_list.summe = room_list.summe + nationstat.ankerwachs + nationstat.ankkind1 + nationstat.ankkind2 + nationstat.ankgratis
                else:
                    room_list.room[i - 1] = nationstat.ankerwachs + nationstat.ankkind1 + nationstat.ankkind2
                    room_list.summe = room_list.summe + nationstat.ankerwachs + nationstat.ankkind1 + nationstat.ankkind2

        for room_list in query(room_list_list, filters=(lambda room_list: room_list.summe != 0)):
            tot_all = tot_all + room_list.summe

        if tot_all > 0:

            for room_list in query(room_list_list, filters=(lambda room_list: room_list.summe != 0)):
                room_list.proz =  to_decimal(room_list.summe) / to_decimal(tot_all) * to_decimal("100")


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    if not mi_arrival:
        create_browse()
    else:
        create_browse1()

    if hide_zero:

        for room_list in query(room_list_list, filters=(lambda room_list: room_list.summe == 0)):
            room_list_list.remove(room_list)

    return generate_output()