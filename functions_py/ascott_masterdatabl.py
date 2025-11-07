# using conversion tools version: 1.0.0.119
"""_yusufwijasena_07/11/2025

    Ticket ID: 5C46F2
        _remark_:   - update from ITA: BFC578
                    - fix python indentation
"""
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Zimkateg, Sourccod, Segment

ratecode_list_data, Ratecode_list = create_model(
    "Ratecode_list",
    {
        "ascott_code": str,
        "rate_code": str,
        "rate_desc": str
    })
roomtype_list_data, Roomtype_list = create_model(
    "Roomtype_list",
    {
        "ascott_code": str,
        "roomtype_code": str,
        "roomtype_desc": str,
        "roomtype_group": str,
        "roomtype_groupdesc": str
    })
sob_list_data, Sob_list = create_model(
    "Sob_list",
    {
        "ascott_code": str,
        "sob_code": str,
        "sob_desc": str
    })
segment_list_data, Segment_list = create_model(
    "Segment_list",
    {
        "ascott_code": str,
        "segment_code": str,
        "segment_name": str
    })


def ascott_masterdatabl(propid: str, ratecode_list_data: Ratecode_list, roomtype_list_data: Roomtype_list, sob_list_data: Sob_list, segment_list_data: Segment_list):

    prepare_cache([Queasy, Zimkateg, Segment])

    data_count = 0
    queasy = zimkateg = sourccod = segment = None
    ratecode_list = roomtype_list = sob_list = segment_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal data_count, queasy, zimkateg, sourccod, segment
        nonlocal propid
        nonlocal ratecode_list, roomtype_list, sob_list, segment_list

        return {
            "data_count": data_count,
            "ratecode-list": ratecode_list_data,
            "roomtype-list": roomtype_list_data,
            "sob-list": sob_list_data,
            "segment-list": segment_list_data
        }

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 2)).order_by(Queasy.char1).all():

        # start - ITA: BFC578
        if not matches(trim(queasy.char1), r"(cp)*") and not matches(trim(queasy.char1), r"(np)*"):
            ratecode_list = Ratecode_list()
            ratecode_list_data.append(ratecode_list)

            ratecode_list.ascott_code = propid
            ratecode_list.rate_code = trim(queasy.char1)
            ratecode_list.rate_desc = trim(queasy.char2)
        # end - ITA: BFC578

    for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
        roomtype_list = Roomtype_list()
        roomtype_list_data.append(roomtype_list)

        roomtype_list.ascott_code = propid
        roomtype_list.roomtype_code = zimkateg.kurzbez
        roomtype_list.roomtype_desc = zimkateg.bezeichnung
        roomtype_list.roomtype_group = "Standard Rooms"
        roomtype_list.roomtype_groupdesc = "Rooms"

    for sourccod in db_session.query(Sourccod).filter(
            (Sourccod.betriebsnr == 0)).order_by(Sourccod._recid).all():
        sob_list = query(sob_list_data, filters=(
            lambda sob_list: sob_list.sob_code == to_string(Sourccod.source_code)), first=True)

        if not sob_list:
            sob_list = Sob_list()
            sob_list_data.append(sob_list)

            sob_list.ascott_code = propid
            sob_list.sob_code = Sourccod.bezeich
            sob_list.sob_desc = Sourccod.bezeich

    for segment in db_session.query(Segment).order_by(Segment._recid).all():
        segment_list = query(segment_list_data, filters=(
            lambda segment_list: segment_list.segment_code == segment.bezeich), first=True)

        if not segment_list:
            segment_list = Segment_list()
            segment_list_data.append(segment_list)

            segment_list.ascott_code = propid
            segment_list.segment_code = segment.bezeich
            segment_list.segment_name = segment.bemerkung

    return generate_output()
