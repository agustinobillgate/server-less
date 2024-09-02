from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Genstat, Sourccod, Segment, Nation, Guest

def correct_statistic_check_genstatbl(date1:date, resnr:int, zinr:str):
    genlist_list = []
    genstat = sourccod = segment = nation = guest = None

    genlist = None

    genlist_list, Genlist = create_model_like(Genstat, {"rsv_name":str, "nat_str":str, "ctry_str":str, "source_str":str, "segment_str":str, "rec_gen":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal genlist_list, genstat, sourccod, segment, nation, guest


        nonlocal genlist
        nonlocal genlist_list
        return {"genlist": genlist_list}

    def check_genstat():

        nonlocal genlist_list, genstat, sourccod, segment, nation, guest


        nonlocal genlist
        nonlocal genlist_list


        genlist_list.clear()

        if resnr != 0 and zinr != "":

            for genstat in db_session.query(Genstat).filter(
                    (Genstat.datum == date1) &  (Genstat.resnr == resnr) &  (func.lower(Genstat.(zinr).lower()) == (zinr).lower())).all():
                genlist = Genlist()
                genlist_list.append(genlist)

                buffer_copy(genstat, genlist)
                get_details()

        elif resnr == 0 and zinr != "":

            for genstat in db_session.query(Genstat).filter(
                    (Genstat.datum == date1) &  (func.lower(Genstat.(zinr).lower()) == (zinr).lower())).all():
                genlist = Genlist()
                genlist_list.append(genlist)

                buffer_copy(genstat, genlist)
                get_details()

        else:

            for genstat in db_session.query(Genstat).filter(
                    (Genstat.datum == date1) &  (Genstat.resnr == resnr)).all():
                genlist = Genlist()
                genlist_list.append(genlist)

                buffer_copy(genstat, genlist)
                get_details()


    def get_details():

        nonlocal genlist_list, genstat, sourccod, segment, nation, guest


        nonlocal genlist
        nonlocal genlist_list


        genlist.rec_gen = genstat._recid

        sourccod = db_session.query(Sourccod).filter(
                (Sourccod.source_code == genstat.SOURCE)).first()

        if Sourccod:
            genlist.source_str = Sourccod.bezeich

        segment = db_session.query(Segment).filter(
                (Segment.segmentcode == genstat.segmentcode)).first()

        if segment:
            genlist.segment_str = segment.bezeich

        nation = db_session.query(Nation).filter(
                (Nationnr == genstat.nationnr)).first()

        if nation:
            genlist.nat_str = nation.bezeich

        nation = db_session.query(Nation).filter(
                (Nationnr == genstat.resident)).first()

        if nation:
            genlist.ctry_str = nation.bezeich

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == genstat.gastnr)).first()

        if guest:
            genlist.rsv_name = guest.name


    check_genstat()

    return generate_output()