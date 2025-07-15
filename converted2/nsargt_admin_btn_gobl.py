#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Arrangement, Argt_line, Artikel

p_list_data, P_list = create_model_like(Arrangement)

def nsargt_admin_btn_gobl(p_list_data:[P_list], q1_recid:int, q2_recid:int, curr_select:string, argt_artnr:int, argt_dept:int, q1_list_argtnr:int, argt_price:Decimal, argt_proz:Decimal, comments:string):

    prepare_cache ([Arrangement, Argt_line, Artikel])

    err = 0
    artikel_bezeich = ""
    arrangement = argt_line = artikel = None

    p_list = argtline = None

    Argtline = create_buffer("Argtline",Argt_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err, artikel_bezeich, arrangement, argt_line, artikel
        nonlocal q1_recid, q2_recid, curr_select, argt_artnr, argt_dept, q1_list_argtnr, argt_price, argt_proz, comments
        nonlocal argtline


        nonlocal p_list, argtline

        return {"err": err, "artikel_bezeich": artikel_bezeich}

    def fill_argtline():

        nonlocal err, artikel_bezeich, arrangement, argt_line, artikel
        nonlocal q1_recid, q2_recid, curr_select, argt_artnr, argt_dept, q1_list_argtnr, argt_price, argt_proz, comments
        nonlocal argtline


        nonlocal p_list, argtline


        argt_line.argtnr = arrangement.argtnr
        argt_line.argt_artnr = argt_artnr
        argt_line.departement = argt_dept
        argt_line.betrag =  to_decimal(argt_price)


        argt_line.vt_percnt =  to_decimal(argt_proz)


    def fill_argt():

        nonlocal err, artikel_bezeich, arrangement, argt_line, artikel
        nonlocal q1_recid, q2_recid, curr_select, argt_artnr, argt_dept, q1_list_argtnr, argt_price, argt_proz, comments
        nonlocal argtline


        nonlocal p_list, argtline


        arrangement.argtnr = p_list.argtnr
        arrangement.arrangement = p_list.arrangement
        arrangement.argt_bez = p_list.argt_bez
        arrangement.argt_rgbez = p_list.argt_bez
        arrangement.artnr_logis = p_list.artnr_logis
        arrangement.intervall = p_list.intervall
        arrangement.segmentcode = 1
        arrangement.zuordnung = comments


    p_list = query(p_list_data, first=True)

    if curr_select.lower()  == ("ins").lower() :

        arrangement = get_cache (Arrangement, {"_recid": [(eq, q1_recid)]})

        if not arrangement:

            return generate_output()

        artikel = get_cache (Artikel, {"artnr": [(eq, argt_artnr)],"artart": [(eq, 0)],"departement": [(eq, argt_dept)]})

        if not artikel:
            err = 1

            return generate_output()

        argtline = get_cache (Argt_line, {"argtnr": [(eq, q1_list_argtnr)],"argt_artnr": [(eq, argt_artnr)],"departement": [(eq, argt_dept)]})

        if argtline:
            err = 2

            return generate_output()
        argt_line = Argt_line()
        db_session.add(argt_line)

        fill_argtline()

        artikel = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})
        artikel_bezeich = artikel.bezeich

    elif curr_select.lower()  == ("chg2").lower() :

        argt_line = get_cache (Argt_line, {"_recid": [(eq, q2_recid)]})

        artikel = get_cache (Artikel, {"artnr": [(eq, argt_artnr)],"artart": [(eq, 0)],"departement": [(eq, argt_dept)]})

        if not artikel:
            err = 1

            return generate_output()
        pass
        argt_line.argt_artnr = argt_artnr
        argt_line.departement = argt_dept
        argt_line.betrag =  to_decimal(argt_price)
        argt_line.vt_percnt =  to_decimal(argt_proz)
        pass

    elif curr_select.lower()  == ("add").lower() :

        artikel = get_cache (Artikel, {"artnr": [(eq, p_list.artnr_logis)],"artart": [(eq, 0)],"departement": [(eq, p_list.intervall)]})

        if not artikel:
            err = 1

            return generate_output()
        arrangement = Arrangement()
        db_session.add(arrangement)

        fill_argt()

    elif curr_select.lower()  == ("chg").lower() :

        arrangement = get_cache (Arrangement, {"_recid": [(eq, q1_recid)]})

        if arrangement:
            pass
            fill_argt()
            pass

    return generate_output()