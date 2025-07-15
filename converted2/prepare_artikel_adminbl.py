#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.artikel_admin_check_btn_exitbl import artikel_admin_check_btn_exitbl
from models import Artikel, Htparam, Waehrung, Hoteldpt, Zwkum, Ekum, Arrangement

def prepare_artikel_adminbl(pvilanguage:int, from_bez:string, dept:int):

    prepare_cache ([Htparam, Waehrung, Hoteldpt, Zwkum, Ekum, Arrangement])

    msg_str = ""
    msg_str2 = ""
    local_nr = 0
    foreign_nr = 0
    d_bezeich = ""
    t_artikel_data = []
    lvcarea:string = "artikel-admin"
    p121:int = 0
    artikel = htparam = waehrung = hoteldpt = zwkum = ekum = arrangement = None

    t_artikel = None

    t_artikel_data, T_artikel = create_model_like(Artikel, {"zk_bezeich":string, "ek_bezeich":string, "argt_bez":string, "rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, msg_str2, local_nr, foreign_nr, d_bezeich, t_artikel_data, lvcarea, p121, artikel, htparam, waehrung, hoteldpt, zwkum, ekum, arrangement
        nonlocal pvilanguage, from_bez, dept


        nonlocal t_artikel
        nonlocal t_artikel_data

        return {"msg_str": msg_str, "msg_str2": msg_str2, "local_nr": local_nr, "foreign_nr": foreign_nr, "d_bezeich": d_bezeich, "t-artikel": t_artikel_data}

    def assign_it():

        nonlocal msg_str, msg_str2, local_nr, foreign_nr, d_bezeich, t_artikel_data, lvcarea, p121, artikel, htparam, waehrung, hoteldpt, zwkum, ekum, arrangement
        nonlocal pvilanguage, from_bez, dept


        nonlocal t_artikel
        nonlocal t_artikel_data


        t_artikel = T_artikel()
        t_artikel_data.append(t_artikel)

        buffer_copy(artikel, t_artikel)
        t_artikel.rec_id = artikel._recid

        zwkum = get_cache (Zwkum, {"zknr": [(eq, artikel.zwkum)],"departement": [(eq, dept)]})

        if zwkum:
            t_artikel.zk_bezeich = zwkum.bezeich

        ekum = get_cache (Ekum, {"eknr": [(eq, artikel.endkum)]})

        if ekum:
            t_artikel.ek_bezeich = ekum.bezeich

        arrangement = get_cache (Arrangement, {"argtnr": [(eq, artikel.artgrp)]})

        if arrangement:
            t_artikel.argt_bez = arrangement.argt_bez
        else:
            t_artikel.argt_bez = "None"


    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if not waehrung:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Local Currency Code incorrect! (Param 152 / Grp 7).", lvcarea, "")

        return generate_output()
    local_nr = waehrung.waehrungsnr

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if (not waehrung):
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Foreign Currency Code incorrect! (Param 144 / Grp 7)", lvcarea, "")

        return generate_output()
    foreign_nr = waehrung.waehrungsnr

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept)]})
    d_bezeich = hoteldpt.depart

    htparam = get_cache (Htparam, {"paramnr": [(eq, 121)]})
    p121 = htparam.finteger


    d_bezeich = d_bezeich + ";" + to_string(p121)

    for artikel in db_session.query(Artikel).filter(
             (Artikel.departement == dept)).order_by(Artikel._recid).all():
        assign_it()
    msg_str2 = get_output(artikel_admin_check_btn_exitbl(pvilanguage))

    return generate_output()