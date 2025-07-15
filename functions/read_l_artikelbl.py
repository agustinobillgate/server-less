#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import L_artikel

def read_l_artikelbl(case_type:int, zwkum:int, artno:int, s_artnr:int, s_bezeich:string):
    t_l_artikel_data = []
    l_artikel = None

    t_l_artikel = None

    t_l_artikel_data, T_l_artikel = create_model_like(L_artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_artikel_data, l_artikel
        nonlocal case_type, zwkum, artno, s_artnr, s_bezeich


        nonlocal t_l_artikel
        nonlocal t_l_artikel_data

        return {"t-l-artikel": t_l_artikel_data}

    def cr_l_artikel():

        nonlocal t_l_artikel_data, l_artikel
        nonlocal case_type, zwkum, artno, s_artnr, s_bezeich


        nonlocal t_l_artikel
        nonlocal t_l_artikel_data


        t_l_artikel = T_l_artikel()
        t_l_artikel_data.append(t_l_artikel)

        buffer_copy(l_artikel, t_l_artikel)


    if case_type == 1:

        l_artikel = db_session.query(L_artikel).first()

        if l_artikel:
            cr_l_artikel()
    elif case_type == 2:

        l_artikel = get_cache (L_artikel, {"zwkum": [(eq, zwkum)],"artnr": [(eq, artno)]})

        if l_artikel:

            curr_recid = l_artikel._recid
            l_artikel = db_session.query(L_artikel).filter(L_artikel._recid > curr_recid).first()

            if l_artikel:
                cr_l_artikel()
    elif case_type == 3:

        for l_artikel in db_session.query(L_artikel).filter(
                 (L_artikel.artnr >= s_artnr)).order_by(L_artikel._recid).all():
            cr_l_artikel()
    elif case_type == 4:

        for l_artikel in db_session.query(L_artikel).filter(
                 (matches(L_artikel.bezeich,(s_bezeich)))).order_by(L_artikel._recid).all():
            cr_l_artikel()
    elif case_type == 5:

        for l_artikel in db_session.query(L_artikel).filter(
                 (L_artikel.bezeich >= (s_bezeich).lower())).order_by(L_artikel._recid).all():
            cr_l_artikel()
    elif case_type == 6:

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, artno)]})

        if l_artikel:
            cr_l_artikel()
    elif case_type == 7:

        for l_artikel in db_session.query(L_artikel).order_by(L_artikel._recid).all():
            cr_l_artikel()
    elif case_type == 8:

        l_artikel = db_session.query(L_artikel).filter(
                 (not_(matches(L_artikel.bezeich,"(Don't use)*"))) & (not_(matches(L_artikel.bezeich,"(Dont use)*"))) & (not_(matches(L_artikel.bezeich,"(Don't used)*"))) & (not_(matches(L_artikel.bezeich,"(Dont used)*"))) & (not_(matches(L_artikel.bezeich,"(Don't Use )*"))) & (not_(matches(L_artikel.bezeich,"*(Don't Use)")))).first()
        while None != l_artikel:
            cr_l_artikel()

            curr_recid = l_artikel._recid
            l_artikel = db_session.query(L_artikel).filter(
                     (not_(matches(L_artikel.bezeich,"(Don't use)*"))) & (not_(matches(L_artikel.bezeich,"(Dont use)*"))) & (not_(matches(L_artikel.bezeich,"(Don't used)*"))) & (not_(matches(L_artikel.bezeich,"(Dont used)*"))) & (not_(matches(L_artikel.bezeich,"(Don't Use )*"))) & (not_(matches(L_artikel.bezeich,"*(Don't Use)"))) & (L_artikel._recid > curr_recid)).first()

    return generate_output()