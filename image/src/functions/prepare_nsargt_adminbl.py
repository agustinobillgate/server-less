from functions.additional_functions import *
import decimal
from models import Arrangement, Artikel, Argt_line, Hoteldpt

def prepare_nsargt_adminbl():
    q1_list_list = []
    q2_list_list = []
    t_hoteldpt_list = []
    arrangement = artikel = argt_line = hoteldpt = None

    q1_list = q2_list = t_hoteldpt = None

    q1_list_list, Q1_list = create_model("Q1_list", {"rec_id":int, "argtnr":int, "arrangement":str, "argt_bez":str, "artnr_logis":int, "intervall":int, "argt_artikelnr":int, "zuordnung":str})
    q2_list_list, Q2_list = create_model("Q2_list", {"rec_id":int, "argtnr":int, "departement":int, "argt_artnr":int, "bezeich":str, "artnr":int, "betrag":decimal, "vt_percnt":decimal})
    t_hoteldpt_list, T_hoteldpt = create_model("T_hoteldpt", {"num":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_list, q2_list_list, t_hoteldpt_list, arrangement, artikel, argt_line, hoteldpt

        nonlocal q1_list, q2_list, t_hoteldpt
        nonlocal q1_list_list, q2_list_list, t_hoteldpt_list
        return {"q1-list": q1_list_list, "q2-list": q2_list_list, "t-hoteldpt": t_hoteldpt_list}

    for arrangement in db_session.query(Arrangement).filter(
            (Arrangement.segmentcode == 1)).all():
        q1_list = Q1_list()

        q1_list.rec_id = arrangement._recid
        q1_list.argtnr = arrangement.argtnr
        q1_list.arrangement = arrangement.arrangement
        q1_list.argt_bez = arrangement.argt_bez
        q1_list.artnr_logis = arrangement.artnr_logis
        q1_list.intervall = arrangement.intervall
        q1_list.argt_artikelnr = arrangement.argt_artikelnr
        q1_list.zuordnung = arrangement.zuordnung
        q1_list_list.append(q1_list)

    for q1_list in query(q1_list_list):

        argt_line_obj_list = []
        for argt_line, artikel in db_session.query(Argt_line, Artikel).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) &  (Artikel.departement == Argt_line.departement)).filter(
                (Argt_line.argtnr == q1_list.argtnr)).all():
            if argt_line._recid in argt_line_obj_list:
                continue
            else:
                argt_line_obj_list.append(argt_line._recid)

            q2_list = Q2_list()
            q2_list.rec_id = argt_line._recid
            q2_list.argtnr = argt_line.argtnr
            q2_list.departement = argt_line.departement
            q2_list.argt_artnr = argt_line.argt_artnr
            q2_list.bezeich = artikel.bezeich
            q2_list.artnr = artikel.artnr
            q2_list.betrag = argt_line.betrag
            q2_list.vt_percnt = argt_line.vt_percnt
            q2_list_list.append(q2_list)

    for hoteldpt in db_session.query(Hoteldpt).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt.num = hoteldpt.num
        t_hoteldpt_list.append(t_hoteldpt)

    return generate_output()