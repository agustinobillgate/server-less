#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_lager, Htparam, L_artikel

def prepare_initial_stockbl():

    prepare_cache ([Htparam, L_artikel])

    m_endkum = 0
    fb_date = None
    m_date = None
    t_l_lager_data = []
    temp_l_artikel_data = []
    l_lager = htparam = l_artikel = None

    temp_l_artikel = t_l_lager = None

    temp_l_artikel_data, Temp_l_artikel = create_model("Temp_l_artikel", {"artnr":int, "bezeich":string, "ek_aktuell":Decimal, "masseinheit":string, "inhalt":Decimal})
    t_l_lager_data, T_l_lager = create_model_like(L_lager)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal m_endkum, fb_date, m_date, t_l_lager_data, temp_l_artikel_data, l_lager, htparam, l_artikel


        nonlocal temp_l_artikel, t_l_lager
        nonlocal temp_l_artikel_data, t_l_lager_data

        return {"m_endkum": m_endkum, "fb_date": fb_date, "m_date": m_date, "t-l-lager": t_l_lager_data, "temp-l-artikel": temp_l_artikel_data}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 268)]})
    m_endkum = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
    fb_date = htparam.fdate
    fb_date = date_mdy(get_month(fb_date) , 1, get_year(fb_date))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
    m_date = htparam.fdate
    m_date = date_mdy(get_month(m_date) , 1, get_year(m_date))

    for l_artikel in db_session.query(L_artikel).order_by(L_artikel._recid).all():
        temp_l_artikel = Temp_l_artikel()
        temp_l_artikel_data.append(temp_l_artikel)

        temp_l_artikel.artnr = l_artikel.artnr
        temp_l_artikel.bezeich = l_artikel.bezeich
        temp_l_artikel.ek_aktuell =  to_decimal(l_artikel.ek_aktuell)
        temp_l_artikel.masseinheit = l_artikel.masseinheit
        temp_l_artikel.inhalt =  to_decimal(l_artikel.inhalt)

    for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():
        t_l_lager = T_l_lager()
        t_l_lager_data.append(t_l_lager)

        buffer_copy(l_lager, t_l_lager)

    return generate_output()