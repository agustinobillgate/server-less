# using conversion tools version: 1.0.0.119
"""_yusufwijasena_13/11/2025

    Ticket ID: 62BADE
        _remark_:   - fix python indentation
                    - only convert to py
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Ratecode, Zimkateg


def if_lodgiq_get_ratebl():

    prepare_cache([Ratecode, Zimkateg])

    temp_room: string = ""
    t_ratecode_data = []
    ratecode = zimkateg = None

    t_ratecode = None

    t_ratecode_data, T_ratecode = create_model(
        "T_ratecode",
        {
            "rcode": string,
            "roomtype": string,
            "enddate": date,
            "startdate": date,
            "adult": int,
            "child": int,
            "roomrate": Decimal
        })

    db_session = local_storage.db_session

    def generate_output():
        nonlocal temp_room, t_ratecode_data, ratecode, zimkateg
        nonlocal t_ratecode
        nonlocal t_ratecode_data

        return {
            "t-ratecode": t_ratecode_data
        }

    for ratecode in db_session.query(Ratecode).filter(
            (Ratecode.startperiode != None) & (Ratecode.endperiode != None)).order_by(Ratecode._recid).all():

        zimkateg = get_cache(
            Zimkateg, {"zikatnr": [(eq, ratecode.zikatnr), (ne, 0)]})

        if zimkateg:
            temp_room = zimkateg.kurzbez

        t_ratecode = T_ratecode()
        t_ratecode_data.append(t_ratecode)

        t_ratecode.rcode = ratecode.code
        t_ratecode.roomtype = temp_room
        t_ratecode.enddate = ratecode.endperiode
        t_ratecode.startdate = ratecode.startperiode
        t_ratecode.adult = ratecode.erwach
        t_ratecode.child = ratecode.kind1
        t_ratecode.roomrate = to_decimal(ratecode.zipreis)

    return generate_output()
