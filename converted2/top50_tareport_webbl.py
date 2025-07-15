#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Guest, Genstat

def top50_tareport_webbl(pvilanguage:int, curr_date:string, curr_month:int, sorttype:int, disptype:int):

    prepare_cache ([Guest, Genstat])

    top50_list_data = []
    mm:int = 0
    yy:int = 0
    i:int = 0
    from_date:date = None
    to_date:date = None
    curr_date_loop:date = None
    datum:date = None
    jml:int = 0
    lvcarea:string = "comp-product"
    res_line = guest = genstat = None

    top50_list = r_list = None

    top50_list_data, Top50_list = create_model("Top50_list", {"num":int, "nr":int, "bezeich":string, "room":[int,12], "ytd":int, "lytd":int, "mtd":int, "gastnr":int})

    R_list = Top50_list
    r_list_data = top50_list_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal top50_list_data, mm, yy, i, from_date, to_date, curr_date_loop, datum, jml, lvcarea, res_line, guest, genstat
        nonlocal pvilanguage, curr_date, curr_month, sorttype, disptype
        nonlocal r_list


        nonlocal top50_list, r_list
        nonlocal top50_list_data

        return {"top50-list": top50_list_data}

    def create_top_50():

        nonlocal top50_list_data, mm, yy, i, from_date, to_date, curr_date_loop, datum, jml, lvcarea, res_line, guest, genstat
        nonlocal pvilanguage, curr_date, curr_month, sorttype, disptype
        nonlocal r_list


        nonlocal top50_list, r_list
        nonlocal top50_list_data

        top50_list = query(top50_list_data, filters=(lambda top50_list: top50_list.gastnr == genstat.gastnr), first=True)

        if not top50_list:
            top50_list = Top50_list()
            top50_list_data.append(top50_list)

            top50_list.gastnr = genstat.gastnr
            top50_list.bezeich = guest.name
        top50_list.room[get_month(genstat.datum) - 1] = top50_list.room[get_month(genstat.datum) - 1] + 1
        top50_list.ytd = top50_list.ytd + 1

    top50_list_data.clear()
    r_list_data.clear()
    mm = to_int(substring(curr_date, 0, 2))
    yy = to_int(substring(curr_date, 2, 4))
    jml = yy - 1
    from_date = date_mdy(1, 1, yy)

    if mm == 12:
        to_date = date_mdy(1, 1, yy + timedelta(days=1)) - timedelta(days=1)
    else:
        to_date = date_mdy(mm + 1, 1, yy) - timedelta(days=1)
    for curr_date_loop in date_range(from_date,to_date) :

        genstat_obj_list = {}
        for genstat, res_line, guest in db_session.query(Genstat, Res_line, Guest).join(Res_line,(Res_line.resnr == Genstat.resnr) & (Res_line.reslinnr == Genstat.res_int[inc_value(0)])).join(Guest,(Guest.gastnr == Genstat.gastnr) & (Guest.karteityp == 2)).filter(
                 (Genstat.datum == curr_date_loop) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Guest.gastnr).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            if disptype == 2:
                create_top_50()

            elif disptype == 3 and guest.steuernr == "":
                create_top_50()

            elif disptype == 4 and guest.steuernr != "":
                create_top_50()
    from_date = date_mdy(1, 1, jml)

    if mm == 12:
        to_date = date_mdy(1, 1, jml + timedelta(days=1)) - timedelta(days=1)
    else:
        to_date = date_mdy(mm + 1, 1, jml) - timedelta(days=1)
    for curr_date_loop in date_range(from_date,to_date) :

        genstat_obj_list = {}
        for genstat, res_line, guest in db_session.query(Genstat, Res_line, Guest).join(Res_line,(Res_line.resnr == Genstat.resnr) & (Res_line.reslinnr == Genstat.res_int[inc_value(0)])).join(Guest,(Guest.gastnr == Genstat.gastnr) & (Guest.karteityp == 2)).filter(
                 (Genstat.datum == curr_date_loop) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Guest.gastnr).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            top50_list = query(top50_list_data, filters=(lambda top50_list: top50_list.gastnr == genstat.gastnr), first=True)

            if top50_list:
                top50_list.lytd = top50_list.lytd + 1

    if curr_month != 0:

        for top50_list in query(top50_list_data):
            top50_list.mtd = top50_list.room[curr_month - 1]

    i = 0

    if sorttype == 0:

        for top50_list in query(top50_list_data, filters=(lambda top50_list: top50_list.ytd != 0 or top50_list.lytd != 0), sort_by=[("ytd",True),("bezeich",False)]):
            i = i + 1
            top50_list.nr = i
            top50_list.num = i

    else:

        for top50_list in query(top50_list_data, filters=(lambda top50_list: top50_list.mtd != 0 or top50_list.lytd != 0), sort_by=[("mtd",True),("bezeich",False)]):
            i = i + 1
            top50_list.nr = i
            top50_list.num = i


    for top50_list in query(top50_list_data, filters=(lambda top50_list:(top50_list.nr == 0) or (top50_list.nr > 50))):
        top50_list_data.remove(top50_list)
    top50_list = Top50_list()
    top50_list_data.append(top50_list)

    top50_list.num = 999
    top50_list.bezeich = translateExtended ("T O T A L", lvcarea, "")

    for r_list in query(r_list_data, filters=(lambda r_list: r_list.num >= 1 and r_list.num <= 50)):
        for i in range(1,12 + 1) :
            top50_list.room[i - 1] = top50_list.room[i - 1] + r_list.room[i - 1]
        top50_list.ytd = top50_list.ytd + r_list.ytd
        top50_list.lytd = top50_list.lytd + r_list.lytd
        top50_list.mtd = top50_list.mtd + r_list.room[curr_month - 1]

    return generate_output()