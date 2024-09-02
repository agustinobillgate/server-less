from functions.additional_functions import *
import decimal
from datetime import date
from models import Guest, Genstat

def top50_tareportbl(pvilanguage:int, curr_date:str, curr_month:int, sorttype:int):
    top50_list_list = []
    mm:int = 0
    yy:int = 0
    i:int = 0
    from_date:date = None
    to_date:date = None
    datum:date = None
    lvcarea:str = "comp_product"
    guest = genstat = None

    top50_list = r_list = None

    top50_list_list, Top50_list = create_model("Top50_list", {"num":int, "nr":int, "bezeich":str, "room":[int, 12], "ytd":int, "lytd":int, "mtd":int, "gastnr":int})

    R_list = Top50_list
    r_list_list = top50_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal top50_list_list, mm, yy, i, from_date, to_date, datum, lvcarea, guest, genstat
        nonlocal r_list


        nonlocal top50_list, r_list
        nonlocal top50_list_list
        return {"top50-list": top50_list_list}


    top50_list_list.clear()
    r_list_list.clear()
    mm = to_int(substring(curr_date, 0, 2))
    yy = to_int(substring(curr_date, 2, 4))

    genstat_obj_list = []
    for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
            (get_year(Genstat.datum) == yy) &  (get_month(Genstat.datum) <= mm) &  (Genstat.zinr != "") &  (Genstat.karteityp == 2) &  (Genstat.res_logic[1])).all():
        if genstat._recid in genstat_obj_list:
            continue
        else:
            genstat_obj_list.append(genstat._recid)

        top50_list = query(top50_list_list, filters=(lambda top50_list :top50_list.gastnr == genstat.gastnr), first=True)

        if not top50_list:
            top50_list = Top50_list()
            top50_list_list.append(top50_list)

            top50_list.gastnr = genstat.gastnr
            top50_list.bezeich = guest.name

        if genstat.resstatus != 13:
            top50_list.room[get_month(genstat.datum) - 1] = top50_list.room[get_month(genstat.datum) - 1] + 1
            top50_list.ytd = top50_list.ytd + 1

    for top50_list in query(top50_list_list):

        for genstat in db_session.query(Genstat).filter(
                (Genstat.gastnr == top50_list.gastnr) &  (get_year(Genstat.datum) == yy - 1) &  (get_month(Genstat.datum) <= mm) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():

            if genstat.resstatus != 13:
                top50_list.lytd = top50_list.lytd + 1

    if curr_month != 0:

        for top50_list in query(top50_list_list):
            top50_list.mtd = top50_list.room[curr_month - 1]

    i = 0

    if sorttype == 0:

        for top50_list in query(top50_list_list, filters=(lambda top50_list :top50_list.ytd != 0)):
            i = i + 1
            top50_list.nr = i
            top50_list.num = i

    else:

        for top50_list in query(top50_list_list, filters=(lambda top50_list :top50_list.mtd != 0)):
            i = i + 1
            top50_list.nr = i
            top50_list.num = i


    for top50_list in query(top50_list_list, filters=(lambda top50_list :(top50_list.nr == 0) or (top50_list.nr > 50))):
        top50_list_list.remove(top50_list)
    top50_list = Top50_list()
    top50_list_list.append(top50_list)

    top50_list.num = 999
    top50_list.bezeich = translateExtended ("T O T A L", lvcarea, "")

    for r_list in query(r_list_list, filters=(lambda r_list :r_list.num <= 50)):
        for i in range(1,12 + 1) :
            top50_list.room[i - 1] = top50_list.room[i - 1] + r_list.room[i - 1]
        top50_list.ytd = top50_list.ytd + r_list.ytd
        top50_list.lytd = top50_list.lytd + r_list.lytd

    return generate_output()