from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Genstat, Bediener, Segment, Res_line, Res_history

def correct_statistic_btn_updatebl(genlist:[Genlist], rec_gen:int, user_init:str):
    genstat = bediener = segment = res_line = res_history = None

    genlist = None

    genlist_list, Genlist = create_model_like(Genstat, {"rsv_name":str, "nat_str":str, "ctry_str":str, "source_str":str, "segment_str":str, "rec_gen":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal genstat, bediener, segment, res_line, res_history


        nonlocal genlist
        nonlocal genlist_list
        return {}

    def res_history():

        nonlocal genstat, bediener, segment, res_line, res_history


        nonlocal genlist
        nonlocal genlist_list

        temp_segment:str = ""

        segment = db_session.query(Segment).filter(
                (Segment.segmentcode == genstat.segmentcode)).first()

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == genlist.resnr)).first()
        temp_segment = segment.bezeich
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.resnr = genlist.resnr
        res_history.reslinnr = res_line.reslinnr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.action = "Segment"
        res_history.aenderung = "Reservation " + to_string(genlist.resnr) + ", Segment has been changed from " +\
                temp_segment + " to " + genlist.segment_str

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    genlist = query(genlist_list, first=True)
    while None != genlist:

        genstat = db_session.query(Genstat).filter(
                    (Genstat._recid == genlist.rec_gen)).first()
        res_history()
        buffer_copy(genlist, genstat,except_fields=["genlist.datum","genlist.zinr"])

        genstat = db_session.query(Genstat).first()

        genlist = query(genlist_list, next=True)


    return generate_output()