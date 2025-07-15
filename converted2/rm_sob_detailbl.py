#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Genstat, Guest, Sourccod, Nation

def rm_sob_detailbl(sob:string, ytdflag:int, f_date:date, t_date:date, to_date:date):

    prepare_cache ([Guest, Sourccod, Nation])

    genlist_data = []
    from_date:date = None
    mm:int = 0
    yy:int = 0
    genstat = guest = sourccod = nation = None

    genlist = g_member = None

    genlist_data, Genlist = create_model_like(Genstat, {"rsv_name":string, "nat_str":string, "ctry_str":string, "source_str":string, "rec_gen":int, "arr_date":date, "depart_date":date, "guest_name":string})

    G_member = create_buffer("G_member",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal genlist_data, from_date, mm, yy, genstat, guest, sourccod, nation
        nonlocal sob, ytdflag, f_date, t_date, to_date
        nonlocal g_member


        nonlocal genlist, g_member
        nonlocal genlist_data

        return {"genlist": genlist_data}

    if ytdflag == 2:
        from_date = f_date
        to_date = t_date
    else:
        from_date = f_date
    genlist_data.clear()

    sourccod = get_cache (Sourccod, {"bezeich": [(eq, sob)]})

    if sourccod:

        for genstat in db_session.query(Genstat).filter(
                 (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.source == sourccod.source_code)).order_by(Genstat._recid).all():
            genlist = Genlist()
            genlist_data.append(genlist)

            buffer_copy(genstat, genlist)
            genlist.rec_gen = genstat._recid
            genlist.source = sourccod.source_code
            genlist.source_str = Sourccod.bezeich
            genlist.arr_date = genstat.res_date[0]
            genlist.depart_date = genstat.res_date[1]

            nation = get_cache (Nation, {"nationnr": [(eq, genstat.nationnr)]})

            if nation:
                genlist.nat_str = nation.bezeich

            nation = get_cache (Nation, {"nationnr": [(eq, genstat.resident)]})

            if nation:
                genlist.ctry_str = nation.bezeich

            guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnr)]})

            if guest:
                genlist.rsv_name = guest.name

            g_member = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

            if g_member:
                genlist.guest_name = g_member.name + " " + g_member.vorname1 + ", " + g_member.anrede1


    return generate_output()