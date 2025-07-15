#using conversion tools version: 1.0.0.105

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Zimkateg, Sourccod, Segment

ratecode_list_list, Ratecode_list = create_model("Ratecode_list", {"ascott_code":string, "rate_code":string, "rate_desc":string})
roomtype_list_list, Roomtype_list = create_model("Roomtype_list", {"ascott_code":string, "roomtype_code":string, "roomtype_desc":string, "roomtype_group":string, "roomtype_groupdesc":string})
sob_list_list, Sob_list = create_model("Sob_list", {"ascott_code":string, "sob_code":string, "sob_desc":string})
segment_list_list, Segment_list = create_model("Segment_list", {"ascott_code":string, "segment_code":string, "segment_name":string})

def ascott_masterdatabl(propid:string, ratecode_list_list:[Ratecode_list], roomtype_list_list:[Roomtype_list], sob_list_list:[Sob_list], segment_list_list:[Segment_list]):

    prepare_cache ([Queasy, Zimkateg, Segment])

    data_count = 0
    queasy = zimkateg = sourccod = segment = None

    ratecode_list = roomtype_list = sob_list = segment_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal data_count, queasy, zimkateg, sourccod, segment
        nonlocal propid


        nonlocal ratecode_list, roomtype_list, sob_list, segment_list

        return {"data_count": data_count, "ratecode-list": ratecode_list_list, "roomtype-list": roomtype_list_list, "sob-list": sob_list_list, "segment-list": segment_list_list}


    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 2)).order_by(Queasy.char1).all():
        ratecode_list = Ratecode_list()
        ratecode_list_list.append(ratecode_list)

        ratecode_list.ascott_code = propid
        ratecode_list.rate_code = trim(queasy.char1)
        ratecode_list.rate_desc = trim(queasy.char2)

    for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
        roomtype_list = Roomtype_list()
        roomtype_list_list.append(roomtype_list)

        roomtype_list.ascott_code = propid
        roomtype_list.roomtype_code = zimkateg.kurzbez
        roomtype_list.roomtype_desc = zimkateg.bezeichnung
        roomtype_list.roomtype_group = "Standard Rooms"
        roomtype_list.roomtype_groupdesc = "Rooms"

    for sourccod in db_session.query(Sourccod).filter(
             (Sourccod.betriebsnr == 0)).order_by(Sourccod._recid).all():

        sob_list = query(sob_list_list, filters=(lambda sob_list: sob_list.sob_code == to_string(Sourccod.source_code)), first=True)

        if not sob_list:
            sob_list = Sob_list()
            sob_list_list.append(sob_list)

            sob_list.ascott_code = propid
            sob_list.sob_code = Sourccod.bezeich
            sob_list.sob_desc = Sourccod.bezeich

    for segment in db_session.query(Segment).order_by(Segment._recid).all():

        segment_list = query(segment_list_list, filters=(lambda segment_list: segment_list.segment_code == segment.bezeich), first=True)

        if not segment_list:
            segment_list = Segment_list()
            segment_list_list.append(segment_list)

            segment_list.ascott_code = propid
            segment_list.segment_code = segment.bezeich
            segment_list.segment_name = segment.bemerkung

    return generate_output()