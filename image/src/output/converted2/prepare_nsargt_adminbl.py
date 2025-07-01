#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Arrangement, Artikel, Argt_line, Hoteldpt

def prepare_nsargt_adminbl():

    prepare_cache ([Arrangement, Artikel, Argt_line, Hoteldpt])

    q1_list_list = []
    q2_list_list = []
    t_hoteldpt_list = []
    arrangement = artikel = argt_line = hoteldpt = None

    q1_list = q2_list = t_hoteldpt = None

    q1_list_list, Q1_list = create_model("Q1_list", {"rec_id":int, "argtnr":int, "arrangement":string, "argt_bez":string, "artnr_logis":int, "intervall":int, "argt_artikelnr":int, "zuordnung":string})
    q2_list_list, Q2_list = create_model("Q2_list", {"rec_id":int, "argtnr":int, "departement":int, "argt_artnr":int, "bezeich":string, "artnr":int, "betrag":Decimal, "vt_percnt":Decimal})
    t_hoteldpt_list, T_hoteldpt = create_model("T_hoteldpt", {"num":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_list, q2_list_list, t_hoteldpt_list, arrangement, artikel, argt_line, hoteldpt


        nonlocal q1_list, q2_list, t_hoteldpt
        nonlocal q1_list_list, q2_list_list, t_hoteldpt_list

        return {"q1-list": q1_list_list, "q2-list": q2_list_list, "t-hoteldpt": t_hoteldpt_list}

    for arrangement in db_session.query(Arrangement).filter(
             (Arrangement.segmentcode == 1)).order_by(Arrangement.argtnr).all():
        q1_list = Q1_list()
        q1_list_list.append(q1_list)

        q1_list.rec_id = arrangement._recid
        q1_list.argtnr = arrangement.argtnr
        q1_list.arrangement = arrangement.arrangement
        q1_list.argt_bez = arrangement.argt_bez
        q1_list.artnr_logis = arrangement.artnr_logis
        q1_list.intervall = arrangement.intervall
        q1_list.argt_artikelnr = arrangement.argt_artikelnr
        q1_list.zuordnung = arrangement.zuordnung

    for q1_list in query(q1_list_list):

        argt_line_obj_list = {}
        argt_line = Argt_line()
        artikel = Artikel()
        for argt_line._recid, argt_line.argtnr, argt_line.departement, argt_line.argt_artnr, argt_line.betrag, argt_line.vt_percnt, artikel.bezeich, artikel.artnr, artikel._recid in db_session.query(Argt_line._recid, Argt_line.argtnr, Argt_line.departement, Argt_line.argt_artnr, Argt_line.betrag, Argt_line.vt_percnt, Artikel.bezeich, Artikel.artnr, Artikel._recid).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == Argt_line.departement)).filter(
                 (Argt_line.argtnr == q1_list.argtnr)).order_by(Argt_line.departement, Artikel.bezeich).all():
            if argt_line_obj_list.get(argt_line._recid):
                continue
            else:
                argt_line_obj_list[argt_line._recid] = True


            q2_list = Q2_list()
            q2_list_list.append(q2_list)

            q2_list.rec_id = argt_line._recid
            q2_list.argtnr = argt_line.argtnr
            q2_list.departement = argt_line.departement
            q2_list.argt_artnr = argt_line.argt_artnr
            q2_list.bezeich = artikel.bezeich
            q2_list.artnr = artikel.artnr
            q2_list.betrag =  to_decimal(argt_line.betrag)
            q2_list.vt_percnt =  to_decimal(argt_line.vt_percnt)

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        t_hoteldpt.num = hoteldpt.num

    return generate_output()