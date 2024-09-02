from functions.additional_functions import *
import decimal
from models import Artikel, Zwkum, Ekum, Arrangement, Argt_line

def artikel_adminbl(pvilanguage:int, case_type:int, dept:int, artno:int):
    msg_str = ""
    t_artikel_list = []
    lvcarea:str = "artikel_admin"
    artikel = zwkum = ekum = arrangement = argt_line = None

    t_artikel = None

    t_artikel_list, T_artikel = create_model_like(Artikel, {"zk_bezeich":str, "ek_bezeich":str, "argt_bez":str, "rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, t_artikel_list, lvcarea, artikel, zwkum, ekum, arrangement, argt_line


        nonlocal t_artikel
        nonlocal t_artikel_list
        return {"msg_str": msg_str, "t-artikel": t_artikel_list}

    def assign_it():

        nonlocal msg_str, t_artikel_list, lvcarea, artikel, zwkum, ekum, arrangement, argt_line


        nonlocal t_artikel
        nonlocal t_artikel_list


        t_artikel = T_artikel()
        t_artikel_list.append(t_artikel)

        buffer_copy(artikel, t_artikel)

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

    def check_argt():

        nonlocal msg_str, t_artikel_list, lvcarea, artikel, zwkum, ekum, arrangement, argt_line


        nonlocal t_artikel
        nonlocal t_artikel_list

        argt_line = db_session.query(Argt_line).filter(
                (Argt_line.departement == dept) &  (Argt_line.argt_artnr == artno)).first()

        if argt_line:

            arrangement = db_session.query(Arrangement).filter(
                    (Arrangement.argtnr == argt_line.argtnr)).first()

            if arrangement:
                msg_str = msg_str + chr(2) + translateExtended ("Wrong Article type as arrangement found using this article", lvcarea, "") + " " + arrangement
            else:
                msg_str = msg_str + chr(2) + translateExtended ("argt_line record exists for this article number!", lvcarea, "")

            return

    if case_type == 2:
        check_argt()

        return generate_output()

    for artikel in db_session.query(Artikel).filter(
            (Artikel.departement == dept)).all():
        assign_it()

    return generate_output()