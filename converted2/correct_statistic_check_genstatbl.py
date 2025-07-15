#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Genstat, Sourccod, Segment, Nation, Guest

def correct_statistic_check_genstatbl(date1:date, resnr:int, zinr:string):

    prepare_cache ([Segment, Nation, Guest])

    genlist_data = []
    genstat = sourccod = segment = nation = guest = None

    genlist = None

    genlist_data, Genlist = create_model_like(Genstat, {"rsv_name":string, "nat_str":string, "ctry_str":string, "source_str":string, "segment_str":string, "rec_gen":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal genlist_data, genstat, sourccod, segment, nation, guest
        nonlocal date1, resnr, zinr


        nonlocal genlist
        nonlocal genlist_data

        return {"genlist": genlist_data}

    def check_genstat():

        nonlocal genlist_data, genstat, sourccod, segment, nation, guest
        nonlocal date1, resnr, zinr


        nonlocal genlist
        nonlocal genlist_data


        genlist_data.clear()

        if resnr != 0 and zinr != "":

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum == date1) & (Genstat.resnr == resnr) & (Genstat.zinr == (zinr).lower())).order_by(Genstat._recid).all():
                genlist = Genlist()
                genlist_data.append(genlist)

                buffer_copy(genstat, genlist)
                get_details()

        elif resnr == 0 and zinr != "":

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum == date1) & (Genstat.zinr == (zinr).lower())).order_by(Genstat._recid).all():
                genlist = Genlist()
                genlist_data.append(genlist)

                buffer_copy(genstat, genlist)
                get_details()

        else:

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum == date1) & (Genstat.resnr == resnr)).order_by(Genstat._recid).all():
                genlist = Genlist()
                genlist_data.append(genlist)

                buffer_copy(genstat, genlist)
                get_details()

    def get_details():

        nonlocal genlist_data, genstat, sourccod, segment, nation, guest
        nonlocal date1, resnr, zinr


        nonlocal genlist
        nonlocal genlist_data


        genlist.rec_gen = genstat._recid

        sourccod = get_cache (Sourccod, {"source_code": [(eq, genstat.source)]})

        if Sourccod:
            genlist.source_str = Sourccod.bezeich

        segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

        if segment:
            genlist.segment_str = segment.bezeich

        nation = get_cache (Nation, {"nationnr": [(eq, genstat.nationnr)]})

        if nation:
            genlist.nat_str = nation.bezeich

        nation = get_cache (Nation, {"nationnr": [(eq, genstat.resident)]})

        if nation:
            genlist.ctry_str = nation.bezeich

        guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnr)]})

        if guest:
            genlist.rsv_name = guest.name

    check_genstat()

    return generate_output()