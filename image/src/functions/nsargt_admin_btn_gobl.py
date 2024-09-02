from functions.additional_functions import *
import decimal
from models import Arrangement, Argt_line, Artikel

def nsargt_admin_btn_gobl(p_list:[P_list], q1_recid:int, q2_recid:int, curr_select:str, argt_artnr:int, argt_dept:int, q1_list_argtnr:int, argt_price:decimal, argt_proz:decimal, comments:str):
    err = 0
    artikel_bezeich = ""
    arrangement = argt_line = artikel = None

    p_list = argtline = None

    p_list_list, P_list = create_model_like(Arrangement)

    Argtline = Argt_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err, artikel_bezeich, arrangement, argt_line, artikel
        nonlocal argtline


        nonlocal p_list, argtline
        nonlocal p_list_list
        return {"err": err, "artikel_bezeich": artikel_bezeich}

    def fill_argtline():

        nonlocal err, artikel_bezeich, arrangement, argt_line, artikel
        nonlocal argtline


        nonlocal p_list, argtline
        nonlocal p_list_list


        argt_line.argtnr = arrangement.argtnr
        argt_line.argt_artnr = argt_artnr
        argt_line.departement = argt_dept
        argt_line.betrag = argt_price


        argt_line.vt_percnt = argt_proz

    def fill_argt():

        nonlocal err, artikel_bezeich, arrangement, argt_line, artikel
        nonlocal argtline


        nonlocal p_list, argtline
        nonlocal p_list_list


        arrangement.argtnr = p_list.argtnr
        arrangement = p_list.arrangement
        arrangement.argt_bez = p_list.argt_bez
        arrangement.argt_rgbez = p_list.argt_bez
        arrangement.artnr_logis = p_list.artnr_logis
        arrangement.intervall = p_list.intervall
        arrangement.segmentcode = 1
        arrangement.zuordnung = comments

    p_list = query(p_list_list, first=True)

    if curr_select.lower()  == "ins":

        arrangement = db_session.query(Arrangement).filter(
                (Arrangement._recid == q1_recid)).first()

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == argt_artnr) &  (Artikel.artart == 0) &  (Artikel.departement == argt_dept)).first()

        if not artikel:
            err = 1

            return generate_output()

        argtline = db_session.query(Argtline).filter(
                (Argtline.argtnr == q1_list_argtnr) &  (Argtline.argt_artnr == argt_artnr) &  (Argtline.departement == argt_dept)).first()

        if argtline:
            err = 2

            return generate_output()
        argt_line = Argt_line()
        db_session.add(argt_line)

        fill_argtline()

        artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == argt_line.argt_artnr) &  (Artikel.departement == argt_line.departement)).first()
        artikel_bezeich = artikel.bezeich

    elif curr_select.lower()  == "chg2":

        argt_line = db_session.query(Argt_line).filter(
                (Argt_line._recid == q2_recid)).first()

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == argt_artnr) &  (Artikel.artart == 0) &  (Artikel.departement == argt_dept)).first()

        if not artikel:
            err = 1

            return generate_output()

        argt_line = db_session.query(Argt_line).first()
        argt_line.argt_artnr = argt_artnr
        argt_line.departement = argt_dept
        argt_line.betrag = argt_price
        argt_line.vt_percnt = argt_proz

        argt_line = db_session.query(Argt_line).first()

    elif curr_select.lower()  == "add":

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == p_list.artnr_logis) &  (Artikel.artart == 0) &  (Artikel.departement == p_list.intervall)).first()

        if not artikel:
            err = 1

            return generate_output()
        arrangement = Arrangement()
        db_session.add(arrangement)

        fill_argt()

    elif curr_select.lower()  == "chg":

        arrangement = db_session.query(Arrangement).filter(
                (Arrangement._recid == q1_recid)).first()

        arrangement = db_session.query(Arrangement).first()
        fill_argt()

        arrangement = db_session.query(Arrangement).first()

    return generate_output()