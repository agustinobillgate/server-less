# using conversion tools version: 1.0.0.119
"""_yusufwijasena_17/11/2025

    Ticket ID: 20FD2B
        _remark_:   - fix python indentation
                    - only converted to python
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.purpose_stat_cldbl import purpose_stat_cldbl
from models import Queasy

payload_list_data, Payload_list = create_model(
    "Payload_list",
    {
        "display_opt": int,
        "idflag": string
    })


def purpose_stat2_webbl(pvilanguage: int, mi_comp1: bool, mi_ftd1: bool, f_date: date, t_date: date, to_date: date, cardtype: int, price_decimal: int, payload_list_data: list[Payload_list]):

    prepare_cache([Queasy])

    pstay_list_data = []
    t_queasy_data = []
    counter: int = 0
    queasy = None

    pstay_list = s_list = t_queasy = payload_list = bqueasy = tqueasy = None

    pstay_list_data, Pstay_list = create_model(
        "Pstay_list",
        {
            "flag": int,
            "purstr": str,
            "room": str,
            "pax": str,
            "logis": str,
            "proz": str,
            "avrgrate": str,
            "m_room": str,
            "m_pax": str,
            "m_logis": str,
            "m_proz": str,
            "m_avrgrate": str,
            "y_room": str,
            "y_pax": str,
            "y_logis": str,
            "y_proz": str,
            "y_avrgrate": str,
            "rmnite1": str,
            "rmrev1": str,
            "rmnite": str,
            "rmrev": str,
            "rmcat": str,
            "segment": str
        })
    s_list_data, S_list = create_model(
        "S_list",
        {
            "catnr": int,
            "purnr": int,
            "purstr": str,
            "rmcat": str,
            "cat_bez": str,
            "room": int,
            "c_room": int,
            "pax": int,
            "logis": Decimal,
            "proz": Decimal,
            "avrgrate": Decimal,
            "m_room": int,
            "mc_room": int,
            "m_pax": int,
            "m_logis": Decimal,
            "m_proz": Decimal,
            "m_avrgrate": Decimal,
            "y_room": int,
            "yc_room": int,
            "y_pax": int,
            "y_logis": Decimal,
            "y_proz": Decimal,
            "y_avrgrate": Decimal,
            "nat_kurbez": str,
            "nat_bezeich": str,
            "domestic": int
        })
    t_queasy_data, T_queasy = create_model_like(Queasy)

    Bqueasy = create_buffer("Bqueasy", Queasy)
    Tqueasy = create_buffer("Tqueasy", Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal pstay_list_data, t_queasy_data, counter, queasy
        nonlocal pvilanguage, mi_comp1, mi_ftd1, f_date, t_date, to_date, cardtype, price_decimal
        nonlocal bqueasy, tqueasy
        nonlocal pstay_list, s_list, t_queasy, payload_list, bqueasy, tqueasy
        nonlocal pstay_list_data, s_list_data, t_queasy_data

        return {
            "pstay-list": pstay_list_data,
            "t-queasy": t_queasy_data
        }

    payload_list = query(payload_list_data, first=True)
    queasy = Queasy()
    db_session.add(queasy)

    queasy.key = 285
    queasy.char1 = "Purpose Stay Report"
    queasy.number1 = 1
    queasy.char2 = payload_list.idFlag

    pstay_list_data, t_queasy_data = get_output(purpose_stat_cldbl(
        pvilanguage, mi_comp1, mi_ftd1, f_date, t_date, to_date, cardtype, price_decimal, payload_list.display_opt, payload_list.idFlag))

    pstay_list = query(pstay_list_data, first=True)
    while pstay_list is not None:

        if pstay_list.purstr == None:
            pstay_list.purstr = ""
        counter = counter + 1
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 280
        queasy.char1 = "Purpose Stay Report"
        queasy.char3 = payload_list.idFlag
        queasy.number1 = 1
        queasy.char2 = pstay_list.purstr + "|" +\
            pstay_list.room + "|" +\
            pstay_list.pax + "|" +\
            pstay_list.logis + "|" +\
            pstay_list.proz + "|" +\
            pstay_list.avrgrate + "|" +\
            pstay_list.m_room + "|" +\
            pstay_list.m_pax + "|" +\
            pstay_list.m_logis + "|" +\
            pstay_list.m_proz + "|" +\
            pstay_list.m_avrgrate + "|" +\
            pstay_list.y_room + "|" +\
            pstay_list.y_pax + "|" +\
            pstay_list.y_logis + "|" +\
            pstay_list.y_proz + "|" +\
            pstay_list.y_avrgrate + "|" +\
            pstay_list.rmnite + "|" +\
            pstay_list.rmrev + "|" +\
            pstay_list.rmnite1 + "|" +\
            pstay_list.rmrev1 + "|" +\
            pstay_list.rmcat

        queasy.number2 = to_int(counter)
        pstay_list_data.remove(pstay_list)

        pstay_list = query(pstay_list_data, next=True)
    counter = 0

    t_queasy = query(t_queasy_data, first=True)
    while t_queasy is not None:
        counter = counter + 1
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 280
        queasy.char1 = "Purpose Stay Report"
        queasy.char3 = payload_list.idFlag
        queasy.number1 = 2
        queasy.char2 = to_string(t_queasy.key) + "|" +\
            to_string(t_queasy.number1) + "|" +\
            to_string(t_queasy.number2) + "|" +\
            to_string(t_queasy.number3) + "|" +\
            to_string(t_queasy.date1) + "|" +\
            to_string(t_queasy.date2) + "|" +\
            to_string(t_queasy.date3) + "|" +\
            to_string(t_queasy.char1) + "|" +\
            to_string(t_queasy.char2) + "|" +\
            to_string(t_queasy.char3) + "|" +\
            to_string(t_queasy.deci1) + "|" +\
            to_string(t_queasy.deci2) + "|" +\
            to_string(t_queasy.deci3) + "|" +\
            to_string(t_queasy.logi1) + "|" +\
            to_string(t_queasy.logi2) + "|" +\
            to_string(t_queasy.logi3) + "|" +\
            to_string(t_queasy.betriebsnr)

        queasy.number2 = to_int(counter)
        t_queasy_data.remove(t_queasy)

        t_queasy = query(t_queasy_data, next=True)

    bqueasy = get_cache(
        Queasy, {"key": [(eq, 285)], "char1": [(eq, "purpose stay report")], "char2": [(eq, payload_list.idflag)]})

    if bqueasy:
        bqueasy.number1 = 0

    return generate_output()
