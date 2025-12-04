# using conversion tools version: 1.0.0.119
"""_yusufwijasena_17/11/2025

    Ticket ID: 20FD2B
        _remark_:   - fix python indentation
                    - fix func lower() usage
"""
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

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


def purpose_stat_create_output_webbl(idflag: str, pstay_list_data: list[Pstay_list]):
    doneflag = False
    t_queasy_data = []
    counter: int = 0
    htl_no = ""
    temp_char = ""
    ankunft = ""
    bill_datum = ""
    depart = ""
    queasy = None

    pstay_list = t_queasy = bqueasy = pqueasy = tqueasy = None

    t_queasy_data, T_queasy = create_model_like(Queasy)

    Bqueasy = create_buffer("Bqueasy", Queasy)
    Pqueasy = create_buffer("Pqueasy", Queasy)
    Tqueasy = create_buffer("Tqueasy", Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal doneflag, t_queasy_data, counter, htl_no, temp_char, ankunft, bill_datum, depart, queasy
        nonlocal idflag
        nonlocal bqueasy, pqueasy, tqueasy

        nonlocal pstay_list, t_queasy, bqueasy, pqueasy, tqueasy
        nonlocal t_queasy_data

        return {
            "doneflag": doneflag,
            "pstay-list": pstay_list_data,
            "t-queasy": t_queasy_data
        }

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 280) & ((Queasy.char1).lower() == "purpose stay report") & (Queasy.number1 == 1)).order_by(Queasy.number2).all():

        if queasy.char3 == idflag:
            counter = counter + 1

            if counter > 500:
                break
            pstay_list = Pstay_list()
            pstay_list_data.append(pstay_list)

            pstay_list.purstr = entry(0, queasy.char2, "|")
            pstay_list.room = entry(1, queasy.char2, "|")
            pstay_list.pax = entry(2, queasy.char2, "|")
            pstay_list.logis = entry(3, queasy.char2, "|")
            pstay_list.proz = entry(4, queasy.char2, "|")
            pstay_list.avrgrate = entry(5, queasy.char2, "|")
            pstay_list.m_room = entry(6, queasy.char2, "|")
            pstay_list.m_pax = entry(7, queasy.char2, "|")
            pstay_list.m_logis = entry(8, queasy.char2, "|")
            pstay_list.m_proz = entry(9, queasy.char2, "|")
            pstay_list.m_avrgrate = entry(10, queasy.char2, "|")
            pstay_list.y_room = entry(11, queasy.char2, "|")
            pstay_list.y_pax = entry(12, queasy.char2, "|")
            pstay_list.y_logis = entry(13, queasy.char2, "|")
            pstay_list.y_proz = entry(14, queasy.char2, "|")
            pstay_list.y_avrgrate = entry(15, queasy.char2, "|")
            pstay_list.rmnite = entry(16, queasy.char2, "|")
            pstay_list.rmrev = entry(17, queasy.char2, "|")
            pstay_list.rmnite1 = entry(18, queasy.char2, "|")
            pstay_list.rmrev1 = entry(19, queasy.char2, "|")
            pstay_list.rmcat = entry(20, queasy.char2, "|")

            bqueasy = db_session.query(Bqueasy).filter(
                (Bqueasy._recid == queasy._recid)).first()
            db_session.delete(bqueasy)

    pqueasy = db_session.query(Pqueasy).filter(
        (Pqueasy.key == 280) & ((Pqueasy.char1).lower() == "purpose stay report") & (Pqueasy.char3 == idflag) & (queasy.number1 == 1)).first()

    if pqueasy:
        doneflag = False

    else:

        tqueasy = db_session.query(Tqueasy).filter(
            (Tqueasy.key == 285) & ((Tqueasy.char1).lower() == "purpose stay report") & (Tqueasy.number1 == 1) & (Tqueasy.char2 == idflag)).first()

        if tqueasy:
            doneflag = False

        else:
            doneflag = True

    tqueasy = db_session.query(Tqueasy).filter(
        (Tqueasy.key == 285) & ((Tqueasy.char1).lower() == "purpose stay report") & (Tqueasy.number1 == 0) & (Tqueasy.char2 == idflag)).first()

    if tqueasy:
        db_session.delete(tqueasy)

    if doneflag:

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 280) & ((Queasy.char1).lower() == "purpose stay report") & (Queasy.number1 == 2)).order_by(Queasy.number2).all():
            if queasy.char3 == idflag:
                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = to_int(entry(0, queasy.char2, "|"))
                t_queasy.number1 = to_int(entry(1, queasy.char2, "|"))
                t_queasy.number2 = to_int(entry(2, queasy.char2, "|"))
                t_queasy.number3 = to_int(entry(3, queasy.char2, "|"))
                t_queasy.date1 = date_mdy(entry(4, queasy.char2, "|"))
                t_queasy.date2 = date_mdy(entry(5, queasy.char2, "|"))
                t_queasy.date3 = date_mdy(entry(6, queasy.char2, "|"))
                t_queasy.char1 = entry(7, queasy.char2, "|")
                t_queasy.char2 = entry(8, queasy.char2, "|")
                t_queasy.char3 = entry(9, queasy.char2, "|")
                t_queasy.deci1 = to_decimal(
                    to_decimal(entry(10, queasy.char2, "|")))
                t_queasy.deci2 = to_decimal(
                    to_decimal(entry(11, queasy.char2, "|")))
                t_queasy.deci3 = to_decimal(
                    to_decimal(entry(12, queasy.char2, "|")))
                t_queasy.logi1 = logical(entry(13, queasy.char2, "|"))
                t_queasy.logi2 = logical(entry(14, queasy.char2, "|"))
                t_queasy.logi3 = logical(entry(15, queasy.char2, "|"))
                t_queasy.betriebsnr = to_int(entry(16, queasy.char2, "|"))

                bqueasy = db_session.query(Bqueasy).filter(
                    (Bqueasy._recid == queasy._recid)).first()
                db_session.delete(bqueasy)

    return generate_output()
