from functions.additional_functions import *
import decimal
from functions.artikel_admin_check_btn_exitbl import artikel_admin_check_btn_exitbl
from models import Artikel, Htparam, Waehrung, Hoteldpt, Zwkum, Ekum, Arrangement

def prepare_artikel_adminbl(pvilanguage:int, from_bez:str, dept:int):
    msg_str = ""
    msg_str2 = ""
    local_nr = 0
    foreign_nr = 0
    d_bezeich = ""
    t_artikel_list = []
    lvcarea:str = "artikel_admin"
    p121:int = 0
    artikel = htparam = waehrung = hoteldpt = zwkum = ekum = arrangement = None

    t_artikel = None

    t_artikel_list, T_artikel = create_model_like(Artikel, {"zk_bezeich":str, "ek_bezeich":str, "argt_bez":str, "rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, msg_str2, local_nr, foreign_nr, d_bezeich, t_artikel_list, lvcarea, p121, artikel, htparam, waehrung, hoteldpt, zwkum, ekum, arrangement


        nonlocal t_artikel
        nonlocal t_artikel_list
        return {"msg_str": msg_str, "msg_str2": msg_str2, "local_nr": local_nr, "foreign_nr": foreign_nr, "d_bezeich": d_bezeich, "t-artikel": t_artikel_list}

    def assign_it():

        nonlocal msg_str, msg_str2, local_nr, foreign_nr, d_bezeich, t_artikel_list, lvcarea, p121, artikel, htparam, waehrung, hoteldpt, zwkum, ekum, arrangement


        nonlocal t_artikel
        nonlocal t_artikel_list


        t_artikel = T_artikel()
        t_artikel_list.append(t_artikel)

        buffer_copy(artikel, t_artikel)
        t_artikel.rec_id = artikel._recid

        zwkum = db_session.query(Zwkum).filter(
                (Zwkum.zknr == artikel.zwkum) &  (Zwkum.departement == dept)).first()

        if zwkum:
            t_artikel.zk_bezeich = zwkum.bezeich

        ekum = db_session.query(Ekum).filter(
                (Ekum.eknr == artikel.endkum)).first()

        if ekum:
            t_artikel.ek_bezeich = ekum.bezeich

        arrangement = db_session.query(Arrangement).filter(
                (Arrangement.argtnr == artikel.artgrp)).first()

        if arrangement:
            t_artikel.argt_bez = arrangement.argt_bez
        else:
            t_artikel.argt_bez = "None"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 152)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()

    if not waehrung:
        msg_str = msg_str + chr(2) + translateExtended ("Local Currency Code incorrect! (Param 152 / Grp 7).", lvcarea, "")

        return generate_output()
    local_nr = waehrung.waehrungsnr

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()

    if (not waehrung):
        msg_str = msg_str + chr(2) + translateExtended ("Foreign Currency Code incorrect! (Param 144 / Grp 7)", lvcarea, "")

        return generate_output()
    foreign_nr = waehrung.waehrungsnr

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == dept)).first()
    d_bezeich = hoteldpt.depart

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 121)).first()
    p121 = htparam.finteger


    d_bezeich = d_bezeich + ";" + to_string(p121)

    for artikel in db_session.query(Artikel).filter(
            (Artikel.departement == dept)).all():
        assign_it()
    msg_str2 = get_output(artikel_admin_check_btn_exitbl(pvilanguage))

    return generate_output()