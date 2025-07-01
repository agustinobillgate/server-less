#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Artikel, Zwkum, Ekum, Arrangement, Argt_line

def artikel_adminbl(pvilanguage:int, case_type:int, dept:int, artno:int):

    prepare_cache ([Zwkum, Ekum, Arrangement, Argt_line])

    msg_str = ""
    t_artikel_list = []
    lvcarea:string = "artikel-admin"
    artikel = zwkum = ekum = arrangement = argt_line = None

    t_artikel = None

    t_artikel_list, T_artikel = create_model_like(Artikel, {"zk_bezeich":string, "ek_bezeich":string, "argt_bez":string, "rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, t_artikel_list, lvcarea, artikel, zwkum, ekum, arrangement, argt_line
        nonlocal pvilanguage, case_type, dept, artno


        nonlocal t_artikel
        nonlocal t_artikel_list

        return {"msg_str": msg_str, "t-artikel": t_artikel_list}

    def assign_it():

        nonlocal msg_str, t_artikel_list, lvcarea, artikel, zwkum, ekum, arrangement, argt_line
        nonlocal pvilanguage, case_type, dept, artno


        nonlocal t_artikel
        nonlocal t_artikel_list


        t_artikel = T_artikel()
        t_artikel_list.append(t_artikel)

        buffer_copy(artikel, t_artikel)

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


    def check_argt():

        nonlocal msg_str, t_artikel_list, lvcarea, artikel, zwkum, ekum, arrangement, argt_line
        nonlocal pvilanguage, case_type, dept, artno


        nonlocal t_artikel
        nonlocal t_artikel_list

        argt_line = get_cache (Argt_line, {"departement": [(eq, dept)],"argt_artnr": [(eq, artno)]})

        if argt_line:

            arrangement = get_cache (Arrangement, {"argtnr": [(eq, argt_line.argtnr)]})

            if arrangement:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Wrong Article type as arrangement found using this article", lvcarea, "") + " " + arrangement.arrangement
            else:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("argt-line record exists for this article number!", lvcarea, "")

            return


    if case_type == 2:
        check_argt()

        return generate_output()

    for artikel in db_session.query(Artikel).filter(
             (Artikel.departement == dept)).order_by(Artikel._recid).all():
        assign_it()

    return generate_output()