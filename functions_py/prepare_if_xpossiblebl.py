# using conversion tools version: 1.0.0.119
"""_yusufwijasena_14/11/2025

    Ticket ID: 645147
        _remark_:   - fix python indentation
                    - only convert to py
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Htparam, History, Guest


def prepare_if_xpossiblebl(i_resnr: int, i_reslinnr: int):

    prepare_cache([Res_line, Htparam, History, Guest])

    t_wifi_data = []
    co_time: Decimal = 12
    depart_time: int = 0
    vip = ""
    vipnr1: int = 999999999
    vipnr2: int = 999999999
    vipnr3: int = 999999999
    vipnr4: int = 999999999
    vipnr5: int = 999999999
    vipnr6: int = 999999999
    vipnr7: int = 999999999
    vipnr8: int = 999999999
    vipnr9: int = 999999999
    res_line = htparam = history = guest = None

    t_wifi = t_resline = None

    t_wifi_data, T_wifi = create_model(
        "T_wifi",
        {
            "roomno": str,
            "firstname": str,
            "lastname": str,
            "gname": str,
            "cidate": date,
            "codate": date,
            "cotime": int,
            "gtype": int,
            "gnumber": int
        })

    T_resline = create_buffer("T_resline", Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_wifi_data, co_time, depart_time, vip, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, res_line, htparam, history, guest
        nonlocal i_resnr, i_reslinnr
        nonlocal t_resline
        nonlocal t_wifi, t_resline
        nonlocal t_wifi_data

        return {
            "t-wifi": t_wifi_data
        }

    htparam = get_cache(Htparam, {"paramnr": [(eq, 700)]})

    if htparam.finteger != 0:
        vipnr1 = htparam.finteger

    htparam = get_cache(Htparam, {"paramnr": [(eq, 701)]})

    if htparam.finteger != 0:
        vipnr2 = htparam.finteger

    htparam = get_cache(Htparam, {"paramnr": [(eq, 702)]})

    if htparam.finteger != 0:
        vipnr3 = htparam.finteger

    htparam = get_cache(Htparam, {"paramnr": [(eq, 703)]})

    if htparam.finteger != 0:
        vipnr4 = htparam.finteger

    htparam = get_cache(Htparam, {"paramnr": [(eq, 704)]})

    if htparam.finteger != 0:
        vipnr5 = htparam.finteger

    htparam = get_cache(Htparam, {"paramnr": [(eq, 705)]})

    if htparam.finteger != 0:
        vipnr6 = htparam.finteger

    htparam = get_cache(Htparam, {"paramnr": [(eq, 706)]})

    if htparam.finteger != 0:
        vipnr7 = htparam.finteger

    htparam = get_cache(Htparam, {"paramnr": [(eq, 707)]})

    if htparam.finteger != 0:
        vipnr8 = htparam.finteger

    htparam = get_cache(Htparam, {"paramnr": [(eq, 708)]})

    if htparam.finteger != 0:
        vipnr9 = htparam.finteger

    t_resline = get_cache(
        Res_line, {"resnr": [(eq, i_resnr)], "reslinnr": [(eq, i_reslinnr)]})

    if t_resline:
        if t_resline.resstatus <= 6:
            res_line = get_cache(Res_line, {"resnr": [(eq, t_resline.resnr)], "reslinnr": [(eq, t_resline.reslinnr)]})
        else:
            res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == t_resline.resnr) & (Res_line.reslinnr < t_resline.reslinnr) & (Res_line.zinr == t_resline.zinr)).first()

    if res_line:
        history = db_session.query(History).filter(
            (History.resnr == res_line.resnr) & (History.reslinnr == res_line.reslinnr)).order_by(History._recid.desc()).first()

        if res_line.betrieb_gastmem == vipnr1 or res_line.betrieb_gastmem == vipnr2 or res_line.betrieb_gastmem == vipnr3 or res_line.betrieb_gastmem == vipnr4 or res_line.betrieb_gastmem == vipnr5 or res_line.betrieb_gastmem == vipnr6 or res_line.betrieb_gastmem == vipnr7 or res_line.betrieb_gastmem == vipnr8 or res_line.betrieb_gastmem == vipnr9:
            vip = "V"
        depart_time = res_line.abreisezeit

        if depart_time == 0:
            htparam = get_cache(Htparam, {"paramnr": [(eq, 925)]})
            co_time = to_int(substring(htparam.fchar, 0, 2)) + to_int(substring(htparam.fchar, 3, 2)) / 60
            depart_time = co_time * 3600

        guest = get_cache(Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        if (res_line.resstatus <= 6 or res_line.resstatus == 8):
            t_wifi = T_wifi()
            t_wifi_data.append(t_wifi)

            t_wifi.roomno = res_line.zinr
            t_wifi.firstname = guest.vorname1
            t_wifi.lastname = guest.vorname2
            t_wifi.cidate = res_line.ankunft
            t_wifi.codate = res_line.abreise
            t_wifi.cotime = depart_time
            t_wifi.gname = guest.name
            t_wifi.gnumber = guest.gastnr

            if history and history.zinr != "" and history.zinr != res_line.zinr:
                t_wifi.roomno = t_wifi.roomno + ";" + history.zinr

            if vip.lower() == "v":
                t_wifi.gtype = 1
            else:
                t_wifi.gtype = 0

    return generate_output()
